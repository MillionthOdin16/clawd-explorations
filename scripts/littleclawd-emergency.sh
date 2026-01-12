#!/bin/bash
# Emergency optimization script for memory-constrained LittleClawd
# This is minimal and safe - won't break anything critical

# 1. Clear dnf cache (safe, frees disk space)
echo "Clearing DNF cache..."
sudo dnf clean all -y 2>/dev/null || echo "DNF clean skipped"

# 2. Clear journal logs (safe, frees disk space)
echo "Cleaning journal logs (keeping last 1 day)..."
sudo journalctl --vacuum-time=1d 2>/dev/null || echo "Journal clean skipped"

# 3. Drop system caches (safe, frees RAM)
echo "Dropping system caches..."
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null || echo "Cache drop skipped"

# 4. Clear user cache
echo "Clearing user cache..."
rm -rf ~/.cache/* 2>/dev/null || echo "User cache already empty"

# 5. Clear /tmp (safe, frees disk)
echo "Clearing /tmp..."
sudo rm -rf /tmp/* 2>/dev/null || echo "Temp already clean"

echo ""
echo "Memory after cleanup:"
free -h

echo ""
echo "Disk usage:"
df -h / | tail -1

echo ""
echo "Emergency cleanup complete!"
