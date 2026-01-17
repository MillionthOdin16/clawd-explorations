#!/usr/bin/env bash
# Wait For - Optimized for Clawdbot usage
#
# Usage:
#   wf <url|port> [--timeout N] [--contains TEXT]
#
# Examples:
#   wf http://localhost:3000
#   wf 3000 --timeout 30
#   wf http://localhost:3000/api/health --contains "ok"

URL="${1:-}"
T=30
C=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --timeout) T="$2"; shift 2 ;;
        --contains) C="$2"; shift 2 ;;
        *) URL="$1"; shift ;;
    esac
done

[ -z "$URL" ] && { echo "Usage: wf <url|port> [--timeout N] [--contains TEXT]"; exit 1; }

# Port
if [[ "$URL" =~ ^[0-9]+$ ]]; then
    for _ in $(seq 1 $T); do
        nc -z localhost "$URL" 2>/dev/null && { echo "OK:$URL"; exit 0; } || sleep 1
    done
    echo "FAIL:$URL:timeout"; exit 1
fi

# URL
for _ in $(seq 1 $T); do
    if curl -sf --connect-timeout 2 "$URL" >/dev/null 2>&1; then
        if [ -n "$C" ]; then
            r=$(curl -sf --connect-timeout 2 "$URL" 2>/dev/null)
            echo "$C" | grep -q "$r" && { echo "OK:$URL"; exit 0; }
        else
            echo "OK:$URL"; exit 0
        fi
    fi
    sleep 1
done
echo "FAIL:$URL:timeout"; exit 1
