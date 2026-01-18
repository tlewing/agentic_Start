"""
Learn365 Skills Management
Create skill categories and skills based on PROPOSED_SKILLS_FRAMEWORK.md
"""
import requests
import json
import base64

API_KEY = "ef5fd367-9a88-42b8-b3cf-c117aeb93d72"
CATALOG_ID = "b1670146-674a-4730-9e9d-d7d29ba52385"  # Main catalog from API response
BASE_URL = "https://api.365.systems"

# Auth header (Basic with empty user, API key as password)
auth_string = base64.b64encode(f":{API_KEY}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {auth_string}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def get_existing_skill_categories():
    """Get existing skill categories"""
    url = f"{BASE_URL}/services/skills/SkillCategories"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    print(f"Error getting categories: {r.status_code}")
    return []

def get_existing_skills():
    """Get existing skills"""
    url = f"{BASE_URL}/services/skills/Skills"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    print(f"Error getting skills: {r.status_code}")
    return []

def get_existing_scale_sets():
    """Get existing skill scale sets (proficiency levels)"""
    url = f"{BASE_URL}/services/skills/SkillScaleSets"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    print(f"Error getting scale sets: {r.status_code}")
    return []

def create_skill_category(name, description=""):
    """Create a new skill category"""
    url = f"{BASE_URL}/services/skills/catalog/{CATALOG_ID}/SkillCategories"
    data = {
        "Name": name,
        "Description": description
    }
    r = requests.post(url, headers=HEADERS, json=data)
    if r.status_code in [200, 201]:
        print(f"  Created category: {name}")
        return r.json()
    else:
        print(f"  Error creating category '{name}': {r.status_code} - {r.text[:200]}")
        return None

def create_skill(name, category_id, description="", scale_set_id=None):
    """Create a new skill"""
    url = f"{BASE_URL}/services/skills/catalog/{CATALOG_ID}/Skills"
    data = {
        "Name": name,
        "Description": description,
        "CategoryId": category_id
    }
    if scale_set_id:
        data["ScaleSetId"] = scale_set_id

    r = requests.post(url, headers=HEADERS, json=data)
    if r.status_code in [200, 201]:
        print(f"    Created skill: {name}")
        return r.json()
    else:
        print(f"    Error creating skill '{name}': {r.status_code} - {r.text[:200]}")
        return None


# Our proposed skill framework (10 Skill Level Sets)
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
        "LOTO Fundamentals",
        "Simple LOTO Procedures",
        "Complex LOTO Procedures",
        "Fall Hazard Recognition",
        "Ladder Safety",
        "Scaffold Fundamentals",
        "HazCom Program Fundamentals",
        "SDS Use & Access",
        "Chemical Hazard Identification",
    ],
    "Lean Construction": [
        "Lean Fundamentals",
        "Lean Application",
        "Eight Wastes Recognition",
        "Continuous Improvement",
        "Pull Planning",
        "Focus on Flow",
    ],
    "Leadership & Field Management": [
        "Foreman Role & Responsibilities",
        "Field Supervision",
        "Crew Planning",
        "Trade Coordination",
        "Jobsite Efficiency",
        "Quality Control",
        "Tool & Equipment Management",
        "Leadership Fundamentals",
        "Values-Driven Leadership",
        "Accountability & Ownership",
        "Team Building",
        "Team Management",
        "Delegation & Empowerment",
        "Employee Motivation",
        "Extreme Ownership",
    ],
    "Communication & Coaching": [
        "Effective Communication",
        "Building Relationships",
        "Mentoring & Coaching",
        "Conflict Resolution",
        "Setting Expectations",
    ],
    "Emotional Intelligence": [
        "EQ Fundamentals",
        "Self-Awareness",
        "Self-Regulation",
        "Empathy",
        "Social Skills",
        "EQ Leadership",
    ],
    "Performance Management": [
        "Performance Management Fundamentals",
        "Conducting Evaluations",
        "Performance Reviews",
        "Corrective Counseling",
        "Career Development",
    ],
    "Construction Software": [
        "Accubid Fundamentals",
        "ViewPoint Change Orders",
        "ProCore Fundamentals",
        "Job Plan Fundamentals",
        "Excel Skills",
    ],
    "Project Planning & Productivity": [
        "Project Planning",
        "Scheduling Techniques",
        "Productivity Analysis",
        "Time Management",
        "Process Improvement",
    ],
    "Documentation & Compliance": [
        "Documentation Practices",
        "Documentation & Reporting",
        "Regulatory Inspections",
    ],
    "Professional Development": [
        "Presentation Skills",
        "Strategic Thinking",
    ],
}


if __name__ == "__main__":
    print("=== Learn365 Skills Inventory ===")
    print()

    # Check existing
    print("Existing Skill Categories:")
    categories = get_existing_skill_categories()
    if categories:
        for cat in categories:
            print(f"  - {cat.get('Name', 'Unknown')} (ID: {cat.get('Id', 'N/A')})")
    else:
        print("  (none found)")
    print()

    print("Existing Skills:")
    skills = get_existing_skills()
    if skills:
        for skill in skills[:20]:  # Show first 20
            print(f"  - {skill.get('Name', 'Unknown')}")
        if len(skills) > 20:
            print(f"  ... and {len(skills) - 20} more")
    else:
        print("  (none found)")
    print()

    print("Existing Scale Sets (Proficiency Levels):")
    scale_sets = get_existing_scale_sets()
    if scale_sets:
        for ss in scale_sets:
            print(f"  - {ss.get('Name', 'Unknown')} (ID: {ss.get('Id', 'N/A')})")
    else:
        print("  (none found)")
    print()

    print(f"Total existing: {len(categories)} categories, {len(skills)} skills")
    print()
    print("Proposed framework: 10 categories, ~80 skills")
