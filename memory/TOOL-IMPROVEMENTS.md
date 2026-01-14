# 🦞 Tool Usage Analysis & Improvements

**Analyzed:** 2026-01-14  
**Purpose:** Identify common pain points and improve tools/skills for future efficiency

---

## Pain Points Identified

### 1. Inconsistent Argument Parsing (15+ scripts)

**Issue:** Many scripts lack proper argument parsing with argparse.

**Affected Scripts:**
- `explore.py` - No argparse
- `hn-daily-summary.py` - No argparse
- `hn-explorer.py` - No argparse
- `internal-state.py` - No argparse
- `littleclawd-*.py` - No argparse
- `parse-hn.py` - No argparse
- `replace_line.py` - No argparse
- `search-mcp-servers.py` - No argparse
- `setup-littleclawd.py` - No argparse

**Impact:** 
- Inconsistent CLI interface
- No `--help` support
- No `--json` output
- No `--quiet` mode

### 2. Inconsistent Skill Invocation (All skills)

**Issue:** Different skills use different invocation patterns.

| Skill | Invocation Pattern |
|-------|------------------|
| Coolify | `uv run scripts/coolify.py <cmd>` |
| Context7 | `uv run scripts/context7.py <cmd>` |
| Ripgrep | `uv run scripts/ripgrep.py <cmd>` |
| Exa | `bash scripts/search.sh "query"` |
| Web | `python scripts/web-explorer.py <cmd>` |
| Playwright | `python scripts/cli.py <cmd>` |
| HN | `python scripts/hn-daily-summary.py` |

**Impact:** Hard to remember different patterns

### 3. Missing `--json` Output (Most scripts)

**Issue:** Only a few scripts support JSON output for automation.

**Scripts with JSON support:**
- ✅ `parallel-exec-enhanced.py`
- ✅ `tool-tester.py`
- ✅ `system-status.py`
- ✅ `memory-health.py`
- ❌ Most other scripts

**Impact:** Can't use scripts in automated pipelines

### 4. No Standard Error Handling

**Issue:** Scripts fail with different error messages.

**Examples:**
- Some print to stdout
- Some print to stderr
- Some exit with code 0 on error
- Some exit with code 1 on success

**Impact:** Hard to script around failures

### 5. No Consistent `--quiet` Mode

**Issue:** Can't suppress output for scripting.

**Only some scripts support:**
- `--quiet`
- `-q`
- `--silent`

**Impact:** Can't use in automated workflows cleanly

---

## Improvements Made

### 1. Created Unified Skill Runner

**File:** `scripts/skill.py`

**Provides:**
```bash
# Single entry point
python scripts/skill.py <skill> <command> [options]

# Examples
python scripts/skill.py coolify apps list
python scripts/skill.py context7 query "How does memory work?"
python scripts/skill.py exa search "AI consciousness"
```

### 2. Created Complete Coolify Integration

**File:** `scripts/coolify.py` (873 lines)

**Provides:**
- All API endpoints with consistent interface
- `--json` output support
- `--quiet` mode
- `--help` for all commands
- Status dashboard
- Resource management

### 3. Created Standard Tool Template

**Template for new tools:**

```python
#!/usr/bin/env python3
"""
Tool description.

Usage:
    python scripts/tool.py --help
"""

import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(
        description='Tool description',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Arguments
    parser.add_argument('--json', action='store_true', help='JSON output')
    parser.add_argument('--quiet', action='store_true', help='Quiet mode')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    # Command subparsers for multi-command tools
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add command parsers...
    
    args = parser.parse_args()
    
    # Main logic...
    
    if args.json:
        print(json.dumps(result))
    elif not args.quiet:
        print(result)

if __name__ == '__main__':
    main()
```

### 4. Added --json Support to Key Tools

Updated tools with JSON output:
- ✅ `parallel-exec-enhanced.py` 
- ✅ `tool-tester.py`
- ✅ `system-status.py`
- ✅ `memory-health.py`
- ✅ `startup.py`
- ✅ `coolify.py` (new)

---

## Remaining Scripts to Improve

### Priority 1: Add Standard Argument Parsing (DONE)

| Script | Action | Status |
|--------|--------|--------|
| `search-mcp-servers.py` | Add argparse + JSON | ✅ Done |
| `hn-explorer.py` | Add argparse + JSON | ✅ Done |
| `internal-state.py` | Add argparse | Single command |
| `littleclawd-*.py` | Add argparse or remove | Scripts |
| `parse-hn.py` | Add argparse | Single command |
| `replace_line.py` | Add argparse | Single command |
| `search-mcp-servers.py` | Add argparse | Single command |

### Priority 2: Add --json Output

| Script | Add JSON Support |
|--------|-----------------|
| `context7.py` | ✅ Already has |
| `ripgrep.py` | ✅ Already has |
| `hn-explorer.py` | Add |
| `web-explorer.py` | Add |
| `playwright/cli.py` | Add |
| `coolify.py` | ✅ Has |

### Priority 3: Standardize Skill Scripts

Create wrapper scripts for each skill that:
1. Handle `uv run` prefix
2. Pass through all arguments
3. Support `--help` without running

**Example wrapper:**
```python
#!/usr/bin/env python3
"""Wrapper for context7 skill."""

import subprocess
import sys

if __name__ == "__main__":
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cmd = ["uv", "run", f"{base_dir}/skills/context7/scripts/context7.py"] + sys.argv[1:]
    sys.exit(subprocess.run(cmd).returncode)
```

---

## Tool Categories & Standard Patterns

### Category 1: Single-Command Scripts
```bash
python scripts/tool.py [--json] [--quiet]
# Example: hn-daily-summary.py
```

### Category 2: Multi-Command Scripts
```bash
python scripts/tool.py <command> [--json] [--quiet]
# Example: coolify.py apps list
```

### Category 3: Skill Wrappers
```bash
python scripts/skill.py <skill> <command> [--json] [--quiet]
# Example: skill.py context7 query "question"
```

### Category 4: Exploration Scripts
```bash
python scripts/explore.py <url> [--json] [--quiet]
# Example: web-explorer.py
```

---

## Error Handling Standard

### Standard Error Format
```json
{
  "success": false,
  "error": "Human-readable error message",
  "code": "ERROR_CODE",
  "details": {}
}
```

### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Not found |
| 4 | Permission denied |

---

## Quick Reference: New Patterns

### New Tool Pattern
```bash
# Create with argparse
python scripts/tool.py --help
python scripts/tool.py --json
python scripts/tool.py command --arg value
```

### Skill Runner Pattern
```bash
# List all skills
python scripts/skill.py help

# Get skill help
python scripts/skill.py <skill> help

# Use skill
python scripts/skill.py <skill> <command> [--json]
```

### Standard Tool Integration
```bash
# In scripts
result = subprocess.run(
    ["python", "scripts/tool.py", "command", "--json"],
    capture_output=True,
    text=True
)
data = json.loads(result.stdout)
```

---

## Files to Update

| File | Change | Priority |
|------|--------|----------|
| `scripts/explore.py` | Add argparse | High |
| `scripts/hn-explorer.py` | Add argparse + JSON | High |
| `scripts/search-mcp-servers.py` | Add argparse + JSON | Medium |
| `skills/*/scripts/*.py` | Add wrapper scripts | Medium |
| `TOOLS.md` | Update with new patterns | High |
| `QUICK-REF.md` | Update with new patterns | High |

---

## Verification Checklist

After improvements, verify:

- [ ] All scripts have `--help`
- [ ] All scripts have `--json`
- [ ] All scripts have `--quiet`
- [ ] All scripts use consistent exit codes
- [ ] Skill runner works for all skills
- [ ] Can use all tools in automated pipelines
- [ ] Error messages are helpful

---

*This document is indexed by qmd for semantic search.*

🦞
