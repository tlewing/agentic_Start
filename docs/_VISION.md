# Vision

## One-Liner

Synchronized operational documentation system connecting training, SOPs, job descriptions, and management directives.

---

## Problem

GSL's operational documentation exists in silos:
- **Training (GSL Academy)** — SCORM content in SharePoint LMS with inconsistent categories, skill levels, and skills
- **SOPs** — Standard Operating Procedures not aligned with training materials or job roles
- **Job Descriptions** — May not reflect actual SOP responsibilities
- **Management Directives** — Policy documents disconnected from day-to-day SOPs

**Result:** Employees can't easily connect "what they're trained on" → "what they're supposed to do" → "what their job requires" → "what policy mandates."

---

## Target Users

| User Type | Description | Primary Need |
|-----------|-------------|--------------|
| Operations Staff | Field employees, foremen | Clear connection between training and job duties |
| Managers | Supervisors, project managers | Know what training applies to which roles/SOPs |
| Training Admin | LMS administrators | Organized, logical training structure |
| HR/Compliance | Policy owners | Aligned documentation across all systems |

---

## Solution

Create a unified, cross-referenced documentation system where:
1. **Training modules** link to the SOPs they support
2. **SOPs** reference applicable job descriptions, management directives, and training
3. **Job Descriptions** reflect actual SOP responsibilities
4. **Management Directives** connect to implementing SOPs

---

## The Four Pillars

### 1. GSL Academy (LMS/Training)
- **Platform:** SharePoint LMS at 365.systems
- **Content:** SCORM packages with video scripts
- **Location:** `C:\Users\tewing\Desktop\Claude Projects\SCORM Files`
- **Needs:** Category cleanup, skill level organization, skill organization, target skill rules

### 2. SOPs (Standard Operating Procedures)
- **Source:** `C:\Users\tewing\Desktop\Claude Projects\SOPs For Review`
- **Output:** `C:\Users\tewing\Desktop\Claude Projects\Revised SOPs`
- **References:** Foreman Training, Job Descriptions, Management Directives, EPMP Manual

### 3. Job Descriptions
- **Location:** `C:\Users\tewing\Desktop\Claude Projects\Job Descriptions`
- **Needs:** Sync with SOPs and Management Directives

### 4. Management Directives
- **Location:** `C:\Users\tewing\Desktop\Claude Projects\Management Directives`
- **Needs:** Sync with SOPs and Job Descriptions

---

## Workflow Sequence

```
Phase 1: Training Foundation
├── Review SCORM content and video scripts
├── Clean up categories
├── Organize skill level sets
├── Organize skills
└── Create target skill rules

Phase 2: SOP Alignment
├── Review SOPs against Foreman Training materials
├── Compare SOPs to Job Descriptions
├── Compare SOPs to Management Directives
├── Compare SOPs to EPMP Manual & Pre-construction Process
├── Rewrite SOPs with references
└── Link SOPs to applicable training modules

Phase 3: Job Description Sync
└── Revise Job Descriptions to align with SOPs and Directives

Phase 4: Management Directive Sync
└── Revise Management Directives to align with SOPs and Job Descriptions

Phase 5: Cross-Reference Completion
├── Training → SOPs (links)
├── SOPs → Training, Job Descriptions, Directives (references)
├── Job Descriptions → SOPs, Directives
└── Directives → SOPs, Job Descriptions
```

---

## Key Resources

| Resource | Path |
|----------|------|
| SCORM Files | `C:\Users\tewing\Desktop\Claude Projects\SCORM Files` |
| SOPs For Review | `C:\Users\tewing\Desktop\Claude Projects\SOPs For Review` |
| Revised SOPs (output) | `C:\Users\tewing\Desktop\Claude Projects\Revised SOPs` |
| Job Descriptions | `C:\Users\tewing\Desktop\Claude Projects\Job Descriptions` |
| Management Directives | `C:\Users\tewing\Desktop\Claude Projects\Management Directives` |
| Foreman Training | `C:\Users\tewing\Desktop\Claude Projects\Foreman Training` |
| SOP Resources | `C:\Users\tewing\Desktop\Claude Projects\SOP Resources` |
| LMS Catalog | `https://us-lms.365.systems/tenant/.../catalog/.../Scorm/Packages` |

---

## Success Looks Like

| Timeframe | Success Metric |
|-----------|----------------|
| Phase 1 Complete | Training has clean categories, organized skills, documented rules |
| Phase 2 Complete | All SOPs rewritten with cross-references to training, jobs, directives |
| Phase 3-4 Complete | Job Descriptions and Directives aligned with SOPs |
| Full Sync | Any document links to all related documents across all four pillars |

---

## Open Questions

1. How should skills map to job roles? (One skill = multiple roles? Role = skill set?)
2. What's the governance model for keeping these in sync going forward?
3. Are there SOPs that need training content that doesn't exist yet?
