# Chapter 1: The Model

The mechanics behind your AI team.

---

## How Agents Work

Agents are AI (like Claude) given a specific role and context. When you activate an agent, it:

1. **Reads its role file** — Understands what it does and doesn't do
2. **Reads your project's status** — Knows what's happening, what's needed
3. **Does the work** — Writes code, creates specs, runs tests
4. **Updates the status** — Records what it did for you and other agents

Agents don't have memory between sessions. They get context by reading files. This means everything important is written down — which is actually how good teams work anyway.

---

## Work Packages

Work flows through agents in bundles called **work packages**.

A work package is a piece of work that:
- Has a clear goal ("User can reset their password")
- Flows through phases (Spec → Design → Build → Test → Ship)
- Has different agents responsible for each phase

Example:

```
Work Package: Password Reset

Phase 1: Spec
├── Agent: Product Manager
├── Output: User story, acceptance criteria
└── Your action: Approve the scope

Phase 2: Design
├── Agent: UX Designer
├── Output: User flow, wireframes
└── Auto-proceed (no approval needed)

Phase 3: Build
├── Agents: Backend + Frontend Engineers
├── Output: Working code
└── Auto-proceed

Phase 4: Test
├── Agent: QA Engineer
├── Output: Tests passing, bugs documented
└── Auto-proceed (unless bugs found)

Phase 5: Security
├── Agent: Security Engineer
├── Output: Security approval
└── Your action: Review and approve

Phase 6: Ship
├── Agent: Platform Engineer
├── Output: Deployed to production
└── Your action: Press the button
```

---

## Checkpoints and Auto-Proceed

You don't need to be involved in every step. That would defeat the purpose.

**Checkpoints** are where you review and decide:
- Approving the spec (before major work starts)
- Security review (before shipping)
- Ship (you decide when it goes live)

**Auto-proceed** is where agents hand off to each other without waiting for you:
- Design → Build (once spec is approved)
- Build → Test (once code is done)
- Backend → Frontend (once API is ready)

You set up the work, then agents execute. You check in at key moments.

---

## Coordination Through Files

Agents coordinate by reading and writing shared files:

| File | Purpose |
|------|---------|
| `_TODAY.md` | What needs your attention today |
| `_AGENTS.md` | Status of all agents and work packages |
| `_VISION.md` | What you're building and why |
| `_ROADMAP.md` | Priorities and phases |

When the Backend Engineer finishes an API, they write a note in `_AGENTS.md`:

```markdown
### Handoff: Backend Engineer → Frontend Engineer

API for user auth is ready:
- POST /api/auth/login
- POST /api/auth/logout
- Types in lib/types.ts

Proceed with frontend implementation.
```

When the Frontend Engineer starts, they read this note and know exactly what to do.

---

## Why This Works

1. **Shared context** — Everything is written down. No tribal knowledge.
2. **Clear roles** — Each agent knows what they do and don't do.
3. **Defined handoffs** — Agents know how to pass work to each other.
4. **Your judgment where it matters** — You decide strategy and approve key moments.
5. **Execution without you** — Agents work between your check-ins.

---

## What You're Not Doing

You're not:
- Managing calendars and meetings
- Explaining the same context to new hires
- Waiting for people to have availability
- Dealing with sick days, vacations, or turnover
- Negotiating salaries or equity

You're just:
- Setting direction
- Making decisions
- Reviewing work
- Shipping

---

## Summary

| Concept | What It Means |
|---------|--------------|
| **Agents** | AI given specific roles (Product Manager, Engineer, etc.) |
| **Work Packages** | Bundles of work that flow through agents |
| **Phases** | Steps in the flow (Spec → Build → Test → Ship) |
| **Checkpoints** | Where you review and approve |
| **Auto-proceed** | Where agents hand off without waiting for you |
| **Shared files** | How everyone stays coordinated |

---

→ [Chapter 2: Your Role](02_YOUR_ROLE.md)

