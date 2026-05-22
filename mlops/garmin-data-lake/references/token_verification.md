# Garmin Connect Token Verification

## Required Token Files
- `oauth1_token.json` - Must contain a non-empty `csrf_token` string
- `oauth2_token.json` - Must contain a future `expires_at` timestamp (Unix epoch)

## Verification Checks
1. **CSRF Token Check**: `oauth1_token.json.csrf_token` must be a non-empty string
2. **Expiration Check**: `oauth2_token.json.expires_at` must be a future timestamp (greater than current Unix time)

## Common Issues
- Empty CSRF token (`""`) → prevents proper authentication → 403 Forbidden on HR/endpoints
- `expires_at: 0` or past timestamp → token cannot be refreshed → requires interactive re-login
- Missing files → token generation required

## How to Generate Valid Tokens
1. Use the interactive one-liner on a TTY-enabled system (Windows PowerShell or local terminal):
   ```bash
   python3 -c "$(hermes skill view garmin-connect --file references/interactive_login_one_liner.md)"
   ```
2. This will launch a browser for Garmin login and save token files to `~/.garminconnect/`
3. Copy the generated files to `/home/mataanek/.hermes/.garminconnect/`:
   ```bash
   cp /mnt/c/Users/<username>/.garminconnect/oauth1_token.json /home/mataanek/.hermes/.garminconnect/
   cp /mnt/c/Users/<username>/.garminconnect/oauth2_token.json /home/mataanek/.hermes/.garminconnect/
   ```

## Token Refresh Mechanism
The garminconnect library automatically refreshes access tokens when:
- CSRF token is valid (non-empty)
- Current access token is expired or expiring soon
- Refresh token is available and valid

If either token is invalid, the library will throw an error requiring interactive re-login.

## Verification Script
Run `python3 scripts/verify_garmin_tokens.py` to automatically check token validity.