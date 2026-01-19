"""
Learn365 Skill Scale Set Updater
Updates all existing skills to use GSL Career Progression scale set

This ensures all skills use the same L0-L9 proficiency scale,
enabling target skill rules to work correctly.
"""
import requests
import base64
import json
import time

API_KEY = "ef5fd367-9a88-42b8-b3cf-c117aeb93d72"
CATALOG_ID = "b1670146-674a-4730-9e9d-d7d29ba52385"
BASE_URL = "https://api.365.systems"
GSL_CAREER_PROGRESSION_ID = "dc10f982-86fa-4a5b-8869-6d5e4dde769b"

# Auth header
auth_string = base64.b64encode(f":{API_KEY}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {auth_string}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def get_all_skills():
    """Get all skills (may be paginated, returns first 100)"""
    url = f"{BASE_URL}/services/skills/Skills"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    print(f"Error getting skills: {r.status_code}")
    return []


def get_all_skills_paginated():
    """Get all skills with pagination"""
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

    return all_skills


def update_skill_scaleset(skill_id, skill_title, new_scaleset_id):
    """Update a skill's scale set"""
    url = f"{BASE_URL}/services/skills/catalog/{CATALOG_ID}/Skills/{skill_id}"

    # PUT requires title and scaleSetId
    data = {
        "title": skill_title,
        "scaleSetId": new_scaleset_id
    }

    r = requests.put(url, headers=HEADERS, json=data)
    if r.status_code in [200, 204]:
        return True
    else:
        print(f"    Error updating: {r.status_code} - {r.text[:200]}")
        return False


def verify_scaleset_exists():
    """Verify GSL Career Progression scale set exists"""
    url = f"{BASE_URL}/services/skills/SkillScaleSets/{GSL_CAREER_PROGRESSION_ID}?$expand=levels"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        data = r.json()
        print(f"  Scale set: {data.get('title')}")
        print(f"  ID: {GSL_CAREER_PROGRESSION_ID}")
        if 'levels' in data:
            print(f"  Levels: {len(data['levels'])}")
        return True
    return False


def main():
    print("=" * 70)
    print("Learn365 Skill Scale Set Updater")
    print("Updates all skills to use GSL Career Progression (L0-L9)")
    print("=" * 70)
    print()

    # Step 1: Verify target scale set exists
    print("Step 1: Verifying GSL Career Progression scale set...")
    if not verify_scaleset_exists():
        print("  ERROR: GSL Career Progression scale set not found!")
        print("  Run learn365_skill_level_sets.py first")
        return
    print()

    # Step 2: Get all existing skills
    print("Step 2: Loading all existing skills...")
    skills = get_all_skills_paginated()
    print(f"  Found {len(skills)} skills")
    print()

    if not skills:
        print("  No skills found to update")
        return

    # Step 3: Analyze current state
    print("Step 3: Analyzing current scale set usage...")
    already_correct = 0
    needs_update = 0
    scaleset_counts = {}

    for skill in skills:
        current_scaleset = skill.get('scaleSetId', 'None')
        scaleset_counts[current_scaleset] = scaleset_counts.get(current_scaleset, 0) + 1

        if current_scaleset == GSL_CAREER_PROGRESSION_ID:
            already_correct += 1
        else:
            needs_update += 1

    print(f"  Already using GSL Career Progression: {already_correct}")
    print(f"  Need update: {needs_update}")
    print()

    print("  Current scale set distribution:")
    for ss_id, count in sorted(scaleset_counts.items(), key=lambda x: -x[1])[:10]:
        marker = " (GSL Career Progression)" if ss_id == GSL_CAREER_PROGRESSION_ID else ""
        print(f"    {ss_id[:20]}...: {count} skills{marker}")
    print()

    if needs_update == 0:
        print("All skills already use GSL Career Progression!")
        return

    # Step 4: Confirm update
    print(f"Step 4: Ready to update {needs_update} skills")
    print()
    confirm = input("  Proceed with update? (yes/no): ").strip().lower()

    if confirm != 'yes':
        print("  Cancelled")
        return
    print()

    # Step 5: Update skills
    print("Step 5: Updating skills...")
    updated = 0
    failed = 0
    skipped = 0

    for i, skill in enumerate(skills):
        skill_id = skill.get('id')
        skill_title = skill.get('title', 'Unknown')
        current_scaleset = skill.get('scaleSetId')

        if current_scaleset == GSL_CAREER_PROGRESSION_ID:
            skipped += 1
            continue

        if update_skill_scaleset(skill_id, skill_title, GSL_CAREER_PROGRESSION_ID):
            updated += 1
            if updated % 20 == 0:
                print(f"    Updated {updated} skills...")
        else:
            print(f"    FAILED: {skill_title}")
            failed += 1

        # Rate limiting
        time.sleep(0.1)

    print()
    print("=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"  Updated: {updated}")
    print(f"  Skipped (already correct): {skipped}")
    print(f"  Failed: {failed}")

    # Verification
    print()
    print("Verification:")
    skills_after = get_all_skills()
    correct_now = sum(1 for s in skills_after if s.get('scaleSetId') == GSL_CAREER_PROGRESSION_ID)
    print(f"  Skills using GSL Career Progression: {correct_now}/{len(skills_after)}")


if __name__ == "__main__":
    main()
