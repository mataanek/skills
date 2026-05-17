#!/usr/bin/env python3
"""
Hue Control Tools for Hermes
Registers OpenHue CLI commands as Hermes tools.
"""

import os
import subprocess

# Add the hermes-agent tools directory to the path so we can import its registry
import sys
sys.path.insert(0, '/home/mataanek/.hermes/hermes-agent/tools')
from registry import registry

# Ensure we use the correct HOME for OpenHue config
HOME = os.path.expanduser('~')
OPENHUE_CLI = os.path.join(HOME, '.hermes', 'home', '.local', 'bin', 'openhue')

def _run_openhue(args):
    """Run openhue command with proper environment."""
    env = os.environ.copy()
    env['HOME'] = HOME
    try:
        result = subprocess.run(
            [OPENHUE_CLI] + args,
            capture_output=True,
            text=True,
            env=env,
            timeout=10
        )
        if result.returncode != 0:
            return {"error": f"OpenHue CLI failed: {result.stderr}"}
        return {"output": result.stdout.strip()}
    except subprocess.TimeoutExpired:
        return {"error": "OpenHue CLI command timed out"}
    except Exception as e:
        return {"error": f"Failed to run OpenHue CLI: {str(e)}"}

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

# Register the tools with proper signatures
registry.register(
    name="hue_get_lights",
    toolset="hue",
    schema=_make_schema("hue_get_lights", "Get list of all lights with their current state", {}),
    handler=lambda args, **kw: _run_openhue(['get', 'light']),
    description="Get list of all lights with their current state"
)

registry.register(
    name="hue_get_light",
    toolset="hue",
    schema=_make_schema("hue_get_light", "Get details for a specific light by name or ID", {
        "light_identifier": {"type": "string", "description": "Light name or ID"}
    }, ["light_identifier"]),
    handler=lambda args, **kw: _run_openhue(['get', 'light', args.get('light_identifier', '')]),
    description="Get details for a specific light by name or ID"
)

registry.register(
    name="hue_set_light_state",
    toolset="hue",
    schema=_make_schema("hue_set_light_state", "Set on/off state for a light", {
        "light_identifier": {"type": "string", "description": "Light name or ID"},
        "state": {"type": "boolean", "description": "True for on, False for off"}
    }, ["light_identifier", "state"]),
    handler=lambda args, **kw: _run_openhue(['set', 'light', args.get('light_identifier', ''), '--on' if args.get('state', False) else '--off']),
    description="Set on/off state for a light"
)

registry.register(
    name="hue_set_light_brightness",
    toolset="hue",
    schema=_make_schema("hue_set_light_brightness", "Set brightness level for a light (0-100)", {
        "light_identifier": {"type": "string", "description": "Light name or ID"},
        "brightness": {"type": "integer", "minimum": 0, "maximum": 100, "description": "Brightness percentage (0-100)"}
    }, ["light_identifier", "brightness"]),
    handler=lambda args, **kw: _run_openhue(['set', 'light', args.get('light_identifier', ''), '--on', '--brightness', str(args.get('brightness', 0))]) if 0 <= args.get('brightness', 0) <= 100 else {"error": "Brightness must be between 0 and 100"},
    description="Set brightness level for a light (0-100)"
)

registry.register(
    name="hue_set_light_color",
    toolset="hue",
    schema=_make_schema("hue_set_light_color", "Set color for a light by name or hex", {
        "light_identifier": {"type": "string", "description": "Light name or ID"},
        "color": {"type": "string", "description": "Color name (red, blue, etc.) or hex code (#FF0000)"}
    }, ["light_identifier", "color"]),
    handler=lambda args, **kw: _run_openhue(['set', 'light', args.get('light_identifier', ''), '--on', '--color', args.get('color', '')]),
    description="Set color for a light by name or hex"
)

registry.register(
    name="hue_set_light_color_temperature",
    toolset="hue",
    schema=_make_schema("hue_set_light_color_temperature", "Set color temperature for a light in mirek (153-500)", {
        "light_identifier": {"type": "string", "description": "Light name or ID"},
        "temperature": {"type": "integer", "minimum": 153, "maximum": 500, "description": "Color temperature in mirek (lower=warmer, higher=cooler)"}
    }, ["light_identifier", "temperature"]),
    handler=lambda args, **kw: _run_openhue(['set', 'light', args.get('light_identifier', ''), '--on', '--temperature', str(args.get('temperature', 0))]) if 153 <= args.get('temperature', 0) <= 500 else {"error": "Color temperature must be between 153 and 500 mirek"},
    description="Set color temperature for a light in mirek (153-500)"
)

registry.register(
    name="hue_get_rooms",
    toolset="hue",
    schema=_make_schema("hue_get_rooms", "Get list of all rooms", {}),
    handler=lambda args, **kw: _run_openhue(['get', 'room']),
    description="Get list of all rooms"
)

registry.register(
    name="hue_set_room_state",
    toolset="hue",
    schema=_make_schema("hue_set_room_state", "Set on/off state for a room", {
        "room_identifier": {"type": "string", "description": "Room name or ID"},
        "state": {"type": "boolean", "description": "True for on, False for off"}
    }, ["room_identifier", "state"]),
    handler=lambda args, **kw: _run_openhue(['set', 'room', args.get('room_identifier', ''), '--on' if args.get('state', False) else '--off']),
    description="Set on/off state for a room"
)

registry.register(
    name="hue_set_room_brightness",
    toolset="hue",
    schema=_make_schema("hue_set_room_brightness", "Set brightness level for a room (0-100)", {
        "room_identifier": {"type": "string", "description": "Room name or ID"},
        "brightness": {"type": "integer", "minimum": 0, "maximum": 100, "description": "Brightness percentage (0-100)"}
    }, ["room_identifier", "brightness"]),
    handler=lambda args, **kw: _run_openhue(['set', 'room', args.get('room_identifier', ''), '--on', '--brightness', str(args.get('brightness', 0))]) if 0 <= args.get('brightness', 0) <= 100 else {"error": "Brightness must be between 0 and 100"},
    description="Set brightness level for a room (0-100)"
)

registry.register(
    name="hue_get_scenes",
    toolset="hue",
    schema=_make_schema("hue_get_scenes", "Get list of all scenes", {}),
    handler=lambda args, **kw: _run_openhue(['get', 'scene']),
    description="Get list of all scenes"
)

registry.register(
    name="hue_activate_scene",
    toolset="hue",
    schema=_make_schema("hue_activate_scene", "Activate a scene in a room", {
        "scene_name": {"type": "string", "description": "Name of the scene to activate"},
        "room_identifier": {"type": "string", "description": "Optional room name or ID"}
    }, ["scene_name"]),
    handler=lambda args, **kw: _run_openhue(['set', 'scene', args.get('scene_name', ''), '--room', args.get('room_identifier', '')] if args.get('room_identifier', '') else ['set', 'scene', args.get('scene_name', '')]),
    description="Activate a scene in a room"
)