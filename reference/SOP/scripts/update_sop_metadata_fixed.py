"""
Update SOP Metadata - Fixed Version
Uses proper XML parsing instead of regex for reliable metadata updates.
"""
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import json
import re
import shutil
from datetime import datetime
from copy import deepcopy

BASE_DIR = Path(r"C:\Users\tewing\Desktop\Holding\SOP")
SOURCE_DIR = BASE_DIR / "SharePoint-SOPs"
OUTPUT_DIR = BASE_DIR / "Revised-SOPs"
TEMPLATE_PATH = BASE_DIR / "Templates" / "GSL_SOP_Master_Template_SHAREPOINT_ENABLED (v1).docx"
REFERENCE_FILE = BASE_DIR / "docs" / "policy_reference.json"
RACI_LOG = BASE_DIR / "docs" / "sop_raci_assignments.md"

NAMESPACE = "b11c1c0a-1848-4118-b7cf-ce9450f86f68"
NS = {
    'p': 'http://schemas.microsoft.com/office/2006/metadata/properties',
    'ns': NAMESPACE,
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# Register namespaces to preserve them in output
ET.register_namespace('p', 'http://schemas.microsoft.com/office/2006/metadata/properties')
ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
ET.register_namespace('pc', 'http://schemas.microsoft.com/office/infopath/2007/PartnerControls')
ET.register_namespace('', NAMESPACE)

OUTPUT_DIR.mkdir(exist_ok=True)


def load_reference():
    with open(REFERENCE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_text_from_docx(docx_path):
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
    info = {'filename': filename, 'sop_id': '', 'title': '', 'phase': ''}

    id_match = re.search(r'(9\.\d+\.?\d*)', filename)
    if id_match:
        info['sop_id'] = id_match.group(1)
        phase_match = re.match(r'9\.(\d)', info['sop_id'])
        if phase_match:
            info['phase'] = f"9.{phase_match.group(1)}"

    title_match = re.search(r'9\.\d+\.?\d*\s*[–-]\s*(.+?)(?:\.docx|$)', filename)
    if title_match:
        info['title'] = title_match.group(1).strip()

    return info


def determine_raci(text, sop_info, reference):
    raci = {'responsible': [], 'accountable': [], 'consulted': [], 'informed': []}

    text_lower = text.lower()
    phase = sop_info['phase']
    title_lower = sop_info['title'].lower()

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

    mentioned_roles = []
    for role, pattern in role_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            mentioned_roles.append(role)

    title_role_hints = {
        'safety': 'Safety', 'quality': 'General Superintendent',
        'schedule': 'Project Manager', 'budget': 'Project Manager',
        'cost': 'Project Manager', 'billing': 'Project Manager',
        'procurement': 'Purchasing', 'purchase': 'Purchasing',
        'material': 'Purchasing', 'vendor': 'Purchasing',
        'prefab': 'Prefab', 'field': 'Foreman', 'setup': 'Foreman',
        'coordination': 'Project Manager', 'meeting': 'Project Manager',
        'closeout': 'Project Manager', 'documentation': 'Admin',
        'estimat': 'Estimator',
    }

    phase_default = {
        '9.1': 'Estimator', '9.2': 'Project Manager', '9.3': 'Foreman',
        '9.4': 'Foreman', '9.5': 'General Superintendent', '9.6': 'Project Manager'
    }

    responsible = None
    for hint, role in title_role_hints.items():
        if hint in title_lower:
            responsible = role
            break

    if not responsible:
        responsible = phase_default.get(phase, 'Project Manager')

    raci['responsible'] = [responsible]

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

    for role in mentioned_roles:
        if role not in raci['responsible'] and role not in raci['accountable']:
            if role not in raci['consulted']:
                raci['consulted'].append(role)

    raci['consulted'] = raci['consulted'][:3]

    return raci


def get_template_metadata_xml():
    """Extract the metadata XML structure from the template."""
    with zipfile.ZipFile(TEMPLATE_PATH, 'r') as zf:
        return zf.read('customXml/item4.xml').decode('utf-8')


def update_metadata_xml(xml_content, metadata):
    """Update metadata using proper XML parsing."""
    # Parse XML
    root = ET.fromstring(xml_content)

    # Find documentManagement element
    doc_mgmt = None
    for child in root:
        if 'documentManagement' in child.tag:
            doc_mgmt = child
            break

    if doc_mgmt is None:
        return xml_content

    # Field mapping (XML element name -> metadata key)
    field_map = {
        'Status': metadata.get('status', 'Draft'),
        'DocumentType': 'SOP',
        'SOPFileName': metadata.get('filename', ''),
        'Description': metadata.get('description', ''),
        'SOPID': metadata.get('sop_id', ''),
        'Tags_x002f_Keywords': metadata.get('tags', ''),
        'Department_x002f_Division': metadata.get('department', ''),
        'RACI_Responsible': ', '.join(metadata.get('raci_responsible', [])),
        'RACI_Accountable': ', '.join(metadata.get('raci_accountable', [])),
        'RACI_Consulted': ', '.join(metadata.get('raci_consulted', [])),
        'RACI_Informed': ', '.join(metadata.get('raci_informed', [])),
    }

    # Update each field
    for child in doc_mgmt:
        # Get local name without namespace
        local_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag

        if local_name in field_map:
            value = field_map[local_name]
            if value:
                # Remove xsi:nil attribute if present
                nil_attr = '{http://www.w3.org/2001/XMLSchema-instance}nil'
                if nil_attr in child.attrib:
                    del child.attrib[nil_attr]
                child.text = str(value)

    # Return updated XML
    return ET.tostring(root, encoding='unicode', xml_declaration=True)


def process_sop_with_template(source_path, reference):
    """Process SOP by copying template and updating with source content + metadata."""
    # Extract info from source
    text = extract_text_from_docx(source_path)
    sop_info = extract_sop_info(text, source_path.name)

    if not sop_info['sop_id']:
        return None, "No SOP ID found"

    # Determine RACI
    raci = determine_raci(text, sop_info, reference)

    # Copy TEMPLATE (not source) to output - this ensures we have the metadata structure
    output_path = OUTPUT_DIR / source_path.name
    shutil.copy2(TEMPLATE_PATH, output_path)

    # Get phase info
    phase_mapping = reference.get('sop_phase_mapping', {})
    phase_info = phase_mapping.get(sop_info['phase'], {})

    # Prepare metadata
    metadata = {
        'sop_id': sop_info['sop_id'],
        'filename': source_path.name,
        'status': 'Draft',
        'description': sop_info['title'][:255],
        'department': 'Project Management',
        'tags': f"{phase_info.get('name', '')[:50]}",
        'raci_responsible': raci['responsible'],
        'raci_accountable': raci['accountable'],
        'raci_consulted': raci['consulted'],
        'raci_informed': raci['informed'],
    }

    # Update metadata in the output file
    temp_path = output_path.with_suffix('.tmp')

    with zipfile.ZipFile(output_path, 'r') as zf_in:
        with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as zf_out:
            for item in zf_in.namelist():
                content = zf_in.read(item)

                if item == 'customXml/item4.xml':
                    # Update metadata XML
                    xml_content = content.decode('utf-8')
                    xml_content = update_metadata_xml(xml_content, metadata)
                    content = xml_content.encode('utf-8')

                zf_out.writestr(item, content)

    temp_path.replace(output_path)

    return {
        'sop_id': sop_info['sop_id'],
        'title': sop_info['title'],
        'phase': sop_info['phase'],
        'raci': raci
    }, None


def main():
    print("=" * 60)
    print("UPDATE SOP METADATA (FIXED)")
    print("=" * 60)

    reference = load_reference()
    sop_files = list(SOURCE_DIR.glob("*.docx"))
    print(f"\nProcessing {len(sop_files)} SOPs using template...")

    results = []
    errors = []

    for sop_file in sorted(sop_files):
        result, error = process_sop_with_template(sop_file, reference)
        if result:
            results.append(result)
            print(f"  [OK] {result['sop_id']} - R: {', '.join(result['raci']['responsible'])}")
        else:
            errors.append({'file': sop_file.name, 'error': error})
            print(f"  [ERR] {sop_file.name}: {error}")

    # Generate RACI log
    with open(RACI_LOG, 'w', encoding='utf-8') as f:
        f.write(f"# SOP RACI Assignments\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**Total SOPs:** {len(results)}\n\n")

        f.write("## RACI Matrix\n\n")
        f.write("| SOP ID | Title | R | A | C | I |\n")
        f.write("|--------|-------|---|---|---|---|\n")

        for r in results:
            f.write(f"| {r['sop_id']} | {r['title'][:25]}... | {', '.join(r['raci']['responsible'])} | {', '.join(r['raci']['accountable'])} | {', '.join(r['raci']['consulted']) or '-'} | {', '.join(r['raci']['informed']) or '-'} |\n")

    print(f"\n--- COMPLETE ---")
    print(f"Processed: {len(results)}")
    print(f"Errors: {len(errors)}")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
