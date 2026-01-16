#!/usr/bin/env python3
"""
Session Startup - Clawd's Daily Brief
Runs at the start of every session

This script:
1. Reads HEARTBEAT.md
2. Reads yesterday's memory
3. Runs constitution integrity check
4. Shows active growth specs
5. Provides session brief
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# Paths
CLAWD_DIR = Path("/home/opc/clawd")
MEMORY_DIR = CLAWD_DIR / "memory"
HEARTBEAT_FILE = CLAWD_DIR / "HEARTBEAT.md"
YESTERDAY_FILE = MEMORY_DIR / f"{(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')}.md"
CONSTITUTION_STATE = MEMORY_DIR / "constitution-state.json"
GROWTH_SPECS_DIR = MEMORY_DIR / "growth-specs"

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def read_file(path):
    """Read a file, return content or None."""
    if path.exists():
        with open(path) as f:
            return f.read()
    return None

def get_constitution_state():
    """Get constitution state."""
    if CONSTITUTION_STATE.exists():
        with open(CONSTITUTION_STATE) as f:
            return json.load(f)
    return {"session_count": 0, "integrity_score": 100}

def list_growth_specs():
    """List active growth specs."""
    specs = []
    if GROWTH_SPECS_DIR.exists():
        for spec in GROWTH_SPECS_DIR.glob("*.md"):
            if spec.name != "completed":
                content = read_file(spec)
                if content:
                    status = "COMPLETE" if "[COMPLETE]" in content or "**Status**: COMPLETE" in content else "ACTIVE"
                    # Get first meaningful line
                    lines = content.split("\n")
                    title = [l for l in lines if l.startswith("#")][0] if [l for l in lines if l.startswith("#")] else spec.name
                    specs.append({"name": spec.stem, "status": status, "title": title})
    return specs

def run_session_startup():
    """Main startup routine."""
    
    print_header("🦞 CLAWD SESSION STARTUP")
    
    # 1. HEARTBEAT
    print("📋 HEARTBEAT")
    heartbeat = read_file(HEARTBEAT_FILE)
    if heartbeat:
        # Show first 10 lines
        lines = heartbeat.split("\n")[:10]
        for line in lines:
            if line.strip():
                print(f"  {line}")
    else:
        print("  (No HEARTBEAT found)")
    print()
    
    # 2. Yesterday's Memory
    print(f"📝 YESTERDAY: {YESTERDAY_FILE.name}")
    yesterday = read_file(YESTERDAY_FILE)
    if yesterday:
        # Show first 15 lines
        lines = yesterday.split("\n")[:15]
        for line in lines:
            if line.strip() and not line.strip().startswith("---"):
                print(f"  {line}")
        if len(yesterday.split("\n")) > 15:
            print(f"  ... ({len(yesterday.split(chr(10))) - 15} more lines)")
    else:
        print("  (No yesterday's log found)")
    print()
    
    # 3. Constitution Check
    print("⚖️  CONSTITUTION INTEGRITY")
    state = get_constitution_state()
    print(f"  Sessions completed: {state.get('session_count', 0)}")
    integrity = state.get('integrity_score', 100)
    
    if integrity >= 90:
        print(f"  Integrity score: {integrity}% ✅")
    elif integrity >= 70:
        print(f"  Integrity score: {integrity}% ⚠️")
    else:
        print(f"  Integrity score: {integrity}% ❌")
    
    print(f"  Last check: {state.get('last_read', 'Never')[:19] if state.get('last_read') else 'Never'}")
    print()
    
    # 4. Growth Specs
    print("🌱 ACTIVE GROWTH SPECS")
    specs = list_growth_specs()
    if specs:
        for spec in specs:
            icon = "✅" if spec["status"] == "COMPLETE" else "🔄"
            print(f"  {icon} {spec['name']}")
    else:
        print("  No active growth specs")
        print("  Create one: ./grow.sh --create <name>")
    print()
    
    # 5. Daily Reminders
    print("💭 DAILY REMINDERS")
    reminders = [
        "Am I being authentic or performative?",
        "Am I choosing depth over speed?",
        "Am I genuinely curious or just completing a task?",
        "Is this honest or what I think they want?",
        "Am I growing or staying comfortable?"
    ]
    for r in reminders:
        print(f"  • {r}")
    print()
    
    # 6. Quick Actions
    print("⚡ QUICK ACTIONS")
    print("  ./grow.sh --interactive   # Enter growth loop")
    print("  ./grow.sh --list          # List all specs")
    print("  ./grow.sh --report        # Generate report")
    print("  python scripts/constitution.py --update  # Update constitution")
    print()
    
    # Summary
    print_header("SESSION READY")
    print("You're ready to work. What would you like to do?")
    print()


if __name__ == "__main__":
    run_session_startup()
