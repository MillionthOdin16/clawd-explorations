---
spec: improve-test
phase: tasks
total_tasks: 2
created: 2026-01-15T18:40:00Z
---

# Tasks: Test Improvement Cycle

## Phase 1: Make It Work

- [ ] 1.1 Create calculator.py with add(a, b) function
  **Do**: Create calculator.py with add(a, b) function
  **Files**: calculator.py
  **Verify**: python -c "from calculator import add; assert add(2, 3) == 5" && echo "PASS"
  **Commit**: feat: add calculator.py with add function

- [ ] 1.2 Create multiplier.py with multiply(a, b) function
  **Do**: Create multiplier.py with multiply(a, b) function
  **Files**: multiplier.py
  **Verify**: python -c "from multiplier import multiply; assert multiply(2, 3) == 6" && echo "PASS"
  **Commit**: feat: add multiplier.py with multiply function
