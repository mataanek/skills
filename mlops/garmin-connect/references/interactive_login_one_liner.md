# One‑Liner Interactive Login (TTY required) - ROBUST TOKEN EXTRACTION
#
# Run this **once** on a machine where you can type (Windows PowerShell, local terminal, etc.):
#
python3 -c "
import getpass, os, time, json, base64
from garminconnect import Garmin, GarminConnectAuthenticationError, GarminConnectTooManyRequestsError

def mfa_prompt():
    return input('Enter the 6-digit SMS code: ').strip()

email    = input('Garmin email: ').strip()
password = getpass.getpass('Garmin password: ')

# Exponential back-off for 429 responses
backoff = 5
while True:
    try:
        g = Garmin(email, password, prompt_mfa=mfa_prompt)
        g.login()                     # will invoke mfa_prompt if 2FA needed
        print('[OK] Login succeeded')
        break                         # exit retry loop
    except GarminConnectTooManyRequestsError:
        print(f'[WARN] Garmin rate-limited (429). Waiting {backoff}s then retrying...')
        time.sleep(backoff)
        backoff = min(backoff * 2, 300)   # cap at 5 min
    except GarminConnectAuthenticationError as e:
        if 'Invalid credentials' in str(e):
            raise SystemExit('[ERROR] Wrong email/password.')
        print('[ERROR] Unexpected auth error:', e)
        raise

# Extract tokens - try multiple locations known to work with garminconnect
def extract_tokens(g):
    # Try 1: direct attributes on g (newer versions)
    if hasattr(g, 'oauth1_token') and hasattr(g, 'oauth2_token'):
        return g.oauth1_token, g.oauth2_token
    # Try 2: via garth (older versions)
    if hasattr(g, 'garth') and hasattr(g.garth, 'oauth1_token') and hasattr(g.garth, 'oauth2_token'):
        return g.garth.oauth1_token, g.garth.oauth2_token
    # Try 3: low-level client (fallback)
    oauth1 = {'csrf_token': getattr(g.client, 'csrf_token', '')}
    oauth2 = {
        'access_token': getattr(g.client, 'di_token', ''),
        'refresh_token': getattr(g.client, 'di_refresh_token', ''),
        'expires_at': getattr(g.client, 'di_token_expires_at', 0),
        'token_type': getattr(g.client, 'di_token_type', 'Bearer'),
        'scope': getattr(g.client, 'di_scope', '')
    }
    # If CSRF token is empty, try to get it from session cookies
    if not oauth1['csrf_token'] and hasattr(g.client, 'session') and hasattr(g.client.session, 'cookies'):
        cookies = g.client.session.cookies
        for cookie_name in ['csrftoken', 'csrf_token']:
            if cookie_name in cookies:
                oauth1['csrf_token'] = cookies[cookie_name]
                break
    # If CSRF token is still empty, try to get it from session headers
    if not oauth1['csrf_token'] and hasattr(g.client, 'session') and hasattr(g.client.session, 'headers'):
        for header, value in g.client.session.headers.items():
            if 'csrf' in header.lower() or 'xsrf' in header.lower():
                oauth1['csrf_token'] = value
                break
    # If CSRF token is still empty, try garth object
    if not oauth1['csrf_token'] and hasattr(g, 'garth') and hasattr(g.garth, 'csrf_token') and g.garth.csrf_token:
        oauth1['csrf_token'] = g.garth.csrf_token
    # Decode expiration from JWT if not set or zero
    if oauth2['expires_at'] == 0:
        token = oauth2['access_token']
        try:
            # Split JWT and decode payload
            parts = token.split('.')
            if len(parts) == 3:
                payload = parts[1]
                # Add padding
                payload += '=' * ((4 - len(payload) % 4) % 4)
                decoded = base64.urlsafe_b64decode(payload)
                data = json.loads(decoded)
                exp = data.get('exp')
                if exp:
                    oauth2['expires_at'] = exp
        except Exception:
            pass  # Keep expires_at as 0, will fallback below
    # Fallback expiration: 24 hours from now if still zero or in the past
    if oauth2['expires_at'] == 0 or oauth2['expires_at'] < time.time():
        oauth2['expires_at'] = int(time.time()) + 24 * 3600
    return oauth1, oauth2

oauth1, oauth2 = extract_tokens(g)

token_dir = os.path.expanduser('~/.garminconnect')
os.makedirs(token_dir, exist_ok=True)
with open(os.path.join(token_dir, 'oauth1_token.json'), 'w') as f:
    json.dump(oauth1, f, indent=2)
with open(os.path.join(token_dir, 'oauth2_token.json'), 'w') as f:
    json.dump(oauth2, f, indent=2)

print(f'[INFO] Tokens written to: {token_dir}')
print('   oauth1_token.json exists:', os.path.exists(os.path.join(token_dir, 'oauth1_token.json')))
print('   oauth2_token.json exists:', os.path.exists(os.path.join(token_dir, 'oauth2_token.json')))
"