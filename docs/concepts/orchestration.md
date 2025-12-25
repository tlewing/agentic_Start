# Orchestration

The human (you) is the conductor. Agents are the orchestra.

## Your Roles

As CEO/CTO/Head of Product, you wear multiple hats:

| Role | Responsibility |
|------|----------------|
| **CEO** | Vision, strategy, final decisions |
| **CTO** | Technical direction, architecture |
| **Head of Product** | Priorities, roadmap, trade-offs |
| **Developer** | Write code alongside agents |

## How Orchestration Works

### 1. Assignment
You assign tasks to agents. Be specific:
- What needs to be done
- Why it matters
- Any constraints
- Expected output

### 2. Activation
Start an agent with:
```
You are [path/to/role.md]

Current task: [specific task]
```

The agent reads its role file, then `docs/_AGENTS.md`, then begins work.

### 3. Monitoring
Check in on agents:
- Review their cross-agent notes
- Answer clarifying questions
- Unblock dependencies
- Approve significant changes

### 4. Handoffs
Agents hand off to each other through you:
1. Agent A completes work, updates notes
2. You review Agent A's output
3. You activate Agent B with context
4. Agent B reads notes, continues work

### 5. Decisions
Agents escalate to you when:
- Architecture decisions needed
- Scope is unclear
- Trade-offs require prioritization
- External dependencies involved
- Risk is significant

## Autonomy Levels

Different roles have different autonomy:

| Level | Meaning | Example |
|-------|---------|---------|
| **High** | Act, then report | Frontend: implement UI component |
| **Medium** | Propose, then act | Backend: suggest API design first |
| **Low** | Ask, then act | Security: get approval before changes |

## Parallel vs Sequential

**Run in parallel when:**
- Tasks are independent
- Different scopes (frontend + backend)
- Time-sensitive work

**Run sequentially when:**
- Tasks depend on each other
- Handoff required
- Shared state changes

## The Single Point of Truth

`docs/_AGENTS.md` is where coordination happens:
- Each agent has a task queue
- Cross-agent notes capture handoffs
- You update status and priorities
- Agents check it when activated

You maintain this file. Agents read and update their sections.
