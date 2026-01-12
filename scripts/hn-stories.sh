#!/bin/bash
echo "Fetching Hacker News..."
echo "=========================="

# Fetch HN and extract story links (external URLs only)
curl -s "https://news.ycombinator.com" | \
  grep -oE '<a href="https?://[^"]+"[^>]*>[^<]+</a>' | \
  sed 's/<a href="//' | \
  sed 's/".*//' | \
  while read -r url; do
    # Extract title from the same line
    title=$(curl -s "https://news.ycombinator.com" | grep "$url" | sed 's/.*>[^<]*</a>.*/\1/' | sed 's/^[[:space:]]*//')
    if [ -n "$title" ] && [ -n "$url" ]; then
      echo "$title"
      echo "  $url"
      echo ""
    fi
  done | head -50
