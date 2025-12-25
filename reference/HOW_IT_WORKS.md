# How It Works

The mechanics behind your AI team. Read this after you've used Agentic and want to understand what's happening.

---

## Agents

Agents are AI given a specific role and context. When you ask for something:

1. The right agent reads its role
2. Reads project status
3. Does the work
4. Updates status for you and other agents

Agents don't have memory between sessions. They get context by reading files. Everything important is written down.

---

## The Flow

You say what you want. Agents make it happen.

```
You: Build password reset.

[Product Manager specs it]
[Designer flows it]
[Engineers build it]
[QA tests it]
[Security reviews it]

Chief of Staff: Password reset ready. Ship it?

You: Ship it.

Chief of Staff: Live.
```

Behind the scenes, agents hand off to each other. You don't manage that.

---

## Your Three Decision Points

You're not involved in every step. Just three:

1. **Approve the spec** — Before work starts
2. **Approve security** — Before shipping
3. **Approve ship** — When it goes live

Everything else flows automatically.

---

## What You Decide vs What Agents Decide

**You decide:**
- What to build and why
- What's in scope
- When to ship
- Acceptable risk

**Agents decide:**
- How to code it
- Which libraries to use
- How to structure it
- How to test it

The rule: You decide *what*. Agents figure out *how*.

---

## Coordination

Agents coordinate through shared files:

| File | Purpose |
|------|---------|
| `_TODAY.md` | What needs your attention |
| `_AGENTS.md` | Agent status and handoffs |
| `_VISION.md` | What you're building |
| `_ROADMAP.md` | Priorities |

When Backend finishes an API, they write a note. When Frontend starts, they read it.

---

## The Phases

```
IDEA → SPEC → DESIGN → BUILD → TEST → SECURITY → PERFORMANCE → SHIP
```

| Phase | Agent | You Involved? |
|-------|-------|---------------|
| Spec | Product Manager | **Yes** |
| Design | UX/UI Designer | No |
| Build | Engineers | No |
| Test | QA Engineer | Only if bugs |
| Security | Security Engineer | **Yes** |
| Performance | Platform Engineer | Only if issues |
| Ship | Platform Engineer | **Yes** |

---

## The Leverage

You *can* do everything yourself. But you shouldn't.

With agents:
- You set direction (minutes)
- Agents execute (hours of equivalent work)
- You review (minutes)
- Repeat

Your judgment applied to more work. That's leverage.
