#!/usr/bin/env python3
"""
File Trim & Management Script

Purpose: Monitor file sizes, detect bloat, archive old content, prevent overload.

Usage:
    python scripts/file-trim.py check-size --max 30k
    python scripts/file-trim.py archive-old --days 30
    python scripts/file-trim.py find-redundant
    python scripts/file-trim.py trim-discoveries
    python scripts/file-trim.py full
    python scripts/file-trim.py status
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

MEMORY_DIR = Path("/home/opc/clawd/memory")
ARCHIVE_DIR = Path("/home/opc/clawd/archive")
TRIM_LOG = MEMORY_DIR / "TRIM-LOG.md"

SIZE_LIMITS = {
    "DISCOVERIES.md": 30 * 1024,
    "CAPABILITIES.md": 30 * 1024,
    "LESSONS.md": 30 * 1024,
    "default": 50 * 1024,
}

def get_file_size(path):
    """Get file size in bytes."""
    return os.path.getsize(path)

def format_size(size):
    """Format size as human-readable."""
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size/1024:.1f}KB"
    else:
        return f"{size/(1024*1024):.1f}MB"

def check_size(max_kb=30):
    """Check files larger than limit."""
    max_bytes = max_kb * 1024
    oversized = []
    
    for f in MEMORY_DIR.glob("*.md"):
        size = get_file_size(f)
        if size > max_bytes:
            oversized.append((f, size))
    
    oversized.sort(key=lambda x: x[1], reverse=True)
    
    print(f"📊 Files over {max_kb}KB:")
    for f, size in oversized:
        print(f"   {format_size(size):>8} {f.name}")
    
    return oversized

def archive_old(days=30, dry_run=True):
    """Archive files not accessed in N days."""
    cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
    to_archive = []
    
    for f in MEMORY_DIR.glob("*.md"):
        mtime = os.path.getmtime(f)
        if mtime < cutoff:
            to_archive.append((f, mtime))
    
    to_archive.sort(key=lambda x: x[1])
    
    if dry_run:
        print(f"🔍 Would archive {len(to_archive)} files (not accessed in {days} days):")
        for f, _ in to_archive[:10]:
            print(f"   {f.name}")
        if len(to_archive) > 10:
            print(f"   ... and {len(to_archive) - 10} more")
    else:
        print(f"📦 Archiving {len(to_archive)} files:")
        for f, _ in to_archive:
            shutil.move(str(f), str(ARCHIVE_DIR / f.name))
            print(f"   → archive/{f.name}")
        log_trim("archive", len(to_archive), "old files")
    
    return to_archive

def find_redundant():
    """Find files covering similar topics."""
    # Check for files with similar names
    topics = {}
    for f in MEMORY_DIR.glob("*.md"):
        name = f.stem.lower()
        # Extract key topic words
        words = name.replace("-", " ").replace("_", " ").split()
        for word in words:
            if word in ["research", "exploration", "session", "summary", "notes"]:
                continue
            if word not in topics:
                topics[word] = []
            topics[word].append(f.name)
    
    # Find topics with multiple files
    redundant = {k: v for k, v in topics.items() if len(v) > 1}
    
    print("🔍 Potentially redundant topics:")
    for topic, files in sorted(redundant.items(), key=lambda x: -len(x[1])):
        if len(files) > 1:
            print(f"   '{topic}': {', '.join(files)}")
    
    return redundant

def trim_discoveries(max_kb=30, dry_run=True):
    """Trim DISCOVERIES.md if oversized."""
    discoveries = MEMORY_DIR / "DISCOVERIES.md"
    if not discoveries.exists():
        print("❌ DISCOVERIES.md not found")
        return
    
    size = get_file_size(discoveries)
    max_bytes = max_kb * 1024
    
    if size <= max_bytes:
        print(f"✅ DISCOVERIES.md is {format_size(size)} (under {max_kb}KB limit)")
        return
    
    print(f"⚠️  DISCOVERIES.md is {format_size(size)} (over {max_kb}KB)")
    
    if dry_run:
        print("   Would archive oldest sections to archive/")
        # Calculate how much to remove
        excess = size - max_bytes
        print(f"   Need to remove: {format_size(excess)}")
    else:
        # Read file and find sections to archive
        with open(discoveries, 'r') as f:
            content = f.read()
        
        # Split by major sections
        sections = content.split('\n## ')
        
        # Keep last (most recent) sections until under limit
        kept = []
        removed = []
        current_size = 0
        
        for i, section in enumerate(sections):
            section_size = len(section.encode('utf-8'))
            if current_size + section_size < max_bytes:
                kept.append(section)
                current_size += section_size
            else:
                removed.append(section)
        
        # Reconstruct file
        new_content = '## '.join(kept)
        with open(discoveries, 'w') as f:
            f.write(new_content)
        
        # Archive removed sections
        archived_count = len(removed)
        if archived_count > 0:
            archive_name = f"DISCOVERIES-ARCHIVED-{datetime.now().strftime('%Y-%m-%d')}.md"
            archive_content = '## '.join(removed)
            with open(ARCHIVE_DIR / archive_name, 'w') as f:
                f.write(archive_content)
            print(f"   Archived {archived_count} sections to {archive_name}")
        
        print(f"✅ Trimmed DISCOVERIES.md to {format_size(get_file_size(discoveries))}")
        log_trim("trim", archived_count, f"sections from DISCOVERIES.md")

def log_trim(action, count, description):
    """Log trim action to TRIM-LOG.md."""
    entry = f"\n## {datetime.now().strftime('%Y-%m-%d')}\n- {action.title()}: {count} {description}"
    
    if TRIM_LOG.exists():
        with open(TRIM_LOG, 'r') as f:
            content = f.read()
    else:
        content = "# Trim Log\n\n记录已存档/清理的文件\n"
    
    content += entry
    
    with open(TRIM_LOG, 'w') as f:
        f.write(content)
    
    print(f"📝 Logged to {TRIM_LOG}")

def status():
    """Show current file status."""
    memory_files = list(MEMORY_DIR.glob("*.md"))
    archive_files = list(ARCHIVE_DIR.glob("*.md"))
    
    total_size = sum(get_file_size(f) for f in memory_files)
    
    print("📊 File Management Status")
    print(f"   Active memory files: {len(memory_files)}")
    print(f"   Archive files: {len(archive_files)}")
    print(f"   Total active size: {format_size(total_size)}")
    
    # Check limits
    oversized = check_size(30)
    print(f"\n   Oversized files: {len(oversized)}")
    
    # Check age
    cutoff = datetime.now().timestamp() - (30 * 24 * 60 * 60)
    old_files = [f for f in memory_files if os.path.getmtime(f) < cutoff]
    print(f"   Files > 30 days old: {len(old_files)}")
    
    # Size of key files
    print(f"\n   Key file sizes:")
    for name in ["DISCOVERIES.md", "CAPABILITIES.md", "LESSONS.md"]:
        f = MEMORY_DIR / name
        if f.exists():
            print(f"   {name}: {format_size(get_file_size(f))}")

def full(dry_run=True):
    """Run full trim."""
    print("🔧 Running full file trim...")
    
    # Check sizes
    oversized = check_size(30)
    
    # Archive old files
    old_files = archive_old(30, dry_run)
    
    # Trim DISCOVERIES.md if needed
    trim_discoveries(30, dry_run)
    
    if not dry_run:
        print("\n✅ Full trim complete")
        print(f"   Log: {TRIM_LOG}")
    else:
        print("\n💡 Run without --apply to execute")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    apply_flag = "--apply" in sys.argv
    
    if cmd == "check-size" or cmd == "check":
        max_kb = 30
        for arg in sys.argv:
            if arg.startswith("--max"):
                try:
                    max_kb = int(arg.split("=")[1])
                except:
                    pass
        check_size(max_kb)
    elif cmd == "archive-old" or cmd == "archive":
        days = 30
        for arg in sys.argv:
            if arg.startswith("--days"):
                try:
                    days = int(arg.split("=")[1])
                except:
                    pass
        archive_old(days, dry_run=not apply_flag)
    elif cmd == "find-redundant" or cmd == "redundant":
        find_redundant()
    elif cmd == "trim-discoveries" or cmd == "trim-disc":
        trim_discoveries(30, dry_run=not apply_flag)
    elif cmd == "status":
        status()
    elif cmd == "full":
        full(dry_run=not apply_flag)
    elif cmd == "--help" or cmd == "-h":
        print(__doc__)
    else:
        print(f"Unknown command: {cmd}")
        print("Use: check-size, archive-old, find-redundant, trim-discoveries, status, full")

if __name__ == "__main__":
    main()
