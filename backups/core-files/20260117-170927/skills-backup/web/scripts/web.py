#!/usr/bin/env python3
"""Web browsing wrapper using Clawdbot's browser tool.

Provides convenient functions for:
- Opening URLs
- Getting page content
- Searching the web
- Extracting specific information
"""

import argparse
import json
import sys
import os
import time
import subprocess

# Try to import clawdbot tools, fallback to subprocess
try:
    from clawdbot.tools.browser import browser
    BROWSER_AVAILABLE = True
except ImportError:
    BROWSER_AVAILABLE = False

def open_url(url: str, wait: bool = True) -> dict:
    """Open a URL and return page content."""
    if BROWSER_AVAILABLE:
        result = browser(action="open", targetUrl=url)
        if wait:
            time.sleep(2)  # Wait for page to load
        return result
    else:
        # Fallback: use subprocess
        result = subprocess.run(
            ["curl", "-s", url],
            capture_output=True,
            text=True
        )
        return {"content": result.stdout[:5000]}

def get_page(url: str, selector: str = None) -> str:
    """Get page content, optionally using selector."""
    if BROWSER_AVAILABLE:
        result = browser(action="open", targetUrl=url)
        time.sleep(2)
        
        if selector:
            # Extract specific element
            result = browser(action="snapshot", selector=selector)
        else:
            # Get full page
            result = browser(action="snapshot", format="aria")
        
        return str(result)
    else:
        result = subprocess.run(
            ["curl", "-s", url],
            capture_output=True,
            text=True
        )
        return result.stdout[:10000]

def search_web(query: str, num_results: int = 5) -> list:
    """Search the web using DuckDuckGo."""
    url = f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"
    
    if BROWSER_AVAILABLE:
        browser(action="open", targetUrl=url)
        time.sleep(2)
        result = browser(action="snapshot", format="aria")
        
        # Parse results
        results = []
        lines = str(result).split('\n')
        for line in lines:
            if 'href="https://' in line and 'duckduckgo' not in line:
                start = line.find('href="') + 6
                end = line.find('"', start)
                if start > 5 and end > start:
                    url = line[start:end]
                    if url not in results and len(results) < num_results:
                        results.append(url)
        return results
    else:
        # Fallback: use curl and basic parsing
        result = subprocess.run(
            ["curl", "-s", f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"],
            capture_output=True,
            text=True
        )
        return [query]  # Placeholder

def get_page_text(url: str, max_chars: int = 5000) -> str:
    """Get plain text from a page."""
    if BROWSER_AVAILABLE:
        browser(action="open", targetUrl=url)
        time.sleep(2)
        result = browser(action="snapshot", format="ai")
        text = str(result)
        return text[:max_chars] if len(text) > max_chars else text
    else:
        result = subprocess.run(
            ["curl", "-s", "-L", url],
            capture_output=True,
            text=True
        )
        return result.stdout[:max_chars]

def take_screenshot(url: str, out_path: str = "/tmp/screenshot.png") -> str:
    """Take a screenshot of a page."""
    if BROWSER_AVAILABLE:
        browser(action="open", targetUrl=url)
        time.sleep(3)
        result = browser(action="screenshot", outPath=out_path)
        return f"Screenshot saved to {out_path}"
    else:
        return "Browser not available, cannot take screenshot"

def main():
    parser = argparse.ArgumentParser(description="Web browsing wrapper")
    parser.add_argument("command", choices=["open", "get", "search", "text", "screenshot"],
                       help="Command to run")
    parser.add_argument("url", help="URL or search query")
    parser.add_argument("--selector", help="CSS selector for element extraction")
    parser.add_argument("--output", help="Output file for screenshot")
    parser.add_argument("--num", type=int, default=5, help="Number of search results")
    
    args = parser.parse_args()
    
    if args.command == "open":
        result = open_url(args.url)
        print(f"Opened: {args.url}")
        print(f"Result: {result}")
    
    elif args.command == "get":
        if args.selector:
            result = get_page(args.url, args.selector)
        else:
            result = get_page(args.url)
        print(result[:2000])
    
    elif args.command == "search":
        results = search_web(args.url, args.num)
        for i, url in enumerate(results, 1):
            print(f"{i}. {url}")
    
    elif args.command == "text":
        result = get_page_text(args.url)
        print(result)
    
    elif args.command == "screenshot":
        out = args.output or "/tmp/screenshot.png"
        result = take_screenshot(args.url, out)
        print(result)

if __name__ == "__main__":
    main()
