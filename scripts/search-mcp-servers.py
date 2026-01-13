#!/usr/bin/env python3
"""Search for relevant MCP servers and skills for context management."""

import json
import subprocess

def gh_api(endpoint):
    """Call GitHub API."""
    result = subprocess.run(
        ["gh", "api", endpoint],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return json.loads(result.stdout)
    return None

def search_repos(query):
    """Search GitHub for repositories."""
    result = subprocess.run(
        ["gh", "api", f"search/repositories?q={query}&per_page=10"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        data = json.loads(result.stdout)
        return data.get("items", [])
    return []

def main():
    print("🔍 Searching for relevant MCP servers and tools...\n")
    
    # Search terms
    searches = [
        ("context7+mcp+server", "Context/Memory MCP servers"),
        ("mcp+server+memory+context", "Memory context MCP"),
        ("mcp+server+documentation+docs", "Documentation MCP servers"),
        ("mcp+server+file+operations", "File operations MCP"),
        ("modelcontextprotocol+servers+context", "MCP context servers"),
    ]
    
    all_results = []
    for query, desc in searches:
        print(f"📦 {desc}:")
        repos = search_repos(query)
        for repo in repos[:5]:
            print(f"  ⭐ {repo['stargazers_count']:5} | {repo['full_name']}")
            print(f"     {repo.get('description', 'N/A')[:80]}")
            print()
            all_results.append(repo)
        print()
    
    # Save results
    with open("/home/opc/clawd/memory/MCP-SERVERS-RESEARCH.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"💾 Saved {len(all_results)} results to MCP-SERVERS-RESEARCH.json")

if __name__ == "__main__":
    main()
