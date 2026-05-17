#!/usr/bin/env python3
"""
Garmin Connect persistent connection for real-time data export.
Handles token refresh automatically and provides data polling for training planning.

Usage:
    python3 garmin_persistent.py

The script expects token files in TOKEN_DIR (default: ~/.hermes/.garminconnect)
Set GARMIN_EMAIL environment variable or edit the EMAIL constant below.
"""

import json
import os
import time
from garminconnect import Garmin, GarminConnectAuthenticationError, GarminConnectTooManyRequestsError

# ------------------- CONFIG -------------------
TOKEN_DIR = os.path.expanduser("~/.hermes/.garminconnect")
# Set your Garmin email here or via GARMIN_EMAIL environment variable
EMAIL = os.environ.get("GARMIN_EMAIL", "mataanek@icloud.com")  # <-- your Garmin login
POLL_INT = 20  # seconds between polls (adjust as you like)
# ------------------------------------------------

def load_tokens():
    """Load OAuth tokens from JSON files."""
    try:
        with open(os.path.join(TOKEN_DIR, "oauth1_token.json")) as f:
            oauth1 = json.load(f)
        with open(os.path.join(TOKEN_DIR, "oauth2_token.json")) as f:
            oauth2 = json.load(f)
        return oauth1, oauth2
    except FileNotFoundError:
        return None, None

def save_tokens(oauth1, oauth2):
    """Save OAuth tokens to JSON files."""
    os.makedirs(TOKEN_DIR, exist_ok=True)
    with open(os.path.join(TOKEN_DIR, "oauth1_token.json"), "w") as f:
        json.dump(oauth1, f)
    with open(os.path.join(TOKEN_DIR, "oauth2_token.json"), "w") as f:
        json.dump(oauth2, f)

def ensure_client():
    """
    Return a logged-in Garmin client, creating tokens if needed.
    Handles token refresh and falls back to interactive login if tokens expired.
    """
    oauth1, oauth2 = load_tokens()
    if not (oauth1 and oauth2):
        print("⚠️  No token files found. Interactive login required.")
        print("Please run the interactive login one-liner first:")
        print("  python3 -c \\\"$(hermes skill view garmin-connect --file references/interactive_login_one_liner.md)\\\"")
        raise SystemExit(
            "❌ Interactive login required. Run the one-liner above on a machine with TTY access."
        )
    
    g = Garmin(EMAIL, None)  # password not needed if we have tokens
    
    # Set tokens on the client's internal auth object
    g.client.di_token = oauth2.get('access_token')
    g.client.di_refresh_token = oauth2.get('refresh_token')
    g.client.di_token_expires_at = oauth2.get('expires_at', 0)
    g.client.csrf_token = oauth1.get('csrf_token')
    
    # Check if access token is expired (or about to expire)
    now = time.time()
    expires_at = g.client.di_token_expires_at
    if expires_at == 0 or (expires_at - now) < 60:  # less than 60 seconds left
        print("🔑 Access token expired or expiring soon – attempting to refresh...")
        try:
            g.login()  # try to refresh access token using refresh token
            # Save refreshed tokens
            oauth1 = {'csrf_token': g.client.csrf_token}
            oauth2 = {
                'access_token': g.client.di_token,
                'refresh_token': g.client.di_refresh_token,
                'expires_at': g.client.di_token_expires_at,
                'token_type': 'Bearer',
                'scope': ''
            }
            save_tokens(oauth1, oauth2)
            print("🔐 Token refresh successful.")
            return g
        except GarminConnectAuthenticationError:
            print("❌ Token refresh failed – interactive re-login required.")
            raise SystemExit(
                "❌ Interactive login required. Run the one-liner above on a machine with TTY access."
            )
        except GarminConnectTooManyRequestsError:
            print("⚠️  Rate limit hit during token refresh – backing off for 60s")
            time.sleep(60)
            # Try once more after backoff
            try:
                g.login()
                oauth1 = {'csrf_token': g.client.csrf_token}
                oauth2 = {
                    'access_token': g.client.di_token,
                    'refresh_token': g.client.di_refresh_token,
                    'expires_at': g.client.di_token_expires_at,
                    'token_type': 'Bearer',
                    'scope': ''
                }
                save_tokens(oauth1, oauth2)
                print("🔐 Token refresh successful after backoff.")
                return g
            except Exception as e:
                print(f"❌ Token refresh failed after backoff: {e}")
                raise SystemExit(
                    "❌ Interactive login required. Run the one-liner above on a machine with TTY access."
                )
    else:
        print("🔐 Logged in via saved tokens.")
        return g

def get_latest_heart_rate(g):
    """Get most recent heart rate reading."""
    try:
        data = g.get_heart_rates()
        return data.get('lastHeartRateValue')
    except Exception:
        return None

def get_daily_steps(g):
    """Get today's step count."""
    try:
        data = g.get_steps()
        return data.get('totalSteps')
    except Exception:
        return None

def get_stress_score(g):
    """Get current stress score (0-100)."""
    try:
        data = g.get_stress_data()
        # Handle different possible response formats
        if isinstance(data, dict):
            return data.get('stressLevel') or data.get('value')
        elif isinstance(data, list) and len(data) > 0:
            # Sometimes returns array of stress data points
            latest = data[-1] if isinstance(data[-1], dict) else {}
            return latest.get('stressLevel') or latest.get('value')
    except Exception:
        return None

def main():
    """Main polling loop for Garmin Connect data export."""
    print("🔄 Starting Garmin Connect data polling...")
    print(f"   Email: {EMAIL}")
    print(f"   Token directory: {TOKEN_DIR}")
    print(f"   Polling interval: {POLL_INT}s")
    print("   Press Ctrl+C to stop\n")
    
    # Initial client setup
    garmin = ensure_client()
    
    # ----- DATA POLLING LOOP -----
    try:
        while True:
            try:
                # Fetch data
                hr = get_latest_heart_rate(garmin)
                steps = get_daily_steps(garmin)
                stress = get_stress_score(garmin)
                
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
                # Try to refresh tokens
                oauth1, oauth2 = load_tokens()
                if not (oauth1 and oauth2):
                    print("❌ No token files available. Interactive re-login required.")
                    break
                garmin = Garmin(EMAIL, None)
                garmin.client.di_token = oauth2.get('access_token')
                garmin.client.di_refresh_token = oauth2.get('refresh_token')
                garmin.client.di_token_expires_at = oauth2.get('expires_at', 0)
                garmin.client.csrf_token = oauth1.get('csrf_token')
                try:
                    garmin.login()
                    # Save refreshed tokens
                    oauth1 = {'csrf_token': garmin.client.csrf_token}
                    oauth2 = {
                        'access_token': garmin.client.di_token,
                        'refresh_token': garmin.client.di_refresh_token,
                        'expires_at': garmin.client.di_token_expires_at,
                        'token_type': 'Bearer',
                        'scope': ''
                    }
                    save_tokens(oauth1, oauth2)
                    garmin = garmin  # use the refreshed client
                    print("🔑 Token refresh successful")
                except Exception as e:
                    print(f"❌ Token refresh failed: {e}")
                    print("🔑 Interactive re-login required.")
                    break
            except Exception as e:
                print(f"❗ Unexpected error: {e}")
                # Continue polling on unexpected errors
            
            time.sleep(POLL_INT)
            
    except KeyboardInterrupt:
        print("\n👋 Polling stopped by user")
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")

if __name__ == "__main__":
    main()