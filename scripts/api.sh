#!/usr/bin/env bash
# API Call - Optimized for Clawdbot usage
#
# Usage:
#   api <method> <url> [--data JSON] [--header "K:V"]
#
# Examples:
#   api GET http://localhost:3000/api/data
#   api POST http://localhost:3000/api --data '{"a":1}'
#   api GET http://localhost:3000 --header "Auth:Bearer token"

M="${1:-GET}"
U="${2:-}"
D=""
H=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --data) D="$2"; shift 2 ;;
        --header) H="$2"; shift 2 ;;
        *) [ -z "$U" ] && U="$1"; shift ;;
    esac
done

[ -z "$U" ] && { echo "Usage: api <method> <url> [--data JSON] [--header K:V]"; exit 1; }

C="curl -s -X $M --max-time 30"
[ -n "$D" ] && [[ "$M" =~ ^(POST|PUT|PATCH)$ ]] && C="$C -H 'Content-Type:application/json' -d '$D'"
[ -n "$H" ] && C="$C -H '$H'"

r=$(eval "$C '$U'" 2>&1)
e=$?
[ $e -eq 0 ] && { echo "$r"; exit 0; } || { echo "ERROR:$r"; exit 1; }
