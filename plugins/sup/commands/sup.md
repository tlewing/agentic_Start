---
allowed-tools: Bash(git:*), Read(*)
description: Quick check on what's up across the project
---

## Context

- Working directory: !`pwd`
- Git status: !`git status`
- Current branch: !`git branch --show-current`
- All branches: !`git branch -a`
- Stash list: !`git stash list`
- Recent commits: !`git log --oneline -10`
- Agents file: !`cat docs/_AGENTS.md 2>/dev/null || echo "No docs/_AGENTS.md found"`
- Today file: !`cat docs/_TODAY.md 2>/dev/null || echo "No docs/_TODAY.md found"`

## Your Task

Report the current coordination state:

### 1. Active Terminals

From `_AGENTS.md`, list:
- Which terminals are active
- What role each has
- What they're working on
- Files they're touching

### 2. Uncommitted Work

From git status:
- Files modified but not committed
- Files staged for commit
- Untracked files

### 3. Potential Conflicts

Cross-reference:
- If Active Terminals lists files, check if current terminal has uncommitted changes to same files
- Flag any overlap

### 4. Branch State

- Current branch and its status
- Any divergence from remote
- Other local branches with uncommitted work (if using worktrees)

### 5. Stashed Work

List any stashes that might be forgotten work.

### 6. Summary

Provide a clear status:
- "Clear to proceed" if no conflicts
- "Potential conflict with Terminal X on [files]" if overlap detected
- "Stale state in _AGENTS.md" if it seems out of date

Keep the report concise and actionable.
