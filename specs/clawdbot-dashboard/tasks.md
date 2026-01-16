# Tasks: Clawdbot Web Dashboard

## Overview

Total tasks: 22
POC-first workflow with 4 phases.

> **Quality Checkpoints**: Intermediate quality gate checks are inserted every 2-3 tasks to catch issues early.

## Phase 1: Make It Work (POC)

Focus: Validate the idea works end-to-end. Skip tests, accept hardcoded values.

- [x] 1.1 Initialize Next.js project with TypeScript and shadcn/ui
  - **Do**:
    1. Create directory: `mkdir -p /home/opc/clawd/clawdbot-dashboard`
    2. Initialize Next.js: `cd /home/opc/clawd/clawdbot-dashboard && pnpm create next-app@latest . --typescript --tailwind --app --no-src-dir --import-alias "@/*"`
    3. Initialize shadcn/ui: `pnpm dlx shadcn@latest init -y`
    4. Install dependencies: `pnpm add @tanstack/react-query zustand lucide-react clsx tailwind-merge`
    5. Add shadcn/ui components: `pnpm dlx shadcn@latest add card button badge scroll-area separator tabs input`
  - **Files**: `/home/opc/clawd/clawdbot-dashboard/` (project root)
  - **Done when**: Next.js app runs locally with `pnpm dev` and shows default page
  - **Verify**: `pnpm dev` (browse to http://localhost:3000)
  - **Commit**: `feat: initialize Next.js project with shadcn/ui`
  - _Requirements: FR-9, FR-10_
  - _Design: Component A, Technical Decisions_

- [x] 1.2 Create TypeScript types and interfaces
  - **Do**:
    1. Create `lib/types.ts` with SessionStatus, ToolCall, Message, Task interfaces
    2. Create `lib/apiClient.ts` with ApiClient interface
    3. Export all types from `lib/index.ts`
  - **Files**: `lib/types.ts`, `lib/apiClient.ts`, `lib/index.ts`
  - **Done when**: TypeScript types compile without errors
  - **Verify**: `pnpm tsc --noEmit`
  - **Commit**: `feat: add TypeScript types and interfaces`
  - _Design: Interfaces_

- [x] 1.3 Create API client with mocked Gateway responses
  - **Do**:
    1. Implement `ApiClient` class in `lib/apiClient.ts`
    2. Add methods: `getSessionStatus()`, `getToolCalls()`, `getMessages()`, `getTasks()`
    3. Return mock data matching the interfaces
    4. Add environment variable for `NEXT_PUBLIC_GATEWAY_API_URL`
  - **Files**: `lib/apiClient.ts`
  - **Done when**: API client instance can be created and returns mock data
  - **Verify**: Create test file to verify mock data structure
  - **Commit**: `feat: implement API client with mock responses`
  - _Requirements: FR-6_
  - _Design: ApiClient_

- [x] 1.4 Quality Checkpoint
  - **Do**: Run all quality checks to verify recent changes don't break the build
  - **Verify**: All commands must pass:
    - Type check: `pnpm tsc --noEmit`
    - Lint: `pnpm lint` (or `pnpm next lint`)
  - **Done when**: All quality checks pass with no errors
  - **Commit**: `chore: pass quality checkpoint` (only if fixes needed)

- [x] 1.5 Create DashboardLayout component
  - **Do**:
    1. Create `components/DashboardLayout.tsx`
    2. Add theme toggle (light/dark mode) using next-themes
    3. Create responsive container layout
    4. Add loading state overlay
    5. Add connection status indicator in header
  - **Files**: `components/DashboardLayout.tsx`, `app/layout.tsx` (modify)
  - **Done when**: Layout displays correctly in light and dark modes
  - **Verify**: `pnpm dev` and toggle theme
  - **Commit**: `feat: add DashboardLayout with theme support`
  - _Requirements: FR-9, FR-10_
  - _Design: DashboardLayout_

- [x] 1.6 Create SessionHeader component
  - **Do**:
    1. Create `components/SessionHeader.tsx`
    2. Display session ID, creation time, model info
    3. Display runtime environment (host, OS, node version)
    4. Show status badge (running/idle/processing)
    5. Use mock data for initial testing
  - **Files**: `components/SessionHeader.tsx`
  - **Done when**: Session header displays mock session data
  - **Verify**: `pnpm dev` and verify header shows mock data
  - **Commit**: `feat: add SessionHeader component`
  - _Requirements: FR-1, AC-1.1, AC-1.2, AC-1.3, AC-1.4_
  - _Design: SessionHeader_

- [x] 1.7 Create ToolCallStream component
  - **Do**:
    1. Create `components/ToolCallStream.tsx`
    2. Display tool calls in chronological order
    3. Color-code status (running=yellow, success=green, error=red)
    4. Add expandable details for parameters/results
    5. Add filter input for tool name
    6. Add status filter dropdown
    7. Use mock data for initial testing
    8. Implement auto-scroll to latest tool call
  - **Files**: `components/ToolCallStream.tsx`
  - **Done when**: Tool call stream displays mock data with filters working
  - **Verify**: `pnpm dev` and verify tool calls render with filters
  - **Commit**: `feat: add ToolCallStream component`
  - _Requirements: FR-2, AC-2.1, AC-2.2, AC-2.3, AC-2.4, AC-2.5, AC-2.6_
  - _Design: ToolCallStream_

- [x] 1.8 Quality Checkpoint
  - **Do**: Run all quality checks to verify recent changes don't break the build
  - **Verify**: All commands must pass:
    - Type check: `pnpm tsc --noEmit`
    - Lint: `pnpm lint`
  - **Done when**: All quality checks pass with no errors
  - **Commit**: `chore: pass quality checkpoint` (only if fixes needed)

- [x] 1.9 Create MessageStream component
  - **Do**:
    1. Create `components/MessageStream.tsx`
    2. Display messages in chronological order
    3. Distinguish user vs. assistant messages visually
    4. Show message timestamps
    5. Add markdown rendering (use react-markdown)
    6. Implement auto-scroll to latest message
    7. Use mock data for initial testing
  - **Files**: `components/MessageStream.tsx`, install `react-markdown` with pnpm
  - **Done when**: Message stream displays mock data with markdown rendering
  - **Verify**: `pnpm dev` and verify messages render with markdown
  - **Commit**: `feat: add MessageStream component with markdown`
  - _Requirements: FR-3, AC-3.1, AC-3.2, AC-3.3, AC-3.4, AC-3.5_
  - _Design: MessageStream_

- [x] 1.10 Create ReasoningPanel component
  - **Do**:
    1. Create `components/ReasoningPanel.tsx`
    2. Display reasoning tokens/content when available
    3. Make panel collapsible (default collapsed)
    4. Render reasoning with appropriate formatting
    5. Show "No reasoning available" when data is empty
    6. Use mock data for initial testing
  - **Files**: `components/ReasoningPanel.tsx`
  - **Done when**: Reasoning panel displays mock data and collapses/expands
  - **Verify**: `pnpm dev` and verify panel works
  - **Commit**: `feat: add ReasoningPanel component`
  - _Requirements: FR-4, AC-4.1, AC-4.2, AC-4.3, AC-4.4_
  - _Design: ReasoningPanel_

- [x] 1.11 Create TaskTracker component
  - **Do**:
    1. Create `components/TaskTracker.tsx`
    2. Display task list with status indicators (pending, in-progress, complete)
    3. Show task descriptions and priorities
    4. Add visual progress indicators
    5. Add filter by task status
    6. Use mock data for initial testing
  - **Files**: `components/TaskTracker.tsx`
  - **Done when**: Task tracker displays mock data with filters working
  - **Verify**: `pnpm dev` and verify tasks render with filters
  - **Commit**: `feat: add TaskTracker component`
  - _Requirements: FR-5, AC-5.1, AC-5.2, AC-5.3, AC-5.4, AC-5.5_
  - _Design: TaskTracker_

- [x] 1.12 Quality Checkpoint
  - **Do**: Run all quality checks to verify recent changes don't break the build
  - **Verify**: All commands must pass:
    - Type check: `pnpm tsc --noEmit`
    - Lint: `pnpm lint`
  - **Done when**: All quality checks pass with no errors
  - **Commit**: `chore: pass quality checkpoint` (only if fixes needed)

- [x] 1.13 Create Zustand store for global state
  - **Do**:
    1. Create `lib/store.ts` with Zustand store
    2. Store: sessionStatus, toolCalls, messages, reasoning, tasks
    3. Add actions to update each state slice
    4. Add connection status to store
  - **Files**: `lib/store.ts`
  - **Done when**: Store can be created and state updates work
  - **Verify**: Create simple test to verify store actions
  - **Commit**: `feat: add Zustand global state store`
  - _Design: State_

- [x] 1.14 Integrate React Query for data fetching
  - **Do**:
    1. Wrap app with QueryProvider in `app/layout.tsx`
    2. Create hooks for each data type:
       - `useSessionStatus()` - fetch session status
       - `useToolCalls()` - fetch tool calls
       - `useMessages()` - fetch messages
       - `useTasks()` - fetch tasks
    3. Configure polling intervals (5 seconds)
    4. Enable refetchOnWindowFocus and staleTime
  - **Files**: `app/layout.tsx` (modify), create `lib/hooks.ts`
  - **Done when**: React Query fetches and caches data properly
  - **Verify**: `pnpm dev` and check browser dev tools for network requests
  - **Commit**: `feat: integrate React Query for data fetching`
  - _Requirements: NFR-2_
  - _Design: React Query_

- [x] 1.15 Connect components to real data
  - **Do**:
    1. Replace mock data in components with React Query hooks
    2. Update DashboardLayout to use real session status
    3. Update all components to display real data
    4. Add loading states and error boundaries
    5. Add retry logic for failed requests
  - **Files**: All component files modify
  - **Done when**: All components display data from API client
  - **Verify**: `pnpm dev` with real Gateway API URL in env
  - **Commit**: `feat: connect components to real Gateway API`
  - _Requirements: All FRs_
  - _Design: Data Flow_

- [x] 1.16 POC Checkpoint
  - **Do**: Verify feature works end-to-end
  - **Done when**:
    - Dashboard loads and displays session data
    - Tool calls, messages, reasoning, tasks all display
    - Auto-refresh works (observe updates every 5s)
    - Filters work on tool calls and tasks
    - Dark mode toggle works
    - Responsive design works on mobile viewport
  - **Verify**: Manual test of core flow with Gateway API
  - **Commit**: `feat: complete POC - dashboard works end-to-end`
  - _Requirements: All requirements_

## Phase 2: Refactoring

After POC validated, clean up code.

- [x] 2.1 Extract common UI patterns
  - **Do**:
    1. Create `components/ui/StatusBadge.tsx` for consistent status display
    2. Create `components/ui/LoadingSpinner.tsx` for loading states
    3. Create `components/ui/EmptyState.tsx` for empty data states
    4. Update components to use shared UI components
  - **Files**: `components/ui/StatusBadge.tsx`, `components/ui/LoadingSpinner.tsx`, `components/ui/EmptyState.tsx`
  - **Done when**: No duplicate status/loading code across components
  - **Verify**: `pnpm lint` passes
  - **Commit**: `refactor: extract common UI components`
  - _Design: Component refactoring_

- [x] 2.2 Improve error handling
  - **Do**:
    1. Add try/catch to all API client methods
    2. Add error boundary in app layout
    3. Add error toast notifications using sonner (or toast from shadcn)
    4. Add retry logic with exponential backoff
    5. Add rate limit handling
  - **Files**: `lib/apiClient.ts`, `app/layout.tsx`, install `sonner` or use shadcn toast
  - **Done when**: All error paths handled gracefully
  - **Verify**: Test with invalid API URL to see error handling
  - **Commit**: `refactor: add comprehensive error handling`
  - _Design: Error Handling_

- [x] 2.3 Quality Checkpoint
  - **Do**: Run all quality checks to verify refactoring doesn't break the build
  - **Verify**: All commands must pass:
    - Type check: `pnpm tsc --noEmit`
    - Lint: `pnpm lint`
  - **Done when**: All quality checks pass with no errors
  - **Commit**: `chore: pass quality checkpoint` (only if fixes needed)

- [x] 2.4 Optimize performance
  - **Do**:
    1. Add React.memo() to expensive components
    2. Implement virtual scrolling for long lists (use react-window)
    3. Batch rapid updates with debounce (100ms window)
    4. Prune old tool calls after 500 entries
    5. Add pagination to message stream (50 per page)
    6. Lazy load images if any
  - **Files**: Install `react-window`, update components
  - **Done when**: Performance improves (check DevTools Profiler)
  - **Verify**: Load dashboard with 1000+ messages/tool calls and check performance
  - **Commit**: `refactor: optimize performance with virtual scrolling and debouncing`
  - _Design: Performance Considerations_
  - _Requirements: NFR-1, NFR-4_

- [x] 2.5 Code cleanup and type safety
  - **Do**:
    1. Remove all TODOs and hardcoded values
    2. Add proper TypeScript types for all props
    3. Enable strict mode in tsconfig.json
    4. Add JSDoc comments for complex functions
    5. Clean up unused imports and variables
    6. Add proper null checks
  - **Files**: All TypeScript files
  - **Done when**: TypeScript strict mode passes, no TODOs remain
  - **Verify**: `pnpm tsc --noEmit` with strict mode enabled
  - **Commit**: `refactor: cleanup code and improve type safety`
  - _Design: TypeScript_

- [x] 2.6 Quality Checkpoint
  - **Do**: Run all quality checks to verify refactoring doesn't break the build
  - **Verify**: All commands must pass:
    - Type check: `pnpm tsc --noEmit` (strict mode)
    - Lint: `pnpm lint`
  - **Done when**: All quality checks pass with no errors
  - **Commit**: `chore: pass quality checkpoint` (only if fixes needed)

## Phase 3: Testing

- [ ] 3.1 Add unit tests for API client
  - **Do**:
    1. Install testing dependencies: `pnpm add -D @testing-library/react @testing-library/jest-dom @testing-library/user-event vitest @vitejs/plugin-react`
    2. Create `lib/__tests__/apiClient.test.ts`
    3. Mock fetch responses for each API method
    4. Test error handling and retry logic
    5. Test data parsing and validation
  - **Files**: `lib/__tests__/apiClient.test.ts`, `vitest.config.ts`
  - **Done when**: Unit tests cover all API client methods
  - **Verify**: `pnpm test` passes
  - **Commit**: `test: add unit tests for API client`
  - _Design: Test Strategy_

- [ ] 3.2 Add component tests
  - **Do**:
    1. Create `components/__tests__/SessionHeader.test.tsx`
    2. Create `components/__tests__/ToolCallStream.test.tsx`
    3. Create `components/__tests__/MessageStream.test.tsx`
    4. Test component rendering with different props
    5. Test user interactions (filters, expand/collapse)
  - **Files**: Component test files
  - **Done when**: All main components have tests
  - **Verify**: `pnpm test` passes
  - **Commit**: `test: add component tests`
  - _Design: Test Strategy_

- [ ] 3.3 Quality Checkpoint
  - **Do**: Run all quality checks to verify tests don't introduce issues
  - **Verify**: All commands must pass:
    - Type check: `pnpm tsc --noEmit`
    - Lint: `pnpm lint`
    - Tests: `pnpm test`
  - **Done when**: All quality checks pass with no errors
  - **Commit**: `chore: pass quality checkpoint` (only if fixes needed)

- [ ] 3.4 Add E2E tests with Playwright
  - **Do**:
    1. Install Playwright: `pnpm add -D @playwright/test`
    2. Initialize Playwright: `pnpm exec playwright install`
    3. Create `e2e/dashboard.spec.ts` with tests:
       - Load dashboard and verify session header
       - Verify tool calls display and filters work
       - Verify messages display and markdown renders
       - Verify dark mode toggle works
       - Verify responsive design on mobile viewport
    4. Run E2E tests
  - **Files**: `e2e/dashboard.spec.ts`, `playwright.config.ts`
  - **Done when**: All E2E tests pass
  - **Verify**: `pnpm playwright test`
  - **Commit**: `test: add E2E tests with Playwright`
  - _Design: Test Strategy_
  - _Requirements: FR-9, FR-10_

## Phase 4: Quality Gates

> **IMPORTANT**: NEVER push directly to the default branch (main/master). Branch management is handled at startup via `/ralph-specum:start`. You should already be on a feature branch by this phase.

> **Default Behavior**: When on a feature branch (not main/master), the final deliverable is a Pull Request with all CI checks passing. This is the default unless explicitly stated otherwise.

- [ ] 4.1 Local quality check
  - **Do**: Run ALL quality checks locally before creating PR
  - **Verify**: All commands must pass:
    - Type check: `pnpm tsc --noEmit` (strict mode)
    - Lint: `pnpm lint`
    - Tests: `pnpm test` and `pnpm playwright test`
  - **Done when**: All commands pass with no errors
  - **Commit**: `fix: address lint/type/test issues` (if fixes needed)

- [ ] 4.2 Create README with setup and deployment instructions
  - **Do**:
    1. Create `README.md` with:
       - Project overview
       - Prerequisites (Node.js, pnpm)
       - Installation steps
       - Development server startup
       - Environment variables required
       - Deployment to Coolify instructions
       - Troubleshooting common issues
  - **Files**: `README.md`
  - **Done when**: README is comprehensive and accurate
  - **Verify**: Follow README instructions from scratch
  - **Commit**: `docs: add comprehensive README`
  - _Requirements: All requirements_

- [ ] 4.3 Add .env.example with required variables
  - **Do**:
    1. Create `.env.example` with:
       - `NEXT_PUBLIC_GATEWAY_API_URL=http://localhost:3000`
       - `NEXT_PUBLIC_GATEWAY_API_KEY=your-api-key-here`
  - **Files**: `.env.example`
  - **Done when**: All required variables documented
  - **Verify**: Copy .env.example to .env and verify app runs
  - **Commit**: `docs: add environment variables example`

- [ ] 4.4 Create Dockerfile for Coolify deployment
  - **Do**:
    1. Create `Dockerfile`:
       - Use Node.js 22-alpine as base
       - Install dependencies with pnpm
       - Build Next.js app
       - Set up production start command
    2. Create `.dockerignore` to exclude unnecessary files
  - **Files**: `Dockerfile`, `.dockerignore`
  - **Done when**: Docker image builds successfully
  - **Verify**: `docker build -t clawdbot-dashboard .`
  - **Commit**: `feat: add Dockerfile for deployment`

- [ ] 4.5 Create PR and verify CI
  - **Do**:
    1. Verify current branch is a feature branch: `git branch --show-current`
    2. If on default branch, STOP and alert user (branch should be set at startup)
    3. Push branch: `git push -u origin $(git branch --show-current)`
    4. Create PR using gh CLI (if available):
       ```bash
       gh pr create --title "feat: Clawdbot Web Dashboard" --body "## Summary
       Built a beautiful real-time web dashboard that displays Clawdbot's internal state, tasks, tool calls, messages, and reasoning process with full transparency.

       ## Features
       - Session status display with connection indicator
       - Real-time tool call stream with filters
       - Message stream with markdown rendering
       - Reasoning panel with collapsible view
       - Task tracker with status indicators
       - Dark mode support
       - Responsive design

       ## Tech Stack
       - Next.js 14 (App Router)
       - TypeScript
       - Tailwind CSS
       - shadcn/ui components
       - React Query for data fetching
       - Zustand for state management

       ## Test Plan
       - [x] Local quality gates pass (types, lint, tests)
       - [ ] CI checks pass"
       ```
    5. If gh CLI unavailable, output: "Create PR at: https://github.com/<org>/<repo>/compare/<branch>"
  - **Verify**: Use gh CLI to verify CI status:
    ```bash
    # Wait for CI and watch status
    gh pr checks --watch

    # Or check current status
    gh pr checks

    # Get detailed status
    gh pr view --json statusCheckRollup --jq '.statusCheckRollup[] | "\(.name): \(.conclusion)"'
    ```
  - **Done when**: All CI checks show ✓ (passing), PR ready for review
  - **If CI fails**:
    1. View failures: `gh pr checks`
    2. Get detailed logs: `gh run view <run-id> --log-failed`
    3. Fix issues locally
    4. Commit and push: `git add . && git commit -m "fix: address CI failures" && git push`
    5. Re-verify: `gh pr checks --watch`

- [ ] 4.6 Merge after approval (optional - only if explicitly requested)
  - **Do**: Merge PR after approval and CI green
  - **Verify**: `gh pr merge --auto` or manual merge
  - **Done when**: Changes in main branch
  - **Note**: Do NOT auto-merge unless user explicitly requests it

## Notes

- **POC shortcuts taken**:
  - Mock data used initially in components
  - No tests in Phase 1
  - Hardcoded polling interval (5s)
  - Simple API key authentication (not OAuth)
  - Polling instead of WebSocket (upgrade later)

- **Production TODOs**:
  - Implement WebSocket for true real-time updates
  - Add OAuth authentication
  - Implement proper pagination for message history
  - Add data export functionality
  - Add multi-session view
  - Implement server-side rendering for initial load
  - Add analytics/monitoring

## Dependencies

```
Phase 1 (POC) → Phase 2 (Refactor) → Phase 3 (Testing) → Phase 4 (Quality)
```
