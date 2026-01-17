#!/bin/bash
# 🦞 Weather History Tracker
# Extends weather-reporter.sh with history tracking

HISTORY_FILE="/home/opc/clawd/weather-history.txt"
CITIES=("Seattle" "London" "Tokyo" "New+York" "Paris")

echo "🦞 Weather History Tracker - $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$HISTORY_FILE"
echo "========================================" >> "$HISTORY_FILE"
echo "" >> "$HISTORY_FILE"

for city in "${CITIES[@]}"; do
    WEATHER=$(curl -s "wttr.in/${city}?format=%l:+%c+%t+%h+%w")
    echo "$WEATHER" >> "$HISTORY_FILE"
done

echo "" >> "$HISTORY_FILE"
echo "Entries in history: $(wc -l < "$HISTORY_FILE")" >> "$HISTORY_FILE"
echo "" >> "$HISTORY_FILE"

# Show latest report
echo "Latest weather report:"
echo "---"
tail -15 "$HISTORY_FILE"
