# CSRF Token Troubleshooting for Garmin Connect

## Symptom
- Heart rate and steps endpoints return 403 Forbidden
- Stress and sleep endpoints may still work
- oauth1_token.json shows `"csrf_token": null` or empty string `""`
- oauth2_token.json may have `"expires_at": 0`

## Root Cause
The garminconnect library failed to extract a valid CSRF token during the OAuth login flow. Without a valid CSRF token, certain endpoints (notably heart rate and steps) reject requests with 403, while others may still succeed.

## Immediate Fix (Manual Token Construction)
If automated token generation produces invalid CSRF or expiration, you can manually construct valid tokens after login:

```python
from garminconnect import Garmin
import json
import time

# Perform login as usual
g = Garmin(email, password)  # or use existing tokens
g.login()  # This should populate g.garth and g.client

# Extract CSRF token - check multiple possible locations
csrf_token = None
# 1. Check client session cookies
if hasattr(g.client, 'session') and hasattr(g.client.session, 'cookies'):
    cookies = g.client.session.cookies
    for cookie in cookies:
        if cookie.name == 'csrftoken':
            csrf_token = cookie.value
            break
# 2. Check client attribute
if not csrf_token and hasattr(g.client, 'csrf_token'):
    csrf_token = g.client.csrf_token
# 3. Check garth object
if not csrf_token and hasattr(g.garth, 'csrf_token'):
    csrf_token = g.garth.csrf_token

# Extract access token expiration from JWT
access_token = g.client.di_token
expires_at = 0
if access_token:
    try:
        # JWT is base64url encoded header.payload.signature
        _, payload, _ = access_token.split('.')
        # Add padding if needed
        missing_padding = len(payload) % 4
        if missing_padding:
            payload += '=' * (4 - missing_padding)
        import base64
        import json
        decoded = base64.b64decode(payload)
        payload_json = json.loads(decoded)
        expires_at = payload_json.get('exp', 0)
    except Exception as e:
        print(f"Could not decode JWT: {e}")

# Write tokens with manually extracted values
oauth1 = {"csrf_token": csrf_token}
oauth2 = {
    "access_token": access_token,
    "refresh_token": g.client.di_refresh_token,
    "expires_at": expires_at,
    "token_type": "Bearer",
    "scope": ""
}

# Save to ~/.garminconnect/
import os
token_dir = os.path.expanduser("~/.garminconnect")
os.makedirs(token_dir, exist_ok=True)
with open(os.path.join(token_dir, "oauth1_token.json"), "w") as f:
    json.dump(oauth1, f)
with open(os.path.join(token_dir, "oauth2_token.json"), "w") as f:
    json.dump(oauth2, f)

print("Tokens written with CSRF:", bool(csrf_token and csrf_token != ""), "expires_at:", expires_at)
```

## Verification
Always verify tokens before copying to target environment:
- `oauth1_token.json.csrf_token` must be a non-empty string (not null, not "")
- `oauth2_token.json.expires_at` must be a future Unix timestamp (e.g., `$(date -d '+1 hour' +%s)`)

## Prevention
- Perform token generation only in a TTY environment (Windows PowerShell recommended)
- Immediately after generation, verify token contents
- Never copy unverified tokens

## References
- Session debug: heart rate/steps 403 while stress/sleep worked
- Garmin Connect API requires CSRF token for certain endpoints