# Agents

Source of truth for "where are we?" Agents read this at session start. Update it when finishing work.

---

## Active Terminals

| Terminal | Role | Working On | Files Touching | Last Update |
|----------|------|------------|----------------|-------------|
| 1 | Backend | Profiles API | lib/profiles.ts, migration 058 | Dec 25 |
| 2 | Frontend | Profile screen | app/profile.tsx, components/profile/ | Dec 25 |
| 3 | QA | Auth flow tests | __tests__/auth/ | Dec 25 |

Update when starting a terminal. Clear your row on wrap.

---

## Active

| Role | Working On | Status |
|------|------------|--------|
| Backend | Profiles API endpoints | In progress — CRUD done, need soft delete |
| Frontend | Profile edit screen | Blocked — waiting on API |
| QA | Auth flow regression | Running tests |

---

## Cross-Agent Notes

*Leave notes here for other agents. Check this section when you activate.*

**For Frontend (from Backend):**
- Profiles API landing at `/api/profiles` — ready for integration
- Types exported from `lib/types.ts` — use `Profile` interface
- Soft delete means `deleted_at` column, not actual deletion

**For QA (from Backend):**
- New RLS policies on profiles table — test with different user roles
- Test account: testuser@example.com

---

## Migration Number Coordination

*Prevents conflicts when multiple agents create migrations.*

| Number | Agent | Purpose | Status |
|--------|-------|---------|--------|
| 058 | Backend | profiles table | In progress |
| 059 | Backend | profile settings | Reserved |
| 060 | — | Available | — |

---

## Handoffs

Capture what was done **and why**. So the next agent (or you, an hour later) has context.

### Dec 25 — Backend

**Done:**
- Profiles API with CRUD operations
- Soft delete implementation (not hard delete)
- RLS policies for profile access

**Why it's built this way:**
- Soft deletes: Users may want to restore accounts
- Rate limited to 100/min: Based on expected 50 concurrent users
- No caching: Premature optimization, can add later if needed

**For Frontend:**
- Endpoints ready at `/api/profiles`
- Types in `lib/types.ts`
- Use `useProfile` hook for queries

---

## Decisions Needed

| Question | Options | Blocking? |
|----------|---------|-----------|
| Profile image storage | Supabase Storage vs Cloudinary | Yes (Frontend) |
| Max profile bio length | 500 chars vs 1000 chars | No |

---

## Recently Completed

| What | When | Notes |
|------|------|-------|
| Auth flow | Dec 24 | Google OAuth only, no password |
| Dashboard v2 | Dec 24 | New layout with stats cards |
| Onboarding | Dec 23 | 4-step flow, waiver signing |

---

## Standing Decisions

Decisions already made. Agents should follow these.

- **Auth:** Google OAuth only, no password auth
- **Styling:** Use theme tokens from constants/theme.ts, no hardcoded colors
- **Types:** All new types go in lib/types.ts, TypeScript strict mode
- **Tests:** Minimum 50% coverage on lib/, Jest for unit tests
- **Commits:** Conventional commits (feat:, fix:, docs:, etc.)

---

## Notes

Anything else agents should know.

- Test accounts: testuser@example.com (regular), admin@example.com (admin)
- Staging URL: https://staging.example.com
- CI/CD runs on push to main
