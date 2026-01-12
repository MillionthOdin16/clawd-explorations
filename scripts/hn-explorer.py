#!/usr/bin/env python3
"""
Hacker News Explorer - Extract and analyze HN stories
"""
import sys
import urllib.request
import re
from html.parser import HTMLParser

class HNStoryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stories = []
        self.current_story = None
        self.in_title = False
        self.in_score = False
        self.in_comment = False
        self.capture_text = False

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'class' and 'titlelink' in value:
                    self.current_story = {'url': ''}
                    self.capture_text = True
                elif attr == 'href' and self.current_story is not None:
                    self.current_story['url'] = value

    def handle_data(self, data):
        if self.capture_text and self.current_story is not None:
            if 'title' not in self.current_story:
                self.current_story['title'] = data
                self.stories.append(self.current_story)
                self.current_story = None
                self.capture_text = False

def explore_hn():
    url = "https://news.ycombinator.com"
    print(f"Fetching: {url}")
    print("=" * 80)

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; ClawdHNExplorer/1.0)'}
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('utf-8', errors='ignore')
            print(f"Fetched {len(data)} characters\n")

            # Use regex to extract stories more reliably
            # HN story format: <a class="titlelink" href="url">title</a>
            story_pattern = r'<a class="titlelink" href="([^"]+)">([^<]+)</a>'
            matches = re.findall(story_pattern, data)

            print(f"Found {len(matches)} stories\n")

            print("Top 15 Stories:")
            print("=" * 80)
            for i, (url, title) in enumerate(matches[:15], 1):
                print(f"{i}. {title}")
                print(f"   {url}")
                print()

            # Extract domains
            domains = {}
            for url, title in matches:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                if domain:
                    domains[domain] = domains.get(domain, 0) + 1

            print("\nTop 15 Domains:")
            print("=" * 80)
            sorted_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)
            for domain, count in sorted_domains[:15]:
                print(f"{domain}: {count} stories")

            print(f"\n\nTotal unique domains: {len(domains)}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    explore_hn()
