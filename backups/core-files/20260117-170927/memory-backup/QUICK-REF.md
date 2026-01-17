# Quick Reference Card

**Optimized for Clawdbot usage patterns**

---

## 🚀 Ultra-Short Aliases (NEW!)

| Task | Command | Example |
|------|---------|---------|
| File edit | `fe` | `fe line path 15 "new"` |
| Wait for | `wf` | `wf http://localhost:3000 --timeout 30` |
| API call | `api` | `api GET http://api.example.com` |

---

## 📝 File Editing (fe)

| Task | Command |
|------|---------|
| Read | `fe read path [--start N] [--end N]` |
| Edit line | `fe line path N "content"` |
| Edit text | `fe text path "old" "new" [--fuzzy]` |
| Edit range | `fe range path S E "new"` |
| Verify | `fe verify path1 path2` |
| Hash | `fe hash path` |

**Examples:**
```bash
fe read path.md --start 10 --end 20
fe line path.md 15 "new content"
fe text path.md "old" "new" --fuzzy
fe verify a.txt b.txt
```

---

## ⏳ Wait For (wf)

```bash
wf <url|port> [--timeout N] [--contains TEXT]

# Examples:
wf http://localhost:3000              # Wait for URL
wf 3000 --timeout 30                  # Wait for port
wf http://localhost/api --contains ok # Wait for content
```

**Output:** `OK:url` or `FAIL:url:reason`

---

## 🌐 API Call (api)

```bash
api <method> <url> [--data JSON] [--header "K:V"]

# Examples:
api GET http://api.example.com/data
api POST http://api.example.com --data '{"a":1}'
api GET https://api.example.com --header "Auth:Bearer token"
```

**Output:** Response body or `ERROR:message`

---

## 🔍 Search (qmd - PRIMARY)

```bash
qmd search "pattern" -c memory          # Search memories
qmd search "pattern" -c workspace       # Search workspace
qmd search "pattern" -c sessions        # Search history
qmd get path/to/file.md:5 -l 20         # Get context
```

---

## 🤖 Sub-Agents

| Need | Command |
|------|---------|
| Dashboard | `python task-orchestrator.py status` |
| Spawn | `sessions_spawn(task="...", agentId="researcher")` |
| Queue | `python task-orchestrator.py queue add "Task"` |
| Run queue | `python task-orchestrator.py queue run --max 4` |

---

## 📁 Tool Locations

| Tool | Path |
|------|------|
| File edit | `/home/opc/clawd/scripts/fe.py` |
| Wait for | `/home/opc/clawd/scripts/wf.sh` |
| API call | `/home/opc/clawd/scripts/api.sh` |
| Task orchestrator | `/home/opc/clawd/scripts/task-orchestrator.py` |
| Sub-agents | `/home/opc/clawd/SUBAGENTS.md` |

---

**Full docs:** `TOOLS.md` | **Research:** `SUBAGENTS.md`
