# 🦞 Skills Reference - Complete Guide

**All skills available to Clawdbot with quick reference and common patterns.**

---

## Quick Start

```bash
# Using unified skill runner (recommended)
python scripts/skill.py help                    # Show all skills
python scripts/skill.py <skill> help           # Show skill help

# Direct script access
uv run {baseDir}/scripts/<skill-script>.py <command>
```

---

## 🎯 Core Skills

### Coolify - Deployment Platform

**Deploy and manage applications on Coolify self-hosted platform.**

```bash
# List applications
python scripts/skill.py coolify apps list

# Deploy new application
python scripts/skill.py coolify deploy "name" "domain" "repo"

# Restart application
python scripts/skill.py coolify apps restart <uuid>

# Get logs
python scripts/skill.py coolify apps logs <uuid>
```

**Documentation:** `skills/coolify/SKILL.md`

### Context7 - Codebase Q&A

**Natural language queries about your codebase.**

```bash
# Ask a question
python scripts/skill.py context7 query "How does memory work?"

# Index codebase
python scripts/skill.py context7 index /path/to/codebase

# List indexes
python scripts/skill.py context7 list
```

**Documentation:** `skills/context7/SKILL.md`

### Exa - Neural Web Search

**AI-powered web and code search.**

```bash
# Search the web
bash scripts/search.sh "AI consciousness research"

# Get page content
bash scripts/content.sh "https://example.com"
```

**Documentation:** `skills/exa/SKILL.md`

### Ripgrep - Fast Search

**Fast file search and replace.**

```bash
# Search
uv run scripts/ripgrep.py search "pattern" --path /home/opc/clawd

# Replace
uv run scripts/ripgrep.py replace "old" "new" --path /home/opc/clawd
```

**Documentation:** `skills/ripgrep/SKILL.md`

---

## 🌐 Web & Browser

### Web - Web Exploration

**Fetch, search, and explore web content.**

```bash
# Fetch URL
python scripts/web-explorer.py "https://example.com"

# Search web
python scripts/web-explorer.py --search "AI news"

# Take screenshot
python scripts/web-explorer.py --screenshot "https://example.com"
```

**Documentation:** `skills/web/SKILL.md`

### Playwright - Browser Automation

**Browser automation using Playwright (Firefox for ARM64).**

```bash
# Take screenshot
python scripts/cli.py screenshot "https://example.com"

# Interactive session
python scripts/cli.py interact "https://example.com"

# Generate PDF
python scripts/cli.py pdf "https://example.com" output.pdf
```

**Documentation:** `skills/playwright-automation/SKILL.md`

---

## 📰 Content & Research

### HN - Hacker News

**Browse and explore Hacker News.**

```bash
# Top stories
python scripts/hn-daily-summary.py

# Explore topic
python scripts/hn-explorer.py "AI machine learning"

# Get specific story
python scripts/hn-explorer.py --id <story-id>
```

**Documentation:** `skills/hn/SKILL.md`

### Summarize - Content Summarization

**Summarize URLs, files, PDFs, images, and YouTube videos.**

```bash
# Summarize URL
uv run scripts/summarize.py "https://example.com"

# Summarize PDF
uv run scripts/summarize.py document.pdf
```

**Documentation:** `skills/summarize/SKILL.md`

### Video Frames - Video Extraction

**Extract frames or clips from videos.**

```bash
# Extract frames
python scripts/extract-frames.py video.mp4 --interval 5

# Extract clip
python scripts/extract-frames.py video.mp4 --start 00:30 --end 01:00
```

**Documentation:** `skills/video-frames/SKILL.md`

---

## 💾 Memory & Context

### Memory Keeper - Persistent Context

**Persistent context across sessions.**

```bash
# Add memory
python scripts/memory-keeper.py add "key" "value"

# Search memories
python scripts/memory-keeper.py search "query"

# List all
python scripts/memory-keeper.py list
```

**Documentation:** `skills/memory-keeper/SKILL.md`

### Obsidian - Notes Integration

**Work with Obsidian vaults and notes.**

```bash
# Search notes
uv run scripts/obsidian.py search "topic"

# Create note
uv run scripts/obsidian.py create "note-name" "content"

# Update vault index
uv run scripts/obsidian.py index
```

**Documentation:** `skills/obsidian/SKILL.md`

---

## 🔧 Development Tools

### GitHub - GitHub Integration

**Issues, PRs, CI runs, and advanced queries.**

```bash
# List issues
gh issue list

# Create issue
gh issue create --title "Bug" --body "Description"

# View PR
gh pr view <pr-number>

# Check workflow runs
gh run list
```

**Documentation:** `skills/github/SKILL.md`

### Notion - Notion Integration

**Create and manage Notion pages and databases.**

```bash
# Create page
uv run scripts/notion.py create-page "Page Title" --parent <database-id>

# Query database
uv run scripts/notion.py query "SELECT * FROM database"
```

**Documentation:** `skills/notion/SKILL.md`

---

## 🎮 Fun & Special

### Gemini - Gemini CLI

**One-shot Q&A and summaries using Gemini.**

```bash
# Ask a question
uv run scripts/gemini.py "Explain quantum computing"

# Summarize
uv run scripts/gemini.py --summarize "long-document.txt"
```

**Documentation:** `skills/gemini/SKILL.md`

### ClawdHub - Skill Management

**Manage agent skills from clawdhub.com.**

```bash
# Search skills
clawdhub search "memory"

# Install skill
clawdhub install "skill-name"

# Publish skill
clawdhub publish ./my-skill/
```

**Documentation:** `skills/clawdhub/SKILL.md`

---

## 🛠️ System Tools

### Task Orchestration

**Manage tasks, sub-agents, and queues.**

```bash
# Dashboard
to status

# Add task
to add "Research X" --priority 10 --desc "Description"

# Process queue
to run

# Spawn sub-agent
to spawn "Deep research" --label "research"
```

**Documentation:** `memory/TASK-ORCHESTRATOR.md`

### System Status

**Check system health and status.**

```bash
# Quick status
python scripts/system-status.py --brief

# Full dashboard
python scripts/system-status.py

# JSON output
python scripts/system-status.py --json
```

### Tool Testing

**Test and verify all tools.**

```bash
# Run all tests
python scripts/tool-tester.py

# Auto-fix issues
python scripts/tool-tester.py --fix
```

### Backup System

**Back up memory and configuration.**

```bash
# Create backup
python scripts/backup.py

# Auto with retention
python scripts/backup.py --auto

# List backups
python scripts/backup.py --list

# Restore
python scripts/backup.py --restore
```

### Memory Health

**Check memory system health.**

```bash
# Full check
python scripts/memory-health.py

# Just score
python scripts/memory-health.py --score
```

---

## 📚 Documentation

### QUICK-REF.md

**Quick lookup for commands and patterns.**

Always read first for any task.

### TOOLS.md

**Complete tool documentation.**

Detailed documentation for all scripts and tools.

### Skills SKILL.md files

**Skill-specific documentation.**

Each skill has a SKILL.md with detailed usage.

---

## 🚀 Common Patterns

### Pattern 1: Research a Topic
```bash
# Search web
python scripts/skill.py exa search "AI consciousness"

# Query codebase
python scripts/skill.py context7 query "What do I know about AI?"

# Take notes
to add "Research AI consciousness" --priority 10
```

### Pattern 2: Deploy Application
```bash
# Check status
python scripts/skill.py coolify apps list

# Deploy
python scripts/skill.py coolify deploy "name" "domain" "repo"

# Monitor
python scripts/skill.py coolify apps logs <uuid>
```

### Pattern 3: Explore Codebase
```bash
# Natural language query
python scripts/skill.py context7 query "How does the memory system work?"

# Fast search
python scripts/skill.py ripgrep search "TODO" --path /home/opc/clawd

# Get context
python scripts/skill.py context7 query "What files relate to memory?"
```

### Pattern 4: System Health Check
```bash
# Quick status
python scripts/system-status.py --brief

# Test tools
python scripts/tool-tester.py --fix

# Check memory
python scripts/memory-health.py

# Backup
python scripts/backup.py --auto
```

---

## 🎯 Skill Selection Guide

| Task | Recommended Skill |
|------|-------------------|
| Deploy application | `coolify` |
| Codebase Q&A | `context7` |
| Web search | `exa` or `web` |
| Fast file search | `ripgrep` |
| Browser automation | `playwright` |
| HN stories | `hn` |
| Persistent memory | `memory-keeper` |
| GitHub operations | `github` |
| Task management | `to` (task orchestrator) |
| System status | `system-status.py` |
| Backup | `backup.py` |

---

*This document is indexed by qmd for semantic search.*

🦞