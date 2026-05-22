#!/usr/bin/env python3
"""
Download images from a list of URLs to a specified directory.
Usage: python3 download_images.py <url_file> <output_dir>
   or: python3 download_images.py --urls "url1,url2,url3" --output ./images
"""

import os
import sys
import argparse
import requests
from urllib.parse import urlparse

def download_image(url, output_dir):
    """Download a single image from URL to output_dir."""
    try:
        # Parse URL to get filename
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path).split('?')[0]
        
        # If no filename in path, generate one
        if not filename or '.' not in filename:
            # Use hash of URL as filename
            import hashlib
            filename = hashlib.md5(url.encode()).hexdigest()[:8] + '.jpg'
        
        # Ensure filename is safe
        filename = "".join(c for c in filename if c.isalnum() or c in '._-')
        if not filename:
            filename = 'image.jpg'
            
        filepath = os.path.join(output_dir, filename)
        
        # Skip if already exists
        if os.path.exists(filepath):
            print(f"Skipping existing: {filename}")
            return True
            
        # Download
        resp = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        resp.raise_for_status()
        
        # Check if content is actually an image
        content_type = resp.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            print(f"Warning: {url} does not appear to be an image (content-type: {content_type})")
            
        with open(filepath, 'wb') as f:
            f.write(resp.content)
            
        print(f"Downloaded: {filename} ({len(resp.content)} bytes)")
        return True
        
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Download images from URLs')
    parser.add_argument('url_file', nargs='?', help='File containing URLs (one per line)')
    parser.add_argument('--urls', help='Comma-separated list of URLs')
    parser.add_argument('--output', default='./images', help='Output directory (default: ./images)')
    parser.add_argument('--max', type=int, help='Maximum number of images to download')
    
    args = parser.parse_args()
    
    # Collect URLs
    urls = []
    if args.url_file:
        with open(args.url_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    elif args.urls:
        urls = [u.strip() for u in args.urls.split(',') if u.strip()]
    else:
        parser.error("Either url_file or --urls must be provided")
    
    if args.max:
        urls = urls[:args.max]
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Download images
    success = 0
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] ", end='')
        if download_image(url, args.output):
            success += 1
    
    print(f"\nCompleted: {success}/{len(urls)} images downloaded")
    return 0 if success == len(urls) else 1

if __name__ == '__main__':
    sys.exit(main())