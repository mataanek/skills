# Netatmo API Response Structure

Based on debugging session on 2026-05-16, the Netatmo API response for `getstationsdata` has the following structure:

```json
{
  "body": {
    "devices": [
      {
        "_id": "70:ee:50:a4:73:88",
        "date_setup": 1705679967,
        "last_setup": 1705679967,
        "type": "NAMain",
        "last_status_store": 1778476311,
        "module_name": "Weather Station living room",
        "firmware": 300,
        "wifi_status": 79,
        "reachable": false,
        "co2_calibrating": false,
        "data_type": [
          "Temperature",
          "CO2",
          "Humidity",
          "Noise",
          "Pressure"
        ],
        "place": {
          "altitude": 334,
          "city": "Pop\vownky",
          "country": "CZ",
          "timezone": "Europe/Prague",
          "location": [
            16.490326,
            49.194777
          ]
        },
        "station_name": "House (Weather Station living room)",
        "home_id": "65aa9c5f7fca1eb93609c1cd",
        "home_name": "House",
        "modules": [
          {
            "_id": "02:00:00:a4:3d:a8",
            "type": "NAModule1",
            "module_name": "Outdoor Module",
            "last_setup": 1705679967,
            "data_type": [
              "Temperature",
              "Humidity"
            ],
            "battery_percent": 50,
            "reachable": false,
            "firmware": 53,
            "last_message": 1778476307,
            "last_seen": 1778476288,
            "rf_status": 120,
            "battery_vp": 5098
          }
        ]
      }
    ]
  }
}
```

## Important Notes for Data Extraction

1. **Measurements Location**: Unlike expected, the actual measurements are NOT in a `measurements` or `dashboard_data` field at the device or module level in the current API response.

2. **Available Data**: The API response shows:
   - `data_type` array listing what measurements are available
   - But the actual measurement values are not present in this response structure

3. **Working Endpoint**: The working implementation in the skill uses a different approach that accesses `dashboard_data` fields, suggesting either:
   - There's a different endpoint being used
   - The API response structure varies based on parameters
   - The `dashboard_data` is populated in a different way

4. **Device Types Observed**:
   - `NAMain`: Main station module
   - `NAModule1`: Outdoor module
   - `NAModule4`: Indoor module

## Recommendation

To get actual measurement values, the skill should investigate:
- Whether additional parameters are needed for the `getstationsdata` call
- If there's a different endpoint for getting measurements
- Whether the `dashboard_data` is populated through a different mechanism

Current working implementation accesses `dashboard_data` on both devices and modules, so the API structure documentation should note that the actual working structure includes these fields even if they weren't visible in the debug output.