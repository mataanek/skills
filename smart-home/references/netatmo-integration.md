# Netatmo Weather Station Integration Details

## Device Information
- **Brand**: Netatmo
- **Model**: Smart Weather Station (includes outdoor module and indoor modules)
- **Control Method**: Cloud API (OAuth2 authentication)
- **Local API**: No, requires internet connection to Netatmo servers
- **Modules Tested**: Outdoor Module (NAModule1), Indoor Smart Module (NAModule4)

## API Authentication
Netatmo uses OAuth2 with password grant type for personal applications.

### Required Credentials
1. **Username**: Netatmo account email
2. **Password**: Netatmo account password
3. **Client ID**: From registered app at dev.netatmo.com
4. **Client Secret**: From registered app at dev.netatmo.com

### Token Endpoint
- **URL**: `https://api.netatmo.com/oauth2/token`
- **Method**: POST
- **Grant Type**: `password` (initial) or `refresh_token` (renewal)

### Initial Token Request
```
POST https://api.netatmo.com/oauth2/token
grant_type: password
username: [your_email]
password: [your_password]
client_id: [your_client_id]
client_secret: [your_client_secret]
scope: read_station
```

### Token Refresh Request
```
POST https://api.netatmo.com/oauth2/token
grant_type: refresh_token
refresh_token: [your_refresh_token]
client_id: [your_client_id]
client_secret: [your_client_secret]
```

## API Endpoints
Base URL: `https://api.netatmo.com/api`

### Get Stations Data
- **Endpoint**: `/api/getstationsdata`
- **Method**: GET
- **Authentication**: Bearer token in Authorization header
- **Response**: JSON with station and module data
- **Scope Required**: `read_station`

### Get Measurements
- **Endpoint**: `/api/getmeasure`
- **Method**: GET
- **Parameters**:
  - `device_id`: ID of station or module
  - `scale`: max, 30min, 3hour, day, week, month, year
  - `type`: Comma-separated measures (Temperature,Humidity,CO2,Pressure,Noise,Rain,etc.)
  - `date_end`: Unix timestamp (default now)
  - `date_begin`: Unix timestamp (default 1 hour ago)
  - `limit`: Number of measures to return (1-1024)

## Response Structure
The `/getstationsdata` API returns:
```json
{
  "body": {
    "devices": [  // Array of stations
      {
        "_id": "station_id",
        "station_name": "Station Name",
        "type": "NAMain",  // Main module
        "module_name": "Module Name",
        "firmware": "firmware_version",
        "wifi_status": wifi_status_code,
        "reachable": true/false,
        "data_type": ["Temperature", "CO2", "Humidity", "Noise", "Pressure"],
        "place": {
          "altitude": altitude_in_meters,
          "city": "City Name",
          "country": "Country Code",
          "timezone": "Timezone",
          "location": [longitude, latitude]
        },
        "dashboard_data": {  // Current readings from main module
          "Temperature": temperature_in_C,
          "Humidity": humidity_percent,
          "Pressure": pressure_in_hPa,
          "CO2": co2_in_ppm,
          "Noise": noise_in_db,
          "min_temp": minimum_today,
          "max_temp": maximum_today,
          "temp_trend": trend_indicator,
          "pressure_trend": trend_indicator,
          "hum_trend": trend_indicator,
          "co2_trend": trend_indicator,
          "wifi_status": wifi_status,
          "rf_status": rf_status,
          "battery_percent": battery_level,
          "battery_vp": battery_voltage,
          "time_utc": unix_timestamp
        },
        "modules": [  // Array of additional modules
          {
            "_id": "module_id",
            "module_name": "Module Name",
            "type": "NAModule1|NAModule2|NAModule3|NAModule4",
            "dashboard_data": {  // Same structure as main module dashboard_data
              // Module-specific readings (varies by type)
            }
          }
        ]
      }
    ]
  }
}
```

## Module Types
- **NAMain**: Main station (indoor air quality)
- **NAModule1**: Outdoor module (temperature, humidity)
- **NAModule2**: Rain gauge
- **NAModule3**: Anemometer (wind)
- **NAModule4**: Additional indoor module (CO2, etc.)

## Common Measurements
- **Temperature**: Celsius
- **Humidity**: Percentage (%)
- **Pressure**: Hectopascals (hPa)
- **CO2**: Parts per million (ppm)
- **Noise**: Decibels (dB)
- **Rain**: Millimeters (mm) - various time intervals

## Integration Process
1. **Register App**: Create application at dev.netatmo.com to get Client ID/Secret
2. **Get Initial Tokens**: Use password grant with username/password
3. **Store Tokens**: Save access_token and refresh_token securely
4. **Refresh Tokens**: Use refresh_token to get new access_token when expired
5. **Make API Calls**: Include Bearer token in Authorization header
6. **Parse Response**: Extract relevant data from JSON structure

## Environment Variables (for skill)
- `NETATMO_USERNAME`: Netatmo account email
- `NETATMO_PASSW`: Netatmo account password
- `NETATMO_CLIENT_ID`: OAuth2 Client ID
- `NETATMO_CLIENT_SECRET`: OAuth2 Client Secret
- `NETATMO_ACCESS_TOKEN`: OAuth2 access token (managed by skill)
- `NETATMO_REFRESH_TOKEN`: OAuth2 refresh token (managed by skill)

## Troubleshooting
- **401 Unauthorized**: Token expired or invalid - trigger refresh
- **403 Forbidden**: Insufficient scope - ensure `read_station` scope granted
- **Connection errors**: Check internet connectivity and Netatmo API status
- **Missing data**: Verify module types and available measurements
- **Rate limiting**: Netatmo API has limits - implement caching and backoff

## Data Freshness
- Netatmo modules typically report every 5-10 minutes
- API responses show `time_utc` timestamps for freshness
- Consider caching responses for 2-5 minutes to reduce API calls

## Example Usage
### Get current outdoor temperature:
1. Call `getstationsdata`
2. Find outdoor module (type: NAModule1)
3. Extract `dashboard_data.Temperature`

### Get indoor CO2 from bedroom module:
1. Call `getstationsdata`
2. Find specific indoor module by name or type (NAModule4)
3. Extract `dashboard_data.CO2`

### Get historical data:
1. Call `getmeasure` with:
   - `device_id`: module or station ID
   - `scale`: "hour" or "day"
   - `type`: "Temperature,Humidity"
   - `limit`: 24 (for hourly)