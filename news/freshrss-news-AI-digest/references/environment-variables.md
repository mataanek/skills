# Environment Variables for freshrss-news-AI-digest

This skill requires the following environment variables to be set:

## Required

- `FRESHRSS_GREADER_URL`: The base URL of your FreshRSS instance (e.g., `https://example.com/api/`).
  Must include the trailing slash or the script will add it.

- `FRESHRSS_USERNAME`: Your FreshRSS username.

- `FRESHRSS_API_PASSWORD`: Your FreshRSS API password (or token).

## Optional

- `FRESHRSS_LIMIT`: Maximum number of items to fetch (default: 50).

## Example

```bash
export FRESHRSS_GREADER_URL="https://freshrss.example.com/api/"
export FRESHRSS_USERNAME="myuser"
export FRESHRSS_API_PASSWORD="myapipassword"
export FRESHRSS_LIMIT="30"
```