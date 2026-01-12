#!/bin/bash
# Setup LittleClawd - Update and install essential tools

echo "🦞 LittleClawd Setup Phase 1"
echo "================================"
echo ""

SSH_KEY="/home/opc/.ssh/baby_clawdbot_key"
HOST="opc@129.153.132.33"

# Helper function for SSH
run_remote() {
    ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o ConnectTimeout=30 "$HOST" "$1"
}

echo "Step 1: Checking system status..."
echo "--------------------------------"
run_remote "free -h && df -h / && uptime"
echo ""

echo "Step 2: Checking Python version and installing pip..."
echo "--------------------------------"
run_remote "python3 --version && sudo dnf install -y python3-pip 2>&1 | tail -5"
echo ""

echo "Step 3: Installing essential Python packages..."
echo "--------------------------------"
run_remote "pip3 install --user requests beautifulsoup4 2>&1 | tail -10"
echo ""

echo "Step 4: Installing git..."
echo "--------------------------------"
run_remote "sudo dnf install -y git 2>&1 | tail -5"
echo ""

echo "Step 5: Checking for Node.js..."
echo "--------------------------------"
run_remote "which node npm || echo 'Node.js not found - will install later'"
echo ""

echo "Step 6: Creating proper workspace structure..."
echo "--------------------------------"
run_remote "mkdir -p ~/littleclawd/{scripts,data,logs,archive,projects} && ls -la ~/littleclawd/"
echo ""

echo "✅ Phase 1 complete!"
echo ""
