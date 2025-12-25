# Chapter 4: The Workflow

How work flows from idea to shipped.

---

## The Big Picture

Every feature follows a path:

```
IDEA → SPEC → DESIGN → BUILD → TEST → SECURITY → SHIP
```

Different agents own different phases. You checkpoint at key moments. The rest flows automatically.

---

## A Work Package

When you have an idea, it becomes a **work package** — a bundle of work that flows through agents.

Here's a simple example:

```markdown
## Work Package: Password Reset

**Objective:** Users can reset their password via email.

**Phases:**
| Phase | Agent | Checkpoint? |
|-------|-------|-------------|
| Spec | Product Manager | Yes — you approve |
| Design | UX Designer | No — auto-proceed |
| Backend | Backend Engineer | No — auto-proceed |
| Frontend | Frontend Engineer | No — auto-proceed |
| Test | QA Engineer | No — auto-proceed |
| Security | Security Engineer | Yes — you approve |
| Ship | Platform Engineer | Yes — you decide |

**Success Criteria:**
- User can request reset from login screen
- Email arrives within 30 seconds
- Link works and allows password change
```

---

## The Phases

### Phase 1: Spec

**Agent:** Product Manager

**What happens:**
- PM takes your idea and creates a clear spec
- Defines user stories, acceptance criteria
- Identifies what's in scope and out of scope
- Surfaces questions and decisions

**Your action:** Review and approve the spec.

**Example output:**
```markdown
## Password Reset Spec

### User Story
As a user who forgot my password, I want to reset it via email
so I can regain access to my account.

### Acceptance Criteria
- [ ] "Forgot password" link on login screen
- [ ] Email input with validation
- [ ] Email sent within 30 seconds
- [ ] Reset link expires after 1 hour
- [ ] New password must meet requirements
- [ ] Old sessions invalidated after reset

### Out of Scope
- SMS reset (future)
- Security questions (not doing)
```

---

### Phase 2: Design

**Agent:** UX Designer (sometimes UI Designer too)

**What happens:**
- Creates user flow
- Wireframes key screens
- Handles edge cases (error states, loading)

**Your action:** None (auto-proceed) — unless major UX change.

**Example output:**
```
User Flow:
Login Screen → "Forgot Password" → Email Input →
"Check your email" → Click Link → New Password Form →
"Password updated" → Redirect to Login
```

---

### Phase 3: Backend

**Agent:** Backend Engineer

**What happens:**
- Implements API endpoints
- Handles email sending
- Database changes if needed
- Writes tests

**Your action:** None (auto-proceed).

**Handoff note:**
```markdown
### Handoff: Backend → Frontend

API ready:
- POST /api/auth/forgot-password
- POST /api/auth/reset-password

Types in lib/types.ts. Tests in __tests__/api/auth.test.ts.
```

---

### Phase 4: Frontend

**Agent:** Frontend Engineer

**What happens:**
- Builds the screens
- Connects to APIs
- Handles loading, errors, success states

**Your action:** None (auto-proceed).

---

### Phase 5: Test

**Agent:** QA Engineer

**What happens:**
- Tests against acceptance criteria
- Finds edge cases
- Reports bugs (if any)

**Your action:** None (auto-proceed) — unless bugs are found.

**If bugs found:**
```markdown
### Bug: Reset link doesn't expire

**Severity:** High
**Steps:** Request reset, wait 2 hours, click link
**Expected:** "Link expired" error
**Actual:** Link still works
```

The bug goes back to Backend Engineer to fix, then returns to QA.

---

### Phase 6: Security

**Agent:** Security Engineer

**What happens:**
- Reviews for vulnerabilities
- Checks auth flows
- Ensures rate limiting, token security

**Your action:** Review the security assessment and approve.

**Example output:**
```markdown
### Security Review: Password Reset

**Status:** Approved

**Checked:**
- [x] Reset tokens are random and unique
- [x] Tokens expire after 1 hour
- [x] Rate limited to 3 requests per hour per email
- [x] Old sessions invalidated on reset

**Notes:**
- Consider adding account lockout after 5 failed resets (future)
```

---

### Phase 7: Ship

**Agent:** Platform Engineer

**What happens:**
- Deploys to production
- Verifies it works
- Monitors for issues

**Your action:** Approve the ship.

---

## The Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│    YOU                                                       │
│     │                                                        │
│     │ "I want password reset"                                │
│     ▼                                                        │
│  ┌─────────────┐                                             │
│  │   SPEC      │◄─── Product Manager                         │
│  └──────┬──────┘                                             │
│         │                                                    │
│    [CHECKPOINT: You approve spec]                            │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                             │
│  │   DESIGN    │◄─── UX Designer                             │
│  └──────┬──────┘                                             │
│         │ auto-proceed                                       │
│         ▼                                                    │
│  ┌─────────────┐                                             │
│  │   BACKEND   │◄─── Backend Engineer                        │
│  └──────┬──────┘                                             │
│         │ auto-proceed                                       │
│         ▼                                                    │
│  ┌─────────────┐                                             │
│  │   FRONTEND  │◄─── Frontend Engineer                       │
│  └──────┬──────┘                                             │
│         │ auto-proceed                                       │
│         ▼                                                    │
│  ┌─────────────┐                                             │
│  │    TEST     │◄─── QA Engineer                             │
│  └──────┬──────┘                                             │
│         │ auto-proceed (if pass)                             │
│         ▼                                                    │
│  ┌─────────────┐                                             │
│  │   SECURITY  │◄─── Security Engineer                       │
│  └──────┬──────┘                                             │
│         │                                                    │
│    [CHECKPOINT: You approve security]                        │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                             │
│  │    SHIP     │◄─── Platform Engineer                       │
│  └──────┬──────┘                                             │
│         │                                                    │
│    [CHECKPOINT: You decide to ship]                          │
│         │                                                    │
│         ▼                                                    │
│      LIVE ✓                                                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Checkpoints vs Auto-Proceed

**Checkpoints** (you're involved):
- Spec approval — before major work starts
- Security review — before shipping
- Ship — you decide when it goes live

**Auto-proceed** (agents coordinate without you):
- Design → Backend
- Backend → Frontend
- Frontend → Test
- Test → Security (if tests pass)

This means you're involved at 3 moments, not 7.

---

## Multiple Work Packages

You can have several packages flowing at once:

```
Package A: [Spec] → [Build] → [Test] → [Ship]
Package B:         [Spec] → [Build] → [Test]
Package C:                  [Spec] → [Build]
```

Agents work on their current phase. You checkpoint when packages reach you.

**Warning:** Too many parallel packages = too many context switches. 2-3 active is usually right.

---

## Shortcuts

Not every feature needs every phase:

### Bug Fix
```
You → Backend or Frontend → QA → Ship
```
Skip spec and design. Go straight to fixing.

### Backend-Only Feature
```
You → Product Manager → Backend → QA → Security → Ship
```
No frontend, no design.

### Quick Experiment
```
You → Growth Engineer → Ship (behind feature flag)
```
Minimal process for fast learning.

---

## Handling Problems

### Bug Found in Test

```
Test → Bug Report → Backend or Frontend fixes → Test again
```

Loop until tests pass.

### Security Issue Found

```
Security → Issue Report → Engineers fix → Security re-reviews
```

Loop until approved.

### Scope Creep

```
Agent: "This requires X which wasn't in scope"
You: "Add to scope" or "Defer to next package"
```

You decide scope changes.

---

## Summary

| Phase | Agent | Checkpoint? |
|-------|-------|-------------|
| Spec | Product Manager | **Yes** |
| Design | UX/UI Designer | No |
| Backend | Backend Engineer | No |
| Frontend | Frontend Engineer | No |
| Test | QA Engineer | Only if bugs |
| Security | Security Engineer | **Yes** |
| Ship | Platform Engineer | **Yes** |

**Your involvement:** 3 checkpoints.
**Agents handle:** Everything between.

---

→ [Chapter 5: Getting Started](05_GETTING_STARTED.md)

