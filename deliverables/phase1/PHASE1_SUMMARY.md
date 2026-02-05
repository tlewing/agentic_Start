# Phase 1 Summary: GSL Academy Training Structure

**Date:** 2026-01-17
**Status:** Complete

---

## Deliverables Created

| File | Purpose | Location |
|------|---------|----------|
| `A_CATEGORIES.md` | 7-level category structure for 150+ modules | `deliverables/phase1/` |
| `B_SKILL_LEVEL_SETS.md` | 9 skill levels (L0-L8 + L9) aligned with job progression | `deliverables/phase1/` |
| `C_SKILLS.md` | 95 skills across 11 categories | `deliverables/phase1/` |
| `D_TARGET_SKILL_RULES.md` | 17 rules mapping roles to required training | `deliverables/phase1/` |

---

## Key Findings

### Training Library Assessment

| Metric | Value |
|--------|-------|
| Total SCORM modules | ~200 files |
| Unique training modules | ~150 |
| Duplicate modules | 30+ |
| Categories proposed | 7 main, 25+ subcategories |
| Skills defined | 95 |
| Target skill rules | 17 |

### Major Issues Identified

1. **Duplicates:** 22 unique modules have 30+ duplicate copies
2. **Missing content:** Safety Coordinator 1.0 and 2.0; Coach K modules 2-6
3. **Fragmented content:** Art of Presenting Chapter 7 has multiple incomplete versions
4. **Unknown content:** `untitled-scorm12` and `test-scorm12` files need review
5. **No versioning:** Duplicate filenames differ only by hash codes

### Role-to-Training Alignment

| Role | Required Skills | Training Modules | Timeline |
|------|-----------------|------------------|----------|
| New Hire | 5 | 6 | 2 weeks |
| Apprentice (4 years) | 26 | 27 | 4 years |
| Journeyman | +4 | +5 | 4 months |
| Lead Journeyman | +10 | +10 | 6 months |
| Foreman | +40 | +48 | 12+ months |
| Superintendent | +6 | +18 | 12 months |

---

## Proposed Category Structure

1. **Safety & Compliance** - New hire, electrical, LOTO, fall protection, confined space, HazCom, general
2. **Safety Coordinator Certification** - 9-module certification series
3. **Field Leadership Program** - 4 sections covering skills, project anatomy, leadership, policy
4. **Lean Construction** - Fundamentals, core curriculum, applied
5. **Leadership Development** - Critical Leadership, Emotional Intelligence, Values-Driven
6. **Professional Skills** - Presentation, performance management, project management
7. **Software & Tools** - Accubid Pro, ViewPoint ERP

---

## Skill Level Progression

```
L1 (Apprentice Year 1) → L2 → L3 → L4 → L5 (Journeyman) → L6 (Lead) → L7 (Foreman) → L8 (Superintendent)
                                                    ↘ L9 (Safety Coordinator)
```

---

## Immediate Actions Required

### Priority 1: Duplicate Cleanup
- Remove 30+ duplicate SCORM packages
- Establish naming convention to prevent future duplicates
- Document master version for each course

### Priority 2: Gap Resolution
- Locate or create Safety Coordinator modules 1.0 and 2.0
- Locate or create Coach K modules 2-6
- Consolidate Art of Presenting Chapter 7 variants
- Review/remove `untitled` and `test` modules

### Priority 3: LMS Configuration
- Create category folders in LMS
- Assign modules to categories
- Configure skill definitions
- Set up target skill rules

---

## Next Steps: Phase 2

Phase 2 (SOP Alignment) will:
1. Review each SOP against established training materials
2. Compare SOPs to Job Descriptions
3. Compare SOPs to Management Directives
4. Compare SOPs to EPMP Manual and Pre-construction Process
5. Rewrite SOPs with cross-references to training, job descriptions, and directives

**Key handoff from Phase 1:**
- Skills inventory (C_SKILLS.md) maps training to competencies
- Target Skill Rules (D_TARGET_SKILL_RULES.md) maps roles to training
- Phase 2 will add SOP references to create complete documentation chain

---

## Cross-Reference Points for Phase 2

### Training → SOP Connections to Establish

| Training Category | Likely SOP Categories |
|-------------------|----------------------|
| Safety (all) | Safety SOPs, Emergency Procedures |
| Lockout/Tagout | LOTO SOPs, Electrical Safety |
| Fall Protection | Fall Protection SOPs, Scaffold Use |
| Field Leadership Section 2 | Job Planning, Documentation, Reporting |
| Lean Construction | Productivity, Waste Reduction |
| Performance Management | HR Procedures, Discipline |
| ViewPoint | Change Order Procedures, Documentation |

### Job Description Connections

| Skill Level | Job Description Reference |
|-------------|--------------------------|
| L1-L4 | Policy Manual 7.2.1 - Apprentice Electrician |
| L5 | Policy Manual 7.2.2 - Journeyman Electrician |
| L6 | Policy Manual 7.2.3 - Lead Journeyman |
| L7 | Policy Manual 7.2.4 - Foreman |
| L8 | Policy Manual 7.2.5 - Project Superintendent |
| L9 | Policy Manual 7.2.6 - Project Safety Coordinator |

---

## Files Ready for Phase 2

**Input files:**
- `C:\Users\tewing\Desktop\Claude Projects\SOPs For Review` - SOPs to revise
- `C:\Users\tewing\Desktop\Claude Projects\Job Descriptions` - Role definitions
- `C:\Users\tewing\Desktop\Claude Projects\Management Directives` - Policy documents
- `C:\Users\tewing\Desktop\Claude Projects\SOP Resources` - EPMP Manual, Pre-construction Process
- `C:\Users\tewing\Desktop\Claude Projects\Foreman Training` - Training binder (32 tabs)

**Output location:**
- `C:\Users\tewing\Desktop\Claude Projects\Revised SOPs`

---

## Appendix: Foreman Training Binder Tabs (Reference)

The Foreman Training binder contains 32 tabs that should align with both training and SOPs:

1. Tool Control
2. Preplanning & Staging
3. Kickoff/Project Turnover Meeting
4-9. (Various project management topics)
10. Job Setup/Schedule of Values
11. Estimating Take-off Procedures
12. Look Ahead
13. Supervisor's Guide to Election Campaigns
14. Daily Reports
15. Integrating Schedule and Daily Reports
16. Weekly Summary Letters
17. Creating Budgets
18. Job Close Out
19. Manpower Projections
20. Job Cost Projections
21. Substance Abuse Policy
22. Document Management
23. Additional Codes
24. Communications
25. Viewpoint - Documents
26. Grounding - Fall of Potential Testing
27. Ten Commandments of Field Supervision
28. Ethics in the Workplace
29. Evaluating the Job Plan
30. Jobsite Efficiency
31. 5 Communication Skills to Avoid Defensiveness
32. Coping with Stress
