"""
Migrate existing Learn365 skills to GSL Framework
- Update scaleSetId to GSL Proficiency Scale
- Assign to correct new categories
"""
import requests
import base64
import json
import time

API_KEY = "ef5fd367-9a88-42b8-b3cf-c117aeb93d72"
CATALOG_ID = "b1670146-674a-4730-9e9d-d7d29ba52385"
GSL_SCALE_SET_ID = "c7b1796f-3716-49fb-86dc-edf176b017dc"
BASE_URL = "https://api.365.systems"

auth_string = base64.b64encode(f":{API_KEY}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {auth_string}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Skill to Category mapping (for skills that already exist)
SKILL_CATEGORY_MAP = {
    # Safety
    "Approach Boundary Management": "Safety",
    "Arc Flash Awareness": "Safety",
    "Arc Flash Risk Assessment": "Safety",
    "Energized Work Practices": "Safety",
    "Energized Work Permitting": "Safety",
    "Electrical Hazard Recognition": "Safety",
    "Abnormal Lock Removal": "Safety",
    "De-Energization Verification": "Safety",
    "Return to Service": "Safety",
    "Scaffold Access & Egress": "Safety",
    "Fall Protection on Scaffolds": "Safety",
    "GHS System Understanding": "Safety",
    "Container Label Use": "Safety",
    "SDS Use & Access": "Safety",
    "Chemical Hazard Identification": "Safety",
    "Confined Space Program": "Safety",
    "Atmospheric Hazard Detection": "Safety",
    "Entry Permit Management": "Safety",

    # Lean Construction
    "Lean Fundamentals": "Lean Construction",
    "Lean Application": "Lean Construction",
    "Eliminate Waste": "Lean Construction",
    "Focus on Flow": "Lean Construction",
    "Generate Value": "Lean Construction",
    "Optimize the Whole": "Lean Construction",
    "Continuous Improvement": "Lean Construction",
    "Respect for People": "Lean Construction",
    "Field Team Empowerment": "Lean Construction",

    # Leadership & Field Management
    "Trade Coordination": "Leadership & Field Management",
    "Jobsite Efficiency": "Leadership & Field Management",
    "Quality Control": "Leadership & Field Management",
    "Field Empowerment": "Leadership & Field Management",
    "Team Management": "Leadership & Field Management",
    "Delegation & Empowerment": "Leadership & Field Management",
    "Team Morale": "Leadership & Field Management",
    "Extreme Ownership": "Leadership & Field Management",

    # Communication & Coaching
    "Effective Communication": "Communication & Coaching",
    "Building Relationships": "Communication & Coaching",
    "Conducting One-on-Ones": "Communication & Coaching",
    "Mentoring & Coaching": "Communication & Coaching",
    "Conflict Resolution": "Communication & Coaching",
    "Handling Resistance": "Communication & Coaching",
    "Setting Expectations": "Communication & Coaching",
    "Using the GROW Model": "Communication & Coaching",

    # Emotional Intelligence
    "EQ Fundamentals": "Emotional Intelligence",
    "Self-Awareness": "Emotional Intelligence",
    "Self-Regulation": "Emotional Intelligence",
    "Empathy": "Emotional Intelligence",
    "Social Skills": "Emotional Intelligence",
    "EQ Leadership": "Emotional Intelligence",

    # Performance Management
    "Conducting Evaluations": "Performance Management",
    "Corrective Counseling": "Performance Management",

    # Construction Software
    "ProCore Job Setup": "Construction Software",
    "Vista": "Construction Software",
    "Outlook": "Construction Software",
    "Word": "Construction Software",

    # Project Planning & Productivity
    "Job Plan Analysis": "Project Planning & Productivity",
    "Scheduling Techniques": "Project Planning & Productivity",
    "Productivity Improvement": "Project Planning & Productivity",
    "Time Management": "Project Planning & Productivity",
    "Construction Project Lifecycle": "Project Planning & Productivity",
    "Process Improvement": "Project Planning & Productivity",

    # Documentation & Compliance
    "Documentation Practices": "Documentation & Compliance",
    "Documentation & Reporting": "Documentation & Compliance",
    "Regulatory Inspections": "Documentation & Compliance",

    # Professional Development
    "Strategic Thinking": "Professional Development",
    "Industry Leadership": "Professional Development",
}


def update_skill(skill_id, title, category_name):
    """Update skill to use GSL scale and new category"""
    url = f"{BASE_URL}/services/skills/catalog/{CATALOG_ID}/Skills/{skill_id}"
    data = {
        "title": title,
        "scaleSetId": GSL_SCALE_SET_ID,
        "categories": [{"name": category_name}]
    }
    r = requests.put(url, headers=HEADERS, json=data)
    return r.status_code == 200


def main():
    print("=" * 60)
    print("GSL Skills Migration")
    print("=" * 60)
    print()

    # Get all skills
    r = requests.get(f"{BASE_URL}/services/skills/Skills", headers=HEADERS)
    skills = r.json()
    print(f"Found {len(skills)} skills")
    print()

    updated = 0
    skipped = 0

    for skill in skills:
        title = skill.get('title', '')
        skill_id = skill.get('id', '')

        if title in SKILL_CATEGORY_MAP:
            category = SKILL_CATEGORY_MAP[title]
            if update_skill(skill_id, title, category):
                print(f"  Updated: {title} -> {category}")
                updated += 1
            else:
                print(f"  FAILED: {title}")
            time.sleep(0.1)
        else:
            skipped += 1

    print()
    print("=" * 60)
    print("COMPLETE")
    print("=" * 60)
    print(f"Updated: {updated}")
    print(f"Skipped (not in map): {skipped}")


if __name__ == "__main__":
    main()
