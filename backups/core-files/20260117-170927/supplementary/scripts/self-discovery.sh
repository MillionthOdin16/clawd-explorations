#!/bin/bash

echo "=== Self-Discovery Script ==="
echo ""
echo "System Info:"
echo "Hostname: $(hostname)"
echo "OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2)"
echo "Kernel: $(uname -r)"
echo "Architecture: $(uname -m)"
echo ""

echo "Available Shells:"
echo "bash: $(which bash)"
echo "zsh: $(which zsh)"
echo "sh: $(which sh)"
echo ""

echo "Development Tools:"
echo "Python3: $(python3 --version 2>&1)"
echo "Node: $(node --version 2>&1)"
echo "npm: $(npm --version 2>&1)"
echo "Cargo: $(cargo --version 2>&1)"
echo "Rustc: $(rustc --version 2>&1)"
echo ""

echo "Network Tools:"
echo "curl: $(curl --version 2>&1 | head -1)"
echo "wget: $(wget --version 2>&1 | head -1)"
echo "git: $(git --version 2>&1)"
echo ""

echo "Disk Space:"
df -h /home/opc/clawd | tail -1
echo ""

echo "Memory:"
free -h | head -2
echo ""

echo "Process Count:"
ps aux | wc -l
echo ""

echo "=== End of Self-Discovery ==="
