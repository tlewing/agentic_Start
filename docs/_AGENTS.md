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

## Workstream: Learn365 Skills Framework (WS1)

### Current State
SCORM taxonomy pass COMPLETE. All 185 unique SCORM courses classified with category, tags, skills, difficulty, target roles, and descriptions. 55 existing skills mapped, 0 new skills proposed. Canonical output: `data/scorm_taxonomy_recommendations.json`. Summary report with appendices: `data/scorm_taxonomy_summary.md`.

Key stats:
- 185 courses, 55 skills, 40 categories, 9 roles
- Confidence: 13 HIGH, 21 MEDIUM-HIGH, 53 MEDIUM, 97 LOW, 1 VERY LOW
- 172 courses need transcript retrieval to upgrade descriptions
- 71 duplicate SCORM packages need consolidation
- 3 proposed Difficulty tags (Foundational/Intermediate/Advanced)
- 2 NEEDS-REVIEW remaining (Untitled, TEST — both flagged for removal)
- All 38 scale sets have 0 defined levels — skill levels pending Admin config

### Blockers
- 172 transcript gaps — need VTT retrieval from Learn365/Azure for accurate descriptions
- Scale set levels need Admin Center UI configuration before skill levels can be assigned
- 36 unused scale sets should be deleted in Admin Center
- Tag data quality issues: leading space on ` lockout/tagout`, typos (Budgetting, Transparancy), trailing comma on `label,`

### Planner Tasks (Open)
- Apply taxonomy recommendations to Learn365 Admin (descriptions, categories, tags, skills) (Important)
- Retrieve transcripts for 172 courses to upgrade LOW/MEDIUM confidence descriptions (Medium)
- Define scale set levels in Admin Center (Medium)
- Delete 36 unused scale sets (Low)
- Consolidate 71 duplicate SCORM packages (Medium)
- Fix tag typos in Learn365 vocabulary (Low)

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
SCORM taxonomy pass completed 2026-05-20. All 185 courses have recommendations ready for Learn365 Admin application. Next priority: apply descriptions/categories/tags/skills via Learn365 API or Admin UI, then retrieve transcripts to upgrade 172 LOW/MEDIUM confidence descriptions. SOP voice reviews and WS4 Pre-Planning App remain paused pending Tom's availability.
