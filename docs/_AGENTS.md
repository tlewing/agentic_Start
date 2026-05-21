# GSL-Operations-Framework — Agent Status

Last updated: 2026-05-20 (wrap — SCORM taxonomy complete)

---

## Workstream: SOPs (WS2)

### Current State
167 SOPs complete. Voice review workflow established. 3 phases reviewed, 8 new SOP drafts parked awaiting Tom's voice reviews.

### Blockers
- 8 SOP drafts need Tom's voice reviews before finalization
- Voice reviews needed for remaining phases (9.1, 9.4A-K, 9.5, 9.6)

### Planner Tasks (Open)
- Voice review 8 new SOP drafts (Important)
- Revise 20 existing Phase 9.2 SOPs using milestone feedback (Medium)
- Voice reviews for remaining phases (Important)
- Execute OneDrive mirror scripts (Low)

### Handoff Notes
Tom reviews draft SOPs using ChatGPT voice mode, narrating how GSL actually does things. ChatGPT produces structured RACI/milestone spreadsheets with feedback. Voice narration is authoritative, not source docs. Tom will provide the full ChatGPT chat transcript alongside the spreadsheet so Jebidiah can cross-check ChatGPT's interpretation against what Tom actually said. Voice review outputs are filed to `GSL-Operations-Framework/evaluations/`.

---

## Workstream: Learn365 Skills & Catalog (WS1) — Job 01

### Current State
JOB 01 COMPLETE through Phase 4. Skill assignment guide ready. Pick up at Learn365 Admin skill entry.

**Completed 2026-05-21 (Job 01 — SCORM Skills Extraction):**
- Extracted all 241 SCORM packages via `scripts/extract_all_scorm.py`
- Classified 180 canonical courses into 20 series (0 unclassified)
- Resolved 49 duplicate groups (57 alternates removed, 2 junk removed, 2 "Copy of" editing copies removed)
- Mapped 91 of 124 S5 skills (73%) to courses via keyword matching
- Built 674-row skill-course crosswalk with awarded levels and confidence ratings
- Approved code convention: `SERIES-##` (e.g., CLT-00, VDL-14)
- Approved catalog taxonomy: 5 categories (Safety & Compliance, Leadership Development, Operations & Productivity, Communication & Soft Skills, Technical Skills)
- Cross-referenced CODE_REGISTRY against live Learn365 catalog: 50 courses matched, 130 not yet uploaded
- Generated `LEARN365_SKILL_ASSIGNMENT_GUIDE.md` — checklist for assigning skills to the 50 courses already in Learn365

**Key artifacts (all in `docs/skills/`):**
- `CODE_REGISTRY.csv` — 180 canonical courses (slug, code, title, series, type, skills)
- `skill_course_crosswalk_full.csv` — 674 skill-to-course mappings
- `LEARN365_SKILL_ASSIGNMENT_GUIDE.md` — step-by-step skill assignment checklist (50 courses ready)
- `_DUPLICATES.md` — resolved duplicate groups (APPROVED)
- `_COVERAGE.md` — coverage analysis and gap report
- `_EXCEPTIONS.md` — overlap and edge case notes
- `CODE_CONVENTION_PROPOSAL.md` — SERIES-## format (APPROVED)
- `level_sets.md` — measurement and award level set definitions
- `per_course/` — 10 pilot extraction sheets

**Key artifacts (in `docs/catalog/`):**
- `category_scheme.md` — 5-category taxonomy (APPROVED)

**Scripts:**
- `scripts/extract_all_scorm.py` — bulk SCORM extraction (output in `%TEMP%\scorm_full_extract\`)
- `scripts/build_full_registry.py` — registry builder + dedup + classification + crosswalk

### RESUME HERE
**Pick up at: Learn365 skill assignment for the 50 courses already in the LMS.**
- Open `docs/skills/LEARN365_SKILL_ASSIGNMENT_GUIDE.md`
- Work through the checklist: open each course in Learn365 Admin > Skills, add skills with awarded levels
- Decision needed: assign skills to 50 existing courses first, OR upload 130 missing courses first?
- 2 unmatched Learn365 courses (FL01 typo, FL04 omnibus) need manual matching
- 33 S5 skills untouched by keyword matching — fill during manual per-course review

### Blockers
- 130 courses not yet in Learn365 — need SCORM upload before skills can be assigned
- 33 skills not matched by automated keyword pass — need content-level review
- FL01 ("Field Leaderaship" — typo) and FL04 (omnibus) need manual CODE_REGISTRY match

### Planner Tasks (Open)
- Assign skills to 50 courses in Learn365 Admin using guide (Important)
- Upload 130 missing SCORM courses to Learn365 (Important)
- Fill 33 untouched skills via content-level review (Medium)
- Retrieve VTT transcripts for deeper skill extraction (Medium)

---

## Workstream: Pre-Planning App (WS4)

### Current State
Not started. Architecture planned (SharePoint lists + Canvas Power App).

### Architecture (planned)
- SharePoint list: `ProjectPrePlanning` -- one record per checklist item
- SharePoint list: `Projects` -- project header info
- Power App: Canvas app with collapsible sections, status toggles, SOP links
- Power Automate: Notifications, overdue alerts, status rollups

### Blockers
- Depends on stable SOP IDs (voice reviews must be substantially complete first)

### Planner Tasks (Open)
- Complete SOP voice reviews -- dependency (Important)
- Design SharePoint list schema (Medium)
- Build Power App (Medium)
- Pilot with one real project (Medium)

### Handoff Notes
Source artifact: `evaluations/GSL_Turnover_PrePlanning_Template.xlsx` (original Smartsheet export with SOP cross-references added). Vision is to replace the 570-row Smartsheet-based "Template - GSL Turnover & Pre-Planning" checklist with a Power App providing role-based views (PM, Foreman, Estimator, GS), SOP links, mobile access, and Power Automate notifications.

---

## Workstream: WS3 (Training Widgets/Grading)

Fully absorbed into training-template project. See `training-template/docs/_AGENTS.md` for current state. Activity classification decision (Feb 17): only capstone submissions (8) feed the Playbook; mid-module exercises are self-contained AI coaching.

---

## General Handoff Notes
Job 01 (SCORM Skills Extraction) complete 2026-05-21. 180 canonical courses registered, 50 matched to live Learn365 catalog with skill assignment guide ready. Next priority: assign skills in Learn365 Admin for the 50 ready courses, then upload remaining 130. SOP voice reviews and WS4 Pre-Planning App remain paused pending Tom's availability.
