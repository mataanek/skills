#!/usr/bin/env python3
"""
Helper script for handling npm deprecated package warnings.
Provides guidance and checks for common deprecated packages.
"""

import os
import json
import subprocess
import sys

def check_package_json():
    """Check if package.json exists and is valid."""
    if not os.path.exists('package.json'):
        print("❌ No package.json found in current directory.")
        return None
    try:
        with open('package.json', 'r') as f:
            data = json.load(f)
        print("✅ package.json found.")
        return data
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in package.json: {e}")
        return None

def check_npm_warnings():
    """Run npm install and capture warnings about deprecated packages."""
    print("\n🔍 Checking for npm deprecated package warnings...")
    try:
        result = subprocess.run(
            ['npm', 'install'],
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout + result.stderr
        warnings = [line for line in output.split('\n') if 'npm warn deprecated' in line]
        if warnings:
            print(f"⚠️  Found {len(warnings)} deprecated package warning(s):")
            for w in warnings:
                print(f"   {w.strip()}")
        else:
            print("✅ No deprecated package warnings found.")
        return warnings
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js/npm.")
        return []
    except subprocess.TimeoutExpired:
        print("❌ npm install timed out.")
        return []

def main():
    print("=== npm Deprecated Package Helper ===")
    pkg_data = check_package_json()
    if pkg_data is None:
        sys.exit(1)
    warnings = check_npm_warnings()
    if warnings:
        print("\n📋 Recommended actions:")
        for w in warnings:
            if 'inflight@1.0.6' in w:
                print("   - Replace inflight with lru-cache or similar modern alternative.")
            if '@babel/plugin-proposal-private-methods' in w:
                print("   - Switch to @babel/plugin-transform-private-methods.")
            if 'glob@7.2.3' in w:
                print("   - Update glob to latest version (^8.x or ^9.x).")
    else:
        print("\n🎉 All good! No deprecated package warnings.")

if __name__ == '__main__':
    main()