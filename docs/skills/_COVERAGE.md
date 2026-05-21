---
Created: 2026-05-21
Last updated: 2026-05-21
Source: Job 01 Full Run — coverage analysis
Context: Coverage summary for all 182 canonical courses (deduplicated from 241 SCORM packages)
Status: COMPLETE — full run
---

# Coverage — Full Run (182 canonical courses)

## Series Breakdown

| Series | Code | Count | Example |
|--------|------|-------|---------|
| IFL | Introduction to Field Leadership | 45 | IFL-00 through IFL-44 |
| LEAN | Lean Construction | 21 | LEAN-00 through LEAN-20 |
| VDL | Values Driven Leadership | 19 | VDL-00 through VDL-18 |
| AOP | Art of Presenting | 13 | AOP-00 through AOP-12 |
| CLT | Critical Leadership Training | 11 | CLT-00 through CLT-10 |
| LOTO | Lockout Tagout | 12 | LOTO-00 through LOTO-11 |
| EQ | Emotional Intelligence | 8 | EQ-00 through EQ-07 |
| FP | Fall Protection | 8 | FP-00 through FP-07 |
| SC | Safety Coordinator | 8 | SC-00 through SC-07 |
| ES | Electrical Safety | 7 | ES-00 through ES-06 |
| SO | Safety Orientation | 6 | SO-00 through SO-05 |
| HAZCOM | Hazard Communication | 5 | HAZCOM-00 through HAZCOM-04 |
| TEAM | Team Management | 5 | TEAM-00 through TEAM-04 |
| PERF | Performance Management | 4 | PERF-00 through PERF-03 |
| SAFE | General Safety | 3 | SAFE-00 through SAFE-02 |
| ACC | Accubid | 2 | ACC-00, ACC-01 |
| PC | ProCore/ViewPoint | 2 | PC-00, PC-01 |
| CS | Confined Space | 1 | CS-00 |
| COMM | Communication | 1 | COMM-00 |
| FTM | Foreman Training Manual | 1 | FTM-00 |

**Total: 182 courses across 20 series**

## Deduplication Summary

| Metric | Value |
|--------|-------|
| Total SCORM packages | 241 |
| Duplicate groups | 49 |
| Duplicate alternates removed | 57 |
| Junk entries removed (TEST, untitled) | 2 |
| Canonical courses in CODE_REGISTRY | 182 |

### Dedup Rule
Prefer descriptive slug over UUID, locale-present over no-locale, skip `(2)` suffix copies.

## Skill Coverage

| Metric | Value |
|--------|-------|
| S5 skills matched to courses | 91 of 124 (73%) |
| S5 skills NOT matched | 33 (27%) |

### Untouched Skills (33)

| Category | Skills | Reason |
|----------|--------|--------|
| AI & Technology (no SCORM yet) | SK-001 to SK-004 | No AI courses in SCORM catalog |
| Fine-grained safety specializations | SK-056, SK-059, SK-062, SK-064, SK-067, SK-069, SK-070, SK-071, SK-078, SK-085, SK-087, SK-091, SK-097 | Courses exist but match more general skills first; will be caught in manual per-course review |
| Leadership/soft skill variants | SK-015, SK-017, SK-020, SK-022, SK-039, SK-047, SK-048, SK-104, SK-105 | Keyword overlap with broader skills; needs content-level review |
| Software specializations | SK-114, SK-116, SK-118, SK-119, SK-120, SK-122 | Accubid/ProCore courses exist but keywords too specific for automated match |

## Classification Stats

| Metric | Value |
|--------|-------|
| INTRO courses | ~2 (CLT-00, and any Chapter 0 patterns) |
| SKILLS courses | ~180 |
| With locale (content extractable) | ~135 |
| Without locale (video-only/older) | ~47 |
| With knowledge checks | ~90 |
| With quizzes | 2 |
| Unclassified | 0 |

## Output Files

| File | Location | Description |
|------|----------|-------------|
| CODE_REGISTRY.csv | `docs/skills/CODE_REGISTRY.csv` | 182 rows, semicolon-delimited. Slug → Code → Title → Series → Type → Skills |
| skill_course_crosswalk_full.csv | `docs/skills/skill_course_crosswalk_full.csv` | 674 rows. Skill-to-course mappings with awarded levels and confidence |
| _DUPLICATES.md | `docs/skills/_DUPLICATES.md` | 49 duplicate groups for manual canonical slug confirmation |
