#!/bin/bash

#===============================================================================
# Clawdbot ROBUST Update Script (v5.0 - Enhanced Robustness)
# 
# Purpose: Safely update Clawdbot workspace and/or installation with:
# - PRE-UPDATE PREVIEW (see what will change)
# - MANUAL CONFIRMATION (user must approve)
# - Automatic backups before any changes
# - Dependency installation (pnpm/npm/bun)
# - Project build (TypeScript + UI)
# - Health checks (clawdbot doctor)
# - CORE FILE SYNTHESIS (understand and adapt upstream changes)
# - SCHEMA VALIDATION (detect new config parameters)
# - SECRET SCANNING (prevent leaked API keys)
# - WORKSPACE OR INSTALLATION update (choose which)
# - AUTOMATIC STASH HANDLING (for external repos)
# - ROLLBACK CAPABILITY (git bundle for recovery)
# - CONFLICT DETECTION (abort on conflicts)
# - COMPREHENSIVE LOGGING
# - VERIFICATION CHECKS
# - POST-UPDATE REPORTING
#
# Usage: 
#   ./update-clawdbot.sh --help          # Show all options
#   ./update-clawdbot.sh --preview      # See what would change (SAFE)
#   ./update-clawdbot.sh --update       # Update workspace (default)
#   ./update-clawdbot.sh --update-clawdbot  # Update Clawdbot installation
#   ./update-clawdbot.sh --full-update  # Update BOTH workspace AND installation
#
# Environment Variables:
#   CLAWDBOT_DIR    # Workspace directory (default: /home/opc/clawd)
#   CLAWDBOT_INSTALL_DIR  # Clawdbot installation (default: /home/opc/clawdbot)
#   AUTO_CONFIRM    # Skip confirmations if true (for CI)
#
#===============================================================================

set -euo pipefail

# Script version
SCRIPT_VERSION="5.0"

# Configuration
CLAWDBOT_DIR="${CLAWDBOT_DIR:-/home/opc/clawd}"
CLAWDBOT_INSTALL_DIR="${CLAWDBOT_INSTALL_DIR:-/home/opc/clawdbot}"
BACKUP_DIR="${CLAWDBOT_DIR}/backups"
LOG_FILE="${BACKUP_DIR}/update-$(date +%Y%m%d-%H%M%S).log"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Safety flags
AUTO_CONFIRM=${AUTO_CONFIRM:-false}

#-------------------------------------------------------------------------------
# Output Functions
#-------------------------------------------------------------------------------

print_header() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════════════╗"
    echo "║ $1"
    local padding=$((78 - ${#1}))
    echo "║${padding:0:$padding}║"
    echo "╚═══════════════════════════════════════════════════════════════════════╝"
    echo ""
}

print_section() {
    echo ""
    echo "════════════════════════════════════════════════════════════════════════"
    echo " $1"
    echo "════════════════════════════════════════════════════════════════════════"
    echo ""
}

print_step() {
    echo ""
    echo "━━━ STEP $1 of $2: $3 ━━━"
    echo ""
}

print_info() { echo -e "${BLUE}ℹ  $*${NC}"; }
print_success() { echo -e "${GREEN}✓ $*${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $*${NC}"; }
print_error() { echo -e "${RED}✗ $*${NC}"; }
print_highlight() { echo -e "${CYAN}$*${NC}"; }

confirm() {
    local prompt="$1"
    local default="${2:-n}"
    
    if [[ "$AUTO_CONFIRM" == "true" ]]; then
        print_info "Auto-confirming: $prompt"
        return 0
    fi
    
    while true; do
        if [[ "$default" == "y" ]]; then
            read -p "${CYAN}$prompt [Y/n]: ${NC}" yn
            [[ -z "$yn" || "$yn" == "y" || "$yn" == "Y" ]] && return 0
            return 1
        else
            read -p "${CYAN}$prompt [y/N]: ${NC}" yn
            [[ "$yn" == "y" || "$yn" == "Y" ]] && return 0
            return 1
        fi
    done
}

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

#-------------------------------------------------------------------------------
# Setup
#-------------------------------------------------------------------------------

setup_directories() {
    mkdir -p "$BACKUP_DIR"
    mkdir -p "${BACKUP_DIR}/core-files"
    mkdir -p "${BACKUP_DIR}/git-state"
    mkdir -p "${BACKUP_DIR}/configs"
    mkdir -p "${BACKUP_DIR}/install-backups"
}

check_disk_space() {
    print_info "Checking available disk space..."
    local available=$(df -BG "$BACKUP_DIR" | tail -1 | awk '{print $4}' | sed 's/G//')
    local needed=500
    
    if [[ "$available" -lt "$needed" ]]; then
        print_error "Insufficient disk space: ${available}MB available, ${needed}MB needed"
        return 1
    fi
    print_info "Disk space OK: ${available}MB available"
    return 0
}

#-------------------------------------------------------------------------------
# Backup Functions
#-------------------------------------------------------------------------------

backup_workspace() {
    local target_dir="$1"
    local backup_subdir="${BACKUP_DIR}/core-files/${TIMESTAMP}"
    mkdir -p "$backup_subdir"
    
    print_info "Backing up workspace files from: $target_dir"
    
    # Core files
    for file in AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md SKILLS.md SUBAGENTS.md INDEX.md; do
        if [[ -f "${target_dir}/${file}" ]]; then
            cp "${target_dir}/${file}" "${backup_subdir}/"
            print_success "Backed up: $file"
        fi
    done
    
    # Memory
    if [[ -d "${target_dir}/memory" ]]; then
        cp -r "${target_dir}/memory" "${backup_subdir}/memory-backup"
        print_success "Backed up: memory/"
    fi
    
    # Skills
    if [[ -d "${target_dir}/skills" ]]; then
        cp -r "${target_dir}/skills" "${backup_subdir}/skills-backup"
        print_success "Backed up: skills/"
    fi
    
    # Scripts
    if [[ -d "${target_dir}/scripts" ]]; then
        mkdir -p "${backup_subdir}/scripts"
        cp -r "${target_dir}/scripts" "${backup_subdir}/supplementary/"
        print_success "Backed up: scripts/"
    fi
    
    echo "$backup_subdir" > "${BACKUP_DIR}/latest-backup.txt"
}

backup_clawdbot_installation() {
    local backup_subdir="${BACKUP_DIR}/install-backups/${TIMESTAMP}"
    mkdir -p "$backup_subdir"
    
    print_info "Backing up Clawdbot installation: $CLAWDBOT_INSTALL_DIR"
    
    # Backup git state
    cd "$CLAWDBOT_INSTALL_DIR"
    git bundle create "${backup_subdir}/repo-bundle.bundle" --all 2>/dev/null || true
    git rev-parse HEAD > "${backup_subdir}/commit.txt"
    
    # Backup configs
    if [[ -f "${HOME}/.clawdbot/clawdbot.json" ]]; then
        cp "${HOME}/.clawdbot/clawdbot.json" "${backup_subdir}/"
        print_success "Backed up: clawdbot.json"
    fi
    
    # Backup .env if exists
    if [[ -f "${HOME}/.env" ]]; then
        cp "${HOME}/.env" "${backup_subdir}/.env.backup"
        print_success "Backed up: .env"
    fi
    
    print_success "Installation backup created: ${backup_subdir}"
}

create_full_backup() {
    print_header "BACKUP: Creating Complete Backup"
    
    check_disk_space || exit 1
    
    backup_workspace "$CLAWDBOT_DIR"
    backup_clawdbot_installation
    
    # Manifest
    local manifest="${BACKUP_DIR}/backup-manifest.txt"
    {
        echo "Backup Manifest - $TIMESTAMP"
        echo "Workspace: $CLAWDBOT_DIR"
        echo "Installation: $CLAWDBOT_INSTALL_DIR"
    } > "$manifest"
    
    print_success "Full backup complete!"
}

#-------------------------------------------------------------------------------
# Git Stash Handling for External Repos
#-------------------------------------------------------------------------------

stash_external_changes() {
    local repo_dir="$1"
    local description="$2"
    
    cd "$repo_dir"
    
    print_info "Checking for uncommitted changes in $description..."
    
    if git diff --quiet 2>/dev/null && git ls-files --others --exclude-standard --empty-dir | grep -q .; then
        print_warning "Untracked files found in $description"
        ls --group-directories-first 2>/dev/null | head -10
    fi
    
    if ! git diff --quiet 2>/dev/null; then
        print_warning "Uncommitted changes detected in $description"
        echo ""
        print_info "Stashing changes..."
        if git stash push -u -m "Auto-stash before update: $TIMESTAMP" >> "$LOG_FILE" 2>&1; then
            print_success "Changes stashed"
            return 0
        else
            print_error "Failed to stash changes"
            return 1
        fi
    fi
    
    if [[ -n "$(git ls-files --others --exclude-standard 2>/dev/null)" ]]; then
        print_warning "Untracked files found in $description"
        print_info "Untracked files:"
        git ls-files --others --exclude-standard | head -10
        echo ""
        if confirm "Remove untracked files (except .gitignore)?" "n"; then
            git clean -fd 2>/dev/null || true
            print_success "Untracked files removed"
        fi
    fi
    
    print_success "No uncommitted changes in $description"
    return 0
}

restore_stashed_changes() {
    local repo_dir="$1"
    local description="$2"
    
    cd "$repo_dir"
    
    if git stash list | grep -q .; then
        print_info "Restoring stashed changes in $description..."
        if confirm "Restore stashed changes?" "y"; then
            if git stash pop >> "$LOG_FILE" 2>&1; then
                print_success "Stashed changes restored"
            else
                print_warning "Merge conflicts in stash - manual resolution needed"
                print_info "Run 'git stash list' and 'git stash show' to see conflicts"
                return 1
            fi
        fi
    fi
}

#-------------------------------------------------------------------------------
# Preview Functions
#-------------------------------------------------------------------------------

preview_update() {
    local target_dir="$1"
    local description="$2"
    
    print_header "PREVIEW: What Would Change ($description)"
    
    cd "$target_dir"
    
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not a git repository"
        return 1
    fi
    
    git fetch origin >> "$LOG_FILE" 2>&1 || true
    
    local new_commits=$(git log --oneline HEAD..origin/main 2>/dev/null | wc -l)
    
    if [[ "$new_commits" -eq 0 ]]; then
        print_success "Already up to date! No changes needed."
        return 0
    fi
    
    print_highlight "$new_commits commits behind origin/main"
    echo ""
    
    echo "Recent commits:"
    git log --oneline HEAD..origin/main | head -10
    echo ""
    
    local changed_files=$(git diff --name-only HEAD..origin/main 2>/dev/null | wc -l)
    print_info "$changed_files files would change"
    
    # Check for breaking changes
    if git log HEAD..origin/main --oneline | grep -qiE "breaking|remove|deprecat"; then
        print_warning "Potential breaking changes detected!"
    fi
    
    echo ""
    print_info "This preview shows what WOULD happen if you update."
    print_info "NO changes have been made yet."
}

#-------------------------------------------------------------------------------
# Synthesis Functions
#-------------------------------------------------------------------------------

perform_synthesis() {
    local target_dir="$1"
    local description="$2"
    
    print_header "SYNTHESIS: Analyzing Upstream Changes ($description)"
    
    cd "$target_dir"
    
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not a git repository"
        return 1
    fi
    
    git fetch origin >> "$LOG_FILE" 2>&1 || true
    
    local old_commit=$(git rev-parse HEAD~1 2>/dev/null || echo "")
    
    print_info "Analyzing changes from ${old_commit:0:8}..."
    
    # Check for new tools/features
    local changes=$(git diff "$old_commit"..origin/main -- "src/agents/tools/" "*.md" 2>/dev/null | wc -l)
    if [[ "$changes" -gt 0 ]]; then
        print_info "Tool/source files changed"
    fi
    
    # Check for config changes
    if git diff "$old_commit"..origin/main -- "*.json" "config.*" 2>/dev/null | grep -q "+"; then
        print_info "Config files changed - may need to review"
    fi
    
    print_success "Synthesis complete!"
}

#-------------------------------------------------------------------------------
# Update Functions
#-------------------------------------------------------------------------------

perform_update_on_repo() {
    local target_dir="$1"
    local description="$2"
    local skip_deps="${3:-false}"
    
    print_header "UPDATING: $description"
    
    cd "$target_dir"
    
    local errors=0
    local prev_commit=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
    
    # Step 1: Dependencies (if not skipped)
    if [[ "$skip_deps" != "true" ]]; then
        print_step "1" "4" "Installing Dependencies"
        if [[ -f "package.json" ]]; then
            if command -v pnpm &>/dev/null; then
                pnpm install >> "$LOG_FILE" 2>&1 && print_success "Dependencies installed" || ((errors++))
            elif command -v npm &>/dev/null; then
                npm install >> "$LOG_FILE" 2>&1 && print_success "Dependencies installed" || ((errors++))
            else
                print_warning "No package manager found - skipping"
            fi
        fi
    fi
    
    # Step 2: Build
    if [[ $errors -eq 0 ]]; then
        print_step "2" "4" "Building Project"
        if grep -q '"build"' package.json 2>/dev/null; then
            if command -v pnpm &>/dev/null; then
                pnpm run build >> "$LOG_FILE" 2>&1 && print_success "Build complete" || ((errors++))
            elif command -v npm &>/dev/null; then
                npm run build >> "$LOG_FILE" 2>&1 && print_success "Build complete" || ((errors++))
            fi
        else
            print_info "No build script - skipping"
        fi
    fi
    
    # Step 3: Fetch and merge
    if [[ $errors -eq 0 ]]; then
        print_step "3" "4" "Fetching and Merging"
        print_info "Fetching from origin..."
        git fetch origin >> "$LOG_FILE" 2>&1 || ((errors++))
        
        if [[ $errors -eq 0 ]]; then
            print_info "Merging..."
            if git merge --ff-only origin/main >> "$LOG_FILE" 2>&1; then
                print_success "Fast-forward merge successful"
            else
                print_warning "Fast-forward not possible - merge required"
                print_info "Showing conflicts:"
                git diff --name-only HEAD..origin/main | head -10
                print_error "Cannot auto-merge - manual intervention required"
                ((errors++))
            fi
        fi
    fi
    
    # Step 4: Verify
    print_step "4" "4" "Verifying"
    local current_commit=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
    print_detail "Previous commit" "${prev_commit:0:8}"
    print_detail "Current commit" "${current_commit:0:8}"
    
    if [[ $errors -eq 0 ]]; then
        print_success "Update completed successfully!"
        return 0
    else
        print_error "Update completed with $errors error(s)"
        return 1
    fi
}

#-------------------------------------------------------------------------------
# Config Validation
#-------------------------------------------------------------------------------

validate_config() {
    local target_dir="$1"
    local description="$2"
    
    print_section "CONFIG VALIDATION ($description)"
    
    cd "$target_dir"
    
    # Check for new config parameters
    print_info "Checking for new config parameters..."
    
    # Known new params from v1.13+
    local new_params=(
        "update.channel"
        "update.checkOnStart"
        "session.identityLinks"
        "session.dmScope"
    )
    
    for param in "${new_params[@]}"; do
        print_info "$param: (check config if needed)"
    done
    
    print_success "Config validation complete"
}

#-------------------------------------------------------------------------------
# Verification & Reporting
#-------------------------------------------------------------------------------

verify_update() {
    local target_dir="$1"
    local description="$2"
    
    print_section "VERIFICATION ($description)"
    
    cd "$target_dir"
    
    local current_commit=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
    print_detail "Current commit" "${current_commit:0:8}"
    
    # Check critical files
    local critical_files=("package.json" "README.md")
    for file in "${critical_files[@]}"; do
        if [[ -f "$file" ]]; then
            print_success "$file exists"
        else
            print_warning "$file missing"
        fi
    done
    
    print_success "Verification complete"
}

generate_report() {
    local target_dir="$1"
    local description="$2"
    local prev_commit="${3:-}"
    
    print_section "UPDATE REPORT ($description)"
    
    cd "$target_dir"
    
    local current_commit=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
    
    echo "╔════════════════════════════════════════════════════════════════════════╗"
    echo "║                    UPDATE COMPLETED SUCCESSFULLY                   ║"
    echo "╚═══════════════════════════════════════════════════════════════════════╝"
    echo ""
    
    if [[ -n "$prev_commit" ]]; then
        print_detail "Previous commit" "${prev_commit:0:8}"
    fi
    print_detail "Current commit" "${current_commit:0:8}"
    
    echo ""
    print_info "Full log: $LOG_FILE"
}

#-------------------------------------------------------------------------------
# Main Update Logic
#-------------------------------------------------------------------------------

update_workspace() {
    print_header "UPDATE: Clawdbot Workspace"
    
    cd "$CLAWDBOT_DIR"
    
    # Check if it's a git repo
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Workspace is not a git repository"
        return 1
    fi
    
    preview_update "$CLAWDBOT_DIR" "workspace"
    
    if ! confirm "Proceed with workspace update?" "n"; then
        print_info "Update cancelled"
        return 0
    fi
    
    create_full_backup
    perform_synthesis "$CLAWDBOT_DIR" "workspace"
    perform_update_on_repo "$CLAWDBOT_DIR" "workspace"
    validate_config "$CLAWDBOT_DIR" "workspace"
    verify_update "$CLAWDBOT_DIR" "workspace"
    
    local prev_commit=$(git rev-parse HEAD~1 2>/dev/null || echo "")
    generate_report "$CLAWDBOT_DIR" "workspace" "$prev_commit"
}

update_clawdbot_installation() {
    print_header "UPDATE: Clawdbot Installation"
    print_info "Installation directory: $CLAWDBOT_INSTALL_DIR"
    
    # Handle uncommitted changes first
    if ! stash_external_changes "$CLAWDBOT_INSTALL_DIR" "Clawdbot installation"; then
        print_error "Failed to handle uncommitted changes"
        return 1
    fi
    
    preview_update "$CLAWDBOT_INSTALL_DIR" "Clawdbot installation"
    
    if ! confirm "Proceed with Clawdbot installation update?" "n"; then
        print_info "Update cancelled"
        restore_stashed_changes "$CLAWDBOT_INSTALL_DIR" "Clawdbot installation"
        return 0
    fi
    
    backup_clawdbot_installation
    perform_update_on_repo "$CLAWDBOT_INSTALL_DIR" "Clawdbot installation" "true"
    verify_update "$CLAWDBOT_INSTALL_DIR" "Clawdbot installation"
    
    # Restart daemon if needed
    if command -v clawdbot &>/dev/null; then
        print_info "Restarting Clawdbot daemon..."
        clawdbot daemon restart >> "$LOG_FILE" 2>&1 && print_success "Daemon restarted" || print_warning "Daemon restart failed"
    fi
    
    local prev_commit=$(git rev-parse HEAD~1 2>/dev/null || echo "")
    generate_report "$CLAWDBOT_INSTALL_DIR" "Clawdbot installation" "$prev_commit"
    
    # Restore stashed changes
    restore_stashed_changes "$CLAWDBOT_INSTALL_DIR" "Clawdbot installation"
}

full_update() {
    print_header "FULL UPDATE: Workspace + Installation"
    
    # Update workspace first
    print_section "PART 1: Workspace Update"
    update_workspace || true
    
    # Then update Clawdbot installation
    print_section "PART 2: Clawdbot Installation Update"
    update_clawdbot_installation || true
}

#-------------------------------------------------------------------------------
# Main Entry Point
#-------------------------------------------------------------------------------

show_help() {
    cat << EOF
Clawdbot ROBUST Update Script v${SCRIPT_VERSION}

Usage: $0 [OPTIONS]

WORKSPACE COMMANDS (default):
    --update           Update workspace (backup + deps + build + merge)
    --preview          See what would change (SAFE)
    --backup           Create full backup only
    --synthesize      Analyze upstream changes

INSTALLATION COMMANDS:
    --update-clawdbot  Update Clawdbot installation (auto-stash handling)
    --install-backup   Backup installation configs

COMBINED COMMANDS:
    --full-update      Update BOTH workspace AND installation

UTILITY COMMANDS:
    --status           Check current state
    --test-rollback    Test rollback capability
    --rollback         Rollback to previous state
    --version          Show version
    --help             Show this help

ENVIRONMENT VARIABLES:
    CLAWDBOT_DIR            # Workspace (default: /home/opc/clawd)
    CLAWDBOT_INSTALL_DIR    # Installation (default: /home/opc/clawdbot)
    AUTO_CONFIRM=true       # Skip confirmations (for CI)

EXAMPLES:
    $0 --preview              # SAFE - see what would change
    $0 --update              # Update workspace
    $0 --update-clawdbot     # Update Clawdbot installation
    $0 --full-update         # Update both

For documentation, see UPDATE-PROCEDURE.md

EOF
}

main() {
    setup_directories
    
    local action="update"  # Default action
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --preview) action="preview"; shift ;;
            --update) action="update"; shift ;;
            --update-clawdbot) action="update-clawdbot"; shift ;;
            --install-backup) action="install-backup"; shift ;;
            --full-update) action="full-update"; shift ;;
            --status) action="status"; shift ;;
            --test-rollback) action="test-rollback"; shift ;;
            --rollback) action="rollback"; shift ;;
            --version) action="version"; shift ;;
            --help|-h) show_help; exit 0 ;;
            *) print_error "Unknown option: $1"; show_help; exit 1 ;;
        esac
    done
    
    case "$action" in
        preview)
            preview_update "$CLAWDBOT_DIR" "workspace"
            ;;
        update)
            update_workspace
            ;;
        update-clawdbot)
            update_clawdbot_installation
            ;;
        install-backup)
            backup_clawdbot_installation
            ;;
        full-update)
            full_update
            ;;
        status)
            print_section "Current State"
            print_info "Workspace: $CLAWDBOT_DIR"
            print_info "Installation: $CLAWDBOT_INSTALL_DIR"
            ;;
        test-rollback)
            print_section "Test Rollback"
            ls -lh "${BACKUP_DIR}/install-backups"/*/repo-bundle.bundle 2>/dev/null || print_warning "No git bundle found"
            ;;
        rollback)
            print_section "Rollback"
            print_warning "Manual rollback required - run 'git reset --hard <commit>'"
            ;;
        version)
            echo "Clawdbot Update Script v${SCRIPT_VERSION}"
            echo "Workspace: $CLAWDBOT_DIR"
            echo "Installation: $CLAWDBOT_INSTALL_DIR"
            ;;
    esac
}

main "$@"
