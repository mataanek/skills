# Concrete Examples from Apple Health Exports (Health Auto Export)

This file contains real examples of the JSON structure encountered during implementation to aid in understanding and debugging.

## Health Export Example Snippets

### heartRateVariability Array
```json
"heartRateVariability": [
  {
    "date": "2026-05-18",
    "unit": "ms",
    "value": 45.2
  },
  {
    "date": "2026-05-19",
    "unit": "ms",
    "value": 48.7
  }
]
```

### sleepTime Array with Stages
```json
"sleepTime": [
  {
    "date": "2026-05-18",
    "unit": "min",
    "value": 420.5,
    "stages": {
      "awake": 15.2,
      "core": 180.3,
      "deep": 95.0,
      "rem": 110.0,
      "unspecified": 20.0
    }
  },
  {
    "date": "2026-05-19",
    "unit": "min",
    "value": 397.0,
    "stages": {
      "awake": 8.5,
      "core": 233.0,
      "deep": 98.0,
      "rem": 66.0,
      "unspecified": 0.0
    }
  }
]
```

## Workouts Export Example Snippets

### Individual Workout Object
```json
{
  "activityType": "Running",
  "duration": 1620.5,
  "endDate": "2026-05-19T06:10:32Z",
  "events": [],
  "source": "Connect",
  "startDate": "2026-05-19T05:40:11Z",
  "statistics": {
    "HKQuantityTypeIdentifierActiveEnergyBurned": {
      "sum": 391,
      "unit": "kcal"
    },
    "HKQuantityTypeIdentifierBasalEnergyBurned": {
      "sum": 43,
      "unit": "kcal"
    },
    "HKQuantityTypeIdentifierDistanceWalkingRunning": {
      "sum": 5020.5,
      "unit": "m"
    }
  }
}
```

### Walk Workout Example
```json
{
  "activityType": "Walking",
  "duration": 3600.0,
  "endDate": "2026-05-19T06:10:32Z",
  "events": [],
  "source": "Connect",
  "startDate": "2026-05-19T05:09:41Z",
  "statistics": {
    "HKQuantityTypeIdentifierActiveEnergyBurned": {
      "sum": 199,
      "unit": "kcal"
    },
    "HKQuantityTypeIdentifierBasalEnergyBurned": {
      "sum": 96,
      "unit": "kcal"
    },
    "HKQuantityTypeIdentifierDistanceWalkingRunning": {
      "sum": 3670.8,
      "unit": "m"
    }
  }
}
```

## Usage
These examples illustrate the actual data structures encountered when processing Health Auto Export files. They can be used to:
- Validate extraction logic
- Understand the format of specific metrics
- Debug issues with missing or malformed data
- Develop test cases for the extraction script