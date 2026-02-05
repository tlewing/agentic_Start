"""
Parse Policy Manual documents (Job Descriptions & Management Directives)
to build a reference model for SOP validation.
"""
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import json
import re

BASE_DIR = Path(r"C:\Users\tewing\Desktop\Holding\SOP\SOP Resources\Policy Manual")
OUTPUT_FILE = Path(r"C:\Users\tewing\Desktop\Holding\SOP\docs\policy_reference.json")

def extract_text_from_doc(doc_path):
    """Extract text from .doc or .docx file."""
    if doc_path.suffix == '.docx':
        try:
            with zipfile.ZipFile(doc_path, 'r') as zf:
                xml_content = zf.read('word/document.xml').decode('utf-8')
                root = ET.fromstring(xml_content)
                text_parts = []
                for elem in root.iter():
                    if elem.text:
                        text_parts.append(elem.text)
                return ' '.join(text_parts)
        except Exception as e:
            print(f"  Error reading {doc_path.name}: {e}")
            return ""
    elif doc_path.suffix == '.doc':
        # .doc files are binary - we'll note them for manual review
        return f"[BINARY .doc file - needs manual review: {doc_path.name}]"
    return ""


def parse_job_description(text, filename):
    """Extract role info from job description text."""
    role = {
        'filename': filename,
        'title': '',
        'responsibilities': [],
        'keywords': []
    }

    # Extract title from filename
    title_match = re.search(r'7\.\d+\.?\d*\s+(.+?)(?:\s*[-–]\s*REVISED|\s*\(Revised\)|\.doc)', filename, re.IGNORECASE)
    if title_match:
        role['title'] = title_match.group(1).strip()

    if '[BINARY' in text:
        role['note'] = 'Binary .doc file - needs manual conversion'
        return role

    # Extract responsibilities (look for bullet points or numbered items)
    resp_patterns = [
        r'(?:responsibilities|duties)[\s:]*(.+?)(?:qualifications|requirements|$)',
        r'•\s*(.+?)(?:\n|$)',
        r'\d+\.\s+(.+?)(?:\n|$)'
    ]

    text_lower = text.lower()

    # Extract keywords based on common PM/field terms
    pm_keywords = ['schedule', 'budget', 'cost', 'billing', 'change order', 'submittal',
                   'rfi', 'coordination', 'meeting', 'client', 'owner', 'subcontractor',
                   'procurement', 'material', 'labor', 'safety', 'quality', 'closeout']

    for kw in pm_keywords:
        if kw in text_lower:
            role['keywords'].append(kw)

    return role


def parse_management_directive(text, filename):
    """Extract directive scope from management directive text."""
    directive = {
        'filename': filename,
        'title': '',
        'scope': [],
        'responsibilities': [],
        'keywords': []
    }

    # Extract title from filename
    title_match = re.search(r'9\.\d+\s+.*?for\s+(.+?)(?:\s*[-–]\s*REVISED|\s*\(Revised\)|\.doc)', filename, re.IGNORECASE)
    if title_match:
        directive['title'] = title_match.group(1).strip()

    if '[BINARY' in text:
        directive['note'] = 'Binary .doc file - needs manual conversion'
        return directive

    text_lower = text.lower()

    # Extract scope keywords
    scope_keywords = ['pre-construction', 'mobilization', 'execution', 'closeout',
                      'estimating', 'bidding', 'field', 'project management',
                      'purchasing', 'safety', 'quality', 'commissioning']

    for kw in scope_keywords:
        if kw in text_lower:
            directive['scope'].append(kw)

    # Activity keywords
    activity_keywords = ['schedule', 'budget', 'billing', 'change order', 'submittal',
                        'rfi', 'coordination', 'meeting', 'procurement', 'material',
                        'labor', 'safety', 'quality', 'documentation', 'reporting']

    for kw in activity_keywords:
        if kw in text_lower:
            directive['keywords'].append(kw)

    return directive


def main():
    print("=" * 60)
    print("PARSING POLICY MANUAL DOCUMENTS")
    print("=" * 60)

    reference = {
        'job_descriptions': [],
        'management_directives': [],
        'sop_phase_mapping': {
            '9.1': {'name': 'Project Procurement, Design & Estimating', 'roles': ['Estimator', 'Business Development']},
            '9.2': {'name': 'Pre-Construction', 'roles': ['Project Manager', 'General Superintendent', 'Estimator', 'Safety']},
            '9.3': {'name': 'Mobilization & Jobsite Setup', 'roles': ['Project Manager', 'General Superintendent', 'Foreman']},
            '9.4': {'name': 'Construction Execution', 'roles': ['Project Manager', 'General Superintendent', 'Foreman', 'Safety', 'Purchasing']},
            '9.5': {'name': 'Testing & Commissioning', 'roles': ['Project Manager', 'General Superintendent', 'Foreman']},
            '9.6': {'name': 'Project Closeout', 'roles': ['Project Manager', 'General Superintendent', 'Admin']}
        }
    }

    # Find job descriptions (prefer Revised versions)
    print("\n--- JOB DESCRIPTIONS ---")
    jd_dir = BASE_DIR / "Section 7 - Job Descriptions"
    jd_files = list(jd_dir.rglob("*Revised*.doc*")) + list(jd_dir.rglob("*(Revised)*.doc*"))

    # If no revised, fall back to originals
    if not jd_files:
        jd_files = list(jd_dir.rglob("*.doc*"))

    # Deduplicate - prefer (Revised).docx over - REVISED.doc
    seen_roles = {}
    for f in jd_files:
        role_match = re.search(r'7\.(\d+\.?\d*)', f.name)
        if role_match:
            role_num = role_match.group(1)
            # Prefer .docx over .doc, and (Revised) over - REVISED
            if role_num not in seen_roles or f.suffix == '.docx':
                seen_roles[role_num] = f

    for f in sorted(seen_roles.values(), key=lambda x: x.name):
        print(f"  Parsing: {f.name}")
        text = extract_text_from_doc(f)
        jd = parse_job_description(text, f.name)
        reference['job_descriptions'].append(jd)

    # Find management directives (prefer Revised versions)
    print("\n--- MANAGEMENT DIRECTIVES ---")
    md_dir = BASE_DIR / "Section 9 - Management Directives"
    md_files = list(md_dir.rglob("*Revised*.doc*")) + list(md_dir.rglob("*(Revised)*.doc*"))

    if not md_files:
        md_files = list(md_dir.rglob("*.doc*"))

    # Deduplicate
    seen_directives = {}
    for f in md_files:
        dir_match = re.search(r'9\.(\d+)', f.name)
        if dir_match:
            dir_num = dir_match.group(1)
            if dir_num not in seen_directives or f.suffix == '.docx':
                seen_directives[dir_num] = f

    for f in sorted(seen_directives.values(), key=lambda x: x.name):
        print(f"  Parsing: {f.name}")
        text = extract_text_from_doc(f)
        md = parse_management_directive(text, f.name)
        reference['management_directives'].append(md)

    # Save reference model
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(reference, f, indent=2)

    print(f"\n--- SUMMARY ---")
    print(f"Job Descriptions parsed: {len(reference['job_descriptions'])}")
    print(f"Management Directives parsed: {len(reference['management_directives'])}")
    print(f"Reference saved to: {OUTPUT_FILE}")

    # List any binary .doc files that need manual conversion
    binary_files = []
    for jd in reference['job_descriptions']:
        if 'note' in jd and 'Binary' in jd['note']:
            binary_files.append(jd['filename'])
    for md in reference['management_directives']:
        if 'note' in md and 'Binary' in md['note']:
            binary_files.append(md['filename'])

    if binary_files:
        print(f"\n--- BINARY .doc FILES (need conversion to .docx) ---")
        for bf in binary_files:
            print(f"  {bf}")


if __name__ == "__main__":
    main()
