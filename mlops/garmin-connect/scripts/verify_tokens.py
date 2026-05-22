#!/usr/bin/env python3
"""
Verify Garmin Connect token files for validity.
Checks:
  - oauth1_token.json contains non-empty csrf_token string
  - oauth2_token.json contains access_token, refresh_token, and future expires_at
Usage:
  python3 verify_tokens.py [token_dir]
Default token_dir: ~/.garminconnect
"""
import json
import os
import sys
import time

def main():
    token_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/.garminconnect")
    oauth1_path = os.path.join(token_dir, "oauth1_token.json")
    oauth2_path = os.path.join(token_dir, "oauth2_token.json")
    
    print(f"Checking token files in: {token_dir}")
    
    # Check oauth1
    try:
        with open(oauth1_path) as f:
            oauth1 = json.load(f)
    except FileNotFoundError:
        print(f"❌ Missing {oauth1_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {oauth1_path}: {e}")
        sys.exit(1)
    
    csrf = oauth1.get("csrf_token")
    if not csrf or not isinstance(csrf, str) or csrf.strip() == "":
        print(f"❌ oauth1_token.json missing or empty csrf_token. Got: {repr(csrf)}")
    else:
        print(f"✅ oauth1_token.json csrf_token present (length {len(csrf)})")
    
    # Check oauth2
    try:
        with open(oauth2_path) as f:
            oauth2 = json.load(f)
    except FileNotFoundError:
        print(f"❌ Missing {oauth2_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {oauth2_path}: {e}")
        sys.exit(1)
    
    access = oauth2.get("access_token")
    refresh = oauth2.get("refresh_token")
    expires = oauth2.get("expires_at")
    
    if not access or not isinstance(access, str) or access.strip() == "":
        print(f"❌ oauth2_token.json missing or empty access_token")
    else:
        print(f"✅ oauth2_token.json access_token present (length {len(access)})")
    
    if not refresh or not isinstance(refresh, str) or refresh.strip() == "":
        print(f"❌ oauth2_token.json missing or empty refresh_token")
    else:
        print(f"✅ oauth2_token.json refresh_token present (length {len(refresh)})")
    
    if not isinstance(expires, (int, float)):
        print(f"❌ oauth2_token.json expires_at missing or not a number. Got: {repr(expires)}")
    else:
        now = time.time()
        if expires > now:
            print(f"✅ oauth2_token.json expires_at is future: {expires} (in {int(expires - now)}s)")
        else:
            print(f"❌ oauth2_token.json expires_at is expired or not future: {expires} (now={now})")
    
    # Overall verdict
    if csrf and isinstance(csrf, str) and csrf.strip() != "" and \
       access and isinstance(access, str) and access.strip() != "" and \
       refresh and isinstance(refresh, str) and refresh.strip() != "" and \
       isinstance(expires, (int, float)) and expires > time.time():
        print("\n🎉 All checks passed. Tokens are valid.")
        sys.exit(0)
    else:
        print("\n❌ Token validation failed. Please regenerate tokens on a TTY host and verify before copying.")
        sys.exit(1)

if __name__ == "__main__":
    main()