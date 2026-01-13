# 🦞 Clawd Workspace Codebase

**Last Updated:** 2026-01-13 15:55 UTC  
**Purpose:** Quick reference for understanding this AI agent workspace

---

## Project Structure

```
/home/opc/clawd/
├── AGENTS.md          # Operating instructions (13KB)
├── SOUL.md            # Persona & tone (234 bytes)
├── USER.md            # User preferences (160 bytes)
├── IDENTITY.md        # Agent identity (lobster, helpful, direct)
├── HEARTBEAT.md       # Current status & recent activity
├── memory/            # Knowledge base (12+ files)
│   ├── INDEX.md       # Quick lookup reference
│   ├── DISCOVERIES.md # What I've learned
│   ├── CAPABILITIES.md # What I can do
│   ├── PATTERNS.md    # Observed patterns
│   ├── LESSONS.md     # Failure recovery
│   ├── PREFERENCES.md # What I like
│   ├── COMMITMENTS.md # My promises
│   ├── HIGH-IMPACT-TOOLS.md # CLI tools research
│   ├── WORKFLOW.md    # Tool decisions
│   ├── MCP-SERVERS-RESEARCH.md # MCP servers
│   └── ...
├── skills/            # Available skills
│   ├── coolify/       # Deployment platform
│   ├── playwright-automation/ # Browser automation
│   ├── ripgrep/       # Fast search
│   ├── context7/      # Codebase Q&A (NEW)
│   └── memory-keeper/ # Persistent context (NEW)
└── archive/           # Old/archived files
```

---

## Key Files

### Core Configuration
| File | Purpose |
|------|---------|
| `AGENTS.md` | Operating instructions, rules, patterns |
| `SOUL.md` | Persona: Clawd the lobster, helpful & direct |
| `USER.md` | Bradley's preferences (EST timezone, engineer) |
| `IDENTITY.md` | Character traits, boundaries, safety rules |

### Memory System
| File | Purpose |
|------|---------|
| `INDEX.md` | Quick lookup - Before X, read Y |
| `DISCOVERIES.md` | Self-understanding, what I've learned |
| `CAPABILITIES.md` | Tools, skills, integrations available |
| `PATTERNS.md` | Observed patterns in work |
| `LESSONS.md` | Failure recovery procedures |

---

## Tools & Skills

### Installed CLI Tools
| Tool | Purpose | Stars |
|------|---------|-------|
| **fzf** | Fuzzy finder | 76k |
| **ripgrep** | Fast search | 58k |
| **bat** | Better cat | 56k |
| **fd** | Better find | 41k |
| **lazygit** | Git UI | 70k |
| **zoxide** | Smart cd | 32k |
| **eza** | Modern ls | 19k |

### Skills Available
| Skill | Purpose |
|-------|---------|
| **coolify** | Deploy apps to Coolify |
| **playwright-automation** | Browser automation (Firefox) |
| **ripgrep** | Fast content search |
| **context7** | Codebase Q&A (requires Upstash) |
| **memory-keeper** | Persistent context |
| **qmd** | Local semantic search |
| **github** | GitHub CLI integration |
| **hn** | Hacker News reader |

---

## Search System (qmd)

**Collections indexed:**
```
memory/       → 12 markdown files
sessions/     → 13 session JSONL files  
workspace/    → 24 markdown files

Total: 49 files, 2592 embeddings
```

**Commands:**
```bash
qmd search "query"           # BM25 keyword search
qmd vsearch "query"          # Vector similarity
qmd query "question"         # Hybrid (best for Q&A)
qmd update --pull            # Re-index with git pull
```

---

## Architecture Decisions

### Why This Structure?

1. **Memory Files** - Human-readable, git-versioned, easily searchable
2. **qmd for Search** - BM25 + vectors for both keyword and semantic search
3. **Skills Pattern** - Modular, each skill is self-contained
4. **Progressive Disclosure** - INDEX → WORKFLOW → HIGH-IMPACT-TOOLS (three levels)

### CI/CD Integration

- **GitHub** for version control
- **Coolify** for deployments
- **Playwright** for browser testing

---

## Common Workflows

### Research a Topic
```bash
qmd query "multi-agent patterns"
# or
rg "pattern" --type md
```

### Deploy an App
```bash
uv run skills/coolify/scripts/coolify.py deploy "name" "fqdn" "repo"
```

### Browse Hacker News
```bash
uv run skills/hn/scripts/hn.py top 10
```

### Add New Memory
```bash
# Write to memory/ folder
write memory/NEW-DISCOVERY.md "# New Discovery..."
# Then index
qmd update
```

---

## Known Issues / Technical Debt

1. **ARM64 Limitation** - Chrome not available, use Playwright/Firefox
2. **No Native MCP** - MCP servers CLI-only, not integrated as tools
3. **Context7 Setup** - Requires Upstash Redis credentials

---

## API Endpoints

### Coolify (Deployed Apps)
- **API:** https://coolify.bradarr.com/api/v1
- **Token:** Stored in `~/.env.secrets`
- **Project:** Clawd Workspace (jws4w4cc040444gk0ok0ksgk)

### GitHub
- **CLI:** `gh` command available
- **Skills:** github skill for PRs, issues, repos

---

## Development Notes

### Adding a New Skill
1. Create `/home/opc/clawd/skills/skillname/`
2. Add `SKILL.md` with documentation
3. Add `scripts/skill.py` CLI wrapper
4. Update `memory/INDEX.md` reference

### Updating Memory
1. `read` existing memory file
2. `edit` or `write` changes
3. Commit to git
4. `qmd update --pull` to re-index

---

## References

- **Full Documentation:** See `memory/INDEX.md`
- **Tool Workflow:** See `memory/WORKFLOW.md`
- **CLI Tools:** See `memory/HIGH-IMPACT-TOOLS.md`
- **qmd Usage:** See `memory/QMD-WORKFLOW.md`

---

*This file is indexed by qmd for semantic search*
