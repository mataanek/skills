---
name: smart-home
description: Class-level skill for smart home device integration and control. Provides framework for adding new device types, common patterns, and best practices for Hermes agent home automation.
category: smart-home
version: 1.0.0
---

# Smart Home Integration Framework

This skill provides a class-level framework for integrating and controlling smart home devices through Hermes agents. Rather than containing specific device implementations, it establishes patterns, conventions, and best practices that device-specific skills (like hue-control, daikin-control, netatmo-control) should follow.

## Core Principles

1. **Modularity**: Each device type gets its own skill under `smart-home/` directory
2. **Consistent Interface**: All skills register tools under a common toolset prefix
3. **Environment Configuration**: Device credentials and connection details stored in `.env`
4. **Error Handling**: Graceful degradation when devices are unreachable
5. **Discovery First**: Always attempt device discovery before control operations

## Skill Structure

Each smart home device skill should follow this structure:

```
~/.hermes/skills/smart-home/<device-type>/
├── SKILL.md              # This skill documentation
├── references/           # Device-specific details, API docs, quirks
│   ├── api-endpoints.md
│   ├── authentication.md
│   └── troubleshooting.md
├── templates/            # Boilerplate configs, examples
│   ├── .env.example
│   └── config.yaml.example
└── scripts/              # Executable registration and helper scripts
    ├── register_<device>_tools.py
    ├── test_<device>_connection.py
    └── <device>_utils.py
```

## Tool Registration Patterns

All smart home skills should:

1. Register tools under a toolset named after the device type (e.g., "hue", "daikin", "netatmo")
2. Use consistent naming: `<device>_<action>` (e.g., `hue_get_light`, `daikin_set_temperature`)
3. Return structured data that can be easily parsed
4. Include comprehensive error handling with meaningful messages
5. Support both individual device control and bulk operations where applicable

### Tool Naming Convention
- `get_*` for retrieving state/status
- `set_*` for changing configuration/state
- `list_*` for enumerating multiple items (lights, rooms, scenes)
- `test_*` for connectivity/validation checks

## Environment Variables

Device credentials should be stored in `~/.hermes/.env` with this pattern:

```
# Device-specific credentials
DEVICE_TYPE_USERNAME=your_username_here
DEVICE_TYPE_PASSWORD=your_password_here
DEVICE_TYPE_CLIENT_ID=your_client_id_here  # For OAuth2 devices
DEVICE_TYPE_CLIENT_SECRET=your_client_secret_here
DEVICE_TYPE_ACCESS_TOKEN=your_access_token_here
DEVICE_TYPE_REFRESH_TOKEN=your_refresh_token_here
```

Where `DEVICE_TYPE` is uppercase version of the skill name (e.g., `HUE`, `DAIKIN`, `NETATMO`).

## Common Implementation Patterns

### 1. HTTP/API Based Devices
Most modern smart home devices use HTTP APIs. Common pattern:

```python
import os
import requests
import subprocess

def _make_api_request(endpoint, method='GET', data=None):
    """Generic API request handler with auth and error handling."""
    base_url = os.environ.get('DEVICE_TYPE_BASE_URL')
    headers = {
        'Authorization': f'Bearer {os.environ.get("DEVICE_TYPE_ACCESS_TOKEN")}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request(
            method, 
            f"{base_url}/{endpoint}", 
            headers=headers, 
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return {"output": response.json()}
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
```

### 2. CLI Tool Based Devices
For devices with command-line interfaces (like OpenHue):

```python
import os
import subprocess

def _run_device_cli(command, args=None):
    """Run device CLI command with proper environment."""
    cli_path = os.environ.get('DEVICE_TYPE_CLI_PATH', '/usr/local/bin/device-cli')
    full_cmd = [cli_path] + (command.split() if isinstance(command, str) else command)
    if args:
        full_cmd.extend(args)
    
    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return {"error": f"CLI command failed: {result.stderr}"}
        return {"output": result.stdout.strip()}
    except subprocess.TimeoutExpired:
        return {"error": "CLI command timed out"}
    except Exception as e:
        return {"error": f"CLI execution failed: {str(e)}"}
```

## Error Handling Standards

All tools should return dictionaries with either:
- `{"output": <data>}` for successful operations
- `{"error": <message>}` for failed operations

Never raise exceptions that aren't caught - all errors should be converted to the error dictionary format.

## Testing and Validation

Each skill should include:
1. Connection/test tools to verify device reachability
2. Tools to get basic device information/status
3. Gradual rollout of control functions (start with read-only)
4. Clear documentation of required permissions and capabilities

## Adding New Device Types

To add a new smart home device type:

1. Create directory: `~/.hermes/skills/smart-home/<device-type>/`
2. Create SKILL.md with device-specific documentation
3. Create implementation scripts in `scripts/`
4. Register tools following the naming conventions
5. Add any device-specific references or templates
6. Test thoroughly before considering complete

## Current Implementations

As of this session, the following device-specific skills exist under smart-home:

- **hue-control**: Philips Hue lighting control via OpenHue CLI
- **daikin-control**: Daikin air conditioning control via local HTTP API
- **netatmo-control**: Netatmo weather station data via cloud API

Each follows the patterns outlined above and can be referenced for implementation details.

## Future Extensions

This framework is designed to accommodate:
- Smart thermostats (Ecobee, Honeywell)
- Smart locks and security systems
- Smart plugs and power monitoring
- Irrigation systems
- HVAC and ventilation systems
- Home entertainment systems
- Any device with local or cloud API access

## Maintenance

When updating this framework:
1. Ensure backward compatibility with existing device skills
2. Document any changes to patterns or conventions
3. Update references with new best practices
4. Consider creating versioned approaches for breaking changes