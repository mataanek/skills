# Daikin Air Conditioner Integration Details

## Device Information
- **Brand**: Daikin Industries
- **Model**: WiFi-enabled AC unit (tested with local HTTP API)
- **Control Method**: Local HTTP API endpoints
- **Local API**: Yes, direct IP-based control (no cloud required for basic functions)

## API Endpoints
Base URL: `http://<DEVICE_IP>/aircon`

### Get Control Information
- **Endpoint**: `/aircon/get_control_info`
- **Method**: GET
- **Response**: CSV-like string of parameters
- **Parameters**:
  - `ret`: Return status (OK/ERROR)
  - `pow`: Power state (0=off, 1=on)
  - `mode`: Operation mode (0=auto, 1=heat, 2=cool/dry, 3=heat, 4=cool, 5=fan, 6=?, 7=auto/heat?)
  - `stemp`: Set temperature (value or "M" for manual)
  - `shum`: Target humidity (0-100%, 0=off/humidification disabled)
  - `f_rate`: Fan rate ("A"=auto, "1"-"5"=speed levels)
  - `f_dir`: Fan direction (0-5, 0=vertical swing)
  - `dt1-dt7`: Temperature sensors
  - `dh1-dh7`: Humidity sensors
  - `dhh`: Humidity hysteresis/target
  - `b_*`: Backup values
  - `alert`: Alert status (255=no alert)

### Set Control Information
- **Endpoint**: `/aircon/set_control_info`
- **Method**: GET (POST doesn't work reliably on tested unit)
- **Parameters**: Same as get_control_info, all required
- **Critical Note**: All parameters must be included in each request, even if not changing

## Parameter Values Reference

### Mode Values:
- 0: Auto
- 1: Heat
- 2: Cool/Dry (context dependent)
- 3: Heat
- 4: Cool
- 5: Fan only
- 6: Unknown/undocumented
- 7: Auto/Heat (observed in testing)

### Fan Rate Values:
- "A": Auto
- "1"-"5": Manual speed levels (1=lowest, 5=highest)

### Fan Direction Values:
- 0: Vertical swing (up/down)
- 1: Position 1 (most upward)
- 2: Position 2
- 3: Position 3 (middle)
- 4: Position 4
- 5: Position 5 (most downward)
- Note: Some units may have different mappings

### Temperature:
- Range: 10.0 to 32.0°C
- Can be set to specific value or "M" for manual mode

### Humidity (shum):
- Range: 0-100% (0=humidification off)
- Note: Some units enforce minimum ~30% to prevent over-drying
- Values outside 30-80% may be clamped or rejected

## Integration Process
1. **Find Device IP**: Check router DHCP list or use network scanning
2. **Verify Connectivity**: `curl http://<IP>/aircon/get_control_info`
3. **Test Control**: Send parameter changes via GET to `/aircon/set_control_info`
4. **Note**: All parameters must be included in each set request

## CLI Tool Usage (via curl)
- Get status: `curl -s http://<IP>/aircon/get_control_info`
- Set power on: `curl -s "http://<IP>/aircon/set_control_info?pow=1&mode=0&stemp=23.0&shum=0&f_rate=A&f_dir=0"`
- Set power off: `curl -s "http://<IP>/aircon/set_control_info?pow=0&mode=0&stemp=23.0&shum=0&f_rate=A&f_dir=0"`
- Set temperature: `curl -s "http://<IP>/aircon/set_control_info?pow=1&mode=0&stemp=22.0&shum=0&f_rate=A&f_dir=0"`
- Set humidity: `curl -s "http://<IP>/aircon/set_control_info?pow=1&mode=0&stemp=23.0&shum=50&f_rate=A&f_dir=0"`

## Environment Variables (for skill)
No specific env vars needed for basic operation - uses direct IP in skill code.
For enhanced flexibility, could support:
- `DAIKIN_IP`: Device IP address
- `DAIKIN_BASE_URL`: Full base URL

## Troubleshooting
- **Connection refused**: Verify device IP and network connectivity
- **Parameter errors**: Ensure all 6 required parameters are included (pow, mode, stemp, shum, f_rate, f_dir)
- **Unreachable device**: Check if device is powered and on network
- **Unexpected mode behavior**: Mode mapping may vary by firmware/model
- **Humidity limits**: Unit may enforce minimum humidity to prevent compressor damage

## Response Format
Parameters returned as comma-separated key=value pairs:
`ret=OK,pow=0,mode=1,adv=,stemp=23.0,shum=0,dt1=23.0,dt2=M,dt3=23.0,dt4=23.0,dt5=23.0,dt7=23.0,dh1=0,dh2=0,dh3=0,dh4=0,dh5=0,dh7=0,dhh=50,b_mode=1,b_stemp=23.0,b_shum=0,alert=255,f_rate=A,b_f_rate=A,dfr1=A,dfr2=A,dfr3=A,dfr4=A,dfr5=A,dfr6=A,dfr7=A,dfrh=A,f_dir=0,b_f_dir=0,dfd1=0,dfd2=0,dfd3=0,dfd4=0,dfd5=0,dfd6=0,dfd7=0,dfdh=0`

## Notes
- Tested unit required ALL parameters in set_control_info requests
- Omitting any parameter resulted in "PARAM NG" error
- Mode values may vary by device model/firmware
- Humidity control effectiveness depends on specific unit capabilities (humidification/dehumidification)
- Backup values (b_*) appear to mirror current settings after successful changes