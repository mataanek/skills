# Manual Token Refresh Procedure

When the automatic token refresh in `register_netatmo_tools.py` fails (e.g., due to network issues or token corruption), you can manually obtain new tokens using the password grant type and update the `.env` file.

## Steps

1. **Check current tokens** (optional):
   ```bash
   cat /home/mataanek/.hermes/.env | grep NETATMO
   ```

2. **Run a manual token refresh script** (or execute the following commands):
   ```python
   import os
   import requests

   env_file = '/home/mataanek/.hermes/.env'
   creds = {}
   with open(env_file, 'r') as f:
       for line in f:
           if '=' in line:
               k, v = line.strip().split('=', 1)
               creds[k] = v

   username = creds.get('NETATMO_USERNAME')
   password = creds.get('NETATMO_PASSW')
   client_id = creds.get('NETATMO_CLIENT_ID')
   client_secret = creds.get('NETATMO_CLIENT_SECRET')
   refresh_token = creds.get('NETATMO_REFRESH_TOKEN')

   token_url = 'https://api.netatmo.com/oauth2/token'

   # Try refresh token first
   data = {
       'grant_type': 'refresh_token',
       'refresh_token': refresh_token,
       'client_id': client_id,
       'client_secret': client_secret
   }
   resp = requests.post(token_url, data=data)
   if resp.status_code == 200:
       token_data = resp.json()
       new_access = token_data.get('access_token')
       new_refresh = token_data.get('refresh_token', refresh_token)
   else:
       # Fall back to password grant
       data = {
           'grant_type': 'password',
           'username': username,
           'password': password,
           'client_id': client_id,
           'client_secret': client_secret,
           'scope': 'read_station'
       }
       resp = requests.post(token_url, data=data)
       if resp.status_code == 200:
           token_data = resp.json()
           new_access = token_data.get('access_token')
           new_refresh = token_data.get('refresh_token')
       else:
           raise Exception(f"Token acquisition failed: {resp.text}")

   # Update .env file
   with open(env_file, 'r') as f:
       lines = f.readlines()
   for i, line in enumerate(lines):
       if line.startswith('NETATMO_ACCESS_TOKEN='):
           lines[i] = f'NETATMO_ACCESS_TOKEN={new_access}\\n'
       if line.startswith('NETATMO_REFRESH_TOKEN='):
           lines[i] = f'NETATMO_REFRESH_TOKEN={new_refresh}\\n'
   with open(env_file, 'w') as f:
       f.writelines(lines)

   print("Tokens updated successfully.")
   ```

3. **Verify** by running the Netatmo data collection script again:
   ```bash
   python3 /home/mataanek/.hermes/skills/smart-home/netatmo-control/scripts/collect_netatmo_data.py
   ```

## Notes

- The `.env` file is located at `/home/mataanek/.hermes/.env`.
- Ensure you have the `requests` Python library installed (it is available in the Hermes environment).
- This procedure is also documented in the skill's pitfalls section under "Token refresh may fail".