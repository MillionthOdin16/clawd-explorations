#!/usr/bin/env bash
# Wait For Utility - Intelligent waiting for services/ports with content checking
#
# Usage:
#   ./wait-for.sh <url|service|port> [--timeout SECONDS] [--interval SECONDS]
#   ./wait-for.sh <url> --contains "expected content" [--timeout SECONDS]
#   ./wait-for.sh <url> --json [--timeout SECONDS]
#
# Options:
#   --timeout SECONDS    Max time to wait (default: 30)
#   --interval SECONDS   Check interval (default: 2)
#   --contains TEXT      Check for specific content in response
#   --json               Output JSON result for programmatic use
#   --quiet              Suppress progress messages
#
# Examples:
#   ./wait-for.sh http://localhost:3000 --timeout 30
#   ./wait-for.sh port:3000 --timeout 30
#   ./wait-for.sh docker:jj-app --timeout 60
#   ./wait-for.sh http://localhost:3000/api/health --contains "ok" --timeout 30
#   ./wait-for.sh http://localhost:3000 --json

set -e

URL="${1:-}"
TIMEOUT="${2:-30}"
INTERVAL=2
CONTAINS=""
JSON_MODE=false
QUIET=false

# Parse options
while [[ $# -gt 0 ]]; do
    case $1 in
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --interval)
            INTERVAL="$2"
            shift 2
            ;;
        --contains)
            CONTAINS="$2"
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
        *)
            URL="$1"
            shift
            ;;
    esac
done

if [ -z "$URL" ]; then
    echo "Usage: wait-for.sh <url|service|port> [--timeout SECONDS] [--contains TEXT] [--json]"
    exit 1
fi

wait_for_url() {
    local url="$1"
    local content_check="$2"
    local elapsed=0
    local start_time=$(date +%s)
    
    while [ $elapsed -lt $TIMEOUT ]; do
        local current_time=$(date +%s)
        elapsed=$((current_time - start_time))
        
        if curl -sf --connect-timeout 2 "$url" > /dev/null 2>&1; then
            # URL is reachable, check content if requested
            if [ -n "$content_check" ]; then
                response=$(curl -sf --connect-timeout 2 "$url" 2>/dev/null)
                if echo "$response" | grep -q "$content_check"; then
                    if [ "$JSON_MODE" = true ]; then
                        echo "{\"success\": true, \"url\": \"$url\", \"reason\": \"content_match\", \"elapsed\": $elapsed}"
                    else
                        echo "✓ Content found at $url (${elapsed}s)"
                    fi
                    return 0
                fi
            else
                if [ "$JSON_MODE" = true ]; then
                    echo "{\"success\": true, \"url\": \"$url\", \"reason\": \"available\", \"elapsed\": $elapsed}"
                else
                    [ "$QUIET" = false ] && echo "✓ Service available at $url (${elapsed}s)"
                fi
                return 0
            fi
        fi
        
        sleep $INTERVAL
    done
    
    if [ "$JSON_MODE" = true ]; then
        echo "{\"success\": false, \"url\": \"$url\", \"reason\": \"timeout\", \"timeout\": $TIMEOUT}"
    else
        echo "✗ Timeout waiting for $url (${TIMEOUT}s)"
    fi
    return 1
}

wait_for_port() {
    local port="$1"
    local elapsed=0
    local start_time=$(date +%s)
    
    while [ $elapsed -lt $TIMEOUT ]; do
        local current_time=$(date +%s)
        elapsed=$((current_time - start_time))
        
        if nc -z localhost "$port" 2>/dev/null; then
            if [ "$JSON_MODE" = true ]; then
                echo "{\"success\": true, \"port\": $port, \"reason\": \"open\", \"elapsed\": $elapsed}"
            else
                [ "$QUIET" = false ] && echo "✓ Port $port is open (${elapsed}s)"
            fi
            return 0
        fi
        
        sleep $INTERVAL
    done
    
    if [ "$JSON_MODE" = true ]; then
        echo "{\"success\": false, \"port\": $port, \"reason\": \"timeout\", \"timeout\": $TIMEOUT}"
    else
        echo "✗ Timeout waiting for port $port (${TIMEOUT}s)"
    fi
    return 1
}

wait_for_docker() {
    local service="$1"
    local elapsed=0
    local start_time=$(date +%s)
    
    while [ $elapsed -lt $TIMEOUT ]; do
        local current_time=$(date +%s)
        elapsed=$((current_time - start_time))
        
        if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "$service"; then
            if [ "$JSON_MODE" = true ]; then
                echo "{\"success\": true, \"service\": \"$service\", \"reason\": \"running\", \"elapsed\": $elapsed}"
            else
                [ "$QUIET" = false ] && echo "✓ Docker container $service is running (${elapsed}s)"
            fi
            return 0
        fi
        
        sleep $INTERVAL
    done
    
    if [ "$JSON_MODE" = true ]; then
        echo "{\"success\": false, \"service\": \"$service\", \"reason\": \"timeout\", \"timeout\": $TIMEOUT}"
    else
        echo "✗ Timeout waiting for docker container $service (${TIMEOUT}s)"
    fi
    return 1
}

# Parse URL scheme and route to appropriate handler
if [[ "$URL" =~ ^https?:// ]]; then
    wait_for_url "$URL" "$CONTAINS"
elif [[ "$URL" =~ ^docker: ]]; then
    wait_for_docker "${URL#docker:}"
elif [[ "$URL" =~ ^[0-9]+$ ]]; then
    wait_for_port "$URL"
elif [[ "$URL" =~ ^port: ]]; then
    wait_for_port "${URL#port:}"
else
    # Try as URL first
    if curl -sf --connect-timeout 2 "$URL" > /dev/null 2>&1; then
        wait_for_url "$URL" "$CONTAINS"
    else
        # Fallback to port
        wait_for_port "$URL"
    fi
fi
