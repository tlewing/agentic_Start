# Wrap Protocol

The standard way to close out a piece of work.

---

## Trigger

User says any of:
- `wrap`
- `wrap it up`
- `close this out`
- `/wrap`

---

## The Protocol

When triggered, execute these steps in order:

### 1. Document What Was Done

Update `docs/_AGENTS.md`:
- Move completed items from "Task Queue" to "Recently Completed"
- Add date to completed items
- Update "Current Status" section

```markdown
### Recently Completed
- [x] User profiles API (Dec 24)
- [x] Profile screen UI (Dec 24)
```

### 2. Write Handoff Notes

If the next phase involves a different agent, add handoff notes:

```markdown
### Handoff: Backend Engineer → Frontend Engineer

**Work Package:** User Profiles
**State:** Complete | Auto-Proceed

**For Frontend Engineer:**
- API endpoints: GET/POST /api/profiles
- Types in lib/types.ts
- Tests in __tests__/api/profiles.test.ts

**For Founder (FYI):**
- Implemented as specified
- Added rate limiting
- No concerns
```

### 3. Update _TODAY.md

Add to the "Since Yesterday" or equivalent section:
- What was completed
- Any decisions made
- Any concerns raised

### 4. Commit and Push

```bash
git add -A
git status  # Show what's being committed
git commit -m "feat(profiles): complete user profiles API and UI

- Add GET/POST /api/profiles endpoints
- Add profile screen with edit capability
- Add tests for API and components

🤖 Generated with Claude Code"
git push
```

Always show the user what's being committed before doing it.

### 5. Clean Up Task Tracking

Check for stale items:
- Look at `docs/_TODAY.md` pending items
- Look at `docs/_AGENTS.md` task queues
- Look at any `docs/plans/*.md` files

For each item marked "pending" or "in progress":
- Check if the code/feature actually exists
- If done → mark complete
- If not done → keep as pending, note it

### 6. Verify Outstanding Items

For any remaining "pending" items:
```
Outstanding items I found:

1. [ ] Add password validation (in _AGENTS.md)
   Status: NOT DONE - still needs implementation

2. [ ] Update error messages (in _TODAY.md)
   Status: DONE - marking complete

3. [ ] Write API documentation (in plans/profiles.md)
   Status: PARTIAL - endpoints documented, examples missing
```

### 7. Report Summary

```
## Wrap Summary

**Completed:**
- User profiles API (4 endpoints, 12 tests)
- Profile screen UI (3 components)

**Committed:** abc123f - "feat(profiles): complete user profiles API and UI"

**Cleaned up:**
- Marked 2 items complete in _AGENTS.md
- Removed stale plan file

**Still pending:**
- Password validation (needs implementation)
- API examples (partial)

**Ready for:** QA Engineer
```

---

## Quick Version

For small changes, the protocol can be abbreviated:

```
Wrap Summary:
- Committed: "fix: profile image upload"
- No outstanding items
- Ready for: QA
```

---

## When to Use

- After completing a feature or significant piece of work
- At end of a work session
- Before switching to a different work package
- Before handing off to another agent

---

## Who Can Trigger

Any agent can execute the wrap protocol. The Chief of Staff, Backend Engineer, Frontend Engineer — whoever is active when the user says "wrap."

