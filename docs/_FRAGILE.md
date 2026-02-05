# Fragile Zones

## SOP-Training Cross-Reference Integrity
If you rename or delete a skill in Learn365, the SOP-Training Cross-Reference list
on GSL Academy will have stale links. Always check and update both sides.

## Learn365 Target Skill Rule Propagation
Changes take 15+ minutes. Don't test immediately after saving. Plan test windows.

## CSV Import Format for Target Skill Rules
Format: CatalogName/SkillName/SkillLevel (e.g., "GSL Academy/NFPA 70E/Certified")
- Catalog names must match EXACTLY (case-sensitive)
- Skill levels must match the Skill Level Set defined for that skill
- Duplicate catalog names will cause import failure
- Global rules: use semicolon (;) in place of criteria field

## SharePoint Permissions
SOP site and GSL Academy are separate site collections.
Cross-site links work but cross-site list lookups do not.
Use hyperlink columns, not lookup columns, for cross-site references.

## Claude API for Grading
- Max tokens: always set to 1000+ for grading responses
- Learner context must be included in EVERY API call (no memory between calls)
- JSON parsing: strip ```json fences before parsing responses
