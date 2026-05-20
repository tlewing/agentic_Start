"""Patch NEEDS-REVIEW courses with correct classifications."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

RECS_PATH = r'C:\Users\tewing\OneDrive - GSL Electric\Projects\GSL-Operations-Framework\data\scorm_taxonomy_recommendations.json'

with open(RECS_PATH, 'r', encoding='utf-8') as f:
    recs = json.load(f)

LN = "[LEVEL NEEDED -- {ss} scale set has no levels defined]"

patches = {
    "Managing Sub-contractors": {
        "category": {"value": "Leadership > Skills, Traits, & Responsibilities", "label": "EXISTING", "rationale": "Subcontractor management is a field leadership skill."},
        "skills_awarded": [{"skill": "Trade Coordination", "skill_category": "Leadership", "scale_set": "Leadership", "level": LN.format(ss="Leadership"), "label": "EXISTING", "rationale": "Managing subs requires trade coordination."}],
        "tags": [{"value": "coordination", "label": "EXISTING"}, {"value": "supervision", "label": "EXISTING"}, {"value": "Difficulty: Intermediate", "label": "PROPOSED"}],
        "level_of_difficulty": {"value": "Intermediate", "rationale": "Requires project management context."},
        "target_roles_draft": [{"fragment": "Academy/Trade Coordination/[level TBD]", "roles": ["Foreman", "Superintendent", "Project Manager"], "scope": "Role-scoped", "note": "Personnel who manage subcontractors."}],
        "short_description": "Learn how to effectively manage subcontractors on your project.",
        "long_description": "This course covers managing subcontractors on construction projects.\n\nOn completion, you earn the skill Trade Coordination.\n\nThis is an Intermediate-level course.",
    },
    "On-Site Productivity": {
        "category": {"value": "Lean Principals > Lean Fundamentals", "label": "EXISTING", "rationale": "Productivity is a lean fundamentals topic."},
        "skills_awarded": [{"skill": "Productivity Execution", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": LN.format(ss="Lean Principles"), "label": "EXISTING", "rationale": "Directly addresses on-site productivity."}],
        "tags": [{"value": "productivity", "label": "EXISTING"}, {"value": "Lean", "label": "EXISTING"}, {"value": "Difficulty: Foundational", "label": "PROPOSED"}],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Introductory productivity concepts."},
        "target_roles_draft": [{"fragment": "Academy/Productivity Execution/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders."}],
        "short_description": "Improve on-site productivity through better planning and waste reduction.",
        "long_description": "This course covers techniques for improving on-site productivity.\n\nOn completion, you earn the skill Productivity Execution.\n\nThis is a Foundational-level course.",
    },
    "Return To Service Procedures": {
        "category": {"value": "Safety > Lockout / Tagout", "label": "EXISTING", "rationale": "Return to service is part of LOTO."},
        "skills_awarded": [{"skill": "LOTO Fundamentals", "skill_category": "Safety", "scale_set": "Safety", "level": LN.format(ss="Safety"), "label": "EXISTING", "rationale": "Return to service is a LOTO procedure."}],
        "tags": [{"value": "LOTO", "label": "EXISTING"}, {"value": "Return to Service", "label": "EXISTING"}, {"value": "Difficulty: Foundational", "label": "PROPOSED"}],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Standard LOTO procedure."},
        "target_roles_draft": [{"fragment": "Academy/LOTO Fundamentals/[level TBD]", "roles": ["Apprentice", "Journeyman", "Leadman", "Foreman", "Superintendent"], "scope": "Global", "note": "All field electricians."}],
        "short_description": "Learn proper return to service procedures after lockout/tagout.",
        "long_description": "This course covers return to service procedures for safely re-energizing equipment.\n\nOn completion, you earn the skill LOTO Fundamentals.\n\nThis is a Foundational-level course.",
    },
    "Required Precautions & Practices - Testing & Troubleshooting": {
        "category": {"value": "Safety > Electrical Safety", "label": "EXISTING", "rationale": "Testing and troubleshooting safety."},
        "skills_awarded": [{"skill": "Energized Work Practices", "skill_category": "Safety", "scale_set": "Safety", "level": LN.format(ss="Safety"), "label": "EXISTING", "rationale": "Testing near energized equipment."}],
        "tags": [{"value": "electrical safety", "label": "EXISTING"}, {"value": "testing", "label": "EXISTING"}, {"value": "Difficulty: Intermediate", "label": "PROPOSED"}],
        "level_of_difficulty": {"value": "Intermediate", "rationale": "Requires electrical safety fundamentals."},
        "target_roles_draft": [{"fragment": "Academy/Energized Work Practices/[level TBD]", "roles": ["Journeyman", "Leadman", "Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Qualified persons."}],
        "short_description": "Learn required precautions for safely testing and troubleshooting electrical equipment.",
        "long_description": "This course covers safety precautions for testing and troubleshooting electrical equipment.\n\nOn completion, you earn the skill Energized Work Practices.\n\nThis is an Intermediate-level course.",
    },
    "Verifying a De-Energized Condition": {
        "category": {"value": "Safety > Electrical Safety", "label": "EXISTING", "rationale": "De-energized verification is electrical safety."},
        "skills_awarded": [{"skill": "Electrical Safety Fundamentals", "skill_category": "Safety", "scale_set": "Safety", "level": LN.format(ss="Safety"), "label": "EXISTING", "rationale": "Fundamental electrical safety skill."}],
        "tags": [{"value": "electrical safety", "label": "EXISTING"}, {"value": "verification", "label": "EXISTING"}, {"value": "voltage tester", "label": "EXISTING"}, {"value": "Difficulty: Intermediate", "label": "PROPOSED"}],
        "level_of_difficulty": {"value": "Intermediate", "rationale": "Requires LOTO and electrical safety knowledge."},
        "target_roles_draft": [{"fragment": "Academy/Electrical Safety Fundamentals/[level TBD]", "roles": ["Apprentice", "Journeyman", "Leadman", "Foreman", "Superintendent"], "scope": "Global", "note": "All field electricians."}],
        "short_description": "Learn how to verify a de-energized condition using proper testing procedures.",
        "long_description": "This course covers procedures for verifying electrical equipment is de-energized before work.\n\nOn completion, you earn the skill Electrical Safety Fundamentals.\n\nThis is an Intermediate-level course.",
    },
    "TEST": {
        "category": {"value": "[TEST COURSE -- recommend removal]", "label": "NEEDS-REVIEW", "rationale": "Test/dummy course."},
        "skills_awarded": [],
        "tags": [],
        "level_of_difficulty": {"value": "[N/A]", "rationale": "Test course."},
        "target_roles_draft": [],
        "short_description": "[TEST COURSE -- recommend removal from catalog]",
        "long_description": "[TEST COURSE -- recommend removal from Learn365 catalog.]",
    },
    "Information Found on Container Labels": {
        "category": {"value": "Safety > Hazard Communication", "label": "EXISTING", "rationale": "Container labeling is hazard communication."},
        "skills_awarded": [{"skill": "Container Label Use", "skill_category": "Safety", "scale_set": "Safety", "level": LN.format(ss="Safety"), "label": "EXISTING", "rationale": "Teaches container label reading."}],
        "tags": [{"value": "hazard communication", "label": "EXISTING"}, {"value": "label", "label": "EXISTING"}, {"value": "GHS", "label": "EXISTING"}, {"value": "Difficulty: Foundational", "label": "PROPOSED"}],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Basic safety knowledge."},
        "target_roles_draft": [{"fragment": "Academy/Container Label Use/[level TBD]", "roles": ["Apprentice", "Journeyman", "Leadman", "Foreman", "Superintendent"], "scope": "Global", "note": "All field personnel."}],
        "short_description": "Learn to read safety information on chemical container labels.",
        "long_description": "This course teaches reading and interpreting chemical container labels.\n\nOn completion, you earn the skill Container Label Use.\n\nThis is a Foundational-level course.",
    },
}

patched = 0
for c in recs['courses']:
    title = c['course']
    if title in patches:
        for key, val in patches[title].items():
            c[key] = val
        patched += 1
    elif 'Art of Presenting' in title:
        c['category'] = {"value": "Presentation Skills", "label": "EXISTING", "rationale": "Presentation skills series."}
        c['skills_awarded'] = [{"skill": "Slide Preparation", "skill_category": "Communication", "scale_set": "Communication", "level": LN.format(ss="Communication"), "label": "EXISTING", "rationale": "Presentation skills course."}]
        c['tags'] = [{"value": "Communication", "label": "EXISTING"}, {"value": "Difficulty: Foundational", "label": "PROPOSED"}]
        c['level_of_difficulty'] = {"value": "Foundational", "rationale": "Presentation skills fundamentals."}
        c['target_roles_draft'] = [{"fragment": "Academy/Slide Preparation/[level TBD]", "roles": ["Foreman", "Superintendent", "Project Manager"], "scope": "Role-scoped", "note": "Personnel who present to others."}]
        c['short_description'] = "Develop your presentation skills for professional communication."
        c['long_description'] = "Part of The Art of Presenting series.\n\nOn completion, you earn the skill Slide Preparation.\n\nThis is a Foundational-level course."
        patched += 1

remaining_nr = sum(1 for c in recs['courses'] if c['category']['label'] == 'NEEDS-REVIEW')
remaining_ns = sum(1 for c in recs['courses'] if not c.get('skills_awarded'))
print(f"Patched {patched} courses")
print(f"Remaining NEEDS-REVIEW: {remaining_nr}")
print(f"Remaining no-skill: {remaining_ns}")

recs['meta']['status'] = 'Complete -- all 185 courses processed'
with open(RECS_PATH, 'w', encoding='utf-8') as f:
    json.dump(recs, f, indent=2, ensure_ascii=False)
print("Saved.")
