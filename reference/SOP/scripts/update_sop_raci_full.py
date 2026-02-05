"""
Update SOP RACI Metadata
Analyzes each SOP and populates RACI (Responsible, Accountable, Consulted, Informed)
fields based on content analysis and phase mapping.
"""
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import json
import re
import shutil
from datetime import datetime

BASE_DIR = Path(r"C:\Users\tewing\Desktop\Holding\SOP")
SOURCE_DIR = BASE_DIR / "SharePoint-SOPs"
OUTPUT_DIR = BASE_DIR / "Revised-SOPs"
TEMPLATE_PATH = BASE_DIR / "Templates" / "GSL_SOP_Master_Template_SHAREPOINT_ENABLED (v1).docx"
REFERENCE_FILE = BASE_DIR / "docs" / "policy_reference.json"
RACI_LOG = BASE_DIR / "docs" / "sop_raci_assignments.md"

NAMESPACE = "b11c1c0a-1848-4118-b7cf-ce9450f86f68"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)


def load_reference():
    """Load the policy reference data."""
    with open(REFERENCE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_text_from_docx(docx_path):
    """Extract plain text from a docx file."""
    try:
        with zipfile.ZipFile(docx_path, 'r') as zf:
            xml_content = zf.read('word/document.xml').decode('utf-8')
            root = ET.fromstring(xml_content)
            text_parts = []
            for elem in root.iter():
                if elem.text:
                    text_parts.append(elem.text)
            return ' '.join(text_parts)
    except Exception as e:
        return f"[ERROR: {e}]"


def extract_sop_info(text, filename):
    """Extract SOP ID and title from text/filename."""
    info = {
        'filename': filename,
        'sop_id': '',
        'title': '',
        'phase': ''
    }

    # Extract SOP ID from filename
    id_match = re.search(r'(9\.\d+\.?\d*)', filename)
    if id_match:
        info['sop_id'] = id_match.group(1)
        phase_match = re.match(r'9\.(\d)', info['sop_id'])
        if phase_match:
            info['phase'] = f"9.{phase_match.group(1)}"

    # Extract title
    title_match = re.search(r'9\.\d+\.?\d*\s*[–-]\s*(.+?)(?:\.docx|$)', filename)
    if title_match:
        info['title'] = title_match.group(1).strip()

    return info


def determine_raci(text, sop_info, reference):
    """
    Determine RACI assignments based on SOP content and phase.

    RACI Logic:
    - Responsible: Primary role that executes the task (first mentioned, or role in title)
    - Accountable: Role that owns the outcome (usually PM or GS)
    - Consulted: Roles mentioned as providing input
    - Informed: Roles mentioned as receiving updates/reports
    """
    raci = {
        'responsible': [],
        'accountable': [],
        'consulted': [],
        'informed': []
    }

    text_lower = text.lower()
    phase = sop_info['phase']
    title_lower = sop_info['title'].lower()

    # Role detection patterns (Field Supervisor = Foreman)
    role_patterns = {
        'Project Manager': r'project\s*manager|PM\b',
        'General Superintendent': r'general\s*superintendent|GS\b',
        'Foreman': r'foreman|field\s*supervisor',
        'Safety': r'safety\s*(rep|coordinator|officer)?',
        'Estimator': r'estimator|estimating',
        'Purchasing': r'purchas(ing|er)|buyer',
        'Prefab': r'prefab|pre-fab',
        'Admin': r'admin|administrative',
        'Lead Journeyman': r'lead\s*journeyman',
    }

    # Find all mentioned roles
    mentioned_roles = []
    for role, pattern in role_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            mentioned_roles.append(role)

    # Determine Responsible based on title keywords
    title_role_hints = {
        'safety': 'Safety',
        'quality': 'General Superintendent',
        'schedule': 'Project Manager',
        'budget': 'Project Manager',
        'cost': 'Project Manager',
        'billing': 'Project Manager',
        'procurement': 'Purchasing',
        'purchase': 'Purchasing',
        'material': 'Purchasing',
        'vendor': 'Purchasing',
        'prefab': 'Prefab',
        'field': 'Foreman',
        'setup': 'Foreman',
        'coordination': 'Project Manager',
        'meeting': 'Project Manager',
        'closeout': 'Project Manager',
        'documentation': 'Admin',
        'estimat': 'Estimator',
    }

    # Default responsible by phase
    phase_default_responsible = {
        '9.1': 'Estimator',
        '9.2': 'Project Manager',
        '9.3': 'Foreman',
        '9.4': 'Foreman',
        '9.5': 'General Superintendent',
        '9.6': 'Project Manager'
    }

    # Determine Responsible
    responsible = None
    for hint, role in title_role_hints.items():
        if hint in title_lower:
            responsible = role
            break

    if not responsible:
        responsible = phase_default_responsible.get(phase, 'Project Manager')

    raci['responsible'] = [responsible]

    # Determine Accountable (always PM or GS)
    if responsible in ['Foreman', 'Safety', 'Lead Journeyman']:
        raci['accountable'] = ['General Superintendent']
    elif responsible in ['Purchasing', 'Admin', 'Prefab']:
        raci['accountable'] = ['Project Manager']
    elif responsible == 'General Superintendent':
        raci['accountable'] = ['Project Manager']
    elif responsible == 'Project Manager':
        raci['accountable'] = ['Operations Manager']
    else:
        raci['accountable'] = ['Project Manager']

    # Determine Consulted (other mentioned roles not R or A)
    for role in mentioned_roles:
        if role not in raci['responsible'] and role not in raci['accountable']:
            if role not in raci['consulted']:
                raci['consulted'].append(role)

    # Determine Informed based on content patterns
    inform_patterns = {
        'notify': True,
        'inform': True,
        'report to': True,
        'update': True,
        'communicate': True,
    }

    for pattern in inform_patterns:
        if pattern in text_lower:
            # Add stakeholders typically informed
            if 'client' in text_lower or 'owner' in text_lower:
                if 'Project Manager' not in raci['informed']:
                    raci['informed'].append('Project Manager')

    # Ensure we don't have duplicates across categories
    # Remove from Consulted if in R or A
    raci['consulted'] = [r for r in raci['consulted']
                         if r not in raci['responsible'] and r not in raci['accountable']]

    # Limit lists
    raci['consulted'] = raci['consulted'][:3]
    raci['informed'] = raci['informed'][:3]

    return raci


def update_sharepoint_metadata(docx_path, metadata):
    """Update the SharePoint metadata in the docx file's custom XML."""
    temp_path = docx_path.with_suffix('.tmp')

    with zipfile.ZipFile(docx_path, 'r') as zf_in:
        with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as zf_out:
            for item in zf_in.namelist():
                if item == 'customXml/item4.xml':
                    xml_content = zf_in.read(item).decode('utf-8')
                    xml_content = update_properties_xml(xml_content, metadata)
                    zf_out.writestr(item, xml_content.encode('utf-8'))
                else:
                    zf_out.writestr(item, zf_in.read(item))

    temp_path.replace(docx_path)


def update_properties_xml(xml_content, metadata):
    """Update the properties XML with new metadata values."""
    # Field mapping
    field_updates = {
        'RACI_Responsible': ', '.join(metadata.get('raci_responsible', [])),
        'RACI_Accountable': ', '.join(metadata.get('raci_accountable', [])),
        'RACI_Consulted': ', '.join(metadata.get('raci_consulted', [])),
        'RACI_Informed': ', '.join(metadata.get('raci_informed', [])),
        'SOPID': metadata.get('sop_id', ''),
        'SOPFileName': metadata.get('filename', ''),
        'Status': metadata.get('status', 'Draft'),
        'Description': metadata.get('description', ''),
        'Department_x002f_Division': metadata.get('department', ''),
        'Tags_x002f_Keywords': metadata.get('tags', ''),
    }

    for field, value in field_updates.items():
        if value:
            # Try to find and update the field
            # Pattern: <FieldName xmlns="...">value</FieldName> or <FieldName ... xsi:nil="true"/>
            pattern = rf'(<{field}[^>]*)(xsi:nil="true")?(/?>)([^<]*)(</[^>]*{field}>)?'

            def replace_field(match):
                opening = match.group(1)
                closing_tag = f'</{field.split()[0]}>'
                # Remove nil attribute if present
                opening = re.sub(r'\s*xsi:nil="true"', '', opening)
                # Check if self-closing
                if match.group(3) == '/>':
                    return f'{opening}>{value}{closing_tag}'
                else:
                    return f'{opening}>{value}{closing_tag}'

            xml_content = re.sub(pattern, replace_field, xml_content, flags=re.IGNORECASE)

    return xml_content


def process_sop(source_path, reference):
    """Process a single SOP and update its RACI metadata."""
    # Extract text
    text = extract_text_from_docx(source_path)
    sop_info = extract_sop_info(text, source_path.name)

    if not sop_info['sop_id']:
        return None, "No SOP ID found"

    # Determine RACI
    raci = determine_raci(text, sop_info, reference)

    # Copy source to output
    output_path = OUTPUT_DIR / source_path.name
    shutil.copy2(source_path, output_path)

    # Prepare metadata
    phase_mapping = reference.get('sop_phase_mapping', {})
    phase_info = phase_mapping.get(sop_info['phase'], {})

    metadata = {
        'sop_id': sop_info['sop_id'],
        'filename': source_path.name,
        'status': 'Draft',
        'description': sop_info['title'],
        'department': 'Project Management',
        'tags': f"{phase_info.get('name', '')}, {sop_info['title'][:50]}",
        'raci_responsible': raci['responsible'],
        'raci_accountable': raci['accountable'],
        'raci_consulted': raci['consulted'],
        'raci_informed': raci['informed'],
    }

    # Update metadata
    update_sharepoint_metadata(output_path, metadata)

    return {
        'sop_id': sop_info['sop_id'],
        'title': sop_info['title'],
        'phase': sop_info['phase'],
        'raci': raci
    }, None


def main():
    print("=" * 60)
    print("UPDATE SOP RACI METADATA")
    print("=" * 60)

    # Load reference
    reference = load_reference()

    # Get all SOPs
    sop_files = list(SOURCE_DIR.glob("*.docx"))
    print(f"\nProcessing {len(sop_files)} SOPs...")

    results = []
    errors = []

    for sop_file in sorted(sop_files):
        result, error = process_sop(sop_file, reference)
        if result:
            results.append(result)
            print(f"  [OK] {result['sop_id']} - R: {', '.join(result['raci']['responsible'])}")
        else:
            errors.append({'file': sop_file.name, 'error': error})
            print(f"  [ERR] {sop_file.name}: {error}")

    # Generate RACI log
    print(f"\nGenerating RACI assignments log...")

    with open(RACI_LOG, 'w', encoding='utf-8') as f:
        f.write(f"# SOP RACI Assignments\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**Total SOPs:** {len(results)}\n\n")

        f.write("## RACI Matrix\n\n")
        f.write("| SOP ID | Title | Responsible | Accountable | Consulted | Informed |\n")
        f.write("|--------|-------|-------------|-------------|-----------|----------|\n")

        for r in results:
            f.write(f"| {r['sop_id']} | {r['title'][:30]} | {', '.join(r['raci']['responsible'])} | {', '.join(r['raci']['accountable'])} | {', '.join(r['raci']['consulted']) or '-'} | {', '.join(r['raci']['informed']) or '-'} |\n")

        if errors:
            f.write(f"\n## Errors\n\n")
            for e in errors:
                f.write(f"- {e['file']}: {e['error']}\n")

    print(f"\n--- COMPLETE ---")
    print(f"Processed: {len(results)}")
    print(f"Errors: {len(errors)}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"RACI Log: {RACI_LOG}")


if __name__ == "__main__":
    main()
