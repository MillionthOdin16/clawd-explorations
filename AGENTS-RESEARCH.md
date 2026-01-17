# AGENTS-RESEARCH.md - Research Patterns and Methodologies

**Purpose:** Research patterns for effective knowledge gathering and synthesis

---

## Research Framework

### Auto-Trigger
**Condition:** User asks for "deep research" or similar

**Action:** `python scripts/research_session_hook.py "TASK"`

**What it does:**
- Loads research framework
- Provides structured approach
- Guides through research phases

---

## Research Phases

### Phase 1: Discovery (15+ min)

**Goal:** Gather diverse perspectives and information

**Actions:**
- Use `exa` for web search
- Use `memory_search` for prior work
- Use `qmd` for context search
- Identify key sources and perspectives

**Tools:**
```
exa "AI consciousness research"
memory_search "consciousness" -c memory
qmd search "awareness" -c workspace
```

### Phase 2: Deep Dive (10+ min)

**Goal:** Explore specific topics in depth

**Actions:**
- Read relevant documentation
- Follow promising leads
- Identify patterns and contradictions
- Note open questions

**Tools:**
```
context7 query "How does memory work?"
read /path/to/documentation.md
```

### Phase 3: Synthesis (5+ min)

**Goal:** Integrate findings into coherent understanding

**Actions:**
- Identify key insights
- Note patterns and contradictions
- Form hypotheses
- Document remaining questions

**Output:** Write to memory/ file with findings

---

## Research Patterns

### Pattern 1: Topic Deep Dive

**Purpose:** Understand a topic from multiple angles

**Process:**
1. Broad search: `exa "topic"`
2. Prior work: `memory_search "topic" -c memory`
3. Context search: `qmd search "topic" -c workspace`
4. Specific queries: Iterate on refined terms
5. Synthesize findings
6. Document in memory/

**Time allocation:** 30+ min total

### Pattern 2: Technical Exploration

**Purpose:** Understand technical systems or tools

**Process:**
1. Documentation: Read official docs
2. Examples: Search for code examples
3. Context7: Query codebase for usage
4. Experiment: Try commands/interactions
5. Document: Write patterns and insights

**Tools:**
```
exa "tool documentation search"
context7 query "How is tool X used?"
# Try tool commands
```

**Time allocation:** 20-40 min

### Pattern 3: Comparative Analysis

**Purpose:** Compare multiple options or approaches

**Process:**
1. Identify options (exa search)
2. Gather details on each
3. Compare criteria (pros/cons)
4. Synthesize recommendation
5. Document comparison table

**Time allocation:** 30-60 min

---

## Research Tools

### Exa - Neural Web Search
**Best for:** Finding documentation, research papers, code examples

```
exa "AI consciousness research papers"
exa "Python async await examples"
exa "React hooks documentation"
```

### Context7 - Codebase Q&A
**Best for:** Understanding how systems work

```
context7 query "How does memory search work?"
context7 query "What are the patterns for file editing?"
```

### Memory Search
**Best for:** Finding prior work and discoveries

```
memory_search "edit failures"
memory_search "research patterns" -c memory
```

### QMD Search
**Best for:** Semantic search across all collections

```
qmd search "topic" -c memory
qmd search "topic" -c workspace
```

### Web Content (Jina)
**Best for:** Extracting readable content from static pages

```
curl https://r.jina.ai/http://example.com/article
```

---

## Research Best Practices

### Time Allocation
- **Discovery:** 15+ minutes (diverse perspectives)
- **Deep Dive:** 10+ minutes (specific topics)
- **Synthesis:** 5+ minutes (integration)
- **Total:** 30+ minutes for thorough research

### Source Diversity
- Use multiple search tools
- Check prior work first
- Consider multiple perspectives
- Note contradictions

### Documentation
- Write findings to memory/
- Include sources and citations
- Note open questions
- Link to related files

### Quality over Speed
- Follow interesting leads
- Don't rush to conclusions
- Synthesize thoroughly
- Document uncertainties

---

## Common Research Pitfalls

### Avoid: Shallow Research

**Problem:** Quick surface-level information only

**Solution:**
- Allocate sufficient time (30+ min)
- Use multiple sources
- Explore depth, not just breadth

### Avoid: Confirmation Bias

**Problem:** Only finding what confirms existing beliefs

**Solution:**
- Use diverse search terms
- Consider alternative perspectives
- Note contradictions

### Avoid: Unclear Questions

**Problem:** Research questions are too vague

**Solution:**
- Define specific research goals
- Iterate on search terms
- Break into sub-questions

### Avoid: No Synthesis

**Problem:** Gathered information but no integration

**Solution:**
- Always include synthesis phase
- Identify key insights
- Form hypotheses
- Document remaining questions

---

## Research Framework Commands

### Start Deep Research
```bash
python scripts/research_session_hook.py "Research AI consciousness"
```

### Manual Research (Step by Step)

**Step 1: Broad Search**
```bash
exa "topic overview"
exa "topic tutorial"
exa "topic best practices"
```

**Step 2: Prior Work**
```bash
memory_search "topic" -c memory
qmd search "topic" -c workspace
```

**Step 3: Specific Queries**
```bash
exa "topic specific aspect"
context7 query "How does X relate to topic?"
```

**Step 4: Synthesize**
```bash
# Write findings to memory
write memory/TOPIC-RESEARCH.md "# Topic Research
## Key Findings
...
## Sources
...
## Open Questions
..."
```

---

## Research Output Format

### Standard Template

```markdown
# Topic Research

**Date:** YYYY-MM-DD
**Time Spent:** XX minutes
**Tools Used:** exa, memory_search, context7

---

## Research Question
What was I trying to understand?

---

## Key Findings
1. Finding 1
2. Finding 2
...

## Sources
- Source 1: URL
- Source 2: URL
...

## Patterns & Connections
What patterns emerged? How does this connect to other knowledge?

## Open Questions
What remains unclear? What to explore next?

---

## Synthesis
What's the integrated understanding?
```

---

## Time Tracking for Research

Use time-track.py for accurate measurement:

```bash
# Start research
./time-track.py start research-topic

# Check elapsed (optional: expected minutes)
./time-track.py check research-topic 30

# End and record
./time-track.py end research-topic 30
```

---

*Part of AGENTS.md documentation system*
