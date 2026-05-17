#!/usr/bin/env python3
"""
Netatmo Data Collection Script for Cron
Collects Netatmo weather station data and stores it in the Hermes wiki for long-term trends.
"""

import os
import sys
import json
from datetime import datetime, timezone

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
        WIKI_PATH = os.environ.get('WIKI_PATH', '/home/mataanek/.hermes/wiki')
        SMART_HOME_DIR = os.path.join(WIKI_PATH, 'smart_home')
        DATA_DIR = os.path.join(SMART_HOME_DIR, 'netatmo')
        LOG_FILE = os.path.join(DATA_DIR, 'sensor_log.jsonl')
        TARGET_STATION_ID = '70:ee:50:c2:2c:ee'
        
        # Ensure directories exist
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Fetch current data from Netatmo
        result = registry.dispatch('netatmo_get_stations', {})
        if 'output' not in result:
            print(f"ERROR: Failed to get stations data: {result}")
            return 1
        
        data = result['output']
        if 'body' not in data or 'devices' not in data['body']:
            print("ERROR: Invalid data structure from Netatmo")
            return 1
        
        # Find the target station
        devices = data['body']['devices']
        target_device = None
        for device in devices:
            if device.get('_id') == TARGET_STATION_ID:
                target_device = device
                break
        
        if not target_device:
            print(f"ERROR: Target station {TARGET_STATION_ID} not found")
            return 1
        
        # Extract and structure the data
        timestamp = datetime.now(timezone.utc).isoformat()
        
        structured_data = {
            "timestamp": timestamp,
            "station_id": target_device.get('_id'),
            "station_name": target_device.get('station_name'),
            "modules": []
        }
        
        # Process main module
        if 'dashboard_data' in target_device:
            main_module = {
                "module_id": "main",
                "module_name": target_device.get('module_name', 'Main Module'),
                "module_type": "NAMain",
                "data": {}
            }
            dashboard = target_device['dashboard_data']
            if 'Temperature' in dashboard:
                main_module['data']['temperature_c'] = dashboard['Temperature']
            if 'Humidity' in dashboard:
                main_module['data']['humidity_percent'] = dashboard['Humidity']
            if 'Pressure' in dashboard:
                main_module['data']['pressure_hpa'] = dashboard['Pressure']
            if 'CO2' in dashboard:
                main_module['data']['co2_ppm'] = dashboard['CO2']
            if 'Noise' in dashboard:
                main_module['data']['noise_db'] = dashboard['Noise']
            if 'time_utc' in dashboard:
                main_module['data']['last_updated_utc'] = dashboard['time_utc']
            
            structured_data['modules'].append(main_module)
        
        # Process additional modules
        for module in target_device.get('modules', []):
            module_data = {
                "module_id": module.get('_id'),
                "module_name": module.get('module_name'),
                "module_type": module.get('type'),
                "data": {}
            }
            if 'dashboard_data' in module:
                dashboard = module['dashboard_data']
                if 'Temperature' in dashboard:
                    module_data['data']['temperature_c'] = dashboard['Temperature']
                if 'Humidity' in dashboard:
                    module_data['data']['humidity_percent'] = dashboard['Humidity']
                if 'Pressure' in dashboard:
                    module_data['data']['pressure_hpa'] = dashboard['Pressure']
                if 'CO2' in dashboard:
                    module_data['data']['co2_ppm'] = dashboard['CO2']
                if 'Noise' in dashboard:
                    module_data['data']['noise_db'] = dashboard['Noise']
                if 'Rain' in dashboard:
                    module_data['data']['rain_mm'] = dashboard['Rain']
                if 'time_utc' in dashboard:
                    module_data['data']['last_updated_utc'] = dashboard['time_utc']
            
            structured_data['modules'].append(module_data)
        
        # Store the data
        timestamp_dt = datetime.now(timezone.utc)
        date_str = timestamp_dt.strftime('%Y-%m-%d')
        time_str = timestamp_dt.strftime('%H:%M:%S')
        
        # 1. Append to JSON Lines log file
        log_entry = {
            "timestamp": structured_data['timestamp'],
            "date": date_str,
            "time": time_str,
            "station_id": structured_data['station_id'],
            "station_name": structured_data['station_name'],
            "modules": structured_data['modules']
        }
        
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # 2. Create/update individual sensor files
        files_updated = 0
        for module in structured_data['modules']:
            module_id = module['module_id']
            module_name = module['module_name'].replace(' ', '_').replace('/', '_')
            
            for metric_name, metric_value in module['data'].items():
                if metric_value is None:
                    continue
                    
                filename = f"{structured_data['station_id']}_{module_id}_{metric_name}.json"
                filepath = os.path.join(DATA_DIR, filename)
                
                # Read existing data
                existing_data = []
                if os.path.exists(filepath):
                    try:
                        with open(filepath, 'r') as f:
                            existing_data = json.load(f)
                        if not isinstance(existing_data, list):
                            existing_data = [existing_data]
                    except:
                        existing_data = []
                
                # Add new data point
                new_point = {
                    "timestamp": structured_data['timestamp'],
                    "date": date_str,
                    "time": time_str,
                    "value": metric_value
                }
                existing_data.append(new_point)
                
                # Keep only last 1000 entries
                if len(existing_data) > 1000:
                    existing_data = existing_data[-1000:]
                
                # Write back
                with open(filepath, 'w') as f:
                    json.dump(existing_data, f, indent=2)
                files_updated += 1
        
        # 3. Update daily summary
        daily_summary_file = os.path.join(DATA_DIR, f"daily_summary_{date_str}.json")
        try:
            with open(daily_summary_file, 'r') as f:
                daily_summary = json.load(f)
            if not isinstance(daily_summary, list):
                daily_summary = []
        except:
            daily_summary = []
        
        # Add today's latest readings
        latest_readings = {
            "timestamp": structured_data['timestamp'],
            "time": time_str,
            "readings": {}
        }
        
        for module in structured_data['modules']:
            module_prefix = f"{module['module_name'].replace(' ', '_')}"
            for metric_name, metric_value in module['data'].items():
                if metric_value is not None:
                    key = f"{module_prefix}_{metric_name}"
                    latest_readings["readings"][key] = metric_value
        
        daily_summary.append(latest_readings)
        
        # Keep only last 48 hours of summaries (assuming 5-min intervals = 576 entries)
        if len(daily_summary) > 576:
            daily_summary = daily_summary[-576:]
        
        with open(daily_summary_file, 'w') as f:
            json.dump(daily_summary, f, indent=2)
        
        # Success message (will go to cron logs)
        print(f"SUCCESS: Collected Netatmo data for {structured_data['station_name']}")
        print(f"  Modules: {len(structured_data['modules'])}")
        print(f"  Files updated: {files_updated}")
        print(f"  Timestamp: {structured_data['timestamp']}")
        
        return 0
        
    except Exception as e:
        print(f"ERROR: Exception in Netatmo data collection: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())