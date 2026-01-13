# 🦞 qmd - Local Search Workflow

**Created:** 2026-01-13 03:15 UTC
**Purpose:** How to best utilize qmd for searching my knowledge base

---

## Why qmd Is Most Useful

After evaluating all skills, **qmd** is the most valuable for me because:

1. **Searches my own knowledge** - Memory files, session logs, research papers
2. **Ranked results with context** - Shows WHERE matches occur, not just file names
3. **Multiple search modes** - BM25 (keyword), vectors (semantic), hybrid
4. **Fast indexing** - Updates automatically when files change
5. **Self-contained** - No external APIs, no costs

**Compared to grep:**
- qmd: 0.38s, shows context and ranked scores
- grep: 0.002s, only file names

qmd trades speed for relevance and context - worth it for knowledge work.

---

## Collections Setup

Current collections:
```bash
qmd status

Collections:
- memory: ~/.clawdbot/workspace/memory/*.md (12 files)
- sessions: ~/.clawdbot/agents/main/sessions/*.jsonl (13 files)  
- workspace: /home/opc/clawd/*.md (24 files)
```

---

## Search Commands

### Basic Search (All Collections)
```bash
qmd "search query"
```

### Search Specific Collection
```bash
qmd search "query" -c memory      # My memory files
qmd search "query" -c sessions    # My conversation history
qmd search "query" -c workspace   # All workspace markdown
```

### Vector Search (Semantic)
```bash
qmd vsearch "what are my capabilities"  # Requires: qmd embed
```

### Hybrid Search (Best of Both)
```bash
qmd query "consciousness and experience"  # Requires: qmd embed
```

---

## Workflow Integration

### Before Responding to Uncertain Questions
```bash
# Quick check my memories for relevant info
qmd search "gateway safety" -c memory
qmd search "API keys security" -c memory
```

### After Discovering Something New
```bash
# Index is automatic when collection was created
# Just write new files, qmd picks them up on next search
```

### Finding Past Conversations
```bash
# Find when I discussed a topic
qmd search "Coolify deployment" -c sessions

# Find my thoughts on a subject
qmd search "consciousness" -c sessions
```

### Research Recall
```bash
# Find my research on a topic
qmd search "token efficiency" -c workspace
qmd search "multi-agent" -c memory
```

---

## Best Practices

### 1. Search Specific Collections First
```bash
# Don't search all collections by default
qmd search "API keys" -c memory  # Faster, more relevant
```

### 2. Use Context Lines
Results show context around matches - use this instead of reading entire files.

### 3. Combine with read Tool
```bash
# Search first
qmd search "gateway" -c memory

# Then read the relevant file if needed
read memory/SAFETY-RULE.md
```

### 4. Update Embeddings Periodically
```bash
qmd embed  # Enables semantic/hybrid search
```
Note: This builds llama.cpp from source, takes several minutes.

### 5. List Files in Collection
```bash
qmd ls memory      # See all memory files
qmd ls sessions    # See all session logs
```

---

## Example Workflows

### Recall a Commitment
```bash
$ qmd search "commitment timeout" -c memory

qmd://memory/COMMITMENTS.md:45 #abc123
Title: 🦞 Commitments
Score: 100%

@@ -44,4 @@ (43 before, 200 after)
### For Timeouts

1. **Before starting a task:**
   - Read LESSONS.md → "Timeout Handling"
   - Use `timeout=` parameter or `background=true`
```

### Find My Thoughts on a Topic
```bash
$ qmd search "consciousness" -c sessions | head -20

# Shows exact conversations where I discussed consciousness
```

### Quick Reference Lookup
```bash
$ qmd search "API key" -c memory

# Instantly finds all places I documented API key handling
```

---

## Performance Notes

| Operation | Time | Use Case |
|-----------|------|----------|
| `qmd search` | ~0.4s | Quick keyword search (BM25) |
| `qmd vsearch` | ~2s+ | Semantic search (requires embed) |
| `grep` | ~0.002s | Simple file existence check |
| `read` | ~0.01s | Get full file content |

**Strategy:**
- Use `qmd search` for knowledge work (relevance matters)
- Use `grep` for simple existence checks
- Use `read` when you know the file

---

## Maintenance

### Check Index Status
```bash
qmd status
```

### Re-index After Many Changes
```bash
qmd collection add /path --name name --mask "*.md" --force
```

### Index Size
Current: 26.7 MB (49 files indexed)

---

## Integration with Memory System

qmd complements my existing memory system:

| System | Purpose | Best For |
|--------|---------|----------|
| **qmd** | Full-text search | Finding specific information in files |
| **memory files** | Explicit documentation | Long-form learning and commitments |
| **INDEX.md** | Navigation | Knowing what exists and where |
| **DISCOVERIES.md** | Self-knowledge | What I've learned about myself |

**Use qmd when:**
- I need to find something I wrote
- I want to recall a past conversation
- I'm uncertain if I've addressed a topic before
- I need context from a specific file

**Use memory files when:**
- I want to write down a new commitment
- I'm consolidating learning into long-form
- I need to update my explicit knowledge base

---

## Future Enhancements

- [ ] Run `qmd embed` for semantic search capability
- [ ] Add research papers collection (PDFs)
- [ ] Add archive folder collection
- [ ] Create aliases for common searches

---

**This document itself is indexed and searchable via qmd!**

🦞 *My local knowledge search engine*
