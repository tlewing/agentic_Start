# GSL Academy Tagging Taxonomy Spec

**Version:** 1.0
**Date:** 2026-05-21
**Scope:** All Learn365 courses across GSL Academy, Safety Training, and Sandbox catalogs (185 SCORM courses)

---

## Core Rule

**One course = one category + N tags.**

- **Categories** are mutually exclusive. Every course gets exactly ONE home category. Categories are for navigation and reporting roll-ups.
- **Tags** are many-to-many. A course carries as many tags as apply. Tags are for search, filtering, and cross-cutting views.
- **Skills** (competencies) are separate from categories. A course can award skills in multiple buckets. Skills are for learner competency tracking.

---

## 1. Course Categories (Navigation Hierarchy)

6 top-level categories, each with up to 6 sub-categories. A course is assigned to the **most specific sub-category** that fits. If none fits, assign to the parent.

### 1.1 Safety

Home for all safety, hazard, compliance, and orientation content. **54 courses.**

| Sub-Category | Description | Course Count |
|-------------|-------------|-------------|
| Electrical Safety | NFPA 70E, arc flash, shock boundaries, energized work | 7 |
| Lockout/Tagout | LOTO procedures, energy control, simple/complex/abnormal | 11 |
| Fall Protection & Scaffolding | Fall arrest, scaffolds, ladders, slips/trips/falls, edges/openings | 7 |
| Hazard Communication | HazCom program, SDS, container labels, chemical hazards | 4 |
| Safety Coordination | Safety coordinator series (orientation, task training, meetings, inspections, investigations, injury mgmt), OSHA/MSHA | 11 |
| General Safety & Orientation | New hire orientation, safety culture, confined spaces, TRACK, general safety awareness | 14 |

**Existing Learn365 IDs to reuse:** Safety (b1428e36), Electrical Safety (b3f5658e), Lockout / Tagout (5ad5da44), Slips, Trips, & Falls (25f7d11a), Hazard Communication (5e97f03d)

**New sub-categories to create:** Safety Coordination, General Safety & Orientation

**Categories to retire:** Employee Orientation, OSHA & MSHA Inspections, Risk Assessment, Safety Planning, Safety Coordinator, Work Area Inspections, Vehicle/Equipment Inspections, Hazard Awareness, First Aid / CPR / AED (merge into sub-categories above)

### 1.2 Leadership

Home for leadership development, field leadership training, values, performance, and policy/compliance content. **79 courses.**

| Sub-Category | Description | Course Count |
|-------------|-------------|-------------|
| Field Leadership Fundamentals | FL Section 1 (skills, traits, responsibilities, roles, communication, time mgmt, team morale, tools/tech) | 19 |
| Project Execution & Planning | FL Section 2 (job plan theory, jobsite efficiency, trade coordination, document mgmt, manpower projection, closeout) | 12 |
| Strategic Leadership | Critical Leadership Training (Extreme Ownership, leadership laws, team building, decision-making) | 13 |
| Values-Driven Leadership | Coach K series (core values, winning team, recruiting, feedback, emotional leadership, legacy) | 18 |
| Performance Management | Performance reviews, corrective counseling, motivating teams, sub-contractor mgmt, on-site productivity | 8 |
| Policy & Compliance | FL Part 4 (FMLA, harassment/discrimination, substance abuse, EAP/mental health) | 9 |

**Existing Learn365 IDs to reuse:** Leadership (7aa1b7b6), Leadership Fundamentals (2d9e4984), Skills, Traits, & Responsibilities (ef6bb972), Performance (a2c33965)

**New sub-categories to create:** Project Execution & Planning, Strategic Leadership, Values-Driven Leadership, Policy & Compliance

**Categories to retire:** Accountability, Delegation, Document Control, Extreme Ownership, Field Empowerment, Labor Planning, Mentor\Teaching, Project Planning & Scheduling, Resource Planning, Strategy, Tools & Technology, Workforce Management, Team Building & Teamwork, General Personal Development, Personal Development, Professional Development, People and Communication Skills, Stress Management (merge into sub-categories above)

### 1.3 Lean Construction

Home for all lean methodology, waste reduction, production planning, and continuous improvement content. **21 courses.**

| Sub-Category | Description | Course Count |
|-------------|-------------|-------------|
| Lean Foundations & Philosophy | What is lean, history, TFV theory, lean vs manufacturing, adoption of new theory | 9 |
| Waste Reduction & Process Improvement | Identifying waste, minimizing waste at project level, 8 wastes, process change | 4 |
| Production Planning & Control | Pull planning, sticky note format, field personnel empowerment | 3 |
| Continuous Improvement & Industry Change | Continuous improvement, training the industry, reshaping the industry, productivity in construction | 5 |

**Existing Learn365 IDs to reuse:** Lean Principals (02396841), Lean Fundamentals (f449071f), Waste Management (c5304c97), Pull Planning (449cba81), Continuous Improvement (55afd43b)

**New sub-categories to create:** Lean Foundations & Philosophy (replaces Lean Fundamentals), Continuous Improvement & Industry Change

**Categories to retire:** Industry Transformation, Process Management, Respect For People (merge into sub-categories above)

### 1.4 Communication & Soft Skills

Home for emotional intelligence, interpersonal skills, presentation skills, and self-management content. **27 courses.**

| Sub-Category | Description | Course Count |
|-------------|-------------|-------------|
| Emotional Intelligence | EQ series (self-awareness, self-regulation, empathy, social skills, self-motivation) | 7 |
| Communication & Presentation | Art of Presenting series, effective communication techniques | 16 |
| Self-Management | Motivation, leadership with emotion, bounce back, self-regulation | 4 |

**Existing Learn365 IDs to reuse:** Soft Skills (0556915b), Emotional Intelligence (6e98492b), Communication (f730178a), Self-Regulation (a44162b9)

**New sub-categories to create:** Communication & Presentation (consolidates Presenting + Presentation Skills)

**Categories to retire:** Presentation Skills, Empathy, Feedback, Motivation, Self-Awareness, Social Skills (merge into sub-categories above)

### 1.5 Software & Technical Skills

Home for software training and tool-specific technical skills. **4 courses (will grow).**

| Sub-Category | Description | Course Count |
|-------------|-------------|-------------|
| Estimating Software | Accubid Pro, Trimble estimating tools | 2 |
| Project Management Software | ViewPoint change orders, Vista | 2 |

**Existing Learn365 IDs to reuse:** Estimating (c3798891), Project Management (0d020aba), Accubid (ad7516a1), Change Orders (09b3195e)

**Categories to retire:** Technology Skills, Task Training (merge as needed)

### 1.6 Culture & Professional Development

Placeholder for culture, values, and professional growth content that doesn't fit other buckets. **0 courses currently assigned; reserved for future content (AI & Technology, onboarding beyond safety, culture/values standalone courses).**

| Sub-Category | Description | Course Count |
|-------------|-------------|-------------|
| Culture & Values | Company mission, core values, ethics | 0 |
| AI & Technology | AI tools, technology adoption | 0 |

**Existing Learn365 IDs to reuse:** Culture (3e2ee9e9), Artificial Intelligence (ce06fd30)

**Categories to retire:** Customer Service, Sales and Customer Service, Qualified Person, Procedure, Project Closeout, Safety Procedure, Test (clean up junk)

---

## 2. Skill Buckets (Competency Tracking)

These are the 9 competency roll-ups from the position-skills-courses matrix. A course can award skills in **one or more** buckets (unlike categories, skills are not mutually exclusive).

| # | Skill Bucket | Description | Courses Awarding |
|---|-------------|-------------|-----------------|
| 1 | Safety | Hazard recognition, compliance, safe work practices | 54 |
| 2 | Leadership | People leadership, decision-making, team development | 51 |
| 3 | Soft Skills | EQ, communication, interpersonal effectiveness | 27 |
| 4 | Lean Principles | Lean thinking, waste reduction, production planning | 23 |
| 5 | Culture & Values | Company mission, ethics, core values | 18 |
| 6 | Software | Tool-specific technical proficiency | 4 |
| 7 | Management | Process, systems, administrative management | 4 |
| 8 | Procurement | Purchasing, subcontractor management, buyout | 2 |
| 9 | AI & Technology | AI tools, technology adoption, digital literacy | 0 (gap) |

Skills are tracked via Learn365's Competencies feature. Each skill has a name and belongs to one bucket. The full skill list (96 existing + any new) maps to these 9 buckets.

---

## 3. Controlled Tag Vocabulary

Tags are organized into **facets** — logical groupings that keep the flat tag list clean and filterable. All tags use **lowercase-hyphenated** canonical spelling. No free-typing; all tags come from this controlled list.

### Naming Convention

- All lowercase
- Hyphens between words (not spaces, not underscores)
- No duplicates or near-duplicates (one canonical form per concept)
- Difficulty and Audience tags use `Title Case:` prefix for easy filtering

### 3.1 Safety Tags

#### Concept / Hazard Tags
`electrical-safety` `arc-flash` `shock-hazard` `nfpa-70e` `lockout-tagout` `hazardous-energy` `fall-protection` `scaffolding` `ladder-safety` `slips-trips-falls` `confined-spaces` `hazard-communication` `chemical-hazard` `safety-data-sheets` `ppe` `safety-culture` `zero-broken-lives` `osha` `msha`

#### Method / Procedure Tags
`energy-control-procedure` `simple-loto` `complex-loto` `abnormal-removal` `return-to-service` `de-energization-verification` `fall-arrest-system` `guardrail-system` `safety-inspection` `pre-task-assessment` `incident-investigation` `safety-meeting` `task-training` `disciplinary-action` `injury-case-management` `hazard-elimination` `risk-assessment`

#### Equipment / System Tags
`harness` `lanyard` `anchorage` `insulated-tools` `voltage-tester` `scaffold-platform` `ghs-labels` `safety-net`

### 3.2 Leadership Tags

#### Concept / Framework Tags
`extreme-ownership` `cover-and-move` `prioritize-and-execute` `decentralize-command` `values-driven-leadership` `servant-leadership` `emotional-leadership` `field-leadership` `team-building` `succession-planning`

#### Method / Practice Tags
`performance-review` `corrective-counseling` `delegation` `job-plan` `manpower-projection` `trade-coordination` `document-management` `project-closeout` `team-motivation` `feedback` `mentoring` `coaching` `recognition`

#### Policy Tags
`fmla` `harassment-prevention` `discrimination-prevention` `substance-abuse` `eap` `mental-health`

### 3.3 Lean Construction Tags

#### Concept / Framework Tags
`lean-construction` `lean-thinking` `value-stream` `transformation-flow-value` `muda-mura-muri` `8-wastes` `continuous-improvement` `respect-for-people` `just-in-time`

#### Method / Tool Tags
`pull-planning` `sticky-note-planning` `kaizen` `pdca` `5-whys` `5s` `value-stream-mapping` `gemba-walk` `root-cause-analysis` `waste-identification` `waste-minimization`

#### Industry Tags
`lean-adoption` `industry-transformation` `field-empowerment` `production-theory`

### 3.4 Soft Skills & Communication Tags

#### Concept / Framework Tags
`emotional-intelligence` `self-awareness` `self-regulation` `empathy` `social-skills` `self-motivation` `active-listening`

#### Method / Practice Tags
`presentation-skills` `slide-preparation` `public-speaking` `effective-communication` `clear-messaging` `conflict-resolution` `rapport-building` `de-escalation`

### 3.5 Software Tags

`accubid` `trimble` `viewpoint` `vista` `change-orders` `takeoff` `cost-codes` `procore` `bluebeam` `excel` `outlook`

### 3.6 Cross-Cutting Tags

These tags span multiple categories and are used for filtering across the catalog.

#### Difficulty Tags
`Difficulty: Foundational` `Difficulty: Intermediate` `Difficulty: Advanced`

#### Audience / Role Tags
`Audience: All Employees` `Audience: Field Entry` `Audience: Field Journeyman` `Audience: Field Leadership` `Audience: Superintendents` `Audience: Project Management` `Audience: General Superintendent` `Audience: Safety` `Audience: Estimating` `Audience: Engineering` `Audience: Administration` `Audience: Executive`

#### Content Type Tags
`series-chapter` `standalone` `ai-generated` `orientation` `certification-required`

---

## 4. Assignment Rules

### Rule 1: Category Assignment
1. Read the course title, description, and series membership.
2. Assign to the **single most specific sub-category** where the course's primary learning objective lives.
3. If the course could fit two categories equally (rare), choose the one matching its **series** (e.g., a communication course in the Field Leadership series goes under Leadership > Field Leadership Fundamentals, not Communication & Soft Skills).

### Rule 2: Tag Assignment
1. Apply all **concept/framework tags** that the course directly teaches.
2. Apply all **method/tool tags** that the course demonstrates or requires the learner to practice.
3. Apply exactly ONE **Difficulty** tag based on the position-skills matrix:
   - Foundational = required for Field Entry / Apprentice
   - Intermediate = required starting at Journeyman or Leadman/Foreman
   - Advanced = required starting at Superintendent or above
4. Apply **Audience** tags based on the mandatory_for and recommended_for fields in course_taxonomy_assignments.json:
   - If a position group is in `mandatory_for`, tag with that audience
   - If a position group is in `recommended_for`, also tag (audience tags don't distinguish M vs R — the skill bucket matrix handles that)
5. Apply **Content Type** tags where applicable (series-chapter for multi-part series, ai-generated for Synthesia content, etc.)

### Rule 3: Skill Assignment
1. Assign skills from the existing Learn365 skill list (96 skills).
2. Each skill maps to exactly one of the 9 skill buckets.
3. A course can award 1-3 skills. Prefer specificity (e.g., "LOTO Fundamentals" over generic "Personal Safety").
4. If no existing skill fits, flag for review — do not create ad hoc skills.

### Rule 4: No Orphans
Every course must have: 1 category, at least 1 tag, at least 1 skill (except TEST/UNKNOWN courses flagged for removal).

---

## 5. Tag Cleanup: Old vs New

The Learn365 vocabulary snapshot shows **393 existing tags**. Most are free-typed garbage with inconsistent casing, typos, and duplicates. Examples of problems:

| Problem | Examples |
|---------|----------|
| Duplicate concepts | `Budgeting` vs `Budgetting`, `5S` vs `five-s`, `LOTO` vs `lockout/tagout` vs `lockout` |
| Inconsistent casing | `Safety` vs `safety`, `Leadership` vs `leadership` |
| Trailing spaces/punctuation | `Lean Principles ` (trailing space), `label,` (trailing comma), `oversight & supervision,` |
| Too granular | `red master lock`, `screw jack`, `mud sill` |
| Too vague | `basics`, `difficult`, `process`, `systems` |

**Action:** The strip script already cleared all course-tag associations. When re-applying, use ONLY tags from this controlled vocabulary (Section 3). Old tags remain in Learn365's vocabulary but won't be assigned to any course. They can be bulk-deleted later via Admin UI.

---

## 6. Learn365 Implementation Notes

### Category Hierarchy
Learn365 supports parent > child categories. Map as:
- Top-level (Section 1.1-1.6) = parent categories
- Sub-categories = child categories under their parent

### Tag Format
Learn365 tags are flat strings. The facet organization (Section 3) is a **design convention**, not enforced by the system. The prefixed tags (`Difficulty:`, `Audience:`) use the colon format to make them filterable in the Learn365 UI.

### Skills / Competencies
Learn365 skills are assigned per-course and auto-awarded on completion. The 96 existing skills cover all current needs. The 9 skill buckets are a reporting concept — Learn365 doesn't have a "bucket" layer, so bucket membership is tracked in this spec and in the position-skills-courses matrix.

### API Fields (PATCH /odata/v2/Courses({Id}))
- `Categories` — array of category objects `[{"Id": "...", "Name": "..."}]`
- `Tags` — array of tag strings `["tag1", "tag2"]`
- `Competencies` — array of skill objects `[{"Id": "...", "Name": "..."}]`

---

## 7. Category-to-Bucket Mapping

Each category maps to a **primary skill bucket** for reporting. This is which bucket gets credit when a course in that category is completed.

| Category | Primary Skill Bucket |
|----------|---------------------|
| Safety > Electrical Safety | Safety |
| Safety > Lockout/Tagout | Safety |
| Safety > Fall Protection & Scaffolding | Safety |
| Safety > Hazard Communication | Safety |
| Safety > Safety Coordination | Safety |
| Safety > General Safety & Orientation | Safety |
| Leadership > Field Leadership Fundamentals | Leadership |
| Leadership > Project Execution & Planning | Leadership |
| Leadership > Strategic Leadership | Leadership |
| Leadership > Values-Driven Leadership | Leadership |
| Leadership > Performance Management | Management |
| Leadership > Policy & Compliance | Culture & Values |
| Lean Construction > Lean Foundations & Philosophy | Lean Principles |
| Lean Construction > Waste Reduction & Process Improvement | Lean Principles |
| Lean Construction > Production Planning & Control | Lean Principles |
| Lean Construction > Continuous Improvement & Industry Change | Lean Principles |
| Communication & Soft Skills > Emotional Intelligence | Soft Skills |
| Communication & Soft Skills > Communication & Presentation | Soft Skills |
| Communication & Soft Skills > Self-Management | Soft Skills |
| Software & Technical Skills > Estimating Software | Software |
| Software & Technical Skills > Project Management Software | Software |
| Culture & Professional Development > Culture & Values | Culture & Values |
| Culture & Professional Development > AI & Technology | AI & Technology |

---

## Appendix A: Categories to Create in Learn365

New categories that don't exist in the current vocabulary:

| Parent | New Sub-Category |
|--------|-----------------|
| Safety | Safety Coordination |
| Safety | General Safety & Orientation |
| Leadership | Project Execution & Planning |
| Leadership | Strategic Leadership |
| Leadership | Values-Driven Leadership |
| Leadership | Policy & Compliance |
| Lean Principals | Lean Foundations & Philosophy |
| Lean Principals | Continuous Improvement & Industry Change |
| Soft Skills | Communication & Presentation |
| Soft Skills | Self-Management |

**Total new categories:** 10

## Appendix B: Categories to Retire from Learn365

These exist in the current vocabulary but will not be used. They can be deleted after all courses are re-tagged.

Accountability, Assured Grounding, Customer Service, Delegation, Document Control, Employee Orientation, Estimating Fundamentals, Extreme Ownership, Feedback, Field Empowerment, General Personal Development, Hazard Awareness, Industry Transformation, Labor Planning, Mentor\Teaching, OSHA & MSHA Inspections, People and Communication Skills, Personal Development, Policy, Presenting, Procedure, Process Management, Professional Development, Project Closeout, Project Planning & Scheduling, Qualified Person, Resource Planning, Respect For People, Risk Assessment, Safety Coordinator, Safety Culture, Safety Planning, Safety Procedure, Sales and Customer Service, Self-Awareness, Social Skills, Strategy, Stress Management, Task Training, Team Building & Teamwork, Technology Skills, Test, Tools & Technology, Vehicle/Equipment Inspections, Work Area Inspections, Workforce Management

**Total categories to retire:** 46

## Appendix C: Tags to Create (New)

These tags are needed but don't exist in the current 393-tag vocabulary:

**Difficulty tags:** `Difficulty: Foundational`, `Difficulty: Intermediate`, `Difficulty: Advanced`

**Audience tags:** `Audience: All Employees`, `Audience: Field Entry`, `Audience: Field Journeyman`, `Audience: Field Leadership`, `Audience: Superintendents`, `Audience: Project Management`, `Audience: General Superintendent`, `Audience: Safety`, `Audience: Estimating`, `Audience: Engineering`, `Audience: Administration`, `Audience: Executive`

**Content type tags:** `series-chapter`, `standalone`, `ai-generated`, `orientation`, `certification-required`

**Total new tags:** 20

All other tags in Section 3 either exist already or will be created on first use when courses are tagged via API (Learn365 auto-creates tags on PATCH).
