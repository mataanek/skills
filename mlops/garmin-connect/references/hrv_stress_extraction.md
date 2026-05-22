# HRV and Stress Data Extraction from Garmin Wellness Snapshots

## Problem
Wellness snapshots (`*_wellnessActivities.json`) may appear to have missing HRV (RMSSD_HRV, SDRR_HRV) and stress (STRESS) values when naively parsing, even though the Garmin Connect app shows them.

## Root Cause
The `summaryTypeDataList` array contains objects with a `summaryType` field that indicates the metric type. The values are not under generic keys like `hrv` or `stress` but are tied to specific `summaryType` strings.

## Correct Extraction Paths

### HRV (RMSSD and SDRR)
- Look for objects in `summaryTypeDataList` where:
  - `summaryType` == `"RMSSD_HRV"` → the `value` field is the RMSSD in milliseconds.
  - `summaryType` == `"SDRR_HRV"` → the `value` field is the SDRR in milliseconds.

### Stress
- Look for objects where:
  - `summaryType` == `"STRESS"` → the `value` field is the stress level (0-100).

### Example Python snippet
```python
def extract_hrv_stress(wellness_data):
    """
    wellness_data: parsed JSON from a *_wellnessActivities.json file (list of daily entries)
    Returns: dict with keys 'rmssd_hrv', 'sdrr_hrv', 'stress' (values or None if not found)
    """
    result = {"rmssd_hrv": None, "sdrr_hrv": None, "stress": None}
    if not isinstance(wellness_data, list):
        return result
    for entry in wellness_data:
        if not isinstance(entry, dict):
            continue
        for summary in entry.get("summaryTypeDataList", []):
            if not isinstance(summary, dict):
                continue
            stype = summary.get("summaryType")
            val = summary.get("value")
            if stype == "RMSSD_HRV":
                result["rmssd_hrv"] = val
            elif stype == "SDRR_HRV":
                result["sdrr_hrv"] = val
            elif stype == "STRESS":
                result["stress"] = val
    return result
```

## Verification
After extraction, verify that values are within expected ranges:
- RMSSD_HRV: typically 10-200 ms (higher = better recovery)
- SDRR_HRV: similar range to RMSSD
- Stress: 0-100 (lower = more relaxed)

If values are still None, double-check that the file being read corresponds to a date with available data (wellness snapshots are not guaranteed for every day).

## Note on Sleep Data
HRV is **not** present in sleep data (`*_sleepData.json`). If you need nightly HRV, you must rely on the weekly average found in `*_healthStatusData.json` files (field `hrvWeeklyAverage`). For daily HRV, use wellness snapshots as above.
