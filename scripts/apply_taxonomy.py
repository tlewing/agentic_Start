"""
Apply the approved taxonomy (categories + tags) to all Learn365 courses.

Phase 1: Categories + Tags only (competencies/skills blocked by API 405).

Usage:
    py -3 apply_taxonomy.py --dry-run         # Show what would change
    py -3 apply_taxonomy.py --test-one        # Apply to one course, then stop
    py -3 apply_taxonomy.py                   # Apply to all courses
    py -3 apply_taxonomy.py --report          # Just print match/mismatch report

Steps:
  1. Fetch all courses from all 3 catalogs (with current metadata)
  2. Load course_taxonomy_assignments.json
  3. Match assignments to live courses by title
  4. Build category lookup (existing IDs from backup + create new sub-categories)
  5. PATCH each course with category + tags
"""
import requests
import base64
import json
import sys
import os
from pathlib import Path

API_KEY = "ef5fd367-9a88-42b8-b3cf-c117aeb93d72"
BASE_URL = "https://api.365.systems"

CATALOGS = {
    "GSL Academy": "b1670146-674a-4730-9e9d-d7d29ba52385",
    "Safety Training": "02c2baf6-0827-4011-b42f-af9b5f008865",
    "Sandbox": "6dec10c7-41f0-4bdc-8305-75171ac3de04",
}

auth_string = base64.b64encode(f":{API_KEY}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {auth_string}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

DRY_RUN = "--dry-run" in sys.argv
TEST_ONE = "--test-one" in sys.argv
REPORT_ONLY = "--report" in sys.argv

DATA_DIR = Path(__file__).parent.parent / "data"
ASSIGNMENTS_FILE = DATA_DIR / "course_taxonomy_verified.json"
BACKUP_FILE = DATA_DIR / "course_metadata_backup_20260521_050600.json"
LIVE_CATS_FILE = DATA_DIR / "learn365_categories_live.json"


def fetch_all_courses():
    """Fetch all courses from all catalogs."""
    all_courses = []
    for name, cat_id in CATALOGS.items():
        url = (
            f"{BASE_URL}/odata/v2/Courses"
            f"?%24filter=CourseCatalogId eq {cat_id}"
            f"&%24top=500"
            f"&%24expand=Categories,Tags,Competencies"
            f"&%24select=Title,Id,CourseCatalogId,Categories,Tags,Competencies"
        )
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        courses = r.json().get("value", [])
        for c in courses:
            c["_catalog_name"] = name
        all_courses.extend(courses)
        print(f"  {name}: {len(courses)} courses")
    return all_courses


def build_category_lookup():
    """Build name -> {Id, ParentId, CatalogId} from live API data + backup."""
    lookup = {}  # (catalog_id, name) -> category obj
    parents = {}  # (catalog_id, name) -> category obj (root-level only)
    by_name = {}  # name -> category obj (cross-catalog fallback)

    # Primary: live categories from API
    if LIVE_CATS_FILE.exists():
        with open(LIVE_CATS_FILE) as f:
            live_cats = json.load(f)
        for cat in live_cats:
            key = (cat["CourseCatalogId"], cat["Name"])
            obj = {
                "Id": cat["Id"],
                "Name": cat["Name"],
                "CourseCatalogId": cat["CourseCatalogId"],
                "ParentCategoryId": cat.get("ParentCategoryId") or "",
            }
            lookup[key] = obj
            by_name.setdefault(cat["Name"], obj)
            if not cat.get("ParentCategoryId"):
                parents[key] = obj

    # Fallback: backup data
    with open(BACKUP_FILE) as f:
        backup = json.load(f)
    for course in backup:
        catalog_id = course.get("CourseCatalogId", "")
        for cat in course.get("Categories", []):
            key = (cat.get("CourseCatalogId", catalog_id), cat["Name"])
            if key not in lookup:
                lookup[key] = {
                    "Id": cat["Id"],
                    "Name": cat["Name"],
                    "CourseCatalogId": cat.get("CourseCatalogId", catalog_id),
                    "ParentCategoryId": cat.get("ParentCategoryId", ""),
                }
                by_name.setdefault(cat["Name"], lookup[key])

    return lookup, parents, by_name


def build_tag_lookup():
    """Build name -> {Id, CatalogId} from backup data."""
    with open(BACKUP_FILE) as f:
        backup = json.load(f)

    lookup = {}  # (catalog_id, name_lower) -> tag obj
    for course in backup:
        catalog_id = course.get("CourseCatalogId", "")
        for tag in course.get("Tags", []):
            key = (tag.get("CourseCatalogId", catalog_id), tag["Name"].lower())
            if key not in lookup:
                lookup[key] = {
                    "Id": tag["Id"],
                    "Name": tag["Name"],
                    "CourseCatalogId": tag.get("CourseCatalogId", catalog_id),
                }

    return lookup


# Mapping from spec subcategory names to existing Learn365 category names
# (where the existing name differs from the spec name)
SUBCATEGORY_NAME_MAP = {
    # Spec name -> existing Learn365 name (if different)
    "Electrical Safety": "Electrical Safety",
    "Lockout/Tagout": "Lockout / Tagout",
    "Fall Protection & Scaffolding": "Slips, Trips, & Falls",  # closest existing
    "Hazard Communication": "Hazard Communication",
    "Field Leadership Fundamentals": "Leadership Fundamentals",
    "Skills, Traits, & Responsibilities": "Leadership Fundamentals",  # sub of Leadership
    "Lean Foundations & Philosophy": "Lean Fundamentals",
    "Waste Reduction & Process Improvement": "Waste Management",
    "Production Planning & Control": "Pull Planning",
    "Continuous Improvement & Industry Change": "Continuous Improvement",
    "Emotional Intelligence": None,  # Need to find
    "Communication & Presentation": "Presenting",  # closest existing
    "Self-Management": None,  # new
    "Estimating Software": None,  # new
    "Project Management Software": None,  # new
}

# Parent category name -> existing root ID mapping
PARENT_ROOTS = {
    "Safety": "3900a6ba-e68d-4499-907c-4fb91a8449fb",
    "Leadership": "cdd2d2ca-2b06-461c-a1bd-5ba00cf52f59",
    "Lean Principals": "02396841-12c7-4242-ad14-fe02ab3d7c62",
    "Soft Skills": None,  # need to find from backup
    "Project Management": None,  # need to find
}


def normalize_title(title):
    """Normalize course title for matching."""
    return title.strip().lower()


def match_courses(live_courses, assignments):
    """Match assignment entries to live courses by title."""
    live_by_title = {}
    for c in live_courses:
        key = normalize_title(c["Title"])
        if key not in live_by_title:
            live_by_title[key] = c
        # Handle duplicates - prefer GSL Academy catalog
        elif c["_catalog_name"] == "GSL Academy":
            live_by_title[key] = c

    matched = []
    unmatched_assignments = []
    for a in assignments:
        key = normalize_title(a["course"])
        if key in live_by_title:
            matched.append((a, live_by_title[key]))
        else:
            unmatched_assignments.append(a)

    return matched, unmatched_assignments


# Map spec subcategory names to existing Learn365 category names
SPEC_TO_EXISTING = {
    "Estimating Software": "Estimating",
    "Fall Protection & Scaffolding": "Slips, Trips, & Falls",
    "Field Leadership Fundamentals": "Leadership Fundamentals",
    "Lean Foundations & Philosophy": "Lean Fundamentals",
    "Lockout/Tagout": "Lockout / Tagout",
    "Performance Management": "Performance",
    "Project Management Software": "Project Management",
    "Waste Reduction & Process Improvement": "Waste Management",
    "Continuous Improvement & Industry Change": "Continuous Improvement",
    "Production Planning & Control": "Pull Planning",
    "Communication & Presentation": "Presenting",
    "Self-Management": "Self-Regulation",
    "General Safety & Orientation": "Employee Orientation",
    "Safety Coordination": "Safety Coordinator",
    "Strategic Leadership": "Leadership Fundamentals",
    "Values-Driven Leadership": "Leadership Fundamentals",
    "Policy & Compliance": "Policy",
    "Project Execution & Planning": "Project Planning & Scheduling",
}


def resolve_category(assignment, live_course, cat_lookup, by_name):
    """Resolve the category for a course assignment.

    Returns a list of category objects for the PATCH payload.
    Uses live category IDs. Remaps spec names to existing Learn365 names.
    """
    cat_name = assignment.get("subcategory") or assignment.get("category")
    catalog_id = live_course.get("CourseCatalogId", "")

    if not cat_name or cat_name.startswith("[UNKNOWN"):
        return []

    # Remap spec names to existing Learn365 names
    if cat_name in SPEC_TO_EXISTING:
        cat_name = SPEC_TO_EXISTING[cat_name]

    # Try exact match (catalog_id, name)
    key = (catalog_id, cat_name)
    if key in cat_lookup:
        cat = cat_lookup[key]
        return [{
            "Id": cat["Id"],
            "Name": cat["Name"],
            "CourseCatalogId": catalog_id,
            "ParentCategoryId": cat.get("ParentCategoryId", ""),
        }]

    # Try cross-catalog by name
    if cat_name in by_name:
        cat = by_name[cat_name]
        return [{
            "Id": cat["Id"],
            "Name": cat["Name"],
            "CourseCatalogId": catalog_id,
            "ParentCategoryId": cat.get("ParentCategoryId", ""),
        }]

    # No existing category found — pass Name only (will be silently ignored)
    return [{"Name": cat_name, "CourseCatalogId": catalog_id}]


def resolve_tags(assignment, live_course, tag_lookup):
    """Build tag list for PATCH payload.

    Learn365 auto-creates tags on PATCH if they don't exist,
    so we just pass Name + CourseCatalogId.
    """
    catalog_id = live_course.get("CourseCatalogId", "")
    raw_tags = assignment.get("tags", [])

    # Add audience tags from mandatory_for / recommended_for
    for role in assignment.get("mandatory_for", []):
        raw_tags.append(f"Audience: {role}")
    for role in assignment.get("recommended_for", []):
        audience_tag = f"Audience: {role}"
        if audience_tag not in raw_tags:
            raw_tags.append(audience_tag)

    # Add content type tag if determinable
    # (series-chapter for courses in a numbered series)
    title = assignment.get("course", "")
    if any(title.startswith(p) for p in ["Chapter ", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.", "11.", "12."]):
        if "series-chapter" not in raw_tags:
            raw_tags.append("series-chapter")

    result = []
    seen = set()
    for tag_name in raw_tags:
        tag_name = tag_name.strip()
        if not tag_name or tag_name.lower() in seen:
            continue
        seen.add(tag_name.lower())

        # Try to find existing tag ID
        key = (catalog_id, tag_name.lower())
        if key in tag_lookup:
            existing = tag_lookup[key]
            result.append({
                "Id": existing["Id"],
                "Name": existing["Name"],
                "CourseCatalogId": catalog_id,
            })
        else:
            # New tag — Learn365 should auto-create on PATCH
            result.append({
                "Name": tag_name,
                "CourseCatalogId": catalog_id,
            })

    return result


def patch_course(course_id, payload):
    """PATCH a course with categories and tags."""
    url = f"{BASE_URL}/odata/v2/Courses({course_id})"
    r = requests.patch(url, headers=HEADERS, json=payload)
    return r.status_code, r.text


def main():
    print("=" * 60)
    print("Learn365 Taxonomy Re-Apply")
    print("=" * 60)

    if DRY_RUN:
        print("*** DRY RUN — no changes will be made ***\n")
    elif TEST_ONE:
        print("*** TEST ONE — will apply to first matched course only ***\n")
    elif REPORT_ONLY:
        print("*** REPORT ONLY — showing match status ***\n")

    # Load assignments
    with open(ASSIGNMENTS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    assignments = data["courses"]
    print(f"Loaded {len(assignments)} assignments from spec\n")

    # Fetch live courses
    print("Fetching live courses...")
    live_courses = fetch_all_courses()
    print(f"Total live courses: {len(live_courses)}\n")

    # Build lookups
    print("Building category + tag lookups from live API + backup...")
    cat_lookup, parent_lookup, by_name = build_category_lookup()
    tag_lookup = build_tag_lookup()
    print(f"  Categories: {len(cat_lookup)} unique (name, catalog) pairs")
    print(f"  By-name fallback: {len(by_name)} unique names")
    print(f"  Tags: {len(tag_lookup)} unique (name, catalog) pairs\n")

    # Match
    matched, unmatched = match_courses(live_courses, assignments)
    print(f"Matched: {len(matched)} courses")
    print(f"Unmatched assignments: {len(unmatched)}")
    if unmatched:
        for a in unmatched[:10]:
            notes = a.get("notes", "")
            print(f"  UNMATCHED: {a['course']}{' — ' + notes if notes else ''}")
        if len(unmatched) > 10:
            print(f"  ... and {len(unmatched) - 10} more")
    print()

    if REPORT_ONLY:
        # Show category resolution for each matched course
        new_cats = set()
        for assignment, live in matched:
            cats = resolve_category(assignment, live, cat_lookup, by_name)
            for c in cats:
                if "Id" not in c:
                    new_cats.add(c["Name"])
        if new_cats:
            print(f"Categories that need creating ({len(new_cats)}):")
            for n in sorted(new_cats):
                print(f"  NEW: {n}")
        else:
            print("All categories resolve to existing IDs.")
        return

    # Apply
    success = 0
    failed = 0
    skipped = 0
    new_categories_needed = set()

    for assignment, live in matched:
        title = live["Title"]
        course_id = live["Id"]

        # Skip unknown/investigation courses
        if assignment.get("category", "").startswith("[UNKNOWN"):
            print(f"  SKIP: {title} — category unknown")
            skipped += 1
            continue

        categories = resolve_category(assignment, live, cat_lookup, by_name)

        # Track new categories (no Id = needs creating in Admin UI first)
        for c in categories:
            if "Id" not in c:
                new_categories_needed.add(c["Name"])

        # Categories only — Tags cannot be set via API (Learn365 limitation)
        payload = {
            "Categories": categories,
        }

        if DRY_RUN:
            cat_names = [c.get("Name", "?") for c in categories]
            tag_names = [t.get("Name", "?") for t in tags]
            has_id = all("Id" in c for c in categories)
            cat_status = "OK" if has_id else "NEW"
            print(f"  [{cat_status}] {title}")
            print(f"       Cat: {', '.join(cat_names)}")
            print(f"       Tags ({len(tag_names)}): {', '.join(tag_names[:5])}{'...' if len(tag_names) > 5 else ''}")
            success += 1
            continue

        # Actually PATCH
        status, text = patch_course(course_id, payload)
        if 200 <= status < 300:
            print(f"  OK ({status}): {title}")
            success += 1
        else:
            print(f"  FAIL ({status}): {title}")
            print(f"       Response: {text[:200]}")
            failed += 1

        if TEST_ONE:
            print(f"\n*** TEST ONE complete — stopping after first course ***")
            break

    print(f"\n{'=' * 60}")
    print(f"Results: {success} success, {failed} failed, {skipped} skipped")

    if new_categories_needed:
        print(f"\nCategories that need creating first ({len(new_categories_needed)}):")
        for n in sorted(new_categories_needed):
            print(f"  NEW: {n}")
        if not DRY_RUN:
            print("NOTE: These courses may have failed if Learn365 doesn't auto-create categories.")
            print("Run with --report to see the full list, then create them in Admin UI.")


if __name__ == "__main__":
    main()
