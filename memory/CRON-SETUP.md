# Cron Job Setup - Document Refinement

## To Add This Cron Job

The cron job requires the Clawdbot CLI. Run:

```bash
# Add cron job (run weekly on Sunday at 8pm UTC)
clawdbot cron add \
  --name "Document Refinement - Weekly" \
  --cron "0 20 * * 0" \
  --session "main" \
  --system-event "document_refinement" \
  --message "🔄 Starting document refinement task..."
```

Or use the Gateway API directly if you have access.

---

## What the Cron Job Should Do

**Trigger:** Weekly (Sunday 8pm UTC)

**Action:**
1. Send notification to Bradley
2. Spawn an isolated session to execute the refinement task
3. Write results to `memory/CRON-DOCUMENT-REFINEMENT-RESULTS.md`
4. Send completion summary

**The task prompt is in:** `memory/CRON-DOCUMENT-REFINEMENT-PROMPT.md`

---

## Manual Execution (If Cron Isn't Working)

You can trigger the task anytime:

```bash
clawdbot sessions spawn \
  --agent "default" \
  --task "Execute the document refinement task from memory/CRON-DOCUMENT-REFINEMENT-PROMPT.md. Read the prompt, follow all 9 steps, write results to memory/CRON-RESULTS.md, then notify Bradley of completion." \
  --label "document-refinement" \
  --cleanup "delete"
```

---

## Cron Job Schedule

| Field | Value | Meaning |
|-------|-------|---------|
| Minute | 0 | At XX:00 |
| Hour | 20 | 8 PM |
| Day of Month | * | Any day |
| Month | * | Any month |
| Day of Week | 0 | Sunday only |

**In EST:** 8pm UTC = 3pm EST (8pm - 5h = 3pm)

---

## Files Involved

| File | Purpose |
|------|---------|
| `CRON-DOCUMENT-REFINEMENT-PROMPT.md` | Task instructions |
| `CRON-SETUP.md` | This setup guide |
| `CRON-RESULTS.md` | Output (created after first run) |

---

**Prompt reference:** `memory/CRON-DOCUMENT-REFINEMENT-PROMPT.md`
