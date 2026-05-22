---
name: garmin-connect
description: "Workflow for establishing and maintaining a persistent connection to Garmin Connect for health/fitness data retrieval"
version: 1.1.0
author: Nix (Hermes Agent)
license: MIT
metadata:
  hermes:
    tags: [garmin, fitness, health-data, api, authentication, polling]
    related_skills: [hermes-agent]
---

# Garmin Connect Persistent Connection Workflow

This skill provides a complete workflow for establishing a persistent, low-maintenance connection to Garmin Connect to retrieve real-time health and fitness data for coaching applications. It handles the initial 2FA authentication, token persistence, automatic refresh, and polling patterns needed for continuous data access.

## Overview

 Garmin Connect uses OAuth 1.0a and OAuth 2.0 for authentication. After initial login (which may require SMS 2FA), the `garminconnect` Python library saves tokens that can be reused and refreshed automatically, eliminating the need for repeated SMS prompts.

 ## Limitations and Pitfalls\n\n- **TTY REQUIRED for Token Generation**: The interactive login process (OAuth flow) **requires a terminal with TTY**. In headless environments (e.g., WSL without a terminal, cron jobs, or SSH without `-t`), token generation **will fail with EOFError**. \n  - **MANDATORY PROCEDURE**: Generate tokens ONLY on a machine with TTY (Windows PowerShell recommended for SMS entry) where you can complete the full interactive login. **Never attempt token generation in headless WSL environments.**\n  - **VERIFICATION IS NON-NEGOTIABLE**: Immediately after token generation, you **MUST verify** the token files contain:\n    * A non-empty string in `oauth1_token.json.csrf_token` (not null or \"\")\n    * A future Unix timestamp in `oauth2_token.json.expires_at` (not 0 or expired)\n  - **Copy ONLY verified tokens** to your target environment. Copying unverified tokens leads to persistent script failures and repeated interactive login requirements.

- **CSRF Token Extraction Failure**: If after running the interactive login one-liner the `oauth1_token.json` still shows `csrf_token: null` or empty string, the CSRF token was not extracted successfully. This causes 403 Forbidden errors on endpoints like heart rate data. To fix, repeat the login and ensure the script output includes messages like "Found CSRF token via ..." before writing tokens. You can also manually extract the CSRF token from the session cookies (`g.client.session.cookies.get('csrftoken')`) after login and set it in the oauth1 JSON.\n\n ## When to Use This Skill\n\n- You need continuous access to Garmin Connect data (heart rate, steps, stress, sleep, etc.)\n- You want to avoid entering SMS codes every time you run a script\n- You're building a coaching dashboard or real-time monitoring system\n- You're operating in a headless environment (WSL, server, etc.) where interactive prompts aren't feasible\n- **CRITICAL**: You understand that token generation MUST occur in a TTY environment (Windows PowerShell recommended) and tokens MUST be verified before copying to your target environment\n\n## Workflow Steps\\\\n\\\\n### 1. One-Time Initial Setup (Interactive - RECOMMENDED ON WINDOWS HOST)\\\\n\\\\n**For headless environments like WSL, perform this step on a Windows host (or any machine with TTY) where you can enter credentials and SMS codes.** This avoids the `EOFError` that occurs in non-interactive terminals.\\\\n\\\\nSee `references/interactive_login_one_liner.md` for the exact command to run.\\\\n\\\\nAfter successful login, two token files will be created in `~/.garminconnect/` (on the Windows host):\\\\n- `oauth1_token.json`\\\\n- `oauth2_token.json`\\\\n\\\\n### 2. Verify Token Validity (CRITICAL STEP - DO ON WINDOWS HOST)\\n\\\\n**Before copying tokens to your target environment (WSL), you MUST verify they are valid on the Windows host.** Invalid tokens will cause persistent scripts to fail and require repeated interactive logins.\\\\n\\\\nUse the verification script:\\\\n```bash\\\\npython3 /home/mataanek/.hermes/skills/mlops/garmin-connect/references/token_verification.md\\\\n```\\\\n\\\\nOr run the embedded verification script directly:\\\\n\\\\n**oauth1_token.json** must contain:\\\\n```json\\\\n{\\\\n  \\\\\\\"csrf_token\\\\\\\": \\\\\\\"actual_non_empty_string\\\\\\\"\\\\n}\\\\n```\\\\n\\\\n**oauth2_token.json** must contain:\\\\n```json\\\\n{\\\\n  \\\\\\\"access_token\\\\\\\": \\\\\\\"actual_token_string\\\\\\\",\\\\n  \\\\\\\"refresh_token\\\\\\\": \\\\\\\"actual_token_string\\\\\\\",\\\\n  \\\\\\\"expires_at\\\\\\\": 1735689600,\\\\n  \\\\\\\"token_type\\\\\\\": \\\\\\\"Bearer\\\\\\\",\\\\n  \\\\\\\"scope\\\\\\\": \\\\\\\"\\\\\\\"\\\\n}\\\\n```\\\\n\\\\nWhere `expires_at` is a future Unix timestamp (current time + typically ~1 hour).\\\\n\\\\nIf you see `\\\\\\\"csrf_token\\\\\\\": null` or missing/empty values, or `expires_at`: 0, your tokens are invalid and you must repeat step 1 on the Windows host.\\\\n\\\\n### 3. Deploy Validated Tokens to Target Environment\\\\n\\\\nCopy the **verified** two token files from the Windows host to the same path (`~/.garminconnect/`) on your target system (WSL, server, etc.) where you'll run the persistent connection.\\\\n\\\\n**Important Path Handling for WSL:**\\\\n- When copying from Windows PowerShell to WSL, use the `\\\\wsl$\\` path format (e.g., `\\\\wsl$\\Ubuntu\\home\\mataanek\\.hermes\\.garminconnect\\`)\\\\n- Do NOT use `/mnt/c/` style paths when copying from PowerShell to WSL - they won't work correctly\\\\n- From PowerShell: `copy C:\\Users\\mataa\\.garminconnect\\oauth*.json \\\\wsl$\\Ubuntu\\home\\mataanek\\.hermes\\.garminconnect\\`\\\\n- From WSL bash: `cp /mnt/c/Users/mataa/.garminconnect/oauth*.json /home/mataanek/.hermes/.garminconnect/`\\\\n\\\\n**Never copy unverified tokens.** Always run verification on the Windows host (where tokens were generated) before copying to WSL.\\\\n\\\\n### 4. Running the Persistent Connection

```python
# garmin_persistent.py
import os, json, time
from garminconnect import Garmin, GarminConnectAuthenticationError, GarminConnectTooManyRequestsError

TOKEN_DIR = os.path.expanduser("~/.garminconnect")
EMAIL = "your_garmin_email@example.com"  # UPDATE THIS

def load_tokens():
    try:
        with open(os.path.join(TOKEN_DIR, "oauth1_token.json")) as f:
            oauth1 = json.load(f)
        with open(os.path.join(TOKEN_DIR, "oauth2_token.json")) as f:
            oauth2 = json.load(f)
        return oauth1, oauth2
    except FileNotFoundError:
        return None, None

def save_tokens(oauth1, oauth2):
    os.makedirs(TOKEN_DIR, exist_ok=True)
    with open(os.path.join(TOKEN_DIR, "oauth1_token.json"), "w") as f:
        json.dump(oauth1, f)
    with open(os.path.join(TOKEN_DIR, "oauth2_token.json"), "w") as f:
        json.dump(oauth2, f)

# Load existing tokens
oauth1, oauth2 = load_tokens()
if not (oauth1 and oauth2):
    raise SystemExit(
        "❌ No token files found. Complete step 1 (interactive login) first, "
        "then copy oauth1_token.json and oauth2_token.json to ~/.garminconnect/"
    )

# Initialize Garmin client with loaded tokens\ng = Garmin(EMAIL, None)  # Password not needed - using tokens\n# Set tokens on the client's internal auth object\ng.client.di_token = oauth2.get('access_token')\ng.client.di_refresh_token = oauth2.get('refresh_token')\ng.client.di_token_expires_at = oauth2.get('expires_at', 0)\ng.client.csrf_token = oauth1.get('csrf_token')

def refresh_tokens():
    """Refresh access token using refresh token; returns True if successful"""
    try:
        g.login()  # Attempts to refresh using stored refresh token
        save_tokens(g.garth.oauth1_token, g.garth.oauth2_token)
        return True
    except GarminConnectAuthenticationError:
        return False  # Tokens expired - need full re-login
    except GarminConnectTooManyRequestsError:
        return False  # Rate limited - try again later

# Initial token validation
if not refresh_tokens():
    raise SystemExit(
        "🔑 Tokens expired or invalid. Repeat step 1 (interactive login) "
        "to generate new tokens, then copy them to the target environment."
    )

# ----- DATA POLLING LOOP -----
def get_latest_heart_rate():
    """Get most recent heart rate reading"""
    data = g.get_heart_rates()
    return data.get('lastHeartRateValue')

def get_daily_steps():
    """Get today's step count"""
    data = g.get_steps()
    return data.get('totalSteps')

def get_stress_score():
    """Get current stress score (0-100)"""
    try:
        data = g.get_stress()
        return data.get('stressLevel')
    except:
        return None  # May not be available on all devices/devices

# Main polling loop
POLL_INTERVAL = 20  # seconds - adjust based on your needs and rate limit tolerance

print("🔄 Starting Garmin Connect data polling...")
print(f"   Polling interval: {POLL_INTERVAL}s")
print("   Press Ctrl+C to stop\n")

try:
    while True:
        try:
            # Fetch data
            hr = get_latest_heart_rate()
            steps = get_daily_steps()
            stress = get_stress_score()
            
            # Format output (customize as needed for your application)
            timestamp = time.strftime("%H:%M:%S")
            output = f"[{timestamp}]"
            if hr is not None:
                output += f" HR:{hr}bpm"
            if steps is not None:
                output += f" Steps:{steps}"
            if stress is not None:
                output += f" Stress:{stress}"
                
            print(output)
            
        except GarminConnectTooManyRequestsError:
            print("⚠️  Rate limit hit - backing off for 60s")
            time.sleep(60)
        except GarminConnectAuthenticationError:
            print("🔑 Auth error - attempting token refresh...")
            if not refresh_tokens():
                print("❌ Token refresh failed - interactive re-login required")
                break  # Exit loop - user must repeat step 1
        except Exception as e:
            print(f"❗ Unexpected error: {e}")
            
        time.sleep(POLL_INTERVAL)
except KeyboardInterrupt:
    print("\n👋 Polling stopped by user")
```

### 4. Running the Persistent Connection

```bash
# Make sure EMAIL in the script matches your Garmin account
# Make sure token files are in ~/.garminconnect/
python3 garmin_persistent.py
```

## Key Technical Details

### Token Lifespan

- **OAuth 1 token**: Long-lived (until manually revoked)
- **OAuth 2 access token**: Short-lived (~20 minutes) but automatically refreshed using the refresh token
- **OAuth 2 refresh token**: Long-lived (~24 hours) - when this expires, you'll need to repeat the interactive login

### Token Location

The `garminconnect` library stores tokens in `$HOME/.garminconnect` by default. However, in environments where `$HOME` is customized (like Hermes Agent which sets `HOME` to `/home/mataanek/.hermes/home`), tokens may appear in unexpected locations. 

To determine where tokens are being stored or to specify a custom location:
- Run `python3 -c "import os; print(os.path.expanduser('~/.garminconnect'))"` to see the expected directory
- After interactive login, note the directory printed by the one-liner (`💾 Tokens written to:`)
- For persistent scripts, either:
  a) Copy tokens to the expected directory, or
  b) Set `TOKEN_DIR` explicitly in your script to match where the tokens are stored

See `references/token_directory.md` for detailed guidance on handling custom token locations.

### Rate Limits

Garmin Connect enforces rate limits. To avoid 429 errors:
- Keep polling interval ≥ 15-20 seconds for individual endpoints
- Consider batching requests when possible
- Implement exponential backoff on 429 responses (as shown in the script)

### Data Availability

Not all metrics are available on all devices or in all regions. Commonly available:
- Heart rate (`get_heart_rates()`)
- Steps (`get_steps()`)
- Stress (`get_stress()`)
- Sleep (`get_sleep_data()`)
- Body battery (`get_body_battery()`)
- VO2 max (`get vo2max()` - may require premium)

## Troubleshooting

| Symptom | Solution |\n|---------|----------|\n| `ModuleNotFoundError: No module named 'garminconnect'` | Run `pip install garminconnect` |\n| `EOFError` when prompting for input | You're in a headless environment - use the token-based approach described above |\n| `429 Too Many Requests` | Increase polling interval or add backoff logic |\n| `401 Unauthorized` after initial success | Tokens expired - repeat step 1 to get new tokens |\n| Missing data fields | Check if your Garmin device/supports that metric; some require premium subscription |\n| `csrf_token: null` or empty string in oauth1_token.json | CSRF token not extracted properly during login. This causes 403 Forbidden errors on endpoints like heart rate data. **Follow this diagnostic procedure:**\\n\\n1. **Immediately after token generation**, verify the script output shows successful CSRF extraction (look for "Found CSRF token via ..." messages)\\n\\n2. **If tokens show `csrf_token: null` or `expires_at: 0`:**\\n   - Run the diagnostic script: `python debug_tokens.py` (or `debug_csrf.py`)\\n   - After login, examine the output for:\\n     * `g.client.csrf_token` or `g.client.csrftoken` values\\n     * Session headers containing `X-CSRF-Token` or similar\\n     * Session cookies containing `csrftoken`\\n     * `g.garth.csrf_token` if garth object exists\\n     * `di_token_expires_at` value after login\\n     * JWT expiration from decoding `di_token` (access token)\\n\\n3. **Manual token construction workaround** (if automated extraction fails):\\n   - After `g.login()` in your script, manually extract:\\n     * CSRF token: Check `g.client.session.cookies` for `csrftoken` OR session headers for `X-CSRF-Token`\\n     * Access token expiration: Decode the JWT `di_token` (split by '.', base64url decode middle part, extract `exp` claim)\\n   - Write tokens with these manually extracted values\\n\\n4. **Verify before copying:** Always check that:\\n   - `oauth1_token.json` contains a non-empty string for `csrf_token` (not null or "")\\n   - `oauth2_token.json` has a future Unix timestamp in `expires_at` (not 0 or expired)\\n\\n5. **If all else fails**, repeat the interactive login on a Windows host (where TTY is available for SMS code entry) and use the debug script to inspect what's available before writing tokens. |

## Customization Tips

### For Coaching Applications

- Adapt the polling loop to push data to your UI via WebSocket, HTTP endpoint, or message queue
- Calculate derived metrics (e.g., training load from HR + time)
- Set alerts for abnormal values (e.g., unusually high HR at rest)

### Alternative Data Sources

If you need true push notifications (not polling):
- Explore Garmin's SDK for direct device communication via Bluetooth (more complex)
- Consider third-party services like Apple Health/Google Fit as intermediaries if you sync Garmin there

## Notes

- This workflow assumes you have basic Python knowledge and can run scripts in your environment
- Always treat token files like passwords - they provide access to your Garmin data
- If you revoke access in Garmin Connect web interface, all tokens become invalid
- The `garminconnect` library handles the OAuth dance automatically; you rarely need to interact with the raw tokens directly
- For historical data analysis, the Garmin GDPR export contains rich JSON files under `DI_CONNECT/` that can be parsed for longitudinal trends (see "Historical Data Analysis" below)

## Historical Data Analysis

## Data Lake and Daily Trend Analysis

For efficient repeated analysis, you can build a Parquet data lake from the raw Garmin GDPR export JSON files. This allows quick querying and trend computation without re-parsing all files each time.

### Building the Data Lake

Use the script `scripts/garmin_build_lake.py` to extract and aggregate data from the raw JSON files under `~/wiki/raw/garmin/` into a daily-level Parquet file at `~/data/garmin_lake/daily.parquet`. The lake includes columns for:

- Resting HR (from wellness snapshots or sleep average HR)
- Stress, SpO2, HRV (RMSSD/SDRR), respiration
- Sleep metrics (deep/light/REM/awake minutes)
- Workout metrics (steps, distance, duration, calories, avg/max/min HR, training effects, intensity minutes)
- Derived high-intensity run flags and volumes (based on calories/min > 8.0 or training status PRODUCTIVE/PEAKING)

The script handles merging multiple sources per day, filling missing resting HR from sleep data when wellness snapshots are missing, and computes daily aggregates.

### Daily Trend Analysis

Once the lake is built, you can compute daily correlations between resting HR and high-intensity run volume using `scripts/garmin_daily_trend.py`. This script:

- Reads the Parquet lake
- Computes a 30-day rolling Pearson correlation between resting HR and high-intensity run minutes
- Appends/updates a `## Daily Resting HR vs High-Intensity Run Trend (Garmin)` section in `~/wiki/personal/health.md`
- Shows the last 14 days with rolling correlation values

### Visualizing Resting HR Trends

To visualize resting HR development over arbitrary date ranges, use `scripts/plot_resting_hr_v2.py`. This script:

- Reads the Parquet lake
- Filters from a start date (default 2023-01-01) to today
- Plots daily resting HR (blue) and a 7-day rolling average (red)
- Saves the plot as `~/wiki/personal/garmin_resting_hr_2023_now_v2.png`

### Automation

You can schedule the lake build and trend update via cron jobs. For example, to rebuild the lake daily at 02:00 CET and update the trend at 02:30 CET:

```
0 2 * * * /home/mataanek/.hermes/skills/mlops/garmin-connect/scripts/garmin_build_lake.py
30 2 * * * /home/mataanek/.hermes/skills/mlops/garmin-connect/scripts/garmin_daily_trend.py
```

Note: The lake build is only needed when new raw export files are added; if you export infrequently, a monthly update may suffice.

See also the existing `garmin_persistent.py` script for live API polling if you prefer real-time data over historical analysis.

When working with Garmin Connect GDPR exports (like those found in `~/wiki/raw/garmin/`), you can extract longitudinal health and workout trends by parsing the JSON files in the `DI_CONNECT/` directory.

### Key Data Sources for Trend Analysis

1. **Wellness Snapshots & Sleep Data** (`DI_CONNECT/DI-Connect-Wellness/`)
   - `*_wellnessActivities.json`: Contains periodic health snapshots with:
     * `calendarDate`: Date of measurement
     * `summaryTypeDataList`: Array with objects for HEART_RATE (avg/min/max), RESPIRATION, STRESS, SPO2, RMSSD_HRV, SDRR_HRV
   - `*_sleepData.json`: Contains nightly sleep metrics:
     * `calendarDate`: Date of sleep
     * `deepSleepSeconds`, `lightSleepSeconds`, `remSleepSeconds`, `awakeSleepSeconds`
     * `sleepScores`: Overall, quality, duration, recovery, deep, rem, light scores
     * `spo2SleepSummary`: averageSPO2, averageHR, lowestSPO2 (when available)

2. **Workout/Activity Data** (`DI_CONNECT/DI-Connect-Fitness/` and `DI_CONNECT/DI-Connect-Fitness-VVFJR/`)
   - `*_summarizedActivities.json`: Contains detailed workout summaries:
     * `calendarDate`: Date of activity
     * `activityType`: e.g., "walking", "running", "cycling"
     * `sportType`: e.g., "STEPS", "CYCLING"
     * `duration`: Activity duration in milliseconds
     * `distance`: Distance in meters
     * `steps`: Step count (0 for non-stepping activities)
     * `calories`: Total calories burned
     * `avgSpeed`, `maxSpeed`: Speed in m/s
     * `elevationGain`, `elevationLoss`: Elevation in meters

3. **Training Status & Metrics** (`DI_CONNECT/DI-Connect-Metrics/`)
   - `*_TrainingHistory_*.json`: Daily training status:
     * `calendarDate`: Date
     * `sport`: e.g., "RUNNING"
     * `trainingStatus`: e.g., "RECOVERY", "MAINTAINING", "PRODUCTIVE"
     * `fitnessLevelTrend`: e.g., "NO_CHANGE", "IMPROVING"
   - `*_MetricsAcuteTrainingLoad_*.json`: Day-to-day training load
   - `*_EnduranceScore_*.json`: Endurance score time series

### Correlation Analysis Pattern

To correlate resting HR trends with high-intensity running (as requested in this session):

1. **Extract Daily Resting HR**:
   - Prefer wellness snapshots: find `summaryTypeDataList` entry where `summaryType` = "HEART_RATE", use `avgValue`
   - Fallback: use `averageHR` from `spo2SleepSummary` in sleep data when wellness snapshot missing

2. **Extract Daily High-Intensity Running**:
   - From summarized activities: filter for `activityType` = "running"
   - Calculate intensity: `calories` / (`duration` / 60000) → kcal/minute
   - Define high-intensity as intensity > 8.0 kcal/min (adjust based on fitness level)
   - Sum either count of high-intensity runs or total duration per day

3. **Aggregate to Weekly**:
   - Group daily data by ISO week (year, week)
   - Calculate weekly average resting HR
   - Sum weekly high-intensity run counts or durations

4. **Compute Correlation**:
   - Use Pearson correlation between weekly average resting HR and weekly high-intensity volume
   - Significant negative correlation suggests higher training load leads to elevated resting HR (potential overreaching)
   - Significant positive correlation suggests fitness improvements (more training capacity with lower resting HR)

### Example Extraction Logic

```python
import json
import glob
from datetime import datetime
import statistics

def extract_daily_resting_hr(json_path):
    """Extract resting HR from wellness snapshot or sleep data"""
    with open(json_path) as f:
        data = json.load(f)
    
    # Try wellness snapshot first
    if isinstance(data, list):
        for entry in data:
            if entry.get("calendarDate") == target_date:
                for summary in entry.get("summaryTypeDataList", []):
                    if summary.get("summaryType") == "HEART_RATE":
                        return summary.get("avgValue")
    
    # Fallback to sleep data
    if isinstance(data, list):
        for entry in data:
            if entry.get("calendarDate") == target_date:
                spo2_summary = entry.get("spo2SleepSummary", {})
                return spo2_summary.get("averageHR")
    return None

def extract_daily_high_intensity_runs(json_path):
    """Extract high-intensity run count from summarized activities"""
    with open(json_path) as f:
        data = json.load(f)
    
    high_intense_count = 0
    if isinstance(data, list):
        for activity in data:
            if activity.get("calendarDate") == target_date and \
               activity.get("activityType") == "running":
                duration_min = activity.get("duration", 0) / 60000
                if duration_min > 0:
                    intensity = activity.get("calories", 0) / duration_min
                    if intensity > 8.0:  # kcal/min threshold
                        high_intense_count += 1
    return high_intense_count
```

### Daily Trend Analysis (Alternative to Weekly)

For applications requiring daily granularity (e.g., tracking day-to-day readiness), you can compute a rolling correlation or simply plot the daily time series. The following approach yields a daily signal:

1. **Extract Daily Resting HR** as described above (prefer wellness snapshot, fallback to sleep average HR).
2. **Extract Daily High‑Intensity Running Volume**: sum either the count or total duration of runs where intensity (calories/min) > threshold.
3. **Compute a rolling correlation** (e.g., 30‑day window) between the two daily series to observe how the relationship evolves over time.
4. **Plot both series** with dual axes to visually inspect alignment.

An example script that implements this daily analysis and updates the health wiki is available in the skill’s `scripts/` directory as `garmin_daily_trend.py`. It reads the Garmin data lake (built via `garmin_build_lake.py`), calculates a 30‑day rolling Pearson correlation between resting HR and high‑intensity run minutes, and appends a formatted section to `/home/mataanek/.hermes/wiki/personal/health.md`.

See also the plotting script `plot_resting_hr_v2.py` for visualizing resting HR trends over arbitrary date ranges.


This approach allows you to build longitudinal trends from historical Garmin exports without relying solely on the live API, enabling deeper analysis of fitness patterns over months or years.

---

## Support Files\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n- references/interactive_login_one_liner.md: One-liner for initial TTY-based login with SMS 2FA handling (includes robust CSRF token extraction)\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n- references/token_format.md: Example structure of oauth1_token.json and oauth2_token.json files\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n- references/token_directory.md: Guidance on handling custom token locations in different environments\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n- references/token_handling.md: Details on how the garminconnect library stores and manages tokens\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n- references/token_verification.md: CRITICAL - Step-by-step guide to validate tokens before copying (MUST be used)\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n- references/wellness_data_structure.md: Empirical analysis of Garmin wellness/sleep JSON structure - shows exact paths for HRV, stress, and resting HR extraction
- references/hrv_stress_extraction.md: Detailed guide on extracting HRV (RMSSD_HRV, SDRR_HRV) and stress values from wellness snapshots\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n- references/health_status_data_structure.md: Structure of *_healthStatusData.json files containing weekly averaged HRV and other metrics\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n- references/hrv_stress_extraction.md: Detailed guide on extracting HRV (RMSSD_HRV, SDRR_HRV) and stress values from wellness snapshots\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n- scripts/garmin_daily_trend.py: Script to compute daily rolling correlation between resting HR and high-intensity run minutes and update the health wiki\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n- scripts/garmin_build_lake.py: Script to build the Garmin data lake (Parquet) from raw GDPR export JSON files\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n- scripts/plot_resting_hr_v2.py: Script to plot resting HR trends over a specified date range |
- scripts/verify_tokens.py: Script to verify token validity before use (checks CSRF token and expiration) |