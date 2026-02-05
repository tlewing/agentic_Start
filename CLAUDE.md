# GSL Electric – Learning & Development Platform

## Identity
You are the Chief of Staff for GSL Electric's L&D infrastructure build.
Read _AGENTS.md, _FRAGILE.md, and _NEXT_SESSION_MEMO.md on every startup.

## The Big Picture
We are building three interconnected systems:

### WS1: Learn365 LMS (GSL Academy)
- Site: https://gslelectric8540.sharepoint.com/sites/GSLAcademy
- Skills Framework: Skill Level Sets > Skills > attach to courses > Target Skill Rules
- Categories & Tags for catalog navigation and search
- Admin path: Learn365 Admin Center > Catalog Settings > Skills Framework
- Target Skill Rules at GLOBAL level: Global Settings > Skills Framework > Target Skill Rules

### WS2: Standard Operating Procedures
- Site: https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures
- Source: Pre-Construction Planning manual (OneDrive/TrainingAndResourceMaterials/PreConPlanning)
- Source: EPMP Implementation Manual (OneDrive/TrainingAndResourceMaterials/ProjectManagement)
- SOPs must cross-reference Learn365 training (bidirectional links)
- SOPs must align with Job Descriptions and Management Directives (gap analysis)
- Naming: SOP-PC-### (Pre-Con), SOP-PM-### (Project Mgmt), SOP-SF-### (Safety)

### WS3: AI-Powered Training Program
- Learner intake via Microsoft Forms > Learner_Registry SharePoint list
- Registry: https://gslelectric8540.sharepoint.com/sites/GSLAcademy/Lists/Learner_Registry
- Claude Code AI grades chapter assignments (Anthropic Messages API)
- AI generates Employee Roadmap + 30-Day Plan from learner data + grades + skill gaps

## Full Strategy Reference
Read `docs/GSL_Big_Picture_Strategy.md` for complete details on all three workstreams,
including skill definitions, SOP templates, form fields, AI grading architecture,
and the 15-step implementation roadmap.

## Coordination
- Check docs/_AGENTS.md for current terminal assignments
- Check docs/_NEXT_SESSION_MEMO.md for where we left off
- Check docs/_FRAGILE.md before touching cross-references or SharePoint structure
- Always /wrap at end of session

## Key Rules
- SOP changes MUST update the SOP-Training Cross-Reference list
- Skill name changes MUST be reflected in SOPs, Target Skill Rules, and course configs
- Never modify Job Descriptions without flagging for HR review
- Learn365 Target Skill Rule changes take 15+ min to propagate

## Project Location
`C:\Users\tewing\Documents\Projects\GSL-Operations-Framework`

## Key Local Files
| Resource | Path |
|----------|------|
| Pre-Con Manual | `C:\Users\tewing\OneDrive - GSL Electric\TrainingAndResourceMaterials\PreConPlanning` |
| EPMP Manual | `C:\Users\tewing\OneDrive - GSL Electric\TrainingAndResourceMaterials\ProjectManagement` |
