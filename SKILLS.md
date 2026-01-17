# 🦞 Skills Reference - Complete Guide

**All skills available to Clawdbot with quick reference and common patterns.**

---

## Skills Directory Structure

Clawdbot has two skills directories:

| Directory | Purpose | Skills |
|-----------|---------|---------|
| `/home/opc/clawdbot/skills/` | **PRIMARY** - Production skills | 47 skills |
| `/home/opc/clawd/skills/` | Workspace - Development/testing | 10 skills |

**Important:** Use `/home/opc/clawdbot/skills/` as the primary source. The workspace directory is for developing new skills before merging into the system directory.

---

## Quick Start

```bash
# Using unified skill runner (recommended)
python scripts/skill.py help                    # Show all skills
python scripts/skill.py <skill> help            # Show skill help

# Direct script access
python skills/<skill>/scripts/<skill>.py <command>
```

---

## 🎯 Available Skills

### Coolify - Deployment Platform

**Deploy and manage applications on Coolify self-hosted platform.**

```bash
# Quick status
python scripts/skill.py coolify status

# List applications
python scripts/skill.py coolify apps list

# Get application details
python scripts/skill.py coolify apps get --uuid <uuid>

# Deploy application
python scripts/skill.py coolify apps deploy --uuid <uuid>

# Get logs
python scripts/skill.py coolify apps logs --uuid <uuid>

# List projects/servers
python scripts/skill.py coolify projects list
python scripts/skill.py coolify servers list
```

**Documentation:** `skills/coolify/SKILL.md`

### Context7 - Codebase Q&A

**Natural language queries about your codebase using Upstash Redis.**

```bash
# Ask a question
python scripts/skill.py context7 query "How does memory work?"

# Force re-indexing
python scripts/skill.py context7 index /path/to/codebase

# List indexes
python scripts/skill.py context7 list
```

**Documentation:** `skills/context7/SKILL.md`

### Exa - Neural Web Search

**AI-powered web and code search.**

```bash
# Search the web
python scripts/skill.py exa search "AI consciousness research"

# Get page content
python scripts/skill.py exa content "https://example.com"
```

**Documentation:** `skills/exa/SKILL.md`

### Ripgrep - Fast Search

**Fast line-oriented search with recursive directory support.**

```bash
# Search for pattern
python scripts/skill.py ripgrep search "TODO" --type py

# List matching files
python scripts/skill.py ripgrep files "def main"

# Count occurrences
python scripts/skill.py ripgrep count "import "

# Find functions
python scripts/skill.py ripgrep find-funcs --type py

# Find classes
python scripts/skill.py ripgrep find-classes --type py
```

**Documentation:** `skills/ripgrep/SKILL.md`

### Hacker News

**Browse Hacker News from the command line.**

```bash
# Top stories
python scripts/skill.py hn top --limit 10

# New stories
python scripts/skill.py hn new --limit 5

# Best stories
python scripts/skill.py hn best --limit 5

# Ask HN
python scripts/skill.py hn ask --limit 5

# Show HN
python scripts/skill.py hn show --limit 5

# Jobs
python scripts/skill.py hn jobs --limit 5

# Get story details
python scripts/skill.py hn story <id>

# Search stories
python scripts/skill.py hn search "AI"
```

**Documentation:** `skills/hn/SKILL.md`

### Web Browsing

**Web browsing wrapper using Clawdbot's browser tool.**

```bash
# Open URL
python scripts/skill.py web open "https://example.com"

# Get page content
python scripts/skill.py web get "https://example.com"

# Get plain text
python scripts/skill.py web text "https://example.com"

# Search the web (DuckDuckGo)
python scripts/skill.py web search "Python AI"

# Take screenshot
python scripts/skill.py web screenshot "https://example.com" --output /tmp/page.png
```

**Documentation:** `skills/web/SKILL.md`

### Playwright - Browser Automation

**Browser automation using Playwright (Firefox-based for ARM64).**

```bash
# Take screenshot
python scripts/skill.py playwright screenshot "https://example.com"

# Interact with page
python scripts/skill.py playwright interact "https://example.com" --action click

# Generate PDF
python scripts/skill.py playwright pdf "https://example.com" --output /tmp/page.pdf
```

**Documentation:** `skills/playwright-automation/SKILL.md`

### Memory Keeper - Persistent Context

**Persistent context/memory management for AI sessions.**

```bash
# Add memory
python scripts/skill.py memory-keeper add "Research AI consciousness" --priority 10

# Search memories
python scripts/skill.py memory-keeper search "AI"

# List memories
python scripts/skill.py memory-keeper list

# Clear memories
python scripts/skill.py memory-keeper clear
```

**Documentation:** `skills/memory-keeper/SKILL.md`

---

## 🎯 Common Patterns

### Pattern 1: Research & Learn
```bash
# Web search
python scripts/skill.py exa search "AI consciousness research"

# Query codebase
python scripts/skill.py context7 query "What do I know about AI?"

# Take notes
to add "Research AI consciousness" --priority 10
```

### Pattern 2: Deploy Application
```bash
# Check status
python scripts/skill.py coolify status

# Deploy
python scripts/skill.py coolify apps deploy <uuid>

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

## 📁 Skill Structure

All skills follow this standard structure:

```
skills/<name>/
├── SKILL.md           # Documentation with frontmatter
└── scripts/
    └── <name>.py      # CLI script (or .sh for shell scripts)
```

### SKILL.md Frontmatter Format

```yaml
---
name: <skill-name>
description: <brief description>
homepage: <optional homepage URL>
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["VAR_NAME"]}}}
---
```

### CLI Script Requirements

- Accept `--help` for documentation
- Support common options: `--json`, `--quiet`
- Return proper exit codes
- Use argparse for argument parsing

---

## 🔧 Configuration

### Environment Variables

| Skill | Variable | Description |
|-------|----------|-------------|
| coolify | `COOLIFY_API_TOKEN` | API key for Coolify |
| exa | `EXA_API_KEY` | Exa AI API key |
| context7 | `CONTEXT7_API_KEY`, `UPSTASH_REST_API_TOKEN` | Redis connection |
| memory-keeper | `MEMORY_KEEPER_PATH` | Path to memory storage |

### Required Binaries

| Skill | Binary | Installation |
|-------|--------|--------------|
| ripgrep | `rg` | `brew install ripgrep` |
| hn | `curl` | Built-in |
| playwright | `python3`, `playwright` | `pip install playwright` |

---

*This document is indexed by qmd for semantic search.*

🦞
