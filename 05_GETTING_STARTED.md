# Chapter 5: Getting Started

Set up your first project in 15 minutes.

---

## What You'll Do

1. Create your project directory
2. Copy the template files
3. Fill in your vision
4. Activate your first agent

By the end, you'll have a working project with an agent helping you.

---

## Step 1: Create Your Project

Make a new directory for your project:

```bash
mkdir my-project
cd my-project
git init
```

---

## Step 2: Copy the Templates

Copy the template files from Agentic to your project:

```bash
mkdir docs
cp ~/.agentic/templates/docs/* docs/
```

(If you cloned agentic elsewhere, adjust the path.)

You now have:

```
my-project/
└── docs/
    ├── _TODAY.md           # Your daily operations file
    ├── _AGENTS.md          # Agent coordination
    ├── _VISION.md          # What you're building
    ├── _ROADMAP.md         # Priorities and phases
    ├── _ARCHITECTURE.md    # Technical decisions
    └── _CONVENTIONS.md     # Coding standards
```

---

## Step 3: Fill In Your Vision

Open `docs/_VISION.md` and fill it in. This is the most important file — it tells agents what you're building.

You don't need to have everything figured out. Start with what you know:

```markdown
# Vision

## One-Liner
A mobile app that helps dog owners find dog walkers.

## Problem
Dog owners struggle to find reliable walkers on short notice.

## Target Users
| User | Need |
|------|------|
| Dog owners | Find walkers quickly |
| Dog walkers | Find clients easily |

## Success Looks Like
| Timeframe | Metric |
|-----------|--------|
| 3 months | 100 users in one city |
| 1 year | Profitable in 3 cities |

## Open Questions
1. Start B2C or partner with apartments?
2. How to handle trust/safety?
```

Don't worry about:
- Perfect prose
- Complete answers
- Technical details

Just get your thoughts down. The Product Manager will help refine it.

---

## Step 4: Activate Your First Agent

Now bring in your first agent — the Product Manager — to help refine your vision:

Start a Claude session and say:

```
You are ~/projects/agentic/reference/roles/product-manager.md

This is a new project. Read docs/_VISION.md and help me:
1. Ask clarifying questions about the vision
2. Identify gaps I haven't considered
3. Propose an MVP scope
4. Create a phased roadmap
```

### What Happens Next

The Product Manager will:

1. **Ask clarifying questions**
   - Who exactly is the target user?
   - What's the core value proposition?
   - What are your constraints?

2. **Identify gaps**
   - "You haven't addressed pricing — subscription or per-walk?"
   - "What about walker verification?"

3. **Propose MVP scope**
   - What's IN: Booking, basic profiles, payment
   - What's OUT: Reviews, recurring walks

4. **Create roadmap**
   - Phase 1: MVP
   - Phase 2: Trust features
   - Phase 3: Growth

### Your Job

- Answer the questions
- Make decisions on trade-offs
- Approve or adjust the scope

### What You'll Have After

- Refined `_VISION.md`
- Populated `_ROADMAP.md`
- Clear first work package

---

## Step 5: Start Your First Work Package

Once the spec is approved, you have your first work package. Activate the next agent:

If it needs design:
```
You are ~/projects/agentic/reference/roles/ux-designer.md

Read docs/_AGENTS.md. Create the user flow for [feature].
```

If it's backend-first:
```
You are ~/projects/agentic/reference/roles/backend-engineer.md

Read docs/_AGENTS.md. Design the database and API for [feature].
```

---

## Your Project Structure

After setup, your project looks like:

```
my-project/
├── docs/
│   ├── _TODAY.md           # Check this every morning
│   ├── _AGENTS.md          # Agents update this
│   ├── _VISION.md          # What you're building
│   ├── _ROADMAP.md         # Where you're going
│   ├── _ARCHITECTURE.md    # How it's built
│   └── _CONVENTIONS.md     # How you code
│
└── [your app code will go here]
```

The `docs/` folder is your command center. Everything about the project is coordinated here.

---

## The Templates Explained

### _TODAY.md

Your morning briefing. Shows:
- Decisions waiting for you
- Checkpoints pending
- What shipped recently

Read this every morning. Clear the queue. Get on with your day.

### _AGENTS.md

Agent coordination file. Contains:
- Work package status
- Agent status
- Handoff notes
- Decision queue

Agents update this as they work. You read it for status.

### _VISION.md

What you're building and why. Contains:
- The problem you're solving
- Who you're solving it for
- What success looks like

You write this. Agents read it for context.

### _ROADMAP.md

Your priorities and phases. Contains:
- Current phase
- What's in scope for MVP
- What's deferred

Product Manager helps create this. You approve it.

### _ARCHITECTURE.md

Technical decisions. Contains:
- Tech stack
- Key patterns
- Design decisions

Backend Engineer helps populate this. You approve major decisions.

### _CONVENTIONS.md

How code should be written. Contains:
- File naming
- Code style
- Testing patterns

Platform Engineer helps document this. All agents follow it.

---

## Common First Steps

### Starting from Scratch (No Code Yet)

1. Fill in `_VISION.md`
2. Activate Product Manager → Get roadmap
3. Activate Backend Engineer → Get architecture
4. Start building work packages

### Existing Project

1. Copy templates to your project
2. Document current state in `_VISION.md` and `_ARCHITECTURE.md`
3. List current priorities in `_ROADMAP.md`
4. Start using agents for new work

---

## Tips for Success

### Start Small

Your first work package should be tiny. Something you can ship in a day. Learn the workflow before tackling big features.

### One Agent at a Time (At First)

Until you're comfortable, work with one agent per session. Sequential is simpler than parallel.

### You're Still the Builder

Agents help, but make sure you understand what's being built. Review code. Stay technical.

### Document Decisions

When you decide something, write it down. In `_ARCHITECTURE.md`, `_AGENTS.md`, wherever. Future-you will be grateful.

---

## Summary

| Step | What You Do |
|------|-------------|
| 1 | Create project directory |
| 2 | Copy template files |
| 3 | Fill in `_VISION.md` |
| 4 | Activate Product Manager |
| 5 | Approve spec, start building |

**Time:** 15 minutes to setup, then you're operating.

---

→ [Chapter 6: Your First Day](06_YOUR_FIRST_DAY.md)

