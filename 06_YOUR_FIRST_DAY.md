# Chapter 6: Your First Day

What a real day looks like, step by step.

---

## The Scenario

Let's say you set up your project yesterday. You have:

- A vision for a dog walking app
- A roadmap from the Product Manager
- Your first work package: "User Registration"

Today is day one of actually building.

---

## Morning (9:00 AM)

### Open _TODAY.md

This is your morning briefing. On day one, it looks like:

```markdown
# Today

*Last updated: [Date] — 8:45 AM by Product Manager*

## Quick Status

| Metric | Count |
|--------|-------|
| Blocking decisions | 1 |
| Checkpoints pending | 0 |
| Ready to ship | 0 |

## Needs Your Attention

### Blocking Decision

**Tech Stack: React Native or Flutter?**
- Package: All
- Agent: Backend Engineer (surfaced during architecture)
- Rec: React Native (larger ecosystem, you know JavaScript)
- Blocking: Can't start building until decided

## Package Status

| Package | Phase | State |
|---------|-------|-------|
| User Registration | Spec | ✅ Approved |
| — | Architecture | Waiting on tech stack decision |
```

### Make the Decision

The Backend Engineer asked about tech stack. They gave a recommendation. You decide:

"React Native. Update `_ARCHITECTURE.md` and proceed."

Now the Architecture phase can complete.

---

## Mid-Morning (10:00 AM)

### Activate the Backend Engineer

```
You are ~/projects/agentic/reference/roles/backend-engineer.md

Tech stack is decided: React Native frontend, Supabase backend.
Read docs/_AGENTS.md and start the User Registration backend:
- Design the database schema
- Create the auth API
- Write tests
```

### Let Them Work

The Backend Engineer:
- Designs the users table
- Sets up Supabase auth
- Creates registration endpoint
- Writes tests
- Updates `_AGENTS.md` with handoff notes for Frontend

**Time spent by you:** 5 minutes to activate
**Work done by agent:** 2-3 hours equivalent

---

## You Go Do Other Things

While the Backend Engineer works, you:
- Have coffee
- Think about marketing
- Talk to a potential user
- Whatever founders do

You don't need to watch. The agent is working.

---

## Early Afternoon (1:00 PM)

### Check Status

Look at `_TODAY.md` or `_AGENTS.md`:

```markdown
## Quick Status

| Metric | Count |
|--------|-------|
| Blocking decisions | 0 |
| Checkpoints pending | 0 |
| Ready to ship | 0 |

## Since This Morning

**Completed:**
- ✅ User Registration backend (Backend Engineer)

## Package Status

| Package | Phase | State |
|---------|-------|-------|
| User Registration | Backend → Frontend | Ready for Frontend |
```

### Activate the Frontend Engineer

```
You are ~/projects/agentic/reference/roles/frontend-engineer.md

Read docs/_AGENTS.md. The backend for User Registration is ready.
Build the registration screens.
```

### Let Them Work

The Frontend Engineer:
- Reads the handoff notes
- Builds the registration form
- Connects to the API
- Handles errors and loading states
- Updates `_AGENTS.md`

---

## Late Afternoon (4:00 PM)

### Check Status Again

```markdown
## Since This Afternoon

**Completed:**
- ✅ User Registration frontend (Frontend Engineer)

## Package Status

| Package | Phase | State |
|---------|-------|-------|
| User Registration | Frontend → Test | Ready for QA |
```

### Activate QA Engineer

```
You are ~/projects/agentic/reference/roles/qa-engineer.md

Read docs/_AGENTS.md. Test the User Registration feature.
```

The QA Engineer:
- Tests the happy path
- Tests error cases
- Verifies the acceptance criteria
- Reports any bugs

---

## End of Day (6:00 PM)

### Final Status

```markdown
# Today

## Summary

**Packages progressed:** 1
**Phases completed:** 3 (Backend, Frontend, Test)
**Blocking decisions:** 0
**Bugs found:** 1 (minor — password validation edge case)

## Package Status

| Package | Phase | State |
|---------|-------|-------|
| User Registration | Test | Bug found — back to Frontend |

## Bug Report

**Password validation accepts spaces**
- Severity: Low
- Fix: Add trim to password input
- Assigned: Frontend Engineer
```

### The Bug Goes Back

The Frontend Engineer will fix the bug. Then QA will retest. Then Security will review. Then Ship.

That's tomorrow.

---

## What You Did Today

| Time | Activity | Duration |
|------|----------|----------|
| 9:00 | Read `_TODAY.md`, made tech stack decision | 10 min |
| 10:00 | Activated Backend Engineer | 5 min |
| 10:05-1:00 | Did other founder work | — |
| 1:00 | Checked status, activated Frontend Engineer | 10 min |
| 1:10-4:00 | Did other founder work | — |
| 4:00 | Checked status, activated QA Engineer | 10 min |
| 6:00 | Read end-of-day status | 5 min |

**Total time managing agents: ~40 minutes**

**Work accomplished:** Full feature built and tested (just one bug to fix)

---

## The Pattern

```
Morning:
├── Read _TODAY.md
├── Clear any blocking decisions
└── Activate agents for new phases

Throughout the day:
├── Do your founder work
├── Check in when phases complete
└── Activate next agents

Evening:
├── Read final status
├── Know what's ready for tomorrow
└── Done
```

---

## A More Realistic First Day

Day one is usually more exploratory:

**Morning:**
- Activate Product Manager
- Refine the spec through conversation
- Approve the spec

**Afternoon:**
- Activate Backend Engineer
- Work through architecture decisions together
- Get the schema designed

**Evening:**
- Review what was built
- Plan tomorrow

You might not ship on day one. That's fine. You're learning the rhythm.

---

## Tips for Day One

### Don't Rush

First day is for learning the workflow. Speed comes later.

### Ask Questions

When agents suggest things, ask why. Understand their reasoning.

### Make Notes

Write down what works and what's confusing. You'll refine your process.

### Celebrate Small Wins

Your first handoff between agents is a milestone. Your first bug found by QA is working as intended. Your first ship is magic.

---

## What Day Two Looks Like

You wake up. Open `_TODAY.md`:

```markdown
## Your Morning

1. **Bug fix ready for review**
   - Password validation fixed
   - QA re-tested: Pass

2. **Security review pending**
   - Package: User Registration
   - Agent: Security Engineer
   - Status: Ready for your activation
```

Activate Security Engineer. They review. Approve. Activate Platform Engineer. Ship.

**Day two: First feature shipped.**

---

## Summary

| Moment | What You Do |
|--------|-------------|
| Morning | Read `_TODAY.md`, clear decisions |
| Throughout | Check status, activate agents |
| Evening | Review progress, plan tomorrow |

**Core rhythm:** Read → Decide → Activate → Let them work → Repeat

---

→ [Chapter 7: Operating](07_OPERATING.md)

