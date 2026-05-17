# OpenHue Troubleshooting

## Common Issues

### "openhue-cli not configured yet"\n- Run `openhue setup` and press the button on the Hue Bridge within 60 seconds.\n- Ensure the bridge is on the same local network as the machine running Hermes.\n- If you have multiple bridges, you may need to specify the IP address.\n\n### "Setup fails to detect bridge"\n- Run `openhue discover` to verify the bridge is found on the network.\n- If no IP is returned, check that the bridge is powered on, connected to the same router, and that your computer is on the same subnet.\n- Restart the bridge and router if necessary.\n- Ensure no VLAN or network isolation is separating the devices.\n\n### "Command timed out after 60s"\n- The bridge button was not pressed in time. Run setup again and press the button promptly.\n- Check network connectivity: can you ping the bridge IP?\n- Make sure no firewall is blocking communication on port 80 (HTTP) to the bridge.

### Light/room names not recognized
- Use `openhue get light` or `openhue get room` to see the exact names (case-sensitive).
- Names must match exactly as shown in the Hue app.

### Colors not working
- Only color-capable bulbs support color commands. White-only bulbs will ignore color/temperature.
- Try setting brightness first to ensure the bulb is on and responding.

## Advanced Tips

### Finding the Bridge IP
- If setup fails to auto-discover, you can find the bridge IP in your router's DHCP list or via the Hue app.
- Then you can manually set it with: `openhue setup --ip <bridge_ip>`

### Using Scenes
- Scenes are defined in the Hue app. To list them: `openhue get scene`
- Activate a scene for a room: `openhue set scene "Scene Name" --room "Room Name"`

### Automation Ideas
- Use Hermes voice commands to trigger scenes (e.g., "movie time" → set living room to movie scene).
- Combine with time-of-day or sensor data for adaptive lighting.
