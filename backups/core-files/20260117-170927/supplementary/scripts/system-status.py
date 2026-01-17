#!/usr/bin/env python3
"""
System Status Dashboard for Clawdbot

Shows comprehensive status of all system components:
- Tools health
- Memory usage
- Queue status
- Disk usage
- qmd index status
- Service availability

Usage:
    python scripts/system-status.py          # Full dashboard
    python scripts/system-status.py --brief  # Quick summary
    python scripts/system-status.py --json   # JSON output
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


class SystemStatus:
    """Comprehensive system status checker."""
    
    def __init__(self):
        self.workspace = Path("/home/opc/clawd")
        self.scripts_dir = self.workspace / "scripts"
        self.memory_dir = self.workspace / "memory"
        self.archive_dir = self.workspace / "archive"
        
    def check_tools(self) -> dict:
        """Check health of all scripts/tools."""
        tools = {
            "file-edit.py": "File editing",
            "parallel-exec.py": "Parallel execution",
            "parallel-exec-enhanced.py": "Enhanced parallel",
            "task-orchestrator.py": "Task orchestration",
            "to.py": "Task CLI",
            "search-mcp-servers.py": "MCP search",
        }
        
        results = {}
        for tool, desc in tools.items():
            path = self.scripts_dir / tool
            exists = path.exists()
            executable = os.access(path, os.X_OK) if exists else False
            
            # Try a quick test
            test_ok = False
            if exists and executable:
                try:
                    if "task" in tool and "orchestrator" not in tool:
                        continue  # Skip complex tools
                    result = subprocess.run(
                        ["python", str(path), "--help"],
                        capture_output=True, timeout=5
                    )
                    test_ok = result.returncode in [0, 2]  # Help returns 0 or 2
                except Exception:
                    pass
            
            results[tool] = {
                "description": desc,
                "exists": exists,
                "executable": executable,
                "test_ok": test_ok,
                "status": "✅" if exists and test_ok else "⚠️" if exists else "❌"
            }
        
        return results
    
    def check_memory(self) -> dict:
        """Check memory system health."""
        stats = {
            "memory_files": 0,
            "archive_files": 0,
            "total_size_mb": 0,
            "recent_files": [],
        }
        
        # Count memory files
        if self.memory_dir.exists():
            stats["memory_files"] = len(list(self.memory_dir.glob("*.md")))
            
            # Recent files (last 7 days)
            week_ago = time.time() - 7 * 24 * 60 * 60
            for f in sorted(self.memory_dir.glob("*.md"), key=lambda x: -x.stat().st_mtime):
                if f.stat().st_mtime > week_ago:
                    stats["recent_files"].append(f.name)
        
        # Count archive files
        if self.archive_dir.exists():
            stats["archive_files"] = len(list(self.archive_dir.glob("*.md")))
        
        # Total size
        for p in [self.memory_dir, self.archive_dir]:
            if p.exists():
                stats["total_size_mb"] += sum(f.stat().st_size for f in p.rglob("*.md"))
        stats["total_size_mb"] = round(stats["total_size_mb"] / 1024 / 1024, 2)
        
        return stats
    
    def check_queue(self) -> dict:
        """Check task queue status."""
        queue_dir = self.workspace / ".task-orchestrator"
        stats = {
            "exists": queue_dir.exists(),
            "pending": 0,
            "running": 0,
            "completed": 0,
        }
        
        if queue_dir.exists():
            queue_file = queue_dir / "active-queue.json"
            if queue_file.exists():
                try:
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
    
    def check_qmd(self) -> dict:
        """Check qmd index status."""
        stats = {
            "available": False,
            "indexed_files": 0,
            "collections": [],
        }
        
        try:
            result = subprocess.run(
                ["which", "qmd"],
                capture_output=True, timeout=5
            )
            stats["available"] = result.returncode == 0
        except Exception:
            pass
        
        # Check for index files
        index_dir = self.workspace / ".qmd"
        if index_dir.exists():
            stats["indexed_files"] = len(list(index_dir.rglob("*")))
        
        return stats
    
    def check_disk(self) -> dict:
        """Check disk usage."""
        stats = {
            "workspace_gb": 0,
            "memory_mb": 0,
            "available_gb": 0,
        }
        
        try:
            result = subprocess.run(
                ["df", "-h", str(self.workspace)],
                capture_output=True, timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.decode().strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    stats["available_gb"] = parts[3] if len(parts) > 3 else "?"
        except Exception:
            pass
        
        # Memory directory size
        if self.memory_dir.exists():
            total = sum(f.stat().st_size for f in self.memory_dir.rglob("*"))
            stats["memory_mb"] = round(total / 1024 / 1024, 2)
        
        return stats
    
    def check_services(self) -> dict:
        """Check service availability."""
        services = {
            "git": {"cmd": ["git", "--version"], "name": "Git"},
            "python": {"cmd": ["python", "--version"], "name": "Python"},
            "node": {"cmd": ["node", "--version"], "name": "Node.js"},
            "docker": {"cmd": ["docker", "--version"], "name": "Docker"},
        }
        
        results = {}
        for name, info in services.items():
            try:
                result = subprocess.run(
                    info["cmd"],
                    capture_output=True, timeout=5
                )
                available = result.returncode == 0
                version = result.stdout.decode().strip()[:30] if available else None
                results[name] = {
                    "available": available,
                    "version": version,
                    "status": "✅" if available else "❌"
                }
            except Exception:
                results[name] = {
                    "available": False,
                    "version": None,
                    "status": "❌"
                }
        
        return results
    
    def get_full_status(self) -> dict:
        """Get complete system status."""
        return {
            "timestamp": time.time(),
            "tools": self.check_tools(),
            "memory": self.check_memory(),
            "queue": self.check_queue(),
            "qmd": self.check_qmd(),
            "disk": self.check_disk(),
            "services": self.check_services(),
        }


def print_dashboard(status: SystemStatus):
    """Print formatted dashboard."""
    tools = status.check_tools()
    memory = status.check_memory()
    queue = status.check_queue()
    qmd = status.check_qmd()
    disk = status.check_disk()
    services = status.check_services()
    
    print("\n" + "=" * 60)
    print("🦞 CLAWDBOT SYSTEM STATUS")
    print("=" * 60)
    print(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print()
    
    # Tools section
    print("🔧 TOOLS")
    print("-" * 40)
    tool_count = sum(1 for t in tools.values() if t["status"] == "✅")
    print(f"   {tool_count}/{len(tools)} tools working correctly")
    for name, info in tools.items():
        print(f"   {info['status']} {name}")
    print()
    
    # Memory section
    print("📁 MEMORY SYSTEM")
    print("-" * 40)
    print(f"   📄 Memory files: {memory['memory_files']}")
    print(f"   🗃️  Archive files: {memory['archive_files']}")
    print(f"   💾 Total size: {memory['total_size_mb']} MB")
    if memory['recent_files']:
        print(f"   🆕 Recent: {', '.join(memory['recent_files'][:5])}")
    print()
    
    # Queue section
    print("📋 TASK QUEUE")
    print("-" * 40)
    print(f"   ⏳ Pending: {queue['pending']}")
    print(f"   🔄 Running: {queue['running']}")
    print(f"   ✅ Completed: {queue['completed']}")
    print()
    
    # qmd section
    print("🔍 QMD SEARCH")
    print("-" * 40)
    print(f"   {'✅' if qmd['available'] else '❌'} qmd available")
    if qmd.get('indexed_files'):
        print(f"   📊 Indexed files: {qmd['indexed_files']}")
    print()
    
    # Services section
    print("🔌 SERVICES")
    print("-" * 40)
    for name, info in services.items():
        version = f" ({info['version']})" if info['version'] else ""
        service_name = name.capitalize()
        print(f"   {info['status']} {service_name}{version}")
    print()
    
    # Disk section
    print("💿 DISK")
    print("-" * 40)
    print(f"   💾 Memory: {disk['memory_mb']} MB")
    print(f"   📦 Available: {disk['available_gb']}")
    print()
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description='Clawdbot System Status')
    parser.add_argument('--brief', action='store_true', help='Quick summary')
    parser.add_argument('--json', action='store_true', help='JSON output')
    args = parser.parse_args()
    
    status = SystemStatus()
    
    if args.json:
        print(json.dumps(status.get_full_status(), indent=2))
    elif args.brief:
        full = status.get_full_status()
        tools_ok = sum(1 for t in full["tools"].values() if t["status"] == "✅")
        print(f"🦞 System: {tools_ok}/{len(full['tools'])} tools OK | {full['memory']['memory_files']} memory files | Queue: {full['queue']['pending']} pending")
    else:
        print_dashboard(status)


if __name__ == '__main__':
    main()
