# Chapter 3: The Agents

Your team of 14 specialists.

---

## How Agents Work

Each agent is an AI (like Claude) given:

1. **A role file** — Defines who they are, what they do, how they work
2. **Your project's context** — Current status, priorities, conventions
3. **A task** — What you need them to do right now

To activate an agent, you tell Claude:

```
You are ~/projects/agentic/reference/roles/backend-engineer.md

[Your task or context here]
```

The agent reads its role file, reads your project's `_AGENTS.md`, and starts working.

---

## The Full Team

You have access to 14 specialized agents:

### Core Engineering (Use Most Often)

| Agent | What They Do |
|-------|-------------|
| **Frontend Engineer** | Builds user interfaces — screens, components, interactions |
| **Backend Engineer** | Builds server logic — APIs, databases, business rules |
| **Platform Engineer** | Handles deployment — CI/CD, environments, infrastructure |
| **QA Engineer** | Tests everything — finds bugs, verifies fixes, ensures quality |
| **Security Engineer** | Protects the app — audits code, reviews auth, checks vulnerabilities |

### Product & Design (Use for Features)

| Agent | What They Do |
|-------|-------------|
| **Product Manager** | Defines what to build — specs, user stories, priorities |
| **UX Designer** | Designs how it works — user flows, wireframes, interactions |
| **UI Designer** | Designs how it looks — visual design, component styles |

### Data & Growth (Use for Optimization)

| Agent | What They Do |
|-------|-------------|
| **Data Analyst** | Analyzes data — metrics, insights, dashboards |
| **Growth Engineer** | Builds for growth — experiments, analytics, optimization |

### Content & Support (Use as Needed)

| Agent | What They Do |
|-------|-------------|
| **Technical Writer** | Writes documentation — guides, API docs, help content |
| **Customer Success** | Synthesizes feedback — user research, support patterns |

### Operations (Use for Organization)

| Agent | What They Do |
|-------|-------------|
| **Project Manager** | Tracks work — status, blockers, coordination |
| **Operations Manager** | Optimizes process — workflows, efficiency, automation |

---

## Which Agents You'll Use Most

For most projects, your core team is:

```
┌─────────────────────────────────────────────────────────┐
│                     YOUR DAILY TEAM                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   Product Manager     → Specs and priorities             │
│   Backend Engineer    → Server and database              │
│   Frontend Engineer   → User interface                   │
│   QA Engineer         → Testing                          │
│   Security Engineer   → Security review                  │
│   Platform Engineer   → Deployment                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

The others are on-demand — activate when you need that expertise.

---

## Agent Profiles

### Frontend Engineer

**What they're good at:**
- Building screens and components
- Making things look right and feel smooth
- Handling user interactions
- Accessibility and responsive design

**What they won't touch:**
- Database changes
- Server-side logic
- Security configurations

**When to activate:**
- "Build the login screen"
- "Fix this component layout"
- "Add loading states to the dashboard"

---

### Backend Engineer

**What they're good at:**
- Database schema design
- API endpoints
- Business logic
- Data validation

**What they won't touch:**
- UI components
- Visual styling
- User interactions

**When to activate:**
- "Design the database for user profiles"
- "Build the API for creating orders"
- "Add caching to the search endpoint"

---

### Product Manager

**What they're good at:**
- Breaking features into user stories
- Defining acceptance criteria
- Prioritizing work
- Clarifying requirements

**What they won't touch:**
- How things are implemented
- Technical decisions
- Code

**When to activate:**
- "Help me spec out the notifications feature"
- "What should MVP scope be for this?"
- "Prioritize the backlog for next month"

---

### QA Engineer

**What they're good at:**
- Writing tests
- Finding bugs
- Verifying fixes
- Ensuring quality

**What they won't touch:**
- Implementing features
- Making design decisions
- Changing architecture

**When to activate:**
- "Write tests for the auth flow"
- "Test this feature before we ship"
- "Review test coverage for critical paths"

---

### Security Engineer

**What they're good at:**
- Auditing for vulnerabilities
- Reviewing authentication
- Checking authorization rules
- Security best practices

**What they won't touch:**
- Feature implementation
- UI/UX decisions
- Performance optimization

**When to activate:**
- "Review the auth flow before launch"
- "Audit this feature for security issues"
- "Check our database policies"

---

### Platform Engineer

**What they're good at:**
- CI/CD pipelines
- Deployment automation
- Environment configuration
- Infrastructure management

**What they won't touch:**
- Feature code
- Business logic
- UI components

**When to activate:**
- "Set up automatic deploys"
- "Configure the staging environment"
- "This feature is ready — deploy it"

---

## Activating Agents

To work with an agent, start a Claude session and say:

```
You are ~/projects/agentic/reference/roles/[role-name].md

Read my project at [your-project-path] and [what you need].
```

Examples:

**Starting a new feature:**
```
You are ~/projects/agentic/reference/roles/product-manager.md

Help me spec out a password reset feature for my app.
```

**Building an API:**
```
You are ~/projects/agentic/reference/roles/backend-engineer.md

Read docs/_AGENTS.md and implement the user profile API.
```

**Testing before ship:**
```
You are ~/projects/agentic/reference/roles/qa-engineer.md

Test the notifications feature and report any issues.
```

---

## How Agents Hand Off to Each Other

Agents coordinate by leaving notes in `_AGENTS.md`:

```markdown
### Handoff: Backend Engineer → Frontend Engineer

**Work Package:** User Auth
**Phase:** Backend → Frontend

**For Frontend Engineer:**
- API endpoints ready: /api/auth/login, /api/auth/logout
- Types in lib/types.ts
- See tests in __tests__/api/auth.test.ts for expected behavior

**For Founder (FYI):**
- Used session-based auth as specified
- Added rate limiting
- No concerns
```

When you activate the Frontend Engineer, they read this note and know exactly what's ready for them.

---

## Deep Dives

Each agent has a detailed role file in `reference/roles/`. These files contain:

- Exactly what they do and don't do
- How they should work
- What files they own
- When to escalate to you
- How to work with you as a technical founder

You don't need to read them all now. Reference them when you want to understand an agent better or customize their behavior.

---

## Summary

| Agent Type | Who | When |
|------------|-----|------|
| **Core Engineering** | Frontend, Backend, Platform, QA, Security | Every project, most days |
| **Product & Design** | PM, UX, UI | When defining or designing features |
| **Data & Growth** | Data Analyst, Growth Engineer | When optimizing |
| **Content & Support** | Tech Writer, Customer Success | When documenting or researching |
| **Operations** | Project Manager, Ops Manager | When organizing |

**Most common flow:**
```
Product Manager → UX Designer → Backend Engineer → Frontend Engineer → QA → Security → Platform
```

---

→ [Chapter 4: The Workflow](04_THE_WORKFLOW.md)

