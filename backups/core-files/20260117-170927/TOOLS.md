# 🦞 Clawdbot Tools Documentation

**Created:** 2026-01-13  
**Last Updated:** 2026-01-13  
**Purpose:** Documentation for all custom scripts and tools in Clawdbot

---

## Overview

This document catalogs all custom tools and scripts created for Clawdbot. Each tool is designed to improve efficiency for specific workflows.

---

## Tool: `scripts/file-edit.py`

**Purpose:** Efficient file editing with partial reads, line editing, and verification

### Commands

| Command | Description |
|---------|-------------|
| `read` | Read specific lines from a file |
| `edit-line` | Edit a specific line |
| `edit-range` | Replace a range of lines |
| `verify` | Verify two files are identical |
| `hash` | Compute file hash |
| `diff-text` | Create diff between two texts |

### Usage Examples

```bash
# Read lines 10-20 from a file
python scripts/file-edit.py read /path/to/file.txt --start 10 --end 20

# Edit line 15
python scripts/file-edit.py edit-line /path/to/file.txt 15 "new content"

# Replace lines 2-4 with new content
python scripts/file-edit.py edit-range /path/to/file.txt 2 4 "line1\nline2\nline3"

# Verify files are identical
python scripts/file-edit.py verify /path/to/original.txt /path/to/modified.txt

# Compute SHA256 hash
python scripts/file-edit.py hash /path/to/file.txt

# Create diff between texts
python scripts/file-edit.py diff-text "old text" "new text"
```

### Features

- **Partial Reads:** Read specific line ranges without loading entire file
- **Line Editing:** Edit specific lines without exact oldText matching
- **Verification:** Compare files with diff
- **Hashing:** SHA256 file integrity verification
- **Diff Creation:** Generate unified diffs from text
- **Backup:** Automatic backup before edits

### Requirements

- Python 3.9+
- Git (for diff verification)
- sed (for line editing)

---

## Tool: `scripts/parallel-exec.py`

**Purpose:** Run commands and API calls in parallel for faster batch processing

### Commands

| Command | Description |
|---------|-------------|
| `curl` | Parallel curl requests |
| `exec` | Parallel command execution |
| `api` | Parallel API calls |
| `download` | Parallel file downloads |
| `git` | Parallel git operations |

### Usage Examples

```bash
# Parallel curl from file (4 workers)
python scripts/parallel-exec.py curl urls.txt -w 4

# Parallel command execution (4 workers)
python scripts/parallel-exec.py exec commands.txt -w 4

# Parallel API calls (8 workers)
python scripts/parallel-exec.py api endpoints.txt -w 8

# Parallel file downloads (4 workers)
python scripts/parallel-exec.py download urls.txt ./downloads -w 4

# Parallel git operations (4 workers)
python scripts/parallel-exec.py git repos.txt "pull" -w 4
```

### Features

- **Configurable Workers:** Control parallelism with `-w N` flag
- **Progress Output:** Real-time progress indication
- **Error Handling:** Reports failed items with errors
- **Output Support:** Save curl/api results to directory
- **Quiet Mode:** Suppress output with `-q` flag
- **Timeout:** 120-second timeout for commands, 30 seconds for URLs

### Input File Format

Each file should contain one item per line:

```text
# Comments are ignored
url1
url2
url3
```

### Requirements

- Python 3.9+
- concurrent.futures (built-in)
- urllib (built-in)

---

## Tool: `skills/coolify/scripts/coolify.py`

**Purpose:** Manage Coolify deployments from CLI

### Commands

| Command | Description |
|---------|-------------|
| `apps list` | List all applications |
| `apps get <uuid>` | Get application details |
| `apps logs <uuid>` | Get application logs |
| `apps watch <uuid>` | Monitor application status |
| `apps restart <uuid>` | Restart application |
| `dbs list` | List all databases |
| `dbs get <uuid>` | Get database details |
| `projects list` | List all projects |
| `deploy <name> <fqdn> <repo>` | Deploy new application |

### Usage Examples

```bash
# List all applications
uv run /home/opc/clawd/skills/coolify/scripts/coolify.py apps list

# Get application details
uv run /home/opc/clawd/skills/coolify/scripts/coolify.py apps get <uuid>

# Watch application status
uv run /home/opc/clawd/skills/coolify/scripts/coolify.py apps watch <uuid>

# Deploy new application
uv run /home/opc/clawd/skills/coolify/scripts/coolify.py deploy "MyApp" app.bradarr.com owner/repo
```

### Features

- Rich table output
- Raw JSON output with `--raw` flag
- Application logs retrieval
- Status monitoring with watch command
- GitHub deployment

### Requirements

- Coolify API key (`COOLIFY_API_KEY` environment variable)
- Python 3.9+
- requests library

---

## Tool: `skills/hn/scripts/hn.py`

**Purpose:** Browse Hacker News from CLI

### Commands

| Command | Description |
|---------|-------------|
| `top [n]` | Get top stories |
| `new [n]` | Get new stories |
| `best [n]` | Get best stories |
| `ask [n]` | Get ask HN stories |
| `show [n]` | Get show HN stories |
| `jobs [n]` | Get jobs stories |
| `story <id>` | Get story with comments |

### Usage Examples

```bash
# Get top 10 stories
uv run /home/opc/clawd/skills/hn/scripts/hn.py top 10

# Get new stories
uv run /home/opc/clawd/skills/hn/scripts/hn.py new

# Get story with comments
uv run /home/opc/clawd/skills/hn/scripts/hn.py story 12345
```

### Features

- Browse top, new, best, ask, show, jobs stories
- Get full story with comments
- Configurable story count
- Rich table output

### Requirements

- Python 3.9+
- requests library

---

## Tool: `skills/context7/scripts/context7.py`

**Purpose:** Codebase Q&A with Context7 MCP

### Commands

| Command | Description |
|---------|-------------|
| `query "question"` | Query codebase with natural language |
| `index` | Re-index codebase |
| `status` | Check index status |

### Usage Examples

```bash
# Query codebase
uv run /home/opc/clawd/skills/context7/scripts/context7.py query "How does file editing work?"

# Re-index codebase
uv run /home/opc/clawd/skills/context7/scripts/context7.py index

# Check status
uv run /home/opc/clawd/skills/context7/scripts/context7.py status
```

### Features

- Natural language codebase queries
- Codebase indexing
- Context7 MCP integration

### Requirements

- Context7 MCP server (`@upstash/context7-mcp`)
- Upstash Redis credentials

---

## Tool: `skills/ripgrep/scripts/ripgrep.py`

**Purpose:** Fast search with ripgrep

### Commands

| Command | Description |
|---------|-------------|
| `search "pattern" [path]` | Search for pattern |
| `files "pattern"` | Find files matching pattern |
| `count "pattern"` | Count matches |

### Usage Examples

```bash
# Search for pattern
uv run /home/opc/clawd/skills/ripgrep/scripts/ripgrep.py search "def function" /path

# Find files
uv run /home/opc/clawd/skills/ripgrep/scripts/ripgrep.py files "*.py"

# Count matches
uv run /home/opc/clawd/skills/ripgrep/scripts/ripgrep.py count "TODO"
```

### Features

- Fast recursive search
- File finding by pattern
- Match counting
- Regular expression support

### Requirements

- ripgrep (installed via Homebrew)

---

## Tool: `skills/playwright-automation/scripts/playwright.py`

**Purpose:** Browser automation with Playwright

### Commands

| Command | Description |
|---------|-------------|
| `install` | Install Playwright browsers |
| `open <url>` | Open URL in browser |
| `screenshot <url> <file>` | Take screenshot |
| `click <url> <selector>` | Click element |

### Usage Examples

```bash
# Install browsers
uv run /home/opc/clawd/skills/playwright-automation/scripts/playwright.py install

# Open URL
uv run /home/opc/clawd/skills/playwright-automation/scripts/playwright.py open "https://example.com"

# Take screenshot
uv run /home/opc/clawd/skills/playwright-automation/scripts/playwright.py screenshot "https://example.com" screenshot.png

# Click element
uv run /home/opc/clawd/skills/playwright-automation/scripts/playwright.py click "https://example.com" "#button"
```

### Features

- Browser automation with Playwright
- Firefox-based (ARM64 compatible)
- Screenshot capture
- Element interaction

### Requirements

- Playwright
- Firefox browser

---

## File Editing Tools (Unified)

### Use the Right Tool for the Job

| Situation | Command | Example |
|-----------|---------|---------|
| Know line number | `edit-line` | `edit-line /path.txt 15 "content"` |
| Know text, not line | `edit-text --fuzzy` | `edit-text /path.txt "old" "new" --fuzzy` |
| Know line range | `edit-range` | `edit-range /path.txt 5 10 "new"` |
| Partial file read | `read` | `read /path.txt --start 10 --end 20` |
| Verify changes | `verify` | `verify /path1.txt /path2.txt` |

**Key insight from session analysis:** 36+ edit failures due to exact text matching. Use `file-edit.py` commands instead of the native `edit` tool.

### `scripts/file-edit.py` (ENHANCED - 2026-01-14)

All file editing in ONE tool with improved commands:

```bash
# Edit line 15 (PREFERRED - no text matching needed)
python scripts/file-edit.py edit-line /path.txt 15 "new content"

# Edit text content with exact match
python scripts/file-edit.py edit-text /path.txt "exact old text" "new text"

# Edit text with fuzzy matching (handles whitespace!)
python scripts/file-edit.py edit-text /path.txt "partial old text" "new text" --fuzzy

# Read lines 10-20
python scripts/file-edit.py read /path.txt --start 10 --end 20

# Verify files are identical
python scripts/file-edit.py verify /path1.txt /path2.txt

# Compute SHA256 hash
python scripts/file-edit.py hash /path.txt

# Create diff between two texts
python scripts/file-edit.py diff-text "old" "new"
```

**New in v2.0:** Added `edit-text` command with `--fuzzy` flag to replace the standalone `safe-edit.py`.

---

## Service Waiting Tools (ENHANCED - 2026-01-14)

### `scripts/utils/wait-for.sh`
Intelligent waiting for services/ports with content checking and JSON output.

```bash
# Wait for URL (basic)
./wait-for.sh http://localhost:3000 --timeout 30

# Wait for port
./wait-for.sh port:3000 --timeout 30

# Wait for Docker container
./wait-for.sh docker:jj-app --timeout 60

# Wait for specific content in response
./wait-for.sh http://localhost:3000/api/health --contains "ok" --timeout 30

# JSON output for programmatic use
./wait-for.sh http://localhost:3000 --json
# Output: {"success": true, "url": "...", "reason": "available", "elapsed": 5}
```

**From session analysis:** 284+ sleep commands found. Replace with this utility.

**New in v2.0:** Added `--contains` for content checking and `--json` for programmatic use.

---

## API Call Tools

### Use the Right Tool for the Job

| Situation | Tool | Why |
|-----------|------|-----|
| Single API call | `api-call.sh` | Simple, standardized |
| Multiple API calls | `parallel-exec.py api` | Batch processing |
| One-off curl | Direct curl | Quick ad-hoc |

### `scripts/utils/api-call.sh` (ENHANCED - 2026-01-14)
Standardized single API calls with error handling and JSON output.

```bash
# GET request
./api-call.sh GET http://localhost:3000/api/data

# POST with data
./api-call.sh POST http://localhost:3000/api/chat --data '{"msg":"hello"}'

# With headers
./api-call.sh GET https://api.example.com --headers "Auth:Bearer token"

# JSON output for programmatic use
./api-call.sh GET http://localhost:3000/api/data --json
# Output: {"success": true, "data": {...}}

# Failed call (JSON mode)
./api-call.sh GET http://localhost:3000/missing --json
# Output: {"success": false, "error": "...", "url": "...", "method": "GET"}
```

**New in v2.0:** Added `--json` for programmatic output with proper error handling.

### `scripts/parallel-exec.py` (EXISTING)
Parallel execution for batch processing.

```bash
# Parallel API calls (8 workers)
python scripts/parallel-exec.py api endpoints.txt -w 8
```

---

## Quick Reference

### File Editing

```bash
# Partial read
python scripts/file-edit.py read <path> --start N --end N

# Line edit
python scripts/file-edit.py edit-line <path> N "content"

# Verify
python scripts/file-edit.py verify <path1> <path2>
```

### Parallel Execution

```bash
# Parallel curl
python scripts/parallel-exec.py curl <file> -w 4

# Parallel exec
python scripts/parallel-exec.py exec <file> -w 4

# Parallel API
python scripts/parallel-exec.py api <file> -w 8
```

### Deployment

```bash
# List apps
uv run /home/opc/clawd/skills/coolify/scripts/coolify.py apps list

# Deploy
uv run /home/opc/clawd/skills/coolify/scripts/coolify.py deploy "name" "fqdn" "repo"
```

### Search

```bash
# Search codebase
uv run /home/opc/clawd/skills/context7/scripts/context7.py query "question"

# Search files
uv run /home/opc/clawd/skills/ripgrep/scripts/ripgrep.py search "pattern"
```

### Task Orchestration

```bash
# Show dashboard
python scripts/to.py status              # Task dashboard

# Add task with priority and retry
python scripts/to.py add "echo task" --priority 10 --retry 3 --desc "Task name"

# Process queue
python scripts/to.py run                 # Process queue

# Spawn sub-agent
python scripts/to.py spawn "Research AI" --label "research"

# Monitor sub-agent
python scripts/to.py history <session-key>

# Cleanup stale sessions
python scripts/to.py cleanup
```

### System Management

```bash
# System status (quick)
python scripts/system-status.py --brief

# System status (full dashboard)
python scripts/system-status.py

# System status (JSON)
python scripts/system-status.py --json

# Startup routine
python scripts/startup.py                # Full startup
python scripts/startup.py --quick        # Quick summary

# Tool tester (run all tests)
python scripts/tool-tester.py

# Tool tester (auto-fix issues)
python scripts/tool-tester.py --fix

# Memory backup (create)
python scripts/backup.py

# Memory backup (auto with retention)
python scripts/backup.py --auto

# Memory backup (list)
python scripts/backup.py --list

# Memory backup (restore)
python scripts/backup.py --restore

# Memory health check
python scripts/memory-health.py

# Memory health check (score only)
python scripts/memory-health.py --score
```

### Parallel Execution Enhanced

```bash
# Auto-scaling workers
python scripts/parallel-exec-enhanced.py exec commands.txt -w 0

# With retry logic
python scripts/parallel-exec-enhanced.py exec commands.txt --retry 3 --retry-delay 1

# Rate-limited API calls
python scripts/parallel-exec-enhanced.py api endpoints.txt --rate-limit 10

# Save queue for later
python scripts/parallel-exec-enhanced.py exec tasks.txt --save my-queue

# List saved queues
python scripts/parallel-exec-enhanced.py queue list
```

---

## Best Practices

### File Editing
1. Use `read` with `--start`/`--end` for partial file access
2. Use `edit-line` for single line changes
3. Use `verify` after edits to confirm changes
4. Use `hash` for integrity verification

### Parallel Execution
1. Start with 4 workers (`-w 4`)
2. Increase to 8 for API calls (`-w 8`)
3. Use quiet mode for automation (`-q`)
4. Check output directory for results

### General
1. Check tool help with `--help`
2. Test with small inputs first
3. Use `--raw` flag for programmatic output
4. Check return codes in scripts

---

## Adding New Tools

To add a new tool:

1. Create directory: `skills/toolname/`
2. Add `SKILL.md` with documentation
3. Add `scripts/toolname.py` CLI wrapper
4. Update this file with documentation

---

*This document is indexed by qmd for semantic search.*

🦞
