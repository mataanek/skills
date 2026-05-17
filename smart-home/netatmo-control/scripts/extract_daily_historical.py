#!/usr/bin/env python3
"""
Netatmo Daily Historical Extraction Script
Extracts last 24 hours of historical data for Netatmo main module at 30-minute intervals.
Designed to run once daily via cron.
"""

import os
import sys
import json
from datetime import datetime, timezone, timedelta

# Add paths for hermes tools and skill scripts
hermes_tools_path = '/home/mataanek/.hermes/hermes-agent/tools'
skill_script_path = '/home/mataanek/.hermes/skills/smart-home/netatmo-control/scripts'

if hermes_tools_path not in sys.path:
    sys.path.insert(0, hermes_tools_path)
if skill_script_path not in sys.path:
    sys.path.insert(0, skill_script_path)

# Load environment variables from .env
env_file = '/home/mataanek/.hermes/.env'
if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

def main():
    try:
        # Import hermes tools
        from registry import registry
        
        # Execute the Netatmo registration script to load tools
        skill_script = '/home/mataanek/.hermes/skills/smart-home/netatmo-control/scripts/register_netatmo_tools.py'
        with open(skill_script, 'r') as f:
            script_content = f.read()
        exec(script_content, globals())
        
        # Configuration
        TARGET_STATION_ID = '70:ee:50:c2:2c:ee'
        WIKI_PATH = os.environ.get('WIKI_PATH', '/home/mataanek/.hermes/wiki')
        SMART_HOME_DIR = os.path.join(WIKI_PATH, 'smart_home')
        DATA_DIR = os.path.join(SMART_HOME_DIR, 'netatmo')
        HISTORY_DIR = os.path.join(DATA_DIR, 'historical')
        
        # Ensure directories exist
        os.makedirs(HISTORY_DIR, exist_ok=True)
        
        # Get station info to confirm we can access the main module
        result = registry.dispatch('netatmo_get_stations', {})
        if 'output' not in result:
            print(f"ERROR: Failed to get stations data: {result}")
            return 1
        
        data = result['output']
        if 'body' not in data or 'devices' not in data['body']:
            print("ERROR: Invalid data structure from Netatmo")
            return 1
        
        devices = data['body']['devices']
        target_device = None
        for device in devices:
            if device.get('_id') == TARGET_STATION_ID:
                target_device = device
                break
        
        if not target_device:
            print(f"ERROR: Station {TARGET_STATION_ID} not found")
            return 1
        
        # Extract last day of data with 30-minute intervals
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=1)  # Last 24 hours
        date_begin = int(start_date.timestamp())
        date_end = int(end_date.timestamp())
        
        # Metrics to extract for the main module
        metrics = ['Temperature', 'Humidity', 'Pressure', 'CO2', 'Noise']
        
        def parse_netatmo_measurements(raw_data):
            """Parse Netatmo getmeasure response into a list of {timestamp, value} dicts."""
            parsed = []
            if not isinstance(raw_data, list):
                return parsed
            
            for bucket in raw_data:
                if not isinstance(bucket, dict):
                    continue
                beg_time = bucket.get('beg_time')
                step_time = bucket.get('step_time')
                values = bucket.get('value', [])
                
                if beg_time is None or step_time is None:
                    continue
                    
                # Each value in the bucket corresponds to a timestamp
                # The first value is at beg_time, second at beg_time + step_time, etc.
                for i, value_array in enumerate(values):
                    if not isinstance(value_array, list) or len(value_array) == 0:
                        continue
                    # Take the first value (Netatmo usually returns single-value arrays)
                    timestamp = beg_time + (i * step_time)
                    value = value_array[0]  # First element
                    parsed.append({
                        'timestamp': timestamp,
                        'datetime': datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat(),
                        'value': value
                    })
            
            return parsed
        
        success_count = 0
        total_data_points = 0
        
        print(f"Extracting last day of historical data for station {target_device.get('station_name')}...")
        
        for metric in metrics:
            try:
                # Prepare parameters for getmeasure
                params = {
                    'device_id': TARGET_STATION_ID,  # Main module uses station ID
                    'scale': '30min',  # 30-minute intervals
                    'type': metric,
                    'date_begin': date_begin,
                    'date_end': date_end,
                    'limit': 1024  # Max allowed
                }
                
                # Call the tool via registry
                result = registry.dispatch('netatmo_get_device_measures', params)
                
                if 'output' in result:
                    data_payload = result['output']
                    # Check if we got data
                    if isinstance(data_payload, dict) and 'body' in data_payload:
                        body = data_payload['body']
                        if isinstance(body, list):
                            # Parse the measurements
                            parsed_data = parse_netatmo_measurements(body)
                            
                            if parsed_data:
                                # Prepare data to store
                                filename = f"{TARGET_STATION_ID}_main_{metric}_historical_1d.json"
                                filepath = os.path.join(HISTORY_DIR, filename)
                                
                                stored_data = {
                                    'station_id': TARGET_STATION_ID,
                                    'station_name': target_device.get('station_name'),
                                    'module_id': 'main',
                                    'module_name': target_device.get('module_name'),
                                    'module_type': 'NAMain',
                                    'metric': metric,
                                    'date_begin': date_begin,
                                    'date_end': date_end,
                                    'scale': '30min',
                                    'retrieved_at': datetime.now(timezone.utc).isoformat(),
                                    'data_points': len(parsed_data),
                                    'data': parsed_data  # Already parsed timestamp-value pairs
                                }
                                
                                with open(filepath, 'w') as f:
                                    json.dump(stored_data, f, indent=2)
                                
                                print(f"  ✓ {metric}: saved {len(parsed_data)} data points")
                                success_count += 1
                                total_data_points += len(parsed_data)
                            else:
                                print(f"  ⚠ {metric}: no data points after parsing")
                        else:
                            print(f"  ⚠ {metric}: unexpected body format: {type(body)}")
                    else:
                        print(f"  ⚠ {metric}: unexpected response structure")
                else:
                    error_msg = result.get('error', 'Unknown error')
                    print(f"  ❌ {metric}: failed to get data: {error_msg}")
                    
            except Exception as e:
                print(f"  ❌ {metric}: exception: {e}")
        
        print(f"\nSummary:")
        print(f"  Successful metric extractions: {success_count}/{len(metrics)}")
        print(f"  Total data points collected: {total_data_points}")
        print(f"  Expected: ~48 points per metric (24 hours × 2 per hour)")
        
        return 0 if success_count > 0 else 1
        
    except Exception as e:
        print(f"ERROR: Exception in Netatmo daily historical extraction: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())