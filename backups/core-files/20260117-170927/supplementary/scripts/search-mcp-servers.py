#!/usr/bin/env python3
"""
Search for relevant MCP servers and skills for context management.

Usage:
    python scripts/search-mcp-servers.py              # Run search
    python scripts/search-mcp-servers.py --json       # JSON output
    python scripts/search-mcp-servers.py --quiet      # Quiet mode
    python scripts/search-mcp-servers.py --help      # Show help
"""

import argparse
import json
import subprocess
import sys


def gh_api(endpoint):
    """Call GitHub API."""
    result = subprocess.run(
        ["gh", "api", endpoint],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return None
    return None


def search_repos(query, max_results=10):
    """Search GitHub for repositories."""
    result = subprocess.run(
        ["gh", "api", f"search/repositories?q={query}&per_page={max_results}"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            return data.get("items", [])
        except json.JSONDecodeError:
            return []
    return []


def format_output(results, verbose=False):
    """Format results for output."""
    output = []
    for repo in results:
        entry = {
            "name": repo.get("full_name", "N/A"),
            "stars": repo.get("stargazers_count", 0),
            "description": repo.get("description", "N/A"),
            "url": repo.get("html_url", "N/A"),
        }
        if verbose:
            entry["topics"] = repo.get("topics", [])
            entry["language"] = repo.get("language", "N/A")
        output.append(entry)
    return output


def main():
    parser = argparse.ArgumentParser(
        description="Search for relevant MCP servers and skills for context management.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress verbose output"
    )
    parser.add_argument(
        "--output",
        default="/home/opc/clawd/memory/MCP-SERVERS-RESEARCH.json",
        help="Output file path"
    )
    parser.add_argument(
        "--max-per-query",
        type=int,
        default=10,
        help="Maximum results per query"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output with more details"
    )
    
    args = parser.parse_args()
    
    # Search terms
    searches = [
        ("context7+mcp+server", "Context/Memory MCP servers"),
        ("mcp+server+memory+context", "Memory context MCP"),
        ("mcp+server+documentation+docs", "Documentation MCP servers"),
        ("mcp+server+file+operations", "File operations MCP"),
        ("modelcontextprotocol+servers+context", "MCP context servers"),
    ]
    
    all_results = []
    
    if not args.quiet:
        print("🔍 Searching for relevant MCP servers and tools...\n")
    
    for query, desc in searches:
        if not args.quiet:
            print(f"📦 {desc}:")
        
        repos = search_repos(query, args.max_per_query)
        formatted = format_output(repos, args.verbose)
        
        for i, repo in enumerate(formatted):
            all_results.append(repo)
            if not args.quiet:
                print(f"  ⭐ {repo['stars']:5} | {repo['name']}")
                print(f"     {repo['description'][:80]}")
                print()
        
        if not args.quiet:
            print()
    
    # Save results
    with open(args.output, "w") as f:
        json.dump(all_results, f, indent=2)
    
    if not args.quiet:
        print(f"💾 Saved {len(all_results)} results to {args.output}")
    
    # JSON output
    if args.json:
        result = {
            "success": True,
            "count": len(all_results),
            "results": all_results
        }
        print(json.dumps(result, indent=2))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
