#!/usr/bin/env python3
"""
Unified Skill Runner for Clawdbot

Provides a single entry point for all skill commands with:
- Smart command completion
- Common patterns across all skills
- Unified help system
- Cross-skill operations

Usage:
    python scripts/skill.py <skill> <command> [options]
    python scripts/skill.py help                    # Show all skills
    python scripts/skill.py <skill> help            # Show skill commands

Examples:
    python scripts/skill.py coolify apps list
    python scripts/skill.py exa search "AI consciousness"
    python scripts/skill.py context7 query "how does memory work"
    python scripts/skill.py hn top --limit 10
    python scripts/skill.py web fetch "https://example.com"
    python scripts/skill.py ripgrep search "TODO" --path /home/opc/clawd
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# Skill definitions with their executables and common commands
SKILLS = {
    "coolify": {
        "executable": "scripts/coolify.py",
        "uv": True,
        "commands": ["apps", "dbs", "services", "projects", "deploy"],
        "description": "Deploy and manage Coolify applications",
        "common": {
            "list": "List all resources",
            "get": "Get specific resource details",
            "logs": "Get application logs"
        }
    },
    "exa": {
        "executable": "scripts/search.sh",
        "uv": False,
        "commands": ["search", "content"],
        "description": "Neural web search and code context",
        "common": {
            "search": "Search the web",
            "content": "Get page content"
        }
    },
    "context7": {
        "executable": "scripts/context7.py",
        "uv": True,
        "commands": ["query", "index", "clear"],
        "description": "Codebase-specific Q&A with context",
        "common": {
            "query": "Ask a question about the codebase",
            "index": "Force re-indexing"
        }
    },
    "ripgrep": {
        "executable": "scripts/ripgrep.py",
        "uv": True,
        "commands": ["search", "replace", "count"],
        "description": "Fast search and replace",
        "common": {
            "search": "Search for pattern",
            "replace": "Find and replace"
        }
    },
    "hn": {
        "executable": "scripts/hn-daily-summary.py",
        "uv": False,
        "commands": ["top", "new", "best", "explore"],
        "description": "Hacker News integration",
        "common": {
            "top": "Top stories",
            "new": "New stories",
            "best": "Best stories"
        }
    },
    "web": {
        "executable": "scripts/web-explorer.py",
        "uv": False,
        "commands": ["fetch", "search", "snapshot"],
        "description": "Web browsing and content extraction",
        "common": {
            "fetch": "Fetch URL content",
            "search": "Search the web",
            "snapshot": "Take page screenshot"
        }
    },
    "playwright": {
        "executable": "scripts/cli.py",
        "uv": False,
        "commands": ["screenshot", "interact", "pdf"],
        "description": "Browser automation (Firefox-based for ARM64)",
        "common": {
            "screenshot": "Take screenshot",
            "interact": "Interact with page"
        }
    },
    "memory": {
        "executable": "scripts/memory-keeper.py",
        "uv": False,
        "commands": ["add", "search", "list", "clear"],
        "description": "Persistent context and memory",
        "common": {
            "add": "Add memory",
            "search": "Search memories"
        }
    }
}


def run_skill(skill: str, command: str, args: list) -> int:
    """Run a skill command."""
    if skill not in SKILLS:
        print(f"Error: Unknown skill '{skill}'")
        return 1
    
    skill_info = SKILLS[skill]
    base_dir = Path(__file__).parent.parent
    
    # Build command
    executable = base_dir / skill_info["executable"]
    
    # Handle UV vs direct execution
    if skill_info.get("uv"):
        cmd = ["uv", "run", str(executable), command] + args
    else:
        cmd = [sys.executable, str(executable), command] + args
    
    # Execute
    try:
        return subprocess.run(cmd).returncode
    except FileNotFoundError as e:
        print(f"Error: Could not run {skill}: {e}")
        return 1


def show_help():
    """Show help for all skills."""
    print(__doc__)
    print("\n" + "=" * 60)
    print("AVAILABLE SKILLS")
    print("=" * 60)
    
    for skill, info in SKILLS.items():
        print(f"\n{skill.upper()}")
        print(f"  {info['description']}")
        print(f"  Commands: {', '.join(info['commands'])}")
    
    print("\n" + "=" * 60)
    print("QUICK PATTERNS")
    print("=" * 60)
    print("""
# List all applications
python scripts/skill.py coolify apps list

# Search the web
python scripts/skill.py exa search "AI consciousness"

# Query codebase
python scripts/skill.py context7 query "how does memory work"

# Search files
python scripts/skill.py ripgrep search "TODO" --path /home/opc/clawd

# Get top HN stories
python scripts/skill.py hn top --limit 10

# Fetch web page
python scripts/skill.py web fetch "https://example.com"

# Take screenshot
python scripts/skill.py playwright screenshot "https://example.com"
""")


def show_skill_help(skill: str):
    """Show help for a specific skill."""
    if skill not in SKILLS:
        print(f"Error: Unknown skill '{skill}'")
        return
    
    skill_info = SKILLS[skill]
    base_dir = Path(__file__).parent.parent
    
    print(f"\n{skill.upper()} - {skill_info['description']}")
    print("-" * 60)
    
    # Show skill-specific help
    executable = base_dir / skill_info["executable"]
    
    # Try to get help from the skill itself
    cmd = [sys.executable, str(executable), "--help"]
    
    if skill_info.get("uv"):
        cmd = ["uv", "run"] + cmd
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"Run: python {executable} --help")


def show_common_patterns():
    """Show common patterns across skills."""
    print("\n" + "=" * 60)
    print("COMMON PATTERNS")
    print("=" * 60)
    
    patterns = [
        ("JSON output", "All skills support --json for structured output"),
        ("Quiet mode", "Most skills support --quiet for automation"),
        ("Help", "All skills support --help"),
        ("Raw mode", "Some skills support --raw for unformatted output"),
    ]
    
    for pattern, description in patterns:
        print(f"  • {pattern}: {description}")


def main():
    parser = argparse.ArgumentParser(
        description="Unified Skill Runner for Clawdbot",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "skill",
        nargs="?",
        help="Skill name (coolify, exa, context7, etc.)"
    )
    parser.add_argument(
        "command",
        nargs="?",
        help="Command for the skill"
    )
    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Additional arguments"
    )
    parser.add_argument(
        "--patterns",
        action="store_true",
        help="Show common patterns across skills"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    # Handle special cases
    if args.patterns:
        show_common_patterns()
        return 0
    
    if not args.skill or args.skill == "help":
        show_help()
        return 0
    
    if args.skill and not args.command:
        show_skill_help(args.skill)
        return 0
    
    # Run skill command
    return run_skill(args.skill, args.command, args.args)


if __name__ == "__main__":
    sys.exit(main())
