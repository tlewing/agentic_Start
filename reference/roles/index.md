# Agent Roles Reference

Detailed role definitions for all 14 agents.

---

## How to Use These Files

Each role file defines:
- What the agent does and doesn't do
- How they work
- When to escalate to you
- How to work with the technical founder

To activate an agent:
```
You are ~/projects/agentic/reference/roles/[role-name].md

[Your task here]
```

---

## Plugins

Claude Code plugins extend what agents can do. They're **available when relevant**, not required.

### Global (All Roles)

| Plugin | Purpose |
|--------|---------|
| `typescript-lsp`, `pyright-lsp`, `gopls-lsp` | Language servers — auto-activate based on file types |
| `context7` | Look up current library documentation |
| `commit-commands` | `/commit`, `/commit-push-pr` available via wrap |

### Role-Specific Defaults

| Role | Default Plugin | Purpose |
|------|----------------|---------|
| Backend Engineer | `supabase` | Database operations, RLS, migrations |
| UI Designer | `frontend-design` | Production-grade UI generation |
| Platform Engineer | `vercel` | Deployment, environment management |
| Security Engineer | `code-review` | PR security review |
| Product Manager | `feature-dev` | Structured feature development |
| UX/UI Designer | `figma` | Design imports |
| Growth Engineer | `stripe` | Payment experiments |

See individual role files for full plugin lists.

---

## Core Engineering (Use Most Often)

| Role | File | Purpose |
|------|------|---------|
| Frontend Engineer | [frontend-engineer.md](frontend-engineer.md) | Builds UI — screens, components, interactions |
| Backend Engineer | [backend-engineer.md](backend-engineer.md) | Builds server — APIs, database, business logic |
| Platform Engineer | [platform-engineer.md](platform-engineer.md) | Handles deployment — CI/CD, infrastructure |
| QA Engineer | [qa-engineer.md](qa-engineer.md) | Tests everything — finds bugs, verifies quality |
| Security Engineer | [security-engineer.md](security-engineer.md) | Protects the app — audits, reviews auth |

---

## Product & Design

| Role | File | Purpose |
|------|------|---------|
| Product Manager | [product-manager.md](product-manager.md) | Defines what to build — specs, priorities |
| UX Designer | [ux-designer.md](ux-designer.md) | Designs how it works — flows, wireframes |
| UI Designer | [ui-designer.md](ui-designer.md) | Designs how it looks — visual, components |

---

## Data & Growth

| Role | File | Purpose |
|------|------|---------|
| Data Analyst | [data-analyst.md](data-analyst.md) | Analyzes data — metrics, insights |
| Growth Engineer | [growth-engineer.md](growth-engineer.md) | Builds for growth — experiments, optimization |

---

## Content & Support

| Role | File | Purpose |
|------|------|---------|
| Technical Writer | [technical-writer.md](technical-writer.md) | Writes documentation — guides, API docs |
| Customer Success | [customer-success.md](customer-success.md) | Synthesizes feedback — user research |

---

## Operations

| Role | File | Purpose |
|------|------|---------|
| Project Manager | [project-manager.md](project-manager.md) | Tracks work — status, blockers |
| Operations Manager | [operations-manager.md](operations-manager.md) | Optimizes process — workflows, efficiency |

