#!/usr/bin/env python3
"""
czech_check_tool.py - Registers a tool for correcting Czech text.
"""
import sys
import re
import subprocess
import os

# Ensure we can import language_tool_python from user site
user_site = "/home/mataanek/.hermes/home/.local/lib/python3.10/site-packages"
if user_site not in sys.path:
    sys.path.insert(0, user_site)

JAVA = 'java'
JAR_PATH = '/home/mataanek/.local/share/languagetool/LanguageTool-6.6/languagetool.jar'

def simple_cs_correction(text: str) -> str:
    """Apply a set of common Czech error corrections."""
    corrections = [
        (r'\bskvela\b', 'skvělý'),
        (r'\bskvely\b', 'skvělý'),
        (r'\bskvele\b', 'skvěle'),
        (r'\brada\b(?=\s)', 'rád'),
        (r'\brada\b(?!\s)', 'rada'),
        (r'\bma rada\b', 'má rád'),
        (r'\bma rad\b', 'má rád'),
        (r'\bdejd\b', 'dej'),
        (r'\bdej mi\b', 'dej mi'),
        (r'\bprosim\b', 'prosím'),
        (r'\bProsim\b', 'Prosím'),
        (r'\bdekuji\b', 'děkuji'),
        (r'\bDekuji\b', 'Děkuji'),
        (r'\bmam\b', 'mám'),
        (r'\bMam\b', 'Mám'),
        (r'\bmas\b', 'máš'),
        (r'\bMas\b', 'Máš'),
        (r'\bma\b(?!\s)', 'má'),
        (r'\bkrasny\b', 'krásný'),
        (r'\bKrasny\b', 'Krásný'),
        (r'\bkrasna\b', 'krásná'),
        (r'\bKrasna\b', 'Krásná'),
        (r'\bkrasne\b', 'krásně'),
        (r'\bKrasne\b', 'Krásně'),
        (r'\bVcerra\b', 'Včera'),
        (r'\bvcerra\b', 'včera'),
    ]
    for pattern, repl in corrections:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return text

def languagetool_correction(text: str) -> str:
    """Use external languagetool jar if available."""
    if not os.path.isfile(JAR_PATH):
        return None
    if subprocess.run(['which', JAVA], capture_output=True).returncode != 0:
        return None
    try:
        proc = subprocess.run(
            [JAVA, '-jar', JAR_PATH, '--language', 'cs', '--replace'],
            input=text.encode('utf-8'),
            capture_output=True,
            timeout=15,
        )
        if proc.returncode == 0:
            return proc.stdout.decode('utf-8')
        else:
            return None
    except Exception:
        return None

def czech_check(text: str) -> str:
    """Public function to correct Czech text."""
    corrected = languagetool_correction(text)
    if corrected is not None:
        return corrected
    return simple_cs_correction(text)

# Register the tool
try:
    from hermes_tools import tools
    tools.register(
        name="czech_check",
        desc="Correct Czech text using LanguageTool (jar) with fallback to rule-based corrections.",
        inputs={"text": {"type": "string", "description": "Czech text to correct"}},
        output={"type": "string", "description": "Corrected Czech text"},
        function=czech_check,
    )
except Exception as e:
    # If we cannot register (e.g., not in a Hermes context), just allow the script to be run directly.
    # For testing, we can still provide a main.
    pass

if __name__ == "__main__":
    # Allow running as a script for testing
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
    else:
        input_text = sys.stdin.read()
    print(czech_check(input_text))