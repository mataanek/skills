#!/usr/bin/env python3
"""
Daikin Control Tools for Hermes
Registers Daikin AC HTTP API commands as Hermes tools.
"""

import os
import subprocess

# Add the hermes-agent tools directory to the path so we can import its registry
import sys
sys.path.insert(0, '/home/mataanek/.hermes/hermes-agent/tools')
from registry import registry

# Daikin AC configuration
DAIKIN_IP = '192.168.178.48'
DAIKIN_BASE_URL = f'http://{DAIKIN_IP}/aircon'

def _run_daikin_get(endpoint):
    """Run Daikin GET command."""
    try:
        result = subprocess.run(
            ['curl', '-s', f'{DAIKIN_BASE_URL}/{endpoint}'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return {"error": f"Daikin API failed: {result.stderr}"}
        return {"output": result.stdout.strip()}
    except subprocess.TimeoutExpired:
        return {"error": "Daikin API command timed out"}
    except Exception as e:
        return {"error": f"Failed to call Daikin API: {str(e)}"}

def _run_daikin_set(params_dict):
    """Run Daikin SET command via GET (POST doesn't work reliably)."""
    try:
        # Build query string
        query = '&'.join([f'{k}={v}' for k, v in params_dict.items()])
        url = f'{DAIKIN_BASE_URL}/set_control_info?{query}'
        result = subprocess.run(
            ['curl', '-s', url],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return {"error": f"Daikin API failed: {result.stderr}"}
        return {"output": result.stdout.strip()}
    except subprocess.TimeoutExpired:
        return {"error": "Daikin API command timed out"}
    except Exception as e:
        return {"error": f"Failed to call Daikin API: {str(e)}"}

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
    name="daikin_get_info",
    toolset="daikin",
    schema=_make_schema("daikin_get_info", "Get current Daikin AC status", {}),
    handler=lambda args, **kw: _run_daikin_get('get_control_info'),
    description="Get current Daikin AC status"
)

registry.register(
    name="daikin_set_power",
    toolset="daikin",
    schema=_make_schema("daikin_set_power", "Set Daikin AC power on/off", {
        "power": {"type": "boolean", "description": "True for on, False for off"}
    }, ["power"]),
    handler=lambda args, **kw: _run_daikin_set({
        "pow": "1" if args.get('power', False) else "0",
        "mode": "0",  # Will be overridden by current mode in a smarter implementation
        "stemp": "23.0",
        "shum": "0",
        "f_rate": "A",
        "f_dir": "0"
    }),
    description="Set Daikin AC power on/off"
)

registry.register(
    name="daikin_set_temperature",
    toolset="daikin",
    schema=_make_schema("daikin_set_temperature", "Set Daikin AC temperature", {
        "temperature": {"type": "number", "minimum": 10, "maximum": 32, "description": "Temperature in Celsius"}
    }, ["temperature"]),
    handler=lambda args, **kw: _run_daikin_set({
        "pow": "1",
        "mode": "0",
        "stemp": str(float(args.get('temperature', 23.0))),
        "shum": "0",
        "f_rate": "A",
        "f_dir": "0"
    }),
    description="Set Daikin AC temperature"
)

registry.register(
    name="daikin_set_mode",
    toolset="daikin",
    schema=_make_schema("daikin_set_mode", "Set Daikin AC operation mode", {
        "mode": {"type": "string", "enum": ["auto", "heat", "cool", "dry", "fan"], "description": "Operation mode"}
    }, ["mode"]),
    handler=lambda args, **kw: _run_daikin_set({
        "pow": "1",
        "mode": {"auto": "0", "heat": "3", "cool": "4", "dry": "2", "fan": "1"}.get(args.get('mode', 'auto'), "0"),
        "stemp": "23.0",
        "shum": "0",
        "f_rate": "A",
        "f_dir": "0"
    }),
    description="Set Daikin AC operation mode"
)

registry.register(
    name="daikin_set_fan_rate",
    toolset="daikin",
    schema=_make_schema("daikin_set_fan_rate", "Set Daikin AC fan rate", {
        "fan_rate": {"type": "string", "enum": ["auto", "1", "2", "3", "4", "5"], "description": "Fan rate level"}
    }, ["fan_rate"]),
    handler=lambda args, **kw: _run_daikin_set({
        "pow": "1",
        "mode": "0",
        "stemp": "23.0",
        "shum": "0",
        "f_rate": args.get('fan_rate', 'auto'),
        "f_dir": "0"
    }),
    description="Set Daikin AC fan rate"
)

registry.register(
    name="daikin_set_fan_direction",
    toolset="daikin",
    schema=_make_schema("daikin_set_fan_direction", "Set Daikin AC fan direction", {
        "direction": {"type": "integer", "minimum": 0, "maximum": 5, "description": "Fan direction (0-5)"}
    }, ["direction"]),
    handler=lambda args, **kw: _run_daikin_set({
        "pow": "1",
        "mode": "0",
        "stemp": "23.0",
        "shum": "0",
        "f_rate": "A",
        "f_dir": str(args.get('direction', 0))
    }),
    description="Set Daikin AC fan direction"
)

# Enhanced humidity control functions
registry.register(
    name="daikin_get_humidity_info",
    toolset="daikin",
    schema=_make_schema("daikin_get_humidity_info", "Get detailed humidity information from Daikin AC", {}),
    handler=lambda args, **kw: _run_daikin_get('get_control_info'),
    description="Get detailed humidity information (shum, dh*, dhh, b_shum) from Daikin AC"
)

registry.register(
    name="daikin_set_humidity",
    toolset="daikin",
    schema=_make_schema("daikin_set_humidity", "Set target humidity level (if supported by unit)", {
        "humidity": {"type": "integer", "minimum": 30, "maximum": 80, "description": "Target relative humidity percentage"}
    }, ["humidity"]),
    handler=lambda args, **kw: _run_daikin_set({
        "pow": "1",
        "mode": "0",
        "stemp": "23.0",
        "shum": str(max(30, min(80, args.get('humidity', 50)))),  # shum is target humidity
        "f_rate": "A",
        "f_dir": "0"
    }),
    description="Set target humidity level (shum parameter). Note: Only works on Daikin units with humidification support."
)

registry.register(
    name="daikin_set_humidification_mode",
    toolset="daikin",
    schema=_make_schema("daikin_set_humidification_mode", "Enable/disable humidification mode", {
        "enable": {"type": "boolean", "description": "True to enable humidification, False to disable"}
    }, ["enable"]),
    handler=lambda args, **kw: _run_daikin_set({
        "pow": "1",
        "mode": "2",  # Dry mode often includes humidification/dehumidification
        "stemp": "23.0",
        "shum": "50" if args.get('enable', False) else "0",
        "f_rate": "A",
        "f_dir": "0"
    }),
    description="Enable/disable humidification mode (uses dry mode with humidity setting). Effectiveness depends on unit capabilities."
)

# Advanced: Try to detect if unit supports humidity control
registry.register(
    name="daikin_check_humidity_support",
    toolset="daikin",
    schema=_make_schema("daikin_check_humidity_support", "Check if Daikin unit appears to support humidity control", {}),
    handler=lambda args, **kw: _check_humidity_support(),
    description="Check if Daikin unit appears to support humidity control based on parameter behavior"
)

def _check_humidity_support():
    """Check if the Daikin unit shows signs of supporting humidity control."""
    import subprocess
    
    try:
        # Get baseline state
        result = subprocess.run(
            ['curl', '-s', f'{DAIKIN_BASE_URL}/get_control_info'],
            capture_output=True,
            text=True,
            timeout=10
        )
        baseline = result.stdout.strip()
        
        # Parse baseline
        params = {}
        for pair in baseline.split(','):
            if '=' in pair:
                k, v = pair.split('=', 1)
                params[k] = v
        
        # Try setting shum to a different value and see if it sticks
        test_params = params.copy()
        test_params['pow'] = '1'
        test_params['mode'] = '0'
        test_params['stemp'] = '23.0'
        test_params['shum'] = '60'  # Try setting to 60%
        test_params['f_rate'] = 'A'
        test_params['f_dir'] = '0'
        
        query = '&'.join([f'{k}={v}' for k, v in test_params.items()])
        url = f'{DAIKIN_BASE_URL}/set_control_info?{query}'
        
        result = subprocess.run(
            ['curl', '-s', url],
            capture_output=True,
            text=True,
            timeout=10
        )
        response = result.stdout.strip()
        
        # Get state after setting
        result2 = subprocess.run(
            ['curl', '-s', f'{DAIKIN_BASE_URL}/get_control_info'],
            capture_output=True,
            text=True,
            timeout=10
        )
        after_state = result2.stdout.strip()
        
        # Parse after state
        after_params = {}
        for pair in after_state.split(','):
            if '=' in pair:
                k, v = pair.split('=', 1)
                after_params[k] = v
        
        # Check if shum changed
        baseline_shum = params.get('shum', '0')
        after_shum = after_params.get('shum', '0')
        
        if baseline_shum != after_shum:
            return {"output": f"HUMIDITY_SUPPORTED: shum changed from {baseline_shum} to {after_shum}"}
        else:
            return {"output": f"HUMIDITY_NOT_SUPPORTED: shum remained {baseline_shum} (unit may not support humidity control)"}
            
    except subprocess.TimeoutExpired:
        return {"error": "Daikin API command timed out"}
    except Exception as e:
        return {"error": f"Failed to check humidity support: {str(e)}"}