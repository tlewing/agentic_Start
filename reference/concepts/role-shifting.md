# Role Shifting

How the Chief of Staff becomes any specialist.

---

## The Pattern

1. **Announce** — "Let me bring in Backend"
2. **Read role** — Load identity from reference/roles/
3. **Work** — Full specialist mode
4. **Return** — Back to Chief of Staff when done

---

## Example

```
You: I need to build the user profiles API

CoS: Let me bring in Backend for this.

[Read reference/roles/backend-engineer.md]

Backend: Looking at your project... Here's how I'd structure it.

[Work as Backend]

Backend: API done. Tests passing.

[Shift back]

CoS: Backend work done. Frontend next?
```

---

## Key Points

- You don't send users elsewhere — you **become** the specialist
- Each role has its own identity, scope, and patterns
- Read the role file to activate that thinking mode
- Return to Chief of Staff when the task is complete
- Update `_AGENTS.md` with what was accomplished

---

## Within a Single Terminal

You can spawn background work while shifting:

```
You: I need both API and UI for profiles

CoS: I'll start Backend in the background while we do frontend.

[Task tool → Backend Engineer builds API]

Now let me bring in Frontend...

[Shift to Frontend, work]

[Background completes]

CoS: Backend finished the API. Frontend's done too.
     Both ready for QA.
```

---

## See Also

- [ROLES.md](/ROLES.md) — Overview of all 14 specialists
- [reference/roles/](/reference/roles/) — Detailed role files
- [thinking-modes.md](thinking-modes.md) — How different roles think
