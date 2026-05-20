"""Generate SCORM Taxonomy Summary Report with Appendices A, B, C."""
import json, sys, os
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DATA_DIR = r'C:\Users\tewing\OneDrive - GSL Electric\Projects\GSL-Operations-Framework\data'
RECS_PATH = os.path.join(DATA_DIR, 'scorm_taxonomy_recommendations.json')
OUT_PATH = os.path.join(DATA_DIR, 'scorm_taxonomy_summary.md')

with open(RECS_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

courses = data['courses']
meta = data['meta']

# ── Helpers ──────────────────────────────────────────────────────────

def confidence_bucket(conf_str):
    if not conf_str:
        return 'UNKNOWN'
    c = conf_str.upper()
    if c.startswith('HIGH'):
        return 'HIGH'
    if c.startswith('MEDIUM-HIGH') or c.startswith('MEDIUM\u2014HIGH'):
        return 'MEDIUM-HIGH'
    if c.startswith('MEDIUM'):
        return 'MEDIUM'
    if c.startswith('LOW'):
        return 'LOW'
    if c.startswith('VERY LOW'):
        return 'VERY LOW'
    return 'UNKNOWN'

# ── Compute stats ────────────────────────────────────────────────────

total = len(courses)

# Confidence
conf_buckets = Counter(confidence_bucket(c.get('confidence', '')) for c in courses)

# Difficulty
diff_counts = Counter(c.get('level_of_difficulty', {}).get('value', 'Unknown') for c in courses)

# Categories
cat_counts = Counter(c['category']['value'] for c in courses)

# Skills
all_skills = []
skill_course_map = defaultdict(list)
for c in courses:
    for s in c.get('skills_awarded', []):
        all_skills.append(s['skill'])
        skill_course_map[s['skill']].append(c['course'])
skill_counts = Counter(all_skills)
unique_skills = len(skill_counts)

# Tags
existing_tags = set()
proposed_tags = set()
for c in courses:
    for t in c.get('tags', []):
        if t.get('label') == 'EXISTING':
            existing_tags.add(t['value'])
        elif t.get('label') == 'PROPOSED':
            proposed_tags.add(t['value'])

# Role matrix
role_skills = defaultdict(set)
role_courses = defaultdict(set)
for c in courses:
    skills_for_course = [s['skill'] for s in c.get('skills_awarded', [])]
    for t in c.get('target_roles_draft', []):
        for r in t.get('roles', []):
            role_skills[r].update(skills_for_course)
            role_courses[r].add(c['course'])

# NEEDS-REVIEW
needs_review = [c for c in courses if c.get('category', {}).get('label') == 'NEEDS-REVIEW']
no_skills = [c for c in courses if not c.get('skills_awarded')]

# Transcript gaps
transcript_gaps = []
for c in courses:
    t = c.get('transcript', {})
    conf = c.get('confidence', '')
    bucket = confidence_bucket(conf)
    has_vtt = t.get('status') == 'found-in-package'
    if not has_vtt:
        transcript_gaps.append({
            'course': c['course'],
            'confidence': bucket,
            'transcript_status': t.get('status', 'unknown'),
            'has_video': bool(c.get('media', {}).get('videos'))
        })

# Series detection
series_map = defaultdict(list)
for c in courses:
    title = c['course']
    if 'Values Driven Leadership' in title or 'Coach K' in title:
        series_map['Values-Driven Leadership (Coach K)'].append(title)
    elif 'Art of Presenting' in title:
        series_map['The Art of Presenting'].append(title)
    elif 'Critical Leadership' in title or 'What Makes A Leader' in title or 'Conclusion: Leadership' in title:
        series_map['Critical Leadership Training'].append(title)
    elif 'Emotional Intelligence' in title or 'EQ' in title.upper() or 'Leading With Emotion' in title:
        series_map['Emotional Intelligence (EQ)'].append(title)
    elif any(kw in title for kw in ['Lean', 'lean', 'Waste', 'Pull Planning', 'Sticky Note', 'Continuous Improvement', 'Productivity', 'Reshaping', 'Training the Industry']):
        series_map['Lean Construction'].append(title)
    elif 'Lockout' in title or 'LOTO' in title or 'De-Energized' in title or 'Return To Service' in title:
        series_map['Lockout/Tagout (LOTO)'].append(title)
    elif 'Introduction to Field Leadership' in title or 'Field Leadership' in title.replace('Section', ''):
        series_map['Introduction to Field Leadership'].append(title)
    elif 'Safety Coordinator' in title:
        series_map['Safety Coordinator Training'].append(title)
    elif 'Scaffold' in title:
        series_map['Scaffolding Safety'].append(title)
    elif 'NFPA 70E' in title or 'Electrical' in title or 'Arc Flash' in title:
        series_map['Electrical Safety / NFPA 70E'].append(title)
    elif 'Accubid' in title:
        series_map['Accubid Estimating'].append(title)
    elif 'Job Plan' in title or 'Jobsite Efficiency' in title:
        series_map['Job Planning'].append(title)

# Batches
batch_counts = Counter(c.get('batch', 0) for c in courses)

# ── Build report ─────────────────────────────────────────────────────

lines = []
def w(line=''):
    lines.append(line)

w('# SCORM Taxonomy Recommendations — Summary Report')
w()
w('| Field | Value |')
w('|-------|-------|')
w(f'| Created | {meta["created"]} |')
w(f'| Last Updated | {meta["last_updated"]} |')
w(f'| Status | {meta["status"]} |')
w(f'| Source | {meta["source"]} |')
w(f'| Vocabulary Ref | {meta["vocabulary_snapshot"]} |')
w()
w('---')
w()

# ── Section 1: Executive Summary ─────────────────────────────────────

w('## 1. Executive Summary')
w()
w(f'Processed **{total} unique SCORM courses** from the GSL Academy Learn365 catalog.')
w(f'Mapped to **{unique_skills} existing skills** across **{len(cat_counts)} categories**.')
w(f'Assigned to **{len(role_skills)} career-track roles**.')
w(f'**0 new skills proposed** — all mapped to the existing Learn365 vocabulary.')
w()
w(f'| Metric | Count |')
w(f'|--------|-------|')
w(f'| Total courses processed | {total} |')
w(f'| Unique skills mapped | {unique_skills} |')
w(f'| New skills proposed | 0 |')
w(f'| Categories used | {len(cat_counts)} |')
w(f'| Roles covered | {len(role_skills)} |')
w(f'| NEEDS-REVIEW remaining | {len(needs_review)} |')
w(f'| Courses with no skills | {len(no_skills)} |')
w(f'| Transcript gaps | {len(transcript_gaps)} |')
w()

# ── Section 2: Confidence Distribution ───────────────────────────────

w('## 2. Confidence Distribution')
w()
w('| Confidence | Count | % |')
w('|------------|-------|---|')
order = ['HIGH', 'MEDIUM-HIGH', 'MEDIUM', 'LOW', 'VERY LOW', 'UNKNOWN']
for bucket in order:
    count = conf_buckets.get(bucket, 0)
    if count > 0:
        pct = round(100 * count / total, 1)
        w(f'| {bucket} | {count} | {pct}% |')
w()
w('> HIGH = full VTT transcript available. MEDIUM-HIGH = multiple descriptively-named videos.')
w('> MEDIUM = bundled video(s) but no VTT. LOW = title-only inference. VERY LOW = no metadata.')
w()

# ── Section 3: Difficulty Distribution ───────────────────────────────

w('## 3. Difficulty Distribution')
w()
w('| Difficulty | Count | % |')
w('|------------|-------|---|')
diff_order = ['Foundational', 'Intermediate', 'Advanced', '[UNKNOWN]', '[N/A]']
for d in diff_order:
    count = diff_counts.get(d, 0)
    if count > 0:
        pct = round(100 * count / total, 1)
        w(f'| {d} | {count} | {pct}% |')
w()

# ── Section 4: Category Distribution ─────────────────────────────────

w('## 4. Category Distribution')
w()
w('| Category | Count |')
w('|----------|-------|')
for cat, count in cat_counts.most_common():
    w(f'| {cat} | {count} |')
w()

# ── Section 5: Skills Inventory ──────────────────────────────────────

w('## 5. Skills Inventory (55 skills)')
w()
w('All skills below are EXISTING in the Learn365 vocabulary. No new skills were proposed.')
w()
w('| Skill | Courses Using |')
w('|-------|--------------|')
for skill in sorted(skill_counts.keys()):
    w(f'| {skill} | {skill_counts[skill]} |')
w()

# ── Section 6: Series Detection ──────────────────────────────────────

w('## 6. Detected Course Series')
w()
for series_name in sorted(series_map.keys()):
    titles = series_map[series_name]
    w(f'### {series_name} ({len(titles)} courses)')
    for t in sorted(titles):
        w(f'- {t}')
    w()

# ── Section 7: NEEDS-REVIEW Items ────────────────────────────────────

w('## 7. NEEDS-REVIEW Items')
w()
if needs_review:
    for c in needs_review:
        w(f'- **{c["course"]}** — {c["category"].get("rationale", "No rationale")}')
else:
    w('No NEEDS-REVIEW items remaining (all resolved).')
w()
w(f'Courses with no skills assigned: {len(no_skills)}')
for c in no_skills:
    w(f'- {c["course"]}')
w()

# ── Section 8: Batch Processing Log ──────────────────────────────────

w('## 8. Batch Processing Log')
w()
w('| Batch | Courses | Method |')
w('|-------|---------|--------|')
for batch_num in sorted(batch_counts.keys()):
    count = batch_counts[batch_num]
    method = 'Hand-crafted' if batch_num <= 3 else 'Automated (rule-based)'
    w(f'| Batch {batch_num} | {count} | {method} |')
w()

# ── Section 9: Data Quality Notes ────────────────────────────────────

w('## 9. Data Quality Notes')
w()
w('### Tag Typos Found in Learn365 Vocabulary')
w('- ` lockout/tagout` — leading space')
w('- `Budgetting` — should be "Budgeting"')
w('- `Transparancy` — should be "Transparency"')
w('- `label,` — trailing comma')
w()
w('### Scale Set Issues')
w('- All 38 scale sets have **0 defined levels**')
w('- Every skill level is marked `[LEVEL NEEDED]` pending Admin Center configuration')
w('- 36 unused scale sets should be deleted (only Leadership and Safety are needed)')
w()
w('### Duplicate SCORM Packages')
w('- 71 duplicate packages detected in Learn365 (256 total packages, 185 unique titles)')
w('- Duplicates should be consolidated to a single package per course')
w()

# ══════════════════════════════════════════════════════════════════════
# APPENDIX A: Proposed Vocabulary
# ══════════════════════════════════════════════════════════════════════

w('---')
w()
w('## Appendix A: Proposed Vocabulary Additions')
w()
w('Only **3 new tags** are proposed. No new skills, categories, or scale sets.')
w()
w('### Proposed Tags (Difficulty)')
w()
w('These tags enable filtering by difficulty level in the Learn365 catalog:')
w()
w('| Tag | Label | Purpose |')
w('|-----|-------|---------|')
w('| `Difficulty: Foundational` | PROPOSED | Introductory-level content, no prerequisites |')
w('| `Difficulty: Intermediate` | PROPOSED | Requires foundational knowledge in the topic |')
w('| `Difficulty: Advanced` | PROPOSED | Requires intermediate mastery and field experience |')
w()
w('### Existing Vocabulary Used')
w()
w(f'- **{len(existing_tags)} unique EXISTING tags** referenced across all courses')
w(f'- **{len(proposed_tags)} unique PROPOSED tags** (the 3 Difficulty tags above)')
w(f'- **{unique_skills} EXISTING skills** — all mapped from the current Learn365 Skills Framework')
w(f'- **0 new skills proposed**')
w()

# ══════════════════════════════════════════════════════════════════════
# APPENDIX B: Role → Target-Skills Matrix
# ══════════════════════════════════════════════════════════════════════

w('---')
w()
w('## Appendix B: Role → Target-Skills Matrix')
w()
w('GSL career track: Apprentice > Journeyman > Leadman > Foreman > Superintendent')
w('Plus: Project Safety Coordinator, Project Manager, General Superintendent, Branch Manager')
w()

# Build a full matrix
all_unique_skills = sorted(skill_counts.keys())
role_order = ['Apprentice', 'Journeyman', 'Leadman', 'Foreman', 'Superintendent',
              'Project Safety Coordinator', 'Project Manager', 'General Superintendent', 'Branch Manager']

# Summary table
w('### Summary')
w()
w('| Role | Skills | Courses |')
w('|------|--------|---------|')
for r in role_order:
    if r in role_skills:
        w(f'| {r} | {len(role_skills[r])} | {len(role_courses[r])} |')
w()

# Detailed per-role
for r in role_order:
    if r not in role_skills:
        continue
    w(f'### {r} ({len(role_skills[r])} skills, {len(role_courses[r])} courses)')
    w()
    for s in sorted(role_skills[r]):
        w(f'- {s}')
    w()

# Cross-reference matrix (skill x role)
w('### Skill Coverage Matrix')
w()
header = '| Skill | ' + ' | '.join(r[:4] for r in role_order) + ' |'
sep = '|-------|' + '|'.join('----' for _ in role_order) + '|'
w(header)
w(sep)
for skill in all_unique_skills:
    row = f'| {skill} |'
    for r in role_order:
        if skill in role_skills.get(r, set()):
            row += ' X |'
        else:
            row += '   |'
    w(row)
w()

# ══════════════════════════════════════════════════════════════════════
# APPENDIX C: Transcript Gap List
# ══════════════════════════════════════════════════════════════════════

w('---')
w()
w('## Appendix C: Transcript Gap List')
w()
w(f'**{len(transcript_gaps)} of {total} courses** lack in-package VTT transcripts.')
w()
w('To improve description quality, retrieve transcripts from:')
w('1. Learn365 video hosting (Azure Media Services / Blob)')
w('2. Rise 360 cloud-hosted captions')
w('3. Manual transcription of bundled MP4 files')
w()

# Group by confidence
gap_by_conf = defaultdict(list)
for g in transcript_gaps:
    gap_by_conf[g['confidence']].append(g)

for bucket in ['LOW', 'VERY LOW', 'MEDIUM', 'MEDIUM-HIGH']:
    gaps = gap_by_conf.get(bucket, [])
    if not gaps:
        continue
    w(f'### {bucket} Confidence ({len(gaps)} courses)')
    w()
    w('| Course | Has Video | Transcript Status |')
    w('|--------|-----------|-------------------|')
    for g in sorted(gaps, key=lambda x: x['course']):
        vid = 'Yes' if g['has_video'] else 'No'
        w(f'| {g["course"]} | {vid} | {g["transcript_status"]} |')
    w()

# ── Write output ─────────────────────────────────────────────────────

report = '\n'.join(lines)
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"Report written to {OUT_PATH}")
print(f"  {len(lines)} lines, {len(report)} bytes")
print(f"  Sections: Summary, Confidence, Difficulty, Categories, Skills, Series, NEEDS-REVIEW, Batches, Data Quality")
print(f"  Appendix A: Proposed Vocabulary (3 tags)")
print(f"  Appendix B: Role-Skills Matrix ({len(role_order)} roles x {len(all_unique_skills)} skills)")
print(f"  Appendix C: Transcript Gaps ({len(transcript_gaps)} courses)")
