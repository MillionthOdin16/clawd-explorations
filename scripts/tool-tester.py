#!/usr/bin/env python3
"""
Tool Tester for Clawdbot

Tests all tools and verifies they work correctly.
Generates report and can fix common issues.

Usage:
    python scripts/tool-tester.py           # Run all tests
    python scripts/tool-tester.py --fix     # Auto-fix issues
    python scripts/tool-tester.py --json    # JSON output
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple


class ToolTester:
    """Tests all Clawdbot tools."""
    
    def __init__(self, workspace: str = "/home/opc/clawd"):
        self.workspace = Path(workspace)
        self.scripts_dir = self.workspace / "scripts"
        self.results: Dict = {}
        
    def get_tools(self) -> Dict[str, dict]:
        """Get list of tools to test."""
        return {
            "file-edit.py": {
                "test": self.test_file_edit,
                "description": "File editing tool"
            },
            "parallel-exec.py": {
                "test": self.test_parallel_exec,
                "description": "Parallel execution"
            },
            "parallel-exec-enhanced.py": {
                "test": self.test_parallel_exec_enhanced,
                "description": "Enhanced parallel execution"
            },
            "task-orchestrator.py": {
                "test": self.test_task_orchestrator,
                "description": "Task orchestration"
            },
            "to.py": {
                "test": self.test_to_cli,
                "description": "Task CLI wrapper"
            },
            "system-status.py": {
                "test": self.test_system_status,
                "description": "System status dashboard"
            },
            "startup.py": {
                "test": self.test_startup,
                "description": "Startup routine"
            },
        }
    
    def test_file_edit(self) -> Tuple[bool, str]:
        """Test file-edit.py."""
        # Test read
        test_file = "/tmp/test-file-edit.txt"
        with open(test_file, 'w') as f:
            f.write("line1\nline2\nline3\nline4\nline5\n")
        
        try:
            result = subprocess.run(
                ["python", str(self.scripts_dir / "file-edit.py"), 
                 "read", test_file, "--start", "1", "--end", "3"],
                capture_output=True, timeout=10
            )
            if result.returncode == 0:
                return True, "File editing works"
            return False, f"Error: {result.stderr.decode()[:100]}"
        except Exception as e:
            return False, str(e)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)
    
    def test_parallel_exec(self) -> Tuple[bool, str]:
        """Test parallel-exec.py."""
        test_file = "/tmp/test-parallel.txt"
        with open(test_file, 'w') as f:
            f.write("echo test1\n echo test2\n")
        
        try:
            result = subprocess.run(
                ["python", str(self.scripts_dir / "parallel-exec.py"), 
                 "exec", test_file, "-w", "2", "-q"],
                capture_output=True, timeout=15
            )
            if result.returncode == 0:
                return True, "Parallel execution works"
            return False, f"Error: {result.stderr.decode()[:100]}"
        except Exception as e:
            return False, str(e)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)
    
    def test_parallel_exec_enhanced(self) -> Tuple[bool, str]:
        """Test parallel-exec-enhanced.py."""
        test_file = "/tmp/test-parallel-enhanced.txt"
        with open(test_file, 'w') as f:
            f.write("echo enhanced1\n")
        
        try:
            result = subprocess.run(
                ["python", str(self.scripts_dir / "parallel-exec-enhanced.py"), 
                 "exec", test_file, "-w", "2", "-q"],
                capture_output=True, timeout=15
            )
            if result.returncode == 0:
                return True, "Enhanced parallel execution works"
            return False, f"Error: {result.stderr.decode()[:100]}"
        except Exception as e:
            return False, str(e)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)
    
    def test_task_orchestrator(self) -> Tuple[bool, str]:
        """Test task-orchestrator.py."""
        try:
            result = subprocess.run(
                ["python", str(self.scripts_dir / "task-orchestrator.py"), "status"],
                capture_output=True, timeout=10
            )
            if "TASK ORCHESTRATOR DASHBOARD" in result.stdout.decode():
                return True, "Task orchestrator works"
            return False, f"Unexpected output"
        except Exception as e:
            return False, str(e)
    
    def test_to_cli(self) -> Tuple[bool, str]:
        """Test to.py CLI."""
        try:
            result = subprocess.run(
                ["python", str(self.scripts_dir / "to.py"), "status"],
                capture_output=True, timeout=10
            )
            if "DASHBOARD" in result.stdout.decode() or result.returncode == 0:
                return True, "TO CLI works"
            return False, f"Unexpected output"
        except Exception as e:
            return False, str(e)
    
    def test_system_status(self) -> Tuple[bool, str]:
        """Test system-status.py."""
        try:
            result = subprocess.run(
                ["python", str(self.scripts_dir / "system-status.py"), "--brief"],
                capture_output=True, timeout=10
            )
            if "System:" in result.stdout.decode():
                return True, "System status works"
            return False, f"Unexpected output"
        except Exception as e:
            return False, str(e)
    
    def test_startup(self) -> Tuple[bool, str]:
        """Test startup.py."""
        try:
            result = subprocess.run(
                ["python", str(self.scripts_dir / "startup.py"), "--quick"],
                capture_output=True, timeout=10
            )
            if "System Ready" in result.stdout.decode():
                return True, "Startup works"
            return False, f"Unexpected output"
        except Exception as e:
            return False, str(e)
    
    def run_tests(self, fix: bool = False) -> Dict:
        """Run all tests."""
        tools = self.get_tools()
        results = {}
        passed = 0
        failed = 0
        
        print("\n" + "=" * 60)
        print("🧪 CLAWDBOT TOOL TESTER")
        print("=" * 60)
        print()
        
        for tool, info in tools.items():
            print(f"Testing {tool}...", end=" ")
            
            # Check if file exists
            path = self.scripts_dir / tool
            if not path.exists():
                print("❌ (file missing)")
                results[tool] = {
                    "passed": False,
                    "error": "File missing",
                    "description": info["description"]
                }
                failed += 1
                continue
            
            # Make executable
            if fix and not os.access(path, os.X_OK):
                os.chmod(path, 0o755)
            
            # Run test
            try:
                passed_test, msg = info["test"]()
                if passed_test:
                    print("✅")
                    results[tool] = {"passed": True, "message": msg, "description": info["description"]}
                    passed += 1
                else:
                    print("❌")
                    results[tool] = {"passed": False, "error": msg, "description": info["description"]}
                    failed += 1
            except Exception as e:
                print("❌")
                results[tool] = {"passed": False, "error": str(e), "description": info["description"]}
                failed += 1
        
        # Summary
        print()
        print("=" * 60)
        print(f"📊 TEST RESULTS: {passed} passed, {failed} failed")
        print("=" * 60)
        
        self.results = results
        return results
    
    def fix_issues(self) -> int:
        """Attempt to fix common issues."""
        fixed = 0
        
        # Make all scripts executable
        for tool in self.get_tools().keys():
            path = self.scripts_dir / tool
            if path.exists() and not os.access(path, os.X_OK):
                os.chmod(path, 0o755)
                print(f"✅ Made executable: {tool}")
                fixed += 1
        
        return fixed


def main():
    parser = argparse.ArgumentParser(description='Clawdbot Tool Tester')
    parser.add_argument('--fix', action='store_true', help='Auto-fix issues')
    parser.add_argument('--json', action='store_true', help='JSON output')
    args = parser.parse_args()
    
    tester = ToolTester()
    
    if args.fix:
        fixed = tester.fix_issues()
        print(f"\n✅ Fixed {fixed} issues")
    else:
        results = tester.run_tests()
        if args.json:
            print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
