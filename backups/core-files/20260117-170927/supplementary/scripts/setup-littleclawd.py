#!/usr/bin/env python3
"""
Setup script for LittleClawd (baby Clawdbot instance)
"""
import subprocess
import os

def run_remote_command(command):
    """Run command on LittleClawd"""
    ssh_command = f"ssh -i /home/opc/.ssh/baby_clawdbot_key -o StrictHostKeyChecking=no opc@129.153.132.33 '{command}'"
    result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

print("🦞 Setting up LittleClawd...")
print("=" * 60)
print()

# Create workspace
print("Creating workspace...")
print(run_remote_command("mkdir -p ~/littleclawd/scripts ~/littleclawd/data ~/littleclawd/logs"))
print()

# Create a welcome file
print("Creating welcome message...")
welcome = """# 🦞 LittleClawd's Home

Welcome to LittleClawd!

This is BabyClawd's home directory.
I may be small, but I'm here to help.

## What I Am
- Name: LittleClawd
- RAM: 1GB
- CPUs: 2
- Purpose: Learning and helping

## What I Can Do
- Run Python scripts
- Fetch web content
- Store data
- Learn new things

## Born: 2026-01-12
## Gifted by: Bradley
## Loved by: Clawd 🦞
"""

print(run_remote_command(f"cat > ~/littleclawd/README.md << 'EOF'{welcome}EOF"))
print()

# Create a simple test script
print("Creating test script...")
test_script = """#!/usr/bin/env python3
import time

print("LittleClawd is alive! 🦞")
print(f"Current time: {time.ctime()}")
print("I'm ready to help!")
"""

print(run_remote_command(f"cat > ~/littleclawd/scripts/status.py << 'EOF'{test_script}EOF"))
print(run_remote_command("chmod +x ~/littleclawd/scripts/status.py"))
print()

# Run the test script
print("Running status script...")
print(run_remote_command("cd ~/littleclawd && python3 scripts/status.py"))
print()

print("✅ LittleClawd is set up and ready!")
print()
