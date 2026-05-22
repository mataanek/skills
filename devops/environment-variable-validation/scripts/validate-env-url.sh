#!/usr/bin/env bash
# Validate-Env-URL.sh
# A script to validate that an environment variable URL is reachable and returns expected content.
#
# Usage: ./validate-env-url.sh <URL> [--auth-user <user> --auth-pass <pass>] [--expected-string <string>]
#        ./validate-env-url.sh --help
#
# Example: ./validate-env-url.sh "http://localhost:8081/api/greader.php" --auth-user mataanek --auth-pass Misanthrope-01 --expected-string "SID="

set -euo pipefail

# Default values
AUTH_USER=""
AUTH_PASS=""
EXPECTED_STRING=""
TIMEOUT=10

# Function to display help
display_help() {
  echo "Usage: $0 <URL> [options]"
  echo ""
  echo "Options:"
  echo "  --auth-user <user>       Username for basic auth (if needed)"
  echo "  --auth-pass <pass>       Password for basic auth (if needed)"
  echo "  --expected-string <str>  String that must be present in the response"
  echo "  --timeout <seconds>      HTTP timeout in seconds (default: 10)"
  echo "  --help                   Display this help and exit"
  echo ""
  echo "Example:"
  echo "  $0 \"http://localhost:8081/api/greader.php\" \\"
  echo "       --auth-user mataanek --auth-pass Misanthrope-01 \\"
  echo "       --expected-string \"SID=\""
  exit 0
}

# Parse arguments
if [[ $# -eq 0 ]]; then
  display_help
fi

URL="$1"
shift

while [[ $# -gt 0 ]]; do
  case $1 in
    --auth-user)
      AUTH_USER="$2"
      shift 2
      ;;
    --auth-pass)
      AUTH_PASS="$2"
      shift 2
      ;;
    --expected-string)
      EXPECTED_STRING="$2"
      shift 2
      ;;
    --timeout)
      TIMEOUT="$2"
      shift 2
      ;;
    --help)
      display_help
      ;;
    *)
      echo "Unknown option: $1"
      display_help
      ;;
  esac
done

# Validate URL is not empty
if [[ -z "$URL" ]]; then
  echo "Error: URL is required" >&2
  exit 1
fi

# Prepare curl command
CURL_CMD=(curl -sS --max-time "$TIMEOUT")

# Add basic auth if provided
if [[ -n "$AUTH_USER" && -n "$AUTH_PASS" ]]; then
  CURL_CMD+=(--user "$AUTH_USER:$AUTH_PASS")
fi

# Add URL
CURL_CMD+=("$URL")

# Execute curl and capture output
echo "Testing URL: $URL" >&2
RESPONSE=$("${CURL_CMD[@]}") || {
  echo "Error: Failed to connect to $URL" >&2
  exit 1
}

# Check if we got a response
if [[ -z "$RESPONSE" ]]; then
  echo "Error: Empty response from $URL" >&2
  exit 1
fi

# If expected string is provided, check for it
if [[ -n "$EXPECTED_STRING" ]]; then
  if [[ ! "$RESPONSE" =~ $EXPECTED_STRING ]]; then
    echo "Error: Expected string '$EXPECTED_STRING' not found in response" >&2
    echo "Response: $RESPONSE" >&2
    exit 1
  fi
fi

echo "Success: URL is reachable and response is valid."
exit 0