#!/bin/bash

#===============================================================================
# Git Safe Commit Script v1.0
# 
# Purpose: Safely commit changes with validation checks:
# - Check for leaked secrets
# - Verify no debug code
# - Validate file changes
# - Safe commit with confirmation
#
# Usage: ./git-safe-commit.sh [message]
#        ./git-safe-commit.sh --dry-run [message]
#
#===============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#-------------------------------------------------------------------------------
# Helper Functions
#-------------------------------------------------------------------------------

print_info() { echo -e "${BLUE}ℹ  $*${NC}"; }
print_success() { echo -e "${GREEN}✓ $*${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $*${NC}"; }
print_error() { echo -e "${RED}✗ $*${NC}"; }

confirm() {
    local prompt="$1"
    read -p "${CYAN}$prompt [y/N]: ${NC}" yn
    [[ "$yn" == "y" || "$yn" == "Y" ]]
}

#-------------------------------------------------------------------------------
# Secret Detection
#-------------------------------------------------------------------------------

scan_for_secrets() {
    print_info "Scanning for potential secrets..."
    
    local secrets_found=0
    local patterns=(
        "api_key\s*[:=]\s*['\"][A-Za-z0-9_-]{20,}['\"]"
        "apikey\s*[:=]\s*['\"][A-Za-z0-9_-]{20,}['\"]"
        "secret\s*[:=]\s*['\"][A-Za-z0-9_-]{20,}['\"]"
        "token\s*[:=]\s*['\"][A-Za-z0-9_-]{20,}['\"]"
        "password\s*[:=]\s*['\"][^'\"]+['\"]"
        "Bearer\s[A-Za-z0-9\-\._~\+\/]+=*"
        "sk-[A-Za-z0-9]{20,}"
    )
    
    local staged_files=$(git diff --cached --name-only 2>/dev/null || echo "")
    local unstaged_files=$(git diff --name-only 2>/dev/null || echo "")
    local all_files="$staged_files $unstaged_files"
    
    for pattern in "${patterns[@]}"; do
        if echo "$all_files" | xargs grep -l "$pattern" 2>/dev/null | grep -q .; then
            print_warning "Potential secret found matching: $pattern"
            secrets_found=1
        fi
    done
    
    # Check for .env in changes
    if echo "$all_files" | grep -q "\.env"; then
        print_warning ".env file in changes - ensure no real secrets!"
        secrets_found=1
    fi
    
    if [[ "$secrets_found" -eq 0 ]]; then
        print_success "No secrets detected"
    fi
    
    return $secrets_found
}

#-------------------------------------------------------------------------------
# Debug Code Detection
#-------------------------------------------------------------------------------

scan_for_debug_code() {
    print_info "Scanning for debug code..."
    
    local debug_patterns=(
        "console\.log\("
        "console\.warn\("
        "console\.error\("
        "print\("
        "TODO.*debug"
        "FIXME.*debug"
        "\/\/.*DEBUG"
        "\/\/.*WIP"
    )
    
    local staged_files=$(git diff --cached --name-only 2>/dev/null | grep -E "\.(ts|js|py|sh)$" || echo "")
    
    if echo "$staged_files" | xargs grep -lE "${debug_patterns[*]}" 2>/dev/null | grep -q .; then
        print_warning "Debug code detected:"
        echo "$staged_files" | xargs grep -nE "${debug_patterns[*]}" 2>/dev/null | head -10
        if ! confirm "Continue with commit?"; then
            print_error "Commit aborted"
            exit 1
        fi
    else
        print_success "No debug code detected"
    fi
}

#-------------------------------------------------------------------------------
# Validation
#-------------------------------------------------------------------------------

validate_commit() {
    print_info "Validating commit..."
    
    # Check if there are changes
    if ! git diff --cached --quiet 2>/dev/null; then
        print_success "Changes staged"
    else
        print_warning "No changes staged"
        return 1
    fi
    
    # Check for large files
    local large_files=$(git diff --cached --name-only | xargs -I{} sh -c 'stat -f%z {} 2>/dev/null || stat -c%s {} 2>/dev/null' | awk '$1 > 1000000' | wc -l)
    if [[ "$large_files" -gt 0 ]]; then
        print_warning "Large files detected (>1MB)"
    fi
    
    # Scan for secrets
    if ! scan_for_secrets; then
        if ! confirm "Secrets detected - continue anyway?"; then
            print_error "Commit aborted"
            exit 1
        fi
    fi
    
    # Scan for debug code
    scan_for_debug_code
    
    print_success "Validation complete"
    return 0
}

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

main() {
    local dry_run=false
    local message=""
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dry-run)
                dry_run=true
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [OPTIONS] [message]"
                echo ""
                echo "Options:"
                echo "  --dry-run    Show what would be committed without committing"
                echo "  --help       Show this help"
                echo ""
                echo "Examples:"
                echo "  $0 \"Add new feature\""
                echo "  $0 --dry-run \"Test commit\""
                exit 0
                ;;
            *)
                message="$1"
                shift
                ;;
        esac
    done
    
    cd "$REPO_ROOT"
    
    echo "╔════════════════════════════════════════════════════════════════════════╗"
    echo "║                    GIT SAFE COMMIT                                  ║"
    echo "╚═══════════════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Show status
    echo "Changes to be committed:"
    git diff --cached --stat 2>/dev/null || print_warning "No staged changes"
    echo ""
    
    # Validate
    if ! validate_commit; then
        print_error "Validation failed"
        exit 1
    fi
    
    echo ""
    
    # Confirm commit
    if [[ "$dry_run" == "true" ]]; then
        print_info "DRY RUN - No commit would be made"
        if [[ -n "$message" ]]; then
            print_info "Message: $message"
        fi
        exit 0
    fi
    
    if ! confirm "Proceed with commit?"; then
        print_info "Commit cancelled"
        exit 0
    fi
    
    # Create commit
    if [[ -n "$message" ]]; then
        git commit -m "$message"
    else
        git commit
    fi
    
    print_success "Commit created successfully!"
    echo ""
    print_info "Run 'git push' to push changes"
}

main "$@"
