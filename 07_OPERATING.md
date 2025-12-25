# Chapter 7: Operating

The daily and weekly rhythm once you're up and running.

---

## The Daily Rhythm

After your first few days, you'll settle into a pattern:

### Morning (15 minutes)

```
1. Open _TODAY.md
   ├── Any blocking decisions?
   ├── Any checkpoints pending?
   └── What shipped overnight?

2. Clear the queue
   ├── Make decisions
   ├── Approve checkpoints
   └── Note anything to discuss later

3. Activate agents for the day
   └── Start phases that are ready
```

### Throughout the Day

```
You do founder work:
├── Talk to users
├── Think about strategy
├── Write code (if you want to)
├── Handle business stuff

Occasionally:
├── Check status
├── Activate new phases
└── Answer agent questions
```

### Evening (10 minutes)

```
1. Check _TODAY.md
   ├── What completed today?
   ├── What's blocked?
   └── What's ready for tomorrow?

2. Clear any final decisions

3. Done
```

**Total time managing agents: ~30-45 minutes**

---

## The Weekly Rhythm

### Monday: Planning

```
1. Review _ROADMAP.md
   ├── What did we ship last week?
   ├── What's the focus this week?
   └── Any priorities need adjusting?

2. Define work packages for the week
   ├── Usually 2-3 packages
   └── Each should be shippable

3. Activate Product Manager for any new specs
```

### Tuesday-Thursday: Execution

```
Normal daily rhythm:
├── Clear decisions
├── Activate agents
├── Ship what's ready
└── Repeat
```

### Friday: Review and Ship

```
1. Push to ship what's ready
   ├── Final QA passes
   ├── Security approvals
   └── Deploy

2. Review the week
   ├── What shipped?
   ├── What didn't? Why?
   └── What did we learn?

3. Light planning for next week
```

---

## Managing Multiple Work Packages

Once you're comfortable, you'll have multiple packages flowing:

```
Package A: ███████████░░░░ [Frontend]
Package B: █████░░░░░░░░░░ [Spec]
Package C: ████████████████ [Ready to Ship]
```

### How to Think About It

Each package is in a phase. Each phase has an agent. You:

1. Track which packages exist
2. Know which phase each is in
3. Activate agents when phases are ready
4. Checkpoint when packages reach you

### Limiting Work in Progress

**Don't have too many active packages.**

Why:
- Each package needs your attention at checkpoints
- Too many = context switching hell
- Things slip through

**Recommended:** 2-3 active packages at a time.

If someone asks for something new: "Great idea. It's next after we ship Package B."

---

## Decision Velocity

Your main bottleneck is decisions. Optimize for speed:

### Batch Decisions

Don't context-switch for every small decision. Let them queue:

```markdown
## Decision Queue

### Blocking (decide now)
- Auth: JWT vs sessions?

### Non-Blocking (decide by EOD)
- Dashboard: Cache TTL?
- Profile: Show email publicly?
```

### Pre-Decide Categories

Reduce runtime decisions by deciding upfront:

```markdown
## Standing Decisions

**When in doubt:**
- Use existing libraries over custom code
- Prefer simple over clever
- Mobile-first, responsive second
- Security over convenience
```

Agents reference these. Fewer questions for you.

### Trust Recommendations

When agents give a recommendation, they've thought about it. Most of the time: "Approved. Proceed."

---

## When to Step In as Builder

Sometimes you should write code yourself:

### Good Reasons to Build

- **Complex logic only you understand** — The matching algorithm, the pricing logic
- **Critical path with subtle requirements** — Auth flow, payment processing
- **Faster to do than explain** — A 20-minute fix vs a 40-minute explanation
- **You want to stay sharp** — Keep your skills current

### Bad Reasons to Build

- **You don't trust agents** — They're good. Let them prove it.
- **It's more fun** — Fun is fine, but leverage is better
- **You're a perfectionist** — "Good enough" ships. Perfect doesn't.

### The Test

Ask: "Is this the highest-value use of my time right now?"

If yes, build. If no, activate an agent.

---

## Handling Problems

### Agent Is Stuck

```
Agent: "I'm not sure how to proceed with X"

You: Look at what they're stuck on. Either:
1. Make a decision to unblock them
2. Provide more context
3. Do that part yourself and let them continue
```

### Work Is Taking Too Long

```
Check:
- Is the scope too big? Break it down.
- Is the agent unclear on requirements? Clarify.
- Is this actually complex? Maybe it should take this long.
```

### Quality Isn't Right

```
Options:
1. Give feedback, have them revise
2. Add to _CONVENTIONS.md to prevent recurrence
3. Review more carefully at earlier checkpoints
```

### You're Overwhelmed

```
Symptoms: Too many decisions, can't keep up

Fix:
1. Reduce active work packages
2. Increase auto-proceed (trust agents more)
3. Pre-decide more categories
4. Batch decisions more aggressively
```

---

## Scaling Up

As you get comfortable:

### Phase 1: Sequential

One work package at a time. Master the workflow.

### Phase 2: Parallel

2-3 work packages at once. Practice context switching.

### Phase 3: Autonomous

More auto-proceed. Agents coordinate without you. You checkpoint at major moments only.

### Phase 4: Strategic

You're mostly in Architect and Reviewer mode. Building strategy, approving ships. Agents run day-to-day.

---

## Working Across Projects

Unlike git, your agents aren't confined to one repository. In a single session, you can:

- Work on `~/projects/app-one`, then switch to `~/projects/app-two`
- Reference the framework at `~/.agentic` while building
- Start a brand new project mid-session
- Copy patterns from one project to another

### Multiple Projects

```
You: What's the status on the mobile app?

Chief of Staff: [checks ~/projects/mobile-app]
Mobile app: Auth complete, dashboard in progress.

You: Good. Switch to the marketing site — how's the blog feature?

Chief of Staff: [checks ~/projects/marketing-site]
Blog feature: In QA. Two minor bugs found, being fixed.
```

### Starting a New Project

```
You: I need to spin up a new project for the admin dashboard.

Chief of Staff: I'll set that up.

mkdir ~/projects/admin-dashboard
cd ~/projects/admin-dashboard
git init
cp -r ~/.agentic/templates/docs ./

Created. What's the core purpose of this admin dashboard?
```

### Sharing Patterns

```
You: The auth flow in project-a worked well. Use the same pattern in project-b.

Chief of Staff: I'll read the auth implementation from project-a and apply it here.
[reads ~/projects/project-a/lib/auth/]
[implements in ~/projects/project-b/lib/auth/]
```

The starting directory is just where the conversation begins — not a boundary.

---

## Anti-Patterns

### Micro-Managing

**Symptom:** Checking every commit, reviewing every decision
**Problem:** You're the bottleneck. Defeats the purpose.
**Fix:** Trust agents. Checkpoint at phases, not tasks.

### Never Building

**Symptom:** Always orchestrating, never coding
**Problem:** You lose technical edge. Some things need your hands.
**Fix:** Schedule Builder mode. Stay sharp.

### Always Building

**Symptom:** You do everything yourself, agents idle
**Problem:** No leverage. You're limited by your time.
**Fix:** Force yourself to delegate. Start small.

### Approval Bottleneck

**Symptom:** Work packages stuck waiting for you
**Problem:** Agents can't proceed. Momentum lost.
**Fix:** Clear the queue daily. Be responsive.

### Too Many Packages

**Symptom:** 5+ active packages, constant context switching
**Problem:** Things fall through. Quality drops.
**Fix:** Limit WIP. Finish before starting.

---

## The Liberation

Here's what operating well feels like:

**Morning:**
You open `_TODAY.md`. Three decisions. You make them in 5 minutes. A package is ready to ship — you approve. Done.

**Midday:**
You're on a call with a potential customer. Agents are building features in parallel. You're not worried about it.

**Afternoon:**
You check status. Two packages progressed. One hit a bug — QA found it, it's being fixed. You didn't have to do anything.

**Evening:**
You shipped a feature today. Another is ready for tomorrow. You worked on the product for 30 minutes. The rest was founder work.

**The feeling:**
You have a team. They're competent. They work without you watching. You make decisions, not do tasks. You're building a company, not just writing code.

---

## Summary

### Daily

| When | What | Time |
|------|------|------|
| Morning | Read `_TODAY.md`, clear decisions, activate agents | 15 min |
| Day | Do founder work, check status occasionally | As needed |
| Evening | Review progress, clear final decisions | 10 min |

### Weekly

| Day | Focus |
|-----|-------|
| Monday | Plan the week, define packages |
| Tue-Thu | Execute, ship |
| Friday | Push to ship, review, light planning |

### Mindset

- You're the decision maker, not the doer
- Trust agents to execute
- Checkpoint at phases, not tasks
- Clear decisions quickly
- Limit work in progress
- Ship small, ship often

---

## You're Ready

You've learned:

1. **The Model** — How agents work together
2. **Your Role** — What you do vs what they do
3. **The Agents** — Your team of 14
4. **The Workflow** — How work flows
5. **Getting Started** — How to set up
6. **Your First Day** — What day one looks like
7. **Operating** — The ongoing rhythm

Now go build something.

---

## Reference Material

When you need to go deeper:

| Resource | Use When |
|----------|----------|
| `reference/roles/` | You want to understand an agent better |
| `reference/concepts/` | You want theory on a topic |
| `templates/` | You're starting a new project |

---

## One More Thing

Remember:

**You could hire 12 people.** Deal with recruiting, interviewing, onboarding, managing, retaining, replacing.

**Or you could do this.** Define the work. Activate agents. Make decisions. Ship.

You're not alone anymore. You have a team.

Go build.

