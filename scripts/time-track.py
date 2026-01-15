#!/usr/bin/env python3
"""
Time Tracking Utility for Clawd

Purpose: Measure actual time spent on tasks, compare to estimates, track accuracy.

Usage:
    python scripts/time-track.py start <task-name>          # Start timer
    python scripts/time-track.py check <task-name>          # Check elapsed
    python scripts/time-track.py end <task-name>            # End and record
    python scripts/time-track.py record <task> <est> <act>  # Log manually
    python scripts/time-track.py report                      # Show accuracy
    python scripts/time-track.py history                     # Show all records
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

TRACKING_DIR = "/home/opc/clawd/.time-tracking"
HISTORY_FILE = f"{TRACKING_DIR}/history.json"
ACTIVE_FILE = f"{TRACKING_DIR}/active.json"

def ensure_tracking_dir():
    """Create tracking directory if needed."""
    Path(TRACKING_DIR).mkdir(parents=True, exist_ok=True)

def load_history():
    """Load time tracking history."""
    ensure_tracking_dir()
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {"records": []}

def save_history(history):
    """Save time tracking history."""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def load_active():
    """Load active timers."""
    ensure_tracking_dir()
    if os.path.exists(ACTIVE_FILE):
        with open(ACTIVE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_active(active):
    """Save active timers."""
    with open(ACTIVE_FILE, 'w') as f:
        json.dump(active, f, indent=2)

def format_duration(seconds):
    """Format seconds as human-readable duration."""
    if seconds < 60:
        return f"{seconds} sec"
    elif seconds < 3600:
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins} min {secs} sec"
    else:
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        return f"{hours} hr {mins} min"

def cmd_start(task_name):
    """Start a timer for a task."""
    active = load_active()
    if task_name in active:
        print(f"⚠️  Timer already running for '{task_name}'")
        print(f"   Started: {active[task_name]['start_time']}")
        return
    
    active[task_name] = {
        "start_time": datetime.now().isoformat(),
        "start_timestamp": datetime.now().timestamp()
    }
    save_active(active)
    print(f"✅ Started timer for '{task_name}'")

def cmd_check(task_name, expected_minutes=None):
    """Check elapsed time for a task."""
    active = load_active()
    if task_name not in active:
        print(f"❌ No active timer for '{task_name}'")
        return
    
    start_ts = active[task_name]['start_timestamp']
    elapsed = datetime.now().timestamp() - start_ts
    elapsed_formatted = format_duration(int(elapsed))
    
    if expected_minutes:
        expected_sec = expected_minutes * 60
        remaining = expected_sec - elapsed
        if remaining > 0:
            print(f"⏱️  '{task_name}': {elapsed_formatted} elapsed")
            print(f"   Expected: {expected_minutes} min | Remaining: {format_duration(int(remaining))}")
        else:
            overtime = abs(remaining)
            print(f"⚠️  '{task_name}': {elapsed_formatted} (OVERTIME: {format_duration(int(overtime))})")
    else:
        print(f"⏱️  '{task_name}': {elapsed_formatted}")

def cmd_end(task_name, estimated_minutes=None):
    """End timer and record duration."""
    active = load_active()
    if task_name not in active:
        print(f"❌ No active timer for '{task_name}'")
        return
    
    start_ts = active[task_name]['start_timestamp']
    elapsed = datetime.now().timestamp() - start_ts
    elapsed_formatted = format_duration(int(elapsed))
    
    # Remove from active
    del active[task_name]
    save_active(active)
    
    # Calculate accuracy if estimate provided
    if estimated_minutes:
        expected_sec = estimated_minutes * 60
        diff = elapsed - expected_sec
        diff_pct = (diff / expected_sec) * 100
        if abs(diff_pct) < 10:
            accuracy = "🎯 Excellent"
        elif abs(diff_pct) < 25:
            accuracy = "✅ Good"
        elif abs(diff_pct) < 50:
            accuracy = "⚠️ Fair"
        else:
            accuracy = "❌ Poor"
        
        print(f"✅ '{task_name}': {elapsed_formatted}")
        print(f"   Expected: {estimated_minutes} min | {accuracy} ({abs(diff_pct):.1f}% {'over' if diff > 0 else 'under'})")
    else:
        print(f"✅ '{task_name}': {elapsed_formatted}")
    
    # Record for history
    history = load_history()
    history["records"].append({
        "task": task_name,
        "estimated_minutes": estimated_minutes,
        "actual_seconds": int(elapsed),
        "timestamp": datetime.now().isoformat()
    })
    save_history(history)

def cmd_record(task_name, estimated_minutes, actual_minutes):
    """Manually record a time entry."""
    history = load_history()
    history["records"].append({
        "task": task_name,
        "estimated_minutes": estimated_minutes,
        "actual_seconds": actual_minutes * 60,
        "timestamp": datetime.now().isoformat()
    })
    save_history(history)
    print(f"✅ Recorded: {task_name} - Est: {estimated_minutes} min, Actual: {actual_minutes} min")

def cmd_report():
    """Show accuracy report."""
    history = load_history()
    records = history.get("records", [])
    
    if not records:
        print("📊 No time tracking records yet.")
        print("   Use 'time-track.py start <task>' to begin tracking.")
        return
    
    # Calculate statistics
    total = len(records)
    with_estimates = [r for r in records if r.get("estimated_minutes")]
    
    if with_estimates:
        ratios = []
        for r in with_estimates:
            expected = r["estimated_minutes"] * 60
            actual = r["actual_seconds"]
            ratios.append(actual / expected)
        
        avg_ratio = sum(ratios) / len(ratios)
        within_20 = sum(1 for r in ratios if 0.8 <= r <= 1.2)
        within_50 = sum(1 for r in ratios if 0.5 <= r <= 1.5)
        
        print(f"📊 Time Tracking Report")
        print(f"   Total records: {total}")
        print(f"   With estimates: {len(with_estimates)}")
        print(f"   Average ratio: {avg_ratio:.2f} ({avg_ratio*100:.0f}% of expected)")
        print(f"   Within 20%: {within_20}/{len(with_estimates)} ({100*within_20/len(with_estimates):.0f}%)")
        print(f"   Within 50%: {within_50}/{len(with_estimates)} ({100*within_50/len(with_estimates):.0f}%)")
    
    # Show recent
    print(f"\n📝 Recent Records (last 5):")
    for r in records[-5:]:
        est = r.get("estimated_minutes", "?")
        act = r["actual_seconds"] / 60
        print(f"   {r['task']}: Est {est} min → Actual {act:.1f} min")

def cmd_history():
    """Show full history."""
    history = load_history()
    records = history.get("records", [])
    
    if not records:
        print("No time tracking records yet.")
        return
    
    print(f"📋 Full History ({len(records)} records):")
    for r in records[-10:]:
        est = r.get("estimated_minutes", "?")
        act = r["actual_seconds"] / 60
        print(f"   {r['timestamp'][:10]}: {r['task']} - Est {est} min → {act:.1f} min")

def cmd_status():
    """Show active timers."""
    active = load_active()
    if not active:
        print("No active timers.")
        return
    
    print(f"⏱️  Active Timers ({len(active)}):")
    for name, data in active.items():
        start_ts = data["start_timestamp"]
        elapsed = datetime.now().timestamp() - start_ts
        print(f"   {name}: {format_duration(int(elapsed))}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "start" and len(sys.argv) >= 3:
        cmd_start(sys.argv[2])
    elif cmd == "check" and len(sys.argv) >= 3:
        est = int(sys.argv[3]) if len(sys.argv) >= 4 else None
        cmd_check(sys.argv[2], est)
    elif cmd == "end" and len(sys.argv) >= 3:
        est = int(sys.argv[3]) if len(sys.argv) >= 4 else None
        cmd_end(sys.argv[2], est)
    elif cmd == "record" and len(sys.argv) >= 5:
        cmd_record(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    elif cmd == "report":
        cmd_report()
    elif cmd == "history":
        cmd_history()
    elif cmd == "status":
        cmd_status()
    elif cmd == "--help" or cmd == "-h":
        print(__doc__)
    else:
        print(f"Unknown command: {cmd}")
        print("Use: start <task>, check <task> [expected_min], end <task> [expected_min], record, report, history, status")

if __name__ == "__main__":
    main()
