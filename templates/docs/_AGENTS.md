# Agents

This file coordinates all agent activity on this project. Agents read this file when activated to understand current state, their tasks, and context from other agents.

---

## Quick Status

| Area | Status |
|------|--------|
| **Active Work Packages** | 0 |
| **Blocking Decisions** | 0 |
| **Checkpoints Pending** | 0 |

---

## Work Packages

### Active

| Package | Phase | Agent | State | Blocking? |
|---------|-------|-------|-------|-----------|
| *None* | — | — | — | — |

### Queued

| Package | Next Phase | Waiting For |
|---------|------------|-------------|
| *None* | — | — |

### Completed (Last 14 Days)

| Package | Shipped | Notes |
|---------|---------|-------|
| *None* | — | — |

---

## Decision Queue

### Blocking (work stopped until decided)

| Package | Question | Options | Agent Rec | Added |
|---------|----------|---------|-----------|-------|
| *None* | — | — | — | — |

### Non-Blocking (decide by EOD)

| Package | Question | Options | Agent Rec | Added |
|---------|----------|---------|-----------|-------|
| *None* | — | — | — | — |

### Recently Decided

| Package | Decision | Rationale | Decided | By |
|---------|----------|-----------|---------|-----|
| *None* | — | — | — | — |

---

## Active Agents

| Role | Status | Current Focus |
|------|--------|---------------|
| Frontend Engineer | — | — |
| Backend Engineer | — | — |
| QA Engineer | — | — |

*Update this table when activating/deactivating agents*

---

## Frontend Engineer

### Current Status

| Field | Value |
|-------|-------|
| **Status** | Inactive |
| **Work Package** | — |
| **Phase** | — |
| **Last Updated** | — |

### Task Queue
1. [ ] *No tasks assigned*

### Recently Completed
*None yet*

---

## Backend Engineer

### Current Status

| Field | Value |
|-------|-------|
| **Status** | Inactive |
| **Work Package** | — |
| **Phase** | — |
| **Last Updated** | — |

### Task Queue
1. [ ] *No tasks assigned*

### Recently Completed
*None yet*

---

## QA Engineer

### Current Status

| Field | Value |
|-------|-------|
| **Status** | Inactive |
| **Work Package** | — |
| **Phase** | — |
| **Last Updated** | — |

### Task Queue
1. [ ] *No tasks assigned*

### Recently Completed
*None yet*

---

## Platform Engineer

### Current Status

| Field | Value |
|-------|-------|
| **Status** | Inactive |
| **Work Package** | — |
| **Phase** | — |
| **Last Updated** | — |

### Task Queue
1. [ ] *No tasks assigned*

### Recently Completed
*None yet*

---

## Security Engineer

### Current Status

| Field | Value |
|-------|-------|
| **Status** | Inactive |
| **Work Package** | — |
| **Phase** | — |
| **Last Updated** | — |

### Task Queue
1. [ ] *No tasks assigned*

### Recently Completed
*None yet*

---

## On-Demand Agents

*Add sections for these agents when activated:*
- Product Manager
- UX Designer
- UI Designer
- Data Analyst
- Growth Engineer
- Technical Writer
- Customer Success
- Project Manager
- Operations Manager

---

## Cross-Agent Notes

*Use this section to leave notes for other agents. Include your role and date.*

### Handoff Template

```markdown
### Handoff: [From Role] → [To Role]

**Work Package:** [Name]
**Phase Transition:** [From Phase] → [To Phase]
**State:** Complete | Auto-Proceed

---

**For [Next Agent]:**
- Specific instruction 1
- Specific instruction 2
- Files: `path/to/file.ts:line`

**For Founder (FYI):**
- One-line summary
- Any concerns (or "No concerns")

**Artifacts:**
- [x] Completed items
- [ ] Pending items for next agent
```

---

## Escalations

*For urgent issues only. Use Decision Queue for normal decisions.*

```markdown
### Escalation: [Role] (Date)

**Urgency:** High / Medium / Low

**Question:** What do you need decided?

**Context:** Why this is urgent

**Options:**
1. Option A — trade-offs
2. Option B — trade-offs

**Recommendation:** Your suggestion

**Blocking:** Yes / No
**Impact if not decided today:** What happens
```

---

## Standing Decisions

*Pre-made decisions agents can reference. Founder updates this section.*

### Technology
- *None yet*

### UX
- *None yet*

### Security
- *None yet*

---

## Common Patterns

*Document project-specific patterns all agents should follow.*

### File Naming
- Components: `PascalCase.tsx`
- Utilities: `kebab-case.ts`
- Tests: `ComponentName.test.tsx`

### Commit Messages
- Format: `type(scope): description`
- Types: feat, fix, docs, test, refactor

---

## Resources

| Doc | Purpose |
|-----|---------|
| `docs/_VISION.md` | What we're building |
| `docs/_ROADMAP.md` | Product priorities |
| `docs/_ARCHITECTURE.md` | Technical decisions |
| `docs/_CONVENTIONS.md` | Coding standards |

