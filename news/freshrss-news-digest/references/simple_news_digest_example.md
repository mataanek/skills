# Simple News Digest Example (Cron-Friendly)

This is a fallback implementation for when the full LLM-based digest generation times out in cron environments.

## Key Features:
- Works reliably in cron with short timeouts
- Groups news by FreshRSS categories/labels
- Uses simple bullet format with emojis for visual appeal
- Maintains the sexy, informal tone user prefers
- Includes clear call-to-action for expansion

## Implementation Notes:
1. After fetching and building candidates (Steps 1-3 of main workflow)
2. Group candidates by `_category_tag` field
3. For each category, show up to 3 articles with title, source, and date
4. Add "and X more" if there are additional articles
5. Format with markdown for readability in Telegram
6. Always end with invitation to expand on topics

## Example Output Structure:
```
Good morning, baby. Here's your news digest:

**AI&Tech**
• Article title
  Source: Source Name
  Published: YYYY-MM-DD

• Article title
  Source: Source Name
  Published: YYYY-MM-DD

  ...and 5 more

**Music**
• Article title
  Source: Metal Injection
  Published: YYYY-MM-DD

  ...and 2 more

Want me to expand on any topic? Just ask, baby.
```

## When to Use:
- Primary hermes CLI call times out (>60s in cron)
- Environment lacks proper LLM access for complex prompts
- Need guaranteed delivery even if less synthesized

## Reference:
See `scripts/simple_news_digest.py` for working implementation.