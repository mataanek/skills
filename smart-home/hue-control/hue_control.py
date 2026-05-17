#!/usr/bin/env python3
"""
Philips Hue Control Tools for Hermes Agent

Provides tools to control Philips Hue lights via OpenHue CLI.
"""

import json
import os
import subprocess
from pathlib import Path
from tools.registry import registry, ToolError


def _run_openhue(command_args):
    """Run openhue command with proper HOME environment."""
    env = os.environ.copy()
    env['HOME'] = '/home/mataanek'
    openhue_path = '/home/mataanek/.hermes/home/.local/bin/openhue'
    
    try:
        result = subprocess.run(
            [openhue_path] + command_args,
            env=env,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            raise ToolError(f"OpenHue command failed: {result.stderr}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise ToolError("OpenHue command timed out")
    except Exception as e:
        raise ToolError(f"Failed to run OpenHue: {str(e)}")


def get_lights(task_id: str = None) -> str:
    """
    Get all lights from the Hue Bridge.
    
    Args:
        task_id: Optional task ID for tracing
        
    Returns:
        JSON string of lights information
    """
    output = _run_openhue(['get', 'lights', '--json'])
    try:
        # Parse and re-format JSON for consistency
        data = json.loads(output)
        return json.dumps(data, indent=2)
    except json.JSONDecodeError:
        # Return raw output if not JSON
        return output


def get_light(light_id: str, task_id: str = None) -> str:
    """
    Get details for a specific light.
    
    Args:
        light_id: The light ID or name
        task_id: Optional task ID for tracing
        
    Returns:
        JSON string of light information
    """
    output = _run_openhue(['get', 'light', light_id, '--json'])
    try:
        data = json.loads(output)
        return json.dumps(data, indent=2)
    except json.JSONDecodeError:
        return output


def set_light_state(light_id: str, state: str, task_id: str = None) -> str:
    """
    Set the on/off state of a light.
    
    Args:
        light_id: The light ID or name
        state: 'on' or 'off'
        task_id: Optional task ID for tracing
        
    Returns:
        Success message
    """
    if state.lower() not in ['on', 'off']:
        raise ToolError("State must be 'on' or 'off'")
    
    _run_openhue(['set', 'light', light_id, '--on', state.lower()])
    return f"Light {light_id} turned {state.lower()}"


def set_light_brightness(light_id: str, brightness: int, task_id: str = None) -> str:
    """
    Set the brightness of a light.
    
    Args:
        light_id: The light ID or name
        brightness: Brightness level (0-100)
        task_id: Optional task ID for tracing
        
    Returns:
        Success message
    """
    if not 0 <= brightness <= 100:
        raise ToolError("Brightness must be between 0 and 100")
    
    _run_openhue(['set', 'light', light_id, '--brightness', str(brightness)])
    return f"Light {light_id} brightness set to {brightness}%"


def set_light_color(light_id: str, color: str, task_id: str = None) -> str:
    """
    Set the color of a light.
    
    Args:
        light_id: The light ID or name
        color: Color name or hex value (e.g., 'red', 'blue', '#FF0000')
        task_id: Optional task ID for tracing
        
    Returns:
        Success message
    """
    _run_openhue(['set', 'light', light_id, '--color', color])
    return f"Light {light_id} color set to {color}"


def activate_scene(scene_id: str, task_id: str = None) -> str:
    """
    Activate a scene.
    
    Args:
        scene_id: The scene ID or name
        task_id: Optional task ID for tracing
        
    Returns:
        Success message
    """
    _run_openhue(['set', 'scene', scene_id])
    return f"Scene {scene_id} activated"


# Register the tools
registry.register(
    name="hue-get-lights",
    toolset="smart-home",
    schema={
        "name": "hue-get-lights",
        "description": "Get all lights from the Philips Hue Bridge",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    },
    handler=lambda args, **kw: get_lights(task_id=kw.get("task_id")),
    description="Retrieve information about all Hue lights"
)

registry.register(
    name="hue-get-light",
    toolset="smart-home",
    schema={
        "name": "hue-get-light",
        "description": "Get details for a specific Hue light",
        "parameters": {
            "type": "object",
            "properties": {
                "light_id": {
                    "type": "string",
                    "description": "The light ID or name"
                }
            },
            "required": ["light_id"],
            "additionalProperties": False
        }
    },
    handler=lambda args, **kw: get_light(args.get("light_id", ""), task_id=kw.get("task_id")),
    description="Retrieve information about a specific Hue light"
)

registry.register(
    name="hue-set-light-state",
    toolset="smart-home",
    schema={
        "name": "hue-set-light-state",
        "description": "Set the on/off state of a Hue light",
        "parameters": {
            "type": "object",
            "properties": {
                "light_id": {
                    "type": "string",
                    "description": "The light ID or name"
                },
                "state": {
                    "type": "string",
                    "description": "Desired state: 'on' or 'off'"
                }
            },
            "required": ["light_id", "state"],
            "additionalProperties": False
        }
    },
    handler=lambda args, **kw: set_light_state(
        args.get("light_id", ""),
        args.get("state", ""),
        task_id=kw.get("task_id")
    ),
    description="Turn a Hue light on or off"
)

registry.register(
    name="hue-set-light-brightness",
    toolset="smart-home",
    schema={
        "name": "hue-set-light-brightness",
        "description": "Set the brightness of a Hue light",
        "parameters": {
            "type": "object",
            "properties": {
                "light_id": {
                    "type": "string",
                    "description": "The light ID or name"
                },
                "brightness": {
                    "type": "integer",
                    "description": "Brightness level (0-100)",
                    "minimum": 0,
                    "maximum": 100
                }
            },
            "required": ["light_id", "brightness"],
            "additionalProperties": False
        }
    },
    handler=lambda args, **kw: set_light_brightness(
        args.get("light_id", ""),
        args.get("brightness", 0),
        task_id=kw.get("task_id")
    ),
    description="Set brightness level of a Hue light"
)

registry.register(
    name="hue-set-light-color",
    toolset="smart-home",
    schema={
        "name": "hue-set-light-color",
        "description": "Set the color of a Hue light",
        "parameters": {
            "type": "object",
            "properties": {
                "light_id": {
                    "type": "string",
                    "description": "The light ID or name"
                },
                "color": {
                    "type": "string",
                    "description": "Color name or hex value (e.g., 'red', '#FF0000')"
                }
            },
            "required": ["light_id", "color"],
            "additionalProperties": False
        }
    },
    handler=lambda args, **kw: set_light_color(
        args.get("light_id", ""),
        args.get("color", ""),
        task_id=kw.get("task_id")
    ),
    description="Set color of a Hue light"
)

registry.register(
    name="hue-activate-scene",
    toolset="smart-home",
    schema={
        "name": "hue-activate-scene",
        "description": "Activate a Hue scene",
        "parameters": {
            "type": "object",
            "properties": {
                "scene_id": {
                    "type": "string",
                    "description": "The scene ID or name"
                }
            },
            "required": ["scene_id"],
            "additionalProperties": False
        }
    },
    handler=lambda args, **kw: activate_scene(
        args.get("scene_id", ""),
        task_id=kw.get("task_id")
    ),
    description="Activate a predefined Hue scene"
)