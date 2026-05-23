# Key Learnings from Netatmo Integration Sessions

## Session 2026-05-16
- **Module ID Limitations for Historical Data**: Historical data extraction works for main module but not individual modules via public API
- **Collection Frequency Optimization**: 6-hour intervals for current data + daily historical backfill balances granularity with API usage
- **Data Storage Structure**: JSON Lines log, individual sensor files, daily summaries, and historical files for main module
- **Cron Job Configuration**: netatmo-data-collection (0 */6 * * *) and netatmo-daily-historical (0 2 * * *)

## Session 2026-05-23
- **Token Expiration Handling**: Netatmo API returns HTTP 403 (not just 401) for expired tokens
- **Fix Applied**: Updated register_netatmo_tools.py to handle both 401 and 403 responses in _make_netatmo_request
- **Verification**: After fix, token refresh succeeded and data collection completed successfully
- **Historical Data Extraction**: extract_daily_historical.py works correctly for main module metrics at 30-minute intervals

## Module ID Limitations for Historical Data
- **Main Module**: Historical data extraction works correctly using station ID as device_id in getdevice/measures calls
- **Individual Modules**: Using module IDs (e.g., 02:00:00:c2:49:5e for Outdoor Module Byt) returns 404 errors
- **Workaround Discovery**: When using station ID as device_id, the API returns main module data regardless of which module's metrics are requested
- **Conclusion**: Historical data for individual modules (outdoor/bedroom) is likely not available via the public Netatmo API
- **Recommendation**: For module-specific historical trends, rely on frequent collection of current module data

## Collection Frequency Optimization
- **Original Plan**: 5-minute intervals for current data collection
- **Revised Approach**: 6-hour intervals (4 times daily) for current data collection
- **Rationale**: Balances data granularity with API usage efficiency
- **Backfill Strategy**: Daily historical extraction (02:00) provides 30-minute interval data for last 24 hours for main module
- **Result**: Detailed historical trends for main station while minimizing API calls

## Data Storage Structure
- **Real-time Data**: 
  - JSON Lines log: `sensor_log.jsonl` (complete records)
  - Individual sensor files: `{station_id}_{module_id}_{metric_name}.json` (rotating buffer of last 1000 readings)
  - Daily summaries: `daily_summary_YYYY-MM-DD.json` (latest readings, kept 48 hours)
- **Historical Data** (Main Module Only):
  - Files: `{station_id}_main_{metric}_historical_1d.json` (last 24 hours at 30-min intervals)
  - Files: `{station_id}_main_{metric}_historical_7d.json` (last 7 days at 30-min intervals)

## API Response Structure Notes
- The `dashboard_data` field contains the primary measurements (Temperature, Humidity, Pressure, CO2, Noise)
- Some modules may not have all metrics (e.g., outdoor modules lack CO2)
- Always verify actual response structure as it may vary by device firmware or account type

## Cron Job Configuration
1. `netatmo-data-collection`: 0 */6 * * * (every 6 hours)
2. `netatmo-daily-historical`: 0 2 * * * (daily at 2 AM)

## Best Practices for Future Sessions
- When debugging Netatmo API, always inspect the full response structure
- For voice integration: Audio is successfully routed through PulseAudio to Windows speakers via RDP sink/source
- Wake word detection (Porcupine) and STT (Whisper) are ready for implementation once access key is provided