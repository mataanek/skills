---
name: hue-control
category: smart-home
description: Control Philips Hue lights via OpenHue CLI. Provides tools for getting light status, setting on/off, brightness, color, and scenes.
version: 1.0.0
author: mataanek
tags: [smart-home, hue, lights, cli, automation]
enabled: true
---

# Hue Control Skill

Provides tools for controlling Philips Hue lighting via the OpenHue CLI. This skill registers CLI commands as Hermes tools for use by agents.

## Available Tools

- `hue_get_lights`: Get list of all lights with their current state
- `hue_get_light`: Get details for a specific light by name or ID
- `hue_set_light_state`: Set on/off state for a light
- `hue_set_light_brightness`: Set brightness level (0-100)
- `hue_set_light_color`: Set color by name or hex
- `hue_set_light_color_temperature`: Set color temperature in mirek (153-500)
- `hue_get_rooms`: Get list of all rooms
- `hue_set_room_state`: Set on/off state for a room
- `hue_set_room_brightness`: Set brightness level for a room
- `hue_get_scenes`: Get list of all scenes
- `hue_activate_scene`: Activate a scene in a room

## Usage

These tools can be called from Hermes agents, subagents, or via the terminal tool when the skill is loaded.

## Configuration

Requires the OpenHue CLI to be installed and configured with a Philips Hue Bridge.
See the `openhue` skill for installation and setup instructions.

## Tool Registration

Tools are registered via `scripts/register_hue_tools.py` which uses `tools.registry.register`.
