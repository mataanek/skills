# Token File Format Reference

After successful interactive login with the Garmin Connect API, two JSON token files are created:

## oauth1_token.json
Contains OAuth 1.0a tokens (long-lived, until manually revoked):
```json
{
  "csrf_token": "string_or_null"
}
```
- `csrf_token`: Cross-site request forgery token used for OAuth 1.0a authentication

## oauth2_token.json
Contains OAuth 2.0 tokens:
- `access_token`: Short-lived token (~20 minutes) used for API calls
- `refresh_token`: Long-lived token (~24 hours) used to refresh the access token
- `expires_at`: Unix timestamp when the access token expires
- `token_type`: Usually "Bearer"
- `scope`: Space-separated list of permissions granted

Example structure:
```json
{
  "access_token": "ya29.a0AfH6SMB...",
  "refresh_token": "1//04gGgGgGgGgGgGgGgGgGgGgGgGgGgGgGgGgGgGgGg",
  "expires_at": 1735689600,
  "token_type": "Bearer",
  "scope": "https://www.googleapis.com/auth/userinfo.profile"
}
```

Note: The actual Garmin Connect tokens may have different field names or additional fields depending on the library version. The `garminconnect` Python library handles the internal format, so you rarely need to inspect these files directly unless debugging.

Both files should be treated as sensitive credentials - anyone with access to these files can access your Garmin Connect data.