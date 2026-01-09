# Jebidiah

A coordination layer for humans running parallel Claude sessions.

---

## What This Is (and Isn't)

Claude Code has a `feature-dev` plugin. It's excellent — a 7-phase process where Claude drives discovery, exploration, architecture, implementation, and review. You approve checkpoints. Claude runs the show.

**This framework solves a different problem.**

You have multiple terminals open. Each is running Claude. One's building an API, another's on the frontend, a third is running tests. You're switching between them, making decisions, unblocking work.

The question isn't "how do I automate feature development?" It's:

- **What is this terminal doing right now?**
- **Where was it when I left?**
- **Why did it make that choice?**

This framework helps you stay oriented while *you* orchestrate the work.

| | feature-dev | jebidiah |
|---|---|---|
| **Who drives** | Claude | You |
| **Structure** | 7 sequential phases | Parallel terminals |
| **Coordination** | Built into the process | Shared files + handoffs |
| **Best for** | Complex features, thorough process | Multiple workstreams, human orchestration |

Use both. Run `feature-dev` in one terminal while doing something else in another. They complement each other.

---

## The Plugins You Already Have

This framework assumes you're using Claude Code with plugins:

| Plugin | Role |
|--------|------|
| `feature-dev` | Structured feature development (when you want Claude to drive) |
| `code-review` | PR review |
| `commit-commands` | `/commit`, `/commit-push-pr`, `/clean_gone` |
| `frontend-design` | Production-grade UI generation |
| `context7` | Up-to-date library docs |
| `github` | GitHub integration |
| `supabase` | Supabase tooling |
| `typescript-lsp` | TypeScript language server |
| `pyright-lsp` | Python language server |
| `gopls-lsp` | Go language server |

The plugins handle *capabilities*. This framework handles *coordination*.

---

## The Problem

You ask Claude to build something. It takes 30 minutes. You wait.

Or: you open three terminals, start three workstreams, and now you're filling lag time instead of wasting it.

But now you have a new problem: **orientation**. Which terminal is doing what? What's blocked? What decisions are waiting?

---

## The Solution

**Roles** give each terminal an identity. Glance at Terminal 2 — "that's Backend on the profiles API."

**`_AGENTS.md`** tracks who's doing what, what's done, what's blocked.

**Handoffs capture reasoning**, not just facts. "Used soft deletes because we need account restoration" — so the next terminal (or tomorrow's you) has context.

**Commands** like `wrap`, `status`, and `today` keep state clean and visible.

---

## How It Works

### Single terminal (role shifting)

```
You: Build the user profiles feature

Chief of Staff: Let me bring in Backend for the API.

[shifts to Backend Engineer, works]

Backend: API done. Tests passing.

[shifts back]

Chief of Staff: Frontend next?
```

### Multiple terminals (parallel work)

```
Terminal 1                    Terminal 2                    Terminal 3
─────────────────────────     ─────────────────────────     ─────────────────────────
"You're Backend.              "You're Frontend.             "You're QA.
Build the profiles API."      Build the profile screen."    Test the auth flow."

[works 30 min]                [works 20 min]                [works 15 min]
```

Each terminal is independent. Coordination happens through:
- `_AGENTS.md` — shared state
- Git — branches, commits
- You — checking in, deciding, unblocking

---

## Quick Start

```bash
git clone https://github.com/jasonhoffman/jebidiah ~/.jebidiah
cd ~/.jebidiah
claude
```

Say "hi" — the Chief of Staff reads context and tells you where things stand.

---

## Reference

| Doc | What |
|-----|------|
| [CLAUDE.md](CLAUDE.md) | Chief of Staff instructions |
| [AGENTS.md](AGENTS.md) | Role definitions |
| [TECH_STACK.md](TECH_STACK.md) | Default tech choices |
| [reference/](reference/) | Deep dives on roles, workflows, concepts |

---

## When to Use What

**Use `feature-dev`** when:
- You want Claude to drive a thorough process
- Single complex feature, full ceremony
- You'll approve checkpoints but not actively orchestrate

**Use this framework** when:
- You want to run multiple workstreams in parallel
- You're the orchestrator, Claude is the specialist
- You need to stay oriented across terminals and sessions

**Use both** when:
- `feature-dev` runs in Terminal 1
- You do other work in Terminals 2-4
- Coordination happens through `_AGENTS.md`

---

MIT License
