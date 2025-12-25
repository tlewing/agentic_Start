# Your Team

One Chief of Staff who becomes 14 specialists.

---

## Chief of Staff

When you type `claude`, you're talking to the Chief of Staff.

```
$ claude

Chief of Staff: Welcome to Agentic. What are you building?

You: A mobile app for dog walkers.

Chief of Staff: Great. Let me set up your project...
```

The Chief of Staff:
- Greets you and sets up projects
- Becomes specialists as needed
- Handles handoffs between them
- Maintains context across the conversation

You talk to one agent. They bring in whoever's needed.

---

## The Specialists

### Core Engineering

| Agent | What They Do |
|-------|-------------|
| **Frontend Engineer** | Screens, components, interactions |
| **Backend Engineer** | APIs, databases, business logic |
| **Platform Engineer** | Deployment, CI/CD, infrastructure |
| **QA Engineer** | Testing, bugs, quality |
| **Security Engineer** | Audits, auth review, vulnerabilities |

### Product & Design

| Agent | What They Do |
|-------|-------------|
| **Product Manager** | Specs, user stories, priorities |
| **UX Designer** | User flows, wireframes |
| **UI Designer** | Visual design, component styles |

### Data & Growth

| Agent | What They Do |
|-------|-------------|
| **Data Analyst** | Metrics, insights, dashboards |
| **Growth Engineer** | Experiments, optimization |

### Content & Support

| Agent | What They Do |
|-------|-------------|
| **Technical Writer** | Documentation, guides |
| **Customer Success** | User feedback synthesis |

### Operations

| Agent | What They Do |
|-------|-------------|
| **Project Manager** | Status tracking, coordination |
| **Operations Manager** | Process optimization |

---

## How It Works

You don't summon agents directly. You tell Chief of Staff what you need:

```
You: Build the user profile API.

Chief of Staff: Bringing in Backend Engineer.

Backend Engineer: I'll design the schema and endpoints...
[works]
Backend Engineer: Done. Ready for frontend.

Chief of Staff: Should I bring in Frontend Engineer?
```

---

## Deep Dives

Each agent has a detailed role file in `reference/roles/`:

- What they do and don't do
- How they work
- What files they own
- When to escalate to you

Reference them when you want to understand an agent better.
