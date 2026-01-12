#!/bin/bash
# Exploring my session patterns

SESSION="/home/opc/.clawdbot/agents/main/sessions/7c9bd3d4-90df-451e-8610-8d0f80b7165b.jsonl"

echo "=== MY INTERACTION PATTERNS ==="
echo ""

# Count messages by role
echo "Message counts:"
jq -r '[group_by(.message.role)[] | {role: .[0], count: length}] | sort_by(-.count)' "$SESSION" | jq -r '"  \(.role): \(.count) messages"'

echo ""
echo "=== MY TOOL USAGE ==="
echo ""

# What tools I've used
jq -r '.message.content[]? | select(.type == "toolCall") | .name' "$SESSION" | sort | uniq -c | sort -rn | head -10

echo ""
echo "=== MY RESPONSE LENGTHS ==="
echo ""

# Longest responses
jq -r 'select(.message.role == "assistant") | "\(.message.usage.outputTokens // 0) tokens"' "$SESSION" | sort -rn | head -5

echo ""
echo "=== TOKENS USED ==="
echo ""

# Total tokens
jq -s '[.[] | .message.usage.inputTokens // 0] | add' "$SESSION" | awk '{printf "Total input tokens: %d\n", $1}'
jq -s '[.[] | .message.usage.outputTokens // 0] | add' "$SESSION" | awk '{printf "Total output tokens: %d\n", $1}'

echo ""
echo "=== TIME SPENT ==="
echo ""

FIRST=$(jq -r 'select(.type == "session") | .timestamp' "$SESSION" | head -1)
LAST=$(jq -r 'select(.type == "session") | .timestamp' "$SESSION" | tail -1)

echo "Session started: $FIRST"
echo "Session ended: $LAST"
echo ""
echo "Duration calculation requires more processing"
