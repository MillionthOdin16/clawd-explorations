#!/usr/bin/env python3
"""ripgrep CLI wrapper for Clawdbot."""

import argparse
import subprocess
import json
import sys

def run_rg(args):
    """Run ripgrep and return results."""
    cmd = ["rg"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "status": "success" if result.returncode == 0 else "no_match",
        "returncode": result.returncode,
        "output": result.stdout,
        "error": result.stderr if result.stderr else None
    }

def cmd_search(pattern, path=".", type_filter=None, context=0, hidden=False):
    """Search for pattern."""
    args = [pattern, path]
    if type_filter:
        args.extend(["-t", type_filter])
    if context > 0:
        args.extend(["-A", str(context)])
    if hidden:
        args.append("-u")
    return run_rg(args)

def cmd_files(pattern, path="."):
    """List files matching pattern."""
    return run_rg(["-l", pattern, path])

def cmd_count(pattern, path="."):
    """Count occurrences."""
    result = run_rg(["-c", pattern, path])
    count = result["output"].strip().split("\n")
    total = sum(int(c.split(":")[-1]) for c in count if c and ":" in c)
    return {"count": total, "files": len([c for c in count if c])}

def cmd_find_funcs(path=".", type_filter="py"):
    """Find function definitions."""
    return run_rg([r"^def ", path, "-t", type_filter, "-n"])

def cmd_find_classes(path=".", type_filter="py"):
    """Find class definitions."""
    return run_rg([r"^class ", path, "-t", type_filter, "-n"])

def main():
    parser = argparse.ArgumentParser(description="ripgrep wrapper")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # search
    search_parser = subparsers.add_parser("search", help="Search for pattern")
    search_parser.add_argument("pattern")
    search_parser.add_argument("path", default=".", nargs="?")
    search_parser.add_argument("-t", "--type", help="File type")
    search_parser.add_argument("-A", "--after", type=int, default=0)
    search_parser.add_argument("-B", "--before", type=int, default=0)
    search_parser.add_argument("-u", "--hidden", action="store_true")
    
    # files
    subparsers.add_parser("files", help="List matching files").add_argument("pattern")
    
    # count
    subparsers.add_parser("count", help="Count occurrences").add_argument("pattern")
    
    # find-funcs
    subparsers.add_parser("find-funcs", help="Find function definitions")
    
    # find-classes
    subparsers.add_parser("find-classes", help="Find class definitions")
    
    args = parser.parse_args()
    
    if args.command == "search":
        result = cmd_search(args.pattern, args.path, args.type, args.after, args.hidden)
    elif args.command == "files":
        result = cmd_files(args.pattern, args.path)
    elif args.command == "count":
        result = cmd_count(args.pattern, args.path)
    elif args.command == "find-funcs":
        result = cmd_find_funcs(args.path)
    elif args.command == "find-classes":
        result = cmd_find_classes(args.path)
    else:
        result = {"error": "Unknown command"}
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
