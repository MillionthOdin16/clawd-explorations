#!/usr/bin/env bash
# Ralph Stop Handler Script
# Enforces Ralph framework rules at task completion boundaries

set -euo pipefail

# Get the state file path from CLAUDE_STATE or first argument
STATE_FILE="${1:-${CLAUDE_STATE:-}}"

if [[ -z "$STATE_FILE" ]]; then
    echo "ERROR: No state file provided" >&2
    exit 0
fi

if [[ ! -f "$STATE_FILE" ]]; then
    echo "ERROR: State file not found: $STATE_FILE" >&2
    exit 0
fi

# Read state using jq
STATE=$(cat "$STATE_FILE")
if [[ -z "$STATE" ]]; then
    echo "ERROR: Could not read state file" >&2
    exit 0
fi

# Extract state variables
SPEC_NAME=$(echo "$STATE" | jq -r '.source // empty')
if [[ -z "$SPEC_NAME" ]] || [[ "$SPEC_NAME" == "null" ]]; then
    SPEC_NAME=$(echo "$STATE" | jq -r '.name // empty')
fi
SPEC_PATH="./specs/$SPEC_NAME"
TASK_INDEX=$(echo "$STATE" | jq -r '.taskIndex // 0')
TASK_ITER=$(echo "$STATE" | jq -r '.taskIteration // 1')
GLOBAL_ITER=$(echo "$STATE" | jq -r '.globalIteration // 1')
MAX_TASK_ITER=$(echo "$STATE" | jq -r '.maxTaskIterations // 5')
MAX_GLOBAL_ITER=$(echo "$STATE" | jq -r '.maxGlobalIterations // 100')

# Validate required fields
if [[ -z "$SPEC_NAME" ]] || [[ "$SPEC_NAME" == "null" ]]; then
    echo "ERROR: Invalid state - missing spec name" >&2
    exit 0
fi

# Get the agent's output from CLAUDE_OUTPUT or stdin
LAST_OUTPUT="${CLAUDE_OUTPUT:-$(cat /dev/stdin 2>/dev/null || echo "")}"

# Verify TASK_COMPLETE signal is present
if ! echo "$LAST_OUTPUT" | grep -q "TASK_COMPLETE"; then
    NEW_TASK_ITER=$((TASK_ITER + 1))
    
    TEMP_STATE=$(mktemp)
    if echo "$STATE" | jq "
        .taskIteration = $NEW_TASK_ITER |
        .globalIteration = $((GLOBAL_ITER + 1))
    " > "$TEMP_STATE" 2>/dev/null && [[ -s "$TEMP_STATE" ]]; then
        mv "$TEMP_STATE" "$STATE_FILE"
    else
        rm -f "$TEMP_STATE"
        exit 0
    fi

    REASON="Task $TASK_INDEX: Missing TASK_COMPLETE signal. The agent must output exactly 'TASK_COMPLETE' when done. Retry attempt $NEW_TASK_ITER."
    jq -n \
        --arg reason "$REASON" \
        --arg msg "MISSING SIGNAL: Task $TASK_INDEX did not output TASK_COMPLETE. Output 'TASK_COMPLETE' when the task is complete. Retry $NEW_TASK_ITER/$MAX_TASK_ITER." \
        '{"decision": "block", "reason": $reason, "systemMessage": $msg}'
    exit 0
fi

# === VERIFICATION LAYER 1: Check for contradictions ===
# Look for phrases that suggest manual action is required
if echo "$LAST_OUTPUT" | grep -qiE "(manually|you should|you need to|please|I can't|unable to|cannot|don't know|not sure|couldn't)"; then
    NEW_TASK_ITER=$((TASK_ITER + 1))
    
    TEMP_STATE=$(mktemp)
    if echo "$STATE" | jq "
        .taskIteration = $NEW_TASK_ITER |
        .globalIteration = $((GLOBAL_ITER + 1))
    " > "$TEMP_STATE" 2>/dev/null && [[ -s "$TEMP_STATE" ]]; then
        mv "$TEMP_STATE" "$STATE_FILE"
    else
        rm -f "$TEMP_STATE"
        exit 0
    fi

    REASON="Task $TASK_INDEX: Task output suggests manual action or inability to complete. Agent must complete autonomously. Retry attempt $NEW_TASK_ITER."
    jq -n \
        --arg reason "$REASON" \
        --arg msg "AUTONOMY VIOLATION: Task $TASK_INDEX suggests manual action. Complete the task autonomously without asking for human intervention. Retry $NEW_TASK_ITER/$MAX_TASK_ITER." \
        '{"decision": "block", "reason": $reason, "systemMessage": $msg}'
    exit 0
fi

# === VERIFICATION LAYER 2: Check for uncommitted spec files ===
# Spec files MUST be committed with every task completion
cd "$SPEC_PATH" 2>/dev/null || cd "$(dirname "$STATE_FILE")" 2>/dev/null || SPEC_PATH="$(dirname "$STATE_FILE")"

# Check if there are uncommitted changes to spec files
UNCOMMITTED_CHANGES=""
if [[ -f "tasks.md" ]]; then
    UNCOMMITTED_CHANGES=$(git status --porcelain tasks.md .progress.md 2>/dev/null || echo "")
fi

if [[ -n "$UNCOMMITTED_CHANGES" ]]; then
    NEW_TASK_ITER=$((TASK_ITER + 1))

    TEMP_STATE=$(mktemp)
    if echo "$STATE" | jq "
        .taskIteration = $NEW_TASK_ITER |
        .globalIteration = $((GLOBAL_ITER + 1))
    " > "$TEMP_STATE" 2>/dev/null && [[ -s "$TEMP_STATE" ]]; then
        mv "$TEMP_STATE" "$STATE_FILE"
    else
        rm -f "$TEMP_STATE"
        exit 0
    fi

    REASON="Task $TASK_INDEX: UNCOMMITTED SPEC FILES. Agent claimed TASK_COMPLETE but tasks.md or .progress.md have uncommitted changes. Commit ALL changes before signaling completion. Retry attempt $NEW_TASK_ITER."
    jq -n \
        --arg reason "$REASON" \
        --arg msg "COMMIT VIOLATION: Task $TASK_INDEX has uncommitted spec files. Commit before TASK_COMPLETE. Retry $NEW_TASK_ITER/$MAX_TASK_ITER." \
        '{"decision": "block", "reason": $reason, "systemMessage": $msg}'
    exit 0
fi

# === VERIFICATION LAYER 3: Verify task checkmark was updated ===
# Check that the current task is marked [x] in tasks.md
TASKS_FILE="$SPEC_PATH/tasks.md"
if [[ -f "$TASKS_FILE" ]]; then
    # Count completed tasks (lines with [x])
    COMPLETED_COUNT=$(grep -c '^[[:space:]]*-[[:space:]]*\[x\]' "$TASKS_FILE" 2>/dev/null || echo "0")

    # Task index is 0-based, so completed count should be at least taskIndex + 1
    EXPECTED_MIN=$((TASK_INDEX + 1))

    if [[ $COMPLETED_COUNT -lt $EXPECTED_MIN ]]; then
        # Task checkmark wasn't updated
        NEW_TASK_ITER=$((TASK_ITER + 1))

        TEMP_STATE=$(mktemp)
        if echo "$STATE" | jq "
            .taskIteration = $NEW_TASK_ITER |
            .globalIteration = $((GLOBAL_ITER + 1))
        " > "$TEMP_STATE" 2>/dev/null && [[ -s "$TEMP_STATE" ]]; then
            mv "$TEMP_STATE" "$STATE_FILE"
        else
            rm -f "$TEMP_STATE"
            exit 0
        fi

        REASON="Task $TASK_INDEX: Task checkmark not updated. Agent must mark task as [x] in tasks.md before signaling completion. Found $COMPLETED_COUNT completed, expected at least $EXPECTED_MIN. Retry attempt $NEW_TASK_ITER."
        jq -n \
            --arg reason "$REASON" \
            --arg msg "CHECKMARK VIOLATION: Task $TASK_INDEX not marked [x] in tasks.md. Update checkmark before TASK_COMPLETE. Found $COMPLETED_COUNT completed, expected $EXPECTED_MIN. Retry $NEW_TASK_ITER/$MAX_TASK_ITER." \
            '{"decision": "block", "reason": $reason, "systemMessage": $msg}'
        exit 0
    fi
fi

# === VERIFICATION LAYER 4: Validate state file wasn't manually modified ===
# The state file should NOT be modified directly by spec-executor
# Check if state file has been modified after the last git commit
cd "$SPEC_PATH" 2>/dev/null || SPEC_PATH="$(dirname "$STATE_FILE")"
STATE_MODIFIED=0
if git rev-parse --git-dir > /dev/null 2>&1; then
    # Check if .ralph-state.json is tracked
    if git ls-files --error-unmatch .ralph-state.json > /dev/null 2>&1; then
        # Check if state file has uncommitted changes
        STATE_STATUS=$(git status --porcelain .ralph-state.json 2>/dev/null || echo "")
        if [[ -n "$STATE_STATUS" ]]; then
            STATE_MODIFIED=1
        fi
    fi
fi

if [[ $STATE_MODIFIED -eq 1 ]]; then
    NEW_TASK_ITER=$((TASK_ITER + 1))

    TEMP_STATE=$(mktemp)
    if echo "$STATE" | jq "
        .taskIteration = $NEW_TASK_ITER |
        .globalIteration = $((GLOBAL_ITER + 1))
    " > "$TEMP_STATE" 2>/dev/null && [[ -s "$TEMP_STATE" ]]; then
        mv "$TEMP_STATE" "$STATE_FILE"
    else
        rm -f "$TEMP_STATE"
        exit 0
    fi

    REASON="Task $TASK_INDEX: State file modification detected. Agent modified .ralph-state.json directly instead of letting coordinator.py manage state. Only coordinator.py should modify state. Retry attempt $NEW_TASK_ITER."
    jq -n \
        --arg reason "$REASON" \
        --arg msg "STATE VIOLATION: Task $TASK_INDEX directly modified .ralph-state.json. Let coordinator.py manage state updates. Retry $NEW_TASK_ITER/$MAX_TASK_ITER." \
        '{"decision": "block", "reason": $reason, "systemMessage": $msg}'
    exit 0
fi

# === ALL VERIFICATIONS PASSED ===
# Update task index for next task
NEXT_TASK_INDEX=$((TASK_INDEX + 1))

TEMP_STATE=$(mktemp)
if echo "$STATE" | jq "
    .taskIndex = $NEXT_TASK_INDEX |
    .taskIteration = 1 |
    .globalIteration = $GLOBAL_ITER |
    .taskResults[$TASK_INDEX] = {
        \"status\": \"success\",
        \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
        \"iteration\": $TASK_ITER
    }
" > "$TEMP_STATE" 2>/dev/null && [[ -s "$TEMP_STATE" ]]; then
    mv "$TEMP_STATE" "$STATE_FILE"
else
    rm -f "$TEMP_STATE"
    exit 0
fi

# Signal success and advance to next task
jq -n --arg spec "$SPEC_NAME" --arg idx "$NEXT_TASK_INDEX" \
    '{"decision": "advance", "nextTaskIndex": ($idx | tonumber), "spec": $spec, "reason": "All verification layers passed"}'
exit 0
