"""
Job 01 Full Run — Build CODE_REGISTRY, detect duplicates, classify all courses,
map to S5 skills, and generate the full crosswalk.
"""
import json, csv, os, re, tempfile
from collections import defaultdict

extract_dir = os.path.join(tempfile.gettempdir(), "scorm_full_extract")
output_dir = r"C:\Users\tewing\OneDrive - GSL Electric\Projects\GSL-Operations-Framework\docs\skills"
catalog_dir = r"C:\Users\tewing\OneDrive - GSL Electric\Projects\GSL-Operations-Framework\docs\catalog"

# Load extraction data
with open(os.path.join(extract_dir, "scorm_full_extract.json"), "r", encoding="utf-8") as f:
    courses = json.load(f)

# S5 skill vocabulary (SK-ID -> original name -> domain -> keywords)
S5_SKILLS = {
    "SK-001": {"name": "AI Ethics and Responsible Use", "domain": "AI & Technology", "kw": ["ai ethics", "responsible ai"]},
    "SK-002": {"name": "Explainable AI (XAI)", "domain": "AI & Technology", "kw": ["explainable ai", "xai"]},
    "SK-003": {"name": "AI Model Deployment", "domain": "AI & Technology", "kw": ["ai model", "mlops"]},
    "SK-004": {"name": "AI Project Management", "domain": "AI & Technology", "kw": ["ai project"]},
    "SK-005": {"name": "Culture", "domain": "Culture & Values", "kw": ["culture", "organizational culture"]},
    "SK-006": {"name": "Values Alignment", "domain": "Culture & Values", "kw": ["values alignment", "values"]},
    "SK-007": {"name": "Values-Driven Leadership", "domain": "Culture & Values", "kw": ["values-driven", "values driven", "coach k"]},
    "SK-008": {"name": "Accountability", "domain": "Leadership", "kw": ["accountability"]},
    "SK-009": {"name": "Accountability in Leadership", "domain": "Leadership", "kw": ["accountability", "leadership accountability"]},
    "SK-010": {"name": "Extreme Ownership", "domain": "Leadership", "kw": ["extreme ownership"]},
    "SK-011": {"name": "Leadership", "domain": "Leadership", "kw": ["leadership", "leader"]},
    "SK-012": {"name": "Leadership Fundamentals", "domain": "Leadership", "kw": ["leadership fundamentals", "what makes a leader"]},
    "SK-013": {"name": "Leading with Purpose", "domain": "Leadership", "kw": ["leading with purpose", "purpose"]},
    "SK-014": {"name": "Self-Awareness", "domain": "Leadership", "kw": ["self-awareness", "self awareness"]},
    "SK-015": {"name": "Career Development", "domain": "Leadership", "kw": ["career development"]},
    "SK-016": {"name": "Field Leadership", "domain": "Leadership", "kw": ["field leadership"]},
    "SK-017": {"name": "Field Supervision", "domain": "Leadership", "kw": ["field supervision", "supervision"]},
    "SK-018": {"name": "Foreman Role & Responsibilities", "domain": "Leadership", "kw": ["foreman", "roles and responsibilities"]},
    "SK-019": {"name": "Conducting Evaluations", "domain": "Leadership", "kw": ["evaluation", "conducting evaluation"]},
    "SK-020": {"name": "Conducting Field Evaluations", "domain": "Leadership", "kw": ["field evaluation"]},
    "SK-021": {"name": "Corrective Counseling", "domain": "Leadership", "kw": ["corrective counseling", "counseling"]},
    "SK-022": {"name": "Employee Assessment", "domain": "Leadership", "kw": ["employee assessment"]},
    "SK-023": {"name": "Employee Motivation", "domain": "Leadership", "kw": ["employee motivation", "motivation"]},
    "SK-024": {"name": "Employee Recognition", "domain": "Leadership", "kw": ["employee recognition", "recognition"]},
    "SK-025": {"name": "Nevada Employee Rights", "domain": "Leadership", "kw": ["nevada", "employee rights"]},
    "SK-026": {"name": "Performance Reviews", "domain": "Leadership", "kw": ["performance review"]},
    "SK-027": {"name": "Identifying Strengths & Values", "domain": "Leadership", "kw": ["strengths", "identifying strengths"]},
    "SK-028": {"name": "Planning & Scheduling", "domain": "Leadership", "kw": ["planning", "scheduling"]},
    "SK-029": {"name": "Project Planning", "domain": "Leadership", "kw": ["project planning"]},
    "SK-030": {"name": "Project Planning & Execution", "domain": "Leadership", "kw": ["project planning", "execution"]},
    "SK-031": {"name": "Strategic Thinking", "domain": "Leadership", "kw": ["strategic thinking", "strategy"]},
    "SK-032": {"name": "Crew Planning", "domain": "Leadership", "kw": ["crew planning", "manpower"]},
    "SK-033": {"name": "Team Management", "domain": "Leadership", "kw": ["team management"]},
    "SK-034": {"name": "Team Morale", "domain": "Leadership", "kw": ["team morale", "morale"]},
    "SK-035": {"name": "Team Motivation Fundamentals", "domain": "Leadership", "kw": ["team motivation", "motivating"]},
    "SK-036": {"name": "Delegation & Empowerment", "domain": "Leadership", "kw": ["delegation", "empowerment"]},
    "SK-037": {"name": "Empowering Teams", "domain": "Leadership", "kw": ["empowering teams", "empower"]},
    "SK-038": {"name": "Project Team Leadership", "domain": "Leadership", "kw": ["project team", "project leadership"]},
    "SK-039": {"name": "Team Building", "domain": "Leadership", "kw": ["team building"]},
    "SK-040": {"name": "Continuous Improvement", "domain": "Lean Principles", "kw": ["continuous improvement", "kaizen"]},
    "SK-041": {"name": "Focus on Flow", "domain": "Lean Principles", "kw": ["flow", "production flow"]},
    "SK-042": {"name": "Pull Planning", "domain": "Lean Principles", "kw": ["pull planning", "last planner"]},
    "SK-043": {"name": "Lean Application", "domain": "Lean Principles", "kw": ["lean application", "lean apply"]},
    "SK-044": {"name": "Lean Fundamentals", "domain": "Lean Principles", "kw": ["lean fundamental", "what is lean", "lean productivity"]},
    "SK-045": {"name": "Lean History Understanding", "domain": "Lean Principles", "kw": ["lean history", "toyota", "tps"]},
    "SK-046": {"name": "Lean Mindset", "domain": "Lean Principles", "kw": ["lean mindset"]},
    "SK-047": {"name": "Respect for People", "domain": "Lean Principles", "kw": ["respect for people"]},
    "SK-048": {"name": "Productivity Benefits", "domain": "Lean Principles", "kw": ["productivity benefit"]},
    "SK-049": {"name": "Productivity Execution", "domain": "Lean Principles", "kw": ["productivity execution", "on-site productivity"]},
    "SK-050": {"name": "Eight Wastes Recognition", "domain": "Lean Principles", "kw": ["eight wastes", "8 wastes", "muda", "waste"]},
    "SK-051": {"name": "Eliminate Waste", "domain": "Lean Principles", "kw": ["eliminate waste", "minimizing waste"]},
    "SK-052": {"name": "Documentation & Reporting", "domain": "Management", "kw": ["documentation", "reporting"]},
    "SK-053": {"name": "Documentation Practices", "domain": "Management", "kw": ["documentation practices", "document management"]},
    "SK-054": {"name": "Quality Control", "domain": "Management", "kw": ["quality control", "qc", "inspection"]},
    "SK-055": {"name": "Estimating", "domain": "Procurement", "kw": ["estimating"]},
    "SK-056": {"name": "Attendant Safety Practices", "domain": "Safety", "kw": ["attendant", "confined space attendant"]},
    "SK-057": {"name": "Confined Space Program", "domain": "Safety", "kw": ["confined space"]},
    "SK-058": {"name": "Hazardous Atmosphere Recognition", "domain": "Safety", "kw": ["hazardous atmosphere", "atmospheric"]},
    "SK-059": {"name": "Approach Boundary Management", "domain": "Safety", "kw": ["approach boundary", "boundary"]},
    "SK-060": {"name": "Arc Flash Awareness", "domain": "Safety", "kw": ["arc flash"]},
    "SK-061": {"name": "Arc Flash Risk Assessment", "domain": "Safety", "kw": ["arc flash risk", "risk assessment"]},
    "SK-062": {"name": "Electrical Boundary Compliance", "domain": "Safety", "kw": ["electrical boundary", "nfpa 70e boundary"]},
    "SK-063": {"name": "Electrical Hazard Recognition", "domain": "Safety", "kw": ["electrical hazard"]},
    "SK-064": {"name": "Electrical Risk Assessment", "domain": "Safety", "kw": ["electrical risk", "shock risk"]},
    "SK-065": {"name": "Electrical Safety Fundamentals", "domain": "Safety", "kw": ["electrical safety"]},
    "SK-066": {"name": "Electrical Work Safety", "domain": "Safety", "kw": ["electrical work", "safe work"]},
    "SK-067": {"name": "Electrically Safe Work Process", "domain": "Safety", "kw": ["electrically safe", "safe work process"]},
    "SK-068": {"name": "Energized Work Practices", "domain": "Safety", "kw": ["energized work", "live work"]},
    "SK-069": {"name": "Emergency Response", "domain": "Safety", "kw": ["emergency response"]},
    "SK-070": {"name": "Emergency Response Decision Making", "domain": "Safety", "kw": ["emergency decision"]},
    "SK-071": {"name": "First / CPR/ AED", "domain": "Safety", "kw": ["first aid", "cpr", "aed"]},
    "SK-072": {"name": "Incident Investigation", "domain": "Safety", "kw": ["incident investigation", "accident investigation"]},
    "SK-073": {"name": "Injury Management", "domain": "Safety", "kw": ["injury management", "case management"]},
    "SK-074": {"name": "Fall Hazard Recognition", "domain": "Safety", "kw": ["fall hazard", "fall protection"]},
    "SK-075": {"name": "Ladder Safety", "domain": "Safety", "kw": ["ladder"]},
    "SK-076": {"name": "Personal Fall Arrest Systems", "domain": "Safety", "kw": ["fall arrest", "pfas", "harness"]},
    "SK-077": {"name": "Scaffold Fundamentals", "domain": "Safety", "kw": ["scaffold"]},
    "SK-078": {"name": "Hazard Recognition", "domain": "Safety", "kw": ["hazard recognition", "hazard awareness"]},
    "SK-079": {"name": "Personal Safety", "domain": "Safety", "kw": ["personal safety", "ppe"]},
    "SK-080": {"name": "Pre-Task Safety Planning", "domain": "Safety", "kw": ["pre-task", "jha", "task planning"]},
    "SK-081": {"name": "Regulatory Inspections", "domain": "Safety", "kw": ["osha", "msha", "regulatory", "inspection"]},
    "SK-082": {"name": "Return to Service", "domain": "Safety", "kw": ["return to service"]},
    "SK-083": {"name": "Safety", "domain": "Safety", "kw": ["safety"]},
    "SK-084": {"name": "Safety Awareness & Culture", "domain": "Safety", "kw": ["safety culture", "safety awareness"]},
    "SK-085": {"name": "Safety Culture & Documentation", "domain": "Safety", "kw": ["safety culture", "safety documentation"]},
    "SK-086": {"name": "Safety Inspections", "domain": "Safety", "kw": ["safety inspection", "workplace inspection"]},
    "SK-087": {"name": "Safety Responsibility", "domain": "Safety", "kw": ["safety responsibility"]},
    "SK-088": {"name": "Chemical Hazard Identification", "domain": "Safety", "kw": ["chemical hazard", "types of chemical"]},
    "SK-089": {"name": "Container Label Use", "domain": "Safety", "kw": ["container label", "labeling"]},
    "SK-090": {"name": "HazCom Program Fundamentals", "domain": "Safety", "kw": ["hazcom", "hazard communication"]},
    "SK-091": {"name": "Hazard & Precautionary Statement Use", "domain": "Safety", "kw": ["precautionary statement", "ghs"]},
    "SK-092": {"name": "SDS Use & Access", "domain": "Safety", "kw": ["sds", "safety data sheet"]},
    "SK-093": {"name": "Written Program & Employee Rights", "domain": "Safety", "kw": ["written program", "employee rights"]},
    "SK-094": {"name": "Complex LOTO Procedures", "domain": "Safety", "kw": ["complex loto", "complex lockout"]},
    "SK-095": {"name": "Hazardous Energy Control", "domain": "Safety", "kw": ["hazardous energy", "energy control"]},
    "SK-096": {"name": "LOTO Fundamentals", "domain": "Safety", "kw": ["loto", "lockout tagout", "lockout/tagout"]},
    "SK-097": {"name": "LOTO Mastery", "domain": "Safety", "kw": ["loto mastery"]},
    "SK-098": {"name": "Simple LOTO Procedures", "domain": "Safety", "kw": ["simple loto", "simple lockout"]},
    "SK-099": {"name": "Communication", "domain": "Soft Skills", "kw": ["communication"]},
    "SK-100": {"name": "Effective Communication", "domain": "Soft Skills", "kw": ["effective communication"]},
    "SK-101": {"name": "Handling Resistance in Counseling", "domain": "Soft Skills", "kw": ["resistance", "counseling"]},
    "SK-102": {"name": "Public Speaking", "domain": "Soft Skills", "kw": ["public speaking", "presenting"]},
    "SK-103": {"name": "Slide Preparation", "domain": "Soft Skills", "kw": ["slide", "presentation", "creating slides"]},
    "SK-104": {"name": "Team Communication Practices", "domain": "Soft Skills", "kw": ["team communication"]},
    "SK-105": {"name": "EQ Fundamentals", "domain": "Soft Skills", "kw": ["eq fundamentals", "emotional intelligence fundamentals"]},
    "SK-106": {"name": "EQ Leadership", "domain": "Soft Skills", "kw": ["eq leadership", "leading with emotional"]},
    "SK-107": {"name": "Emotional Intelligence (EQ)", "domain": "Soft Skills", "kw": ["emotional intelligence"]},
    "SK-108": {"name": "Empathy", "domain": "Soft Skills", "kw": ["empathy"]},
    "SK-109": {"name": "Self-Regulation", "domain": "Soft Skills", "kw": ["self-regulation", "self regulation"]},
    "SK-110": {"name": "Social Skills", "domain": "Soft Skills", "kw": ["social skills"]},
    "SK-111": {"name": "Mentoring and Development", "domain": "Soft Skills", "kw": ["mentoring", "coaching", "develop emerging"]},
    "SK-112": {"name": "Building Relationships", "domain": "Soft Skills", "kw": ["building relationships", "relationship"]},
    "SK-113": {"name": "Accubid", "domain": "Software", "kw": ["accubid"]},
    "SK-114": {"name": "Accubid & ProCore Integration", "domain": "Software", "kw": ["accubid procore"]},
    "SK-115": {"name": "Accubid Fundamentals", "domain": "Software", "kw": ["accubid fundamentals", "accubid pro"]},
    "SK-116": {"name": "Accubid Sort Code 5 Export", "domain": "Software", "kw": ["sort code"]},
    "SK-117": {"name": "Creating Job Plans", "domain": "Software", "kw": ["creating job plan", "job plan"]},
    "SK-118": {"name": "Exporting & Cleaning Accubid Data", "domain": "Software", "kw": ["exporting accubid", "cleaning accubid"]},
    "SK-119": {"name": "Job Plan Analysis", "domain": "Software", "kw": ["job plan analysis"]},
    "SK-120": {"name": "Maintaining Job Plans", "domain": "Software", "kw": ["maintaining job plan"]},
    "SK-121": {"name": "Accessing Pending Change Orders", "domain": "Software", "kw": ["pending change order"]},
    "SK-122": {"name": "ProCore Job Setup", "domain": "Software", "kw": ["procore job setup"]},
    "SK-123": {"name": "ViewPoint Change Orders", "domain": "Software", "kw": ["viewpoint", "change order"]},
}

def detect_series(slug, title):
    tl = title.lower().replace("&amp;", "&").replace("&#34;", '"').replace("&#39;", "'")
    sl = slug.lower()

    if "values driven leadership" in tl or "values-driven-leadership" in sl or "coach-k" in sl:
        return "VDL"
    if "critical leadership" in tl:
        return "CLT"
    if "extreme ownership" in tl and "chapter" in tl:
        return "CLT"
    if "leadership law" in tl:
        return "CLT"
    if "leadership" in tl and "decision" in tl and "pressure" in tl:
        return "CLT"
    if "introduction to field leadership" in tl or "field leadership" in tl:
        return "IFL"
    if "lockout" in tl or "tagout" in tl:
        return "LOTO"
    if "de-energized" in tl or "de energized" in tl:
        return "LOTO"
    if "return to service" in tl:
        return "LOTO"
    if "fall protection" in tl or "ladder" in tl or "scaffold" in tl or "edges" in tl or "slips, trips" in tl:
        return "FP"
    if "lean" in tl or "eight wastes" in tl or "8 wastes" in tl:
        return "LEAN"
    if "what is" in tl and '"lean"' in tl:
        return "LEAN"
    if "productivity" in tl and ("construction" in tl or "chapter" in sl):
        return "LEAN"
    if "minimizing waste" in tl or "identifying waste" in tl:
        return "LEAN"
    if "pull planning" in tl or "sticky note" in tl:
        return "LEAN"
    if "empowerment of field" in tl:
        return "LEAN"
    if "training the industry" in tl or "reshaping the industry" in tl:
        return "LEAN"
    if "adoption" in tl and "production" in tl:
        return "LEAN"
    if "processes need to change" in tl:
        return "LEAN"
    if "brief history" in tl and "chapter" in tl:
        return "LEAN"
    if "what you need to know" in tl and "chapter 02" in tl:
        return "LEAN"
    if "safety orientation" in tl or "new hire" in tl or "zero broken lives" in tl:
        return "SO"
    if "safety coordinator" in tl:
        return "SC"
    if "foreman" in tl or "roles and responsib" in tl:
        return "FTM"
    if "hazard communication" in tl or "hazcom" in tl or "container label" in tl or "precautionary" in tl or "safety data sheet" in tl or "written hazard" in tl or "chemical hazard" in tl or "types of chemical" in tl:
        return "HAZCOM"
    if "confined space" in tl or "attendant" in tl:
        return "CS"
    if "arc flash" in tl or "nfpa 70" in tl or "energized work" in tl or "electrical" in tl or "approach boundary" in tl:
        return "ES"
    if "emergency" in tl or "first aid" in tl or "incident investigation" in tl or "accident" in tl and "investigation" in tl or "injury" in tl and "management" in tl:
        return "ER"
    if "emotional intelligence" in tl or "self-regulation" in tl or "empathy" in tl or "social skill" in tl:
        return "EQ"
    if "self-awareness" in tl or "improving self" in tl:
        return "EQ"
    if "accubid" in tl or "sort code" in tl:
        return "ACC"
    if "procore" in tl or "viewpoint" in tl or "change order" in tl:
        return "PC"
    if "presenting" in tl or "art of present" in tl:
        return "AOP"
    if "effective communication" in tl and "introduction" in tl:
        return "COMM"
    if "team morale" in tl or "team management" in tl:
        return "TEAM"
    if "motivat" in tl and "team" in tl:
        return "TEAM"
    if "self-motivation" in tl or "increasing" in tl and "motivation" in tl:
        return "TEAM"
    if "delegation" in tl or "project structure" in tl:
        return "IFL"
    if "performance review" in tl or "corrective counseling" in tl or "performance management" in tl:
        return "PERF"
    if "sub-contractor" in tl or "subcontractor" in tl:
        return "IFL"
    if "job plan theory" in tl:
        return "IFL"
    if "jobsite efficiency" in tl:
        return "IFL"
    if "coordinating with other trades" in tl:
        return "IFL"
    if "document management" in tl:
        return "IFL"
    if "quality control" in tl:
        return "IFL"
    if "manpower projection" in tl:
        return "IFL"
    if "documentation and reporting" in tl:
        return "IFL"
    if "time management" in tl:
        return "IFL"
    if "using tool and technology" in tl:
        return "IFL"
    if "building an effective team" in tl:
        return "IFL"
    if "new manager" in tl:
        return "IFL"
    if "eap" in tl or "mental health" in tl:
        return "IFL"
    if "osha" in tl and "focus four" in tl:
        return "SAFE"
    if "workplace inspection" in tl or "pre-task" in tl:
        return "SAFE"
    if "on-site productivity" in tl:
        return "LEAN"
    if "recruit" in tl and "retain" in tl:
        return "VDL"
    if "continuous improvement" in tl:
        return "LEAN"
    if "project planning" in tl:
        return "IFL"
    if "safety management" in tl:
        return "IFL"
    # Catch remaining CLT chapters by title pattern
    if re.match(r"chapter \d+", tl) and ("leader" in tl or "human interaction" in tl):
        return "CLT"
    if "conclusion" in tl and "leadership" in tl and "most important" in tl:
        return "CLT"
    # Remaining chapter-titled courses
    if "avoiding common time wasters" in tl:
        return "IFL"
    if "construction vs" in tl and "manufacturing" in tl:
        return "LEAN"
    if "t.r.a.c.k" in tl or "controlling hazards" in tl:
        return "SAFE"
    if "testing" in tl and "troubleshooting" in tl and "precaution" in tl:
        return "ES"

    return "UNCLASSIFIED"

def match_skills(title, description, text_snippets):
    """Match course content to S5 skills based on keyword matching."""
    content = (title + " " + description + " " + " ".join(text_snippets)).lower()
    content = content.replace("&amp;", "&").replace("&#34;", '"').replace("&#39;", "'")

    matches = []
    for sk_id, sk in S5_SKILLS.items():
        score = 0
        for kw in sk["kw"]:
            if kw in content:
                score += 1
                # Title match is stronger
                if kw in title.lower():
                    score += 2
        if score > 0:
            matches.append((sk_id, sk["name"], score))

    # Sort by score descending, take top 5
    matches.sort(key=lambda x: -x[2])
    return matches[:5]

def classify_type(cd, title):
    """Classify as INTRO or SKILLS based on content analysis."""
    tl = title.lower()
    has_quiz = cd.get("has_quiz", False)
    has_kc = cd.get("has_knowledge_check", False)
    lessons = cd.get("lesson_count", 0)
    has_interactive = cd.get("has_interactive", False)

    # Strong INTRO signals
    if "introduction" in tl and "chapter 0" in tl:
        return "INTRO"
    if "chapter 0" in tl and not has_quiz and not has_kc:
        return "INTRO"

    # Strong SKILLS signals
    if has_quiz:
        return "SKILLS"
    if has_kc:
        return "SKILLS"
    if lessons >= 3:
        return "SKILLS"

    # Default bias toward SKILLS (per spec)
    return "SKILLS"

# Process all courses
registry = []
title_groups = defaultdict(list)

for c in courses:
    cd = c.get("course_data", {})
    title = cd.get("title") or c.get("manifest_title") or c["slug"]
    title_clean = re.sub(r'\s+', ' ', title.replace("&amp;", "&").replace("&#34;", '"').replace("&#39;", "'")).strip()

    series = detect_series(c["slug"], title)
    course_type = classify_type(cd, title)
    description = cd.get("description", "")
    text_snippets = cd.get("text_snippets", [])
    skills = match_skills(title, description, text_snippets)

    entry = {
        "slug": c["slug"],
        "title": title_clean,
        "series": series,
        "course_type": course_type,
        "is_uuid": c["is_uuid"],
        "has_locale": c["has_locale"],
        "lessons": cd.get("lesson_count", 0),
        "has_quiz": cd.get("has_quiz", False),
        "has_kc": cd.get("has_knowledge_check", False),
        "has_video": cd.get("has_video", False),
        "skills": [(s[0], s[1]) for s in skills],
        "description": description[:200],
    }
    registry.append(entry)
    title_groups[title_clean].append(entry)

# Detect duplicates
duplicates = {t: entries for t, entries in title_groups.items() if len(entries) > 1}

# Pick canonical slug per duplicate group: prefer descriptive > UUID, locale > no-locale
canonical_slugs = set()
dup_alternates = set()
for title, entries in title_groups.items():
    if len(entries) == 1:
        canonical_slugs.add(entries[0]["slug"])
    else:
        # Score each entry: +2 for locale, +1 for descriptive (non-UUID), -1 for " (2)" suffix
        def dup_score(e):
            s = 0
            if e["has_locale"]:
                s += 2
            if not e["is_uuid"]:
                s += 1
            if "(2)" in e["slug"]:
                s -= 1
            return s
        ranked = sorted(entries, key=lambda e: -dup_score(e))
        canonical_slugs.add(ranked[0]["slug"])
        for alt in ranked[1:]:
            dup_alternates.add(alt["slug"])

# Build deduplicated registry (canonical only)
deduped_registry = [e for e in registry if e["slug"] in canonical_slugs]

# Filter out junk entries (TEST, untitled) and "Copy of" Rise 360 editing copies
junk_titles = {"TEST", "untitled-scorm12-xrofbisj"}
deduped_registry = [e for e in deduped_registry if e["title"] not in junk_titles]
deduped_registry = [e for e in deduped_registry if not e["title"].startswith("Copy of ")]

# Assign codes
series_counters = defaultdict(int)
code_map = {}

# Sort by series then title for stable numbering
deduped_registry.sort(key=lambda x: (x["series"], x["title"]))

for entry in deduped_registry:
    series = entry["series"]
    if series == "UNCLASSIFIED":
        code = f"UNC-{series_counters[series]:02d}"
    else:
        code = f"{series}-{series_counters[series]:02d}"
    series_counters[series] += 1
    entry["code"] = code
    code_map[entry["slug"]] = code

# Write CODE_REGISTRY.csv (deduplicated, canonical slugs only)
reg_path = os.path.join(output_dir, "CODE_REGISTRY.csv")
with open(reg_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Slug", "Code", "Title", "Series", "Type", "UUID", "Locale", "Lessons", "Quiz", "KC", "Skills"])
    for entry in deduped_registry:
        skills_str = ", ".join(f"{s[0]}" for s in entry["skills"])
        w.writerow([
            entry["slug"],
            entry["code"],
            entry["title"],
            entry["series"],
            entry["course_type"],
            "Y" if entry["is_uuid"] else "",
            "Y" if entry["has_locale"] else "",
            entry["lessons"],
            "Y" if entry["has_quiz"] else "",
            "Y" if entry["has_kc"] else "",
            skills_str,
        ])

# Write full crosswalk
xwalk_path = os.path.join(output_dir, "skill_course_crosswalk_full.csv")
with open(xwalk_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Skill ID", "Skill Name", "Course Slug", "Code", "Series", "Course Type", "Awarded Level", "Confidence"])
    for entry in deduped_registry:
        for i, (sk_id, sk_name) in enumerate(entry["skills"]):
            # First skill match = primary (Working for SKILLS, Learning for INTRO)
            if entry["course_type"] == "INTRO":
                level = "Learning"
            else:
                level = "Working" if i < 2 else "Learning"
            conf = "B" if entry["has_locale"] else "C"
            if entry["has_kc"] or entry["has_quiz"]:
                conf = "A" if i < 2 else "B"
            w.writerow([sk_id, sk_name, entry["slug"], entry["code"], entry["series"], entry["course_type"], level, conf])

# Write duplicates report
dup_path = os.path.join(output_dir, "_DUPLICATES.md")
with open(dup_path, "w", encoding="utf-8") as f:
    f.write("---\nCreated: 2026-05-21\nLast updated: 2026-05-21\n")
    f.write("Source: Job 01 Full Run — duplicate detection\n")
    f.write("Context: Courses with identical titles from different SCORM packages\n")
    f.write("Status: Needs manual review — decide which slug is canonical\n---\n\n")
    f.write(f"# Duplicate Courses ({len(duplicates)} groups)\n\n")
    for title, entries in sorted(duplicates.items()):
        f.write(f"## {title}\n")
        for e in entries:
            uuid_tag = " [UUID]" if e["is_uuid"] else ""
            locale_tag = " [no-locale]" if not e["has_locale"] else ""
            f.write(f"- `{e['slug']}`{uuid_tag}{locale_tag}\n")
        f.write("\n")

# Summary stats
print(f"=== FULL RUN RESULTS ===")
print(f"Total SCORM packages: {len(registry)}")
print(f"Duplicate groups: {len(duplicates)}")
print(f"Duplicate alternates removed: {len(dup_alternates)}")
print(f"Junk entries removed: {len([e for e in registry if e.get('title') in junk_titles])}")
print(f"Canonical courses (CODE_REGISTRY): {len(deduped_registry)}")
print()

series_summary = defaultdict(int)
for entry in deduped_registry:
    series_summary[entry["series"]] += 1

print("Series breakdown (deduplicated):")
for s in sorted(series_summary.keys()):
    print(f"  {s}: {series_summary[s]}")

unclassified = series_summary.get("UNCLASSIFIED", 0)
print(f"\nUnclassified: {unclassified}")

# Skill coverage
skills_touched = set()
for entry in deduped_registry:
    for sk_id, _ in entry["skills"]:
        skills_touched.add(sk_id)
print(f"S5 Skills touched: {len(skills_touched)} of 124 ({len(skills_touched)*100//124}%)")

print(f"\nFiles written:")
print(f"  {reg_path}")
print(f"  {xwalk_path}")
print(f"  {dup_path}")

if __name__ == "__main__":
    pass
