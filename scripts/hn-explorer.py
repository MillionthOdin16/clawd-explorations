#!/usr/bin/env python3
"""
Hacker News Explorer - Extract and analyze HN stories.

Usage:
    python scripts/hn-explorer.py                  # Top 15 stories
    python scripts/hn-explorer.py --limit 30       # More stories
    python scripts/hn-explorer.py --domains       # Show domains only
    python scripts/hn-explorer.py --json         # JSON output
    python scripts/hn-explorer.py --help         # Show help
"""

import argparse
import json
import sys
import urllib.request
import re
from html.parser import HTMLParser
from urllib.parse import urlparse


class HNStoryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stories = []
        self.current_story = None
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
                self.current_story['title'] = data.strip()
                self.stories.append(self.current_story)
                self.current_story = None
                self.capture_text = False


def fetch_stories(url="https://news.ycombinator.com", limit=30):
    """Fetch stories from HN."""
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; ClawdHNExplorer/1.0)'}
    req = urllib.request.Request(url, headers=headers)
    
    with urllib.request.urlopen(req, timeout=10) as response:
        data = response.read().decode('utf-8', errors='ignore')
        
        # Use regex to extract stories
        story_pattern = r'<a class="titlelink" href="([^"]+)">([^<]+)</a>'
        matches = re.findall(story_pattern, data)
        
        stories = []
        for url, title in matches:
            domain = urlparse(url).netloc
            stories.append({
                "title": title.strip(),
                "url": url,
                "domain": domain if domain else urlparse(url).path.split('/')[1] if urlparse(url).path else url
            })
        
        return stories[:limit]


def format_stories(stories, show_domains=False):
    """Format stories for output."""
    if show_domains:
        domains = {}
        for story in stories:
            domain = story.get('domain', 'N/A')
            domains[domain] = domains.get(domain, 0) + 1
        
        sorted_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)
        output = []
        for domain, count in sorted_domains:
            output.append({"domain": domain, "count": count})
        return output
    return stories


def main():
    parser = argparse.ArgumentParser(
        description="Explore Hacker News stories and analyze trends.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=15,
        help="Number of stories to fetch (default: 15)"
    )
    parser.add_argument(
        "--domains", "-d",
        action="store_true",
        help="Show domain statistics instead of stories"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress headers and formatting"
    )
    parser.add_argument(
        "--url",
        default="https://news.ycombinator.com",
        help="HN URL to explore"
    )
    
    args = parser.parse_args()
    
    stories = fetch_stories(args.url, args.limit)
    
    if args.json:
        result = {
            "success": True,
            "count": len(stories),
            "stories": format_stories(stories, args.domains)
        }
        print(json.dumps(result, indent=2))
        return 0
    
    if args.quiet:
        for story in stories:
            print(f"{story['title']}")
            print(f"{story['url']}")
        return 0
    
    if args.domains:
        formatted = format_stories(stories, show_domains=True)
        print("\nTop Domains:")
        print("=" * 40)
        for item in formatted[:15]:
            print(f"{item['domain']}: {item['count']} stories")
        print(f"\nTotal unique domains: {len(formatted)}")
        return 0
    
    # Default: Show stories
    print(f"\n{'=' * 80}")
    print(f"Hacker News Stories (Top {len(stories)})")
    print(f"{'=' * 80}\n")
    
    for i, story in enumerate(stories, 1):
        print(f"{i:2}. {story['title']}")
        print(f"   {story['url']}")
        print()
    
    # Domain stats
    domains = {}
    for story in stories:
        domain = story.get('domain', 'N/A')
        domains[domain] = domains.get(domain, 0) + 1
    
    print("\nTop 10 Domains:")
    print("=" * 40)
    sorted_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)
    for domain, count in sorted_domains[:10]:
        print(f"{domain}: {count} stories")
    
    print(f"\nTotal unique domains: {len(domains)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
