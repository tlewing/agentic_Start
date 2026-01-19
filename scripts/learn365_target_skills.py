"""
Learn365 Target Skill Rules Management
Creates target skill rules based on D_TARGET_SKILL_RULES.md

Target Skills define which skills are required for each role and drive
automatic training assignments in the LMS.

API Endpoint: POST /services/skills/TargetSkills
"""
import requests
import base64
import json
import time

API_KEY = "ef5fd367-9a88-42b8-b3cf-c117aeb93d72"
CATALOG_ID = "b1670146-674a-4730-9e9d-d7d29ba52385"
BASE_URL = "https://api.365.systems"

# User Field IDs (required for conditions)
USER_FIELD_IDS = {
    "Job Title": "5c6065be-ef67-434b-aa90-de594d84cac6",
    "Department": "a162a140-3e57-4e2e-9749-1bb3ddea2eaa",
    "Office": "2596c9cf-8cc5-4cdc-a4a6-bfec71bd818b",
    "Company": "36e51899-1c42-4623-9f46-1433104c7a2a",
    "City": "a5031414-ab0b-4ff4-9365-0f0275bf38e4",
    "Country": "7dd89e71-470a-4932-904d-6890b7f06f82",
    "Manager": "d61a7b2b-3e12-45ce-977b-a24216db4dda",
}

# Auth header
auth_string = base64.b64encode(f":{API_KEY}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {auth_string}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# =============================================================================
# TARGET SKILL RULES DEFINITION
# Based on D_TARGET_SKILL_RULES.md
#
# Each rule has:
#   - name: Display name for the rule
#   - conditions: List of {userField, operator, value} to match users
#   - skills: List of skill names required (mapped to IDs at runtime)
#   - level: Minimum skill level required (e.g., "L1", "L5", "L7")
# =============================================================================

TARGET_SKILL_RULES = [
    # Universal Requirements
    {
        "name": "UNIV-001: New Hire Requirements",
        "description": "Core safety and policy training for all new employees",
        "isGlobal": True,  # Applies to all users
        "conditions": [],  # Global = no conditions needed
        "skills": [
            "Safety Awareness & Culture",  # SAF-001
            "Slip Trip Fall Prevention",   # SAF-024 -> mapped to existing skill
            "Harassment Prevention",       # POL-002
            "Substance Abuse Policy",      # POL-003
            "EAP Awareness",              # POL-004
        ],
        "level": "L1"
    },
    {
        "name": "UNIV-002: Nevada Employees",
        "description": "Additional requirements for Nevada-based employees",
        "isGlobal": False,
        "conditions": [
            {"userField": "Office", "operator": "contains", "value": "Nevada"},
            {"userField": "Office", "operator": "contains", "value": "Las Vegas"},
        ],
        "skills": [
            "Nevada Employee Rights",  # Not in current skill list - may need to add
        ],
        "level": "L1"
    },

    # Apprentice Rules
    {
        "name": "APP-001: First Year Apprentice",
        "description": "Foundation safety and electrical skills for Year 1 apprentices",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Apprentice"},
        ],
        "skills": [
            "Safety Awareness & Culture",
            "Arc Flash Awareness",
            "LOTO Fundamentals",
            "Fall Hazard Recognition",
            "Ladder Safety",
            "HazCom Program Fundamentals",
            "Container Label Use",
        ],
        "level": "L1"
    },
    {
        "name": "APP-002: Second Year Apprentice",
        "description": "Intermediate safety skills for Year 2 apprentices",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Apprentice"},
        ],
        "skills": [
            "Approach Boundary Management",
            "Simple LOTO Procedures",
            "Personal Fall Arrest Systems",
            "Scaffold Fundamentals",
            "SDS Use & Access",
            "Chemical Hazard Identification",
        ],
        "level": "L2"
    },
    {
        "name": "APP-003: Third Year Apprentice",
        "description": "Advanced safety procedures for Year 3 apprentices",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Apprentice"},
        ],
        "skills": [
            "Complex LOTO Procedures",
            "Return to Service",
            "Confined Space Program",
            "Energized Work Practices",
        ],
        "level": "L3"
    },
    {
        "name": "APP-004: Fourth Year Apprentice",
        "description": "Leadership and lean fundamentals for Year 4 apprentices",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Apprentice"},
        ],
        "skills": [
            "Time Management",
            "Effective Communication",
            "Lean Fundamentals",
            "Eight Wastes Recognition",
            "EQ Fundamentals",
        ],
        "level": "L4"
    },

    # Journeyman Rules
    {
        "name": "JRN-001: Journeyman Core",
        "description": "Core competencies for Journeyman Electricians",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Journeyman"},
        ],
        "skills": [
            "Tool & Equipment Management",
            "Arc Flash Risk Assessment",
            "Lean Application",
            "Continuous Improvement",
        ],
        "level": "L5"
    },

    # Lead Journeyman Rules
    {
        "name": "LEAD-001: Lead Journeyman Core",
        "description": "Leadership and supervision skills for Lead Journeyman",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Lead"},
        ],
        "skills": [
            "Field Supervision",
            "Crew Planning",
            "Jobsite Efficiency",
            "Trade Coordination",
            "Leadership Fundamentals",
            "Team Building",
            "Self-Awareness",
            "Self-Regulation",
            "Focus on Flow",
        ],
        "level": "L6"
    },

    # Foreman Rules
    {
        "name": "FOR-001: Foreman Safety Coordinator",
        "description": "Safety Coordinator certification requirements for Foremen",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Foreman"},
        ],
        "skills": [
            "Safety Inspections",
            "Incident Investigation",
            "Injury Management",
            "Regulatory Inspections",
        ],
        "level": "L7"
    },
    {
        "name": "FOR-002: Foreman Field Leadership",
        "description": "Field leadership skills for Foremen",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Foreman"},
        ],
        "skills": [
            "Foreman Role & Responsibilities",
            "Documentation & Reporting",
            "Quality Control",
            "Team Management",
            "Project Planning",
            "Manpower Projection",
            "Job Closeout",
        ],
        "level": "L7"
    },
    {
        "name": "FOR-003: Foreman Leadership",
        "description": "Leadership development for Foremen",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Foreman"},
        ],
        "skills": [
            "Extreme Ownership",
            "Accountability & Ownership",
            "Team Building",
            "Delegation & Empowerment",
            "Empathy",
            "Social Skills",
        ],
        "level": "L7"
    },
    {
        "name": "FOR-004: Foreman Lean Construction",
        "description": "Lean construction implementation for Foremen",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Foreman"},
        ],
        "skills": [
            "Pull Planning",
            "Continuous Improvement",
            "Field Team Empowerment",
            "Eliminate Waste",
        ],
        "level": "L7"
    },
    {
        "name": "FOR-005: Foreman Policy",
        "description": "Policy and compliance training for Foremen",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Foreman"},
        ],
        "skills": [
            "Performance Reviews",
            "Corrective Counseling",
            "Employee Motivation",
        ],
        "level": "L7"
    },
    {
        "name": "FOR-006: Foreman Software",
        "description": "Software proficiency for Foremen",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Foreman"},
        ],
        "skills": [
            "ViewPoint Change Orders",
        ],
        "level": "L7"
    },

    # Superintendent Rules
    {
        "name": "SUP-001: Superintendent Advanced Leadership",
        "description": "Advanced leadership for Superintendents",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Superintendent"},
            {"userField": "JobTitle", "operator": "contains", "value": "General Foreman"},
        ],
        "skills": [
            "Values-Driven Leadership",
            "EQ Leadership",
            "Career Development",
            "Strategic Thinking",
        ],
        "level": "L8"
    },

    # Safety Coordinator Rules
    {
        "name": "PSC-001: Project Safety Coordinator",
        "description": "Complete safety specialist requirements",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Safety Coordinator"},
            {"userField": "JobTitle", "operator": "contains", "value": "Safety"},
        ],
        "skills": [
            "Safety Inspections",
            "Incident Investigation",
            "Injury Management",
            "Regulatory Inspections",
            "Pre-Task Safety Planning",
            "Hazard Recognition",
            "Emergency Response",
        ],
        "level": "L9"
    },

    # Estimator Rules
    {
        "name": "EST-001: Estimator Software",
        "description": "Software requirements for Estimators",
        "isGlobal": False,
        "conditions": [
            {"userField": "JobTitle", "operator": "contains", "value": "Estimat"},
        ],
        "skills": [
            "Accubid Fundamentals",
        ],
        "level": "L5"
    },
]


# =============================================================================
# API FUNCTIONS
# =============================================================================

def get_existing_skills():
    """Get all existing skills with pagination and build name->ID map"""
    GSL_CAREER_PROGRESSION_ID = "dc10f982-86fa-4a5b-8869-6d5e4dde769b"
    all_skills = []
    skip = 0
    page_size = 100

    while True:
        url = f"{BASE_URL}/services/skills/Skills?$skip={skip}&$top={page_size}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print(f"Error getting skills page: {r.status_code}")
            break

        page = r.json()
        if not page:
            break

        all_skills.extend(page)

        if len(page) < page_size:
            break
        skip += page_size

    # Build lookup map (case-insensitive)
    # Prefer skills using GSL Career Progression scale set when there are duplicates
    skills_map = {}
    for s in all_skills:
        title_lower = s.get('title', '').lower()
        existing = skills_map.get(title_lower)

        if existing is None:
            # First skill with this title
            skills_map[title_lower] = s
        elif s.get('scaleSetId') == GSL_CAREER_PROGRESSION_ID:
            # This skill uses GSL Career Progression - prefer it
            skills_map[title_lower] = s

    return skills_map


def get_existing_scale_sets():
    """Get existing skill scale sets"""
    url = f"{BASE_URL}/services/skills/SkillScaleSets"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    return []


def get_scale_set_details(scale_set_id):
    """Get full details of a scale set including levels"""
    # Use $expand to include levels in response
    url = f"{BASE_URL}/services/skills/SkillScaleSets/{scale_set_id}?$expand=levels"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    return None


def get_existing_target_skills():
    """Get existing target skills"""
    url = f"{BASE_URL}/services/skills/TargetSkills"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    print(f"Error getting target skills: {r.status_code}")
    return []


def delete_target_skill(target_id):
    """Delete a target skill"""
    url = f"{BASE_URL}/services/skills/TargetSkills/{target_id}"
    r = requests.delete(url, headers=HEADERS)
    return r.status_code in [200, 204]


def create_target_skill(target_data):
    """Create a new target skill"""
    url = f"{BASE_URL}/services/skills/TargetSkills"
    r = requests.post(url, headers=HEADERS, json=target_data)
    if r.status_code in [200, 201]:
        return r.json()
    else:
        print(f"  Error creating target skill: {r.status_code}")
        print(f"  Response: {r.text[:300]}")
        return None


def build_level_map(scale_sets):
    """Build a map from level value (L1, L2, etc) to level ID"""
    level_map = {}

    # Use hardcoded GSL Career Progression ID (API pagination makes searching unreliable)
    GSL_CAREER_PROGRESSION_ID = "dc10f982-86fa-4a5b-8869-6d5e4dde769b"

    # Get full details with levels
    details = get_scale_set_details(GSL_CAREER_PROGRESSION_ID)
    if not details or 'levels' not in details:
        print(f"WARNING: Could not get levels for GSL Career Progression")
        # Fallback to searching
        for ss in scale_sets:
            if ss.get('title') == 'GSL Career Progression':
                details = get_scale_set_details(ss['id'])
                break

    if not details or 'levels' not in details:
        print("WARNING: No skill scale set found!")
        return level_map

    for level in details['levels']:
        value = level.get('value', 0)
        level_key = f"L{value}"
        level_map[level_key] = {
            'id': level.get('id'),
            'title': level.get('title'),
            'value': value
        }

    return level_map


def main():
    print("=" * 70)
    print("Learn365 Target Skill Rules Management")
    print("=" * 70)
    print()

    # Step 1: Get existing skills
    print("Step 1: Loading existing skills...")
    skills_map = get_existing_skills()
    print(f"  Found {len(skills_map)} skills")
    print()

    # Step 2: Get skill level sets and build level map
    print("Step 2: Loading skill level sets...")
    scale_sets = get_existing_scale_sets()
    level_map = build_level_map(scale_sets)
    print(f"  Found {len(level_map)} levels")
    for k, v in sorted(level_map.items(), key=lambda x: x[1]['value']):
        print(f"    {k}: {v['title']} (ID: {v['id'][:8]}...)")
    print()

    if not level_map:
        print("ERROR: No skill levels found. Run learn365_skill_level_sets.py first!")
        return

    # Step 3: Check existing target skills
    print("Step 3: Checking existing target skills...")
    existing_targets = get_existing_target_skills()
    print(f"  Found {len(existing_targets)} existing target skill(s)")

    if existing_targets:
        print()
        print("  Existing target skills:")
        for t in existing_targets:
            print(f"    - {t.get('name', 'Unknown')} (ID: {t.get('id', 'N/A')})")

        print()
        print("  Options:")
        print("    1. Delete all existing and create fresh")
        print("    2. Add new rules (skip existing names)")
        print("    3. Cancel")
        print()

        choice = input("  Enter choice (1/2/3): ").strip()

        if choice == "1":
            print()
            print("  Deleting existing target skills...")
            deleted = 0
            for t in existing_targets:
                if delete_target_skill(t['id']):
                    deleted += 1
            print(f"  Deleted {deleted} target skills")
        elif choice == "3":
            print("  Cancelled")
            return
        # choice 2 = continue without deleting

    print()

    # Step 4: Create target skills
    print("Step 4: Creating target skill rules...")
    print()

    created = 0
    skipped = 0
    errors = 0

    existing_names = {t.get('name', '').lower() for t in existing_targets}

    for rule in TARGET_SKILL_RULES:
        rule_name = rule['name']

        # Skip if already exists (and we didn't delete)
        if rule_name.lower() in existing_names:
            print(f"  SKIP: {rule_name} (already exists)")
            skipped += 1
            continue

        print(f"  Creating: {rule_name}")

        # Build the rules array (skill + level requirements)
        rules_array = []
        missing_skills = []

        for skill_name in rule.get('skills', []):
            skill_key = skill_name.lower()
            skill_data = skills_map.get(skill_key)

            if not skill_data:
                missing_skills.append(skill_name)
                continue

            level_key = rule.get('level', 'L1')
            level_data = level_map.get(level_key)

            if not level_data:
                print(f"    WARNING: Level {level_key} not found, using L1")
                level_data = level_map.get('L1', {})

            if skill_data.get('id') and level_data.get('id'):
                rules_array.append({
                    "skillId": skill_data['id'],
                    "skillLevelId": level_data['id']
                })

        if missing_skills:
            print(f"    WARNING: {len(missing_skills)} skills not found: {', '.join(missing_skills[:3])}{'...' if len(missing_skills) > 3 else ''}")

        if not rules_array:
            print(f"    ERROR: No valid skills found, skipping rule")
            errors += 1
            continue

        # Build conditions array
        conditions_array = []
        for cond in rule.get('conditions', []):
            # Map field names and get userFieldId
            field_name = cond.get('userField', 'Job Title')
            # Handle legacy "JobTitle" -> "Job Title"
            if field_name == 'JobTitle':
                field_name = 'Job Title'

            field_id = USER_FIELD_IDS.get(field_name)
            if not field_id:
                print(f"    WARNING: Unknown user field '{field_name}', skipping condition")
                continue

            conditions_array.append({
                "userField": field_name,
                "userFieldId": field_id,
                "operator": cond.get('operator', 'Contains'),
                "value": cond.get('value', '')
            })

        # Build target skill payload
        target_payload = {
            "name": rule_name,
            "isGlobal": rule.get('isGlobal', False),
            "conditions": conditions_array,
            "rules": rules_array
        }

        # Create the target skill
        result = create_target_skill(target_payload)

        if result:
            print(f"    Created with {len(rules_array)} skill requirements")
            created += 1
        else:
            print(f"    FAILED")
            errors += 1

        # Small delay to avoid rate limiting
        time.sleep(0.2)

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total rules defined: {len(TARGET_SKILL_RULES)}")
    print(f"  Created: {created}")
    print(f"  Skipped (existing): {skipped}")
    print(f"  Errors: {errors}")

    # Final verification
    print()
    print("Final verification:")
    final = get_existing_target_skills()
    print(f"  Total target skills in Learn365: {len(final)}")


if __name__ == "__main__":
    main()
