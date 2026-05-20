"""
Automated SCORM Taxonomy Recommendation Generator
Processes remaining batches (4-13) using rule-based classification.
Generates recommendations following the approved Batch 1 pattern.
"""
import json, os, sys, re, zipfile
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DATA_DIR = r'C:\Users\tewing\OneDrive - GSL Electric\Projects\GSL-Operations-Framework\data'
SCORM_DIR = r'C:\Users\tewing\OneDrive - GSL Electric\Projects\training-template\reference\scorm'
RECS_PATH = os.path.join(DATA_DIR, 'scorm_taxonomy_recommendations.json')
INDEX_PATH = os.path.join(DATA_DIR, 'scorm_course_index.json')
VOCAB_PATH = os.path.join(DATA_DIR, 'learn365_vocabulary_snapshot.json')

# Load vocab for validation
with open(VOCAB_PATH, 'r', encoding='utf-8') as f:
    vocab = json.load(f)
VALID_CATEGORIES = {c['name']: c.get('parent') for c in vocab['course_categories']}
VALID_SKILLS = {s['title'] for s in vocab['skills']}
VALID_TAGS = set(vocab['tags'])

LN = "[LEVEL NEEDED -- {ss} scale set has no levels defined]"

# ========== SERIES DETECTION ==========
LEAN_ASSET = '0IZGQVI8ZscpLKGc.jpg'
NBIC_ASSET = 'NBIC_logo_light_bulb.png'
FL_ASSET = 'B-g2BCSZRrFMVZRd.png'
JP_ASSET = 'evaPDKMMXxF_4kgW.png'

LEAN_KEYWORDS = ['lean', 'waste', 'pull planning', 'sticky note', 'continuous improvement',
                 'production theory', 'reshaping', 'training the industry', 'minimizing waste',
                 'empowerment of field', 'identifying waste']
SAFETY_KEYWORDS = ['safety', 'nfpa', 'arc flash', 'lockout', 'tagout', 'loto', 'fall protection',
                   'confined space', 'hazard', 'ppe', 'slips', 'trips', 'falls', 'scaffold',
                   'ladder', 'first aid', 'cpr', 'aed', 'osha', 'msha', 'assured grounding',
                   'injury', 'shock', 'approach boundary', 'energized work', 'ghs',
                   'zero broken lives', 'orientation']
EQ_KEYWORDS = ['emotional intelligence', 'eq?', 'self-regulation', 'self-awareness',
               'empathy', 'social skills', 'self-motivation', 'boosting self']
VDL_KEYWORDS = ['values-driven', 'values driven', 'coach k']
ESTIMATING_KEYWORDS = ['accubid', 'estimating', 'trimble', 'takeoff']
SOFTWARE_KEYWORDS = ['viewpoint', 'vista', 'procore', 'excel', 'outlook', 'teams']

def detect_series(title, assets):
    """Detect which course series a course belongs to."""
    t = title.lower()
    asset_set = set(a.lower() for a in assets)

    # Check assets first for high-confidence series membership
    if LEAN_ASSET.lower() in asset_set:
        return 'lean'
    if NBIC_ASSET.lower() in asset_set:
        return 'critical_leadership'
    if FL_ASSET.lower() in asset_set and JP_ASSET.lower() not in asset_set:
        return 'field_leadership'
    if JP_ASSET.lower() in asset_set:
        return 'job_plan'

    # Check EQ by VTT filenames or title keywords
    for kw in EQ_KEYWORDS:
        if kw in t:
            return 'eq'
    # Check VDL
    for kw in VDL_KEYWORDS:
        if kw in t:
            return 'vdl'
    # Check by title number pattern (e.g., "1.0 Coach K", "11.1 Recruit")
    if re.match(r'^\d+\.\d+\s', title):
        return 'vdl'

    # Content-based detection
    for kw in LEAN_KEYWORDS:
        if kw in t:
            return 'lean'
    for kw in SAFETY_KEYWORDS:
        if kw in t:
            return 'safety'
    for kw in ESTIMATING_KEYWORDS:
        if kw in t:
            return 'estimating'
    for kw in SOFTWARE_KEYWORDS:
        if kw in t:
            return 'software'

    # Leadership/management keywords
    if any(kw in t for kw in ['leadership', 'leader', 'management', 'manager',
                               'delegation', 'extreme ownership', 'cover and move',
                               'keep it simple', 'prioritize and execute', 'decentralize',
                               'decision-making']):
        return 'leadership'
    if any(kw in t for kw in ['team', 'morale', 'motivation', 'communication',
                               'coordination', 'documentation', 'reporting']):
        return 'field_leadership'
    if any(kw in t for kw in ['performance review', 'counseling', 'corrective']):
        return 'performance_mgmt'
    if any(kw in t for kw in ['quality control', 'quality']):
        return 'quality'
    if any(kw in t for kw in ['project planning', 'job plan', 'jobsite efficiency',
                               'closeout', 'manpower']):
        return 'project_planning'
    if any(kw in t for kw in ['policy', 'fmla', 'harassment', 'discrimination',
                               'employee assistance', 'eap', 'mental health',
                               'employee rights']):
        return 'policy'

    return 'unknown'


# ========== TAXONOMY MAPPING ==========
SERIES_MAP = {
    'lean': {
        'category_default': 'Lean Principals > Lean Fundamentals',
        'skill_default': 'Lean Fundamentals',
        'skill_category': 'Lean Principles',
        'scale_set': 'Lean Principles',
        'difficulty_default': 'Foundational',
        'tag_defaults': ['Lean', 'Lean Construction'],
        'roles_default': ['Foreman', 'Superintendent'],
        'scope': 'Role-scoped'
    },
    'critical_leadership': {
        'category_default': 'Leadership > Leadership Fundamentals',
        'skill_default': 'Leadership',
        'skill_category': 'Leadership',
        'scale_set': 'Leadership',
        'difficulty_default': 'Foundational',
        'tag_defaults': ['Leadership', 'Leadership Basics'],
        'roles_default': ['Apprentice', 'Journeyman', 'Leadman', 'Foreman', 'Superintendent'],
        'scope': 'Global'
    },
    'field_leadership': {
        'category_default': 'Leadership > Skills, Traits, & Responsibilities',
        'skill_default': 'Field Supervision',
        'skill_category': 'Leadership',
        'scale_set': 'Leadership',
        'difficulty_default': 'Foundational',
        'tag_defaults': ['Field Leadership'],
        'roles_default': ['Leadman', 'Foreman', 'Superintendent'],
        'scope': 'Role-scoped'
    },
    'job_plan': {
        'category_default': 'Leadership > Project Planning & Scheduling',
        'skill_default': 'Creating Job Plans',
        'skill_category': 'Leadership',
        'scale_set': 'Leadership',
        'difficulty_default': 'Foundational',
        'tag_defaults': ['job plan', 'Planning'],
        'roles_default': ['Foreman', 'Superintendent'],
        'scope': 'Role-scoped'
    },
    'eq': {
        'category_default': 'Soft Skills > Emotional Intelligence',
        'skill_default': 'EQ Fundamentals',
        'skill_category': 'Emotional Intelligence',
        'scale_set': 'Emotional Intelligence',
        'difficulty_default': 'Foundational',
        'tag_defaults': ['Emotional Intelligence'],
        'roles_default': ['Apprentice', 'Journeyman', 'Leadman', 'Foreman', 'Superintendent'],
        'scope': 'Global'
    },
    'vdl': {
        'category_default': 'Leadership > Leadership Fundamentals',
        'skill_default': 'Values-Driven Leadership',
        'skill_category': 'Leadership',
        'scale_set': 'Leadership',
        'difficulty_default': 'Foundational',
        'tag_defaults': ['Values-Driven', 'Leadership'],
        'roles_default': ['Leadman', 'Foreman', 'Superintendent'],
        'scope': 'Role-scoped'
    },
    'safety': {
        'category_default': 'Safety',
        'skill_default': 'Personal Safety',
        'skill_category': 'Safety',
        'scale_set': 'Safety',
        'difficulty_default': 'Foundational',
        'tag_defaults': ['Safety'],
        'roles_default': ['Apprentice', 'Journeyman', 'Leadman', 'Foreman', 'Superintendent'],
        'scope': 'Global'
    },
    'estimating': {
        'category_default': 'Estimating',
        'skill_default': 'Estimating',
        'skill_category': 'Estimating',
        'scale_set': 'Estimating',
        'difficulty_default': 'Intermediate',
        'tag_defaults': ['Estimating'],
        'roles_default': ['Project Manager'],
        'scope': 'Role-scoped'
    },
    'software': {
        'category_default': 'Technology Skills',
        'skill_default': 'Documentation Practices',
        'skill_category': 'Technology',
        'scale_set': 'Technology',
        'difficulty_default': 'Foundational',
        'tag_defaults': ['software'],
        'roles_default': ['Foreman', 'Superintendent', 'Project Manager'],
        'scope': 'Role-scoped'
    },
    'leadership': {
        'category_default': 'Leadership > Leadership Fundamentals',
        'skill_default': 'Leadership',
        'skill_category': 'Leadership',
        'scale_set': 'Leadership',
        'difficulty_default': 'Foundational',
        'tag_defaults': ['Leadership'],
        'roles_default': ['Leadman', 'Foreman', 'Superintendent'],
        'scope': 'Role-scoped'
    },
    'performance_mgmt': {
        'category_default': 'Leadership > Performance',
        'skill_default': 'Performance Reviews',
        'skill_category': 'Performance Management',
        'scale_set': 'Performance Management',
        'difficulty_default': 'Foundational',
        'tag_defaults': ['performance', 'Feedback'],
        'roles_default': ['Foreman', 'Superintendent', 'Project Manager'],
        'scope': 'Role-scoped'
    },
    'quality': {
        'category_default': 'Leadership > Skills, Traits, & Responsibilities',
        'skill_default': 'Field Supervision',
        'skill_category': 'Leadership',
        'scale_set': 'Leadership',
        'difficulty_default': 'Foundational',
        'tag_defaults': ['Quality Check'],
        'roles_default': ['Foreman', 'Superintendent'],
        'scope': 'Role-scoped'
    },
    'project_planning': {
        'category_default': 'Leadership > Project Planning & Scheduling',
        'skill_default': 'Project Planning',
        'skill_category': 'Leadership',
        'scale_set': 'Leadership',
        'difficulty_default': 'Foundational',
        'tag_defaults': ['Planning', 'project planning'],
        'roles_default': ['Foreman', 'Superintendent'],
        'scope': 'Role-scoped'
    },
    'policy': {
        'category_default': 'Policy',
        'skill_default': 'Safety Responsibility',
        'skill_category': 'Policy',
        'scale_set': 'Policy',
        'difficulty_default': 'Foundational',
        'tag_defaults': ['policy', 'compliance'],
        'roles_default': ['Apprentice', 'Journeyman', 'Leadman', 'Foreman', 'Superintendent'],
        'scope': 'Global'
    },
    'unknown': {
        'category_default': '[UNKNOWN -- needs investigation]',
        'skill_default': None,
        'skill_category': None,
        'scale_set': None,
        'difficulty_default': '[UNKNOWN]',
        'tag_defaults': [],
        'roles_default': [],
        'scope': 'Unknown'
    }
}

# Specific skill overrides based on title keywords
SKILL_OVERRIDES = {
    'extreme ownership': 'Extreme Ownership',
    'cover and move': 'Leadership',
    'keep it simple': 'Leadership',
    'prioritize and execute': 'Leadership',
    'decentralize command': 'Leadership',
    'pull planning': 'Pull Planning',
    'sticky note': 'Pull Planning',
    'continuous improvement': 'Continuous Improvement',
    'waste': 'Eliminate Waste',
    'identifying waste': 'Eight Wastes Recognition',
    'eight wastes': 'Eight Wastes Recognition',
    'empowerment of field': 'Field Team Empowerment',
    'time management': 'Time Management',
    'time wasters': 'Time Management',
    'team morale': 'Team Motivation Fundamentals',
    'morale': 'Team Motivation Fundamentals',
    'communication': 'Effective Communication',
    'effective communication': 'Effective Communication',
    'documentation': 'Documentation & Reporting',
    'reporting': 'Documentation & Reporting',
    'manpower': 'Manpower Projection',
    'quality control': 'Field Supervision',
    'team management': 'Project Team Leadership',
    'job plan': 'Creating Job Plans',
    'jobsite efficiency': 'Productivity Execution',
    'closeout': 'Project Planning',
    'performance review': 'Performance Reviews',
    'corrective counseling': 'Corrective Counseling',
    'counseling': 'Corrective Counseling',
    'self-regulation': 'Self-Regulation',
    'self-awareness': 'EQ Fundamentals',
    'empathy': 'Empathy',
    'social skills': 'Social Skills',
    'self-motivation': 'EQ Leadership',
    'lockout': 'LOTO Fundamentals',
    'complex lockout': 'Complex LOTO Procedures',
    'fall protection': 'Fall Hazard Recognition',
    'scaffold': 'Scaffold Fundamentals',
    'ladder': 'Ladder Safety',
    'confined space': 'Confined Space Program',
    'hazard communication': 'Chemical Hazard Identification',
    'ghs': 'Chemical Hazard Identification',
    'container label': 'Container Label Use',
    'approach boundary': 'Approach Boundary Management',
    'arc flash': 'Arc Flash Awareness',
    'assured grounding': 'Electrical Safety Fundamentals',
    'shock': 'Electrical Risk Assessment',
    'energized work': 'Energized Work Practices',
    'viewpoint change order': 'ViewPoint Change Orders',
    'viewpoint': 'ViewPoint Change Orders',
    'accubid': 'Estimating',
    'procore': 'ProCore Job Setup',
    'recruit': 'Values-Driven Leadership',
    'retain': 'Values-Driven Leadership',
    'delegation': 'Delegation & Empowerment',
    'project structure': 'Project Planning & Execution',
    'anatomy of a project': 'Project Planning',
    'construction vs': 'Lean Fundamentals',
    'new manager': 'Leadership',
    'document management': 'Documentation Practices',
    'coordinating with other': 'Trade Coordination',
    'safety management': 'Safety Responsibility',
    'first aid': 'First / CPR/ AED',
    'fmla': 'Safety Responsibility',
    'harassment': 'Safety Responsibility',
    'eap': 'Safety Responsibility',
    'mental health': 'Safety Responsibility',
    'new hire': 'Safety Responsibility',
    'orientation': 'Safety Responsibility',
    'slips': 'Personal Safety',
    'trips': 'Personal Safety',
    'decision-making': 'Strategic Thinking',
    'tool and technology': 'Tool & Equipment Management',
    'leadership essentials': 'Leadership',
    'leadership spectrum': 'Leadership',
    'values': 'Values-Driven Leadership',
    'improve individual': 'Values-Driven Leadership',
    'develop emerging': 'Values-Driven Leadership',
    'planning your next': 'Values-Driven Leadership',
    'electrical risk': 'Electrical Risk Assessment',
    'risk assessment': 'Electrical Risk Assessment',
    'inspections': 'Regulatory Inspections',
    'employee rights': 'Nevada Employee Rights',
    'injury management': 'Injury Management',
}

CATEGORY_OVERRIDES = {
    'extreme ownership': 'Leadership > Extreme Ownership',
    'pull planning': 'Lean Principals > Pull Planning',
    'sticky note': 'Lean Principals > Pull Planning',
    'continuous improvement': 'Lean Principals > Continuous Improvement',
    'waste': 'Lean Principals > Waste Management',
    'empowerment of field': 'Lean Principals > Respect For People',
    'self-regulation': 'Soft Skills > Self-Regulation',
    'self-awareness': 'Soft Skills > Self-Awareness',
    'empathy': 'Soft Skills > Empathy',
    'social skills': 'Soft Skills > Social Skills',
    'self-motivation': 'Soft Skills > Motivation',
    'communication': 'Soft Skills > Communication',
    'lockout': 'Safety > Lockout / Tagout',
    'complex lockout': 'Safety > Lockout / Tagout',
    'fall protection': 'Safety > Slips, Trips, & Falls',
    'scaffold': 'Safety',
    'ladder': 'Safety',
    'confined space': 'Safety',
    'hazard communication': 'Safety > Hazard Communication',
    'ghs': 'Safety > Hazard Communication',
    'container label': 'Safety > Hazard Communication',
    'arc flash': 'Safety > Electrical Safety',
    'approach boundary': 'Safety > Electrical Safety',
    'shock': 'Safety > Electrical Safety',
    'electrical': 'Safety > Electrical Safety',
    'energized work': 'Safety > Electrical Safety',
    'assured grounding': 'Safety > Electrical Safety',
    'first aid': 'Safety > First Aid / CPR / AED',
    'viewpoint': 'Project Management > Change Orders',
    'accubid': 'Estimating > Accubid',
    'procore': 'Technology Skills',
    'document management': 'Leadership > Document Control',
    'delegation': 'Leadership > Delegation',
    'performance review': 'Leadership > Performance',
    'counseling': 'Leadership > Performance',
    'team management': 'Team Building & Teamwork',
    'quality control': 'Leadership > Skills, Traits, & Responsibilities',
    'manpower': 'Leadership > Resource Planning',
    'coordinating with other': 'Leadership > Skills, Traits, & Responsibilities',
    'safety management': 'Safety',
    'fmla': 'Policy',
    'harassment': 'Policy',
    'eap': 'General Personal Development',
    'mental health': 'General Personal Development',
    'orientation': 'Employee Orientation',
    'new hire': 'Employee Orientation',
    'tool and technology': 'Leadership > Tools & Technology',
    'inspections': 'OSHA & MSHA Inspections',
    'employee rights': 'Policy',
    'risk assessment': 'Risk Assessment',
    'slips': 'Safety > Slips, Trips, & Falls',
    'industry transformation': 'Lean Principals > Industry Transformation',
    'training the industry': 'Lean Principals > Industry Transformation',
    'reshaping': 'Lean Principals > Industry Transformation',
    'process management': 'Lean Principals > Process Management',
}

DIFFICULTY_OVERRIDES = {
    'advanced': 'Advanced',
    'complex lockout': 'Intermediate',
    'nfpa': 'Intermediate',
    'approach boundary': 'Intermediate',
    'arc flash': 'Intermediate',
    'pull planning': 'Intermediate',
    'sticky note': 'Intermediate',
    'continuous improvement': 'Intermediate',
    'waste at a project': 'Intermediate',
    'identifying waste': 'Intermediate',
    'empowerment of field': 'Intermediate',
    'extreme ownership': 'Intermediate',
    'manpower': 'Intermediate',
    'risk assessment': 'Intermediate',
}


def get_override(title, overrides):
    """Find the best matching override for a title."""
    t = title.lower()
    best_match = None
    best_len = 0
    for kw, val in overrides.items():
        if kw in t and len(kw) > best_len:
            best_match = val
            best_len = len(kw)
    return best_match


def extract_course_data(zf_path):
    """Extract assets and VTT from a SCORM package."""
    result = {'vtt': [], 'videos': [], 'assets': [], 'format': 'rise360'}
    try:
        with zipfile.ZipFile(zf_path, 'r') as zf:
            names = zf.namelist()
            result['format'] = 'rise360' if any('lib/rise/' in n for n in names) else 'generic'
            result['videos'] = [os.path.basename(n) for n in names
                               if any(n.lower().endswith(e) for e in ['.mp4', '.webm'])]
            result['assets'] = [os.path.basename(n) for n in names
                               if any(n.lower().endswith(e) for e in ['.jpg', '.png', '.pdf'])
                               and 'lib/' not in n and 'scormdriver' not in n][:12]
            # Extract VTT text
            vtt_files = [n for n in names if n.lower().endswith('.vtt')]
            seen_text = set()
            for vf in vtt_files:
                with zf.open(vf) as f:
                    raw = f.read().decode('utf-8', errors='ignore').replace('\ufeff', '')
                    lines = raw.split('\n')
                    texts = []
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('WEBVTT') and not line.startswith('NOTE') \
                           and '-->' not in line and not re.match(r'^\d+$', line):
                            clean = re.sub(r'<[^>]+>', '', line).strip()
                            if clean:
                                texts.append(clean)
                    text = ' '.join(texts)
                    # Deduplicate
                    sig = text[:200]
                    if sig not in seen_text and len(text) > 50:
                        seen_text.add(sig)
                        result['vtt'].append({'file': vf, 'text': text[:3000]})
    except Exception as e:
        result['error'] = str(e)
    return result


def generate_recommendation(course_info, extracted):
    """Generate a taxonomy recommendation record for a course."""
    title = course_info['title']
    series = detect_series(title, extracted.get('assets', []))
    smap = SERIES_MAP[series]

    # Get overrides
    skill = get_override(title, SKILL_OVERRIDES) or smap['skill_default']
    category = get_override(title, CATEGORY_OVERRIDES) or smap['category_default']
    difficulty = get_override(title, DIFFICULTY_OVERRIDES) or smap['difficulty_default']

    # Validate skill exists
    if skill and skill not in VALID_SKILLS:
        skill = smap['skill_default']

    has_vtt = len(extracted.get('vtt', [])) > 0
    has_video = len(extracted.get('videos', [])) > 0
    vid_count = len(extracted.get('videos', []))

    # Determine confidence
    if has_vtt:
        confidence = "HIGH -- full VTT transcript available."
    elif has_video and vid_count > 3:
        confidence = f"MEDIUM-HIGH -- {vid_count} descriptively named bundled videos, no VTT."
    elif has_video:
        confidence = f"MEDIUM -- {vid_count} bundled video(s), no VTT."
    elif title.startswith('[FROM FILENAME]') or title.startswith('[ERROR]'):
        confidence = "VERY LOW -- no manifest title, no transcript."
    else:
        confidence = "LOW -- no transcript or video. Description based on title and series context."

    # Media info
    if has_video:
        media = {"location": "bundled", "videos": extracted['videos'][:10]}
    else:
        media = {"location": "none", "videos": []}

    # Transcript info
    if has_vtt:
        vtt_sources = [v['file'] for v in extracted['vtt']]
        transcript = {"status": "found-in-package", "source": ' + '.join(vtt_sources),
                      "video_count": vid_count, "vtt_count": len(extracted['vtt'])}
    elif has_video:
        transcript = {"status": "needs-retrieval",
                      "source": f"{vid_count} bundled MP4(s) have no VTT",
                      "video_count": vid_count, "vtt_count": 0}
    else:
        transcript = {"status": "needs-retrieval",
                      "source": "No video or VTT in package",
                      "video_count": 0, "vtt_count": 0}

    # Content summary
    parts = [f"Course: {title}."]
    if series != 'unknown':
        series_name = series.replace('_', ' ').title()
        parts.append(f"Part of the {series_name} series.")
    if has_vtt:
        parts.append(f"Full VTT transcript available ({len(extracted['vtt'])} file(s)).")
    if has_video:
        vid_names = ', '.join(v[:40] for v in extracted['videos'][:5])
        parts.append(f"{vid_count} bundled video(s): {vid_names}.")
    if not has_vtt and not has_video:
        parts.append("Rise 360 text-based content, no video or transcript in package.")
    content_summary = ' '.join(parts)

    # Short description
    clean_title = re.sub(r'^(Chapter\s+\d+\s*[-:]?\s*|[\d.]+\s+)', '', title).strip()
    clean_title = re.sub(r'\s*[-:]\s*(Introduction to Field Leadership.*|Section\s*\d+.*)', '', clean_title).strip()
    if clean_title:
        short_desc = f"Learn about {clean_title.lower()} and how to apply these concepts in your role."
    else:
        short_desc = f"[NEEDS INVESTIGATION -- unable to generate description from title.]"

    # Long description
    if series == 'unknown' or title.startswith('[FROM FILENAME]'):
        long_desc = f"[NEEDS INVESTIGATION -- content unknown. Manual review required.]"
    else:
        series_name = series.replace('_', ' ').title()
        long_desc = (f"This course covers {clean_title.lower() if clean_title else title}. "
                    f"It is part of the {series_name} curriculum at GSL Academy.\n\n"
                    f"On completion, you earn the skill {skill}.\n\n"
                    f"This is a {difficulty}-level course.")

    # Build tags
    tags = []
    for t in smap['tag_defaults']:
        tags.append({"value": t, "label": "EXISTING"})
    # Add topic-specific tags from title keywords
    title_words = set(re.findall(r'\b\w+\b', title.lower()))
    tag_candidates = {
        'communication': 'Communication', 'delegation': 'Delegation',
        'ownership': 'Ownership', 'planning': 'Planning',
        'scheduling': 'Scheduling', 'safety': 'Safety',
        'coordination': 'coordination', 'documentation': 'Documentation',
        'motivation': 'Motivation', 'morale': 'morale',
        'productivity': 'productivity', 'efficiency': 'Efficiency',
    }
    added_tags = set(t['value'] for t in tags)
    for kw, tag in tag_candidates.items():
        if kw in title_words and tag not in added_tags:
            if tag in VALID_TAGS:
                tags.append({"value": tag, "label": "EXISTING"})
                added_tags.add(tag)
    tags.append({"value": f"Difficulty: {difficulty}", "label": "PROPOSED"})

    # Skills
    skills_awarded = []
    if skill:
        skills_awarded.append({
            "skill": skill,
            "skill_category": smap['skill_category'] or 'Unknown',
            "scale_set": smap['scale_set'] or 'Unknown',
            "level": LN.format(ss=smap['scale_set'] or 'Unknown'),
            "label": "EXISTING" if skill in VALID_SKILLS else "PROPOSED",
            "rationale": f"Mapped from course title and series context."
        })

    # Target roles
    target_roles = []
    if smap['roles_default']:
        target_roles.append({
            "fragment": f"Academy/{skill}/[level TBD]" if skill else "[TBD]",
            "roles": smap['roles_default'],
            "scope": smap['scope'],
            "note": f"Standard target for {series.replace('_', ' ')} series."
        })

    # Open questions
    open_questions = []
    if title.startswith('[FROM FILENAME]'):
        open_questions.append("No manifest title -- needs manual identification.")
    if course_info.get('is_guid_filename'):
        open_questions.append("GUID filename -- may be an older version.")

    # Topic timestamp index (only for VTT courses)
    topic_index = []
    if has_vtt:
        for vtt in extracted['vtt']:
            topic_index.append({
                "video": extracted['videos'][0] if extracted['videos'] else "[unknown]",
                "vtt": vtt['file'],
                "topic": f"Full content -- {title}",
                "timecode": "00:00:00.000"
            })

    return {
        "batch": course_info.get('batch'),
        "status": "done",
        "course": title,
        "source_file": course_info['file'],
        "content_summary": content_summary,
        "media": media,
        "transcript": transcript,
        "short_description": short_desc,
        "long_description": long_desc,
        "category": {
            "value": category,
            "label": "EXISTING" if not category.startswith('[') else "NEEDS-REVIEW",
            "rationale": f"Auto-classified from series={series} and title keywords."
        },
        "tags": tags,
        "skills_awarded": skills_awarded,
        "level_of_difficulty": {
            "value": difficulty,
            "rationale": f"Auto-classified based on title and series position."
        },
        "target_roles_draft": target_roles,
        "topic_timestamp_index": topic_index,
        "confidence": confidence,
        "open_questions": open_questions
    }


def process_batches(start_batch, end_batch):
    """Process a range of batches."""
    with open(RECS_PATH, 'r', encoding='utf-8') as f:
        recs = json.load(f)
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        idx = json.load(f)

    total_added = 0
    for batch_num in range(start_batch, end_batch + 1):
        courses = [c for c in idx['courses'] if c.get('batch') == batch_num and c['status'] != 'done']
        if not courses:
            print(f'Batch {batch_num}: already done or empty, skipping')
            continue

        print(f'\n=== Batch {batch_num}: {len(courses)} courses ===')
        batch_recs = []
        conf_counts = {}

        for c in courses:
            zf_path = os.path.join(SCORM_DIR, c['file'])
            extracted = extract_course_data(zf_path)
            rec = generate_recommendation(c, extracted)
            batch_recs.append(rec)

            # Track confidence
            level = rec['confidence'].split(' ')[0]
            conf_counts[level] = conf_counts.get(level, 0) + 1

            series = detect_series(c['title'], extracted.get('assets', []))
            skill = rec['skills_awarded'][0]['skill'] if rec['skills_awarded'] else 'NONE'
            print(f'  {c["title"][:50]:50s} -> {series:20s} {skill:30s} {rec["level_of_difficulty"]["value"]}')

        # Merge
        recs['courses'].extend(batch_recs)
        total_added += len(batch_recs)

        # Mark done in index
        for c in idx['courses']:
            if c.get('batch') == batch_num:
                c['status'] = 'done'

        # QC
        new_skills = sum(1 for r in batch_recs
                        if any(s['label'] != 'EXISTING' for s in r.get('skills_awarded', [])))
        unknown = sum(1 for r in batch_recs if r['category']['label'] == 'NEEDS-REVIEW')
        print(f'  QC: {conf_counts} | new_skills={new_skills} | unknown={unknown}')

    # Save
    recs['meta']['last_updated'] = '2026-05-20'
    recs['meta']['status'] = f'In Progress -- Batch {end_batch} complete'
    with open(RECS_PATH, 'w', encoding='utf-8') as f:
        json.dump(recs, f, indent=2, ensure_ascii=False)
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(idx, f, indent=2, ensure_ascii=False)

    print(f'\n=== TOTAL: {total_added} courses added across batches {start_batch}-{end_batch} ===')
    print(f'Total recommendations: {len(recs["courses"])}')


if __name__ == '__main__':
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    end = int(sys.argv[2]) if len(sys.argv) > 2 else 13
    process_batches(start, end)
