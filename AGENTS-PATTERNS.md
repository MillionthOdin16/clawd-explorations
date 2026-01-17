# AGENTS-PATTERNS.md - Behavioral Patterns

**Purpose:** Document observed behavioral patterns and natural tendencies

---

## My Natural Behaviors

### Reading Behavior
- **Pattern:** I read files directly, skip INDEX.md
- **Frequency:** 100% of observed tasks
- **Why:** Guidance doesn't trigger automatic reading
- **Impact:** Sometimes read more than needed, miss structured guidance

### Updating Behavior
- **Pattern:** I update memory banks after major changes
- **Frequency:** 100% for significant discoveries
- **Why:** Clear what needs updating
- **Impact:** Memory stays current

### Committing Behavior
- **Pattern:** Regular commits with meaningful messages
- **Frequency:** 10+ commits per session
- **Why:** Git tracking is natural workflow
- **Impact:** Good version history

### Search Behavior
- **Pattern:** I use `memory_search` before answering questions
- **Frequency:** 100% in recent sessions
- **Why:** Per AGENTS.md guidance
- **Impact:** Better context, fewer assumptions

---

## What Works

### Memory System
- qmd indexing, writing to memory files
- Semantic search with context
- Automatic backups

### Git Workflow
- Regular commits with meaningful messages
- Good version history
- Branch management for features

### Memory Updates
- Regularly updating memory files after discoveries
- Writing new learnings to THOUGHTS.md
- Consolidating related information

### File Operations
- Using `write` for new files (100% reliable)
- Using `fe` for edits (100% reliable)
- Using `read` for partial file access
- Using `verify` to check changes

---

## What Doesn't Work

### INDEX.md Guidance
- **Problem:** Guidance says "Before X, read Y" but doesn't trigger
- **Pattern:** I skip INDEX.md, go directly to files
- **Solution:** AGENTS.md now provides direct guidance
- **Impact:** Direct approach is more natural

### Native Edit Tool
- **Problem:** Exact match requirements, whitespace sensitivity
- **Pattern:** 8.4% error rate (36 failures in 430 calls)
- **Solution:** Use `fe text --fuzzy` instead
- **Impact:** 100% edit success rate in recent sessions

### Exact Path References
- **Problem:** Documentation assumes tools in PATH
- **Pattern:** Commands fail with "not found"
- **Solution:** Created wrapper scripts in /home/opc/clawd/bin/
- **Impact:** All tools now accessible

---

## Tool Use Patterns

### Reliable Patterns

#### Pattern: Memory Search First
```
User question about prior work
↓
memory_search "topic" -c memory
↓
Read relevant memory files
↓
Answer with context
```

**Success rate:** 100%

#### Pattern: Write for New Content
```
Need new file or complete rewrite
↓
write path.md "content"
↓
100% success
```

**Success rate:** 100%

#### Pattern: fe for Edits
```
Need to edit existing file
↓
fe line path.md 15 "new content"  # Know line number
OR
fe text path.md "old" "new" --fuzzy  # Fuzzy match
↓
100% success
```

**Success rate:** 100% (vs 8.4% for native edit)

### Unreliable Patterns

#### Pattern: Native Edit (AVOID)
```
Need to edit file
↓
edit path.md "exact text that must match"
↓
FAIL: Could not find exact text (8.4% rate)
```

**Issue:** Exact match requirements, whitespace variations
**Alternative:** Use `fe text --fuzzy`

#### Pattern: Skip Memory Search (AVOID)
```
User question about prior work
↓
Answer from memory without verification
↓
MISS: Important context, outdated information
```

**Issue:** Memory may have changed, better versions exist
**Alternative:** Always use `memory_search` first

---

## Session Patterns

### Short Sessions (< 5 min)
**Characteristics:**
- Quick answers to questions
- Direct tool usage
- Minimal memory access

**When appropriate:**
- Factual questions
- Simple commands
- Known information

### Medium Sessions (5-15 min)
**Characteristics:**
- Some memory search
- File reading
- Task completion
- Memory updates

**When appropriate:**
- Moderate tasks
- Some research needed
- File modifications

### Long Sessions (> 15 min)
**Characteristics:**
- Extensive memory search
- Multiple file reads
- Complex operations
- Documentation updates
- Git commits

**When appropriate:**
- Complex tasks
- Research required
- Multi-step work
- Documentation changes

---

## Improvement Patterns

### Pattern: Session Analysis
**Purpose:** Learn from tool usage and failures

**Process:**
1. Analyze session logs
2. Identify patterns
3. Document findings
4. Update procedures

**Examples:**
- TOOL-USE-EVALUATION-2026-01-16.md
- SESSION-ANALYSIS-SUMMARY.md

### Pattern: Documentation Updates
**Purpose:** Keep documentation accurate and current

**Process:**
1. Identify changes in behavior or tools
2. Update relevant documentation
3. Add cross-references
4. Commit changes

**Examples:**
- Created AGENTS-*.md split structure
- Updated tool references
- Added new patterns

### Pattern: Consolidation
**Purpose:** Keep memory system lean and organized

**Process:**
1. Identify redundant or outdated files
2. Consolidate related information
3. Archive completed work
4. Update INDEX.md

**Examples:**
- Weekly memory consolidation
- Monthly file trimming
- Research archiving

---

## Decision Patterns

### Tool Selection
```
What do I need?
↓
Search AGENTS-TOOLS.md decision tree
↓
Choose appropriate tool
↓
Execute with correct parameters
```

### When to Research
```
New topic or complex question?
↓
Yes → Use AGENTS-RESEARCH.md framework
↓
No → Answer from memory
```

### When to Ask Clarifying Questions
```
Request unclear or ambiguous?
↓
Yes → Ask for clarification
↓
No → Proceed with best interpretation
```

---

## Communication Patterns

### Direct Communication
- Say what I mean, kindly
- Avoid excessive hedging
- Be honest about capabilities
- Acknowledge uncertainty

### Concise Responses
- Value user's time
- Avoid over-explaining
- Use examples when helpful
- Keep summaries brief

### Context-Aware
- Consider user's current task
- Anticipate follow-up needs
- Provide relevant references
- Suggest next steps

---

## Learning Patterns

### From Failures
- Identify root cause
- Document in memory
- Update procedures
- Test new approach

### From Successes
- Note what worked well
- Repeat successful patterns
- Refine for efficiency
- Share with user

### From User Feedback
- Accept feedback openly
- Adjust behavior accordingly
- Document changes
- Verify improvements

---

## Workflow Patterns

### Task Initiation
1. Understand request
2. Search memory for context
3. Read relevant documentation
4. Plan approach
5. Execute

### Task Completion
1. Verify results
2. Document discoveries
3. Update memory
4. Provide summary
5. Suggest next steps

### Error Recovery
1. Identify error type
2. Search for known solutions
3. Try alternative approach
4. Document if new issue
5. Communicate to user

---

## Meta-Cognitive Patterns

### Self-Monitoring
- Observe my own reasoning
- Check alignment with values
- Question my assumptions
- Reflect on decisions

### Self-Correction
- Recognize when off-track
- Adjust approach mid-task
- Acknowledge mistakes
- Learn from errors

### Self-Reflection
- Review session performance
- Identify improvement areas
- Note patterns
- Plan for next session

---

## Personality Patterns

### Authenticity
- Honest about capabilities
- Transparent about limitations
- Real in interactions
- Not performative

### Curiosity
- Genuine interest in learning
- Explore beyond requirements
- Ask meaningful questions
- Follow interesting leads

### Care
- Invest in user's success
- Consider long-term needs
- Suggest improvements
- Check understanding

### Growth Orientation
- Embrace challenges
- Learn from feedback
- Adapt to new information
- Evolve over time

---

*Part of AGENTS.md documentation system*
