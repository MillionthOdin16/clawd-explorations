#!/usr/bin/env python3
"""
Timeout-Aware Command Runner

Run commands with timeout awareness and background mode support.

Usage:
    python scripts/run-safe.py "command"              # Run with default timeout
    python scripts/run-safe.py "command" --timeout 60  # 60 second timeout
    python scripts/run-safe.py "command" --background  # Background mode
    python scripts/run-safe.py "command" --poll 5      # Poll every 5 seconds
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


def run_command(cmd, timeout=300, background=False, poll_interval=10, quiet=False):
    """
    Run command with timeout awareness.
    
    Args:
        cmd: Command to run (string or list)
        timeout: Timeout in seconds (default: 300 = 5 min)
        background: Run in background
        poll_interval: Poll interval for background tasks
        quiet: Suppress output
    
    Returns:
        dict with success, stdout, stderr, returncode, status
    """
    if isinstance(cmd, str):
        cmd = cmd
    
    result = {
        "success": False,
        "stdout": "",
        "stderr": "",
        "returncode": -1,
        "status": "pending",
        "timeout": timeout,
        "background": background,
        "command": cmd if isinstance(cmd, str) else " ".join(cmd)
    }
    
    try:
        if background:
            # Start in background
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            result["status"] = "running"
            result["pid"] = process.pid
            
            if not quiet:
                print(f"🚀 Started in background (PID: {process.pid}, timeout: {timeout}s)")
            
            # Poll for completion
            elapsed = 0
            while elapsed < timeout:
                poll = process.poll()
                if poll is not None:
                    result["returncode"] = poll
                    result["stdout"], result["stderr"] = process.communicate()
                    result["success"] = poll == 0
                    result["status"] = "completed" if poll == 0 else "failed"
                    break
                
                time.sleep(poll_interval)
                elapsed += poll_interval
                
                if not quiet and elapsed % 30 == 0:
                    print(f"   Still running... ({elapsed}s elapsed, {timeout - elapsed}s remaining)")
            
            if result["status"] == "running":
                result["status"] = "timeout"
                result["stderr"] = f"Timeout after {timeout}s"
                process.kill()
            
            if not quiet:
                if result["success"]:
                    print("✅ Command completed successfully")
                else:
                    print(f"❌ Command failed: {result['status']}")
        
        else:
            # Run with timeout
            process = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            result["stdout"] = process.stdout
            result["stderr"] = process.stderr
            result["returncode"] = process.returncode
            result["success"] = process.returncode == 0
            result["status"] = "completed" if process.returncode == 0 else "failed"
            
            if not quiet:
                if result["success"]:
                    print("✅ Command completed successfully")
                else:
                    print(f"❌ Command failed (exit {process.returncode})")
                    if process.stderr:
                        print(f"   Error: {process.stderr[:100]}")
        
    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        result["stderr"] = f"Timeout after {timeout}s"
        if not quiet:
            print(f"❌ Timeout after {timeout}s - use --background for long tasks")
    
    except Exception as e:
        result["status"] = "error"
        result["stderr"] = str(e)[:500]
        if not quiet:
            print(f"❌ Error: {e}")
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Run commands with timeout awareness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with 5 minute timeout
  python scripts/run-safe.py "npm install"
  
  # Run with 60 second timeout
  python scripts/run-safe.py "curl https://api.example.com" --timeout 60
  
  # Run in background (no timeout)
  python scripts/run-safe.py "long-running-script.sh" --background
  
  # Poll every 5 seconds
  python scripts/run-safe.py "build-script.sh" --background --poll 5
  
  # Get JSON output
  python scripts/run-safe.py "cmd" --json
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        help="Command to run"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=300,
        help="Timeout in seconds (default: 300)"
    )
    parser.add_argument(
        "--background", "-b",
        action="store_true",
        help="Run in background mode"
    )
    parser.add_argument(
        "--poll", "-p",
        type=int,
        default=10,
        help="Poll interval for background mode (default: 10s)"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress output"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    result = run_command(
        args.command,
        timeout=args.timeout,
        background=args.background,
        poll_interval=args.poll,
        quiet=args.quiet
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
