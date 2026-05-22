# Apple Health and Garmin Connect Data Fields

## Apple Health (Health Auto Export JSON)

### Health Export (health_export_*.json)
- `heartRateVariability`: array of objects with `date`, `value` (ms)
- `restingHeartRate`: array of objects with `date`, `value` (bpm)
- `sleepAnalysis`: array of sleep entries with `startDate`, `endDate`, `value` (HKCategoryValueSleepAnalysisInBed/Asleep)
- `appleExerciseTime`: array of exercise minutes
- `activeEnergyBurned`: array of active energy (kcal)
- `basalEnergyBurned`: array of basal energy (kcal)
- `stepCount`: array of steps
- `distanceWalkingRunning`: array of distance (m)
- `vo2Max`: array of VO2Max estimates (ml/kg/min)
- `bodyMass`: array of weight measurements (kg)

### Workouts Export (workouts_export_*.json)
Array of workout objects:
- `workoutActivityType`: e.g., `HKWorkoutActivityTypeRunning`, `HKWorkoutActivityTypeWalking`
- `duration`: duration in seconds
- `totalDistance`: distance in meters
- `totalEnergyBurned`: total calories (active + basal?)
- `activeEnergyBurned`: active calories
- `sourceName`: device/app name
- `creationDate`, `startDate`, `endDate`
- `metadata`: may include `HKIndoorWorkout`, `HKWeatherTemperature`, etc.

## Garmin Connect Export JSON Structure

### Wellness Activities (*_wellnessActivities.json)
Array of snapshot objects (usually two per day: morning/evening):
- `calendarDate`: YYYY-MM-DD
- `summaryTypeDataList`: array of objects:
  - `summaryType`: `HEART_RATE`, `RESPIRATION`, `STRESS`, `SPO2`, `RMSSD_HRV`, `SDRR_HRV`
  - `minValue`, `maxValue`, `avgValue`
- `timeInZoneList`: heart rate zones (millis in zone 0-5)

### Sleep Data (*_sleepData.json)
Array of nightly sleep objects:
- `calendarDate`: YYYY-MM-DD
- `deepSleepSeconds`, `lightSleepSeconds`, `remSleepSeconds`, `awakeSleepSeconds`
- `spo2SleepSummary`: object with `averageSPO2`, `averageHR`, `lowestSPO2`

### Summarized Activities (*_summarizedActivities.json)
Array of activity summaries (under DI-Connect-Fitness):
- `activityId`
- `activityType`: e.g., `running`, `walking`, `cycling`
- `sportType`: e.g., `RUNNING`, `WALKING`, `CYCLING`
- `beginTimestamp` / `startTimeGmt`: epoch ms
- `duration`: ms
- `distance`: meters
- `steps`: step count
- `calories`: total calories (kcal)
- `bmrCalories`: basal metabolic rate calories
- `avgHr`, `maxHr`, `minHr`: heart rate (bpm)
- `aerobicTrainingEffect`, `anaerobicTrainingEffect`: 0.0-5.0
- `moderateIntensityMinutes`, `vigorousIntensityMinutes`
- `vO2MaxValue`: estimated VO2Max from activity
- `trainingEffectLabel`: e.g., `RECOVERY`, `ENDURANCE`
- `activityTrainingLoad`: Garmin's training load score
- `differenceBodyBattery`: change in Body Battery
- `hrTimeInZone_0` to `_6`: milliseconds in each HR zone

### Training History (*_TrainingHistory_*.json)
Daily aggregation:
- `calendarDate`: YYYY-MM-DD
- `sport`: e.g., `RUNNING`
- `trainingStatus`: `RECOVERY`, `MAINTAINING`, `PRODUCTIVE`, `PEAKING`
- `fitnessLevelTrend`: `IMPROVING`, `MAINTAINING`, `DECLINING`
- `timestamp`: epoch ms

## Data Lake Schema (daily.parquet)

One row per calendar date with columns:

### Health Metrics
- `resting_hr_bpm`: from wellness snapshot HR avg
- `stress_avg`: average stress (0-100)
- `spo2_pct`: average SpO2 (%)
- `hrv_rmssd_ms`: RMSSD HRV (ms)
- `hrv_sdrr_ms`: SDRR HRV (ms)
- `respiration_bpm`: average respiration (breaths/min)

### Sleep Metrics
- `sleep_deep_min`: deep sleep duration (minutes)
- `sleep_light_min`: light sleep duration (minutes)
- `sleep_rem_min`: REM sleep duration (minutes)
- `sleep_awake_min`: awake duration (minutes)
- `sleep_avg_hr_bpm`: average HR during sleep (from spo2SleepSummary)
- `sleep_avg_spo2_pct`: average SpO2 during sleep

### Run Metrics (sum of all runs that day)
- `run_steps`: total steps
- `run_distance_km`: total distance (km)
- `run_duration_min`: total duration (minutes)
- `run_calories`: total active calories (kcal)
- `run_avg_hr`: average HR (weighted by duration?)
- `run_max_hr`: maximum HR observed
- `run_min_hr`: minimum HR observed
- `run_aerobic_te`: average aerobic training effect
- `run_anaerobic_te`: average anaerobic training effect
- `run_mod_int_min`: total moderate intensity minutes
- `run_vig_int_min`: total vigorous intensity minutes
- `run_sport_type`: most common sport type that day
- `run_activity_type`: most common activity type that day
- `run_training_status`: boolean (True if any run had status PRODUCTIVE or PEAKING)
- `run_fitness_trend`: most common fitness trend that day

### Derived Intensity Flags
- `high_intensity_run_flag`: True if run_calories/run_duration_min > 8 kcal/min OR run_training_status == True
- `high_intensity_run_min`: total duration of high-intensity runs (approximated as total run duration if flag set)
- `high_intensity_run_count`: count of high-intensity runs (approximated as 1 if flag set)

## Validation Rules
- Wellness data: ~1 entry per day (sometimes 2)
- Sleep data: 1 entry per night
- Run data: 0-N entries per day
- Dates are aligned via `calendarDate` field in all JSON objects
- Missing values are represented as NULL in Parquet