#!/usr/bin/env python3
"""Playwright CLI for Clawdbot - Browser automation on ARM64."""

import argparse
import sys
import json
import asyncio
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright

DEFAULT_OUTPUT_DIR = Path.home() / ".clawdbot" / "playwright" / "screenshots"
DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def get_browser():
    """Launch Firefox browser."""
    p = await async_playwright().start()
    browser = await p.firefox.launch(headless=True)
    return p, browser

async def cmd_navigate(url):
    """Navigate to URL and return status."""
    if not urlparse(url).scheme:
        url = "https://" + url
    
    p, browser = await get_browser()
    page = await browser.new_page()
    await page.goto(url)
    result = {"url": page.url, "title": await page.title(), "status": "success"}
    await browser.close()
    await p.stop()
    return result

async def cmd_content(url):
    """Get page content as clean text."""
    if not urlparse(url).scheme:
        url = "https://" + url
    
    p, browser = await get_browser()
    page = await browser.new_page()
    await page.goto(url, wait_until="domcontentloaded")
    
    text = await page.evaluate("""
        () => {
            document.querySelectorAll('script, style, nav, footer, header').forEach(el => el.remove());
            return document.body.innerText.trim();
        }
    """)
    
    result = {"url": page.url, "title": await page.title(), "content": text[:5000], "status": "success"}
    await browser.close()
    await p.stop()
    return result

async def cmd_title(url):
    """Get page title."""
    if not urlparse(url).scheme:
        url = "https://" + url
    
    p, browser = await get_browser()
    page = await browser.new_page()
    await page.goto(url)
    result = {"title": await page.title(), "url": page.url, "status": "success"}
    await browser.close()
    await p.stop()
    return result

async def cmd_screenshot(url, output=None):
    """Take screenshot of page."""
    if not urlparse(url).scheme:
        url = "https://" + url
    
    if output is None:
        import time
        filename = f"screenshot_{Path(urlparse(url).netloc).stem}_{int(time.time())}.png"
        output = str(DEFAULT_OUTPUT_DIR / filename)
    
    p, browser = await get_browser()
    page = await browser.new_page()
    await page.set_viewport_size({"width": 1280, "height": 800})
    await page.goto(url, wait_until="networkidle")
    await page.screenshot(path=output, full_page=True)
    result = {"screenshot": output, "status": "success"}
    await browser.close()
    await p.stop()
    return result

async def cmd_find(url, selector):
    """Find elements matching selector."""
    if not urlparse(url).scheme:
        url = "https://" + url
    
    p, browser = await get_browser()
    page = await browser.new_page()
    await page.goto(url)
    
    elements = await page.query_selector_all(selector)
    results = []
    for el in elements[:20]:
        text = await el.inner_text() if el else ""
        tag = await el.evaluate("el => el.tagName") if el else ""
        results.append({"tag": tag, "text": text[:200]})
    
    result = {"selector": selector, "count": len(results), "elements": results, "status": "success"}
    await browser.close()
    await p.stop()
    return result

async def cmd_links(url):
    """Extract all links from page."""
    if not urlparse(url).scheme:
        url = "https://" + url
    
    p, browser = await get_browser()
    page = await browser.new_page()
    await page.goto(url)
    
    links = await page.evaluate("""
        () => Array.from(document.querySelectorAll('a'))
            .filter(a => a.href)
            .map(a => ({text: a.innerText.trim().substring(0, 100), href: a.href}))
    """)
    
    result = {"url": page.url, "links": links[:50], "count": len(links), "status": "success"}
    await browser.close()
    await p.stop()
    return result

async def cmd_snapshot(url, format_type="ai"):
    """Get full page snapshot for AI."""
    if not urlparse(url).scheme:
        url = "https://" + url
    
    p, browser = await get_browser()
    page = await browser.new_page()
    await page.goto(url)
    
    if format_type == "ai":
        snapshot = await page.evaluate("""
            () => {
                return Array.from(document.querySelectorAll('a, button, input, select, textarea, h1, h2, h3, h4, h5, h6, p, img, form'))
                    .slice(0, 100).map(el => ({
                        tag: el.tagName.toLowerCase(),
                        text: el.innerText ? el.innerText.substring(0, 100) : '',
                        href: el.href || el.action || '',
                        placeholder: el.placeholder || '',
                        type: el.type || '',
                        id: el.id || '',
                        class: el.className ? el.className.substring(0, 50) : ''
                    }));
            }
        """)
    else:
        snapshot = await page.accessibility_snapshot()
    
    result = {"url": page.url, "format": format_type, "snapshot": snapshot, "status": "success"}
    await browser.close()
    await p.stop()
    return result

async def cmd_click(url, selector):
    """Click an element."""
    if not urlparse(url).scheme:
        url = "https://" + url
    
    p, browser = await get_browser()
    page = await browser.new_page()
    await page.goto(url)
    await page.click(selector)
    result = {"url": page.url, "clicked": selector, "status": "success"}
    await browser.close()
    await p.stop()
    return result

async def cmd_type(url, selector, text):
    """Type text into an element."""
    if not urlparse(url).scheme:
        url = "https://" + url
    
    p, browser = await get_browser()
    page = await browser.new_page()
    await page.goto(url)
    await page.fill(selector, text)
    result = {"url": page.url, "typed": text[:50], "selector": selector, "status": "success"}
    await browser.close()
    await p.stop()
    return result

async def cmd_scroll(url, direction="down"):
    """Scroll the page."""
    if not urlparse(url).scheme:
        url = "https://" + url
    
    p, browser = await get_browser()
    page = await browser.new_page()
    await page.goto(url)
    
    if direction == "down":
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    else:
        await page.evaluate("window.scrollTo(0, 0)")
    
    result = {"url": page.url, "scrolled": direction, "status": "success"}
    await browser.close()
    await p.stop()
    return result

async def main():
    parser = argparse.ArgumentParser(description="Playwright browser automation")
    parser.add_argument("command", choices=[
        "navigate", "content", "title", "screenshot", 
        "find", "links", "snapshot", "click", "type", "scroll"
    ])
    parser.add_argument("url", help="URL to interact with")
    parser.add_argument("--selector", "-s", help="CSS selector for actions")
    parser.add_argument("--text", "-t", help="Text to type")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--direction", "-d", choices=["up", "down"], default="down")
    parser.add_argument("--format", choices=["ai", "aria"], default="ai")
    parser.add_argument("--raw", action="store_true", help="Output raw JSON")
    
    args = parser.parse_args()
    
    try:
        if args.command == "navigate":
            result = await cmd_navigate(args.url)
        elif args.command == "content":
            result = await cmd_content(args.url)
        elif args.command == "title":
            result = await cmd_title(args.url)
        elif args.command == "screenshot":
            result = await cmd_screenshot(args.url, args.output)
        elif args.command == "find":
            if not args.selector:
                print("Error: --selector required for 'find' command")
                sys.exit(1)
            result = await cmd_find(args.url, args.selector)
        elif args.command == "links":
            result = await cmd_links(args.url)
        elif args.command == "snapshot":
            result = await cmd_snapshot(args.url, args.format)
        elif args.command == "click":
            if not args.selector:
                print("Error: --selector required for 'click' command")
                sys.exit(1)
            result = await cmd_click(args.url, args.selector)
        elif args.command == "type":
            if not args.selector or not args.text:
                print("Error: --selector and --text required for 'type' command")
                sys.exit(1)
            result = await cmd_type(args.url, args.selector, args.text)
        elif args.command == "scroll":
            result = await cmd_scroll(args.url, args.direction)
        else:
            result = {"error": "Unknown command"}
        
        if args.raw:
            print(json.dumps(result))
        else:
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        print(json.dumps({"error": str(e), "status": "failed"}, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
