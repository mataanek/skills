#!/usr/bin/env python3
"""
czech_check.py - Correct Czech text using LanguageTool.
Usage:
    echo "Some text" | czech_check.py
    czech_check.py "Some text"
    czech_check.py < input.txt > output.txt
Exits with 0.
"""
import sys
# Ensure user site-packages is in path
user_site = "/home/mataanek/.hermes/home/.local/lib/python3.10/site-packages"
if user_site not in sys.path:
    sys.path.insert(0, user_site)

import language_tool_python

def main():
    # Initialize LanguageTool for Czech
    tool = language_tool_python.LanguageTool('cs-CZ')
    # Read input: either from args or stdin
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = sys.stdin.read()
    # Correct
    corrected = tool.correct(text)
    # Output
    sys.stdout.write(corrected)

if __name__ == '__main__':
    main()