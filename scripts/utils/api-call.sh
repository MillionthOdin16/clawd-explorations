#!/usr/bin/env bash
# API Call Utility - Standardized API calls with error handling
#
# Usage:
#   ./api-call.sh <method> <url> [--data <json>] [--headers <k:v>] [--json]
#
# Options:
#   --method     HTTP method (GET, POST, PUT, PATCH, DELETE)
#   --url        URL to call
#   --data       Request body (for POST/PUT/PATCH)
#   --headers    Headers as "Key:Value,Key2:Value2"
#   --json       Output JSON result (for programmatic use)
#   --quiet      Suppress the "Executing:" message
#   --timeout    Request timeout in seconds (default: 30)
#
# Examples:
#   ./api-call.sh GET http://localhost:3000/api/data
#   ./api-call.sh POST http://localhost:3000/api/chat --data '{"msg":"hello"}'
#   ./api-call.sh GET https://api.example.com --headers "Authorization:Bearer token"
#   ./api-call.sh GET http://localhost:3000/api/data --json

set -e

METHOD=""
URL=""
DATA=""
HEADERS=""
JSON_MODE=false
QUIET=false
TIMEOUT=30

# Parse options
while [[ $# -gt 0 ]]; do
    case $1 in
        --method)
            METHOD="$2"
            shift 2
            ;;
        --url)
            URL="$2"
            shift 2
            ;;
        --data)
            DATA="$2"
            shift 2
            ;;
        --headers)
            HEADERS="$2"
            shift 2
            ;;
        --json)
            JSON_MODE=true
            shift
            ;;
        --quiet)
            QUIET=true
            shift
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        *)
            # First positional is method, second is URL
            if [ -z "$METHOD" ]; then
                METHOD="$1"
            elif [ -z "$URL" ]; then
                URL="$1"
            else
                DATA="$1"
            fi
            shift
            ;;
    esac
done

# Set defaults
METHOD="${METHOD:-GET}"

if [ -z "$URL" ]; then
    echo "Usage: api-call.sh <method> <url> [--data <json>] [--headers <k:v>] [--json]"
    exit 1
fi

# Build curl command
CURL_CMD="curl -s -X $METHOD"

# Add timeout
CURL_CMD="$CURL_CMD --max-time $TIMEOUT"

# Add headers if provided
if [ -n "$HEADERS" ]; then
    IFS=',' read -ra HDRS <<< "$HEADERS"
    for hdr in "${HDRS[@]}"; do
        CURL_CMD="$CURL_CMD -H '$hdr'"
    done
fi

# Add data if provided (POST/PUT/PATCH)
if [ -n "$DATA" ] && [[ "$METHOD" =~ ^(POST|PUT|PATCH)$ ]]; then
    CURL_CMD="$CURL_CMD -H 'Content-Type: application/json' -d '$DATA'"
fi

# Execute
if [ "$QUIET" = false ]; then
    echo "Executing: $CURL_CMD $URL" >&2
fi

set +e
RESULT=$(eval "$CURL_CMD" "$URL" 2>&1)
EXIT_CODE=$?
set -e

if [ $EXIT_CODE -eq 0 ]; then
    if [ "$JSON_MODE" = true ]; then
        # Try to parse and format as JSON
        if echo "$RESULT" | grep -q '^{' 2>/dev/null; then
            echo "$RESULT"
        else
            # Wrap non-JSON response
            echo "{\"success\": true, \"data\": $(echo "$RESULT" | jq -Rs .)}"
        fi
    else
        echo "$RESULT"
    fi
else
    if [ "$JSON_MODE" = true ]; then
        echo "{\"success\": false, \"error\": $(echo "$RESULT" | jq -Rs .), \"url\": \"$URL\", \"method\": \"$METHOD\"}"
    else
        echo "API call failed: $RESULT" >&2
        exit 1
    fi
fi
