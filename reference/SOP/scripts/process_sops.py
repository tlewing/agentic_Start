"""
GSL SOP Processor
Reads existing SOPs, rewrites them using the SharePoint-enabled template,
and populates both content and metadata fields.
"""
import zipfile
import shutil
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches
from datetime import datetime

# Paths
BASE_DIR = Path(r"C:\Users\tewing\Desktop\Holding\SOP")
TEMPLATE_PATH = BASE_DIR / "Templates" / "GSL_SOP_Master_Template_SHAREPOINT_ENABLED (v1).docx"
SOURCE_DIR = BASE_DIR / "SharePoint-SOPs"
OUTPUT_DIR = BASE_DIR / "Revised-SOPs"
NAMESPACE = "b11c1c0a-1848-4118-b7cf-ce9450f86f68"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)


def extract_text_from_docx(docx_path):
    """Extract plain text from a docx file."""
    with zipfile.ZipFile(docx_path, 'r') as zf:
        xml_content = zf.read('word/document.xml').decode('utf-8')
        root = ET.fromstring(xml_content)
        # Extract all text
        text_parts = []
        for elem in root.iter():
            if elem.text:
                text_parts.append(elem.text)
        return ''.join(text_parts)


def parse_sop_content(text):
    """Parse SOP text into structured sections."""
    sections = {
        'sop_id': '',
        'title': '',
        'department': '',
        'related_sops': '',
        'purpose': '',
        'scope': '',
        'roles': '',
        'requirements': '',
        'procedure': '',
        'appendix': ''
    }

    # Extract SOP ID and title from header
    sop_match = re.search(r'SOP:\s*([\d.]+)\s*[–-]\s*(.+?)(?:Department|$)', text, re.IGNORECASE)
    if sop_match:
        sections['sop_id'] = sop_match.group(1).strip()
        sections['title'] = sop_match.group(2).strip()

    # Extract department
    dept_match = re.search(r'Department:\s*(.+?)(?:Related|Purpose|$)', text, re.IGNORECASE | re.DOTALL)
    if dept_match:
        sections['department'] = dept_match.group(1).strip()

    # Extract related SOPs
    related_match = re.search(r'Related SOPs?:?\s*(.+?)(?:Purpose|$)', text, re.IGNORECASE | re.DOTALL)
    if related_match:
        sections['related_sops'] = related_match.group(1).strip()

    # Extract purpose
    purpose_match = re.search(r'Purpose\s*(.+?)(?:Scope|$)', text, re.IGNORECASE | re.DOTALL)
    if purpose_match:
        sections['purpose'] = purpose_match.group(1).strip()

    # Extract scope
    scope_match = re.search(r'Scope\s*(.+?)(?:Roles|$)', text, re.IGNORECASE | re.DOTALL)
    if scope_match:
        sections['scope'] = scope_match.group(1).strip()

    # Extract roles & responsibilities
    roles_match = re.search(r'Roles\s*(?:&|and)?\s*Responsibilities?\s*(.+?)(?:Requirements?|$)', text, re.IGNORECASE | re.DOTALL)
    if roles_match:
        sections['roles'] = roles_match.group(1).strip()

    # Extract requirements
    req_match = re.search(r'Requirements?\s*(.+?)(?:Procedure|$)', text, re.IGNORECASE | re.DOTALL)
    if req_match:
        sections['requirements'] = req_match.group(1).strip()

    # Extract procedure
    proc_match = re.search(r'Procedure\s*(.+?)(?:Appendix|$)', text, re.IGNORECASE | re.DOTALL)
    if proc_match:
        sections['procedure'] = proc_match.group(1).strip()

    # Extract appendix
    app_match = re.search(r'Appendix\s*(.+?)$', text, re.IGNORECASE | re.DOTALL)
    if app_match:
        sections['appendix'] = app_match.group(1).strip()

    return sections


def extract_raci_roles(roles_text):
    """Extract RACI roles from the roles section."""
    raci = {
        'responsible': [],
        'accountable': [],
        'consulted': [],
        'informed': []
    }

    # Common role patterns (Field Supervisor = Foreman)
    role_patterns = [
        r'Project Manager|PM',
        r'General Superintendent|GS',
        r'Foreman|Field Supervisor',
        r'Safety|Safety Representative',
        r'Prefab|Prefab Lead',
        r'Purchasing|Buyer',
        r'Estimator',
        r'Admin|Administrative'
    ]

    text_lower = roles_text.lower()

    # Simple heuristic: first mentioned role is responsible, second is accountable
    found_roles = []
    for pattern in role_patterns:
        if re.search(pattern, roles_text, re.IGNORECASE):
            match = re.search(pattern, roles_text, re.IGNORECASE)
            found_roles.append(match.group(0))

    if len(found_roles) >= 1:
        raci['responsible'] = [found_roles[0]]
    if len(found_roles) >= 2:
        raci['accountable'] = [found_roles[1]]
    if len(found_roles) >= 3:
        raci['consulted'] = found_roles[2:4]
    if len(found_roles) >= 5:
        raci['informed'] = found_roles[4:]

    return raci


def determine_phase_category(sop_id):
    """Determine the phase category from SOP ID."""
    phase_map = {
        '9.1': ('9.1', 'Project Procurement, Design & Estimating'),
        '9.2': ('9.2', 'Pre-Construction'),
        '9.3': ('9.3', 'Mobilization & Jobsite Setup'),
        '9.4': ('9.4', 'Construction Execution'),
        '9.5': ('9.5', 'Testing & Commissioning'),
        '9.6': ('9.6', 'Project Closeout')
    }

    for prefix, (code, name) in phase_map.items():
        if sop_id.startswith(prefix):
            return code, name
    return '', ''


def update_sharepoint_metadata(docx_path, metadata):
    """Update the SharePoint metadata in the docx file's custom XML."""

    # Read the docx as a zip
    temp_path = docx_path.with_suffix('.tmp')

    with zipfile.ZipFile(docx_path, 'r') as zf_in:
        with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as zf_out:
            for item in zf_in.namelist():
                if item == 'customXml/item4.xml':
                    # Update the SharePoint properties XML
                    xml_content = zf_in.read(item).decode('utf-8')
                    xml_content = update_properties_xml(xml_content, metadata)
                    zf_out.writestr(item, xml_content.encode('utf-8'))
                else:
                    zf_out.writestr(item, zf_in.read(item))

    # Replace original with updated
    temp_path.replace(docx_path)


def update_properties_xml(xml_content, metadata):
    """Update the properties XML with new metadata values."""
    ns = {'p': 'http://schemas.microsoft.com/office/2006/metadata/properties',
          'ns': NAMESPACE,
          'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

    root = ET.fromstring(xml_content)
    doc_mgmt = root.find('.//documentManagement', {'': ''})

    if doc_mgmt is None:
        # Find it without namespace
        for child in root:
            if 'documentManagement' in child.tag:
                doc_mgmt = child
                break

    if doc_mgmt is None:
        return xml_content

    # Field mapping
    field_map = {
        'Status': metadata.get('status', 'Draft'),
        'DocumentType': 'SOP',
        'SOPFileName': metadata.get('filename', ''),
        'Description': metadata.get('description', ''),
        'RelatedSOPs': metadata.get('related_sops', ''),
        'SOPID': metadata.get('sop_id', ''),
        'Tags_x002f_Keywords': metadata.get('tags', ''),
        'Department_x002f_Division': metadata.get('department', ''),
        'Category_x0028_CCCTag_x0029_': metadata.get('category', ''),
        'RACI_Responsible': ', '.join(metadata.get('raci_responsible', [])),
        'RACI_Accountable': ', '.join(metadata.get('raci_accountable', [])),
        'RACI_Consulted': ', '.join(metadata.get('raci_consulted', [])),
        'RACI_Informed': ', '.join(metadata.get('raci_informed', [])),
        'Appendix_x003a_': metadata.get('appendix', ''),
    }

    for child in doc_mgmt:
        # Get the local name (without namespace)
        local_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag

        if local_name in field_map and field_map[local_name]:
            # Remove nil attribute if present
            for attr in list(child.attrib.keys()):
                if 'nil' in attr:
                    del child.attrib[attr]
            child.text = field_map[local_name]

    return ET.tostring(root, encoding='unicode', xml_declaration=True)


def process_single_sop(source_path):
    """Process a single SOP file."""
    print(f"\nProcessing: {source_path.name}")

    # Extract text from source
    text = extract_text_from_docx(source_path)
    sections = parse_sop_content(text)

    if not sections['sop_id']:
        print(f"  WARNING: Could not extract SOP ID from {source_path.name}")
        # Try to get from filename
        fname_match = re.search(r'([\d.]+)\s*[–-]', source_path.name)
        if fname_match:
            sections['sop_id'] = fname_match.group(1)

    print(f"  SOP ID: {sections['sop_id']}")
    print(f"  Title: {sections['title'][:50]}..." if len(sections['title']) > 50 else f"  Title: {sections['title']}")

    # Copy template to output
    output_filename = f"{sections['sop_id']} – {sections['title']}.docx" if sections['title'] else source_path.name
    # Clean filename
    output_filename = re.sub(r'[<>:"/\\|?*]', '', output_filename)
    output_path = OUTPUT_DIR / output_filename

    shutil.copy2(TEMPLATE_PATH, output_path)

    # Open and update content
    doc = Document(output_path)

    # Track which section we're in
    current_section = None
    section_headers = ['Purpose', 'Scope', 'Roles & Responsibilities', 'Requirements', 'Procedure', 'Appendix']
    paragraphs_to_update = []

    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()

        # Header replacements
        if '[SOP #]' in para.text or '[SOP Title]' in para.text:
            para.text = para.text.replace('[SOP #]', sections['sop_id']).replace('[SOP Title]', sections['title'])
            continue

        if '[Department(s)]' in para.text:
            para.text = para.text.replace('[Department(s)]', sections['department'] or 'Project Management')
            continue

        # Track section headers
        if text in section_headers or text.startswith('Roles'):
            current_section = text.split('&')[0].strip().lower()
            continue

        # Replace content based on current section
        if current_section == 'purpose' and '[Describe the purpose' in text:
            para.text = sections['purpose'] if sections['purpose'] else text
        elif current_section == 'scope' and ('[Condition' in text or 'Applies to' in text):
            if '[Condition' in text:
                para.text = sections['scope'] if sections['scope'] else text
        elif current_section == 'roles' and '[Role' in text:
            para.text = sections['roles'][:500] if sections['roles'] else text
        elif current_section == 'requirements' and '[Requirement' in text:
            para.text = sections['requirements'][:500] if sections['requirements'] else text
        elif current_section == 'procedure' and '[Describe what' in text:
            para.text = sections['procedure'][:1500] if sections['procedure'] else text
        elif 'Related SOP' in text and '[Related SOP Title]' in text:
            para.text = sections['related_sops'][:300] if sections['related_sops'] else ''

    doc.save(output_path)

    # Extract RACI info
    raci = extract_raci_roles(sections['roles'])
    phase_code, phase_name = determine_phase_category(sections['sop_id'])

    # Prepare metadata
    metadata = {
        'status': 'Draft',
        'filename': output_filename,
        'description': sections['purpose'][:255] if sections['purpose'] else sections['title'],
        'related_sops': sections['related_sops'][:255] if sections['related_sops'] else '',
        'sop_id': sections['sop_id'],
        'tags': f"{phase_name}, Project Management",
        'department': sections['department'] or 'Project Management',
        'category': phase_code,
        'raci_responsible': raci['responsible'],
        'raci_accountable': raci['accountable'],
        'raci_consulted': raci['consulted'],
        'raci_informed': raci['informed'],
        'appendix': 'Yes' if sections['appendix'] else ''
    }

    # Update SharePoint metadata
    update_sharepoint_metadata(output_path, metadata)

    print(f"  Output: {output_path.name}")
    return True


def main():
    """Process all SOPs."""
    print("=" * 60)
    print("GSL SOP PROCESSOR")
    print("=" * 60)
    print(f"\nTemplate: {TEMPLATE_PATH.name}")
    print(f"Source: {SOURCE_DIR}")
    print(f"Output: {OUTPUT_DIR}")

    # Get all source SOPs
    source_files = list(SOURCE_DIR.glob("*.docx"))
    print(f"\nFound {len(source_files)} SOPs to process")

    success = 0
    failed = 0

    for source_file in sorted(source_files):
        try:
            if process_single_sop(source_file):
                success += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"COMPLETE: {success} processed, {failed} failed")
    print(f"Output folder: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
