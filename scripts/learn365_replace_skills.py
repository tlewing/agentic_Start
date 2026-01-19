"""
Learn365 Skills Framework Replacement
Delete all existing skills/categories and create clean framework

IMPORTANT: This script requires a Skill Level Set to exist first.
Run learn365_skill_level_sets.py before this script.

API Requirements:
- SkillDto requires: title (string), scaleSetId (uuid)
- SkillCategoryDto requires: name (string)
"""
import requests
import base64
import json
import time

API_KEY = "ef5fd367-9a88-42b8-b3cf-c117aeb93d72"
CATALOG_ID = "b1670146-674a-4730-9e9d-d7d29ba52385"
BASE_URL = "https://api.365.systems"

# Auth header
auth_string = base64.b64encode(f":{API_KEY}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {auth_string}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# New clean framework (10 Skill Categories with skills)
SKILL_FRAMEWORK = {
    "Safety": [
        "Safety Awareness & Culture",
        "Accident Prevention",
        "Hazard Recognition",
        "Pre-Task Safety Planning",
        "Safety Inspections",
        "Incident Investigation",
        "Injury Management",
        "First Aid/CPR/AED",
        "Emergency Response",
        "NFPA 70E Fundamentals",
        "Approach Boundary Management",
        "Arc Flash Awareness",
        "Arc Flash Risk Assessment",
        "Arc Flash PPE Selection",
        "Energized Work Practices",
        "Energized Work Permitting",
        "Electrical Hazard Recognition",
        "Electrically Safe Work Condition",
        "LOTO Fundamentals",
        "Simple LOTO Procedures",
        "Complex LOTO Procedures",
        "Abnormal Lock Removal",
        "De-Energization Verification",
        "Return to Service",
        "Fall Hazard Recognition",
        "Personal Fall Arrest Systems",
        "Ladder Safety",
        "Scaffold Fundamentals",
        "Scaffold Access & Egress",
        "Scaffold Assembly & Inspection",
        "Fall Protection on Scaffolds",
        "HazCom Program Fundamentals",
        "GHS System Understanding",
        "Container Label Use",
        "SDS Use & Access",
        "Chemical Hazard Identification",
        "Pictogram Interpretation",
        "Confined Space Program",
        "Atmospheric Hazard Detection",
        "Entry Permit Management",
    ],
    "Lean Construction": [
        "Lean Fundamentals",
        "Lean History",
        "Lean Application",
        "Eight Wastes Recognition",
        "Eliminate Waste",
        "Focus on Flow",
        "Generate Value",
        "Optimize the Whole",
        "Continuous Improvement",
        "Respect for People",
        "Pull Planning",
        "Field Team Empowerment",
    ],
    "Leadership & Field Management": [
        "Foreman Role & Responsibilities",
        "Field Supervision",
        "Crew Planning",
        "Trade Coordination",
        "Jobsite Efficiency",
        "Quality Control",
        "Tool & Equipment Management",
        "Manpower Projection",
        "Job Closeout",
        "Field Empowerment",
        "Leadership Fundamentals",
        "Values-Driven Leadership",
        "Accountability & Ownership",
        "Team Building",
        "Team Management",
        "Delegation & Empowerment",
        "Employee Motivation",
        "Team Morale",
        "Organizational Structuring",
        "Extreme Ownership",
    ],
    "Communication & Coaching": [
        "Effective Communication",
        "Building Relationships",
        "Conducting One-on-Ones",
        "Mentoring & Coaching",
        "Conflict Resolution",
        "Handling Resistance",
        "Setting Expectations",
        "Using the GROW Model",
    ],
    "Emotional Intelligence": [
        "EQ Fundamentals",
        "Self-Awareness",
        "Self-Regulation",
        "Empathy",
        "Social Skills",
        "EQ Leadership",
        "Trust Building",
    ],
    "Performance Management": [
        "Performance Management Fundamentals",
        "Conducting Evaluations",
        "Performance Reviews",
        "Corrective Counseling",
        "Escalation & Termination",
        "Career Development",
        "Identifying Strengths",
    ],
    "Construction Software": [
        "Accubid Fundamentals",
        "Accubid Data Export",
        "ViewPoint Change Orders",
        "ProCore Fundamentals",
        "ProCore Job Setup",
        "ProCore Job Plans",
        "Job Plan Fundamentals",
        "Job Plan Setup",
        "Job Plan Maintenance",
        "Excel Skills",
        "Vista",
        "Teams",
        "Outlook",
        "Word",
    ],
    "Project Planning & Productivity": [
        "Project Planning",
        "Job Plan Analysis",
        "Scheduling Techniques",
        "Productivity Analysis",
        "Productivity Improvement",
        "Time Management",
        "Construction Project Lifecycle",
        "Process Improvement",
    ],
    "Documentation & Compliance": [
        "Documentation Practices",
        "Documentation & Reporting",
        "Regulatory Inspections",
        "Compliance Management",
    ],
    "Professional Development": [
        "Presentation Skills",
        "Strategic Thinking",
        "Industry Leadership",
    ],
}


def get_all_skills():
    r = requests.get(f"{BASE_URL}/services/skills/Skills", headers=HEADERS)
    return r.json() if r.status_code == 200 else []


def get_all_categories():
    r = requests.get(f"{BASE_URL}/services/skills/SkillCategories", headers=HEADERS)
    return r.json() if r.status_code == 200 else []


def get_all_scale_sets():
    r = requests.get(f"{BASE_URL}/services/skills/SkillScaleSets", headers=HEADERS)
    return r.json() if r.status_code == 200 else []


def get_scale_set_details(scale_set_id):
    """Get full details of a scale set"""
    url = f"{BASE_URL}/services/skills/SkillScaleSets/{scale_set_id}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    return None


def delete_skill(skill_id):
    url = f"{BASE_URL}/services/skills/catalog/{CATALOG_ID}/Skills/{skill_id}"
    r = requests.delete(url, headers=HEADERS)
    return r.status_code in [200, 204]


def delete_category(cat_id):
    url = f"{BASE_URL}/services/skills/catalog/{CATALOG_ID}/SkillCategories/{cat_id}"
    r = requests.delete(url, headers=HEADERS)
    return r.status_code in [200, 204]


def create_category(name):
    url = f"{BASE_URL}/services/skills/catalog/{CATALOG_ID}/SkillCategories"
    data = {"name": name}
    r = requests.post(url, headers=HEADERS, json=data)
    if r.status_code in [200, 201]:
        return r.json()
    else:
        print(f"    Error creating category: {r.status_code} - {r.text[:200]}")
        return None


def create_skill(title, scale_set_id, category_id=None):
    """
    Create a skill with required fields.

    SkillDto requires:
    - title: string (required)
    - scaleSetId: uuid (required)
    """
    url = f"{BASE_URL}/services/skills/catalog/{CATALOG_ID}/Skills"

    # Try minimal payload first - just title and scaleSetId
    data = {
        "title": title,
        "scaleSetId": scale_set_id
    }

    r = requests.post(url, headers=HEADERS, json=data)
    if r.status_code in [200, 201]:
        return r.json()
    elif "already exists" in r.text:
        # Skill exists - this is OK, return success indicator
        return {"title": title, "exists": True}
    else:
        print(f"    Error creating skill '{title}': {r.status_code} - {r.text[:300]}")
        return None


def find_or_create_scale_set():
    """Find GSL Career Progression scale set"""
    # Hardcoded ID from creation - API pagination makes searching unreliable
    GSL_CAREER_PROGRESSION_ID = "dc10f982-86fa-4a5b-8869-6d5e4dde769b"

    # Verify it exists
    details = get_scale_set_details(GSL_CAREER_PROGRESSION_ID)
    if details:
        print(f"  Found: {details.get('title')} (ID: {GSL_CAREER_PROGRESSION_ID})")
        return GSL_CAREER_PROGRESSION_ID

    # Fallback to searching
    scale_sets = get_all_scale_sets()
    for ss in scale_sets:
        if ss.get('title') == 'GSL Career Progression':
            print(f"  Found via search: {ss.get('title')} (ID: {ss.get('id')})")
            return ss.get('id')

    print("  ERROR: GSL Career Progression scale set not found!")
    print("  Please run learn365_skill_level_sets.py first")
    return None


def main():
    print("=" * 60)
    print("Learn365 Skills Framework Replacement")
    print("=" * 60)
    print()

    # Step 0: Find or verify skill level set exists
    print("Step 0: Finding Skill Level Set...")
    scale_set_id = find_or_create_scale_set()

    if not scale_set_id:
        print()
        print("ABORTED: Cannot create skills without a Skill Level Set")
        print("Run: python learn365_skill_level_sets.py")
        return
    print()

    # Step 1: Delete all existing skills (optional, may fail if in use)
    print("Step 1: Attempting to delete existing skills...")
    skills = get_all_skills()
    print(f"  Found {len(skills)} existing skills")

    if skills:
        deleted = 0
        failed = 0
        for skill in skills:
            if delete_skill(skill['id']):
                deleted += 1
            else:
                failed += 1
        print(f"  Deleted: {deleted}, Failed: {failed} (may be in use)")
    print()

    # Step 2: Delete all existing categories (optional, may fail if in use)
    print("Step 2: Attempting to delete existing categories...")
    categories = get_all_categories()
    print(f"  Found {len(categories)} existing categories")

    if categories:
        deleted = 0
        failed = 0
        for cat in categories:
            if delete_category(cat['id']):
                deleted += 1
            else:
                failed += 1
        print(f"  Deleted: {deleted}, Failed: {failed} (may be in use)")
    print()

    time.sleep(1)

    # Step 3: Create new categories
    print("Step 3: Creating new skill categories...")
    category_map = {}
    for cat_name in SKILL_FRAMEWORK.keys():
        result = create_category(cat_name)
        if result:
            category_map[cat_name] = result.get('id')
            print(f"  Created: {cat_name} (ID: {result.get('id', 'N/A')[:8]}...)")
        else:
            print(f"  FAILED: {cat_name}")
    print(f"  Total: {len(category_map)} categories created")
    print()

    # Step 4: Create skills under each category
    print("Step 4: Creating skills...")
    total_skills = sum(len(skills) for skills in SKILL_FRAMEWORK.values())
    created = 0
    failed = 0

    for cat_name, skills in SKILL_FRAMEWORK.items():
        cat_id = category_map.get(cat_name)
        if not cat_id:
            print(f"  Skipping {cat_name} - no category ID")
            failed += len(skills)
            continue

        print(f"  {cat_name} ({len(skills)} skills)...")
        for skill_title in skills:
            result = create_skill(skill_title, scale_set_id, cat_id)
            if result:
                created += 1
            else:
                failed += 1
            # Small delay to avoid rate limiting
            time.sleep(0.1)

    print()
    print("=" * 60)
    print("COMPLETE")
    print("=" * 60)
    print(f"Categories: {len(category_map)} created")
    print(f"Skills: {created}/{total_skills} created, {failed} failed")

    # Final count
    print()
    print("Final verification:")
    final_skills = get_all_skills()
    final_cats = get_all_categories()
    print(f"  Total skills in Learn365: {len(final_skills)}")
    print(f"  Total categories in Learn365: {len(final_cats)}")


if __name__ == "__main__":
    main()
