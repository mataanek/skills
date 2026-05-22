#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timezone

def verify_garmin_tokens():
    """Verify Garmin Connect tokens are valid for automatic refresh."""
    token_dir = "/home/mataanek/.hermes/.garminconnect"
    oauth1_path = os.path.join(token_dir, "oauth1_token.json")
    oauth2_path = os.path.join(token_dir, "oauth2_token.json")
    
    # Check if files exist
    if not os.path.exists(oauth1_path):
        print("❌ ERROR: oauth1_token.json not found")
        return False
        
    if not os.path.exists(oauth2_path):
        print("❌ ERROR: oauth2_token.json not found")
        return False
    
    # Load and verify oauth1_token.json
    try:
        with open(oauth1_path, 'r') as f:
            oauth1_data = json.load(f)
        
        csrf_token = oauth1_data.get('csrf_token', '')
        if not csrf_token or not isinstance(csrf_token, str) or csrf_token.strip() == '':
            print("❌ ERROR: csrf_token is empty or missing in oauth1_token.json")
            print(f"   Current value: {repr(csrf_token)}")
            return False
        else:
            print("✅ oauth1_token.json: csrf_token is present and non-empty")
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON in oauth1_token.json: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: Failed to read oauth1_token.json: {e}")
        return False
    
    # Load and verify oauth2_token.json
    try:
        with open(oauth2_path, 'r') as f:
            oauth2_data = json.load(f)
        
        expires_at = oauth2_data.get('expires_at', 0)
        if not isinstance(expires_at, (int, float)) or expires_at <= 0:
            print("❌ ERROR: expires_at is missing, zero, or invalid in oauth2_token.json")
            print(f"   Current value: {expires_at}")
            return False
        
        # Check if expiration is in the future
        now = datetime.now(timezone.utc).timestamp()
        if expires_at <= now:
            print("❌ ERROR: expires_at is in the past (token expired)")
            print(f"   Expires at: {datetime.fromtimestamp(expires_at, tz=timezone.utc)}")
            print(f"   Current time: {datetime.fromtimestamp(now, tz=timezone.utc)}")
            return False
        else:
            print("✅ oauth2_token.json: expires_at is in the future")
            print(f"   Expires at: {datetime.fromtimestamp(expires_at, tz=timezone.utc)}")
            print(f"   Time until expiry: {int((expires_at - now) / 3600)} hours")
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON in oauth2_token.json: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: Failed to read oauth2_token.json: {e}")
        return False
    
    print("\n✅ All token checks passed! Tokens are valid for automatic refresh.")
    return True

if __name__ == "__main__":
    if verify_garmin_tokens():
        sys.exit(0)
    else:
        sys.exit(1)