# Garmin Data Lake Schema

The data lake is a Parquet file with one row per calendar date, containing aggregated health and workout metrics from the Garmin Connect export.

## Columns

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Calendar date (YYYY-MM-DD) |
| resting_hr_bpm | FLOAT? | Average resting heart rate from wellness snapshots (HEART_RATE.avgValue) or sleep average HR (spo2SleepSummary.averageHR) |
| stress_avg | FLOAT? | Average stress score from wellness snapshots |
| spo2_pct | FLOAT? | Average SpO2 percentage from wellness snapshots |
| hrv_rmssd_ms | FLOAT? | Average RMSSD HRV (milliseconds) from wellness snapshots |
| hrv_sdrr_ms | FLOAT? | Average SDRR HRV (milliseconds) from wellness snapshots |
| respiration_bpm | FLOAT? | Average respiration rate from wellness snapshots |
| sleep_deep_min | FLOAT? | Deep sleep duration in minutes |
| sleep_light_min | FLOAT? | Light sleep duration in minutes |
| sleep_rem_min | FLOAT? | REM sleep duration in minutes |
| sleep_awake_min | FLOAT? | Awake duration during sleep period in minutes |
| sleep_avg_hr_bpm | FLOAT? | Average heart rate during sleep from spo2SleepSummary.averageHR |
| sleep_avg_spo2_pct | FLOAT? | Average SpO2 during sleep from spo2SleepSummary.averageSPO2 |
| run_steps | INT | Total steps from running activities |
| run_distance_km | FLOAT | Total distance from running activities (km) |
| run_duration_min | FLOAT | Total duration from running activities (minutes) |
| run_calories | FLOAT | Total calories burned from running activities |
| run_avg_hr | FLOAT? | Time-weighted average heart rate during runs |
| run_max_hr | FLOAT? | Maximum heart rate observed during runs |
| run_min_hr | FLOAT? | Minimum heart rate observed during runs |
| run_aerobic_te | FLOAT? | Aerobic training effect (from summarized activities) |
| run_anaerobic_te | FLOAT? | Anaerobic training effect (from summarized activities) |
| run_mod_int_min | FLOAT? | Moderate intensity minutes (from summarized activities) |
| run_vig_int_min | FLOAT? | Vigorous intensity minutes (from summarized activities) |
| run_training_status | STRING? | Most frequent training status for the day (RECOVERY, MAINTAINING, PRODUCTIVE, PEAKING) |
| run_fitness_trend | STRING? | Fitness trend indicator (e.g., NO_CHANGE, IMPROVING) |
| high_intensity_run_flag | BOOL | True if any run exceeded intensity threshold (calories/min > 8.0) or training status in {PRODUCTIVE, PEAKING} |
| high_intensity_run_min | FLOAT | Sum of duration (minutes) of runs flagged as high-intensity |
| high_intensity_run_count | INT | Count of runs flagged as high-intensity |

## Notes
- Nullable columns (indicated with `?`) may be missing if no data source contributed value for that date.
- Intensity threshold for high-intensity runs is configurable; default is 8.0 kcal/min.
- Training status and fitness trend are derived from `TrainingHistory_*.json` files; if multiple values exist per day, the mode is taken.
- All durations are converted to minutes; distances to kilometers.