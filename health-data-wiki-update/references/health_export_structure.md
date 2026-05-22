# Health Export JSON Structure

Based on the actual export from Health Auto Export, the JSON file has the following structure:

```json
{
  "activeCalories": [
    {
      "date": "YYYY-MM-DD",
      "unit": "kcal",
      "value": <number>
    }
  ],
  "basalCalories": [
    {
      "date": "YYYY-MM-DD",
      "unit": "kcal",
      "value": <number>
    }
  ],
  "bmi": [
    {
      "date": "YYYY-MM-DD",
      "unit": "",
      "value": <number>
    }
  ],
  "bodyFat": [
    {
      "date": "YYYY-MM-DD",
      "unit": "%",
      "value": <number>
    }
  ],
  "dietaryCarbohydrates": [
    {
      "date": "YYYY-MM-DD",
      "unit": "g",
      "value": <number>
    }
  ],
  "dietaryEnergy": [
    {
      "date": "YYYY-MM-DD",
      "unit": "kcal",
      "value": <number>
    }
  ],
  "dietaryFatTotal": [
    {
      "date": "YYYY-MM-DD",
      "unit": "g",
      "value": <number>
    }
  ],
  "dietaryProtein": [
    {
      "date": "YYYY-MM-DD",
      "unit": "g",
      "value": <number>
    }
  ],
  "exerciseMinutes": [
    {
      "date": "YYYY-MM-DD",
      "unit": "min",
      "value": <number>
    }
  ],
  "exportInfo": {
    // export metadata
  },
  "flightsClimbed": [
    {
      "date": "YYYY-MM-DD",
      "unit": "count",
      "value": <number>
    }
  ],
  "heartRateVariability": [
    {
      "date": "YYYY-MM-DD",
      "unit": "ms",
      "value": <number>
    }
  ],
  "leanBodyMass": [
    {
      "date": "YYYY-MM-DD",
      "unit": "kg",
      "value": <number>
    }
  ],
  "oxygenSaturation": [
    {
      "date": "YYYY-MM-DD",
      "unit": "%",
      "value": <number>
    }
  ],
  "respiratoryRate": [
    {
      "date": "YYYY-MM-DD",
      "unit": "breaths/min",
      "value": <number>
    }
  ],
  "restingHeartRate": [
    {
      "date": "YYYY-MM-DD",
      "unit": "bpm",
      "value": <number>
    }
  ],
  "sleepTime": [
    {
      "date": "YYYY-MM-DD",
      "unit": "hr",
      "value": <number>
    }
  ],
  "stepCount": [
    {
      "date": "YYYY-MM-DD",
      "unit": "count",
      "value": <number>
    }
  ],
  "vo2Max": [
    {
      "date": "YYYY-MM-DD",
      "unit": "ml/kg/min",
      "value": <number>
    }
  ],
  "walkingDistance": [
    {
      "date": "YYYY-MM-DD",
      "unit": "km",
      "value": <number>
    }
  ],
  "walkingHeartRate": [
    {
      "date": "YYYY-MM-DD",
      "unit": "bpm",
      "value": <number>
    }
  ],
  "weight": [
    {
      "date": "YYYY-MM-DD",
      "unit": "kg",
      "value": <number>
    }
  ],
  "wristTemperature": [
    {
      "date": "YYYY-MM-DD",
      "unit": "°C",
      "value": <number>
    }
  ]
}
```

Note: Each metric key maps to an array of objects, where each object contains:
- `date`: string in YYYY-MM-DD format
- `unit`: string representing the unit of measurement
- `value`: numeric value

Some metrics may have multiple entries per day (e.g., stepCount might have hourly data), but the exports we receive appear to be daily summaries.