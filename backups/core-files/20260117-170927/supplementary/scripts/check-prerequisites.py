#!/usr/bin/env python3
"""
Prerequisite Checker - Check tool availability before use (v1.0.0)

Usage:
    python scripts/check-prerequisites.py <tool>
    python scripts/check-prerequisites.py all

Tools:
    browser      - Check browser availability (ARM64: Firefox)
    gateway      - Check gateway status
    coolify      - Check Coolify API accessibility
    exa          - Check Exa API key
    context7     - Check Redis connection
    all          - Check all prerequisites
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error


class PrerequisiteChecker:
    """Check tool availability and prerequisites."""
    
    def __init__(self):
        self.results = {}
    
    def check_browser(self) -> dict:
        """Check browser availability (ARM64: Firefox)."""
        result = {"status": "unknown", "message": "", "recommendation": ""}
        
        # Check if Firefox is available
        firefox_paths = [
            "/usr/bin/firefox",
            "/usr/local/bin/firefox",
            "/opt/homebrew/bin/firefox",
        ]
        
        firefox_available = any(os.path.exists(p) for p in firefox_paths)
        
        if firefox_available:
            result["status"] = "ready"
            result["message"] = "Firefox available (ARM64 compatible)"
            result["recommendation"] = "Use browser tool with Firefox"
        else:
            result["status"] = "missing"
            result["message"] = "No browser found"
            result["recommendation"] = "Install Firefox: brew install firefox"
        
        return result
    
    def check_gateway(self) -> dict:
        """Check gateway status."""
        result = {"status": "unknown", "message": "", "recommendation": ""}
        
        # Try to connect to gateway
        gateway_urls = [
            "http://127.0.0.1:18789/health",
            "http://127.0.0.1:18789/",
        ]
        
        for url in gateway_urls:
            try:
                req = urllib.request.Request(url, method="GET")
                with urllib.request.urlopen(req, timeout=3) as response:
                    if response.status == 200:
                        result["status"] = "ready"
                        result["message"] = "Gateway is accessible"
                        result["recommendation"] = "Gateway tools are available"
                        return result
            except:
                continue
        
        result["status"] = "unavailable"
        result["message"] = "Gateway not accessible"
        result["recommendation"] = "Start gateway: clawdbot daemon start"
        return result
    
    def check_coolify(self) -> dict:
        """Check Coolify API accessibility."""
        result = {"status": "unknown", "message": "", "recommendation": ""}
        
        api_token = os.environ.get("COOLIFY_API_TOKEN", "")
        if not api_token:
            result["status"] = "missing_config"
            result["message"] = "COOLIFY_API_TOKEN not set"
            result["recommendation"] = "Set: export COOLIFY_API_TOKEN='your-token'"
            return result
        
        try:
            url = "https://coolify.bradarr.com/api/v1/applications"
            req = urllib.request.Request(
                url,
                method="GET",
                headers={"Authorization": f"Bearer {api_token}"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    result["status"] = "ready"
                    result["message"] = "Coolify API accessible"
                    result["recommendation"] = "Coolify operations available"
        except urllib.error.HTTPError as e:
            result["status"] = "error"
            result["message"] = f"HTTP {e.code}"
            result["recommendation"] = "Check API token and permissions"
        except Exception as e:
            result["status"] = "unavailable"
            result["message"] = str(e)
            result["recommendation"] = "Check network connection"
        
        return result
    
    def check_exa(self) -> dict:
        """Check Exa API key."""
        result = {"status": "unknown", "message": "", "recommendation": ""}
        
        api_key = os.environ.get("EXA_API_KEY", "")
        if not api_key:
            result["status"] = "missing_config"
            result["message"] = "EXA_API_KEY not set"
            result["recommendation"] = "Set: export EXA_API_KEY='your-key'"
        else:
            result["status"] = "ready"
            result["message"] = "EXA_API_KEY configured"
            result["recommendation"] = "Exa operations available"
        
        return result
    
    def check_context7(self) -> dict:
        """Check Context7 (Redis) connection."""
        result = {"status": "unknown", "message": "", "recommendation": ""}
        
        upstash_token = os.environ.get("UPSTASH_REST_API_TOKEN", "")
        context7_key = os.environ.get("CONTEXT7_API_KEY", "")
        
        if not upstash_token and not context7_key:
            result["status"] = "missing_config"
            result["message"] = "UPSTASH_REST_API_TOKEN not set"
            result["recommendation"] = "Set: export UPSTASH_REST_API_TOKEN='your-token'"
        else:
            result["status"] = "ready"
            result["message"] = "Context7 credentials configured"
            result["recommendation"] = "Context7 operations available"
        
        return result
    
    def check_all(self) -> dict:
        """Check all prerequisites."""
        checks = {
            "browser": self.check_browser,
            "gateway": self.check_gateway,
            "coolify": self.check_coolify,
            "exa": self.check_exa,
            "context7": self.check_context7,
        }
        
        results = {}
        for name, check_func in checks.items():
            results[name] = check_func()
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description="Check tool prerequisites before use",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
    python scripts/check-prerequisites.py browser
    python scripts/check-prerequisites.py gateway
    python scripts/check-prerequisites.py all

EXIT CODES:
    0 - All checked tools are ready
    1 - One or more tools have issues
"""
    )
    
    parser.add_argument(
        "tool",
        choices=["browser", "gateway", "coolify", "exa", "context7", "all"],
        help="Tool to check"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    checker = PrerequisiteChecker()
    
    if args.tool == "all":
        results = checker.check_all()
    else:
        check_func = getattr(checker, f"check_{args.tool}")
        results = {args.tool: check_func()}
    
    if args.json:
        print(json.dumps(results, indent=2))
        return
    
    # Human-readable output
    all_ready = True
    
    for tool, result in results.items():
        status = result["status"]
        icon = "✅" if status == "ready" else "⚠️" if status == "missing_config" else "❌"
        
        print(f"{icon} {tool.upper()}")
        print(f"   Status: {result['message']}")
        
        if status != "ready":
            all_ready = False
            print(f"   Fix: {result['recommendation']}")
        print()
    
    # Exit code
    sys.exit(0 if all_ready else 1)


if __name__ == "__main__":
    main()
