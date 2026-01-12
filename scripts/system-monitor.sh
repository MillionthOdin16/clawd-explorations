#!/bin/bash
# 🦞 System Health Monitor
# Run this to check system status

echo "🦞 SYSTEM HEALTH CHECK 🦞"
echo "======================="
echo ""

# Memory usage
MEM_PERCENT=$(free | awk '/Mem/{printf("%.1f"), $3/$2*100}')
echo "Memory: ${MEM_PERCENT}% used"

# Disk usage
DISK_PERCENT=$(df / | awk 'NR==2{printf("%.1f"), $5}')
echo "Disk: ${DISK_PERCENT}% used"

# CPU load (1 min avg)
LOAD=$(cat /proc/loadavg | awk '{print $1}')
echo "Load average: $LOAD"

# Clawdbot status
echo ""
echo "🦞 CLAWDBOT STATUS:"
if pgrep -f "clawdbot" > /dev/null; then
  echo "✓ Running"
else
  echo "✗ Not running"
fi

# Check node processes
NODE_PROCS=$(pgrep -c node 2>/dev/null || echo "0")
echo "Node processes: $NODE_PROCS"

echo ""
echo "Done! 🦞"
