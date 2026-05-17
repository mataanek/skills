#!/usr/bin/env python3
import os
import sys
import json
import requests

BASE_URL = os.getenv("FRESHRSS_GREADER_URL", "").rstrip("/")
USERNAME = os.getenv("FRESHRSS_USERNAME", "")
API_PASSWORD = os.getenv("FRESHRSS_API_PASSWORD", "")
LIMIT = int(os.getenv("FRESHRSS_LIMIT", "10"))


def login(base_url, username, api_password):
    r = requests.post(
        f"{base_url}/accounts/ClientLogin",
        data={"Email": username, "Passwd": api_password},
        timeout=20,
    )
    r.raise_for_status()

    auth_line = next((line for line in r.text.splitlines() if line.startswith("Auth=")), None)
    if not auth_line:
        raise RuntimeError(f"No Auth token returned. Response was:\n{r.text}")

    return auth_line.split("=", 1)[1].strip()


def fetch_items(base_url, token, limit):
    r = requests.get(
        f"{base_url}/reader/api/0/stream/contents/reading-list",
        headers={"Authorization": f"GoogleLogin auth={token}"},
        params={"output": "json", "n": limit},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def normalize_item(item):
    canonical = item.get("canonical") or []
    alternate = item.get("alternate") or []
    origin = item.get("origin") or {}
    summary = item.get("summary") or {}

    url = ""
    if canonical and isinstance(canonical, list):
        url = canonical[0].get("href", "") or url
    if not url and alternate and isinstance(alternate, list):
        url = alternate[0].get("href", "") or url

    return {
        "id": item.get("id", ""),
        "title": item.get("title", ""),
        "url": url,
        "source": origin.get("title", ""),
        "source_html_url": origin.get("htmlUrl", ""),
        "published": item.get("published"),
        "categories": item.get("categories", []),
        "author": item.get("author", ""),
        "summary_html": summary.get("content", ""),
    }


def main():
    if not BASE_URL:
        print(json.dumps({"error": "Missing FRESHRSS_GREADER_URL"}, indent=2))
        sys.exit(1)

    if not USERNAME:
        print(json.dumps({"error": "Missing FRESHRSS_USERNAME"}, indent=2))
        sys.exit(1)

    if not API_PASSWORD:
        print(json.dumps({"error": "Missing FRESHRSS_API_PASSWORD"}, indent=2))
        sys.exit(1)

    token = login(BASE_URL, USERNAME, API_PASSWORD)
    payload = fetch_items(BASE_URL, token, LIMIT)
    items = payload.get("items", [])
    normalized = [normalize_item(item) for item in items]

    print(json.dumps(normalized, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()