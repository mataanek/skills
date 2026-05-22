# Garmin Wellness Data JSON Structure

## Overview
This document describes the exact JSON structure found in Garmin Connect GDPR export wellness files (`*_wellnessActivities.json`) based on empirical analysis of the user's data export.

## File Structure
The wellness data file is a JSON array where each element represents a health snapshot:

```json
[
  {
    "version": 1651513426176,
    "metaData": {
      "userProfilePk": 104416285,
      "activityUuid": {
        "uuid": "53daa569-a318-4696-a88b-e6b30a9d6d6c"
      },
      "deviceMetaData": {
        "deviceId": 3407465147,
        "deviceTypeId": 36889,
        "deviceVersionId": 897364,
        "deviceVersion": "6.57.0.0"
      }
    },
    "calendarDate": "2022-05-02",
    "rulePK": 2,
    "activityName": "Health Snapshot - Evening",
    "wellnessActivityType": "HEALTH_MONITORING",
    "startTimestampGMT": "2022-05-02T15:35:42.0",
    "endTimestampGMT": "2022-05-02T15:37:43.354",
    "startTimestampLocal": "2022-05-02T17:35:42.0",
    "endTimestampLocal": "2022-05-02T17:37:43.354",
    "createDate": "2022-05-02T17:43:46.176",
    "updateDate": "2022-05-02T17:43:46.176",
    "snapshotTimeOfDayType": "EVENING",
    "summaryTypeDataList": [
      // ...see below...
    ],
    "timeInZoneList": [
      // ...see below...
    ]
  },
  // ...more entries...
]
```

## Key Data: summaryTypeDataList
The `summaryTypeDataList` array contains the actual health metrics. Each element has:
- `summaryType`: string identifying the metric type
- `minValue`: minimum value observed (optional)
- `maxValue`: maximum value observed (optional)
- `avgValue`: average value (the primary value we extract)

### Relevant summaryType Values:
| summaryType | What it represents | Value we extract |
|-------------|-------------------|------------------|
| `HEART_RATE` | Resting heart rate from wellness snapshot | `avgValue` → resting_hr_bpm |
| `STRESS` | Stress level (0-100) | `avgValue` → stress_avg |
| `SPO2` | Blood oxygen saturation percentage | `avgValue` → spo2_pct |
| `RMSSD_HRV` | Heart Rate Variability - RMSSD (ms) | `avgValue` → hrv_rmssd_ms |
| `SDRR_HRV` | Heart Rate Variability - SDRR (ms) | `avgValue` → hrv_sdrr_ms |
| `RESPIRATION` | Respiratory rate (breaths/min) | `avgValue` → respiration_bpm |

## Sleep Data Structure (`*_sleepData.json`)
For comparison, sleep data has a different structure:

```json
[
  {
    "version": 1649958000000,
    "metaData": {
      "userProfilePk": 104416285,
      "activityUuid": {
        "uuid": "f3e1c4b2-a1b2-c3d4-e5f6-a7b8c9d0e1f2"
      },
      "deviceMetaData": {
        "deviceId": 3407465147,
        "deviceTypeId": 36889,
        "deviceVersionId": 899019,
        "deviceVersion": "7.35.0.0"
      }
    },
    "calendarDate": "2022-05-02",
    "rulePK": 1,
    "activityName": "Sleep",
    "wellnessActivityType": "SLEEP",
    "startTimestampGMT": "2022-05-01T22:00:00.0",
    "endTimestampGMT": "2022-05-02T08:00:00.0",
    "startTimestampLocal": "2022-05-02T00:00:00.0",
    "endTimestampLocal": "2022-05-02T10:00:00.0",
    "createDate": "2022-05-02T10:05:32.123",
    "updateDate": "2022-05-02T10:05:32.123",
    "deepSleepSeconds": 1800,
    "lightSleepSeconds": 3600,
    "remSleepSeconds": 1800,
    "awakeSleepSeconds": 900,
    "sleepScores": {
      "overallScore": 85,
      "qualityScore": 90,
      "durationScore": 80,
      "recoveryScore": 88,
      "deepScore": 75,
      "remScore": 92,
      "lightScore": 82
    },
    "spo2SleepSummary": {
      "averageSPO2": 96,
      "averageHR": 58.0,  // ← This is what we use as fallback for resting HR
      "lowestSPO2": 92
    },
    "respirationSummary": {
      "averageValue": 14.5
    }
  }
]
```

## Important Notes
1. **Wellness snapshots are sparse**: Not every calendar date will have a wellness snapshot entry. In the user's export, wellness snapshots appear only every few days/weeks.
2. **Sleep data is more consistent**: Sleep data exists for nearly every night, making `spo2SleepSummary.averageHR` a reliable fallback for resting HR when wellness data is missing.
3. **HRV and Stress are only in wellness snapshots**: These metrics do NOT appear in sleep data - they are ONLY available in the wellness snapshot `summaryTypeDataList`.
4. **Extraction priority**: 
   - First choice: Wellness snapshot `HEART_RATE.avgValue`
   - Fallback: Sleep data `spo2SleepSummary.averageHR`
   - HRV/Stress: Only available from wellness snapshots (will be NaN on days without snapshots)

## Verification
To verify your extraction is working correctly:
- Check that `resting_hr_bpm` has values for dates where wellness snapshots exist
- Check that `hrv_rmssd_ms` and `stress_avg` are populated on the same dates as wellness snapshots
- On dates without wellness snapshots, `resting_hr_bpm` should still have values (from sleep data) but HRV/stress will be NaN
