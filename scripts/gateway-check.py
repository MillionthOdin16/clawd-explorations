#!/usr/bin/env python3
"""
Gateway State Checker

Check gateway state before attempting config changes.
Prevents "unauthorized" errors by detecting blocked gateway state.

Usage:
    python scripts/gateway-check.py          # Check state
    python scripts/gateway-check.py --fix  # Attempt fix
"""

import argparse
import subprocess
import sys


def check_gateway_state():
    """Check if gateway is in usable state."""
    try:
        result = subprocess.run(
            ["clawdbot", "sessions", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        output = result.stdout + result.stderr
        
        if "unauthorized" in output or "blocked" in output:
            return {
                "status": "blocked",
                "message": "Gateway is in blocked state",
                "action": "gateway restart may help"
            }
        
        if "error" in output.lower() and "unauthorized" not in output:
            return {
                "status": "error",
                "message": result.stderr[:100],
                "action": "check gateway status manually"
            }
        
        return {
            "status": "active",
            "message": "Gateway is active",
            "action": None
        }
        
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "message": "Gateway check timed out",
            "action": "check if clawdbot is running"
        }
    except FileNotFoundError:
        return {
            "status": "not-found",
            "message": "clawdbot CLI not found",
            "action": "install clawdbot"
        }
    except Exception as e:
        return {
            "status": "unknown",
            "message": str(e)[:100],
            "action": "check gateway manually"
        }


def attempt_fix():
    """Attempt to fix gateway state."""
    print("🔧 Attempting gateway fix...")
    
    # Try gateway restart via CLI
    result = subprocess.run(
        ["clawdbot", "daemon", "restart"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode == 0:
        print("✅ Gateway restart initiated")
        print("   Waiting 5 seconds for restart...")
        import time
        time.sleep(5)
        return True
    else:
        print(f"❌ Restart failed: {result.stderr[:100]}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Check gateway state before config changes"
    )
    parser.add_argument(
        "--fix", "-f",
        action="store_true",
        help="Attempt to fix blocked gateway"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    state = check_gateway_state()
    
    if args.json:
        print(json.dumps(state, indent=2))
        return 0 if state["status"] == "active" else 1
    
    # Human-readable output
    print(f"\n{'='*50}")
    print("GATEWAY STATE CHECK")
    print(f"{'='*50}\n")
    
    status = state["status"]
    
    if status == "active":
        print(f"✅ Status: {status}")
        print(f"   {state['message']}")
        return 0
    
    elif status == "blocked":
        print(f"⚠️  Status: {status}")
        print(f"   {state['message']}")
        print(f"\n💡 Action: {state['action']}")
        
        if args.fix:
            print("\n🛠️  Attempting fix...")
            if attempt_fix():
                print("\n✅ Fix may have worked - check status again")
            else:
                print("\n❌ Fix failed - manual intervention needed")
        else:
            print(f"\n🔧 Run with --fix to attempt auto-fix")
        return 1
    
    else:
        print(f"❓ Status: {status}")
        print(f"   {state['message']}")
        print(f"\n💡 Action: {state['action']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
