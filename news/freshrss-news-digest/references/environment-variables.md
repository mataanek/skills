# Environment Variables for FreshRSS News Digest

The freshrss-news-digest skill requires the following environment variables:

- `FRESHRSS_GREADER_URL`: Base URL for the FreshRSS GReader API (must include `/api/greader.php`)
- `FRESHRSS_USERNAME`: Username for FreshRSS authentication
- `FRESHRSS_API_PASSWORD`: API password (not the regular login password)
- `FRESHRSS_LIMIT`: (Optional) Number of items to fetch, defaults to 10

These variables can be set in:
1. The current shell environment
2. `~/.hermes/.env` (recommended for persistence)
3. A `.env` file in the current working directory

If variables appear missing, check `~/.hermes/.env` first, as this is where Hermes Agent typically stores persistent configuration.

Example `~/.hermes/.env` entry:
```
FRESHRSS_GREADER_URL="http://localhost:8081/api/greader.php"
FRESHRSS_USERNAME="mataanek"
FRESHRSS_API_PASSWORD="your-api-password-here"
FRESHRSS_LIMIT="10"
```