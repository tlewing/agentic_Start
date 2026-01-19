"""
Learn365 Skill Level Sets Management
Creates the GSL Career Progression scale set with levels L0-L9

API Endpoint: POST /services/skills/catalog/{catalogId}/SkillScaleSets
"""
import requests
import base64
import json

API_KEY = "ef5fd367-9a88-42b8-b3cf-c117aeb93d72"
CATALOG_ID = "b1670146-674a-4730-9e9d-d7d29ba52385"
BASE_URL = "https://api.365.systems"

# Auth header (Basic with empty user, API key as password)
auth_string = base64.b64encode(f":{API_KEY}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {auth_string}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# GSL Career Progression Skill Level Set
# Based on B_SKILL_LEVEL_SETS.md
SKILL_LEVEL_SET = {
    "title": "GSL Career Progression",
    "isDefault": True,
    "levels": [
        {"title": "L0 - Pre-Employment", "value": 0},
        {"title": "L1 - Entry Level (Apprentice Year 1)", "value": 1},
        {"title": "L2 - Developing (Apprentice Year 2)", "value": 2},
        {"title": "L3 - Proficient (Apprentice Year 3)", "value": 3},
        {"title": "L4 - Advanced Apprentice (Year 4)", "value": 4},
        {"title": "L5 - Journeyman", "value": 5},
        {"title": "L6 - Lead Journeyman", "value": 6},
        {"title": "L7 - Foreman", "value": 7},
        {"title": "L8 - Superintendent", "value": 8},
        {"title": "L9 - Safety Specialist", "value": 9},
    ]
}


def get_existing_scale_sets():
    """Get existing skill scale sets"""
    url = f"{BASE_URL}/services/skills/SkillScaleSets"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    print(f"Error getting scale sets: {r.status_code} - {r.text[:200]}")
    return []


def get_scale_set_by_id(scale_set_id):
    """Get a specific scale set by ID"""
    url = f"{BASE_URL}/services/skills/SkillScaleSets/{scale_set_id}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    return None


def delete_scale_set(scale_set_id):
    """Delete a skill scale set"""
    url = f"{BASE_URL}/services/skills/catalog/{CATALOG_ID}/SkillScaleSets/{scale_set_id}"
    r = requests.delete(url, headers=HEADERS)
    return r.status_code in [200, 204]


def create_scale_set(scale_set_data):
    """Create a new skill scale set"""
    url = f"{BASE_URL}/services/skills/catalog/{CATALOG_ID}/SkillScaleSets"
    r = requests.post(url, headers=HEADERS, json=scale_set_data)
    if r.status_code in [200, 201]:
        return r.json()
    else:
        print(f"Error creating scale set: {r.status_code}")
        print(f"Response: {r.text[:500]}")
        return None


def update_scale_set(scale_set_id, scale_set_data):
    """Update an existing skill scale set"""
    url = f"{BASE_URL}/services/skills/catalog/{CATALOG_ID}/SkillScaleSets/{scale_set_id}"
    r = requests.put(url, headers=HEADERS, json=scale_set_data)
    if r.status_code in [200, 204]:
        return r.json() if r.text else scale_set_data
    else:
        print(f"Error updating scale set: {r.status_code}")
        print(f"Response: {r.text[:500]}")
        return None


def main():
    print("=" * 60)
    print("Learn365 Skill Level Sets Management")
    print("=" * 60)
    print()

    # Step 1: Check existing scale sets
    print("Step 1: Checking existing skill scale sets...")
    existing = get_existing_scale_sets()

    if existing:
        print(f"  Found {len(existing)} existing scale set(s):")
        for ss in existing:
            print(f"    - {ss.get('title', 'Unknown')} (ID: {ss.get('id', 'N/A')})")
            if 'levels' in ss:
                print(f"      Levels: {len(ss['levels'])}")
    else:
        print("  No existing scale sets found")
    print()

    # Step 2: Check if GSL Career Progression already exists
    gsl_set = None
    for ss in existing:
        if ss.get('title') == 'GSL Career Progression':
            gsl_set = ss
            break

    if gsl_set:
        print("Step 2: GSL Career Progression already exists")
        print(f"  ID: {gsl_set.get('id')}")
        print(f"  Current levels: {len(gsl_set.get('levels', []))}")

        # Ask if user wants to update
        print()
        print("  Options:")
        print("    1. Update existing scale set with new level definitions")
        print("    2. Delete and recreate")
        print("    3. Skip (keep existing)")
        print()

        choice = input("  Enter choice (1/2/3): ").strip()

        if choice == "1":
            print()
            print("  Updating scale set...")
            update_data = SKILL_LEVEL_SET.copy()
            update_data['id'] = gsl_set['id']
            result = update_scale_set(gsl_set['id'], update_data)
            if result:
                print("  Updated successfully!")
            else:
                print("  Update failed")

        elif choice == "2":
            print()
            print("  Deleting existing scale set...")
            if delete_scale_set(gsl_set['id']):
                print("  Deleted successfully")
                print("  Creating new scale set...")
                result = create_scale_set(SKILL_LEVEL_SET)
                if result:
                    print(f"  Created: {result.get('title')} (ID: {result.get('id')})")
                else:
                    print("  Creation failed")
            else:
                print("  Delete failed")
        else:
            print("  Skipping - keeping existing scale set")
    else:
        # Step 3: Create new scale set
        print("Step 2: Creating GSL Career Progression scale set...")
        result = create_scale_set(SKILL_LEVEL_SET)

        if result:
            print(f"  Created successfully!")
            print(f"  ID: {result.get('id')}")
            print(f"  Title: {result.get('title')}")
            if 'levels' in result:
                print(f"  Levels created: {len(result['levels'])}")
                for level in result['levels']:
                    print(f"    - {level.get('title')} (value: {level.get('value')}, id: {level.get('id', 'N/A')})")
        else:
            print("  Creation failed")

    print()
    print("=" * 60)
    print("COMPLETE")
    print("=" * 60)

    # Final verification
    print()
    print("Final verification:")
    final = get_existing_scale_sets()
    for ss in final:
        if ss.get('title') == 'GSL Career Progression':
            print(f"  GSL Career Progression exists with ID: {ss.get('id')}")
            # Get full details
            full = get_scale_set_by_id(ss['id'])
            if full and 'levels' in full:
                print(f"  Levels ({len(full['levels'])}):")
                for level in sorted(full['levels'], key=lambda x: x.get('value', 0)):
                    print(f"    {level.get('value')}: {level.get('title')} (ID: {level.get('id', 'N/A')})")


if __name__ == "__main__":
    main()
