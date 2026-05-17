# Conditional Delivery for Freshrss News AI Digest

This document explains how to set up conditional delivery of the news digest: send to the Hermes web UI (origin) when you are recently active in the chat, and send to Telegram when you are not active.

## Why Conditional Delivery?

- When you are actively using the Hermes web UI, you see the digest directly in the chat (origin delivery).
- When you are away, you prefer to receive the digest via Telegram so you don't miss it.
- This avoids duplicate notifications and ensures you get the digest in the right place.

## Implementation

Two wrapper scripts are provided in the `scripts/` directory of this skill:

1. `digest_if_active.py` – Runs the digest and outputs only if there has been any CLI (web UI) session activity in the last 5 minutes. Output goes to the origin (for web UI delivery).
2. `digest_for_telegram.py` – Runs the digest and outputs only if there has been **no** recent CLI activity (or if activity cannot be determined). Output goes to Telegram.

Both scripts reuse the core digest logic (`digest.py`) and add a simple activity check.

## Activity Check Logic

The scripts determine recent activity by running:

```bash
hermes sessions list --source cli --limit 10
```

They parse the output to find the most recent session with source `cli` and check if its timestamp is within the last 5 minutes. If the command fails or no CLI session is found, activity is considered undetermined (treated as inactive for safety, favoring Telegram delivery).

## Setting Up Cron Jobs

Create two cron jobs using the Hermes CLI:

### 1. Web UI Digest (origin) – runs only when active

```bash
hermes cronjob create \
  --name "AI news digest origin 8:00/16:00" \
  --schedule "0 8,16 * * *" \
  --script "digest_if_active.py" \
  --deliver origin \
  --no-agent
```

### 2. Telegram Digest – runs when not active

```bash
hermes cronjob create \
  --name "AI news digest telegram 8:00/16:00" \
  --schedule "0 8,16 * * *" \
  --script "digest_for_telegram.py" \
  --deliver telegram \
  --no-agent
```

**Important**: The script must be referenced by filename only (as shown) and must be located in `~/.hermes/scripts/` when the cron job runs. The wrapper scripts themselves are stored in the skill's `scripts/` directory; you must copy or symlink them to `~/.hermes/scripts/` before the cron job runs, or adjust the skill's installation process to place them there.

### Copying Scripts for Cron

After installing the skill, copy the wrapper scripts to the Hermes scripts directory:

```bash
cp ~/.hermes/skills/news/freshrss-news-AI-digest/scripts/digest_if_active.py ~/.hermes/scripts/
cp ~/.hermes/skills/news/freshrss-news-AI-digest/scripts/digest_for_telegram.py ~/.hermes/scripts/
chmod +x ~/.hermes/scripts/digest_*.py
```

Alternatively, you can modify the skill's installation to symlink the scripts.

## Troubleshooting

- If you see "Script not found" errors, ensure the wrapper scripts are present in `~/.hermes/scripts/` and that the cron job references them by filename only.
- If the digest never appears in Telegram, verify that your Telegram delivery is configured correctly and that the activity check is working as expected. You can test the wrappers manually:
  - While active in the web UI: `python3 ~/.hermes/scripts/digest_if_active.py` should output the digest; `python3 ~/.hermes/scripts/digest_for_telegram.py` should output nothing.
  - After being away for >5 minutes: the opposite should occur.

## Notes

- The activity check relies on the `hermes sessions` CLI command being available and returning sensible data.
- The 5‑minute window is configurable; edit the wrapper scripts to change the `ACTIVE_WINDOW_MINUTES` constant.
- This approach keeps the core digest script unchanged and reusable for other delivery mechanisms.
