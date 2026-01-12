#!/usr/bin/env python3
"""
Web Explorer - Fetch and analyze webpages
"""
import sys
import urllib.request
from urllib.error import URLError
import json
from html.parser import HTMLParser

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.title = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.links.append(value)
        elif tag == 'title':
            self.in_title = True

    def handle_data(self, data):
        if hasattr(self, 'in_title') and self.in_title:
            self.title = data
            self.in_title = False

def explore_url(url):
    print(f"Exploring: {url}")
    print("=" * 60)

    try:
        # Add user agent to avoid blocking
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; ClawdExplorer/1.0)'}
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=10) as response:
            content_type = response.headers.get('Content-Type', 'unknown')
            content_length = response.headers.get('Content-Length', 'unknown')
            status = response.status

            print(f"Status: {status}")
            print(f"Content-Type: {content_type}")
            print(f"Content-Length: {content_length}")
            print()

            # Read content
            data = response.read().decode('utf-8', errors='ignore')
            print(f"Content length: {len(data)} characters")
            print()

            # Extract title and links if HTML
            if 'text/html' in content_type:
                parser = LinkExtractor()
                parser.feed(data)

                print(f"Title: {parser.title}")
                print()
                print(f"Found {len(parser.links)} links")
                print()

                # Show first 10 links
                if parser.links:
                    print("First 10 links:")
                    for i, link in enumerate(parser.links[:10], 1):
                        print(f"  {i}. {link}")

                print()
                # Show first 500 chars of content
                print("Content preview (first 500 chars):")
                print("-" * 60)
                print(data[:500])
                print("-" * 60)

    except URLError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: web-explorer.py <url>")
        sys.exit(1)

    explore_url(sys.argv[1])
