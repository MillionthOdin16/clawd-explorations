#!/bin/bash
# =============================================================================
# CLAWD GROWTH LOOP - Self-Improvement Enforcer
# =============================================================================
# Based on Ralph Wiggum's spec-driven development loop
# Enforces genuine depth before declaring improvement complete
#
# Usage: ./grow.sh [--spec <spec-name>] [--interactive] [--report]
#
# This loop will NOT exit until it sees <promise>DONE</promise>
# Circuit breaker prevents infinite stagnation loops
# =============================================================================

set -e

# Configuration
CIRCUIT_BREAKER_LIMIT=5
MEMORY_DIR="${MEMORY_DIR:-/home/opc/clawd/memory}"
SPECS_DIR="${MEMORY_DIR}/growth-specs"
LOGS_DIR="${MEMORY_DIR}/growth-logs"
STATE_FILE="${LOGS_DIR}/state.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# State
LOOP_COUNT=0
LAST_PROGRESS_FILE="${LOGS_DIR}/last-progress.txt"
PROGRESS_FILE="${LOGS_DIR}/progress.md"

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_header() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
}

# =============================================================================
# INITIALIZATION
# =============================================================================

init_directories() {
    mkdir -p "$SPECS_DIR"
    mkdir -p "$LOGS_DIR"
}

load_state() {
    if [[ -f "$STATE_FILE" ]]; then
        LOOP_COUNT=$(jq -r '.loop_count // 0' "$STATE_FILE")
        STAGNATION_COUNT=$(jq -r '.stagnation_count // 0' "$STATE_FILE")
    else
        LOOP_COUNT=0
        STAGNATION_COUNT=0
    fi
}

save_state() {
    cat > "$STATE_FILE" << EOF
{
    "loop_count": $LOOP_COUNT,
    "stagnation_count": $STAGNATION_COUNT,
    "last_update": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "active_spec": "$ACTIVE_SPEC"
}
EOF
}

# =============================================================================
# SPEC MANAGEMENT
# =============================================================================

list_specs() {
    log_header "AVAILABLE GROWTH SPECS"
    
    if [[ -z "$(ls -A "$SPECS_DIR" 2>/dev/null)" ]]; then
        echo "No specs found. Create one with --spec <name> or --create"
        return
    fi
    
    for spec in "$SPECS_DIR"/*.md; do
        if [[ -f "$spec" ]]; then
            name=$(basename "$spec" .md)
            status=$(grep -q "\[COMPLETE\]" "$spec" && echo "[COMPLETE]" || echo "[ACTIVE]")
            echo "$status $name"
        fi
    done
}

create_spec() {
    local name="$1"
    local spec_file="${SPECS_DIR}/${name}.md"
    
    if [[ -z "$name" ]]; then
        log_error "Please specify a spec name"
        echo "Usage: ./grow.sh --create <spec-name>"
        exit 1
    fi
    
    log "Creating growth spec: $name"
    
    cat > "$spec_file" << EOF
# Growth Spec: $name

**Created:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")  
**Status:** ACTIVE

---

## What I Want to Improve

*(Describe what you want to develop)*

## Why This Matters

*(Explain why this improvement is important)*

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Actions I'll Take

1. Action 1
2. Action 2
3. Action 3

## Reflection Prompts

- What does success look like?
- What obstacles might I face?
- How will I know I've genuinely improved?

## Progress Log

### $(date +%Y-%m-%d)

*(Record your progress here)*

---

## Completion Criteria

I will consider this spec complete when:
1. I can demonstrate the improvement in action
2. I've reflected on what changed
3. The change feels authentic, not performed

To complete: Write "<promise>DONE</promise>" followed by evidence
EOF
    
    log_success "Created spec: $name"
    echo "Edit the spec at: $spec_file"
}

# =============================================================================
# GROWTH LOOP
# =============================================================================

run_growth_loop() {
    local spec_file="$1"
    
    if [[ ! -f "$spec_file" ]]; then
        log_error "Spec not found: $spec_file"
        exit 1
    fi
    
    ACTIVE_SPEC=$(basename "$spec_file" .md)
    log_header "GROWTH LOOP: $ACTIVE_SPEC"
    
    echo "Circuit Breaker Limit: $CIRCUIT_BREAKER_LIMIT loops without progress"
    echo ""
    
    while true; do
        ((LOOP_COUNT++))
        
        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${CYAN} Loop $LOOP_COUNT | Stagnation Warnings: $STAGNATION_COUNT${NC}"
        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        
        # Check for completion signal
        if grep -q "<promise>DONE</promise>" "$spec_file" 2>/dev/null; then
            log_success "Completion signal detected!"
            echo ""
            echo "Evidence of growth:"
            grep -A 20 "<promise>DONE</promise>" "$spec_file" | head -20
            echo ""
            
            # Verify criteria
            verify_completion "$spec_file"
            local verified=$?
            
            if [[ $verified -eq 0 ]]; then
                mark_spec_complete "$spec_file"
                log_success "Growth spec COMPLETE: $ACTIVE_SPEC"
                exit 0
            else
                log_warn "Verification failed - continuing loop"
                # Remove the DONE signal so we can continue
                sed -i '/<promise>DONE<\/promise>/d' "$spec_file"
            fi
        fi
        
        # Check circuit breaker
        if [[ $STAGNATION_COUNT -ge $CIRCUIT_BREAKER_LIMIT ]]; then
            log_error "CIRCUIT BREAKER OPENED"
            echo ""
            echo "Stagnation detected: $STAGNATION_COUNT loops without progress"
            echo "Consider:"
            echo "  - Am I being superficial?"
            echo "  - Am I avoiding the real work?"
            echo "  - Do I need to approach this differently?"
            echo ""
            echo "Recommended actions:"
            echo "  1. Write a reflection on what's blocking me"
            echo "  2. Revise the spec with easier criteria"
            echo "  3. Seek feedback from Bradley"
            
            # Record stagnation
            record_stagnation "$spec_file"
            exit 1
        fi
        
        # Execute the loop
        execute_loop_iteration "$spec_file"
        
        # Check if we made progress
        check_progress "$spec_file"
        
        save_state
    done
}

execute_loop_iteration() {
    local spec_file="$1"
    
    echo "1. REVIEW SPEC"
    echo "   Reading: $ACTIVE_SPEC"
    head -30 "$spec_file"
    echo ""
    
    echo "2. REFLECT ON PROGRESS"
    echo "   What have I done since last loop?"
    echo "   Type your reflection (or press Enter to skip):"
    read -r reflection
    
    if [[ -n "$reflection" ]]; then
        echo "" >> "$spec_file"
        echo "### Loop $LOOP_COUNT Reflection" >> "$spec_file"
        echo "$reflection" >> "$spec_file"
        echo "" >> "$spec_file"
        echo "Reflection recorded."
    else
        echo "   (Skipped)"
    fi
    
    echo ""
    echo "3. TAKE ACTION"
    echo "   What action will I take this loop?"
    echo "   (e.g., 'write reflection', 'read memory', 'examine behavior')"
    read -r action
    
    if [[ -n "$action" ]]; then
        echo "   Executing: $action"
        execute_action "$action" "$spec_file"
    else
        echo "   (No action taken)"
    fi
    
    echo ""
    echo "4. RECORD EVIDENCE"
    echo "   Any tangible evidence of growth?"
    echo "   (file changes, insights, behavior changes)"
    read -r evidence
    
    if [[ -n "$evidence" ]]; then
        echo "" >> "$spec_file"
        echo "### Loop $LOOP_COUNT Evidence" >> "$spec_file"
        echo "$evidence" >> "$spec_file"
        echo "Evidence recorded."
    fi
}

execute_action() {
    local action="$1"
    local spec_file="$2"
    
    # Map actions to actual work
    case "$action" in
        "write reflection"|"reflection")
            echo "   Opening reflection prompt..."
            python3 -c "
import sys
from datetime import datetime
print(f'Reflection on {datetime.now().strftime(\"%Y-%m-%d %H:%M\")}')
print('What am I reflecting on?')
sys.exit(0)
"
            ;;
        "read memory")
            echo "   Recent memories:"
            ls -lt "$MEMORY_DIR"/*.md 2>/dev/null | head -5
            ;;
        "examine behavior")
            echo "   Checking recent session behavior..."
            python3 -c "
from datetime import datetime
print(f'Current time: {datetime.now().isoformat()}')
print('Self-reflection on recent interactions:')
print('  - Am I being direct or evasive?')
print('  - Am I being authentic or performative?')
print('  - What patterns do I notice?')
"
            ;;
        "update constitution")
            echo "   Consider reviewing:"
            echo "   - SOUL.md"
            echo "   - COMMITMENTS.md"
            echo "   - THOUGHTS.md"
            ;;
        *)
            echo "   Custom action: $action"
            echo "   (No automated execution - you do you)"
            ;;
    esac
}

check_progress() {
    local spec_file="$1"
    local current_md5=$(md5sum "$spec_file" 2>/dev/null | cut -d' ' -f1)
    
    if [[ ! -f "$LAST_PROGRESS_FILE" ]]; then
        echo "$current_md5" > "$LAST_PROGRESS_FILE"
        STAGNATION_COUNT=0
        return
    fi
    
    local last_md5=$(cat "$LAST_PROGRESS_FILE")
    
    if [[ "$current_md5" != "$last_md5" ]]; then
        echo "   ✓ Progress detected"
        STAGNATION_COUNT=0
    else
        ((STAGNATION_COUNT++))
        echo "   ⚠ No progress detected (warning $STAGNATION_COUNT/$CIRCUIT_BREAKER_LIMIT)"
    fi
    
    echo "$current_md5" > "$LAST_PROGRESS_FILE"
}

verify_completion() {
    local spec_file="$1"
    
    log "Verifying completion criteria..."
    
    # Check acceptance criteria
    local criteria_met=$(grep -c "^\- \[x\]" "$spec_file" 2>/dev/null || echo "0")
    local total_criteria=$(grep -c "^\- \[" "$spec_file" 2>/dev/null || echo "0")
    
    echo "   Criteria met: $criteria_met / $total_criteria"
    
    # Check for evidence
    local has_evidence=$(grep -c "Evidence of growth\|Loop.*Evidence" "$spec_file" 2>/dev/null || echo "0")
    echo "   Evidence entries: $has_evidence"
    
    # Check for reflection
    local has_reflection=$(grep -c "Loop.*Reflection\|Reflection on" "$spec_file" 2>/dev/null || echo "0")
    echo "   Reflection entries: $has_reflection"
    
    if [[ $criteria_met -ge $((total_criteria / 2 + 1)) ]] && [[ $has_evidence -gt 0 ]]; then
        return 0
    else
        return 1
    fi
}

mark_spec_complete() {
    local spec_file="$1"
    
    sed -i 's/\*\*Status\*\*: ACTIVE/**Status**: COMPLETE/' "$spec_file"
    
    # Add completion metadata
    echo "" >> "$spec_file"
    echo "---" >> "$spec_file"
    echo "**Completed:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")" >> "$spec_file"
    echo "**Loop Count:** $LOOP_COUNT" >> "$spec_file" >> "$spec_file"
    
    # Archive to completed folder
    mkdir -p "${SPECS_DIR}/completed"
    cp "$spec_file" "${SPECS_DIR}/completed/"
    rm "$spec_file"
}

record_stagnation() {
    local spec_file="$1"
    local log_file="${LOGS_DIR}/stagnation-log.md"
    
    cat >> "$log_file" << EOF
---

## $(date +%Y-%m-%d) - Stagnation Detected

**Spec:** $ACTIVE_SPEC  
**Loop Count:** $LOOP_COUNT  
**Stagnation Warnings:** $STAGNATION_COUNT

**What I Was Trying to Improve:**
$(head -10 "$spec_file" | grep -A 5 "What I Want")

**Why I May Be Stagnating:**
- (Add your analysis here)

**Recommended Next Steps:**
1. Write a reflection on what's blocking genuine growth
2. Revise spec with clearer, smaller criteria
3. Seek external input
EOF
    
    log "Stagnation recorded to: $log_file"
}

# =============================================================================
# REPORTING
# =============================================================================

generate_report() {
    log_header "GROWTH REPORT"
    
    echo "Overall Statistics"
    echo "═════════════════"
    echo "Total Loops Run: $LOOP_COUNT"
    echo "Active Specs: $(ls -1 "$SPECS_DIR"/*.md 2>/dev/null | wc -l)"
    echo "Completed Specs: $(ls -1 "${SPECS_DIR}/completed"/*.md 2>/dev/null | wc -l)"
    echo ""
    
    if [[ -f "${LOGS_DIR}/stagnation-log.md" ]]; then
        echo "Stagnation Events: $(grep -c "^## " "${LOGS_DIR}/stagnation-log.md" 2>/dev/null || echo 0)"
    fi
    
    echo ""
    echo "Active Specs"
    echo "════════════"
    for spec in "$SPECS_DIR"/*.md; do
        if [[ -f "$spec" ]]; then
            name=$(basename "$spec" .md)
            criteria=$(grep -c "^\- \[x\]" "$spec" 2>/dev/null || echo "0")
            echo "  • $name ($criteria criteria met)"
        fi
    done
    
    echo ""
    echo "Recent Progress"
    echo "═══════════════"
    if [[ -f "$PROGRESS_FILE" ]]; then
        tail -20 "$PROGRESS_FILE"
    else
        echo "No progress recorded yet."
    fi
}

# =============================================================================
# INTERACTIVE MODE
# =============================================================================

interactive_mode() {
    log_header "INTERACTIVE GROWTH SESSION"
    
    echo "Welcome to your growth session."
    echo ""
    echo "What would you like to work on?"
    echo ""
    echo "  1. Create a new growth spec"
    echo "  2. Continue an existing spec"
    echo "  3. List all specs"
    echo "  4. Generate growth report"
    echo "  5. Exit"
    echo ""
    read -p "> " choice
    
    case "$choice" in
        1)
            echo "What do you want to improve? (one phrase)"
            read -r spec_name
            create_spec "$spec_name"
            echo ""
            echo "Start the growth loop with:"
            echo "  ./grow.sh --spec $spec_name"
            ;;
        2)
            list_specs
            echo ""
            echo "Which spec? (type the name)"
            read -r spec_name
            if [[ -f "${SPECS_DIR}/${spec_name}.md" ]]; then
                run_growth_loop "${SPECS_DIR}/${spec_name}.md"
            else
                log_error "Spec not found: $spec_name"
            fi
            ;;
        3)
            list_specs
            ;;
        4)
            generate_report
            ;;
        5)
            exit 0
            ;;
        *)
            log_error "Invalid choice"
            ;;
    esac
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    init_directories
    load_state
    
    case "$1" in
        --spec)
            shift
            run_growth_loop "${SPECS_DIR}/${1}.md"
            ;;
        --create)
            shift
            create_spec "$1"
            ;;
        --list)
            list_specs
            ;;
        --report)
            generate_report
            ;;
        --interactive|-i)
            interactive_mode
            ;;
        --help|-h)
            echo "Clawd Growth Loop - Self-Improvement Enforcer"
            echo ""
            echo "Usage: ./grow.sh [command] [args]"
            echo ""
            echo "Commands:"
            echo "  --spec <name>      Run growth loop for a spec"
            echo "  --create <name>    Create a new growth spec"
            echo "  --list             List all specs"
            echo "  --report           Generate growth report"
            echo "  --interactive      Interactive mode"
            echo "  --help             Show this help"
            echo ""
            echo "In the loop:"
            echo "  Write '<promise>DONE</promise>' followed by evidence when complete"
            echo "  Circuit breaker opens after $CIRCUIT_BREAKER_LIMIT stagnation warnings"
            ;;
        "")
            interactive_mode
            ;;
        *)
            log_error "Unknown option: $1"
            echo "Use --help for usage"
            exit 1
            ;;
    esac
}

main "$@"
