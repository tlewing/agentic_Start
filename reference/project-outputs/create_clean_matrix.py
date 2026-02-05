#!/usr/bin/env python3
"""
Create Clean Key_SOP_Matrix.xlsx
================================
Uses authoritative SOP list as source of truth for IDs and Titles.
Matches to files in Revised SOPs folder for content extraction.
"""

import csv
import re
from datetime import datetime, timedelta
from pathlib import Path
from docx import Document
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Regex pattern for illegal XML characters
ILLEGAL_CHARS_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')


def clean_text(text):
    """Remove control characters that are illegal in Excel/XML."""
    if not text:
        return ""
    cleaned = ILLEGAL_CHARS_RE.sub('', text)
    cleaned = re.sub(r'^[=\s]+', '', cleaned)
    cleaned = re.sub(r'[=\s]+$', '', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()


def style_header_row(ws, num_cols):
    """Apply consistent header styling."""
    header_font = Font(bold=True, color="FFFFFF", size=11)
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    for col in range(1, num_cols + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def find_file_for_sop(sop_id, files_dict):
    """Find the matching file for a given SOP ID."""
    return files_dict.get(sop_id)


def extract_content_from_doc(doc_path):
    """Extract purpose, scope, and roles from a Word document."""
    try:
        doc = Document(doc_path)
    except Exception as e:
        return {'purpose': '', 'scope': '', 'roles': [], 'department': ''}

    content = {
        'purpose': '',
        'scope': '',
        'roles': [],
        'department': ''
    }

    current_section = None
    section_text = []

    for para in doc.paragraphs:
        text = clean_text(para.text)
        if not text:
            continue

        # Get department
        if text.startswith('Department:'):
            content['department'] = text.replace('Department:', '').strip()
            continue

        # Section headers
        if text == 'PURPOSE':
            current_section = 'purpose'
            section_text = []
            continue
        elif text == 'SCOPE':
            if current_section == 'purpose':
                content['purpose'] = ' '.join(section_text)
            current_section = 'scope'
            section_text = []
            continue
        elif text in ['ROLES & RESPONSIBILITIES', 'ROLES AND RESPONSIBILITIES']:
            if current_section == 'scope':
                content['scope'] = ' '.join(section_text)
            current_section = 'roles'
            section_text = []
            continue
        elif text in ['REQUIREMENTS', 'PROCEDURE'] or text.startswith('====='):
            if current_section == 'purpose':
                content['purpose'] = ' '.join(section_text)
            elif current_section == 'scope':
                content['scope'] = ' '.join(section_text)
            elif current_section == 'roles':
                content['roles'] = section_text.copy()
            current_section = None
            section_text = []
            continue

        # Collect section content
        if current_section:
            if current_section == 'roles':
                # Check for RACI pattern
                if re.search(r'\([RACI]\)', text):
                    section_text.append(text)
                elif section_text and re.search(r'\([RACI]\)', section_text[-1]):
                    # Append description to previous role
                    section_text[-1] = section_text[-1] + ' | ' + text
            else:
                section_text.append(text)

    # Save any remaining content
    if current_section == 'purpose':
        content['purpose'] = ' '.join(section_text)
    elif current_section == 'scope':
        content['scope'] = ' '.join(section_text)
    elif current_section == 'roles':
        content['roles'] = section_text

    return content


def parse_roles(roles_list):
    """Parse roles with RACI designations."""
    parsed = []
    for role_text in roles_list:
        match = re.match(r'^([^(]+)\s*\(([RACI])\)', role_text)
        if match:
            role_name = match.group(1).strip()
            raci = match.group(2)
            remainder = role_text[match.end():].strip()
            desc = remainder.split(' | ', 1)[1].strip() if ' | ' in remainder else remainder.lstrip('| ').strip()
            parsed.append({'role': role_name, 'raci': raci, 'description': desc})
    return parsed


def infer_roles(sop_id, title, purpose, scope):
    """Infer roles from SOP content when not explicitly defined."""
    combined = f"{title} {purpose} {scope}".lower()
    inferred = []
    added = set()

    rules = [
        (['safety meeting', 'safety orientation', 'safety inspection', 'safety audit', 'accident', 'incident', 'emergency'],
         'Safety Coordinator', 'R', 'Leads safety activities'),
        (['safety'], 'Safety Coordinator', 'C', 'Reviews for safety compliance'),
        (['quality meeting', 'quality inspection', 'nonconformance', 'ncr', 'quality management'],
         'Quality Inspector', 'R', 'Performs quality activities'),
        (['quality', 'punch list'], 'Quality Inspector', 'C', 'Provides quality oversight'),
        (['purchase order', 'procurement', 'vendor', 'supplier', 'expedit', 'delivery', 'material receiving', 'inventory'],
         'Purchasing', 'R', 'Manages procurement'),
        (['billing', 'pay application', 'invoice', 'accounts receivable', 'retainage', 'cost code', 'job cost', 'reconcile'],
         'Accounting', 'R', 'Manages financial documentation'),
        (['budget', 'cost', 'profit', 'forecast'], 'Accounting', 'C', 'Provides financial support'),
        (['subcontractor'], 'Subcontractors', 'R', 'Performs subcontracted work'),
        (['prefab', 'prefabrication'], 'Prefabrication Lead', 'R', 'Coordinates prefabrication'),
        (['foreman meeting', 'daily huddle', 'crew'], 'Foreman', 'R', 'Leads crew activities'),
        (['daily report', 'production', 'manpower', 'field coordination', 'field problem', 'field rework'],
         'Field Supervisor', 'R', 'Manages field operations'),
        (['general superintendent', 'resource allocation'], 'General Superintendent', 'A', 'Approves resource allocations'),
        (['schedule', 'lookahead'], 'Superintendent', 'C', 'Coordinates scheduling'),
        (['site administrator', 'filing', 'correspondence', 'meeting minutes', 'documentation system', 'archive'],
         'Site Administrator', 'R', 'Manages documentation'),
        (['branch manager', 'claims'], 'Branch Manager', 'A', 'Provides executive approval'),
        (['client', 'owner'], 'Branch Manager', 'C', 'Participates in client communications'),
        (['estimat'], 'Estimator', 'C', 'Provides estimating support'),
        (['change order', 'scope', 'backcharge', 'force account'], 'Project Manager', 'R', 'Manages contract changes'),
        (['turnover', 'closeout', 'warranty', 'o&m'], 'Project Manager', 'A', 'Oversees closeout'),
        (['setup', 'mobilization', 'trailer', 'temporary'], 'Field Supervisor', 'R', 'Coordinates site setup'),
        (['coordination meeting', 'kickoff'], 'Project Manager', 'R', 'Leads coordination'),
        (['rfi', 'submittal', 'drawing', 'specification'], 'Project Manager', 'R', 'Manages technical documentation'),
        (['communication'], 'Project Manager', 'R', 'Manages communications'),
    ]

    for keywords, role, raci, desc in rules:
        if any(kw in combined for kw in keywords):
            if role not in added:
                inferred.append({'role': role, 'raci': raci, 'description': f"{desc} for {title}"})
                added.add(role)

    # Always add PM if not present
    if 'Project Manager' not in added:
        phase = sop_id.split('.')[1] if '.' in sop_id else ''
        pm_raci = 'A' if phase in ['2', '4', '6'] else 'R'
        inferred.append({'role': 'Project Manager', 'raci': pm_raci, 'description': f"Oversees {title}"})
        added.add('Project Manager')

    # Add Field Supervisor for execution phases
    if sop_id.startswith('9.3.') or sop_id.startswith('9.4.'):
        if 'Field Supervisor' not in added:
            inferred.append({'role': 'Field Supervisor', 'raci': 'C', 'description': f"Field coordination for {title}"})

    return inferred


def get_phase(sop_id):
    """Get phase from SOP ID."""
    if sop_id.startswith('9.1.'): return "1 - Estimating"
    if sop_id.startswith('9.2.'): return "2 - Preconstruction"
    if sop_id.startswith('9.3.'): return "3 - Mobilization"
    if sop_id.startswith('9.4.'): return "4 - Execution"
    if sop_id.startswith('9.5.'): return "5 - Commissioning"
    if sop_id.startswith('9.6.'): return "6 - Closeout"
    return "Unknown"


def get_directive(role):
    """Get directive section for a role."""
    if 'Project Manager' in role: return "Sec. 9.5 PM Directives"
    if 'Field' in role or 'Foreman' in role: return "Sec. 9.3 Field Leadership"
    if 'Safety' in role: return "Sec. 9.7 Safety Directives"
    if 'Superintendent' in role: return "Sec. 9.4 Superintendent Directives"
    if 'Branch' in role: return "Sec. 9.6 Branch Management"
    if 'Purchasing' in role: return "Sec. 9.10 Purchasing Directives"
    if 'Accounting' in role: return "Sec. 9.11 Accounting Directives"
    if 'Quality' in role: return "Sec. 9.13 Quality Directives"
    if 'Estimat' in role: return "Sec. 9.9 Estimating Directives"
    if 'Site Administrator' in role: return "Sec. 9.8 Site Administration"
    return "Sec. 9.2 General Directives"


def main():
    auth_csv = r"C:\Users\tewing\Desktop\Claude Projects\Project Outputs\Authoritative_SOP_List.csv"
    sops_folder = Path(r"C:\Users\tewing\Desktop\Claude Projects\Revised SOPs")
    output_path = r"C:\Users\tewing\Desktop\Claude Projects\Project Outputs\Key_SOP_Matrix_Clean.xlsx"

    # Load authoritative list
    auth_sops = []
    with open(auth_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            auth_sops.append({'sop_id': row['SOPID'], 'title': row['Title']})

    print(f"Loaded {len(auth_sops)} SOPs from authoritative list")

    # Build file lookup by SOP ID
    files_dict = {}
    for f in sops_folder.glob('*.docx'):
        if f.name.startswith('~$'):
            continue
        match = re.match(r'^(\d+\.\d+\.\d+)', f.stem)
        if match:
            files_dict[match.group(1)] = f

    print(f"Found {len(files_dict)} SOP files")

    # Process each SOP
    all_sops = []
    all_coverage = []
    all_raci = []
    all_roles_set = set()
    matched = 0
    unmatched = []

    for sop in auth_sops:
        sop_id = sop['sop_id']
        title = sop['title']
        file_path = find_file_for_sop(sop_id, files_dict)

        if file_path:
            matched += 1
            content = extract_content_from_doc(file_path)
            filename = file_path.name
        else:
            unmatched.append(sop_id)
            content = {'purpose': '', 'scope': '', 'roles': [], 'department': 'Operations'}
            filename = f"{sop_id} - {title}.docx"

        # Parse or infer roles
        parsed_roles = parse_roles(content['roles'])
        if not parsed_roles:
            parsed_roles = infer_roles(sop_id, title, content['purpose'], content['scope'])
            roles_inferred = True
        else:
            roles_inferred = False

        phase = get_phase(sop_id)
        sop_title = f"{sop_id} - {title}"

        # Store SOP data
        all_sops.append({
            'sop_id': sop_id,
            'title': title,
            'filename': filename,
            'purpose': content['purpose'],
            'scope': content['scope'],
            'department': content['department'] or 'Operations',
            'parsed_roles': parsed_roles,
            'roles_inferred': roles_inferred,
            'phase': phase
        })

        # Build coverage/RACI entries
        for pr in parsed_roles:
            all_roles_set.add(pr['role'])
            directive = get_directive(pr['role'])
            status = 'Inferred' if roles_inferred else 'Covered'

            all_coverage.append({
                'sop_title': sop_title,
                'action': pr['description'][:200] if pr['description'] else f"Executes {title.lower()}",
                'role': pr['role'],
                'directive': directive,
                'status': status,
                'recommendation': 'Verify role assignment.' if roles_inferred else 'No change required.',
                'category': phase
            })

            all_raci.append({
                'sop_title': sop_title,
                'action': pr['description'][:200] if pr['description'] else f"Executes {title.lower()}",
                'role': pr['role'],
                'directive': directive,
                'status': status,
                'recommendation': 'Verify role assignment.' if roles_inferred else 'No change required.',
                'category': phase,
                'raci': pr['raci']
            })

    print(f"\nMatched: {matched}/{len(auth_sops)} SOPs")
    if unmatched:
        print(f"Unmatched: {unmatched}")
    print(f"Unique roles: {len(all_roles_set)}")
    print(f"Coverage entries: {len(all_coverage)}")

    # Create workbook
    wb = Workbook()

    # Sheet 1: GSL_SOP_Metadata
    ws1 = wb.active
    ws1.title = "GSL_SOP_Metadata"
    headers = ["SOP ID", "Name", "SOP File Name", "Title", "Description", "Phase",
               "Category", "Roles (RACI)", "Discipline", "Status", "Document Type"]
    ws1.append(headers)

    for sop in all_sops:
        roles_str = '; '.join([f"{r['role']} ({r['raci']})" for r in sop['parsed_roles']])
        if sop['roles_inferred']:
            roles_str = "[Inferred] " + roles_str
        desc = sop['purpose'][:500] + "..." if len(sop['purpose']) > 500 else sop['purpose']

        ws1.append([
            sop['sop_id'],
            f"{sop['sop_id']} - {sop['title']}",
            sop['filename'],
            sop['title'],
            desc,
            sop['phase'],
            sop['phase'].split(' - ')[1] if ' - ' in sop['phase'] else sop['phase'],
            roles_str,
            sop['department'],
            "Approved",
            "SOP"
        ])

    style_header_row(ws1, len(headers))
    ws1.column_dimensions['A'].width = 12
    ws1.column_dimensions['B'].width = 55
    ws1.column_dimensions['C'].width = 55
    ws1.column_dimensions['D'].width = 45
    ws1.column_dimensions['E'].width = 70
    ws1.column_dimensions['H'].width = 60

    # Sheet 2: Coverage Matrix
    ws2 = wb.create_sheet("Coverage Matrix")
    cov_headers = ["SOP Title", "SOP Action", "Responsible Role", "Directive Section",
                   "Coverage Status", "Gap Closure Recommendation", "Category"]
    ws2.append(cov_headers)
    for entry in all_coverage:
        ws2.append([entry['sop_title'], entry['action'], entry['role'], entry['directive'],
                    entry['status'], entry['recommendation'], entry['category']])
    style_header_row(ws2, len(cov_headers))

    # Sheet 3: RACI Matrix
    ws3 = wb.create_sheet("RACI Matrix")
    raci_headers = cov_headers + ["RACI"]
    ws3.append(raci_headers)
    for entry in all_raci:
        ws3.append([entry['sop_title'], entry['action'], entry['role'], entry['directive'],
                    entry['status'], entry['recommendation'], entry['category'], entry['raci']])
    style_header_row(ws3, len(raci_headers))

    # Sheet 4: Role Alignment Matrix
    ws4 = wb.create_sheet("Role Alignment Matrix")
    all_roles = sorted(list(all_roles_set))
    role_headers = ["SOP ID", "SOP Title", "Phase"] + all_roles
    ws4.append(role_headers)

    for sop in all_sops:
        sop_roles = {r['role']: r['raci'] for r in sop['parsed_roles']}
        row = [sop['sop_id'], f"{sop['sop_id']} - {sop['title']}", sop['phase']]
        for role in all_roles:
            if role in sop_roles:
                raci = sop_roles[role]
                if sop['roles_inferred']:
                    raci = f"{raci}*"
                row.append(raci)
            else:
                row.append(None)
        ws4.append(row)

    style_header_row(ws4, len(role_headers))
    ws4.column_dimensions['A'].width = 12
    ws4.column_dimensions['B'].width = 55

    # Save
    wb.save(output_path)
    print(f"\nSaved to: {output_path}")
    print(f"Sheets: {len(wb.sheetnames)}")
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        print(f"  {sheet}: {ws.max_row} rows x {ws.max_column} cols")


if __name__ == "__main__":
    main()
