# Sample Course Catalog Entries

**Date:** 2026-01-17
**Status:** Pattern Established

---

## Catalog Entry Format

Each course will have the following metadata:

| Field | Description |
|-------|-------------|
| Course ID | SCORM package identifier |
| Title | Official course title |
| Short Description | 1-2 sentence summary (for LMS display) |
| Long Description | Full course description (for course detail page) |
| Skill Level Set | One of the 10 approved sets |
| Primary Skill | Main skill developed |
| Secondary Skills | Additional skills (if applicable) |
| Category | Top-level category |
| Subcategory | Second-level category |
| Tags | Searchable keywords |
| Duration | Estimated completion time |
| Proficiency Level | Awareness / Basic / Proficient / Advanced / Expert |
| Prerequisites | Required prior courses (if any) |
| Series | Course series name (if part of a series) |
| Series Order | Position in series (if applicable) |

---

## Sample Entry 1: Safety - NFPA 70E

| Field | Value |
|-------|-------|
| **Course ID** | dumyti56 |
| **File** | 2024-nfpa-70-e-required-boundaries-scorm12-dumyti56.zip |
| **Title** | 2024 NFPA 70E Required Boundaries |
| **Short Description** | Learn the required approach boundaries for electrical safety per the 2024 NFPA 70E standard. |
| **Long Description** | This course covers the critical approach boundaries defined in the 2024 edition of NFPA 70E (Standard for Electrical Safety in the Workplace). You will learn to identify and apply the Limited Approach Boundary, Restricted Approach Boundary, and Arc Flash Boundary. Understanding these boundaries is essential for protecting workers from electrical hazards during energized work. |
| **Skill Level Set** | Safety |
| **Primary Skill** | Approach Boundary Management |
| **Secondary Skills** | NFPA 70E Fundamentals, Arc Flash Awareness |
| **Category** | Safety & Compliance |
| **Subcategory** | Electrical Safety |
| **Tags** | NFPA 70E, electrical safety, approach boundaries, arc flash, shock hazard, 2024 |
| **Duration** | 15-20 min |
| **Proficiency Level** | Proficient |
| **Prerequisites** | NFPA 70E Fundamentals recommended |
| **Series** | 2024 NFPA 70E Training |
| **Series Order** | - |

---

## Sample Entry 2: Leadership

| Field | Value |
|-------|-------|
| **Course ID** | xpvxgbur |
| **File** | 1-0-coach-k-teaches-values-driven-leadership-scorm12-xpvxgbur.zip |
| **Title** | Coach K Teaches Values-Driven Leadership |
| **Short Description** | Learn values-driven leadership principles from legendary Coach Mike Krzyzewski. |
| **Long Description** | Legendary Duke basketball coach Mike Krzyzewski (Coach K) shares his approach to leading with values at the core. This course explores how to define and communicate core values, build trust through consistent behavior, and create a culture where team members are motivated by shared purpose rather than external rewards. Applicable to construction foremen, superintendents, and project leaders. |
| **Skill Level Set** | Leadership & Field Management |
| **Primary Skill** | Values-Driven Leadership |
| **Secondary Skills** | Leadership Fundamentals, Team Building |
| **Category** | Leadership & Management |
| **Subcategory** | Leadership Fundamentals |
| **Tags** | values, leadership, culture, Coach K, motivation, team building |
| **Duration** | 20-25 min |
| **Proficiency Level** | Basic |
| **Prerequisites** | None |
| **Series** | Leadership Foundations |
| **Series Order** | 1.0 |

---

## Sample Entry 3: Lean Construction

| Field | Value |
|-------|-------|
| **Course ID** | pvxdpabr |
| **File** | chapter-05-what-is-lean-scorm12-pvxdpabr.zip |
| **Title** | Chapter 05 - What is Lean? |
| **Short Description** | Introduction to Lean principles and their application in construction. |
| **Long Description** | This course introduces the fundamental concepts of Lean methodology. You will learn what Lean is, where it originated (Toyota Production System), and how its principles of waste elimination and continuous improvement apply to the construction industry. This foundation is essential for understanding subsequent Lean construction techniques. |
| **Skill Level Set** | Lean Construction |
| **Primary Skill** | Lean Fundamentals |
| **Secondary Skills** | Lean History |
| **Category** | Lean & Productivity |
| **Subcategory** | Lean Principles |
| **Tags** | lean, waste elimination, Toyota, continuous improvement, construction |
| **Duration** | 15-20 min |
| **Proficiency Level** | Awareness |
| **Prerequisites** | None |
| **Series** | Introduction to Lean Construction |
| **Series Order** | 5 |

---

## Sample Entry 4: Field Leadership

| Field | Value |
|-------|-------|
| **Course ID** | vclfcl72 |
| **File** | coordinating-with-other-trades-introduction-to-field-leadership-section-2-scorm12-vclfcl72.zip |
| **Title** | Coordinating with Other Trades - Introduction to Field Leadership Section 2 |
| **Short Description** | Learn effective techniques for coordinating work with other trades on the jobsite. |
| **Long Description** | Successful electrical construction requires seamless coordination with mechanical, plumbing, structural, and other trades. This course teaches foremen and field leaders how to communicate effectively with other trade supervisors, resolve scheduling conflicts, share workspace efficiently, and maintain productive relationships. Part of the Introduction to Field Leadership series. |
| **Skill Level Set** | Leadership & Field Management |
| **Primary Skill** | Trade Coordination |
| **Secondary Skills** | Effective Communication, Field Supervision |
| **Category** | Field Operations |
| **Subcategory** | Trade Coordination |
| **Tags** | trade coordination, foreman, field leadership, communication, scheduling, jobsite |
| **Duration** | 20-25 min |
| **Proficiency Level** | Basic |
| **Prerequisites** | Introduction to Field Leadership Section 1 |
| **Series** | Introduction to Field Leadership |
| **Series Order** | 2 |

---

## Sample Entry 5: Safety Orientation

| Field | Value |
|-------|-------|
| **Course ID** | k9ggo4z0 |
| **File** | a-commitment-to-zero-broken-lives-new-hire-safety-orientation-scorm12-k9ggo4z0.zip |
| **Title** | A Commitment to Zero Broken Lives - New Hire Safety Orientation |
| **Short Description** | GSL's core safety orientation for all new hires, emphasizing our commitment to zero injuries. |
| **Long Description** | This is GSL Electric's foundational safety orientation course for all new employees. "Zero Broken Lives" reflects our commitment that every worker returns home safely. This course covers GSL's safety culture, individual responsibility for safety, stop-work authority, hazard recognition basics, and reporting procedures. Required for all new hires before beginning field work. |
| **Skill Level Set** | Safety |
| **Primary Skill** | Safety Awareness & Culture |
| **Secondary Skills** | Hazard Recognition, Accident Prevention |
| **Category** | Safety & Compliance |
| **Subcategory** | General Safety |
| **Tags** | new hire, orientation, safety culture, zero injuries, GSL, onboarding |
| **Duration** | 30-45 min |
| **Proficiency Level** | Awareness |
| **Prerequisites** | None (required for all new hires) |
| **Series** | New Hire Safety Orientation |
| **Series Order** | 1 |

---

## Pattern Summary

### Course ID Extraction
- Extract from filename suffix (e.g., `dumyti56` from `...-scorm12-dumyti56.zip`)
- Use for unique identification in LMS

### Title Cleanup
- Remove "Chapter XX - " prefixes for standalone display
- Keep series/section info in Series fields
- Standardize capitalization

### Skill Level Set Assignment Rules
1. **Safety** - Any NFPA 70E, LOTO, fall protection, scaffolding, HazCom, general safety
2. **Lean Construction** - Waste, flow, continuous improvement, lean principles
3. **Leadership & Field Management** - Foreman topics, team building, leadership principles, supervision
4. **Communication & Coaching** - Feedback, mentoring, conflict, GROW model
5. **Emotional Intelligence** - EQ, self-awareness, empathy, social skills
6. **Performance Management** - Evaluations, counseling, discipline
7. **Construction Software** - ViewPoint, ProCore, Accubid, Excel, Job Plans
8. **Project Planning & Productivity** - Scheduling, productivity, time management
9. **Documentation & Compliance** - Reporting, regulatory, documentation
10. **Professional Development** - Presentations, career growth

### Category Mapping
| Skill Level Set | Primary Category |
|-----------------|------------------|
| Safety | Safety & Compliance |
| Lean Construction | Lean & Productivity |
| Leadership & Field Management | Leadership & Management / Field Operations |
| Communication & Coaching | Communication & Interpersonal |
| Emotional Intelligence | Communication & Interpersonal |
| Performance Management | Leadership & Management |
| Construction Software | Construction Software |
| Project Planning & Productivity | Project Management |
| Documentation & Compliance | Project Management |
| Professional Development | Professional Development |

---

## Next Steps

1. **Approve pattern** - Confirm this catalog entry format
2. **Process all courses** - Extract metadata from all ~180-200 unique courses
3. **Export to spreadsheet** - Create SCORM_COURSE_CATALOG.xlsx with all entries
4. **Create Target Skill Rules** - Map roles to required courses

---

**Pattern established. Ready to process full catalog.**
