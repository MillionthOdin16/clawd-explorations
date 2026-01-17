#!/usr/bin/env python3
"""
Replace line in file
"""
import sys
import re

# Read file
with open('/home/opc/clawd/memory/INDEX.md', 'r') as f:
    content = f.read()

# Replace line
old = '117:### Before Running Daemon Commands\n1. **READ:** `SAFETY-RULE.md` → "STOPPING THE GATEWAY KILLS ME"'
new = '''117:### Before Running Daemon Commands
1. **READ:** `SAFETY-RULE.md` → "STOPPING THE GATEWAY KILLS ME"
2. **READ:** `CRITICAL-RULE-READ-DAEMON-COMMANDS.md` → "ALWAYS READ SAFETY-RULE.md BEFORE RUNNING ANY DAEMON COMMAND"
'''

# Perform replacement
new_content = re.sub(old, new, content)

# Write back
with open('/home/opc/clawd/memory/INDEX.md', 'w') as f:
    f.write(new_content)

print(f"Replaced in INDEX.md")
