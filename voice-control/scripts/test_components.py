#!/usr/bin/env python3
"""
Test script to verify voice control components
"""
import os
import sys

def test_imports():
    print("Testing imports...")
    try:
        import pyaudio
        print("✓ PyAudio")
    except ImportError as e:
        print(f"✗ PyAudio: {e}")
    
    try:
        import openwakeword
        print("✓ openWakeWord")
    except ImportError as e:
        print(f"✗ openWakeWord: {e}")
    
    try:
        import whisper
        print("✓ Whisper")
    except ImportError as e:
        print(f"✗ Whisper: {e}")
    
    try:
        import numpy
        print("✓ NumPy")
    except ImportError as e:
        print(f"✗ NumPy: {e}")
    
    # Test Hermes tools
    try:
        sys.path.insert(0, '/home/mataanek/.hermes/hermes-agent/tools')
        from registry import registry
        print("✓ Hermes registry")
    except Exception as e:
        print(f"✗ Hermes registry: {e}")

if __name__ == "__main__":
    test_imports()