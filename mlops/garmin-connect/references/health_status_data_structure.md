# Health Status Data Structure (HRV Weekly Average)

Garmin Connect exports a `*_healthStatusData.json` file under `DI_CONNECT/DI-Connect-Wellness/` that contains **weekly averaged health metrics**, including Heart Rate Variability (HRV).

## File Naming Pattern
- `YYYY-MM-DD_YYYY-MM-DD_<userID>_healthStatusData.json`
  - Example: `2025-11-01_2026-02-08_104416285_healthStatusData.json`

## JSON Structure
The file is a JSON array where each element represents one day's health status summary.

Each element contains:
- `calendarDate`: string (YYYY-MM-DD) – the date this summary applies to.
- `timestamp`: string (ISO-like) – generation timestamp.
- `metrics`: array of objects, each representing a specific metric.

### Metrics Objects
Each metric object includes:
- `type`: string – metric identifier (e.g., `"HRV"`, `"HR"`, `"SPO2"`, `"RESPIRATION"`).
- `value`: numeric – the measured value for that day.
- `baselineUpperLimit`: numeric – upper bound of the user's personal baseline.
- `baselineLowerLimit`: numeric – lower bound of the user's personal baseline.
- `status`: string – `"IN_RANGE"`, `"BELOW"`, or `"ABOVE"` relative to baseline.
- `percentage`: numeric – where the value falls within the baseline range (0-100).
- `feedbackKey`: string – Garmin-specific feedback identifier.

### HRV Specifics
- When `"type": "HRV"`, the `value` is the **weekly averaged RMSSD** (in milliseconds).
- This value is **not** a daily snapshot but a rolling weekly average computed by Garmin.
- The `baselineUpperLimit` and `baselineLowerLimit` define the user's typical HRV range.
- `status` indicates whether the weekly average is within, below, or above baseline.
- `percentage` shows the relative position within the baseline (e.g., 50 = median).

## Usage Notes
- HRV from this file is **weekly averaged**, suitable for longitudinal trend analysis (e.g., weekly correlation with training load).
- For daily HRV, the wellness snapshot files (`*_wellnessActivities.json`) contain sporadic daily RMSSD/SDRR values, but they are sparse.
- To obtain the most reliable HRV trend, combine:
  - Weekly average from `healthStatusData.json` (consistent, long-term).
  - Daily snapshots from wellness files when available (for granularity).

## Example Entry
```json
{
  "calendarDate": "2025-11-15",
  "timestamp": "2025-11-15T06:54:18.784",
  "outliersCount": 3,
  "metrics": [
    {
      "type": "HRV",
      "value": 27.0,
      "baselineUpperLimit": 66.0,
      "baselineLowerLimit": 38.0,
      "status": "BELOW",
      "percentage": 0.0,
      "feedbackKey": "LHA_OFF_YOUR_BASELINE_FEEDBACK_HRV_BELOW_RANGE"
    },
    {
      "type": "HR",
      "value": 74.0,
      "baselineUpperLimit": 66.0,
      "baselineLowerLimit": 48.0,
      "status": "ABOVE",
      "percentage": 100.0,
      "feedbackKey": "LHA_OFF_YOUR_BASELINE_FEEDBACK_HEART_RATE_ABOVE_RANGE"
    },
    {
      "type": "SPO2",
      "value": 92.0,
      "baselineUpperLimit": 100.0,
      "baselineLowerLimit": 90.0,
      "status": "IN_RANGE",
      "percentage": 20.0,
      "feedbackKey": "LHA_OFF_YOUR_BASELINE_FEEDBACK_BLOOD_OXYGEN_IN_RANGE"
    },
    {
      "type": "SKIN_TEMP_C",
      "baselineUpperLimit": 0.0,
      "baselineLowerLimit": 0.0,
      "status": "UNKNOWN",
      "percentage": 0.0,
      "feedbackKey": "LHA_OFF_YOUR_BASELINE_FEEDBACK_SKIN_TEMPERATURE_UNKNOWN"
    },
    {
      "type": "RESPIRATION",
      "value": 17.1,
      "baselineUpperLimit": 16.2,
      "baselineLowerLimit": 12.8,
      "status": "ABOVE",
      "percentage": 100.0,
      "feedbackKey": "LHA_OFF_YOUR_BASELINE_FEEDBACK_RESPIRATION_RATE_ABOVE_RANGE"
    }
  ]
}
```

## Extraction Guidance
When building a data lake or performing trend analysis:
1. Parse each `*_healthStatusData.json` file.
2. For each entry, locate the metric where `type == "HRV"`.
3. Record `calendarDate` as the date and `value` as the weekly averaged HRV (RMSSD ms).
4. Optionally store `baselineUpperLimit`/`baselineLowerLimit` for normalization.
5. Aggregate as needed (e.g., keep weekly values as-is, or compute rolling averages).

---
*This reference is based on empirical inspection of Garmin GDPR export files stored in `/home/mataanek/.hermes/wiki/raw/garmin/`.*