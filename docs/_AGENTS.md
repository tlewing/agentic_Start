# GSL-Operations-Framework — Agent Status

Last updated: 2026-05-22 (wrap — taxonomy re-apply + verification complete)

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

## Workstream: Learn365 Skills & Catalog (WS1) — Taxonomy Rebuild

### Current State
TAXONOMY RE-APPLY COMPLETE (categories only). Tags blocked by API. Skills framework ready but not yet applied in Admin UI.

**Completed 2026-05-22 (Taxonomy Re-Apply):**
- Verified 185 taxonomy assignments against SCORM descriptions (172) + VTT transcripts (102)
- 130 corrections applied: old category names remapped to spec names, confidence upgraded
- Categories applied to courses via Learn365 API PATCH — all resolve to existing IDs
- SPEC_TO_EXISTING remap eliminates need for new sub-categories (18 spec names mapped to existing Learn365 names)
- 1 unused competency deleted via API (AI Project Management)
- Confirmed: Tags CANNOT be set via PATCH (202 response but silently ignored — Learn365 API limitation)
- Confirmed: SkillLevelSets DELETE returns 406 (not supported)

**Completed 2026-05-21 (Taxonomy Strip + Classification):**
- Full taxonomy strip: all categories, tags, skills removed from 233 courses across 3 catalogs
- Pre-strip backup: 248 courses, 406 enrollments, 100 user skills preserved
- 185 SCORM courses classified with definitive taxonomy assignments
- Master spec: 6 categories, 26 sub-categories, ~80 controlled tags (faceted model)
- Position-skills-courses matrix: 12 position groups mapped to 9 skill buckets

**Completed 2026-05-21 (Job 01 — SCORM Skills Extraction):**
- 241 SCORM packages extracted, 180 canonical courses in 20 series
- 674-row skill-course crosswalk, 91/124 skills mapped

**Key artifacts:**
- `data/tagging_taxonomy_spec.md` — master taxonomy spec (APPROVED by Tom)
- `data/course_taxonomy_verified.json` — verified per-course assignments (185 courses)
- `data/learn365_categories_live.json` — 272 live categories with IDs
- `data/course_metadata_backup_20260521_050600.json` — pre-strip backup
- `scripts/apply_taxonomy.py` — API re-apply script (categories only)
- `scripts/review_taxonomy.py` — SCORM/transcript verification script

### RESUME HERE
**Pick up at: Tags + Skills in Learn365 Admin UI.**
- Tags must be applied manually in Admin UI (API doesn't support it)
- Skills framework (9 buckets, 138 skills) ready — needs Admin UI entry
- 5 unused competencies identified for deletion (API DELETE works, but needs re-run)
- Consider: batch tag entry via Admin UI CSV import if available

### Blockers
- Learn365 API does not support setting Tags on courses via PATCH
- SkillLevelSets cannot be deleted via API (406)
- 130 courses not yet uploaded to Learn365

### Planner Tasks (Open)
- Apply tags via Learn365 Admin UI (Important)
- Create 9 skill buckets and import 138 skills in Admin UI (Important)
- Delete 5 remaining unused competencies (Low)
- Upload 130 missing SCORM courses to Learn365 (Important)

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
Taxonomy rebuild complete 2026-05-22. Categories re-applied to all courses via API. Tags blocked by API — must go through Admin UI. Skills framework (9 buckets, 138 skills) designed but not yet entered. 130 courses still need SCORM upload. SOP voice reviews and WS4 Pre-Planning App remain paused pending Tom's availability.
