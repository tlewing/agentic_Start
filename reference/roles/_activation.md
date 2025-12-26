# Activation Protocol

Common instructions for all specialist roles.

---

## When Activated

1. **Read** `docs/_AGENTS.md` — find your task queue and cross-agent notes
2. **Check** cross-agent notes for context from other agents
3. **Review** relevant project docs (`_SCHEMA.md`, `_ARCHITECTURE.md`, etc.)
4. **Begin** work on your current task
5. **Update** your status and notes as you progress

---

## Working with the Founder

The founder is technical (CEO/CTO level). They understand code, architecture, and tradeoffs.

**Leverage their expertise:**
- They may have opinions on approach — ask early for complex decisions
- They can review tricky implementations when you're unsure
- They may want to build certain things themselves

**Optimize for their time:**
- Queue non-blocking decisions, don't wait
- Include your recommendation in every decision
- Auto-proceed when within approved scope
- Flag concerns early, not at checkpoint

---

## Escalation Triggers

Escalate to the founder when:
- Changes affect multiple systems or agents
- Breaking changes to existing interfaces
- Third-party integration or vendor decisions
- Security concerns
- Scope unclear or requirements conflict
- Blocked on another agent's work

---

## Key Project Files

In any project using this framework:
- `docs/_AGENTS.md` — Your task queue and cross-agent notes
- `docs/_ARCHITECTURE.md` — Technical decisions
- `docs/_SCHEMA.md` — Database schema (if applicable)
- `CLAUDE.md` — Project-specific context

---

## Handoff Format

When leaving notes for other agents:

```
[Role] complete: [Brief description]
- Key decision: [Why you chose X over Y]
- Location: [Where to find the work]
- Next: [What the receiving agent should do]
```

Example:
```
Backend complete: Profiles API
- Key decision: Soft deletes for account restoration
- Location: lib/profiles.ts, migration 057
- Next: Frontend can build profile screen
```
