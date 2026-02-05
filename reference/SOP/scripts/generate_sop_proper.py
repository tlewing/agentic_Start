"""
Generate SOP with Proper Formatting

Follows all 20 formatting rules from the SOP Formatting Instructions.
Builds Word XML from scratch using template structure.
"""

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import re
import shutil
from datetime import datetime
from copy import deepcopy

BASE_DIR = Path(r"C:\Users\tewing\Desktop\Holding\SOP")
SOURCE_DIR = BASE_DIR / "SharePoint-SOPs"
OUTPUT_DIR = BASE_DIR / "Revised-SOPs"
TEMPLATE_PATH = BASE_DIR / "Templates" / "GSL_SOP_Master_Template_SHAREPOINT_ENABLED (v1).docx"

OUTPUT_DIR.mkdir(exist_ok=True)

# SharePoint namespace
SP_NS = "b11c1c0a-1848-4118-b7cf-ce9450f86f68"

# Word namespaces
NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'v': 'urn:schemas-microsoft-com:vml',
    'o': 'urn:schemas-microsoft-com:office:office',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}

for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)


def extract_source_content(source_path):
    """Extract text content from source SOP."""
    with zipfile.ZipFile(source_path, 'r') as zf:
        xml_content = zf.read('word/document.xml').decode('utf-8')

    # Extract all text
    texts = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', xml_content)
    full_text = ' '.join(texts)

    content = {
        'sop_id': '',
        'title': '',
        'department': '',
        'related_sops': [],
        'purpose': '',
        'scope_intro': '',
        'scope_items': [],
        'roles': [],  # List of {'name': str, 'responsibilities': [str]}
        'requirements': [],
        'procedure': [],  # List of {'name': str, 'description': str}
        'appendix': [],
    }

    # Extract SOP ID and title from filename
    filename = source_path.name
    id_match = re.search(r'(9\.\d+\.\d+)', filename)
    if id_match:
        content['sop_id'] = id_match.group(1)

    title_match = re.search(r'9\.\d+\.\d+\s*[–-]\s*(.+?)(?:\.docx|$)', filename)
    if title_match:
        content['title'] = title_match.group(1).strip()

    # Parse structured content from full text
    # Department
    dept_match = re.search(r'Department:\s*([^R]+?)(?:Related|Purpose|$)', full_text)
    if dept_match:
        content['department'] = dept_match.group(1).strip()

    # Related SOPs - look for 9.x.xxx patterns after "Related SOPs:"
    related_section = re.search(r'Related SOPs:(.+?)(?:Purpose|$)', full_text)
    if related_section:
        related_text = related_section.group(1)
        # Find all SOP references
        sop_refs = re.findall(r'(9\.\d+\.\d+)\s*[-–]\s*([^9�]+?)(?=9\.\d|Purpose|$)', related_text)
        for sop_id, sop_title in sop_refs:
            content['related_sops'].append(f"{sop_id} – {sop_title.strip()}")

    # Purpose
    purpose_match = re.search(r'Purpose\s+(.+?)(?:Scope|$)', full_text)
    if purpose_match:
        content['purpose'] = purpose_match.group(1).strip()

    # Scope
    scope_match = re.search(r'Scope\s+(.+?)(?:Roles|$)', full_text, re.DOTALL)
    if scope_match:
        scope_text = scope_match.group(1).strip()
        # Check for intro line
        intro_match = re.match(r'(This SOP applies[^.]+\.)', scope_text)
        if intro_match:
            content['scope_intro'] = intro_match.group(1)
        else:
            applies_match = re.match(r'(Applies to[^:]+:?)', scope_text)
            if applies_match:
                content['scope_intro'] = applies_match.group(1)

    # Roles & Responsibilities - parse structured format
    roles_match = re.search(r'Roles & Responsibilities\s+(.+?)(?:Requirements|$)', full_text, re.DOTALL)
    if roles_match:
        roles_text = roles_match.group(1).strip()
        # Split by role patterns (Role Name: or Role Name (abbreviation):)
        role_sections = re.split(r'(?=(?:Branch Manager|General Superintendent|Project Manager|Foreman|Safety|Estimator|Purchasing|Admin|Lead Journeyman)[^:]*:)', roles_text)
        for section in role_sections:
            if not section.strip():
                continue
            # Extract role name and responsibilities
            role_match = re.match(r'([^:]+):\s*(.+)', section.strip())
            if role_match:
                role_name = role_match.group(1).strip()
                resp_text = role_match.group(2).strip()
                # Split responsibilities (they may be separated by periods or newlines)
                responsibilities = []
                for resp in re.split(r'(?<=[.!])\s+(?=[A-Z])', resp_text):
                    resp = resp.strip()
                    if resp and len(resp) > 5:
                        responsibilities.append(resp)
                if responsibilities:
                    content['roles'].append({
                        'name': role_name,
                        'responsibilities': responsibilities
                    })

    # Requirements
    req_match = re.search(r'Requirements\s+(.+?)(?:Procedure|$)', full_text, re.DOTALL)
    if req_match:
        req_text = req_match.group(1).strip()
        # Split by bullet markers or newlines
        for item in re.split(r'[•�]\s*', req_text):
            item = item.strip()
            if item and len(item) > 3 and not item.startswith('['):
                content['requirements'].append(item)

    # Procedure - parse steps
    proc_match = re.search(r'Procedure\s+(.+?)(?:Appendix|$)', full_text, re.DOTALL)
    if proc_match:
        proc_text = proc_match.group(1).strip()
        # Split by "Step N:" pattern
        step_sections = re.split(r'Step\s+(\d+):', proc_text)
        for i in range(1, len(step_sections), 2):
            if i + 1 < len(step_sections):
                step_num = step_sections[i]
                step_content = step_sections[i + 1].strip()
                # First line is typically the step name/trigger
                lines = step_content.split('�')
                if not lines:
                    lines = step_content.split('\n')
                step_name = lines[0].strip() if lines else f"Step {step_num}"
                step_desc = ' '.join(lines[1:]).strip() if len(lines) > 1 else step_content
                content['procedure'].append({
                    'number': step_num,
                    'name': step_name,
                    'description': step_desc
                })

    # Appendix
    app_match = re.search(r'Appendix\s+(.+?)$', full_text, re.DOTALL)
    if app_match:
        app_text = app_match.group(1).strip()
        # Extract document/form references
        for item in re.findall(r'(?:�|•|-)\s*([^�•\n]+)', app_text):
            item = item.strip()
            if item and len(item) > 3 and not item.startswith('['):
                content['appendix'].append(item)

    return content


def create_para_with_text(text, bold=False, keep_next=False, keep_lines=False, style=None, num_id=None, indent=None):
    """Create a Word paragraph element with text."""
    w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

    p = ET.Element(f'{w}p')
    pPr = ET.SubElement(p, f'{w}pPr')

    if keep_next:
        ET.SubElement(pPr, f'{w}keepNext')
    if keep_lines:
        ET.SubElement(pPr, f'{w}keepLines')
    if style:
        pStyle = ET.SubElement(pPr, f'{w}pStyle')
        pStyle.set(f'{w}val', style)
    if num_id is not None:
        numPr = ET.SubElement(pPr, f'{w}numPr')
        ilvl = ET.SubElement(numPr, f'{w}ilvl')
        ilvl.set(f'{w}val', '0')
        numIdEl = ET.SubElement(numPr, f'{w}numId')
        numIdEl.set(f'{w}val', str(num_id))
    if indent:
        ind = ET.SubElement(pPr, f'{w}ind')
        ind.set(f'{w}left', str(indent))

    # Create run with text
    r = ET.SubElement(p, f'{w}r')
    if bold:
        rPr = ET.SubElement(r, f'{w}rPr')
        ET.SubElement(rPr, f'{w}b')
        ET.SubElement(rPr, f'{w}bCs')

    t = ET.SubElement(r, f'{w}t')
    if text.startswith(' ') or text.endswith(' '):
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text

    return p


def create_hr_paragraph():
    """Create a horizontal rule paragraph."""
    w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    v = '{urn:schemas-microsoft-com:vml}'
    o = '{urn:schemas-microsoft-com:office:office}'
    w14 = '{http://schemas.microsoft.com/office/word/2010/wordml}'

    p = ET.Element(f'{w}p')
    pPr = ET.SubElement(p, f'{w}pPr')
    ET.SubElement(pPr, f'{w}keepLines')

    r = ET.SubElement(p, f'{w}r')
    pict = ET.SubElement(r, f'{w}pict')
    pict.set(f'{w14}anchorId', '00000000')

    rect = ET.SubElement(pict, f'{v}rect')
    rect.set('id', '_x0000_i1025')
    rect.set('style', 'width:0;height:1.5pt')
    rect.set(f'{o}hralign', 'center')
    rect.set(f'{o}hrstd', 't')
    rect.set(f'{o}hr', 't')
    rect.set('fillcolor', '#a0a0a0')
    rect.set('stroked', 'f')

    return p


def create_two_run_paragraph(label, value, label_bold=True, keep_next=False):
    """Create a paragraph with two runs - bold label and normal value."""
    w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

    p = ET.Element(f'{w}p')
    pPr = ET.SubElement(p, f'{w}pPr')
    if keep_next:
        ET.SubElement(pPr, f'{w}keepNext')

    # Label run (bold)
    r1 = ET.SubElement(p, f'{w}r')
    if label_bold:
        rPr1 = ET.SubElement(r1, f'{w}rPr')
        ET.SubElement(rPr1, f'{w}b')
        ET.SubElement(rPr1, f'{w}bCs')
    t1 = ET.SubElement(r1, f'{w}t')
    t1.text = label

    # Value run (normal)
    r2 = ET.SubElement(p, f'{w}r')
    t2 = ET.SubElement(r2, f'{w}t')
    t2.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t2.text = ' ' + value

    return p


def create_empty_paragraph():
    """Create an empty paragraph for spacing."""
    w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    p = ET.Element(f'{w}p')
    return p


def build_document_body(content):
    """Build the document body XML from content."""
    w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

    body = ET.Element(f'{w}body')

    # === HEADER BLOCK ===
    # SOP Title (bold)
    title_text = f"SOP: {content['sop_id']} – {content['title']}"
    body.append(create_para_with_text(title_text, bold=True, keep_next=True))

    # Department (bold label, normal value)
    body.append(create_two_run_paragraph("Department:", content['department'] or "Project Management / Operations", keep_next=True))

    # Related SOPs label (bold)
    body.append(create_para_with_text("Related SOPs:", bold=True, keep_next=True))

    # Related SOP entries (normal, no bullets)
    for related in content['related_sops']:
        body.append(create_para_with_text(related, keep_next=True, keep_lines=True))

    # Horizontal rule
    body.append(create_hr_paragraph())

    # === PURPOSE ===
    body.append(create_para_with_text("Purpose", bold=True, keep_next=True, keep_lines=True))
    body.append(create_para_with_text(content['purpose'], keep_lines=True))
    body.append(create_empty_paragraph())

    # Horizontal rule
    body.append(create_hr_paragraph())

    # === SCOPE ===
    body.append(create_para_with_text("Scope", bold=True, keep_next=True, keep_lines=True))
    if content['scope_intro']:
        body.append(create_para_with_text(content['scope_intro'], keep_lines=True))

    # Scope bullet items (using numId=37 from template)
    for item in content['scope_items']:
        body.append(create_para_with_text(item, style='ListParagraph', num_id=37, keep_lines=True))

    body.append(create_empty_paragraph())

    # Horizontal rule
    body.append(create_hr_paragraph())

    # === ROLES & RESPONSIBILITIES ===
    body.append(create_para_with_text("Roles & Responsibilities", bold=True, keep_next=True))

    for role in content['roles']:
        # Role name (normal text, not bold)
        body.append(create_para_with_text(role['name'], keep_next=True))
        # Responsibilities as bullets
        for resp in role['responsibilities']:
            body.append(create_para_with_text(resp, style='ListParagraph', num_id=37, keep_lines=True))
        body.append(create_empty_paragraph())

    # Horizontal rule
    body.append(create_hr_paragraph())

    # === REQUIREMENTS ===
    body.append(create_para_with_text("Requirements", bold=True, keep_next=True, keep_lines=True))

    for req in content['requirements']:
        body.append(create_para_with_text(req, style='ListParagraph', num_id=37, keep_lines=True))

    body.append(create_empty_paragraph())

    # Horizontal rule
    body.append(create_hr_paragraph())

    # === PROCEDURE ===
    body.append(create_para_with_text("Procedure", bold=True, keep_next=True, keep_lines=True))

    for step in content['procedure']:
        # Step header (bold, indented)
        step_header = f"Step {step['number']} – {step['name']}"
        body.append(create_para_with_text(step_header, bold=True, keep_next=True, indent=360))
        # Step description (normal, indented)
        if step.get('description'):
            body.append(create_para_with_text(step['description'], indent=360, keep_lines=True))
        body.append(create_empty_paragraph())

    # === APPENDIX ===
    body.append(create_para_with_text("Appendix", bold=True, keep_next=True, keep_lines=True))

    for item in content['appendix']:
        body.append(create_para_with_text(item, style='ListParagraph', num_id=37, keep_lines=True))

    # Section break at end
    sectPr = ET.SubElement(body, f'{w}sectPr')

    return body


def update_core_properties(xml_content, content):
    """Update core.xml with SOP metadata."""
    root = ET.fromstring(xml_content)

    ns = {
        'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'dcterms': 'http://purl.org/dc/terms/',
    }

    # Update title
    title_el = root.find('dc:title', ns)
    if title_el is not None:
        title_el.text = f"SOP: {content['sop_id']} – {content['title']}"

    # Update subject
    subject_el = root.find('dc:subject', ns)
    if subject_el is not None:
        subject_el.text = content['department']

    # Update keywords
    keywords_el = root.find('cp:keywords', ns)
    if keywords_el is not None:
        keywords_el.text = f"{content['sop_id']}, {content['department']}, {content['title']}"

    # Update description
    desc_el = root.find('dc:description', ns)
    if desc_el is not None:
        desc_el.text = content['purpose'][:500] if content['purpose'] else ''

    # Update modified date
    modified_el = root.find('dcterms:modified', ns)
    if modified_el is not None:
        modified_el.text = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    return ET.tostring(root, encoding='unicode', xml_declaration=True)


def update_custom_properties(xml_content, content, raci):
    """Update custom.xml with SharePoint metadata."""
    root = ET.fromstring(xml_content)

    vt = 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'
    ET.register_namespace('vt', vt)

    # Add RACI properties
    pid = 3

    # (RACI)Responsible
    prop = ET.SubElement(root, 'property')
    prop.set('fmtid', '{D5CDD505-2E9C-101B-9397-08002B2CF9AE}')
    prop.set('pid', str(pid))
    prop.set('name', '(RACI)Responsible')
    lpwstr = ET.SubElement(prop, f'{{{vt}}}lpwstr')
    lpwstr.text = ', '.join(raci.get('responsible', []))
    pid += 1

    # (RACI)Accountable
    prop = ET.SubElement(root, 'property')
    prop.set('fmtid', '{D5CDD505-2E9C-101B-9397-08002B2CF9AE}')
    prop.set('pid', str(pid))
    prop.set('name', '(RACI)Accountable')
    lpwstr = ET.SubElement(prop, f'{{{vt}}}lpwstr')
    lpwstr.text = ', '.join(raci.get('accountable', []))
    pid += 1

    # Roles(RACI)
    prop = ET.SubElement(root, 'property')
    prop.set('fmtid', '{D5CDD505-2E9C-101B-9397-08002B2CF9AE}')
    prop.set('pid', str(pid))
    prop.set('name', 'Roles(RACI)')
    lpwstr = ET.SubElement(prop, f'{{{vt}}}lpwstr')
    all_roles = [r['name'] for r in content['roles']]
    lpwstr.text = ';#' + ';#'.join(all_roles) + ';#' if all_roles else ''

    return ET.tostring(root, encoding='unicode', xml_declaration=True)


def update_sharepoint_metadata(xml_content, content, raci):
    """Update customXml/item4.xml with SharePoint column values."""
    root = ET.fromstring(xml_content)

    sp_ns = 'b11c1c0a-1848-4118-b7cf-ce9450f86f68'
    xsi_ns = 'http://www.w3.org/2001/XMLSchema-instance'

    # Find documentManagement element
    doc_mgmt = None
    for child in root:
        if 'documentManagement' in child.tag:
            doc_mgmt = child
            break

    if doc_mgmt is None:
        return xml_content

    field_values = {
        'SOPID': content['sop_id'],
        'SOPFileName': f"{content['sop_id']} – {content['title']}.docx",
        'Description': content['title'],
        'Department_x002f_Division': content['department'],
        'Status': 'Draft',
        'RACI_Responsible': ', '.join(raci.get('responsible', [])),
        'RACI_Accountable': ', '.join(raci.get('accountable', [])),
        'RACI_Consulted': ', '.join(raci.get('consulted', [])),
        'RACI_Informed': ', '.join(raci.get('informed', [])),
        'RelatedSOPs': ', '.join([r.split(' – ')[0] for r in content['related_sops']]),
    }

    for child in doc_mgmt:
        local_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag

        if local_name in field_values and field_values[local_name]:
            # Remove xsi:nil attribute
            nil_attr = f'{{{xsi_ns}}}nil'
            if nil_attr in child.attrib:
                del child.attrib[nil_attr]
            child.text = str(field_values[local_name])

    return ET.tostring(root, encoding='unicode', xml_declaration=True)


def determine_raci(content):
    """Determine RACI assignments from content."""
    raci = {'responsible': [], 'accountable': [], 'consulted': [], 'informed': []}

    # Get all role names
    role_names = [r['name'] for r in content['roles']]

    # Determine responsible based on title/content
    title_lower = content['title'].lower()

    if 'branch manager' in ' '.join(role_names).lower():
        raci['responsible'] = ['Branch Manager']
    elif 'project manager' in title_lower or 'pm' in title_lower:
        raci['responsible'] = ['Project Manager']
    elif 'foreman' in title_lower or 'field' in title_lower:
        raci['responsible'] = ['Foreman']
    elif 'safety' in title_lower:
        raci['responsible'] = ['Safety']
    else:
        # Default to first role
        if role_names:
            raci['responsible'] = [role_names[0]]
        else:
            raci['responsible'] = ['Project Manager']

    # Determine accountable
    if raci['responsible'][0] in ['Foreman', 'Safety', 'Lead Journeyman']:
        raci['accountable'] = ['General Superintendent']
    elif raci['responsible'][0] in ['Project Manager', 'Branch Manager']:
        raci['accountable'] = ['Operations Manager']
    else:
        raci['accountable'] = ['Project Manager']

    # Consulted = other roles mentioned
    for role in role_names:
        if role not in raci['responsible'] and role not in raci['accountable']:
            raci['consulted'].append(role)

    raci['consulted'] = raci['consulted'][:3]

    return raci


def generate_sop(source_path, output_path):
    """Generate a properly formatted SOP from source."""

    # Extract content from source
    content = extract_source_content(source_path)

    if not content['sop_id']:
        return None, "No SOP ID found"

    # Determine RACI
    raci = determine_raci(content)

    # Copy template to output
    shutil.copy2(TEMPLATE_PATH, output_path)

    # Read template and modify
    temp_path = output_path.with_suffix('.tmp')

    with zipfile.ZipFile(output_path, 'r') as zf_in:
        with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as zf_out:
            for item in zf_in.namelist():
                data = zf_in.read(item)

                if item == 'word/document.xml':
                    # Build new document body
                    # For now, we'll do placeholder replacement
                    # Full XML rebuild would be more complex
                    xml_content = data.decode('utf-8')

                    # Replace placeholders
                    xml_content = xml_content.replace('[SOP #] – [SOP Title]', f"{content['sop_id']} – {content['title']}")
                    xml_content = xml_content.replace('[Department(s)]', content['department'] or 'Project Management / Operations')

                    # Replace purpose placeholder
                    xml_content = re.sub(
                        r'\[Describe the purpose[^\]]*\]',
                        content['purpose'] if content['purpose'] else 'To establish standardized procedures for this activity.',
                        xml_content
                    )

                    data = xml_content.encode('utf-8')

                elif item == 'docProps/core.xml':
                    data = update_core_properties(data.decode('utf-8'), content).encode('utf-8')

                elif item == 'docProps/custom.xml':
                    data = update_custom_properties(data.decode('utf-8'), content, raci).encode('utf-8')

                elif item == 'customXml/item4.xml':
                    data = update_sharepoint_metadata(data.decode('utf-8'), content, raci).encode('utf-8')

                zf_out.writestr(item, data)

    temp_path.replace(output_path)

    return {
        'sop_id': content['sop_id'],
        'title': content['title'],
        'raci': raci
    }, None


def main():
    print("=" * 60)
    print("GENERATE SOP WITH PROPER FORMATTING")
    print("=" * 60)

    # Process single SOP for testing
    test_sop = SOURCE_DIR / "9.2.010 – Team Selection.docx"
    output_path = OUTPUT_DIR / test_sop.name

    print(f"\nProcessing: {test_sop.name}")

    result, error = generate_sop(test_sop, output_path)

    if result:
        print(f"  [OK] Generated: {result['sop_id']} – {result['title']}")
        print(f"       RACI: R={result['raci']['responsible']}, A={result['raci']['accountable']}")
    else:
        print(f"  [ERR] {error}")

    print(f"\nOutput: {output_path}")


if __name__ == "__main__":
    main()
