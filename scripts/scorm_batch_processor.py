"""
SCORM Batch Processor
Extracts content and generates taxonomy recommendations for batches of SCORM courses.
Reads from scorm_course_index.json, writes to scorm_taxonomy_recommendations.json.
Designed to be run incrementally — only processes courses assigned to the given batch.
"""
import zipfile, os, json, re, sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SCORM_DIR = r'C:\Users\tewing\OneDrive - GSL Electric\Projects\training-template\reference\scorm'
DATA_DIR = r'C:\Users\tewing\OneDrive - GSL Electric\Projects\GSL-Operations-Framework\data'
INDEX_PATH = os.path.join(DATA_DIR, 'scorm_course_index.json')
RECS_PATH = os.path.join(DATA_DIR, 'scorm_taxonomy_recommendations.json')
VOCAB_PATH = os.path.join(DATA_DIR, 'learn365_vocabulary_snapshot.json')


def load_vocab():
    with open(VOCAB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_vtt_text(content):
    content = content.replace('\ufeff', '')
    lines = content.split('\n')
    texts = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('WEBVTT') and not line.startswith('NOTE') \
           and '-->' not in line and not re.match(r'^\d+$', line):
            clean = re.sub(r'<[^>]+>', '', line).strip()
            if clean:
                texts.append(clean)
    return ' '.join(texts)


def extract_content(zf_path):
    """Extract all available content from a SCORM zip."""
    result = {}
    with zipfile.ZipFile(zf_path, 'r') as zf:
        names = zf.namelist()

        # Manifest
        for n in names:
            if n.lower().endswith('imsmanifest.xml'):
                with zf.open(n) as mf:
                    tree = ET.parse(mf)
                    root = tree.getroot()
                    ns = root.tag.split('}')[0] + '}' if '}' in root.tag else ''
                    orgs = root.find(f'{ns}organizations')
                    if orgs is not None:
                        org = orgs.find(f'{ns}organization')
                        if org is not None:
                            items = []
                            for item in org.iter(f'{ns}item'):
                                it = item.find(f'{ns}title')
                                if it is not None and it.text:
                                    items.append(it.text.strip())
                            result['manifest_items'] = items
                break

        # VTTs
        vtt_files = [n for n in names if n.lower().endswith('.vtt')]
        vtts = []
        for vf in vtt_files:
            with zf.open(vf) as f:
                text = extract_vtt_text(f.read().decode('utf-8', errors='ignore'))
                vtts.append({'file': vf, 'text': text})
        result['vtt'] = vtts

        # Videos and assets
        result['videos'] = [os.path.basename(n) for n in names
                           if any(n.lower().endswith(e) for e in ['.mp4', '.webm'])]
        result['assets'] = [os.path.basename(n) for n in names
                           if any(n.lower().endswith(e) for e in ['.jpg', '.png', '.pdf'])
                           and 'lib/' not in n and 'scormdriver' not in n][:12]

        result['format'] = 'rise360' if any('lib/rise/' in n for n in names) else 'generic'
        result['file_count'] = len(names)

    return result


def get_batch_courses(batch_num):
    """Get courses assigned to a specific batch from the index."""
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        idx = json.load(f)
    return [c for c in idx['courses'] if c.get('batch') == batch_num and c['status'] != 'done']


def load_existing_recs():
    """Load existing recommendations file."""
    if os.path.exists(RECS_PATH):
        with open(RECS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"meta": {}, "courses": []}


def save_recs(recs):
    with open(RECS_PATH, 'w', encoding='utf-8') as f:
        json.dump(recs, f, indent=2, ensure_ascii=False)


def mark_batch_done(batch_num):
    """Mark all courses in a batch as done in the index."""
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        idx = json.load(f)
    for c in idx['courses']:
        if c.get('batch') == batch_num:
            c['status'] = 'done'
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(idx, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    batch_num = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    courses = get_batch_courses(batch_num)
    print(f'Batch {batch_num}: {len(courses)} courses to process')

    for c in courses:
        zf_path = os.path.join(SCORM_DIR, c['file'])
        content = extract_content(zf_path)
        vtt_chars = sum(len(v['text']) for v in content.get('vtt', []))
        print(f'  {c["title"][:55]:55s} vtt={vtt_chars:>5d} vid={len(content.get("videos",[]))} assets={len(content.get("assets",[]))}')
