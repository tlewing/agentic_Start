# Architecture

> **Instructions:** This file is typically created by the Backend Engineer agent after the vision and roadmap are clear. It captures technical decisions and patterns.

---

## Overview

*High-level description of the system architecture.*

[Describe the overall structure — what are the major components and how do they interact?]

---

## Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Frontend** | [e.g., React, Next.js] | [Why this choice] |
| **Backend** | [e.g., Node.js, Supabase] | [Why this choice] |
| **Database** | [e.g., PostgreSQL] | [Why this choice] |
| **Auth** | [e.g., Supabase Auth] | [Why this choice] |
| **Hosting** | [e.g., Vercel, AWS] | [Why this choice] |
| **Other** | [Any other key tech] | [Why this choice] |

---

## Key Decisions

### Decision 1: [Title]

**Context:** [What situation prompted this decision?]

**Options Considered:**
1. [Option A] — [Pros/cons]
2. [Option B] — [Pros/cons]
3. [Option C] — [Pros/cons]

**Decision:** [What we chose]

**Rationale:** [Why we chose it]

**Consequences:** [What this means for the project]

**Date:** [When decided] | **Decided By:** [Who]

---

### Decision 2: [Title]

**Context:** [What situation prompted this decision?]

**Decision:** [What we chose]

**Rationale:** [Why we chose it]

**Date:** [When decided] | **Decided By:** [Who]

---

## Patterns

### Patterns We Follow

| Pattern | Description | Example |
|---------|-------------|---------|
| [Pattern 1] | [What it is] | [Where to see it] |
| [Pattern 2] | [What it is] | [Where to see it] |

### Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | What To Do Instead |
|--------------|--------------|---------------------|
| [Anti-pattern 1] | [The problem] | [The alternative] |
| [Anti-pattern 2] | [The problem] | [The alternative] |

---

## Data Model

*High-level overview of the data model. See `_SCHEMA.md` for details.*

```
[Entity 1] ──── has many ──── [Entity 2]
     │
     └── belongs to ── [Entity 3]
```

Key entities:
- **[Entity 1]** — [What it represents]
- **[Entity 2]** — [What it represents]

---

## Security Model

| Area | Approach |
|------|----------|
| **Authentication** | [How users authenticate] |
| **Authorization** | [How permissions work] |
| **Data Access** | [How data access is controlled] |
| **Secrets** | [How secrets are managed] |

---

## External Integrations

| Integration | Purpose | Status |
|-------------|---------|--------|
| [Service 1] | [What it does for us] | Active / Planned |
| [Service 2] | [What it does for us] | Active / Planned |

---

## Infrastructure

| Component | Details |
|-----------|---------|
| **Environments** | [Dev, Staging, Production] |
| **CI/CD** | [How code gets deployed] |
| **Monitoring** | [How we know things are working] |
| **Backups** | [How data is protected] |

---

## Open Technical Questions

| Question | Impact | Status |
|----------|--------|--------|
| [Technical question] | [What it affects] | Open / Resolved |

---

## Diagrams

*Add architecture diagrams as needed.*

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│     API     │────▶│  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

> **Maintenance:** Backend Engineer owns this document. Update when making architectural decisions.
