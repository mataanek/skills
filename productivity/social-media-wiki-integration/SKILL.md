---
name: social-media-wiki-integration
description: Extract educational content from social media threads and save as markdown wiki with images.
---
# Social Media Wiki Integration Skill

## Description
Extract educational content from social media threads (e.g., X/Twitter) and save it as a markdown wiki page with associated images. This skill automates the process of collecting valuable educational threads, preserving formatting, and downloading referenced media for offline wiki use.

## When to Use
- You encounter a valuable educational thread on X/Twitter or similar platform.
- You want to preserve the content in your personal/wiki knowledge base.
- The thread includes images or media you wish to retain.

## Steps
1. **Navigate to the post**
   - Use `browser_navigate` to load the tweet URL.
   - Handle cookie consent popups if present (click "Accept all cookies" or similar).

2. **Extract the main text content**
   - Prefer `web_extract` for the tweet URL (often returns the full thread text in markdown).
   - If blocked, use `browser_console` to query the tweet text via JavaScript (e.g., `document.querySelector('[data-testid="tweetText"]')?.innerText`).
   - For threaded content, consider navigating to the article view if available (look for links like `x.com/i/article/...`).

3. **Collect media URLs**
   - Call `browser_get_images` to retrieve all image URLs on the page.
   - Filter to relevant media (e.g., exclude avatars, icons unless needed).

4. **Download images**
   - Use an executable script (see `scripts/download_images.py`) or inline `execute_code` with `requests` to fetch each image.
   - Save images to a dedicated folder under the wiki directory (e.g., `wiki/educational/images/`).

5. **Save the markdown file**
   - Write the extracted content to a markdown file in the appropriate wiki location (e.g., `wiki/educational/<slug>.md`).
   - Include a section referencing the downloaded images (or embed them if desired).
   - Add a citation line with the original thread URL and date.

6. **Verify**
   - Confirm the markdown file exists and contains the expected content.
   - Confirm images are present and accessible.

## Pitfalls
- **Cookie popups**: Some regions require accepting cookies before content is visible. Look for buttons with text like "Accept all cookies" and click them via `browser_click`.
- **Rate limits**: Excessive requests to Twitter/X may trigger temporary blocks; space out requests if processing many threads.
- **Missing images**: Some images may be lazy-loaded or require JavaScript execution; scrolling the page (`browser_scroll`) can help load them.
- **Character limits**: Extracted text may be truncated; prefer `web_extract` for longer content when available.

## Reference
- Original workflow derived from saving Rahul's "20 AI Concepts You Must Understand in 2026" thread.
- Images are saved as-is; consider renaming to descriptive filenames if needed.

## Script
See `scripts/download_images.py` for a ready-to-use image downloader that accepts a list of URLs and a target directory.