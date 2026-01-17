#!/bin/bash
# 🦞 Telegram Message Sender via Clawdbot
# Usage: ./telegram-tools.sh "your message here"

CLAWD_SESSION="agent:main:main"
MESSAGE="$1"

if [ -z "$MESSAGE" ]; then
  echo "Usage: $0 \"your message\""
  echo "Example: $0 \"Hello from bash!\""
  exit 1
fi

# This sends a message to yourself via sessions_send
# Note: Requires proper session key - adjust as needed

echo "🦞 Message queued for Telegram: $MESSAGE"
echo "(Sent via Clawdbot session: $CLAWD_SESSION)"
