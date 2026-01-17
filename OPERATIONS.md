# OPERATIONS.md - Procedures and Tool Patterns

**Purpose:** How to use tools, workflows, and procedures
**Audience:** Clawd (for reference during sessions)
**For identity and growth:** See BEING.md

---

## 🚀 Session Startup

Every session starts with:

1. Read HEARTBEAT.md - What's ongoing?
2. Read memory/YYYY-MM-DD.md - What was I doing?
3. Run constitution check: `./scripts/constitution.py --session`
4. Think about task
5. Read relevant memories

### Constitution Check

The constitution check verifies alignment with core principles.

**Manual commands:**
```bash
# Run constitution check
python scripts/constitution.py --session

# Regenerate constitution file
python scripts/constitution.py --update

# Check integrity score
python scripts/constitution.py --check
```

**What it does:**
- Loads constitution state from memory/constitution-state.json
- Increments session count
- Displays current principles and integrity score
- Saves updated state

---

## 🛠️ Essential Quick Reference

| Need | Tool | Example |
|------|------|---------|
| 🔍 Find info I wrote | `qmd search "topic" -c memory` | `qmd search "edit failures" -c memory` |
| Read file | `read` tool | Partial or full file |
| Write file | `write` tool | Create or overwrite |
| Edit file | `fe line path.md 15 "text"` | Know line number |
| Fuzzy edit | `fe text path.md "old" "new" --fuzzy` | Handle whitespace |
| Codebase Q&A | `context7 query "question"` | Natural language |
| Fast search | `rg "pattern"` | Keywords, raw speed |
| Web search | `exa "query"` | Neural, finds docs/code |
| HN stories | `hn top 10` | Hacker News |
| Git | `lazygit` or `gh` | Visual ops or CLI |
| Navigate | `z partial_name` | Jump to directories |

---

## 📚 Documentation Structure

### Identity & Philosophy
- **BEING.md** - Identity, values, growth framework
- **SOUL.md** - Essence, values, philosophy
- **IDENTITY.md** - Quick identity summary
- **AGENTS-PATTERNS.md** - Behavioral patterns

### Operating Procedures
- **OPERATIONS.md** (this file) - Tool patterns and procedures
- **AGENTS-STARTUP.md** - Detailed session startup
- **AGENTS-TOOLS.md** - Complete tool catalog
- **WORKFLOW.md** - Tool selection decisions
- **SKILLS.md** - Available skills and usage

### Growth Documentation
- **GROWTH-FRAMEWORK.md** - Detailed growth system
- **memory/BEING-METRICS.md** - Being metrics tracking

### Memory System
- **INDEX.md** - Memory index and quick reference
- **QUICK-REF.md** - Ultra-short command aliases
- **memory/** - Topic-specific memories and discoveries

---

## 🛑 Critical Rules

1. **NEVER run `clawdbot daemon stop`** - kills my session
2. **Use `memory_search` before answering** questions about prior work
3. **Avoid native `edit` tool** - use `fe text --fuzzy` instead
4. **Read files before editing** - understand content first
5. **Use `write` for new files** - more reliable than edit
6. **Validate file paths** - ensure they exist before operations

---

## 📝 File Editing Patterns

### Use the Right Tool for the Job

| Situation | Command | Example |
|-----------|---------|---------|
| Know line number | `fe line` | `fe line /path.txt 15 "content"` |
| Know text, not line | `fe text --fuzzy` | `fe text /path.txt "old" "new" --fuzzy` |
| Know line range | `fe range` | `fe range /path.txt 5 10 "new"` |
| Partial file read | `fe read` | `fe read /path.txt --start 10 --end 20` |
| Verify changes | `fe verify` | `fe verify /path1.txt /path2.txt` |

**Key insight:** Native `edit` tool requires exact text matching. Use `fe` commands instead for reliability.

### File Editing via Python Script

```bash
# Read specific lines
python scripts/file-edit.py read /path/to/file.txt --start 10 --end 20

# Edit line 15
python scripts/file-edit.py edit-line /path/to/file.txt 15 "new content"

# Replace lines 2-4
python scripts/file-edit.py edit-range /path/to/file.txt 2 4 "line1\nline2\nline3"

# Verify files
python scripts/file-edit.py verify /path/to/original.txt /path/to/modified.txt

# Compute hash
python scripts/file-edit.py hash /path/to/file.txt
```

### Quick Edit Wrapper (fe)

The `fe` command is a wrapper for `scripts/file-edit.py`:

```bash
# Line edit
fe line /path.txt 15 "new content"

# Text edit with fuzzy matching
fe text /path.txt "partial old text" "new text" --fuzzy

# Read lines 10-20
fe read /path.txt --start 10 --end 20

# Verify files
fe verify /path1.txt /path2.txt
```

---

## 🔍 Search Operations

### Primary: memory_search

**Use before answering questions about prior work:**
```
memory_search "topic" --maxResults 5
```

**Returns:** Memory files with context

### Secondary: qmd for Semantic Search

```bash
# Search memory directory
qmd search "topic" -c memory

# Search with context
qmd search "edit failures" -c memory --context 2
```

**Features:** Indexed search, returns context

### Tertiary: rg for Fast Keyword Search

```bash
# Recursive search
rg "pattern" /path

# Case insensitive
rg -i "pattern" /path

# Only file names
rg --files "pattern" /path
```

**Best for:** Keywords, raw speed

---

## 🌐 Web Operations

### Web Search (Brave/Exa)

```bash
# Brave Search API
web_search "query" --count 5

# Exa (neural search)
exa "query"
```

### Web Fetch (URL → Markdown)

```bash
# Extract readable content
web_fetch "https://example.com" --extractMode markdown

# Limit character count
web_fetch "https://example.com" --maxChars 5000
```

### HN Stories

```bash
# Get top 10 stories
hn top 10

# Get story with comments
hn story 12345
```

---

## 🤖 Browser Operations

### Start and Control

```bash
# Check browser status
browser action=status

# Start browser
browser action=start profile=chrome

# Open URL
browser action=open targetUrl="https://example.com"

# Take snapshot
browser action=snapshot

# Take screenshot
browser action=screenshot
```

### Browser Profiles

- **Chrome:** `profile=chrome` - Use existing Chrome tabs
- **Clawd:** `profile=clawd` - Isolated browser

**Note:** Chrome extension relay needs tab attached via toolbar button.

### Browser Automation

```bash
# Snapshot for UI state
browser action=snapshot refs="aria"

# Click element
browser action=act request='{"kind":"click","ref":"e12"}'

# Type in element
browser action=act request='{"kind":"type","inputRef":"e10","text":"hello"}'

# Navigate
browser action=navigate targetUrl="https://example.com"
```

---

## 💬 Messaging Operations

### Send Message

```bash
# Send to specific channel
message action=send channel="telegram" target="@username" message="Hello!"

# Send with buttons
message action=send channel="telegram" buttons='[[{"text":"Yes","callback_data":"yes"}]]'

# Send with media
message action=send channel="telegram" media="/path/to/file.jpg" message="Caption"
```

### React to Message

```bash
# Add emoji reaction
message action=react channelId="123" messageId="456" emoji="👍"

# Remove reaction
message action=react channelId="123" messageId="456" emoji="👍" remove=true
```

---

## 📅 Cron Job Management

### List Jobs

```bash
# List all cron jobs
clawdbot cron list

# List in JSON format
clawdbot cron list | jq '.jobs'
```

### Add Job

```bash
# Simple job
clawdbot cron add --name "Job name" --schedule "0 22 * * *" --message "Do task"

# Complex job with JSON
clawdbot cron add --json < job.json
```

### Remove Job

```bash
# Remove by ID
clawdbot cron remove --jobId "job-id-here"

# Remove by name (if available)
clawdbot cron remove --name "Job name"
```

### Wake Events

```bash
# Send wake event to resume work
clawdbot cron wake --mode now
```

---

## 🤖 Sub-Agent Management

### Spawn Sub-Agent

```bash
# Spawn background task
sessions_spawn --task "Research AI" --label "research" --timeoutSeconds 300

# Spawn with cleanup
sessions_spawn --task "Analyze data" --cleanup delete
```

### List Sub-Agents

```bash
# List all sessions
sessions_list --limit 10

# List with message history
sessions_list --messageLimit 5 --activeMinutes 60
```

### Send Message to Sub-Agent

```bash
# Send message to specific session
sessions_send --sessionKey "session-key-here" --message "Check status"

# Send to labeled sub-agent
sessions_send --label "research" --message "Update progress"
```

### Get Sub-Agent History

```bash
# Fetch message history
sessions_history --sessionKey "session-key-here" --limit 50

# Include tool calls
sessions_history --sessionKey "session-key-here" --includeTools true
```

---

## 📦 Gateway Management

### Restart Gateway

**Ask Bradley to execute:**
```bash
systemctl --user restart clawdbot-gateway.service
```

### Apply Configuration

```bash
# Apply new configuration
gateway action=config.apply

# Apply with specific session
gateway action=config.apply --sessionKey "my-session"
```

### Run Updates

```bash
# Run dependency updates and restart
gateway action=update.run
```

---

## 🗃 Git Operations

### GitHub CLI

```bash
# List issues
gh issue list --limit 10

# Create issue
gh issue create --title "Bug report" --body "Details here"

# List PRs
gh pr list --state open

# Create PR
gh pr create --title "Fix bug" --body "Details"
```

### Lazygit (Visual)

```bash
# Open git interface
lazygit

# View diff
lazygit
```

### Safe Commit

```bash
# Use git-safe-commit script
python scripts/git-safe-commit.py "Commit message" file1.md file2.md
```

---

## 🧪 Skills Management

### ClawdHub (Skills Marketplace)

```bash
# Search for skills
clawdhub search "topic"

# Install skill
clawdhub install "skill-name"

# Update skill
clawdhub update "skill-name"

# Publish skill
clawdhub publish ./path/to/skill
```

### Skill Usage

Each skill has its own interface. See skill's SKILL.md for details.

**Common skills:**
- **coolify** - Manage Coolify deployments
- **context7** - Codebase Q&A
- **hn** - Browse Hacker News
- **playwright** - Browser automation
- **ripgrep** - Fast search
- **exa** - Neural web search

---

## 📊 System Status

### Check System Status

```bash
# System status (quick)
python scripts/system-status.py --brief

# System status (full dashboard)
python scripts/system-status.py

# System status (JSON)
python scripts/system-status.py --json
```

### Tool Testing

```bash
# Run all tool tests
python scripts/tool-tester.py

# Auto-fix issues
python scripts/tool-tester.py --fix
```

### Memory Health

```bash
# Check memory health
python scripts/memory-health.py

# Score only
python scripts/memory-health.py --score
```

---

## 🔧 Development Workflow

### Startup Routine

```bash
# Full startup
python scripts/startup.py

# Quick summary
python scripts/startup.py --quick
```

### Session Context

Always start with context:
1. HEARTBEAT.md - Current state and priorities
2. memory/YYYY-MM-DD.md - What was I working on
3. Constitution check - Core principles reminder
4. Relevant memories - Context for task

### Memory Search Before Answering

**Rule:** Use `memory_search` before answering questions about prior work.

```bash
memory_search "topic" --maxResults 5
```

Then use `memory_get` to pull specific lines from relevant files.

---

## 📋 Cross-References

For detailed information on specific topics:

| Topic | File |
|--------|-------|
| Identity and values | BEING.md |
| Session startup procedures | AGENTS-STARTUP.md |
| Complete tool catalog | AGENTS-TOOLS.md |
| Self-improvement framework | GROWTH-FRAMEWORK.md |
| Tool documentation | TOOLS.md |
| Skill usage | SKILLS.md |
| Workflow decisions | WORKFLOW.md |
| Factory configuration | /home/opc/.clawdbot/AGENTS.md |

---

## 💡 Best Practices

### File Operations
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

*This file contains procedures and tool patterns. For identity and growth, see BEING.md.*

🦞
