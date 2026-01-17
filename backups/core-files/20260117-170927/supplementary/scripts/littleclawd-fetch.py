#!/usr/bin/env python3
"""Simple web fetcher for LittleClawd"""
import urllib.request
import urllib.error
import sys
import json
from datetime import datetime

def fetch_url(url, timeout=10):
    """Fetch a URL and return content"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'LittleClawd/1.0'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read().decode('utf-8', errors='ignore')
            return {
                'success': True,
                'status': response.status,
                'content_length': len(content),
                'content_type': response.headers.get('Content-Type', 'unknown'),
                'content_preview': content[:500]
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: fetch.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"LittleClawd fetching: {url}")
    print(f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()

    result = fetch_url(url)

    if result['success']:
        print(f"Status: {result['status']}")
        print(f"Content-Type: {result['content_type']}")
        print(f"Content-Length: {result['content_length']}")
        print()
        print("Preview:")
        print("-" * 60)
        print(result['content_preview'])
        print("-" * 60)
    else:
        print(f"Error: {result['error']}")
