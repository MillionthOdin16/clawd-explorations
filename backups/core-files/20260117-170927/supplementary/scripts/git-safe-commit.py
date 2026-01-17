#!/usr/bin/env python3
"""
Git Safe Commit - Verify no secrets before commit

Prevents credential leaks by checking for secrets in staging.

Usage:
    python scripts/git-safe-commit.sh          # Check staging
    python scripts/git-safe-commit.sh --check-files   # Check all files
"""

import argparse
import subprocess
import sys
import os

# Patterns that indicate secrets
DANGEROUS_PATTERNS = [
    ".env",
    ".secrets",
    "secrets",
    "keys",
    "token",
    "password",
    "api_key",
    "API_KEY",
    "SECRET",
    "private_key",
    "credential",
    "auth",
    ".bashrc",  # May contain credentials
    ".bash_history",  # May contain secrets
    ".ssh/",  # SSH keys
]


def check_staging():
    """Check git staging area for secrets."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )
    
    if result.returncode != 0:
        return {"success": False, "error": result.stderr[:100]}
    
    dangerous_files = []
    
    for line in result.stdout.splitlines():
        # Staged files start with "A " or "M " in second column
        if line.startswith("A ") or line.startswith("M "):
            filename = line[3:].strip()
            for pattern in DANGEROUS_PATTERNS:
                if pattern in filename.lower():
                    dangerous_files.append(filename)
                    break
    
    if dangerous_files:
        return {
            "success": False,
            "dangerous_files": dangerous_files,
            "message": f"Found {len(dangerous_files)} potentially dangerous files in staging"
        }
    
    return {"success": True, "message": "No dangerous files detected"}


def check_all_files():
    """Check all tracked files for secrets (slower)."""
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )
    
    if result.returncode != 0:
        return {"success": False, "error": result.stderr[:100]}
    
    files = result.stdout.strip().split("\n")
    dangerous_files = []
    
    for filename in files:
        for pattern in DANGEROUS_PATTERNS:
            if pattern in filename.lower():
                dangerous_files.append(filename)
                break
    
    if dangerous_files:
        # Check if already in .gitignore
        gitignore_result = subprocess.run(
            ["git", "check-ignore"] + dangerous_files,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        ignored = gitignore_result.stdout.strip().split("\n") if gitignore_result.returncode == 0 else []
        
        tracked_dangerous = [f for f in dangerous_files if f not in ignored]
        
        if tracked_dangerous:
            return {
                "success": False,
                "dangerous_files": tracked_dangerous,
                "message": f"Found {len(tracked_dangerous)} dangerous files TRACKED by git"
            }
    
    return {"success": True, "message": "No dangerous tracked files"}


def check_gitignore():
    """Check if .gitignore is committed."""
    result = subprocess.run(
        ["git", "ls-files", ".gitignore"],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )
    
    if result.returncode == 0 and result.stdout.strip():
        return {"committed": True, "message": ".gitignore is committed"}
    
    return {"committed": False, "message": ".gitignore NOT committed!"}


def main():
    parser = argparse.ArgumentParser(
        description="Check for secrets before commit",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--check-files", "-f",
        action="store_true",
        help="Check ALL tracked files (slower)"
    )
    parser.add_argument(
        "--gitignore", "-g",
        action="store_true",
        help="Check if .gitignore is committed"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--fix", "-x",
        action="store_true",
        help="Exit 1 if dangerous files found"
    )
    
    args = parser.parse_args()
    
    # Check .gitignore first
    if args.gitignore or args.gitignore:
        gitignore_status = check_gitignore()
        
        if args.json:
            print(json.dumps(gitignore_status, indent=2))
        else:
            print(f"\n{'='*50}")
            print("GITIGNORE CHECK")
            print(f"{'='*50}\n")
            
            if gitignore_status["committed"]:
                print("✅ .gitignore IS committed")
                print("   Safe to stage and commit")
            else:
                print("❌ .gitignore NOT committed!")
                print("   CRITICAL: Add .gitignore before any secrets files")
        
        return 0
    
    # Check staging area
    if args.check_files:
        check = check_all_files()
    else:
        check = check_staging()
    
    if args.json:
        print(json.dumps(check, indent=2))
        return 0 if check["success"] else (1 if args.fix else 0)
    
    # Human output
    print(f"\n{'='*50}")
    print("SECURITY CHECK")
    print(f"{'='*50}\n")
    
    if check["success"]:
        print("✅ PASSED - No dangerous files detected")
        print(f"   {check['message']}")
        return 0
    
    print(f"❌ FAILED - {check['message']}\n")
    
    if "dangerous_files" in check:
        print("🚫 DANGEROUS FILES IN STAGING:")
        for f in check["dangerous_files"]:
            print(f"   - {f}")
        print("\n💡 REMEDY:")
        print("   1. Unstage: git reset <file>")
        print("   2. Add to .gitignore")
        print("   3. Commit .gitignore FIRST")
        print("   4. Then commit other files")
    
    return 1 if args.fix else 0


if __name__ == "__main__":
    sys.exit(main())
