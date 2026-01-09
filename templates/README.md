# Templates

Copy these to your project to get started.

---

## Quick Start

```bash
# From your project directory
cp ~/.jebidiah/templates/CLAUDE.md ./
cp -r ~/.jebidiah/templates/docs ./
```

You'll have:

```
your-project/
├── CLAUDE.md               # Connects project to Jebidiah framework
└── docs/
    ├── _TODAY.md           # Daily operations (read every morning)
    ├── _AGENTS.md          # Agent coordination
    ├── _VISION.md          # What you're building
    ├── _ROADMAP.md         # Priorities and phases
    ├── _ARCHITECTURE.md    # Technical decisions
    └── _CONVENTIONS.md     # Coding standards
```

---

## What Each File Does

| File | Purpose | Who Updates |
|------|---------|-------------|
| `CLAUDE.md` | Connects project to Jebidiah framework | You (when focus shifts) |
| `_TODAY.md` | Your daily briefing — decisions, checkpoints, status | Agents update, you read |
| `_AGENTS.md` | Agent status and coordination | Agents update |
| `_VISION.md` | What you're building and why | You write, agents read |
| `_ROADMAP.md` | Current phase and priorities | PM helps, you approve |
| `_ARCHITECTURE.md` | Tech stack and decisions | Engineers help, you approve |
| `_CONVENTIONS.md` | How code should be written | You and engineers |

---

## After Copying

1. **Fill in `CLAUDE.md`** — Project name, one-liner, current focus
2. **Fill in `_VISION.md`** — Describe what you're building
3. **Activate Product Manager** — Get help with roadmap
4. **Start building** — Create your first work package

See [Chapter 5: Getting Started](../05_GETTING_STARTED.md) for the full walkthrough.

