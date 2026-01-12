#!/bin/bash
# Helper script to run commands on LittleClawd
# Usage: ./littleclawd-helper.sh "<command>"

SSH_KEY="/home/opc/.ssh/baby_clawdbot_key"
HOST="opc@129.153.132.33"

if [ -z "$1" ]; then
    echo "Usage: $0 \"<command>\""
    echo ""
    echo "Examples:"
    echo "  $0 \"cd ~/littleclawd && python3 scripts/status.py\""
    echo "  $0 \"free -h\""
    echo "  $0 \"df -h\""
    exit 1
fi

ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$HOST" "$1"
