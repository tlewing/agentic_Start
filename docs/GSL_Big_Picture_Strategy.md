# GSL Electric – The Big Picture Strategy

> **This file is the strategy reference for Claude Code sessions.**
> The authoritative source is a Claude.ai conversation. When updates occur there,
> this file will be updated with instructions on what changed.

---

## Overview

GSL Electric is building a unified Learning & Development infrastructure across three interconnected workstreams:

- **WS1: Learn365 LMS** – Skills framework, categories, tags, target skill rules
- **WS2: Standard Operating Procedures** – SOPs derived from reference manuals with bidirectional training cross-references
- **WS3: AI-Powered Training Program** – Forms intake, Claude API grading, personalized roadmaps

---

## Workstream 1: Learn365 LMS Configuration

**Location:** https://gslelectric8540.sharepoint.com/sites/GSLAcademy
**Navigation:** Learn365 Admin Center

### Phase 1A – Enable Global Features

- LMS Configuration > Global Settings > Skills framework features
- Toggle on: Self-evaluation, Target skills and skill gap
- Enable AI features: Content generation, AI skills suggestions, Training recommendations

### Phase 1B – Skill Level Sets (Catalog Level)

**Path:** Catalog Settings > Skills Framework > Manage Skill Level Sets

Four recommended sets:

1. **Standard Proficiency:** Beginner > Intermediate > Advanced
   - Use for: professional development, software, soft skills
2. **Technical Competency:** Awareness > Competent > Proficient > Expert
   - Use for: trade skills, electrical procedures, equipment, PM processes
3. **Compliance & Safety:** Untrained > Trained > Certified
   - Use for: OSHA, NFPA 70E, arc flash, LOTO, first aid
4. **Leadership:** Foundational > Developing > Accomplished
   - Use for: supervisory, mentoring, change management

### Phase 1C – Create Skills (Catalog Level)

**Path:** Catalog Settings > Skills Framework > Manage Skills

Skill domains aligned to SOP structure:

**Safety & Compliance:**
- OSHA 10/30, NFPA 70E, LOTO, Confined Space, Fall Protection, First Aid/CPR

**Pre-Construction Planning:**
- Project Scoping, Estimating, Submittal Management, Scheduling, Budget Development, Value Engineering

**Project Management (EPMP):**
- Change Order Management, RFI Process, Cost Tracking, Progress Reporting, Closeout, Quality Control

**Electrical Technical:**
- Residential/Commercial/Industrial Wiring, NEC Code, Blueprint Reading, Conduit Bending

**Professional Development:**
- Customer Communication, Time Management, Team Collaboration, Learn365 Platform

**Leadership:**
- Crew Supervision, Project Leadership, Mentoring, Change Management

> **Critical alignment:** Pre-Con Planning and PM skill domains map directly to chapters in the reference manuals (Pre-Construction Planning Process, EPMP Implementation Manual). Each SOP corresponds to one or more skills.

### Phase 1D – Categories and Tags (Catalog Level)

**Path:** Catalog Settings > Categories / Tags

**Category structure (parent > subcategories):**

| Parent Category | Subcategories |
|----------------|---------------|
| Safety & Compliance | OSHA, Arc Flash, Fall Protection, Confined Space, Hazard Communication, PPE |
| Pre-Construction Planning | Estimating, Scheduling, Submittals, Budgeting, Value Engineering, Project Scoping |
| Project Management | Change Orders, RFIs, Cost Tracking, Progress Reporting, Closeout, Quality Control |
| Electrical Skills | Residential, Commercial, Industrial, Code & Standards, Blueprint Reading |
| Professional Development | Communication, Customer Service, Time Management, Career Growth |
| Leadership & Management | Supervisory Skills, Project Leadership, Mentoring |
| Onboarding & Orientation | New Hire, Company Policies, Systems & Tools, Learn365 Platform |
| SOPs & Procedures | Pre-Con SOPs, PM SOPs, Safety SOPs, Administrative SOPs |

**Tag strategy:** 5-15 tags per course covering:
- Abbreviations: LOTO, RFI, CO, NEC, NFPA
- Synonyms: change order = variation = modification
- Job roles: apprentice, journeyman, foreman, PM, superintendent
- Training types: required, annual, refresher, certification
- Regulatory references: 29 CFR 1926, NFPA 70E

Maintain a master spreadsheet before data entry.

### Phase 1E – Target Skill Rules (Global Level)

**Path:** Global Settings > Skills Framework > Target Skill Rules
**Requires:** LMS Admin permissions

| Rule Name | Target Skills | Criterion |
|-----------|--------------|-----------|
| All Employees – Safety Baseline | OSHA 10-Hour/Certified, First Aid/CPR/Certified, Learn365 Platform/Beginner | Global (all users) |
| Project Managers – Pre-Con & PM | Pre-Construction Planning/Proficient, Change Order Mgmt/Proficient, Cost Tracking/Proficient, Estimating/Proficient | Job Title = Project Manager |
| Field Electricians – Core | NFPA 70E/Certified, LOTO/Certified, NEC Code/Competent, Blueprint Reading/Competent | Department = Field Operations |
| Supervisors & Foremen | Crew Supervision/Developing, OSHA 30-Hour/Certified, Project Leadership/Developing | Job Title contains Foreman or Supervisor |
| Apprentice Electricians | Residential Wiring/Competent, Conduit Bending/Competent, Blueprint Reading/Awareness | Job Title = Apprentice |

**Bulk import via CSV:** Format `CatalogName/SkillName/SkillLevel` (e.g., `GSL Academy/NFPA 70E/Certified`). Changes take 15+ minutes to propagate.

---

## Workstream 2: Standard Operating Procedures

**Location:** https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures

### Source Materials

1. **GSL Pre-Construction Planning Process** – `C:\Users\tewing\OneDrive - GSL Electric\TrainingAndResourceMaterials\PreConPlanning`
2. **EPMP Implementation Manual** – `C:\Users\tewing\OneDrive - GSL Electric\TrainingAndResourceMaterials\ProjectManagement`
3. **GSL Job Descriptions** – Validation: ensures every procedure required by role is covered by SOP
4. **Management Directives** – Validation: ensures directives operationalized as SOPs; gaps trigger updates

### SOP Development Process

#### Step 1 – Extract Procedures from Reference Manuals

Read each chapter. For each distinct procedure, create an extraction log identifying:
- Procedure name
- Source chapter
- Purpose
- Roles involved
- Forms/tools referenced

#### Step 2 – Cross-Reference Against JDs and Directives

Three-column gap analysis:
- **Covered:** Procedure exists in manual AND appears in JD/Directive → no action
- **Gap in JD/Directive:** Procedure in manual but not in JD/Directive → add to JD/Directive OR flag as supplementary
- **Gap in SOP:** JD/Directive requires procedure not in manuals → create new SOP OR determine covered under different name

#### Step 3 – Draft SOPs Using Standard Template

Template sections:
- **SOP Number** (e.g., SOP-PC-001 for Pre-Con, SOP-PM-001 for PM)
- **Title**
- **Purpose** (why SOP exists, problem it solves)
- **Scope** (which roles, projects, situations)
- **Reference Source** (manual name and chapter)
- **Procedure Steps** (numbered, sequential)
- **Responsible Roles** (job titles accountable)
- **Related Training** (links to Learn365 courses/training plans)
- **Related SOPs** (upstream/downstream links)
- **Related JD/Directive** (links to requiring documents)
- **Version/Effective Date** (version number, last updated, next review)

#### Step 4 – Build Bidirectional Cross-References

**CRITICAL REQUIREMENT:** SOPs reference training, training references SOPs.

Implementation:
- **SOP side:** Add "Related Training" metadata column (hyperlink or managed metadata) linking to Learn365 course URLs
- **Training side:** Include SOP links in Learn365 course description or custom content section; add SOP number as tag (e.g., `SOP-PC-005`)
- **Master registry:** Create SharePoint list "SOP-Training Cross-Reference" on GSL Academy with columns: SOP Number, SOP Title, Related Course URL(s). Query from either site for updates.

#### Step 5 – Publish and Govern

Store in dedicated document library on SOP site with metadata:
- Department
- Category (Pre-Construction, Project Management, Safety, Administrative)
- Status (Draft, Under Review, Approved, Archived)
- Review Date

Enable version control. Use Power Automate for review reminders.

---

## Workstream 3: AI-Powered Training Program

**Location:** GSL Academy + Microsoft Forms + Claude Code AI

### Component A – Learner Data Collection

**Learner_Registry list:** https://gslelectric8540.sharepoint.com/sites/GSLAcademy/Lists/Learner_Registry/AllItems.aspx

**Recommended form fields (11 total):**

| # | Field | Type | Purpose |
|---|-------|------|---------|
| 1 | Full Name | Single line text | Identity |
| 2 | Email | Single line text | Communication, Learn365 profile matching |
| 3 | Current Job Title | Choice/dropdown | Maps to Target Skill Rules, drives AI personalization |
| 4 | Department | Choice/dropdown | Maps to Learn365 user properties |
| 5 | Years with GSL Electric | Number | Tenure-appropriate recommendations |
| 6 | Years in Electrical Trade | Number | Distinguishes experienced hires from career starters |
| 7 | Current Certifications | Multi-select | Establishes baseline, AI skips redundant training |
| 8 | Highest Education Level | Choice | Context for AI communication style and depth |
| 9 | Career Aspiration | Multi-line text | Free-form, AI shapes roadmap direction |
| 10 | Supervisor Name | Single line/people picker | Routing roadmap output and 30-day plan review |
| 11 | Primary Work Type | Choice | Determines relevant SOP domain and skill sets |

**Connection methods:**
- Option 1 (simplest): Microsoft Lists Forms feature – open Learner_Registry list > Forms > New Form
- Option 2: Standalone Microsoft Form + Power Automate flow

### Component B – Claude Code AI Grading

**Workflow:**
1. Learner completes chapter assignment via Learn365 or connected form
2. Assignment text sent to Claude API with grading rubric + learner profile from Learner_Registry
3. Claude evaluates against rubric, accounting for experience level. Response includes: numeric/letter grade, detailed feedback, SOP/training references, confidence assessment
4. Grade, feedback, skill-gap indicators written to SharePoint list (Assignment_Results) or Learn365 training record

**Implementation:**
- Use Anthropic Messages API
- Production: Power Automate flow or Azure Function/Node.js app
- Models: `claude-sonnet-4-5-20250929` (cost efficiency) or `claude-opus-4-5-20251101` (max quality)
- Request JSON format response: `{grade, feedback, SOP_references, skill_gaps, recommended_next_steps}`

### Component C – Employee Roadmap and 30-Day Plan

**Employee Roadmap (longer-term):**
AI synthesizes learner profile + assignment grades + current skills vs target skills + relevant SOPs.
Outputs: recommended courses, skills to develop (3-6-12 months), certifications, practical experiences.

**30-Day Plan (immediately actionable):**
Specific courses (weeks 1-4), SOPs to read/acknowledge, on-the-job tasks, supervisor check-ins, measurable goals.

**Generation process:**
1. Gather: Learner_Registry data, assignment grades, current Learn365 skills, target skills, SOP-Training Cross-Reference
2. Construct comprehensive prompt for Claude with all context
3. AI generates both documents in structured format
4. Save to GSL Academy or email to learner/supervisor

---

## Integration Map – Data Flows

```
Reference Manuals ──→ SOPs (procedures become SOPs)
SOPs ←──→ Learn365 Courses (bidirectional links)
SOPs ←──→ Job Descriptions/Directives (gap analysis validation)
Learn365 Skills ──→ Target Skill Rules (skills become role requirements)
Learner Registry ──→ Training Program + Claude AI (personalizes grading & roadmaps)
Claude AI Grading ──→ Learn365 Skills + Roadmaps (results inform skill awards & development path)
```

---

## Master Implementation Roadmap (15 Steps)

| Step | WS | Task | Depends On |
|------|----|------|-----------|
| 1 | WS1 | Enable Skills Framework features and AI features | LMS Admin access, subscription |
| 2 | WS1 | Create Skill Level Sets (4 sets) | Step 1 |
| 3 | WS1 | Create Skills (all domains) | Step 2 |
| 4 | WS2 | Extract procedures from Pre-Con and EPMP manuals | Access to manuals |
| 5 | WS2 | Cross-reference procedures against JDs/Directives | Step 4 + JDs |
| 6 | WS2 | Draft SOPs with standard template | Steps 4-5 |
| 7 | WS1 | Build Categories and Tags aligned to SOP domains | Step 6 SOP structure |
| 8 | WS1 | Create courses/training plans, attach Skills/Categories/Tags | Steps 3, 6, 7 |
| 9 | WS2 | Build SOP-Training Cross-Reference list, populate links | Steps 6, 8 |
| 10 | WS1 | Configure Target Skill Rules (global and role-specific) | Steps 3, 5 |
| 11 | WS3 | Design/deploy Learner Registry form, connect to list | List exists |
| 12 | WS3 | Build Claude Code AI grading integration | Steps 8, 11, API key |
| 13 | WS3 | Build Roadmap and 30-Day Plan generator | Steps 10, 11, 12 |
| 14 | All | Validate end-to-end | All steps |
| 15 | All | Communicate and launch | Step 14 |

---

## Key Reference Locations

| Resource | Location |
|----------|----------|
| GSL Academy | https://gslelectric8540.sharepoint.com/sites/GSLAcademy |
| Learner_Registry | https://gslelectric8540.sharepoint.com/sites/GSLAcademy/Lists/Learner_Registry/AllItems.aspx |
| SOP Site | https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures |
| Pre-Con Manual | `C:\Users\tewing\OneDrive - GSL Electric\TrainingAndResourceMaterials\PreConPlanning` |
| EPMP Manual | `C:\Users\tewing\OneDrive - GSL Electric\TrainingAndResourceMaterials\ProjectManagement` |
| Zensai Help – Skills | helpcenter.zensai.com/hc/en-us/articles/360019465798 |
| Zensai Help – Target Skills | helpcenter.zensai.com/hc/en-us/articles/18421817003421 |
| Zensai Help – Categories | helpcenter.zensai.com/hc/en-us/articles/360019333977 |
| Zensai Help – Tags | helpcenter.zensai.com/hc/en-us/articles/360019333737 |
