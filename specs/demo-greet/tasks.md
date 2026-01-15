---
spec: demo-greet
phase: tasks
total_tasks: 1
created: 2026-01-15T18:20:00Z
---

# Tasks: Demo Greeting Tool

## Phase 1: Make It Work (POC)

- [ ] 1.1 Create greet.py with hello function
  **Do**: Create `greet.py` with function that returns "Hello, World!"
  **Files**: `greet.py`
  **Done when**: `python greet.py` outputs "Hello, World!"
  **Verify**: `python greet.py | grep -q "Hello, World!" && echo "PASS"`
  **Commit**: `feat: add greet.py with hello function`
