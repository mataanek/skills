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

## When to Use This Skill

- You need continuous access to Garmin Connect data (heart rate, steps, stress, sleep, etc.)
- You want to avoid entering SMS codes every time you run a script
- You're building a coaching dashboard or real-time monitoring system
- You're operating in a headless environment (WSL, server, etc.) where interactive prompts aren't feasible

## Workflow Steps\n\n### 1. One-Time Initial Setup (Interactive)\n\nThis step must be performed once on a machine with a functional TTY (terminal) where you can enter credentials and SMS codes.\n\nSee `references/interactive_login_one_liner.md` for the exact command to run.\n\nAfter successful login, two token files will be created in `~/.garminconnect/`:\n- `oauth1_token.json`\n- `oauth2_token.json`\n\n### 2. Validate and Deploy Tokens to Target Environment\n\nAfter generating tokens, **verify they are valid** before copying:\n\n**oauth1_token.json** must contain:\n```json\n{\n  \"csrf_token\": \"actual_non_empty_string\"\n}\n```\n\n**oauth2_token.json** must contain:\n```json\n{\n  \"access_token\": \"actual_token_string\",\n  \"refresh_token\": \"actual_token_string\",\n  \"expires_at\": 1735689600,\n  \"token_type\": \"Bearer\",\n  \"scope\": \"\"\n}\n```\n\nWhere `expires_at` is a future Unix timestamp (current time + typically ~1 hour).\n\nIf you see `\"csrf_token\": null` or missing/empty values, or `expires_at`: 0, your tokens are invalid and you must repeat step 1.\n\nCopy the **validated** two token files from step 1 to the same path (`~/.garminconnect/`) on your target system (WSL, server, etc.) where you'll run the persistent connection.\n\n### 3. Persistent Connection Script (Non-Interactive)\n\nUse this script for continuous data access. It handles token refresh automatically and only requires interactive input if tokens fully expire (rare).

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

---

## References\\n- GarminConnect Python Library: https://pypi.org/project/garminconnect/\\n- Garmin Connect API Documentation (unofficial): Various community resources\\n- OAuth 2.0 Refresh Token Flow: Standard OAuth 2.0 specification\\n\\n## Related Skills\\n- `hermes-agent`: For configuring and extending the Hermes Agent framework itself\\n\\n## Support Files\\n- references/interactive_login_one_liner.md: One-liner for initial TTY-based login with SMS 2FA handling (includes robust CSRF token extraction)\\n- references/token_format.md: Example structure of oauth1_token.json and oauth2_token.json files\\n- references/token_directory.md: Guidance on handling custom token locations in different environments\\n- references/token_handling.md: Details on how the garminconnect library stores and manages tokens