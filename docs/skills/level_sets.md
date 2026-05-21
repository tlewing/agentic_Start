---
Created: 2026-05-21
Last updated: 2026-05-21
Source: Job 01 Phase 2 — derived from 00_Path_A_Architecture_Decision_2.md
Context: Defines the two level sets for the Learn365 skills framework. Used by all skill awards, target rules, and self-evaluations.
Status: PILOT — for Tom's review
---

# Level Sets

## A. Measurement Level Set (Self-Evaluation)

Used when learners rate their OWN proficiency. Full 0–4 scale.

| Level | Name | Descriptor |
|-------|------|------------|
| 0 | Not yet exposed | Has not encountered this skill in training or practice. No familiarity with concepts or procedures. **Measurement-only — never a target or award.** |
| 1 | Learning | Has been introduced to the concepts. Needs step-by-step guidance to attempt the skill. Can recognize key terms and describe the general purpose. |
| 2 | Working | Can perform the skill with some support or reference material. Understands the procedures and can execute them in standard situations with occasional guidance. |
| 3 | Proficient | Performs the skill independently and consistently. Can troubleshoot common issues, adapt to variations, and produce reliable results without supervision. |
| 4 | Expert | Can teach, mentor, or lead others in this skill. Understands edge cases, underlying principles, and can develop or improve procedures. Recognized resource for the team. |

## B. Award / Target Level Set

Used when COURSES award skills and when TARGET RULES set expectations per role. Excludes 0.

| Level | Name | When Awarded by a Course | When Set as a Target |
|-------|------|--------------------------|----------------------|
| Learning | Learning | Intro/exposure courses that introduce concepts without hands-on practice | Role requires awareness-level familiarity |
| Working | Working | Courses that include hands-on practice, exercises, or procedural walkthroughs | Role requires ability to perform with support |
| Proficient | Proficient | Advanced courses that develop independent performance capability | Role requires independent, reliable performance |
| Expert | Expert | Courses that develop teaching, mentoring, or procedure-development capability | Role requires ability to teach/lead others in this skill |

## Display Rule

Levels are shown by **NAME** (Learning, Working, Proficient, Expert), never by number, in all user-facing and rule contexts. Numbers exist underneath only for the self-eval gap math. This prevents collision with the Performance Review 1–5 scale.

## Learn365 Configuration

- Create TWO level sets in Learn365 Admin > Catalog Settings > Skills Framework > Skill Level Sets:
  1. **Self-Evaluation (0–4)** — used for learner self-rating
  2. **Award/Target (Learning–Expert)** — used for course awards and target rules
- All 124 skills bind to the Award/Target set
- Both sets use the NAME descriptors above
