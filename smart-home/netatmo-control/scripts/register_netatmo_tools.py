#!/usr/bin/env python3
"""
Netatmo Control Tools for Hermes
Registers Netatmo Weather Station API commands as Hermes tools.
"""

import os
import time
import json
import base64
import requests

# Add the hermes-agent tools directory to the path so we can import its registry
import sys
sys.path.insert(0, '/home/mataanek/.hermes/hermes-agent/tools')
from registry import registry

# Netatmo API configuration
NETATMO_TOKEN_URL = 'https://api.netatmo.com/oauth2/token'
NETATMO_API_URL = 'https://api.netatmo.com/api'

def _get_netatmo_credentials():
    """Get Netatmo credentials from environment."""
    return {
        'username': os.environ.get('NETATMO_USERNAME'),
        'password': os.environ.get('NETATMO_PASSW'),
        'client_id': os.environ.get('NETATMO_CLIENT_ID'),
        'client_secret': os.environ.get('NETATMO_CLIENT_SECRET')
    }

def _get_stored_tokens():
    """Get stored tokens from environment."""
    return {
        'access_token': os.environ.get('NETATMO_ACCESS_TOKEN'),
        'refresh_token': os.environ.get('NETATMO_REFRESH_TOKEN')
    }

def _save_tokens_to_env(access_token, refresh_token=None):
    """Save tokens to .env file (requires file rewrite)."""
    env_file = '/home/mataanek/.hermes/.env'
    try:
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Update or add token lines
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('NETATMO_ACCESS_TOKEN='):
                lines[i] = f'NETATMO_ACCESS_TOKEN={access_token}\n'
                updated = True
                break
        if not updated:
            lines.append(f'NETATMO_ACCESS_TOKEN={access_token}\n')
        
        if refresh_token:
            updated = False
            for i, line in enumerate(lines):
                if line.startswith('NETATMO_REFRESH_TOKEN='):
                    lines[i] = f'NETATMO_REFRESH_TOKEN={refresh_token}\n'
                    updated = True
                    break
            if not updated:
                lines.append(f'NETATMO_REFRESH_TOKEN={refresh_token}\n')
        
        with open(env_file, 'w') as f:
            f.writelines(lines)
            
        # Update current environment
        os.environ['NETATMO_ACCESS_TOKEN'] = access_token
        if refresh_token:
            os.environ['NETATMO_REFRESH_TOKEN'] = refresh_token
            
        return True
    except Exception as e:
        print(f"Error saving tokens to .env: {e}")
        return False

def _refresh_access_token():
    """Refresh the access token using refresh token."""
    creds = _get_netatmo_credentials()
    tokens = _get_stored_tokens()
    
    if not creds['client_id'] or not creds['client_secret'] or not tokens['refresh_token']:
        return {"error": "Missing credentials for token refresh"}
    
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': tokens['refresh_token'],
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret']
    }
    
    try:
        response = requests.post(NETATMO_TOKEN_URL, data=data, timeout=10)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            refresh_token = token_data.get('refresh_token', tokens['refresh_token'])  # Keep old if not provided
            
            if _save_tokens_to_env(access_token, refresh_token):
                return {"access_token": access_token}
            else:
                return {"error": "Failed to save refreshed tokens"}
        else:
            return {"error": f"Token refresh failed: {response.status_code} {response.text}"}
    except Exception as e:
        return {"error": f"Token refresh request failed: {str(e)}"}

def _get_valid_access_token():
    """Get a valid access token, refreshing if necessary."""
    tokens = _get_stored_tokens()
    access_token = tokens['access_token']
    
    # If we have no token, try to get one via password grant
    if not access_token:
        return _get_access_token_via_password()
    
    # For now, we'll assume tokens are valid and let API calls fail if expired
    # In a production system, we'd check expiration time
    return {"access_token": access_token}

def _get_access_token_via_password():
    """Get access token using password grant type."""
    creds = _get_netatmo_credentials()
    
    if not all([creds['username'], creds['password'], creds['client_id'], creds['client_secret']]):
        return {"error": "Missing credentials for password grant"}
    
    data = {
        'grant_type': 'password',
        'username': creds['username'],
        'password': creds['password'],
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'scope': 'read_station'
    }
    
    try:
        response = requests.post(NETATMO_TOKEN_URL, data=data, timeout=10)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            refresh_token = token_data.get('refresh_token')
            
            if access_token and _save_tokens_to_env(access_token, refresh_token):
                return {"access_token": access_token}
            else:
                return {"error": "Failed to save tokens from password grant"}
        else:
            return {"error": f"Password grant failed: {response.status_code} {response.text}"}
    except Exception as e:
        return {"error": f"Password grant request failed: {str(e)}"}

def _make_netatmo_request(endpoint, params=None):
    """Make a request to Netatmo API with proper authentication."""
    # Get valid token
    token_result = _get_valid_access_token()
    if "error" in token_result:
        return token_result
    
    access_token = token_result["access_token"]
    
    # Make the API request
    url = f"{NETATMO_API_URL}/{endpoint}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return {"output": response.json()}
        elif response.status_code == 401:
            # Token might be expired, try to refresh once
            refresh_result = _refresh_access_token()
            if "error" not in refresh_result:
                # Retry with new token
                access_token = refresh_result["access_token"]
                headers['Authorization'] = f'Bearer {access_token}'
                response = requests.get(url, headers=headers, params=params, timeout=10)
                if response.status_code == 200:
                    return {"output": response.json()}
                else:
                    return {"error": f"API request failed after token refresh: {response.status_code} {response.text}"}
            else:
                return {"error": f"API request failed (401) and token refresh failed: {refresh_result.get('error')}"}
        else:
            return {"error": f"API request failed: {response.status_code} {response.text}"}
    except Exception as e:
        return {"error": f"API request exception: {str(e)}"}

# Define a helper to create a basic schema for our tools
def _make_schema(name, description, properties, required=None):
    if required is None:
        required = []
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required
        }
    }

# Register the tools
registry.register(
    name="netatmo_get_stations",
    toolset="netatmo",
    schema=_make_schema("netatmo_get_stations", "Get all Netatmo stations and modules", {}),
    handler=lambda args, **kw: _make_netatmo_request('getstationsdata'),
    description="Get all Netatmo stations and modules data"
)

registry.register(
    name="netatmo_get_device_measures",
    toolset="netatmo",
    schema=_make_schema("netatmo_get_device_measures", "Get measurements for a specific device", {
        "device_id": {"type": "string", "description": "Device ID (station or module)"},
        "scale": {"type": "string", "enum": ["max", "30min", "3hour", "day", "week", "month", "year"], "description": "Time scale for measurements"},
        "type": {"type": "string", "description": "Comma-separated list of measures to get (e.g., Temperature,Humidity,CO2,Pressure,Noise)"},
        "date_end": {"type": "integer", "description": "End timestamp (Unix timestamp), default now"},
        "date_begin": {"type": "integer", "description": "Start timestamp (Unix timestamp), default 1 hour ago"},
        "limit": {"type": "integer", "minimum": 1, "maximum": 1024, "description": "Number of measures to return (default 1)"}
    }, ["device_id"]),
    handler=lambda args, **kw: _make_netatmo_request('getmeasure', {
        'device_id': args.get('device_id'),
        'scale': args.get('scale', 'max'),
        'type': args.get('type', 'Temperature,Humidity,CO2,Pressure,Noise'),
        'date_end': args.get('date_end'),
        'date_begin': args.get('date_begin'),
        'limit': args.get('limit', 1)
    }),
    description="Get measurements for a specific Netatmo device"
)

# Convenience tools for common use cases
registry.register(
    name="netatmo_get_outdoor_data",
    toolset="netatmo",
    schema=_make_schema("netatmo_get_outdoor_data", "Get current outdoor measurements", {}),
    handler=lambda args, **kw: _make_netatmo_request('getstationsdata'),
    description="Get current outdoor measurements from Netatmo Weather Station"
)

registry.register(
    name="netatmo_get_indoor_data",
    toolset="netatmo",
    schema=_make_schema("netatmo_get_indoor_data", "Get current indoor measurements from the main module", {}),
    handler=lambda args, **kw: _make_netatmo_request('getstationsdata'),
    description="Get current indoor measurements from Netatmo main module"
)

registry.register(
    name="netatmo_get_module_data",
    toolset="netatmo",
    schema=_make_schema("netatmo_get_module_data", "Get current measurements from a specific module", {
        "module_id": {"type": "string", "description": "Module ID (e.g., bedroom module)"}
    }, ["module_id"]),
    handler=lambda args, **kw: _make_netatmo_request('getstationsdata'),
    description="Get current measurements from a specific Netatmo module"
)

# Helper to parse and format Netatmo data
def _format_netatmo_stations_data(raw_data):
    """Format Netatmo stations data into a readable format."""
    if "error" in raw_data:
        return raw_data
    
    try:
        data = raw_data.get("output", {}).get("body", {})
        if not data:
            return {"error": "No data in response"}
        
        formatted = {
            "status": "ok",
            "timestamp": data.get("time_utc"),
            "stations": []
        }
        
        for station in data.get("devices", []):
            station_info = {
                "station_id": station.get("_id"),
                "station_name": station.get("station_name"),
                "place": f"{station.get('place', {}).get('city', '')} {station.get('place', {}).get('country', '')}".strip(),
                "modules": []
            }
            
            # Main module data
            if "dashboard_data" in station:
                dashboard = station["dashboard_data"]
                station_info["main_module"] = {
                    "temperature": dashboard.get("Temperature"),
                    "humidity": dashboard.get("Humidity"),
                    "pressure": dashboard.get("Pressure"),
                    "co2": dashboard.get("CO2"),
                    "noise": dashboard.get("Noise"),
                    "min_temp": dashboard.get("min_temp"),
                    "max_temp": dashboard.get("max_temp"),
                    "temp_trend": dashboard.get("temp_trend"),
                    "pressure_trend": dashboard.get("pressure_trend"),
                    "humidity_trend": dashboard.get("hum_trend"),
                    "co2_trend": dashboard.get("co2_trend"),
                    "wifi_status": dashboard.get("wifi_status"),
                    "rf_status": dashboard.get("rf_status"),
                    "battery_percent": dashboard.get("battery_percent"),
                    "battery_vp": dashboard.get("battery_vp"),
                    "last_updated": dashboard.get("time_utc")
                }
            
            # Additional modules
            for module in station.get("modules", []):
                module_info = {
                    "module_id": module.get("_id"),
                    "module_name": module.get("module_name"),
                    "module_type": module.get("type")
                }
                
                if "dashboard_data" in module:
                    dashboard = module["dashboard_data"]
                    module_info["data"] = {
                        "temperature": dashboard.get("Temperature"),
                        "humidity": dashboard.get("Humidity"),
                        "pressure": dashboard.get("Pressure"),
                        "co2": dashboard.get("CO2"),
                        "noise": dashboard.get("Noise"),
                        "rain": dashboard.get("Rain"),
                        "sum_rain_1": dashboard.get("sum_rain_1"),
                        "sum_rain_24": dashboard.get("sum_rain_24"),
                        "sum_rain_7": dashboard.get("sum_rain_7"),
                        "min_temp": dashboard.get("min_temp"),
                        "max_temp": dashboard.get("max_temp"),
                        "temp_trend": dashboard.get("temp_trend"),
                        "pressure_trend": dashboard.get("pressure_trend"),
                        "humidity_trend": dashboard.get("hum_trend"),
                        "last_updated": dashboard.get("time_utc")
                    }
                
                station_info["modules"].append(module_info)
            
            formatted["stations"].append(station_info)
        
        return {"output": formatted}
    except Exception as e:
        return {"error": f"Failed to format Netatmo data: {str(e)}"}

# Register formatted data tools
registry.register(
    name="netatmo_get_formatted_stations",
    toolset="netatmo",
    schema=_make_schema("netatmo_get_formatted_stations", "Get formatted Netatmo stations data", {}),
    handler=lambda args, **kw: _format_netatmo_stations_data(_make_netatmo_request('getstationsdata')),
    description="Get formatted Netatmo stations data with station/module structure"
)

registry.register(
    name="netatmo_get_formatted_outdoor",
    toolset="netatmo",
    schema=_make_schema("netatmo_get_formatted_outdoor", "Get formatted outdoor measurements", {}),
    handler=lambda args, **kw: _format_netatmo_stations_data(_make_netatmo_request('getstationsdata')),
    description="Get formatted outdoor measurements from Netatmo Weather Station"
)

registry.register(
    name="netatmo_get_formatted_indoor",
    toolset="netatmo",
    schema=_make_schema("netatmo_get_formatted_indoor", "Get formatted indoor measurements from main module", {}),
    handler=lambda args, **kw: _format_netatmo_stations_data(_make_netatmo_request('getstationsdata')),
    description="Get formatted indoor measurements from Netatmo main module"
)