#!/usr/bin/env python3
"""
News digest script that synthesizes FreshRSS items into themed paragraphs.
Extended version with more items per theme.
"""

import os
import requests
import json
from urllib.parse import quote
from datetime import datetime
from html import unescape
import re
from pathlib import Path
from collections import defaultdict

def load_env():
    """Load environment variables from /home/mataanek/.hermes/.env"""
    env_path = Path("/home/mataanek/.hermes/.env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    if '=' in line:
                        k, v = line.strip().split('=', 1)
                        os.environ[k] = v.strip('"\'')
    else:
        raise FileNotFoundError(f"Env file not found at {env_path}")

def authenticate_freshrss():
    """Authenticate with FreshRSS and return headers"""
    load_env()
    
    base = os.environ["FRESHRSS_GREADER_URL"].replace("/api/greader.php", "")
    username = os.environ["FRESHRSS_USERNAME"]
    password = os.environ["FRESHRSS_API_PASSWORD"]

    r = requests.post(
        f"{base}/api/greader.php/accounts/ClientLogin",
        data={"Email": username, "Passwd": password},
        timeout=10,
    )
    r.raise_for_status()
    token = dict(line.split("=", 1) for line in r.text.strip().splitlines()).get("Auth")
    if not token:
        raise RuntimeError("FreshRSS authentication failed: missing Auth token")
    return {"Authorization": f"GoogleLogin auth={token}"}, base

def fetch_items(headers, base, limit=50):
    """Fetch unread items from FreshRSS feeds"""
    r_feeds = requests.get(
        f"{base}/api/greader.php/reader/api/0/subscription/list",
        headers=headers,
        params={"output": "json"},
        timeout=10,
    )
    r_feeds.raise_for_status()
    feeds = r_feeds.json().get("subscriptions", [])

    # Fix: handle case where feeds might be empty
    feed_count = len(feeds) if feeds else 1
    items_per_feed = max(3, limit // feed_count)
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
            feed_items = r_feed.json().get("items", [])
            for item in feed_items:
                canonical = item.get("canonical") or []
                url = canonical.get("href", "") if canonical and isinstance(canonical, dict) else ""
                source = item.get("origin", {}).get("title", "unknown source")
                title = unescape(item.get("title", "")).strip()
                published_ts = item.get("published", 0)
                published = datetime.fromtimestamp(published_ts).strftime("%Y-%m-%d") if published_ts else ""
                raw_summary = item.get("summary", {}).get("content", "")
                summary_text = re.sub(r"<[^>]+>", "", raw_summary or "").strip()
                items.append({
                    "title": title,
                    "source": source,
                    "url": url,
                    "published": published,
                    "summary": summary_text[:1000],
                })
    return items

def match_theme(title, summary):
    """Match item to theme based on keywords"""
    text = (title + " " + summary).lower()
    themes = {
        "AI & Technology": ["ai", "gpt", "llama", "model", "neural", "deep learning", "chatbot", "claude", "codex", "openai", "gemini", "spark", "antigravity", "quantum", "algorithm", "code", "llm", "openai", "codex", "copilot", "github"],
        "Metal Music": ["metal", "band", "album", "guitar", "drums", "vocals", "tour", "concert", "festival", "crüe", "sixx", "vincent", "neil", "coppersmith", "carpenter", "cathedral", "mötley", "ninety", "bury tomorrow", "brent hinds", "john carpenter", "guitar solo"],
        "Security": ["security", "breach", "hack", "vulnerability", "malware", "ransomware", "phishing", "cyber", "darkreading", "exploit", "patch", "github", "breach", "privacy", "tracking"],
        "General News": ["news", "bbc", "nbc", "congo", "ebola", "india", "cockroach", "politics", "election", "government", "world", "trump", "senate", "house", "nbc", "mayor", "twitch", "waymo", "floods", "gaza", "flotilla"],
        "Tech": ["apple", "samsung", "microsoft", "google", "android", "ios", "iphone", "watch", "mac", "pixel", "surface", "watch", "airpods", "tv", "9to5mac", "techcrunch", "decoder", "iphone", "apple watch", "airpods"],
        "Science": ["science", "research", "study", "discovery", "nasa", "space", "climate", "environment", "biology", "chemistry", "physics", "astronomy", "genetics", "dna", "virus", "vaccine"],
    }
    
    scores = {}
    for theme, keywords in themes.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[theme] = score
    if scores:
        return max(scores, key=scores.get)
    return "General News"

def synthesize_digest(items):
    """Create synthesized digest from items"""
    if not items:
        return "NO_UNREAD_ITEMS"
    
    # Group by theme
    themed = defaultdict(list)
    for c in items:
        theme = match_theme(c["title"], c["summary"])
        themed[theme].append(c)
    
    # Build digest
    digest_lines = ["Good morning, baby. Here's your news digest:"]
    
    for theme, items in themed.items():
        if not items:
            continue
        digest_lines.append(f"\n**{theme}**")
        
        # Sort by recency
        def get_date(item):
            return item.get("published", "0000-00-00")
        sorted_items = sorted(items, key=get_date, reverse=True)
        
        # Take up to 8 items for synthesis (more detailed as requested)
        top = sorted_items[:8]
        
        # Create synthesis paragraph
        if len(top) == 0:
            continue
        elif len(top) == 1:
            para = f"{top[0]['title']} ({top[0]['source']})."
        else:
            # Build a list of phrases
            phrases = [f"{it['title']} ({it['source']})" for it in top]
            # Combine with transitions to avoid list feel
            if len(top) == 2:
                para = f"{phrases[0]}; meanwhile, {phrases[1]}."
            elif len(top) == 3:
                para = f"{phrases[0]}; additionally, {phrases[1]}; meanwhile, {phrases[2]}."
            elif len(top) == 4:
                para = f"{phrases[0]}; additionally, {phrases[1]}; meanwhile, {phrases[2]}; furthermore, {phrases[3]}."
            elif len(top) == 5:
                para = f"{phrases[0]}; additionally, {phrases[1]}; meanwhile, {phrases[2]}; furthermore, {phrases[3]}; lastly, {phrases[4]}."
            else:
                # For 6-8 items, use a combination
                para = f"{phrases[0]}; additionally, {phrases[1]}; meanwhile, {phrases[2]}; furthermore, {phrases[3]}; lastly, {phrases[4]}."
                if len(top) > 5:
                    para += f" Moreover, {phrases[5]}."
                if len(top) > 6:
                    para += f" Also, {phrases[6]}."
                if len(top) > 7:
                    para += f" Finally, {phrases[7]}."
        # Ensure ends with period
        if not para.endswith('.'):
            para += '.'
        # Capitalize first letter
        para = para[0].upper() + para[1:]
        digest_lines.append(para)
        
        # Note about additional items
        remaining = len(items) - len(top)
        if remaining > 0:
            digest_lines.append(f"There are {remaining} more stories on this theme.")
    
    digest_lines.append("\nWant me to expand on any topic? Just ask, baby.")
    return "\n".join(digest_lines)

def main():
    """Main function"""
    try:
        headers, base = authenticate_freshrss()
        items = fetch_items(headers, base)
        digest = synthesize_digest(items)
        print(digest)
    except Exception as e:
        print(f"Error generating news digest: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())