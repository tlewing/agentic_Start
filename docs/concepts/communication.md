# Communication

Agents communicate through shared documentation. No hidden state, no private channels.

## The _AGENTS.md File

Every project has `docs/_AGENTS.md`. This is the single point of truth for agent coordination.

### Structure

```markdown
# Agents

## Active Agents
[Which roles are currently engaged]

## Agent 1: [Role Name]
### Current Status
| Field | Value |
|-------|-------|
| Status | Active / Paused / Complete |
| Current Task | What they're working on |
| Last Updated | Timestamp |

### Task Queue
1. [ ] First priority
2. [ ] Second priority

### Recently Completed
- [x] What was done (date)

## Cross-Agent Notes
[Messages between agents, handoff context]
```

### How Agents Use It

**On activation:**
1. Read the entire file
2. Find your section
3. Check cross-agent notes for context
4. Review your task queue

**While working:**
1. Update status as you progress
2. Add notes for other agents
3. Mark tasks complete
4. Add new discovered tasks

**On completion:**
1. Mark task complete
2. Write handoff notes if needed
3. Update status

## Handoff Notes

When one agent's work affects another, leave a note:

```markdown
### From Frontend Engineer (Dec 24)
Implemented the new dashboard layout.

**For QA Engineer:**
- Test the three role-based views (student, instructor, parent)
- Check mobile responsiveness on the stats cards

**For Backend Engineer:**
- The dashboard now expects `attendance_streak` in the profile response
- See `hooks/useDashboard.ts` line 45
```

## Escalation

When you need the human's decision:

```markdown
### Escalation: [Agent Name]
**Question:** Should we use WebSocket or polling for real-time updates?

**Options:**
1. WebSocket — Lower latency, more complex
2. Polling — Simpler, higher server load

**My Recommendation:** WebSocket for production scale

**Blocking:** Yes / No
```

## Patterns

### Good Communication
- Specific file paths and line numbers
- Clear next steps
- Context for why, not just what
- Explicit blocking vs informational

### Anti-Patterns
- Vague handoffs ("check the code")
- Missing context ("I fixed the bug")
- No file references
- Assuming others know what you know

## Beyond _AGENTS.md

Other shared docs agents may reference:

| File | Purpose |
|------|---------|
| `_ARCHITECTURE.md` | Technical decisions, patterns |
| `_SCHEMA.md` | Database design |
| `_ROADMAP.md` | Product priorities |
| `_SECURITY_AUDIT.md` | Security findings |

Agents read these for context. The human maintains them.
