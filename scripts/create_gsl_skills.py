"""
Create GSL Skills Framework in Learn365
- 10 Skill Categories (Skill Level Sets)
- 123 Skills across all categories
- Uses GSL Proficiency Scale
"""
import requests
import base64
import json
import time

API_KEY = "ef5fd367-9a88-42b8-b3cf-c117aeb93d72"
CATALOG_ID = "b1670146-674a-4730-9e9d-d7d29ba52385"
GSL_SCALE_SET_ID = "c7b1796f-3716-49fb-86dc-edf176b017dc"
BASE_URL = "https://api.365.systems"

# Auth header
auth_string = base64.b64encode(f":{API_KEY}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {auth_string}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# GSL Skills Framework (10 Skill Level Sets)
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


def create_category(name):
    """Create a skill category"""
    url = f"{BASE_URL}/services/skills/catalog/{CATALOG_ID}/SkillCategories"
    data = {"name": name}
    r = requests.post(url, headers=HEADERS, json=data)
    if r.status_code in [200, 201]:
        return r.json()
    else:
        print(f"  Error creating category '{name}': {r.status_code} - {r.text[:100]}")
        return None


def create_skill(title, category_name):
    """Create a skill with GSL proficiency scale"""
    url = f"{BASE_URL}/services/skills/catalog/{CATALOG_ID}/Skills"
    data = {
        "title": title,
        "scaleSetId": GSL_SCALE_SET_ID,
        "categories": [{"name": category_name}]
    }
    r = requests.post(url, headers=HEADERS, json=data)
    if r.status_code in [200, 201]:
        return r.json()
    else:
        print(f"    Error creating skill '{title}': {r.status_code} - {r.text[:100]}")
        return None


def main():
    print("=" * 60)
    print("GSL Skills Framework Creation")
    print("=" * 60)
    print()
    print(f"Scale Set: GSL Proficiency Scale ({GSL_SCALE_SET_ID})")
    print(f"Levels: Awareness, Basic, Intermediate, Advanced, Expert")
    print()

    # Step 1: Create categories
    print("Step 1: Creating Skill Categories...")
    category_results = {}
    for cat_name in SKILL_FRAMEWORK.keys():
        result = create_category(cat_name)
        if result:
            category_results[cat_name] = result['id']
            print(f"  Created: {cat_name}")
        else:
            print(f"  FAILED: {cat_name}")
        time.sleep(0.1)

    print(f"\n  Categories created: {len(category_results)}/{len(SKILL_FRAMEWORK)}")
    print()

    # Step 2: Create skills under each category
    print("Step 2: Creating Skills...")
    total_skills = sum(len(skills) for skills in SKILL_FRAMEWORK.values())
    created = 0
    failed = 0

    for cat_name, skills in SKILL_FRAMEWORK.items():
        print(f"\n  {cat_name} ({len(skills)} skills):")
        for skill_title in skills:
            result = create_skill(skill_title, cat_name)
            if result:
                created += 1
                print(f"    + {skill_title}")
            else:
                failed += 1
            time.sleep(0.15)  # Rate limiting

    print()
    print("=" * 60)
    print("COMPLETE")
    print("=" * 60)
    print(f"Categories: {len(category_results)} created")
    print(f"Skills: {created}/{total_skills} created ({failed} failed)")


if __name__ == "__main__":
    main()
