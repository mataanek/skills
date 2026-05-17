# Cron Deployment for Freshrss News AI Digest

When setting up the freshrss-news-AI-digest skill to run via Hermes cron jobs (especially for delivery to platforms like Telegram), note the following deployment requirement:

## Script Location Requirement
Hermes cron jobs with `no_agent: true` and `deliver: telegram` (or other platforms) require the script to be located in `~/.hermes/scripts/` and referenced by filename only in the cron configuration.

## Deployment Steps
1. The main script resides in the skill directory:  
   `~/.hermes/skills/news/freshrss-news-AI-digest/scripts/digest.py`

2. For cron deployment, copy (or symlink) this script to:  
   `~/.hermes/scripts/digest.py`  
   Ensure it is executable: `chmod +x ~/.hermes/scripts/digest.py`

3. In the cron job configuration, reference the script by filename only:  
   `script: digest.py`  
   (Do not use absolute or home-relative paths)

## Why This Is Required
The Hermes cron system for platform-delivered jobs (when `no_agent: true`) executes scripts from a restricted environment that only allows scripts in `~/.hermes/scripts/`. Attempting to use absolute paths (like `/home/user/.hermes/skills/.../script.py`) will result in "Script not found" errors.

## Example Cron Configuration
```yaml
- name: "AI news digest 8:00/16:00"
  script: "digest.py"  # Filename only - must be in ~/.hermes/scripts/
  schedule: "0 8,16 * * *"
  deliver: "telegram"
  no_agent: true
```

## Troubleshooting
If you see errors like:  
`Script not found: /home/mataanek/.hermes/scripts/python3 /home/mataanek/.hermes/skills/...`  
This indicates you included the full path or incorrectly prefixed the command. The cron system expects only the script filename (e.g., `digest.py`) and will automatically prepend the interpreter and path from `~/.hermes/scripts/`.

See also: `references/hermes_timeout_fallback.md` for handling potential Hermes CLI timeouts in the script.