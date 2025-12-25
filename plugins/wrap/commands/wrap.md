---
allowed-tools: Bash(git:*), Read(*), Write(*), Edit(*)
description: Close out work with handoff notes and commit
---

## Context

- Working directory: !`pwd`
- Git status: !`git status`
- Changes (staged and unstaged): !`git diff HEAD | head -500`
- Recent commits: !`git log --oneline -5`
- Current agents file: !`cat docs/_AGENTS.md 2>/dev/null || echo "No docs/_AGENTS.md found"`
- Current today file: !`cat docs/_TODAY.md 2>/dev/null || echo "No docs/_TODAY.md found"`

## Your Task

Execute the wrap protocol:

### 1. Analyze Changes

Review the git diff and understand:
- What files were modified
- What the changes accomplish
- Why decisions were made (infer from code patterns, comments, naming)

### 2. Write Handoff

Generate handoff notes with this structure:

```
**Done:**
- [Concrete list of what was completed]

**Why it's built this way:**
- [Key decisions and reasoning]
- [Tradeoffs made]

**For next:**
- Key files: `path/file.ts:line` (with specific locations)
- [What the next agent needs to know or do]
```

### 3. Update Coordination Files

If `docs/_AGENTS.md` exists:
- Add handoff to the Handoffs section with today's date
- Update Recently Completed
- Clear your row from Active Terminals (if present)

If `docs/_TODAY.md` exists:
- Add to Done Recently section

### 4. Stage and Review

- Stage all relevant changes
- For non-trivial changes, note if code review is recommended
- Skip review for: single-file doc changes, config only, formatting only

### 5. Commit

Create a commit with a clear message following conventional commit style if the repo uses it.

### 6. Report

Summarize:
- What was wrapped up
- What was committed
- Any handoff notes for the next role
- Suggested next steps
