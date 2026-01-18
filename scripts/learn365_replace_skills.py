"""
Learn365 Skills Replacement
Delete all existing skills/categories and create clean framework
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

# New clean framework (10 Skill Level Sets with skills)
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
        "Documentation & Compliance",
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
        print(f"    Error creating category: {r.status_code} - {r.text[:100]}")
        return None

def create_skill(title, category_id):
    url = f"{BASE_URL}/services/skills/catalog/{CATALOG_ID}/Skills"
    data = {
        "title": title,
        "categoryId": category_id
    }
    r = requests.post(url, headers=HEADERS, json=data)
    if r.status_code in [200, 201]:
        return r.json()
    else:
        print(f"    Error creating skill '{title}': {r.status_code} - {r.text[:100]}")
        return None


def main():
    print("=" * 60)
    print("Learn365 Skills Framework Replacement")
    print("=" * 60)
    print()

    # Step 1: Delete all existing skills
    print("Step 1: Deleting existing skills...")
    skills = get_all_skills()
    print(f"  Found {len(skills)} skills to delete")
    deleted = 0
    for skill in skills:
        if delete_skill(skill['id']):
            deleted += 1
            if deleted % 20 == 0:
                print(f"    Deleted {deleted}/{len(skills)}...")
        else:
            print(f"    Failed to delete skill: {skill['title']}")
    print(f"  Deleted {deleted} skills")
    print()

    # Step 2: Delete all existing categories
    print("Step 2: Deleting existing categories...")
    categories = get_all_categories()
    print(f"  Found {len(categories)} categories to delete")
    deleted = 0
    for cat in categories:
        if delete_category(cat['id']):
            deleted += 1
            if deleted % 20 == 0:
                print(f"    Deleted {deleted}/{len(categories)}...")
        else:
            print(f"    Failed to delete category: {cat['name']}")
    print(f"  Deleted {deleted} categories")
    print()

    # Brief pause
    time.sleep(1)

    # Step 3: Create new categories
    print("Step 3: Creating new skill categories (10)...")
    category_map = {}
    for cat_name in SKILL_FRAMEWORK.keys():
        result = create_category(cat_name)
        if result:
            category_map[cat_name] = result['id']
            print(f"  Created: {cat_name}")
        else:
            print(f"  FAILED: {cat_name}")
    print(f"  Created {len(category_map)} categories")
    print()

    # Step 4: Create skills under each category
    print("Step 4: Creating skills...")
    total_skills = sum(len(skills) for skills in SKILL_FRAMEWORK.values())
    created = 0
    for cat_name, skills in SKILL_FRAMEWORK.items():
        cat_id = category_map.get(cat_name)
        if not cat_id:
            print(f"  Skipping {cat_name} - no category ID")
            continue

        print(f"  {cat_name} ({len(skills)} skills)...")
        for skill_title in skills:
            result = create_skill(skill_title, cat_id)
            if result:
                created += 1
            # Small delay to avoid rate limiting
            time.sleep(0.1)

    print()
    print("=" * 60)
    print("COMPLETE")
    print("=" * 60)
    print(f"Categories: {len(category_map)} created")
    print(f"Skills: {created}/{total_skills} created")


if __name__ == "__main__":
    main()
