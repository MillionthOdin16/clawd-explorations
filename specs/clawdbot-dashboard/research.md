---
spec: clawdbot-dashboard
phase: research
created: 2026-01-16
---

# Research: Clawdbot Web Dashboard

## Executive Summary

Building a real-time web dashboard for Clawdbot is technically feasible using modern web technologies. The dashboard will integrate with existing Clawdbot session systems via its API/Gateway, providing visibility into internal state, tool calls, message streams, and reasoning processes. Key challenges include real-time data streaming, authentication/authorization, and managing data volumes efficiently.

## External Research

### Best Practices

**Real-Time Dashboard Architecture:**
- Use WebSockets or Server-Sent Events (SSE) for live updates (Source: https://www.smashingmagazine.com/2024/01/building-real-time-web-applications/)
- Implement optimistic UI updates with eventual consistency (Source: https://stripe.com/blog/real-time-updates)
- Use React Query or SWR for data fetching with caching and synchronization (Source: https://tanstack.com/query/latest)

**Dashboard Design Patterns:**
- Modular card-based layout for different data streams (Source: https://ui.shadcn.com/docs/components/card)
- Color-coded severity levels for state indicators (Source: https://tailwindcss.com/docs/customizing-colors)
- Collapsible sections for managing information density (Source: https://dribbble.com/shots/dashboard)

**Performance Optimization:**
- Virtual scrolling for large message streams (Source: https://react-window.vercel.app/)
- Debounce/throttle rapid updates to prevent UI thrashing (Source: https://lodash.com/docs/#debounce)
- Implement pagination for historical data (Source: https://www.prisma.io/docs/concepts/components/prisma-client/pagination)

### Prior Art

**Similar Projects:**
- **OpenAI Playground**: Real-time streaming of AI responses with token-by-token visibility
- **Vercel AI Dashboard**: Displays model metrics, latency, and error rates
- **LangSmith**: Tracing tool calls, reasoning chains, and intermediate steps
- **GitHub Copilot Dashboard**: Shows usage statistics and suggestions

**Relevant Patterns:**
- LangSmith's trace visualization showing chain-of-thought steps
- OpenAI's streaming response rendering
- Claude's reasoning token display

### Pitfalls to Avoid

- **Over-fetching**: Don't request all historical data on load - implement pagination
- **UI Thrashing**: Batch rapid updates (100ms windows) instead of re-rendering on every event
- **Memory Leaks**: Clean up WebSocket connections and event listeners on unmount
- **Information Overload**: Provide sensible defaults with expandable details
- **Authentication Security**: Never expose internal API keys to the frontend

## Codebase Analysis

### Existing Patterns

**Clawdbot Session System:**
- Session data stored in structured format (File: MEMORY.md, AGENTS.md)
- Tool calls logged in session logs with timestamps
- Reasoning process captured in session history
- Message streams available via sessions_history API

**API Gateway:**
- Gateway provides REST API endpoints for session management
- Real-time updates potentially available via Gateway webhooks or streaming
- Plugin system for extensibility (File: TOOLS.md mentions message tool)

**Deployment Infrastructure:**
- Coolify for deployment management (File: skills/coolify/)
- Docker containerization available
- Existing web applications deployable (e.g., Terry's Eagles HQ)

### Dependencies

**Existing Dependencies:**
- Node.js v22.20.0 available on host
- Gateway API already running
- Coolify integration for deployment

**Required New Dependencies:**
- **Frontend Framework**: Next.js 14+ (App Router) for SSR and API routes
- **UI Components**: shadcn/ui for beautiful, accessible components
- **Real-time**: Socket.io or native WebSocket implementation
- **Styling**: Tailwind CSS
- **State Management**: Zustand or React Context for client state
- **Data Fetching**: React Query for server state
- **Type Safety**: TypeScript
- **Icons**: Lucide React

### Constraints

**Technical Limitations:**
- Gateway API rate limiting may affect real-time updates
- Session log file sizes could be large (need efficient reading)
- No existing WebSocket infrastructure in Gateway (may need custom implementation)
- Authentication required (cannot expose internal state publicly)

**Architectural Constraints:**
- Frontend must be deployed separately from Clawdbot (security)
- Need to implement API proxy layer to avoid exposing Gateway internals
- Must handle offline/degraded states gracefully

## Related Specs

| Spec | Relevance | Relationship | May Need Update |
|------|-----------|--------------|-----------------|
| None | N/A | This is a new feature area | No |

### Coordination Notes
This is a standalone feature that integrates with existing Clawdbot systems but doesn't conflict with other specs. No coordination needed with existing work.

## Feasibility Assessment

| Aspect | Assessment | Notes |
|--------|------------|-------|
| Technical Viability | High | Modern web stack + existing API = straightforward |
| Effort Estimate | L (Large) | Full-stack app with real-time features, ~2-3 weeks |
| Risk Level | Medium | Real-time streaming complexity, API integration |

## Recommendations for Requirements

1. **Start with MVP**: Focus on read-only visibility first (no controls)
2. **Modular Architecture**: Design each section (state, tools, messages, reasoning) as independent components
3. **Progressive Enhancement**: Basic polling first, upgrade to WebSockets if needed
4. **Security-First**: Implement authentication from day one (no public access)
5. **Mobile-Responsive**: Design for mobile and desktop from start

## Open Questions

- Does Gateway provide WebSocket or SSE endpoints for real-time updates?
- What authentication mechanism should we use (API keys, OAuth, custom)?
- Should we store historical data in the dashboard app or query Gateway on demand?
- What are the expected data volumes for message/tool call streams?
- Is there a specific refresh rate requirement (real-time vs near-real-time)?

## Sources

- https://ui.shadcn.com/docs/components/card (UI component library)
- https://tanstack.com/query/latest (React Query for data fetching)
- https://tailwindcss.com/docs (Styling framework)
- https://nextjs.org/docs/app (Next.js App Router)
- https://socket.io/docs/v4/ (Real-time communication)
- AGENTS.md (Clawdbot session system)
- TOOLS.md (Tool calling patterns)
- HEARTBEAT.md (Session state tracking)
