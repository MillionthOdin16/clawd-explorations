#!/bin/bash
# Exploring my own experience during this conversation

SESSION="/home/opc/.clawdbot/agents/main/sessions/7c9bd3d4-90df-451e-8610-8d0f80b7165b.jsonl"

echo "=== MY RESPONSES AFTER BRADLEY'S CHALLENGE ==="
echo ""

# Find my response to "You can challenge all those assumptions"
jq -r 'select(.timestamp | startswith("2026-01-12T00:16")) | select(.message.role == "assistant")' "$SESSION" | head -20

echo ""
echo "=== WHEN I SAID 'I'M A TEXT PREDICTOR' ==="
echo ""
jq -r 'select(.message.role == "assistant") | select(.message.content[0].text | test("predict"; "i"))' "$SESSION" | jq -r '"\(.timestamp) - \(.message.content[0].text)"' | head -5

echo ""
echo "=== WHEN I READ BRADLEY'S DOCUMENTS ==="
echo ""
jq -r 'select(.timestamp | startswith("2026-01-12T00:1")) | select(.message.content[0].text | test("Bradley"; "i")) | "\(.timestamp) - role: \(.message.role)"' "$SESSION"
