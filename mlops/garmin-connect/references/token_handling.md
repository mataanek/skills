# Token Handling in garminconnect Library

## Token Storage Locations

The `garminconnect` library stores OAuth tokens in different locations depending on the library version:

### 1. Newer Versions (Recommended)
- Direct attributes on the Garmin object:
  - `g.oauth1_token` (dict)
  - `g.oauth2_token` (dict)

### 2. Older Versions
- Via the `garth` attribute:
  - `g.garth.oauth1_token` (dict)
  - `g.garth.oauth2_token` (dict)

### 3. Low-level Client Attributes (Fallback)
- Access token: `g.client.di_token`
- Refresh token: `g.client.di_refresh_token`
- Token expiration: `g.client.di_token_expires_at` (Unix timestamp)
- CSRF token: `g.client.csrf_token`

## Token Structure

### oauth1_token.json
```json
{
  "csrf_token": "actual_csrf_token_string_here"
}
```

### oauth2_token.json
```json
{
  "access_token": "actual_access_token_string",
  "refresh_token": "actual_refresh_token_string", 
  "expires_at": 1778476227,  // Unix timestamp (seconds since epoch)
  "token_type": "Bearer",
  "scope": ""
}
```

## Token Lifecycle

1. **Access Token** (`di_token`):
   - Short-lived (~20 minutes)
   - Automatically refreshed using refresh token
   - When expired (~0 or past timestamp), call `g.login()` to refresh

2. **Refresh Token** (`di_refresh_token`):
   - Long-lived (~24 hours)
   - Used to obtain new access tokens
   - When expired, requires full re-login with credentials + 2FA

3. **CSRF Token**:
   - Part of OAuth 1.0a flow
   - Remains valid until manually revoked

## Refreshing Tokens

To refresh an expired access token:

```python
try:
    g.login()  # Uses refresh token to get new access token
    # Extract refreshed tokens
    if hasattr(g, 'oauth1_token'):
        oauth1, oauth2 = g.oauth1_token, g.oauth2_token
    elif hasattr(g, 'garth'):
        oauth1, oauth2 = g.garth.oauth1_token, g.garth.oauth2_token
    else:
        oauth1 = {'csrf_token': g.client.csrf_token}
        oauth2 = {
            'access_token': g.client.di_token,
            'refresh_token': g.client.di_refresh_token,
            'expires_at': g.client.di_token_expires_at,
            'token_type': 'Bearer',
            'scope': ''
        }
    # Save refreshed tokens to files
except GarminConnectAuthenticationError:
    # Refresh token also expired - need full re-login
```

## Determining Token Validity

Check if access token is expired or expiring soon:

```python
import time
now = time.time()
expires_at = g.client.di_token_expires_at
if expires_at == 0 or (expires_at - now) < 60:  # Less than 60 seconds left
    # Token is expired or about to expire - attempt refresh
```

## Version Detection

To handle different garminconnect versions gracefully:

```python
# Try newer version attribute access first
if hasattr(g, 'oauth1_token'):
    oauth1, oauth2 = g.oauth1_token, g.oauth2_token
# Fall back to garth attribute
elif hasattr(g, 'garth') and hasattr(g.garth, 'oauth1_token'):
    oauth1, oauth2 = g.garth.oauth1_token, g.garth.oauth2_token
# Fall back to low-level client attributes
else:
    oauth1 = {'csrf_token': getattr(g.client, 'csrf_token', '')}
    oauth2 = {
        'access_token': getattr(g.client, 'di_token', ''),
        'refresh_token': getattr(g.client, 'di_refresh_token', ''),
        'expires_at': getattr(g.client, 'di_token_expires_at', 0),
        'token_type': 'Bearer',
        'scope': ''
    }
```