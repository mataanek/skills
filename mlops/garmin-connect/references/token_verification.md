# Token Verification Guide for Garmin Connect

## Why Token Verification Matters

The `garminconnect` library requires:
1. A valid CSRF token in `oauth1_token.json` (non-empty string)
2. A valid access token with future expiration in `oauth2_token.json` (expires_at > current time)

Without these, you will experience:
- 403 Forbidden errors on endpoints like heart rate data
- Failed token refresh attempts
- Requirement for repeated interactive logins

## How to Verify Token Files

### Step 1: Check oauth1_token.json

```bash
cat ~/.hermes/.garminconnect/oauth1_token.json
```

**VALID example:**
```json
{
  "csrf_token": "actual_non_empty_string_here"
}
```

**INVALID examples:**
```json
{
  "csrf_token": null
}
```
```json
{
  "csrf_token": ""
}
```
```json
{
  "csrf_token": " "
}
```

### Step 2: Check oauth2_token.json

```bash
cat ~/.hermes/.garminconnect/oauth2_token.json
```

**VALID example:**
```json
{
  "access_token": "actual_jwt_token_string",
  "refresh_token": "actual_refresh_token_string",
  "expires_at": 1735689600,
  "token_type": "Bearer",
  "scope": ""
}
```
Where `expires_at` is a future Unix timestamp (e.g., current time + 1 hour).

**INVALID examples:**
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "expires_at": 0,
  "token_type": "Bearer",
  "scope": ""
}
```
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "expires_at": 1234567890,  // Past timestamp
  "token_type": "Bearer",
  "scope": ""
}
```

### Step 3: Quick Validation Script

Save this as `verify_garmin_tokens.py` and run it:

```python
#!/usr/bin/env python3
import json
import os
import time

TOKEN_DIR = os.path.expanduser("~/.hermes/.garminconnect")

def verify_tokens():
    # Check oauth1
    oauth1_path = os.path.join(TOKEN_DIR, "oauth1_token.json")
    if not os.path.exists(oauth1_path):
        print("❌ oauth1_token.json not found")
        return False
        
    with open(oauth1_path) as f:
        oauth1 = json.load(f)
    
    csrf_token = oauth1.get("csrf_token")
    if not csrf_token or not isinstance(csrf_token, str) or csrf_token.strip() == "":
        print(f"❌ Invalid CSRF token: {repr(csrf_token)}")
        print("   Must be a non-empty string")
        return False
    else:
        print(f"✅ CSRF token valid: {csrf_token[:10]}... (length: {len(csrf_token)})")
    
    # Check oauth2
    oauth2_path = os.path.join(TOKEN_DIR, "oauth2_token.json")
    if not os.path.exists(oauth2_path):
        print("❌ oauth2_token.json not found")
        return False
        
    with open(oauth2_path) as f:
        oauth2 = json.load(f)
    
    access_token = oauth2.get("access_token")
    refresh_token = oauth2.get("refresh_token")
    expires_at = oauth2.get("expires_at", 0)
    
    if not access_token or not isinstance(access_token, str):
        print("❌ Invalid access_token")
        return False
        
    if not refresh_token or not isinstance(refresh_token, str):
        print("❌ Invalid refresh_token")
        return False
    
    now = time.time()
    if expires_at == 0:
        print("❌ expires_at is 0 (token cannot be refreshed)")
        return False
    elif expires_at <= now:
        print(f"❌ Token expired: expires_at={expires_at}, now={int(now)}")
        return False
    else:
        time_left = expires_at - now
        hours_left = time_left / 3600
        print(f"✅ Tokens valid: {hours_left:.1f} hours until expiry")
        return False if hours_left < 0.1 else True  # Warn if < 6 minutes

if __name__ == "__main__":
    if verify_tokens():
        print("\n🎉 All tokens are valid and ready for use!")
        exit(0)
    else:
        print("\n💥 Token verification failed - see errors above")
        exit(1)
```

Run it with: `python3 verify_garmin_tokens.py`

## Regenerating Invalid Tokens

If verification fails:

1. **On Windows host** (where you have TTY for SMS entry):
   ```powershell
   # Run the interactive login one-liner from skill references
   python3 -c "$(hermes skill view garmin-connect --file references/interactive_login_one_liner.md)"
   ```

2. **Verify the generated tokens** using the script above

3. **Copy to WSL**:
   ```powershell
   copy C:\Users\mataa\.garminconnect\oauth1_token.json \\wsl$\Ubuntu\home\mataanek\.hermes\.garminconnect\
   copy C:\Users\mataa\.garminconnect\oauth2_token.json \\wsl$\Ubuntu\home\mataanek\.hermes\.garminconnect\
   ```

4. **Re-verify in WSL**:
   ```bash
   python3 /home/mataanek/.hermes/skills/mlops/garmin-connect/references/verify_garmin_tokens.py
   ```

## Common Pitfalls

### Pitfall: Assuming token generation succeeded without verification
**Symptom**: Script runs but gets 403 errors on heart rate data  
**Fix**: Always verify token contents after generation - look for non-empty CSRF token and future expires_at

### Pitfall: Copying tokens before verifying they're valid
**Symptom**: Persistent script immediately asks for re-login  
**Fix**: Verify tokens on the generation machine FIRST, then copy

### Pitfall: Using tokens with expires_at: 0
**Symptom**: "Token refresh failed – interactive re-login required" loop  
**Fix**: Regenerate tokens - a valid OAuth 2.0 access token MUST have a future expiration time

## Quick Reference

| File | Required Field | Valid Value |
|------|----------------|-------------|
| oauth1_token.json | csrf_token | Non-empty string (e.g., "a1b2c3d4...") |
| oauth2_token.json | expires_at | Future Unix timestamp (e.g., 1735689600) |
| oauth2_token.json | access_token | Non-empty JWT string |
| oauth2_token.json | refresh_token | Non-empty string |

**Never accept**: null, "", 0, or missing fields