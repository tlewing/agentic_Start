# Phase 1 Prompt: GSL Academy Training Structure Cleanup

Copy and use this prompt to begin Phase 1 work.

---

## The Prompt

```
# GSL Operations Framework — Phase 1: Training Foundation

## Big Picture

I'm building a synchronized operational documentation system for GSL Electric that connects four pillars:

1. **GSL Academy (LMS/Training)** — SCORM courses in SharePoint LMS
2. **SOPs** — Standard Operating Procedures
3. **Job Descriptions** — Role definitions
4. **Management Directives** — Policy documents

The goal: Any employee can trace from "what I'm trained on" → "what I'm supposed to do" → "what my job requires" → "what policy mandates."

We're starting with **Phase 1: Training Foundation** — cleaning up and organizing the LMS before we sync it with SOPs.

---

## Your Task

Review the SCORM training content, including video scripts where available, then:

### A. Clean Up Categories
- Review all training modules and their current category assignments
- Identify inconsistencies, duplicates, or misplaced items
- Propose a clean, logical category structure
- Map each module to its proper category

### B. Clean Up and Organize Skill Level Sets
- Review how skill levels are currently defined
- Propose a consistent skill level framework (e.g., Apprentice → Journeyman → Foreman → Superintendent)
- Ensure skill levels align with job progression at GSL

### C. Clean Up and Organize Skills
- Inventory all skills currently in the system
- Remove duplicates and consolidate similar skills
- Organize skills into logical groupings
- Ensure skill names are consistent and descriptive

### D. Create Target Skill Rules
- Define which skills are required for which roles
- Create a complete matrix of: Role → Required Skills → Training Modules
- Identify gaps where training exists but isn't linked to skills
- Identify gaps where skills exist but have no supporting training

---

## Resources

**SCORM Files (local copy):**
`C:\Users\tewing\Desktop\Claude Projects\SCORM Files`

**LMS Catalog (if needed):**
`https://us-lms.365.systems/tenant/6bfd84e47f3f4493a606c23022e1e048/env/567874efa5e24394939b91bbc5999041/catalog/6dec10c741f04bdc830575171ac3de04/Scorm/Packages`

**Reference Materials:**
- Foreman Training: `C:\Users\tewing\Desktop\Claude Projects\Foreman Training`
- Job Descriptions: `C:\Users\tewing\Desktop\Claude Projects\Job Descriptions`

---

## Output Format

For each deliverable, create a structured document:

### Categories (A)
| Category | Subcategory | Modules |
|----------|-------------|---------|
| Safety | Arc Flash | [list] |
| Safety | Fall Protection | [list] |
| Leadership | Field Leadership | [list] |
| ... | ... | ... |

### Skill Level Sets (B)
| Level | Description | Typical Role | Prerequisites |
|-------|-------------|--------------|---------------|
| Level 1 | Entry | Apprentice | None |
| Level 2 | ... | ... | Level 1 |

### Skills (C)
| Skill ID | Skill Name | Category | Level | Training Modules |
|----------|------------|----------|-------|------------------|
| ... | ... | ... | ... | ... |

### Target Skill Rules (D)
| Role | Required Skills | Training Path |
|------|-----------------|---------------|
| Apprentice Electrician | [skills] | [modules in order] |
| Journeyman | [skills] | [modules] |
| Foreman | [skills] | [modules] |

---

## Important Notes

- This is Phase 1. We'll later connect these training modules to SOPs (Phase 2).
- Focus on organization and structure first. Don't worry about SOP linkage yet.
- When reviewing SCORM content, note any video scripts or learning objectives that will help with SOP alignment later.
- Flag any training that appears outdated or needs revision.

---

## When Complete

Save deliverables to:
`C:\Users\tewing\Documents\Projects\GSL-Operations-Framework\deliverables\phase1\`

Then we'll proceed to Phase 2 (SOP Alignment).
```

---

## Notes

This prompt gives Claude:
- The big picture context (four pillars)
- Specific tasks with clear deliverables
- File locations for all resources
- Output format expectations
- Scope boundaries (Phase 1 only)
