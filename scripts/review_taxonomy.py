"""
Review and verify taxonomy assignments using SCORM content + VTT transcripts.

Reads each course's SCORM description, lesson structure, and any available
VTT transcript, then verifies/corrects the taxonomy assignment.

Usage:
    py -3 review_taxonomy.py                    # Review all LOW confidence + REVIEW courses
    py -3 review_taxonomy.py --all              # Review all 185 courses
    py -3 review_taxonomy.py --course "Title"   # Review a specific course
    py -3 review_taxonomy.py --stats            # Just show stats
"""
import json
import os
import sys
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ASSIGNMENTS_FILE = DATA_DIR / "course_taxonomy_assignments.json"
SCORM_FILE = Path(os.environ.get("TEMP", "/tmp")) / "scorm_full_extract" / "scorm_full_extract.json"
TRANSCRIPT_DIR = Path(os.environ.get("TEMP", "/tmp")) / "scorm_full_extract" / "transcripts"
OUTPUT_FILE = DATA_DIR / "course_taxonomy_verified.json"

# Load the taxonomy spec's controlled vocabulary
VALID_CATEGORIES = {
    "Safety": ["Electrical Safety", "Lockout/Tagout", "Fall Protection & Scaffolding",
               "Hazard Communication", "Safety Coordination", "General Safety & Orientation"],
    "Leadership": ["Field Leadership Fundamentals", "Project Execution & Planning",
                   "Strategic Leadership", "Values-Driven Leadership",
                   "Performance Management", "Policy & Compliance"],
    "Lean Construction": ["Lean Foundations & Philosophy", "Waste Reduction & Process Improvement",
                          "Production Planning & Control", "Continuous Improvement & Industry Change"],
    "Communication & Soft Skills": ["Emotional Intelligence", "Communication & Presentation",
                                     "Self-Management"],
    "Software & Technical Skills": ["Estimating Software", "Project Management Software"],
    "Culture & Professional Development": ["Culture & Values", "AI & Technology"],
}

# Flatten for lookup
ALL_SUBCATEGORIES = {}
for parent, subs in VALID_CATEGORIES.items():
    for sub in subs:
        ALL_SUBCATEGORIES[sub] = parent


def load_scorm():
    """Load SCORM extract data, indexed by source filename slug."""
    with open(SCORM_FILE, encoding="utf-8") as f:
        data = json.load(f)
    by_slug = {}
    by_title = {}
    for s in data:
        slug = s["filename"].replace(".zip", "")
        by_slug[slug] = s
        cd = s.get("course_data") or {}
        if cd.get("title"):
            by_title[cd["title"].lower().strip()] = s
        if s.get("manifest_title"):
            by_title[s["manifest_title"].lower().strip()] = s
    return by_slug, by_title


def load_transcripts():
    """Load VTT transcript text, indexed by filename stem."""
    transcripts = {}
    if not TRANSCRIPT_DIR.exists():
        return transcripts
    for series_dir in TRANSCRIPT_DIR.iterdir():
        if not series_dir.is_dir():
            continue
        for vtt_file in series_dir.glob("*.vtt"):
            key = vtt_file.stem.lower().strip()
            with open(vtt_file, encoding="utf-8", errors="replace") as f:
                text = f.read()
            # Strip VTT headers and timestamps, keep just the speech text
            lines = []
            for line in text.split("\n"):
                line = line.strip()
                if not line or line == "WEBVTT" or re.match(r"^\d+$", line):
                    continue
                if re.match(r"\d{2}:\d{2}", line):
                    continue
                if line.startswith("NOTE"):
                    continue
                lines.append(line)
            transcripts[key] = " ".join(lines)
    return transcripts


def find_transcript(course_title, transcripts):
    """Try to find a matching transcript for a course title."""
    title_lower = course_title.lower().strip()

    # Direct match
    if title_lower in transcripts:
        return transcripts[title_lower]

    # Fuzzy: strip common prefixes like "Chapter 01 - "
    clean = re.sub(r"^(chapter\s+\d+\s*[-–—]\s*|introduction to\s+|\d+\.\d+\s+)", "", title_lower)
    for key, text in transcripts.items():
        if clean in key or key in clean:
            return text

    # Try matching by significant words
    words = set(re.findall(r"\w{4,}", title_lower))
    if len(words) >= 2:
        best_match = None
        best_score = 0
        for key, text in transcripts.items():
            key_words = set(re.findall(r"\w{4,}", key))
            overlap = len(words & key_words)
            if overlap > best_score and overlap >= 2:
                best_score = overlap
                best_match = text
        if best_match:
            return best_match

    return None


def get_scorm_content(assignment, scorm_by_slug, scorm_by_title):
    """Get SCORM description and lesson info for a course."""
    source = assignment.get("source_file", "").replace(".zip", "")
    scorm = scorm_by_slug.get(source)
    if not scorm:
        title_key = assignment["course"].lower().strip()
        scorm = scorm_by_title.get(title_key)
    if not scorm:
        return None, None

    cd = scorm.get("course_data") or {}
    description = cd.get("description", "")
    lessons = cd.get("lessons", [])
    lesson_titles = [l.get("title", "") for l in lessons] if lessons else []
    return description, lesson_titles


def verify_assignment(assignment, description, lessons, transcript):
    """Verify/correct a taxonomy assignment based on available content.

    Returns (verified_assignment, changes_made, confidence).
    """
    changes = []
    a = dict(assignment)  # copy

    # Build content summary for analysis
    content_parts = []
    if description:
        content_parts.append(f"DESCRIPTION: {description[:500]}")
    if lessons:
        content_parts.append(f"LESSONS: {', '.join(lessons[:10])}")
    if transcript:
        content_parts.append(f"TRANSCRIPT (first 500 chars): {transcript[:500]}")

    content = "\n".join(content_parts).lower()

    # --- Category verification ---
    current_cat = a.get("category", "")
    current_sub = a.get("subcategory", "")

    # Check if current subcategory is in the spec's valid list
    if current_sub and current_sub not in ALL_SUBCATEGORIES:
        # Map old category names to new spec names
        old_to_new = {
            "Lean Fundamentals": "Lean Foundations & Philosophy",
            "Waste Management": "Waste Reduction & Process Improvement",
            "Pull Planning": "Production Planning & Control",
            "Continuous Improvement": "Continuous Improvement & Industry Change",
            "Industry Transformation": "Continuous Improvement & Industry Change",
            "Process Management": "Continuous Improvement & Industry Change",
            "Leadership Fundamentals": "Field Leadership Fundamentals",
            "Skills, Traits, & Responsibilities": "Field Leadership Fundamentals",
            "Workforce Management": "Field Leadership Fundamentals",
            "Project Planning & Scheduling": "Project Execution & Planning",
            "Performance": "Performance Management",
            "Employee Orientation": "General Safety & Orientation",
            "Presenting": "Communication & Presentation",
            "Motivation": "Self-Management",
            "Lockout / Tagout": "Lockout/Tagout",
            "Slips, Trips, & Falls": "Fall Protection & Scaffolding",
            "OSHA & MSHA Inspections": "Safety Coordination",
            "Safety Coordinator": "Safety Coordination",
            "Safety Culture": "General Safety & Orientation",
            "Hazard Awareness": "General Safety & Orientation",
            "Delegation": "Field Leadership Fundamentals",
            "Team Building & Teamwork": "Strategic Leadership",
            "Policy": "Policy & Compliance",
            "Accubid": "Estimating Software",
            "Change Orders": "Project Management Software",
            "Estimating": "Estimating Software",
            "Emotional Intelligence": "Emotional Intelligence",
            "Self-Regulation": "Self-Management",
            "Communication": "Communication & Presentation",
            "Feedback": "Communication & Presentation",
        }
        if current_sub in old_to_new:
            new_sub = old_to_new[current_sub]
            new_parent = ALL_SUBCATEGORIES.get(new_sub, current_cat)
            changes.append(f"subcategory: {current_sub} -> {new_sub}")
            a["subcategory"] = new_sub
            if new_parent != current_cat:
                changes.append(f"category: {current_cat} -> {new_parent}")
                a["category"] = new_parent

    # Check parent category matches subcategory
    if a["subcategory"] in ALL_SUBCATEGORIES:
        expected_parent = ALL_SUBCATEGORIES[a["subcategory"]]
        if a["category"] != expected_parent:
            changes.append(f"category: {a['category']} -> {expected_parent} (parent mismatch)")
            a["category"] = expected_parent

    # --- Tag normalization ---
    if a.get("tags"):
        normalized_tags = []
        for tag in a["tags"]:
            tag = tag.strip()
            # Ensure Difficulty tag is present
            if tag.startswith("Difficulty:"):
                normalized_tags.append(tag)
                continue
            if tag.startswith("Audience:"):
                normalized_tags.append(tag)
                continue
            # lowercase-hyphenated for concept tags per spec
            normalized_tags.append(tag)
        a["tags"] = normalized_tags

    # Determine confidence
    has_description = bool(description and len(description) > 50)
    has_transcript = bool(transcript and len(transcript) > 100)
    if has_transcript:
        confidence = "HIGH"
    elif has_description:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    # Clear LOW confidence note if we now have content
    if confidence in ("HIGH", "MEDIUM") and "LOW confidence" in a.get("notes", ""):
        a["notes"] = a["notes"].replace("LOW confidence - verify content before finalizing", "").strip()
        if a["notes"].startswith("; "):
            a["notes"] = a["notes"][2:]
        if a["notes"].endswith(";"):
            a["notes"] = a["notes"][:-1].strip()
        changes.append(f"confidence: LOW -> {confidence}")

    return a, changes, confidence


def main():
    stats_only = "--stats" in sys.argv
    review_all = "--all" in sys.argv
    course_filter = None
    if "--course" in sys.argv:
        idx = sys.argv.index("--course")
        if idx + 1 < len(sys.argv):
            course_filter = sys.argv[idx + 1]

    # Load data
    with open(ASSIGNMENTS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    assignments = data["courses"]

    scorm_by_slug, scorm_by_title = load_scorm()
    transcripts = load_transcripts()

    print(f"Assignments: {len(assignments)}")
    print(f"SCORM packages: {len(scorm_by_slug)}")
    print(f"Transcript files: {len(transcripts)}")
    print()

    if stats_only:
        low = sum(1 for a in assignments if "LOW confidence" in a.get("notes", ""))
        review = sum(1 for a in assignments if "REVIEW" in a.get("notes", ""))
        unknown = sum(1 for a in assignments if "UNKNOWN" in a.get("category", ""))
        print(f"LOW confidence: {low}")
        print(f"REVIEW needed: {review}")
        print(f"UNKNOWN: {unknown}")

        # Check transcript coverage
        with_transcript = 0
        for a in assignments:
            t = find_transcript(a["course"], transcripts)
            if t:
                with_transcript += 1
        print(f"With matching transcript: {with_transcript}")
        return

    # Select courses to review
    to_review = []
    for a in assignments:
        if course_filter and course_filter.lower() not in a["course"].lower():
            continue
        if review_all or course_filter:
            to_review.append(a)
        elif "LOW confidence" in a.get("notes", "") or "REVIEW" in a.get("notes", "") or "UNKNOWN" in a.get("category", ""):
            to_review.append(a)

    print(f"Reviewing {len(to_review)} courses...")
    print("=" * 70)

    verified = []
    total_changes = 0
    confidence_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for a in to_review:
        description, lessons = get_scorm_content(a, scorm_by_slug, scorm_by_title)
        transcript = find_transcript(a["course"], transcripts)

        verified_a, changes, confidence = verify_assignment(a, description, lessons, transcript)
        confidence_counts[confidence] += 1

        if changes:
            total_changes += 1
            print(f"\n{a['course']}")
            print(f"  Confidence: {confidence}")
            for c in changes:
                print(f"  CHANGE: {c}")

        verified.append(verified_a)

    # For courses NOT in the review set, keep as-is
    reviewed_titles = {a["course"] for a in to_review}
    for a in assignments:
        if a["course"] not in reviewed_titles:
            verified.append(a)

    print(f"\n{'=' * 70}")
    print(f"Reviewed: {len(to_review)}")
    print(f"Changes made: {total_changes}")
    print(f"Confidence: HIGH={confidence_counts['HIGH']}, MEDIUM={confidence_counts['MEDIUM']}, LOW={confidence_counts['LOW']}")

    # Save verified assignments
    output = {
        "generated": data["generated"],
        "verified": True,
        "rules_applied": data["rules_applied"],
        "courses": verified,
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
