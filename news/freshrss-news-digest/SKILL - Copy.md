---
name: freshrss-news-digest
description: Use when you want a themed news digest from FreshRSS. Fetch unread items, group and summarize them with the configured primary LLM, send a digest to chat, and save selected items to wiki/News Clippings on request.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: news, freshrss, digest, rss, summarization, obsidian
    relatedskills: note-taking, research
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

```python
import os
import requests

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
```

### Step 2 - Fetch unread items per category

Fetch unread items from FreshRSS categories rather than individual feeds. This keeps the candidate pool balanced across your configured topic groups instead of over-weighting categories that simply have more subscriptions.

```python
import requests

items = []
seen_ids = set()
items_per_category = 12

r_tags = requests.get(
    f"{base}/api/greader.php/reader/api/0/tag/list",
    headers=headers,
    params={"output": "json"},
    timeout=10,
)
r_tags.raise_for_status()

tags = r_tags.json().get("tags", [])

category_tags = [
    tag["id"]
    for tag in tags
    if "/label/" in tag.get("id", "")
]

for category_tag in category_tags:
    r_cat = requests.get(
        f"{base}/api/greader.php/reader/api/0/stream/contents/{requests.utils.quote(category_tag, safe='')}",
        headers=headers,
        params={
            "output": "json",
            "n": items_per_category,
            "xt": "user/-/state/com.google/read",
        },
        timeout=20,
    )
    if r_cat.status_code != 200:
        continue

    cat_items = r_cat.json().get("items", [])
    for item in cat_items:
        item_id = item.get("id")
        if item_id and item_id in seen_ids:
            continue
        if item_id:
            seen_ids.add(item_id)
        item["_category_tag"] = category_tag
        items.append(item)

if not items:
    # reply no unread items and stop
    pass
```

### Step 3 — Build Article Candidates

Prepare article candidates for digest generation and follow-up actions. Keep internal IDs for matching and persistence, but do not expose them in the visible digest unless debugging is enabled.

```python
from datetime import datetime
from html import unescape
import re

def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").strip()

candidates = []
for i, item in enumerate(items, start=1):
    canonical = item.get("canonical") or []
    url = canonical[0].get("href", "") if canonical and isinstance(canonical[0], dict) else ""
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
```

### Step 4 — Generate Themed Digest

Use Hermes configured primary model to turn the article candidates into a themed digest. Keep the prompt simple. The model should produce the final digest text directly, not JSON.

```python
article_block = "\n\n".join(
    f"{c['title']}\nSource: {c['source']}\nPublished: {c['published']}\nURL: {c['url']}\nSummary: {c['summary']}"
    for c in candidates
)

prompt = (
    "You are preparing a concise morning news brief for a senior software engineer.\n"
    "Use the articles below as source material.\n\n"
    "Instructions:\n"
    "- Organize the digest by themes, not by individual articles.\n"
    "- Write one short section per important theme.\n"
    "- Synthesize related articles together.\n"
    "- Keep each section concise and information-dense.\n"
    "- Do not write a ranked list.\n"
    "- Do not explain your reasoning.\n"
    "- If useful, add a final line such as: Worth expanding: Meta AI updates / phishing campaign / new album release\n\n"
    "Return the digest as plain text:\n"
    "[optional title]\n"
    "[optional intro]\n"
    "[theme]\n"
    "[paragraph]\n\n"
    f"Articles:\n{article_block}"
)

from hermes_tools import terminal

escaped_prompt = prompt.replace("'", "'\\''")
result = terminal(f"hermes -z '{escaped_prompt}'")
digest = result if isinstance(result, str) else str(result)
```

If the output is weak, retry once with a shorter prompt and fewer candidate articles rather than adding more output-format complexity.

### Step 5 — Send Digest to Chat

Send digest directly to chat. Append a short natural-language action footer such as:

```
Ask for more on any theme or story, for example:
- expand on the metal music news
- tell me more about the security section
- save the story about phishing
```

Do not expose internal candidate indices in the visible digest unless debugging is enabled.

### Step 6 — Resolve Follow-Up Requests

When the user asks to expand, explain, or save something from the digest:
- resolve the request from the latest digest context and the current candidate set
- match against theme names, company names, product names, source names, and distinctive story phrases
- prefer exact and obvious matches
- if several matches are plausible, ask one short clarifying question
- keep internal candidate indices in memory for routing, but do not require the user to refer to them

Examples of supported follow-up language:
- expand on the Meta news
- tell me more about the ransomware story
- save the AI section
- save the item about Anthropic

### Step 7 — Expand Stories or Sections

When the user asks for more on a story or theme:
- identify the matching candidate or related group of candidates
- reply with a compact source rundown including title, source, published date, URL, and a short item-specific summary
- if the request points to a theme rather than a single story, summarize the most relevant supporting items under that theme
- do not save anything during expand

### Step 8 - Save Selected Items to Wiki

When the user asks to save a story or section in natural language:
- resolve the request to one or more matching candidates,
- save the resolved items as markdown notes,
- if the request is ambiguous, ask a clarifying question before saving.

```python
import re
from pathlib import Path

wiki_dir = Path("/home/mataanek/.hermes/wiki/News Clippings")
wiki_dir.mkdir(parents=True, exist_ok=True)

matched_candidates = resolve_candidates_from_user_request(user_reply, candidates, digest)

saved = 0

for c in matched_candidates:
    safe_title = re.sub(r"[^\w\s-]", "-", c["title"])[:80].strip().replace(" ", "-")
    published = c.get("published") or "undated"
    filename = wiki_dir / f"{published}-{safe_title}.md"

    content = f"""# {c["title"]}

**Source:** {c["source"]}
**Published:** {published}
**URL:** {c["url"]}

## Summary

{c["summary"]}
"""
    filename.write_text(content, encoding="utf-8")
    saved += 1

reply = f"Saved {saved} item(s) to News Clippings."
```

Save item-specific notes only. Do not write the full multi-theme digest into every saved note.

## Digest Composition

When generating a digest, treat individual articles as source material rather than the final output. The goal is a compact themed brief that reads like a short article, not a ranked list of links.

### Core Rules

- Organize the digest by themes, not by individual articles.
- Create one section per requested theme, inferred theme, or clearly dominant topic cluster.
- Do not force a fixed number of sections unless the user explicitly asks for one.
- Keep each section concise and information-dense.
- Synthesize multiple relevant articles inside a section whenever possible instead of summarizing one article at a time.
- Avoid numbered article lists unless the user explicitly requests a list, ranking, or source rundown.
- Keep the writing direct and editorial - do not explain the system, selection process, or reasoning unless asked.

### Section Behavior

Each section should:
- open with the most important development, tension, or pattern inside that theme
- merge overlapping stories into one coherent update where possible
- mention notable divergence only when it changes the takeaway
- end naturally once the key point is delivered instead of padding for symmetry

A section may be short if the theme is quiet that day. A section may be longer if several connected developments clearly belong together.

### Length Guidance

Keep each theme section concise and information-dense, usually around 60-120 words. Allow shorter sections for lighter themes and longer sections only when several related developments need to be synthesized together. Do not force equal section length. Keep the overall digest readable in roughly 2-3 minutes unless the user explicitly asks for broader coverage. If the number of themes increases, compress section length before expanding total length too aggressively.

### Theme Selection

If the user specifies themes, use those themes directly. If not, infer themes from the strongest clusters in the selected article set. For the current default setup, recurring themes may include AI, metal music news, and IT security threats, but these should remain configurable rather than hardcoded into every digest.

### Source Handling

Source articles should support the section, not dominate it. Do not output one bullet per source article inside the main digest unless requested. Preserve the ability to expand a section into:
- source article list
- longer explanation
- why this theme was included
- more or less coverage next time

### Output Preference

Preferred default shape:
- optional opening line or title
- one section per theme
- optional short closing line or expandable threads

Do not add a concluding summary unless the user asks for one. The digest should feel complete without a forced wrap-up.

### Anti-Patterns

Avoid:
- per-article bullet lists with one-line commentary
- repeating the same relevance phrasing across sections
- mechanically giving every section the same size regardless of content
- sounding like a recommender system instead of a morning brief

### Example Shape

Good:
- AI section synthesizes model, tooling, and infra stories into one update.
- Security section groups threats, exploits, or defensive trends into one clear takeaway.
- Music section highlights scene movement, releases, or notable discussion threads without listing every item.

Bad:
- Article 1: why relevant
- Article 2: why relevant
- Article 3: why relevant

## Common Pitfalls

1. FRESHRSS_GREADER_URL must include /api/greader.php - base URL is derived from it.
2. xt param filters read items - remove only if you want all items.
3. Do not hardcode one LLM provider.
4. Always use Path("/home/mataanek/.hermes/wiki/News Clippings") - never Path.home().
5. Retry once with shorter prompt if output is weak.
6. canonical is a list - handle defensively.
7. Save notes contain item-specific summaries, not the full digest.
8. Save resolution uses natural language, not numeric indices.
9. Env vars may live in ~/.hermes/.env.
10. If requested themes are absent, say so clearly - do not fabricate.

## Verification Checklist

- [ ] FRESHRSS_GREADER_URL, FRESHRSS_USERNAME, FRESHRSS_API_PASSWORD present
- [ ] All feeds return unread items via per-feed API calls
- [ ] All categories (AI, security, music, news) represented in candidates
- [ ] LLM responds to chat completions
- [ ] Digest appears as themed brief, not ranked list
- [ ] Natural language follow-up resolves correctly
- [ ] Save creates files in /home/mataanek/.hermes/wiki/News Clippings
- [ ] Saved files contain correct source, date, URL, summary
- [ ] Runtime scheduling is defined outside the skill in project config or documentation