---
name: freshrss-news-digest
description: Use when you want a themed news digest from FreshRSS. Fetch unread items, group and summarize them with the configured primary LLM, send a digest to chat, and save selected items to wiki/News Clippings on request.
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: news, freshrss, digest, rss, summarization, obsidian
    relatedskills: note-taking, research
required_environment_variables:
  - name: FRESHRSS_GREADER_URL
    prompt: "FreshRSS GReader API URL (e.g. http://localhost:8080/api/greader.php)"
    required_for: "FreshRSS API access"
  - name: FRESHRSS_USERNAME
    prompt: "FreshRSS username"
    required_for: "FreshRSS authentication"
  - name: FRESHRSS_API_PASSWORD
    prompt: "FreshRSS API password"
    required_for: "FreshRSS authentication"
---

# FreshRSS News Digest

## Overview

Fetch unread items from FreshRSS via the GReader API, group and summarize them with the configured primary LLM, send a themed digest to chat, and save user-selected items as markdown notes to `/home/mataanek/.hermes/wiki/News Clippings`. Scheduling and delivery cadence live in runtime configuration, not in this skill.

## When to Use

- User says "news", "what's new", "digest", "show me feeds", "fetch news"
- User asks for a FreshRSS-based summary of unread items
- User asks to expand or save stories after receiving a digest
- An external scheduler or automation triggers the digest workflow

## Workflow

### Step 1 — Authenticate with FreshRSS

Use `execute_code` to authenticate and obtain a session token:

```python
import os
import requests
import json

base = os.environ["FRESHRSS_GREADER_URL"].replace("/api/greader.php", "")
username = os.environ["FRESHRSS_USERNAME"]
password = os.environ["FRESHRSS_API_PASSWORD"]
limit = int(os.environ.get("FRESHRSS_LIMIT", 20))

r = requests.post(
    f"{base}/api/greader.php/accounts/ClientLogin",
    data={"Email": username, "Passwd": password},
    timeout=10,
)
r.raise_for_status()
token = dict(line.split("=", 1) for line in r.text.strip().splitlines()).get("Auth")
if not token:
    raise RuntimeError("FreshRSS authentication failed: missing Auth token")
headers = {"Authorization": f"GoogleLogin auth={token}"}
print(json.dumps({"ok": True, "token_present": True}))
```

### Step 2 — Fetch Per-Feed Items

Fetch items per feed so all sources are represented regardless of posting frequency.

```python
from urllib.parse import quote

r_feeds = requests.get(
    f"{base}/api/greader.php/reader/api/0/subscription/list",
    headers=headers,
    params={"output": "json"},
    timeout=10,
)
r_feeds.raise_for_status()
feeds = r_feeds.json().get("subscriptions", [])

items_per_feed = max(3, limit // max(len(feeds), 1))
items = []
for feed in feeds:
    feed_id = feed["id"]
    encoded_id = quote(feed_id, safe="")
    r_feed = requests.get(
        f"{base}/api/greader.php/reader/api/0/stream/contents/{encoded_id}",
        headers=headers,
        params={
            "output": "json",
            "n": items_per_feed,
            "xt": "user/-/state/com.google/read",
        },
        timeout=20,
    )
    if r_feed.status_code == 200:
        items.extend(r_feed.json().get("items", []))

if not items:
    print("NO_UNREAD_ITEMS")
else:
    print(f"Fetched {len(items)} items from {len(feeds)} feeds.")
```

If the output is `NO_UNREAD_ITEMS`, reply to the user that there are no unread items and stop.

### Step 3 — Build Article Candidates

```python
from datetime import datetime
from html import unescape
import re
import json

def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").strip()

candidates = []
for i, item in enumerate(items, start=1):
    canonical = item.get("canonical") or []
    url = canonical.get("href", "") if canonical and isinstance(canonical, dict) else ""
    source = item.get("origin", {}).get("title", "unknown source")
    title = unescape(item.get("title", "")).strip()
    published_ts = item.get("published", 0)
    published = datetime.fromtimestamp(published_ts).strftime("%Y-%m-%d") if published_ts else ""
    raw_summary = item.get("summary", {}).get("content", "")
    summary_text = strip_html(unescape(raw_summary))
    candidates.append({
        "index": i,
        "title": title,
        "source": source,
        "url": url,
        "published": published,
        "summary": summary_text[:1000],
    })

# Persist candidates to /tmp for follow-up resolution
with open("/tmp/hermes_digest_candidates.json", "w", encoding="utf-8") as f:
    json.dump(candidates, f, ensure_ascii=False, indent=2)

print(f"Built {len(candidates)} candidates. Saved to /tmp/hermes_digest_candidates.json")
for c in candidates:
    print(f"[{c['index']}] {c['title']} | {c['source']} | {c['published']}")
```

### Step 4 — Generate Themed Digest

After Step 3 completes, the agent synthesizes the digest directly. Do **not** call any LLM API here — the agent is the LLM.

Using the candidates printed above, write a themed morning news brief following these rules:

- Organize by themes, not individual articles
- One short section per important theme
- Synthesize related articles together
- Keep each section concise and information-dense (60–120 words)
- Do not write a ranked list
- Do not explain your reasoning
- If useful, add a final line: `Worth expanding: <topic 1> / <topic 2> / <topic 3>`

Format:
[optional title]
[optional one-line intro]

[Theme Name]
[paragraph]

[Theme Name]
[paragraph]

Worth expanding: ...


### Step 5 — Send Digest to Chat

Send the digest directly to chat. Append this footer:
Ask for more on any theme or story, for example:

expand on the metal music news
tell me more about the security section
save the story about phishing

### Step 6 — Resolve Follow-Up Requests

When the user asks to expand, explain, or save something from the digest:

- Reload candidates from `/tmp/hermes_digest_candidates.json` if needed
- Match against theme names, company names, product names, source names, story phrases
- Prefer exact and obvious matches
- If ambiguous, ask one short clarifying question
- Keep internal candidate indices in memory; do not require the user to refer to them

Examples:
- `expand on the Meta news`
- `tell me more about the ransomware story`
- `save the AI section`
- `save the item about Anthropic`

### Step 7 — Expand Stories or Sections

When the user asks for more on a story or theme:

- Identify the matching candidate or related group
- Reply with title, source, published date, URL, and short item-specific summary
- Do not save anything during expand

### Step 8 — Save Selected Items to Wiki

```python
import re
import json
from pathlib import Path

wiki_dir = Path("/home/mataanek/.hermes/wiki/News Clippings")
wiki_dir.mkdir(parents=True, exist_ok=True)

# Load persisted candidates
with open("/tmp/hermes_digest_candidates.json", encoding="utf-8") as f:
    candidates = json.load(f)

# matched_candidates must be resolved by the agent before running this block
# Replace the list below with the actual resolved matches
matched_candidates = resolve_candidates_from_user_request(user_reply, candidates)

saved = 0
for c in matched_candidates:
    safe_title = re.sub(r"[^\w\s-]", "-", c["title"])[:80].strip().replace(" ", "-")
    published = c.get("published") or "undated"
    filename = wiki_dir / f"{published}-{safe_title}.md"
    content = (
        f"# {c['title']}\n\n"
        f"**Source:** {c['source']}\n"
        f"**Published:** {published}\n"
        f"**URL:** {c['url']}\n\n"
        f"## Summary\n\n"
        f"{c['summary']}\n"
    )
    filename.write_text(content, encoding="utf-8")
    saved += 1
    print(f"Saved: {filename}")

print(f"Saved {saved} item(s) to News Clippings.")
```

Reply: `Saved N item(s) to News Clippings.`

---

## Digest Composition

### Core Rules

- Organize by themes, not individual articles
- One section per theme or dominant topic cluster
- Synthesize multiple articles per section where possible
- No numbered article lists unless explicitly requested
- Direct and editorial tone

### Section Behavior

- Open with the most important development in the theme
- Merge overlapping stories into one coherent update
- End naturally without padding

### Length Guidance

60–120 words per section. Overall digest readable in 2–3 minutes.

### Theme Selection

Use user-specified themes if provided. Otherwise infer from content clusters. Recurring themes may include AI, metal music, and IT security.
**Important**: Ensure themes are coherent and logically grouped. Avoid forcing unrelated topics together (e.g., do not mix music news with AI developments unless there is a clear, substantive connection). If clusters feel awkward or disjointed, reconsider the thematic grouping or consider having more, narrower sections.

### Anti-Patterns

Avoid:
- Per-article bullet lists
- Repeating relevance phrasing across sections
- Equal section sizes regardless of content
- Recommender-system tone
- Creating sections with fewer than 30 words (too insubstantial)
- Having only 1-2 sections when there is sufficient diverse content for 3+ meaningful themes

---

## Common Pitfalls

1. `FRESHRSS_GREADER_URL` must include `/api/greader.php` — base URL is derived from it by stripping that suffix.
2. `xt` param filters read items — remove only if you want all items including already-read ones.
3. Do not hardcode any LLM provider or call any LLM API from within skill code — the agent IS the LLM.
4. Always use `Path(\"/home/mataanek/.hermes/wiki/News Clippings\")` — never `Path.home()`.
5. Retry once with a shorter prompt if output is weak or empty.
6. `canonical` is a list — handle defensively (check length and type before indexing).
7. Save notes contain item-specific summaries, not the full digest.
8. Save resolution uses natural language matching, not numeric indices.
9. Env vars may live in `~/.hermes/.env` — Hermes loads them automatically when the skill is active.
10. If requested themes are absent in the fetched items, say so clearly — do not fabricate content.
11. Persist candidates to `/tmp/hermes_digest_candidates.json` in Step 3 so Step 6–8 can reload them without re-fetching.
12. The per-feed fetch limit (items_per_feed) may cause some feeds to be underrepresented if they have many unread items. 
    If you are looking for a specific topic and it doesn't appear in the digest, consider increasing the overall limit or checking the relevant category directly.
13. In some environments, the `hermes_tools` module may not be available. If attempting to call the Hermes CLI from Python code, use `subprocess.run()` instead of trying to import `hermes_tools`. Adjust timeouts based on prompt complexity - longer prompts may need longer timeouts. Example:
    ```python
    import subprocess
    result = subprocess.run(
        [\"hermes\", \"-z\", escaped_prompt],
        capture_output=True,
        text=True,
        timeout=120,  # Increase for complex prompts
        cwd=\"/home/mataanek/.hermes/hermes-agent\"
    )
    ```
14. **Content Freshness**: Always check item publication dates. Avoid including very old items (older than 2-3 days) unless specifically requested. If you see repetitive content from previous digests, consider adjusting the FRESHRSS_LIMIT or checking if the xt parameter is working correctly to filter already-read items.
15. **Workflow Discipline**: Follow the exact workflow steps. After completing Step 3 (building candidates), output the candidates and stop. Do NOT attempt to synthesize the digest in the same execution block. The agent (you) will synthesize the digest in a subsequent turn after seeing the candidates output. Attempting to do both in one step violates the skill's design and often leads to poor results.