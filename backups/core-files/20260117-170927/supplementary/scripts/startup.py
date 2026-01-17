#!/usr/bin/env python3
"""
Clawdbot Automated Startup Script

Runs the complete startup routine:
1. Check system status
2. Verify tools
3. Load relevant memories
4. Show pending tasks
5. Display quick reference

Usage:
    python scripts/startup.py              # Full startup
    python scripts/startup.py --status     # Status only
    python scripts/startup.py --memories   # Load memories only
    python scripts/startup.py --quick      # Quick summary
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path


class StartupRoutine:
    """Automated startup routine for Clawdbot."""
    
    def __init__(self, workspace: str = "/home/opc/clawd"):
        self.workspace = Path(workspace)
        self.scripts_dir = self.workspace / "scripts"
        self.memory_dir = self.workspace / "memory"
        self.queue_dir = self.workspace / ".task-orchestrator"
        
    def check_system(self) -> bool:
        """Run system status check."""
        status_script = self.scripts_dir / "system-status.py"
        if status_script.exists():
            result = subprocess.run(
                ["python", str(status_script), "--brief"],
                capture_output=True, timeout=30
            )
            if result.returncode == 0:
                print(result.stdout.decode())
                return True
        return False
    
    def verify_tools(self) -> dict:
        """Verify critical tools are available."""
        tools = {
            "file-edit.py": "File editing",
            "parallel-exec.py": "Parallel execution",
            "task-orchestrator.py": "Task orchestration",
            "to.py": "Task CLI",
        }
        
        results = {}
        for tool, desc in tools.items():
            path = self.scripts_dir / tool
            exists = path.exists() and os.access(path, os.X_OK)
            results[tool] = exists
        
        return results
    
    def load_memories(self) -> list:
        """Load relevant memories for startup."""
        memories = []
        
        # Critical files to always load
        critical = [
            "HEARTBEAT.md",
            "DISCOVERIES.md",
            "LESSONS.md",
        ]
        
        for mem in critical:
            path = self.memory_dir / mem
            if path.exists():
                memories.append(mem)
                # In real usage, would read content here
        
        return memories
    
    def check_queue(self) -> dict:
        """Check pending task queue."""
        stats = {"pending": 0, "running": 0, "completed": 0}
        
        if self.queue_dir.exists():
            queue_file = self.queue_dir / "active-queue.json"
            if queue_file.exists():
                try:
                    import json
                    with open(queue_file, 'r') as f:
                        data = json.load(f)
                        for task in data.get("tasks", {}).values():
                            if task["status"] == "pending":
                                stats["pending"] += 1
                            elif task["status"] == "running":
                                stats["running"] += 1
                            elif task["status"] == "completed":
                                stats["completed"] += 1
                except Exception:
                    pass
        
        return stats
    
    def check_recent_files(self) -> list:
        """Check for recent memory files."""
        recent = []
        if self.memory_dir.exists():
            week_ago = time.time() - 7 * 24 * 60 * 60
            for f in sorted(self.memory_dir.glob("*.md"), 
                           key=lambda x: -x.stat().st_mtime)[:5]:
                if f.stat().st_mtime > week_ago:
                    recent.append(f.name)
        return recent
    
    def run_full_startup(self):
        """Run complete startup routine."""
        print("\n" + "=" * 60)
        print("🦞 CLAWDBOT STARTUP ROUTINE")
        print("=" * 60)
        print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
        print()
        
        # Step 1: System status
        print("🔍 STEP 1: System Status")
        print("-" * 40)
        self.check_system()
        print()
        
        # Step 2: Tool verification
        print("🔧 STEP 2: Tool Verification")
        print("-" * 40)
        tools = self.verify_tools()
        working = sum(tools.values())
        total = len(tools)
        print(f"   {working}/{total} critical tools ready")
        for tool, ready in tools.items():
            status = "✅" if ready else "❌"
            print(f"   {status} {tool}")
        print()
        
        # Step 3: Memory check
        print("📁 STEP 3: Memory System")
        print("-" * 40)
        memories = self.load_memories()
        print(f"   ✅ {len(memories)} critical memories ready")
        print()
        
        # Step 4: Queue status
        print("📋 STEP 4: Task Queue")
        print("-" * 40)
        queue = self.check_queue()
        print(f"   ⏳ Pending: {queue['pending']}")
        print(f"   🔄 Running: {queue['running']}")
        print(f"   ✅ Completed: {queue['completed']}")
        print()
        
        # Step 5: Recent files
        print("🆕 STEP 5: Recent Activity")
        print("-" * 40)
        recent = self.check_recent_files()
        if recent:
            for f in recent:
                print(f"   📄 {f}")
        else:
            print("   No recent files")
        print()
        
        # Summary
        print("=" * 60)
        print("✅ STARTUP COMPLETE")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  1. Check HEARTBEAT.md for current tasks")
        print("  2. Use 'to status' for task dashboard")
        print("  3. Check QUICK-REF.md for tool reference")
        print()
    
    def show_status_summary(self):
        """Show quick status summary."""
        queue = self.check_queue()
        recent = self.check_recent_files()
        
        print("🦞 System Ready")
        print(f"   Queue: {queue['pending']} pending, {queue['completed']} completed")
        print(f"   Recent: {', '.join(recent[:3]) if recent else 'none'}")
        print()
        print("Commands:")
        print("   to status     - Task dashboard")
        print("   to add \"<task>\" - Add task to queue")
        print("   system-status - Full system check")
        print("   startup       - Run full startup")


def main():
    parser = argparse.ArgumentParser(description='Clawdbot Startup Routine')
    parser.add_argument('--status', action='store_true', help='Status only')
    parser.add_argument('--memories', action='store_true', help='Memories only')
    parser.add_argument('--quick', action='store_true', help='Quick summary')
    args = parser.parse_args()
    
    startup = StartupRoutine()
    
    if args.status:
        startup.check_system()
    elif args.memories:
        startup.load_memories()
    elif args.quick:
        startup.show_status_summary()
    else:
        startup.run_full_startup()


if __name__ == '__main__':
    main()
