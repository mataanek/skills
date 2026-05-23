---
name: netatmo-control
description: Collect and store Netatmo weather station data for long-term trend analysis in Hermes wiki.
category: smart-home
version: 1.0.0
author: mataanek
---
# Netatmo Control Skill

This skill provides tools and scripts to collect data from Netatmo weather stations and store it in the Hermes wiki for long-term trend analysis.

## Overview

The skill includes scripts to:
- Fetch current station data from the Netatmo API every 6 hours via cron
- Store readings in structured JSON files per sensor
- Maintain a JSONL log of all readings
- Generate daily summary files
- Extract daily historical data (last 24 hours at 30-minute intervals) for the main module once per day

## How It Works

The skill uses the Hermes tool registry to load Netatmo-specific tools. The `register_netatmo_tools.py` script executes to register tools like `netatmo_get_stations`. The main collection script `collect_netatmo_data.py` then uses these tools to fetch and process data.

### Data Collection Scheduling

- **Current Data Collection**: Runs every 6 hours via cron job `netatmo-data-collection` (0 */6 * * *) to capture real-time conditions
- **Historical Data Extraction**: Runs daily at 02:00 AM via cron job `netatmo-daily-historical` (0 2 * * *) to extract last 24 hours of historical data for the main module at 30-minute intervals

### Data Structure

Netatmo API returns data with the following relevant structure:
- Each device has a `dashboard_data` field containing measurements (Temperature, Humidity, Pressure, CO2, Noise)
- Each module also has a `dashboard_data` field with its specific measurements
- The `data_type` array lists what measurements are available for a device/module

## Pitfalls

- **API Response Structure**: Initial debugging showed that the `getstationsdata` endpoint does not include `dashboard_data` or `measurements` fields in the response. However, the working implementation accesses these fields, suggesting either:
  - Different API parameters are needed
  - The response structure varies based on account type or device firmware
  - The `dashboard_data` is populated through a different mechanism
  Always verify the actual response structure when integrating with Netatmo API.

- **Module Historical Data**: Historical data extraction via `getdevice/measures` endpoint works for the main module (using station ID as device_id) but returns 404 errors for individual modules when using their module IDs. Testing showed that using the station ID as device_id returns main module data regardless of which module's metrics are requested. This suggests that historical data for individual modules may not be available via the public Netatmo API, or requires a different approach not yet discovered.

- **Collection Frequency Balance**: The original 5-minute collection interval was changed to 6-hour intervals (4 times daily) to reduce API calls while still capturing meaningful trends. A daily historical extraction job (at 02:00) backfills the main module with 30-minute interval data for the last 24 hours. This approach balances data granularity with API usage efficiency.

- **Token Expiration**: Netatmo access tokens expire and require refresh using the refresh token. The `register_netatmo_tools.py` script includes automatic token refresh functionality (_refresh_access_token) that updates the stored tokens in the .env file. The script has been updated to handle both HTTP 401 and 403 responses for expired tokens, triggering a token refresh attempt in both cases. If data collection fails with "Access token expired" error (often code 3) and refresh fails, re-authentication via password grant may be necessary.

- **Token refresh may fail**: If the access token is invalid even after refresh, the refresh token itself may be expired or revoked. In this case, re-authenticate using the password grant type (username/password/client_id/client_secret) to obtain new tokens, then update the .env file manually.

## Scripts

### collect_netatmo_data.py
Main collection script for cron jobs. Fetches current data and stores it in:
- `sensor_log.jsonl`: JSON lines log of all readings
- Individual sensor files: `{station_id}_{module_id}_{metric_name}.json` (last 1000 readings)
- Daily summary: `daily_summary_YYYY-MM-DD.json`

### register_netatmo_tools.py
Loads Netatmo-specific tools into the Hermes registry by defining tool functions.

### extract_daily_historical.py
Extracts historical data from Netatmo API for backfilling the wiki with past measurements.

## Usage

Run the collection script via cron:
```bash
python3 /home/mataanek/.hermes/skills/smart-home/netatmo-control/scripts/collect_netatmo_data.py
```

## References

See `references/netatmo_api_structure.md` for detailed API response structure.
See `references/token_refresh_troubleshooting.md` for token refresh troubleshooting steps.
See `references/token_refresh_procedure.md` for manual token refresh procedure.