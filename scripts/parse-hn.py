#!/usr/bin/env python3
"""
Parse Hacker News stories from HTML
"""
import subprocess
import re

def parse_hn_stories():
    print("Fetching Hacker News stories...")
    print("=" * 80)
    print()

    # Fetch HN and extract story links
    result = subprocess.run(
        ['curl', '-s', 'https://news.ycombinator.com'],
        capture_output=True,
        text=True
    )

    html = result.stdout

    # Find all external links with their titles
    # Pattern: <a href="URL">TITLE</a>
    pattern = r'<a href="(https?://[^"]+)">([^<]+)</a>'
    matches = re.findall(pattern, html)

    print(f"Found {len(matches)} links total\n")

    # Filter to likely stories (skip user links, etc.)
    stories = []
    for url, title in matches:
        # Skip navigation links and short titles
        if len(title) > 30 and 'ycombinator.com' not in url:
            stories.append((title, url))

    print(f"Filtered to {len(stories)} story candidates\n")

    print("Top 30 Stories:")
    print("=" * 80)
    for i, (title, url) in enumerate(stories[:30], 1):
        # Clean up HTML entities
        title = title.replace('&amp;', '&')
        title = title.replace('&#x27;', "'")
        title = title.replace('&quot;', '"')
        print(f"{i}. {title}")
        print(f"   {url}")
        print()

    # Extract domains
    from urllib.parse import urlparse
    domains = {}
    for url, title in stories:
        domain = urlparse(url).netloc
        if domain:
            domains[domain] = domains.get(domain, 0) + 1

    print("\n" + "=" * 80)
    print("Top 20 Domains:")
    print("=" * 80)
    sorted_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)
    for domain, count in sorted_domains[:20]:
        print(f"{domain:40s} {count}")

    print(f"\nTotal unique domains: {len(domains)}")

if __name__ == "__main__":
    parse_hn_stories()
