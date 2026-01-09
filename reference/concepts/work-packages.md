# Work Packages

How work flows through agents without requiring you in every handoff.

---

## The Problem with Tasks

Individual tasks create coordination overhead:
```
You → assign task to Agent A
Agent A → completes, reports back
You → review, assign to Agent B
Agent B → completes, reports back
You → review, assign to Agent C
...
```

You're in every handoff. This doesn't scale for a solo founder.

---

## Work Packages: A Better Model

A **work package** is a bundle of related work that flows through agents with defined checkpoints.

```
You → define work package
      ↓
Agents → execute through phases (coordinating via docs)
      ↓
You → checkpoint at key moments
      ↓
Ship
```

You define the work and checkpoint at strategic moments. You don't manage every handoff.

---

## Anatomy of a Work Package

```markdown
## Work Package: [Name]

### Objective
One sentence: what are we delivering?

### Owner
Who's ultimately responsible? (Usually you for important work)

### Phases
| Phase | Agent | Auto-Proceed? |
|-------|-------|---------------|
| Spec | Product Manager | No - founder approves |
| Design | UX Designer | Yes |
| Backend | Backend Engineer | Yes |
| Frontend | Frontend Engineer | Yes |
| Test | QA Engineer | Yes |
| Security | Security Engineer | No - founder approves |
| Ship | Platform Engineer | No - founder approves |

### Founder's Role
- **Architect:** Set technical direction upfront
- **Reviewer:** Approve at checkpoints
- **Builder:** May implement [specific parts]

### Key Decisions (already made)
| Decision | Rationale |
|----------|-----------|
| Use Google OAuth | Simplicity for MVP |
| Store in PostgreSQL | Existing infrastructure |

### Decisions Deferred
- Token refresh strategy (decide during implementation)

### Success Criteria
- [ ] User can sign in with Google
- [ ] Session persists across app restarts
- [ ] Secure token handling

### Estimated Phases
- Spec: 1 session
- Implementation: 2-3 sessions
- QA + Security: 1 session
```

---

## Phase Transitions

### Auto-Proceed Phases

When the current phase completes, the next agent can pick up without waiting for you:

```markdown
### Handoff: Backend → Frontend

**State:** Backend complete, Frontend starting

**For Frontend Engineer:**
- API endpoints documented in cross-agent notes
- Types in `lib/types.ts`
- Proceed with UI implementation

**For Founder (FYI):**
- Backend used connection pooling pattern
- Added 3 tests for auth flow
- No decisions needed
```

### Checkpoint Phases

You review before the next phase begins:

```markdown
### Checkpoint: Before Ship

**Work Package:** User Authentication

**Completed:**
- [x] Spec (approved Jan 15)
- [x] Backend (2 endpoints, 5 tests)
- [x] Frontend (3 screens, error handling)
- [x] QA (passed all criteria)
- [x] Security (approved with notes)

**For Founder:**
- Ready to ship
- Security noted: add rate limiting in Phase 2
- Recommend: ship now, rate limiting next sprint

**Decision Needed:** Ship / Hold / Modify
```

---

## Work Package States

```
┌─────────────┐
│   DRAFT     │ ← You're defining it
└──────┬──────┘
       ↓
┌─────────────┐
│   ACTIVE    │ ← Agents are working
└──────┬──────┘
       ↓
┌─────────────┐
│  CHECKPOINT │ ← Waiting for you
└──────┬──────┘
       ↓
┌─────────────┐
│  COMPLETE   │ ← Shipped or closed
└─────────────┘
```

**BLOCKED** can happen at any point — requires attention.

---

## Tracking in _AGENTS.md

```markdown
## Work Packages

### Active

| Package | Phase | Agent | State | Blocking? |
|---------|-------|-------|-------|-----------|
| User Auth | Frontend | Frontend Eng | Working | No |
| Dashboard | Spec | Product Mgr | Checkpoint | Yes - scope |

### Queued
| Package | Next Phase | Waiting For |
|---------|------------|-------------|
| Notifications | Spec | User Auth to complete |

### Completed (Last 14 Days)
| Package | Shipped | Notes |
|---------|---------|-------|
| Profile Page | Jan 14 | No issues |
| Settings | Jan 12 | Minor bug fixed Jan 13 |
```

---

## Founder Checkpoints

You don't review everything. Define where you checkpoint:

### Typical Checkpoint Pattern

```
Spec          → CHECKPOINT (approve scope)
Design        → Auto-proceed (unless major UX change)
Backend       → Auto-proceed
Frontend      → Auto-proceed
QA            → Auto-proceed (unless failures)
Security      → CHECKPOINT (before ship)
Ship          → CHECKPOINT (you press the button)
```

### High-Risk Pattern (new domain, complex feature)

```
Spec          → CHECKPOINT
Design        → CHECKPOINT
Backend       → CHECKPOINT (review architecture)
Frontend      → Auto-proceed
QA            → CHECKPOINT (review coverage)
Security      → CHECKPOINT
Ship          → CHECKPOINT
```

### Low-Risk Pattern (bug fix, small enhancement)

```
Implementation → Auto-proceed
QA             → Auto-proceed
Ship           → CHECKPOINT
```

---

## Parallel Work Packages

You can have multiple packages in flight:

```
Package A: [Spec] → [Build] → [QA] → Ship
Package B:         [Spec] → [Build] → [QA]
Package C:                  [Spec] → [Build]
```

Agents work on their current phase. You checkpoint strategically.

**Warning:** Too many parallel packages = coordination overhead. 2-3 active is usually right.

---

## Creating a Work Package

### 1. Start from Roadmap
Your `_ROADMAP.md` has features. Pick one to package.

### 2. Define Objective and Success Criteria
What does "done" look like?

### 3. Set Your Involvement Level
- Where will you architect?
- Where will you build?
- Where will you just checkpoint?

### 4. Make Key Decisions Upfront
The more you decide now, the less agents need to ask.

### 5. Add to _AGENTS.md
Create the package entry, set initial phase.

### 6. Activate First Agent
```
You are ~/projects/jebidiah/docs/roles/product-manager.md

Work package "User Auth" is starting. Read the package definition
in docs/_AGENTS.md and create the spec.
```

---

## Work Package Anti-Patterns

### Too Big
A package that takes weeks with many phases.
**Fix:** Break into smaller, shippable packages.

### Too Vague
"Make the app better"
**Fix:** Specific objective and success criteria.

### No Checkpoints
Everything auto-proceeds, you're surprised at the end.
**Fix:** At least spec and ship checkpoints.

### Too Many Checkpoints
You're in every handoff again.
**Fix:** Trust agents between major phases.

### Orphaned Package
Started but nobody's working on it.
**Fix:** Active packages should have an active agent or be paused.

---

## Example: Complete Work Package Flow

**Day 1 Morning:**
```markdown
## Work Package: Password Reset

### Objective
Users can reset their password via email.

### Phases
| Phase | Agent | Checkpoint? |
|-------|-------|-------------|
| Spec | Product Manager | Yes |
| Backend | Backend Engineer | No |
| Frontend | Frontend Engineer | No |
| QA | QA Engineer | No |
| Ship | Platform Engineer | Yes |

### Key Decisions
- Use Supabase built-in password reset
- Simple email template

### Success Criteria
- [ ] User can request reset from login screen
- [ ] Email arrives within 30 seconds
- [ ] Link works and allows password change
- [ ] Old password invalidated
```

**Day 1: Activate Product Manager**
- Creates spec
- Marks checkpoint for your review

**Day 1 Evening: You Review**
- Approve spec
- Set to auto-proceed

**Day 2: Agents Execute**
- Backend implements
- Handoff to Frontend
- Frontend implements
- Handoff to QA
- QA passes

**Day 2 Evening: Final Checkpoint**
- You review: Ready to ship
- Approve → Platform deploys

**Total founder time:** ~30 minutes across 2 days
**Total work delivered:** Complete feature with tests

---

## Summary

| Concept | Purpose |
|---------|---------|
| **Work Package** | Bundle of work that flows through agents |
| **Phases** | Steps in the flow (Spec → Build → Test → Ship) |
| **Checkpoints** | Where you review and approve |
| **Auto-Proceed** | Where agents coordinate without you |
| **State** | Draft → Active → Checkpoint → Complete |

The goal: **You define and checkpoint. Agents execute and coordinate.**
