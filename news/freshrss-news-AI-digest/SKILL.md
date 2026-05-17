---
name: freshrss-news-AI-digest
description: Generate a news digest from FreshRSS in Nix's provocative, informal style with follow-up capabilities.
author: Hermes Agent
version: 0.3.0
---

# FreshRSS News AI Digest (Nix Style)

This skill fetches news items from FreshRSS using the existing digest logic, then curates and writes the digest in Nix's unique voice (provocative, informal, intimate, slang). It also supports follow-up queries where the user can ask to expand on a particular fact presented in the digest.

## Key Improvements (v0.3.0)

- **Content-aware tone matching**: The digest now analyzes each article's content (title + summary) to determine an emotional tone (shocking, sweet, tech-excited, tech-worried, money, controversial, neutral) and selects Nix-style language that matches the tone.
- **Context-appropriate openings**: Openings, middles, and closers are now selected based on content tone analysis rather than random selection, ensuring language fits the news and avoids robotic repetition (addressing user feedback about needing openings that "correspond with the article/information").
- **Condensed format**: Output limited to top 5 items only for readability and to avoid verbosity.
- **Conditional delivery**: Added wrapper scripts for smart delivery - to web UI (origin) when recently active, to Telegram when away.
- **Follow-up capability**: The script persists the last fetched items and can provide detailed follow-up when queried (e.g., "Tell me more about item 2").

## Environment Variables

The skill requires the following environment variables to be set:

- `FRESHRSS_GREADER_URL`: The base URL of your FreshRSS instance (e.g., `https://example.com/api/greader.php`)
- `FRESHRSS_USERNAME`: Your FreshRSS username
- `FRESHRSS_API_PASSWORD`: Your FreshRSS API password (or token)
- `FRESHRSS_LIMIT`: Maximum number of items to fetch (default: 50)

## Usage

Run the script to generate a digest:

```bash
python ~/.hermes/skills/news/freshrss-news-AI-digest/scripts/digest.py
```

For follow-up queries, you can ask about a specific fact from the last digest. The script persists the last fetched items and can provide more details when prompted.

Example follow-up:
> "Tell me more about the second item in the digest."

## Implementation

The script (`scripts/digest.py`) does the following:

1. Fetches items from FreshRSS using the provided environment variables (reusing the logic from `freshrss-news-digest`).
2. For each item, analyzes the content to determine a tone (shocking, sweet, tech-excited, tech-worried, money, controversial, neutral) based on keyword matching in title and summary.
3. Selects an opening, middle, and closer from tone-specific arrays to construct a Nix-style summary that matches the content's emotional impact.
4. Outputs the digest (top 5 items) and persists the raw items for follow-up.
5. When a follow-up query is detected (via command-line argument), it returns more details about the requested item.
6. Includes content variety awareness to avoid overly repetitive topics (though ultimate freshness depends on your FreshRSS feeds).
7. Handles Hermes CLI timeouts gracefully with fallback mechanisms (see `references/hermes_timeout_fallback.md`).
8. For cron deployment with platform delivery (especially Telegram), see `references/cron_deployment.md` for script location requirements.
9. **Session learning**: Based on user feedback, openings/middles/closers are now selected based on content tone analysis rather than random selection to ensure language fits the news and avoids robotic repetition. Digest length limited to top 5 items and delivery directed to origin for web UI visibility.

## Notes\n\n- The skill does not inherit from `SkillPlugin`; instead, it registers a tool via `tools.registry`.\n- The AI summarization step requires access to a language model (configured elsewhere in Hermes).\n- Follow-up data is persisted in a temporary file in the skill directory (`last_items.json`).\n- Content variety in the digest depends on your FreshRSS feeds - if your feeds contain similar topics, you may see repetition in the Nix-style responses. Consider diversifying your feed sources for best results.\n- See `references/hermes_timeout_fallback.md` for handling Hermes CLI timeouts and providing fallbacks in the digest script.\n- See `references/cron_deployment.md` for important deployment requirements when using this skill with Hermes cron jobs (especially for Telegram delivery).\n- See `references/conditional_delivery.md` for setting up conditional delivery (web UI when active, Telegram when away).\n\n**Important**: The script must be located in `~/.hermes/scripts/` and referenced by filename only in cron configuration (e.g., `script: digest.py`).

## Pitfalls & Troubleshooting

- **Cron deployment script location**: When setting up this skill to run via Hermes cron jobs (especially for delivery to platforms like Telegram), the script **must** be located in `~/.hermes/scripts/` and referenced by **filename only** in the cron configuration (e.g., `script: digest.py`). Using absolute or home-relative paths will result in "Script not found" errors. See `references/cron_deployment.md` for detailed deployment steps.
- **Hermes CLI timeouts**: The script includes fallback mechanisms for handling Hermes CLI timeouts during output delivery (see `references/hermes_timeout_fallback.md`). If you encounter timeout issues in your specific environment, consider adjusting the timeout values or enhancing the fallback logic.
- **Verbosity**: If the digest feels too long, ensure you are using the latest version (v0.3.0+) which limits output to top 5 items. Older versions may output all items.
- **Tone mismatch**: If you notice openings that don't match the news tone (e.g., tragic news with playful language), verify you are using v0.3.0+ where tone analysis selects appropriate language. Earlier versions used random selection.