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
