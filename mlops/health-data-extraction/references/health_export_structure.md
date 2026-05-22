# Apple Health Export JSON Structure (via Health Auto Export)

## Health Export (`health_export_*.json`)
A JSON object where each key is a metric name and the value is an array of daily entries.

### Common Structure for Metric Arrays
Each element in the array is an object with:
- `date`: string in `YYYY-MM-DD` format
- `unit`: string representing the unit of measurement
- `value`: number (integer or float) representing the metric value for that date

### Metrics Observed
- `activeCalories`: Total active energy burned (kcal)
- `basalCalories`: Basal energy burned (kcal)
- `bmi`: Body Mass Index
- `bodyFat`: Body fat percentage
- `dietaryCarbohydrates`: Carbohydrates consumed (g)
- `dietaryEnergy`: Dietary energy consumed (kcal)
- `dietaryFatTotal`: Fat consumed (g)
- `dietaryProtein`: Protein consumed (g)
- `exerciseMinutes`: Minutes of exercise
- `exportInfo`: Metadata about the export (not an array)
- `flightsClimbed`: Number of flights climbed
- `heartRateVariability`: HRV in milliseconds (ms)
- `leanBodyMass`: Lean body mass (kg)
- `oxygenSaturation`: Blood oxygen saturation (%)
- `respiratoryRate`: Breaths per minute
- `restingHeartRate`: Resting heart rate (bpm)
- `sleepTime`: Sleep duration with stages (see below)
- `stepCount`: Step count
- `vo2Max`: VO₂Max (ml/kg/min)
- `walkingDistance`: Distance walked (m)
- `walkingHeartRate`: Average heart rate during walking (bpm)
- `weight`: Body weight (kg)
- `wristTemperature`: Wrist temperature (°C)

### Special Structures
#### `sleepTime`
Each element includes:
- `date`: string
- `unit`: "min"
- `value`: total sleep minutes
- `stages`: object with keys `awake`, `core`, `deep`, `rem`, `unspecified` (all in minutes)

#### `exportInfo`
Not an array; a single object with:
- `appVersion`: string
- `activityTypes`: array of strings (e.g., ["running", "walking"])
- `dataTypes`: array of strings (list of metrics included)
- `startDate`: string (YYYY-MM-DD)
- `endDate`: string (YYYY-MM-DD)
- `exportDate`: string (ISO timestamp)
- `measurementSystem`: string (e.g., "metric")

## Workouts Export (`workouts_export_*.json`)
A JSON object with two main keys:

### `exportInfo`
Metadata about the workout export:
- `activityTypes`: array of strings (types of workouts included)
- `appVersion`: string
- `endDate`: string (YYYY-MM-DD) - end of export period
- `exportDate`: string (ISO timestamp)
- `startDate`: string (YYYY-MM-DD) - start of export period
- `workoutCount`: integer

### `workouts`
An array of workout objects. Each workout object includes:
- `activityType`: string (e.g., "Walking", "Running", "Cycling")
- `duration`: number (seconds)
- `endDate`: string (ISO timestamp)
- `events`: array (usually empty in exports)
- `source`: string (e.g., "Connect", "Watch")
- `startDate`: string (ISO timestamp)
- `statistics`: object containing various health metrics for the workout

#### Workout Statistics Keys Observed
- `HKQuantityTypeIdentifierActiveEnergyBurned`: Active energy burned during workout (kcal)
- `HKQuantityTypeIdentifierBasalEnergyBurned`: Basal energy burned during workout (kcal)
- `HKQuantityTypeIdentifierDistanceWalkingRunning`: Distance walked/ran (m)
- `HKQuantityTypeIdentifierHeartRate`: Average heart rate (count/min) - may include more detailed stats
- `HKQuantityTypeIdentifierStepCount`: Step count during workout

Note: The exact statistics keys may vary by workout type and device.

## Usage
This structure is used by the `health_extract.py` script to pull daily metrics and workout details for logging into the training wiki.