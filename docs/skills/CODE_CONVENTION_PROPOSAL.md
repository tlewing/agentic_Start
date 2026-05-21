---
Created: 2026-05-21
Last updated: 2026-05-21
Source: Job 01 Phase 3 — Pilot code convention proposal
Context: Proposed naming convention for canonical course codes (PASS 2 of the two-pass scheme). Currently using SCORM slug as working key (PASS 1).
Status: APPROVED (2026-05-21) — SERIES-## format, no type indicator
---

# Course Code Naming Convention — Approved

## Format

```
{SERIES}-{##}
```

| Component | Description | Examples |
|-----------|-------------|---------|
| **SERIES** | 2–5 letter abbreviation for the course series | CLT, VDL, LOTO, FP, LEAN, SO |
| **##** | Zero-padded chapter number within the series | 00, 01, 02, 08 |

Course type (intro vs skills) lives in the crosswalk metadata, not the code. This keeps codes stable if a course is reclassified.

## Pilot Examples

| Code | Full Title | Series | Course Type |
|------|-----------|--------|-------------|
| CLT-00 | Chapter 0 - Introduction to Critical Leadership Training | Critical Leadership Training | INTRO |
| CLT-01 | Chapter 1 - What Makes A Leader | Critical Leadership Training | SKILLS |
| VDL-01 | 1.0 Coach K Teaches Values-Driven Leadership | Values Driven Leadership | SKILLS |
| VDL-08 | Values Driven Leadership: 8 Effective Communication | Values Driven Leadership | SKILLS |
| LOTO-01 | Lockout Tagout - Hazardous Energy Control | Lockout Tagout | INTRO |
| LOTO-02 | Simple Lockout-Tagout Procedures | Lockout Tagout | SKILLS |
| LOTO-03 | Complex Lockout-Tagout Procedures | Lockout Tagout | SKILLS |
| FP-04 | Using Portable and Fixed Ladders | Fall Protection | SKILLS |
| LEAN-01 | Chapter 01 - Embracing Lean Productivity | Lean Construction | SKILLS |
| SO-01 | New Hire Safety Orientation | Safety Orientation | SKILLS |

## Proposed Series Abbreviations (to validate against full catalog)

| Abbreviation | Series | Est. # Courses |
|-------------|--------|----------------|
| CLT | Critical Leadership Training | ~15 |
| VDL | Values Driven Leadership | ~15 |
| LOTO | Lockout Tagout | ~7 |
| FP | Fall Protection | ~5 |
| LEAN | Lean Construction | ~10 |
| SO | Safety Orientation | 1+ |
| FTM | Foreman Training Manual | ~13 |
| HAZCOM | Hazard Communication | ~6 |
| CS | Confined Space | ~3 |
| ES | Electrical Safety | ~10 |
| ER | Emergency Response | ~5 |
| EQ | Emotional Intelligence | ~6 |
| ACC | Accubid | ~7 |
| PC | ProCore | ~3 |

## Rules

1. **SERIES abbreviation must be unique** across the full catalog
2. **NUMBER reflects position within the series**, not difficulty level
3. **Intro courses use `I`**, skills courses use `C`**
4. **Standalone courses** (not part of a series) use the series abbreviation + `C1`
5. **CODE_REGISTRY.csv** is the authoritative lookup: Slug | Canonical Code | Course Title | Series

## What Tom Needs to Decide

1. **Is the `SERIES-TYPE#` format workable?** Alternative: `SERIES-###` (e.g., CLT-001) without type indicator.
2. **Series abbreviation preferences** — any GSL conventions to follow?
3. **Numbering**: Should intro always be `I0` (zero-indexed) or `I1` (one-indexed)?
4. **Standalone courses**: Use `C1` or just `C` with no number?

Once approved, PASS 2 produces `CODE_REGISTRY.csv` with all 185 courses mapped.
