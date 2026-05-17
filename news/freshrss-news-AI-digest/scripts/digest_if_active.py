#!/usr/bin/env python3
"""
Conditional digest runner for Hermes web UI (origin) delivery.
Runs the digest only if there has been CLI session activity in the last 5 minutes.
Output goes to origin (for web UI delivery).
"""
import os
import subprocess
from datetime import datetime, timedelta

# Configuration
ACTIVE_WINDOW_MINUTES = 5
DIGEST_SCRIPT = "digest.py"  # Assumes this is in the same directory or in PATH

def check_recent_cli_activity():
    """Check if there has been any CLI (web UI) session activity in the last N minutes."""
    try:
        # Get recent CLI sessions
        result = subprocess.run(
            ["hermes", "sessions", "list", "--source", "cli", "--limit", "10"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            # If we can't check activity, assume inactive (safe default for Telegram)
            return False
            
        output = result.stdout.strip()
        if not output:
            return False
            
        # Parse output to find the most recent CLI session timestamp
        lines = output.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('[') and 'cli' in line:
                # Try to extract timestamp - format may vary
                # This is a simplified parser; adjust based on actual hermes sessions output
                parts = line.split()
                if len(parts) >= 3:
                    # Look for a timestamp-like pattern
                    for part in parts:
                        if ':' in part and len(part) >= 5:  # HH:MM or HH:MM:SS
                            try:
                                # Try to parse as time
                                time_str = part.split('.')[0]  # Remove microseconds if present
                                if len(time_str) == 8:  # HH:MM:SS
                                    session_time = datetime.strptime(time_str, '%H:%M:%S')
                                elif len(time_str) == 5:  # HH:MM
                                    session_time = datetime.strptime(time_str, '%H:%M')
                                else:
                                    continue
                                
                                # Combine with today's date
                                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                                session_datetime = today.replace(
                                    hour=session_time.hour,
                                    minute=session_time.minute,
                                    second=session_time.second
                                )
                                
                                # Handle case where time might be from yesterday (if current time is early morning)
                                if session_datetime > datetime.now():
                                    session_datetime -= timedelta(days=1)
                                
                                # Check if within active window
                                if datetime.now() - session_datetime <= timedelta(minutes=ACTIVE_WINDOW_MINUTES):
                                    return True
                            except ValueError:
                                continue
        return False
    except Exception:
        # On any error, assume inactive (safe default)
        return False

def main():
    """Main entry point."""
    if check_recent_cli_activity():
        # Run the digest script and output normally (for origin delivery)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        digest_path = os.path.join(script_dir, DIGEST_SCRIPT)
        if not os.path.exists(digest_path):
            # Fallback: try to find it in the skills directory
            digest_path = os.path.join(
                os.path.dirname(script_dir), 
                "scripts", 
                DIGEST_SCRIPT
            )
        
        if os.path.exists(digest_path):
            # Run the digest script
            result = subprocess.run(
                ["python3", digest_path],
                capture_output=False,  # Let output go directly to stdout/stderr
                text=True
            )
            return result.returncode
        else:
            print(f"Error: Could not find digest script at {digest_path}", flush=True)
            return 1
    else:
        # No recent activity - output nothing (so Telegram job won't deliver)
        return 0

if __name__ == "__main__":
    exit(main())