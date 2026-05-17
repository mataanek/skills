# Philips Hue Integration Details

## Device Information
- **Brand**: Philips Hue
- **Model**: Hue Bridge (tested with IP discovery)
- **Control Method**: OpenHue CLI (`openhue` command)
- **Local API**: Yes, requires bridge button press for initial pairing

## Integration Process
1. **Install OpenHue CLI**:
   ```bash
   curl -L https://github.com/openhue/openhue-cli/releases/latest/download/openhue-linux-amd64 -o ~/.local/bin/openhue
   chmod +x ~/.local/bin/openhue
   ```

2. **Pair with Bridge**:
   ```bash
   ~/.local/bin/openhue setup
   ```
   - Press the physical button on Hue Bridge when prompted
   - Wait for "Successfully paired" message

3. **Configuration Storage**:
   - Saved to: `~/.openhue/config.yaml`
   - Format: YAML with `bridge` IP and `key` (authorization token)

## CLI Tool Usage
- `openhue get light` - List all lights with details
- `openhue set light "<light_name>" --on` - Turn light on
- `openhue set light "<light_name>" --off` - Turn light off
- `openhue set light "<light_name>" --brightness <0-100>` - Set brightness
- `openhue set light "<light_name>" --color <color_name_or_hex>` - Set color
- `openhue set light "<light_name>" --color_temp <mirek>` - Set color temperature (153-500 mirek)
- `openhue get light "<light_name>"` - Get specific light status
- `openhue get room` - List rooms
- `openhue get scene` - List scenes

## Environment Variables (for skill)
No specific env vars needed - uses local CLI with system PATH.

## Troubleshooting
- **Command not found**: Ensure `~/.local/bin` is in PATH
- **Pairing fails**: Bridge button must be pressed within ~30 seconds
- **Lights not responding**: Check bridge connectivity and power
- **Authentication expired**: Re-run `openhue setup` and press bridge button

## Light Properties Returned
Each light returns:
- ID (UUID)
- Name
- Type (e.g., "hue_play", "wall_shade")
- Status (`[on]` or `[  ]`)
- Brightness percentage
- Room assignment

## Notes
- The OpenHue CLI requires setting `HOME=/home/mataanek` for proper config location
- All lights in the test setup were reachable and responsive
- Color names supported: red, green, blue, white, yellow, purple, orange, pink
- Color temperature: 153 (warmest) to 500 (coolest) mirek