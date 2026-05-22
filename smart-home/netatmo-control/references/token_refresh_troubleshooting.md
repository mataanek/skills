# Netatmo Token Refresh Troubleshooting

## Issue
During a cron job run, the Netatmo data collection script failed with:
```
ERROR: Failed to get stations data: {'error': 'API request failed: 403 {\r\n  \"error\": {\r\n    \"code\": 2,\r\n    \"message\": \"Invalid access token\"\r\n  }\r\n}'}
```
Even after attempting to refresh the access token using the refresh token, the new access token was still rejected as invalid.

## Root Cause
The refresh token itself had expired or been revoked, causing the token refresh endpoint to return a new access token that was not actually valid for the API (possibly due to account restrictions or token binding issues).

## Resolution Steps
1. **Re-authenticate using password grant**: Use the Netatmo username, password, client ID, and client secret to obtain a fresh access token and refresh token via the OAuth2 password grant type.
2. **Update the .env file**: Replace both `NETATMO_ACCESS_TOKEN` and `NETATMO_REFRESH_TOKEN` with the newly obtained values.
3. **Verify the new token**: Test the new access token against the `getstationsdata` endpoint to ensure it returns a successful response.

## Commands Used
```bash
# Request new tokens via password grant
curl -X POST "https://api.netatmo.com/oauth2/token" \
  -d "grant_type=password" \
  -d "username=mataanek@icloud.com" \
  -d "password=Misanthrope-01" \
  -d "client_id=6a08b1067990c5a01807db07" \
  -d "client_secret=3NQlMb6tOaRnC0ROx60syU8AGj4KHmRa8kye2yV" \
  -d "scope=read_station"

# Extract access_token and refresh_token from the JSON response
# Update .env file (manually or via script)
```

## Prevention
- Consider adding a fallback mechanism in `register_netatmo_tools.py` to detect repeated token failures and trigger password grant re-authentication.
- Monitor token expiration times and proactively refresh before expiry.