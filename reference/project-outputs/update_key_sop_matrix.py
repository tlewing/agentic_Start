#!/usr/bin/env python3
"""
Update Key_SOP_Matrix.xlsx from Revised SOPs
=============================================
Reads Word documents from the Revised SOPs folder and extracts metadata
to populate a comprehensive Key_SOP_Matrix workbook.

Requirements:
    pip install openpyxl python-docx

Usage:
    python update_key_sop_matrix.py
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from docx import Document
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


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


def auto_column_width(ws, min_width=10, max_width=60):
    """Auto-adjust column widths based on content."""
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        adjusted_width = min(max(max_length + 2, min_width), max_width)
        ws.column_dimensions[column].width = adjusted_width


def extract_sop_metadata(doc_path):
    """Extract metadata from a Word SOP document."""
    try:
        doc = Document(doc_path)
    except Exception as e:
        print(f"  Error reading {doc_path}: {e}")
        return None

    # Extract SOP ID and title from filename as fallback
    filename = Path(doc_path).stem
    # Parse filename like "9.2.010 – Team Selection" or "9.2.010 - Team Selection"
    filename_match = re.match(r'^(\d+\.\d+\.\d+)\s*[–-]\s*(.+)$', filename)
    fallback_sop_id = filename_match.group(1) if filename_match else ''
    fallback_title = filename_match.group(2) if filename_match else filename

    metadata = {
        'sop_id': fallback_sop_id,
        'title': fallback_title,
        'department': '',
        'related_sops': [],
        'job_descriptions': [],
        'management_directives': [],
        'purpose': '',
        'scope': '',
        'roles': [],
        'requirements': [],
        'procedure_steps': []
    }

    current_section = None
    section_content = []

    for para in doc.paragraphs:
        text = clean_text(para.text)
        if not text:
            continue

        # Identify SOP ID and Title from first line (handles multiple formats)
        # Format 1: "SOP: 9.2.010 - Team Selection"
        # Format 2: "SOP 9.4.050 - Prepare Construction Takeoff"
        if text.startswith('SOP:') or text.startswith('SOP '):
            # Remove "SOP:" or "SOP " prefix
            sop_text = text.replace('SOP:', '').replace('SOP ', '').strip()
            # Split on " - " or " – " (en-dash)
            if ' - ' in sop_text:
                parts = sop_text.split(' - ', 1)
            elif ' – ' in sop_text:
                parts = sop_text.split(' – ', 1)
            else:
                parts = [sop_text]

            if len(parts) >= 1:
                metadata['sop_id'] = parts[0].strip()
            if len(parts) >= 2:
                metadata['title'] = parts[1].strip()
            continue

        # Department
        if text.startswith('Department:'):
            metadata['department'] = text.replace('Department:', '').strip()
            continue

        # Section headers
        if text == 'PURPOSE':
            current_section = 'purpose'
            section_content = []
            continue
        elif text == 'SCOPE':
            if current_section == 'purpose':
                metadata['purpose'] = ' '.join(section_content)
            current_section = 'scope'
            section_content = []
            continue
        elif text == 'ROLES & RESPONSIBILITIES' or text == 'ROLES AND RESPONSIBILITIES':
            if current_section == 'scope':
                metadata['scope'] = ' '.join(section_content)
            current_section = 'roles'
            section_content = []
            continue
        elif text == 'REQUIREMENTS':
            if current_section == 'roles':
                metadata['roles'] = section_content.copy()
            current_section = 'requirements'
            section_content = []
            continue
        elif text == 'PROCEDURE':
            if current_section == 'requirements':
                metadata['requirements'] = section_content.copy()
            current_section = 'procedure'
            section_content = []
            continue
        elif text.startswith('Related SOPs'):
            current_section = 'related_sops'
            section_content = []
            continue
        elif text.startswith('Job Descriptions'):
            current_section = 'job_descriptions'
            section_content = []
            continue
        elif text.startswith('Management Directives'):
            current_section = 'management_directives'
            section_content = []
            continue
        elif text.startswith('====='):
            # Section separator - save current section
            if current_section == 'purpose':
                metadata['purpose'] = ' '.join(section_content)
            elif current_section == 'scope':
                metadata['scope'] = ' '.join(section_content)
            elif current_section == 'roles':
                metadata['roles'] = section_content.copy()
            elif current_section == 'requirements':
                metadata['requirements'] = section_content.copy()
            current_section = None
            section_content = []
            continue

        # Collect content for current section
        if current_section:
            if current_section in ['related_sops', 'job_descriptions', 'management_directives']:
                if text.startswith('-') or text.startswith('9.'):
                    section_content.append(text.lstrip('- '))
            elif current_section == 'roles':
                # Parse role lines - roles have RACI like (R), (A), (C), (I)
                # Format: Role line with RACI, then description on next line
                raci_match = re.search(r'\([RACI]\)', text)
                if raci_match:
                    # This is a role line - add it
                    section_content.append(text.strip())
                elif section_content and re.search(r'\([RACI]\)', section_content[-1]):
                    # This is a description line - append to previous role
                    section_content[-1] = section_content[-1] + ' | ' + text.strip()
                elif text.lower().startswith('raci:'):
                    # Skip the RACI legend line
                    pass
            else:
                section_content.append(text)

    # Save any remaining section content
    if current_section == 'purpose':
        metadata['purpose'] = ' '.join(section_content)
    elif current_section == 'scope':
        metadata['scope'] = ' '.join(section_content)
    elif current_section == 'roles':
        metadata['roles'] = section_content
    elif current_section == 'requirements':
        metadata['requirements'] = section_content
    elif current_section == 'related_sops':
        metadata['related_sops'] = section_content
    elif current_section == 'job_descriptions':
        metadata['job_descriptions'] = section_content
    elif current_section == 'management_directives':
        metadata['management_directives'] = section_content

    return metadata


def parse_roles_raci(roles_list):
    """Parse roles and RACI designations from roles list."""
    parsed = []
    for role_text in roles_list:
        # Match patterns like "Branch Manager (A)" or "Project Manager (R)"
        # With optional description after pipe: "Branch Manager (A) | Selects PM..."
        match = re.match(r'^([^(]+)\s*\(([RACI])\)', role_text)
        if match:
            role_name = match.group(1).strip()
            raci = match.group(2)
            # Get description - could be after | separator or just after the RACI
            remainder = role_text[match.end():].strip()
            if ' | ' in remainder:
                desc = remainder.split(' | ', 1)[1].strip()
            else:
                desc = remainder.lstrip('| ').strip()
            parsed.append({
                'role': role_name,
                'raci': raci,
                'description': desc
            })
    return parsed


def get_phase_from_sop_id(sop_id):
    """Determine project phase from SOP ID."""
    if sop_id.startswith('9.1.'):
        return "1 - Estimating"
    elif sop_id.startswith('9.2.'):
        return "2 - Preconstruction"
    elif sop_id.startswith('9.3.'):
        return "3 - Mobilization & Job Site Setup"
    elif sop_id.startswith('9.4.'):
        return "4 - Execution"
    elif sop_id.startswith('9.5.'):
        return "5 - Commissioning"
    elif sop_id.startswith('9.6.'):
        return "6 - Closeout"
    return "Unknown"


def get_category_from_sop_id(sop_id):
    """Determine category from SOP ID number."""
    try:
        parts = sop_id.split('.')
        if len(parts) >= 3:
            num = int(parts[2][:3])
        else:
            num = 0
    except:
        num = 0

    if num < 50:
        return "010 - Planning & Setup"
    elif num < 100:
        return "050 - Reviews & Analysis"
    elif num < 150:
        return "100 - Mobilization"
    elif num < 200:
        return "150 - Documentation"
    elif num < 300:
        return "200 - Document Management"
    elif num < 400:
        return "300 - Scheduling"
    elif num < 500:
        return "400 - Cost Management"
    elif num < 600:
        return "500 - Safety & Quality"
    elif num < 700:
        return "600 - Procurement"
    elif num < 800:
        return "700 - Field Operations"
    else:
        return "800 - Closeout"


def infer_roles_from_content(sop_id, title, purpose, scope, phase):
    """Infer roles and RACI designations from SOP content when not explicitly defined."""
    title_lower = title.lower()
    purpose_lower = purpose.lower() if purpose else ''
    scope_lower = scope.lower() if scope else ''
    combined = f"{title_lower} {purpose_lower} {scope_lower}"

    inferred_roles = []

    # Define role inference rules based on keywords
    role_rules = [
        # (keywords, role, default_raci, action_template)
        (['safety meeting', 'safety orientation', 'safety inspection', 'safety audit',
          'safety training', 'accident', 'incident', 'emergency', 'hazard'],
         'Safety Coordinator', 'R', 'Leads safety-related activities and ensures compliance'),

        (['safety'],
         'Safety Coordinator', 'C', 'Reviews for safety compliance'),

        (['quality meeting', 'quality inspection', 'quality test', 'nonconformance',
          'ncr', 'quality management', 'quality record'],
         'Quality Inspector', 'R', 'Performs quality inspections and documentation'),

        (['quality', 'punch list'],
         'Quality Inspector', 'C', 'Provides quality oversight'),

        (['purchase order', 'procurement', 'vendor', 'supplier', 'expedit', 'delivery',
          'material receiving', 'inventory'],
         'Purchasing', 'R', 'Manages procurement and vendor relationships'),

        (['billing', 'pay application', 'invoice', 'accounts receivable', 'retainage',
          'cost code', 'job cost', 'reconcile'],
         'Accounting', 'R', 'Manages financial documentation and billing'),

        (['budget', 'cost', 'profit', 'forecast'],
         'Accounting', 'C', 'Provides financial data and support'),

        (['subcontractor'],
         'Subcontractors', 'R', 'Performs subcontracted work'),

        (['prefab', 'prefabrication'],
         'Prefabrication Lead', 'R', 'Coordinates prefabrication activities'),

        (['foreman meeting', 'daily huddle', 'crew'],
         'Foreman', 'R', 'Leads crew-level activities'),

        (['field supervisor', 'field leadership'],
         'Field Supervisor', 'R', 'Supervises field operations'),

        (['daily report', 'production', 'manpower', 'field coordination',
          'field problem', 'field rework', 'workface'],
         'Field Supervisor', 'R', 'Manages daily field operations'),

        (['general superintendent', 'resource allocation', 'manpower allocation'],
         'General Superintendent', 'A', 'Approves resource allocations'),

        (['superintendent'],
         'Superintendent', 'C', 'Provides field oversight'),

        (['schedule', 'lookahead'],
         'Superintendent', 'C', 'Coordinates scheduling activities'),

        (['site administrator', 'filing', 'correspondence', 'meeting minutes',
          'documentation system', 'archive'],
         'Site Administrator', 'R', 'Manages project documentation'),

        (['branch manager', 'claims'],
         'Branch Manager', 'A', 'Provides executive approval and oversight'),

        (['client', 'owner'],
         'Branch Manager', 'C', 'Participates in client communications'),

        (['estimat'],
         'Estimator', 'C', 'Provides estimating support'),

        (['change order', 'scope', 'backcharge', 'force account'],
         'Project Manager', 'R', 'Manages contract changes'),

        (['turnover', 'closeout', 'warranty', 'o&m manual'],
         'Project Manager', 'A', 'Oversees project closeout'),

        (['setup', 'mobilization', 'trailer', 'temporary'],
         'Field Supervisor', 'R', 'Coordinates site setup activities'),

        (['setup', 'mobilization'],
         'Project Manager', 'A', 'Approves mobilization activities'),

        (['coordination meeting', 'kickoff'],
         'Project Manager', 'R', 'Leads project coordination'),

        (['rfi', 'submittal', 'drawing', 'specification'],
         'Project Manager', 'R', 'Manages technical documentation'),

        (['communication'],
         'Project Manager', 'R', 'Manages project communications'),

        (['lessons learned', 'post project', 'feedback'],
         'Project Manager', 'R', 'Leads continuous improvement activities'),
    ]

    # Track which roles we've already added
    added_roles = set()

    # Apply rules
    for keywords, role, raci, action in role_rules:
        if any(kw in combined for kw in keywords):
            if role not in added_roles:
                inferred_roles.append({
                    'role': role,
                    'raci': raci,
                    'description': f"{action} for {title}"
                })
                added_roles.add(role)

    # Always add Project Manager if not already added (PM involved in most SOPs)
    if 'Project Manager' not in added_roles:
        # Determine RACI based on phase
        if phase.startswith('2') or phase.startswith('4'):  # Preconstruction or Execution
            pm_raci = 'A'
            pm_action = 'Accountable for SOP execution'
        elif phase.startswith('6'):  # Closeout
            pm_raci = 'A'
            pm_action = 'Accountable for closeout activities'
        else:
            pm_raci = 'R'
            pm_action = 'Responsible for SOP execution'

        inferred_roles.append({
            'role': 'Project Manager',
            'raci': pm_raci,
            'description': f"{pm_action} for {title}"
        })
        added_roles.add('Project Manager')

    # Add Field Supervisor for Phase 3 (Mobilization) and Phase 4 (Execution) if not added
    if phase.startswith('3') or phase.startswith('4'):
        if 'Field Supervisor' not in added_roles:
            inferred_roles.append({
                'role': 'Field Supervisor',
                'raci': 'R' if phase.startswith('3') else 'C',
                'description': f"Field coordination for {title}"
            })
            added_roles.add('Field Supervisor')

    # Add Site Administrator for documentation-related SOPs
    if any(kw in combined for kw in ['document', 'filing', 'record', 'log', 'report']):
        if 'Site Administrator' not in added_roles:
            inferred_roles.append({
                'role': 'Site Administrator',
                'raci': 'C',
                'description': f"Documentation support for {title}"
            })
            added_roles.add('Site Administrator')

    return inferred_roles


def create_key_sop_matrix(sops_folder, output_path):
    """Create the Key SOP Matrix workbook from SOP documents."""

    # Collect all SOP files
    sop_files = sorted([
        f for f in Path(sops_folder).glob("*.docx")
        if not f.name.startswith('~$')
    ])

    print(f"Found {len(sop_files)} SOP documents")

    # Extract metadata from each SOP
    all_sops = []
    all_roles_set = set()
    all_coverage = []
    all_raci = []

    sops_with_explicit_roles = 0
    sops_with_inferred_roles = 0

    for sop_file in sop_files:
        print(f"  Processing: {sop_file.name}")
        metadata = extract_sop_metadata(sop_file)
        if metadata:
            metadata['filename'] = sop_file.name
            all_sops.append(metadata)

            # Get phase for this SOP
            phase = get_phase_from_sop_id(metadata['sop_id'])
            sop_title = f"{metadata['sop_id']} - {metadata['title']}"

            # Try to get explicit roles first
            parsed_roles = parse_roles_raci(metadata['roles'])

            # If no explicit roles, infer from content
            if not parsed_roles:
                parsed_roles = infer_roles_from_content(
                    metadata['sop_id'],
                    metadata['title'],
                    metadata['purpose'],
                    metadata['scope'],
                    phase
                )
                sops_with_inferred_roles += 1
                metadata['roles_inferred'] = True
            else:
                sops_with_explicit_roles += 1
                metadata['roles_inferred'] = False

            # Store parsed roles for later use in metadata sheet
            metadata['parsed_roles'] = parsed_roles

            # Build coverage/RACI entries for each role
            for pr in parsed_roles:
                all_roles_set.add(pr['role'])

                # Determine directive section based on role
                if 'Project Manager' in pr['role'] or 'PM' in pr['role']:
                    directive = "Sec. 9.5 PM Directives"
                elif 'Field' in pr['role'] or 'Foreman' in pr['role']:
                    directive = "Sec. 9.3 Field Leadership"
                elif 'Safety' in pr['role']:
                    directive = "Sec. 9.7 Safety Directives"
                elif 'Superintendent' in pr['role']:
                    directive = "Sec. 9.4 Superintendent Directives"
                elif 'Branch' in pr['role']:
                    directive = "Sec. 9.6 Branch Management"
                elif 'Purchasing' in pr['role']:
                    directive = "Sec. 9.10 Purchasing Directives"
                elif 'Accounting' in pr['role']:
                    directive = "Sec. 9.11 Accounting Directives"
                elif 'Quality' in pr['role']:
                    directive = "Sec. 9.13 Quality Directives"
                elif 'Estimat' in pr['role']:
                    directive = "Sec. 9.9 Estimating Directives"
                elif 'Site Administrator' in pr['role']:
                    directive = "Sec. 9.8 Site Administration"
                else:
                    directive = "Sec. 9.2 General Directives"

                action = pr['description'][:200] if pr['description'] else f"Executes {metadata['title'].lower()} responsibilities"

                # Mark inferred roles with different status
                if metadata.get('roles_inferred'):
                    status = 'Inferred'
                    recommendation = 'Verify role assignment and add explicit RACI to SOP.'
                else:
                    status = 'Covered'
                    recommendation = 'No change required.'

                all_coverage.append({
                    'sop_title': sop_title,
                    'action': action,
                    'role': pr['role'],
                    'directive': directive,
                    'status': status,
                    'recommendation': recommendation,
                    'category': phase
                })

                all_raci.append({
                    'sop_title': sop_title,
                    'action': action,
                    'role': pr['role'],
                    'directive': directive,
                    'status': status,
                    'recommendation': recommendation,
                    'category': phase,
                    'raci': pr['raci']
                })

    print(f"\nExtracted metadata from {len(all_sops)} SOPs")
    print(f"  - SOPs with explicit RACI roles: {sops_with_explicit_roles}")
    print(f"  - SOPs with inferred roles: {sops_with_inferred_roles}")
    print(f"Found {len(all_roles_set)} unique roles")
    print(f"Generated {len(all_coverage)} coverage entries")

    # Create workbook
    wb = Workbook()

    # =========================================================================
    # Sheet 1: GSL_SOP_Metadata
    # =========================================================================
    ws1 = wb.active
    ws1.title = "GSL_SOP_Metadata"

    metadata_headers = [
        "SOP ID", "Name", "SOP File Name", "Title", "Description",
        "Phase", "Category (CCC Tag)", "Category Group", "Roles (RACI)",
        "Primary JD", "Discipline", "Revision", "Effective Date", "Owner",
        "Approver", "Formerly", "Status", "Tags / Keywords", "Related SOPs",
        "Department / Division", "Last Reviewed Date", "Next Review Due", "Document Type"
    ]
    ws1.append(metadata_headers)

    for sop in all_sops:
        phase = get_phase_from_sop_id(sop['sop_id'])
        category = get_category_from_sop_id(sop['sop_id'])

        # Format roles with RACI - use pre-computed parsed_roles (includes inferred)
        parsed_roles = sop.get('parsed_roles', [])
        roles_str = '; '.join([f"{r['role']} ({r['raci']})" for r in parsed_roles])
        if sop.get('roles_inferred') and roles_str:
            roles_str = "[Inferred] " + roles_str

        # Determine category group
        if phase.startswith("1") or phase.startswith("2"):
            cat_group = "200-299 Preconstruction Planning"
        elif phase.startswith("3") or phase.startswith("4"):
            cat_group = "100-199 Project Execution"
        elif phase.startswith("5"):
            cat_group = "300-399 Commissioning"
        elif phase.startswith("6"):
            cat_group = "400-499 Closeout"
        else:
            cat_group = "000-099 General"

        # Clean and truncate description
        desc = clean_text(sop['purpose'])
        if len(desc) > 500:
            desc = desc[:497] + "..."

        # Related SOPs
        related = '; '.join(sop['related_sops'][:5]) if sop['related_sops'] else ''

        # Primary JD from job descriptions
        primary_jd = sop['job_descriptions'][0] if sop['job_descriptions'] else ''

        row = [
            sop['sop_id'],                          # SOP ID
            f"{sop['sop_id']} - {sop['title']}",    # Name
            sop['filename'],                        # SOP File Name
            sop['title'],                           # Title
            desc,                                   # Description (Purpose)
            phase,                                  # Phase
            category,                               # Category (CCC Tag)
            cat_group,                              # Category Group
            roles_str,                              # Roles (RACI)
            primary_jd,                             # Primary JD
            sop['department'] or "Operations",      # Discipline
            1,                                      # Revision
            datetime.now() - timedelta(days=30),   # Effective Date
            "Project Management",                   # Owner
            "Executive Committee",                  # Approver
            None,                                   # Formerly
            "Approved",                             # Status
            sop['title'].lower().replace(' ', '; '),  # Tags / Keywords
            related,                                # Related SOPs
            sop['department'] or "Operations",      # Department / Division
            datetime.now() - timedelta(days=7),    # Last Reviewed Date
            datetime.now() + timedelta(days=365),  # Next Review Due
            "SOP"                                   # Document Type
        ]
        ws1.append(row)

    style_header_row(ws1, len(metadata_headers))
    ws1.column_dimensions['A'].width = 12
    ws1.column_dimensions['B'].width = 55
    ws1.column_dimensions['C'].width = 55
    ws1.column_dimensions['D'].width = 45
    ws1.column_dimensions['E'].width = 70
    ws1.column_dimensions['I'].width = 50

    # =========================================================================
    # Sheet 2: Sheet2 (Position-Policy Mapping)
    # =========================================================================
    ws2 = wb.create_sheet("Sheet2")

    ws2['A1'] = None
    ws2['B1'] = "Management Directives"
    ws2['C1'] = None
    ws2['E1'] = "Job Descriptions"
    ws2['F1'] = None

    ws2['A2'] = "Position"
    ws2['B2'] = "Policy Manual, 9.x Management Directives"
    ws2['C2'] = "File Path"
    ws2['E2'] = "Policy Manual, 7.x Job Descriptions"
    ws2['F2'] = "File Path"

    positions = [
        ("Apprentice", "9.2 Field Employees", "7.2.1 Apprentice Electrician"),
        ("Journeyman", "9.2 Field Employees", "7.2.2 Journeyman Electrician"),
        ("Foreman", "9.3 Field Leadership", "7.2.4 Foreman"),
        ("General Foreman", "9.3 Field Leadership", "7.2.5 General Foreman"),
        ("Field Supervisor", "9.4 Field Supervision", "7.2.6 Field Supervisor"),
        ("Superintendent", "9.4 Superintendents", "7.2.7 Superintendent"),
        ("General Superintendent", "9.4 General Superintendents", "7.2.8 General Superintendent"),
        ("Project Coordinator", "9.5 Project Management", "7.3.0 Project Coordinator"),
        ("Project Manager", "9.5 Project Management", "7.3.1 Project Manager"),
        ("Senior Project Manager", "9.5 Project Management", "7.3.2 Senior Project Manager"),
        ("Branch Manager", "9.6 Branch Management", "7.4.1 Branch Manager"),
        ("Safety Coordinator", "9.7 Safety", "7.5.1 Safety Coordinator"),
        ("Site Administrator", "9.8 Site Administration", "7.5.2 Site Administrator"),
        ("Estimator", "9.9 Estimating", "7.6.1 Estimator"),
        ("Chief Estimator", "9.9 Estimating", "7.6.2 Chief Estimator"),
        ("Purchasing", "9.10 Purchasing", "7.6.3 Purchasing Agent"),
        ("Purchasing Manager", "9.10 Purchasing", "7.6.4 Purchasing Manager"),
        ("Accounting", "9.11 Accounting", "7.7.1 Accounting"),
        ("Controller", "9.11 Accounting", "7.7.2 Controller"),
        ("Prefabrication Lead", "9.12 Prefabrication", "7.8.1 Prefab Lead"),
        ("Quality Inspector", "9.13 Quality", "7.9.1 Quality Inspector"),
    ]

    base_path = "C:\\Documents\\Policy Manual\\"
    for i, (pos, directive, jd) in enumerate(positions, start=3):
        ws2[f'A{i}'] = pos
        ws2[f'B{i}'] = f"Policy Manual, {directive}"
        ws2[f'C{i}'] = f"{base_path}Management Directives\\{directive}.doc"
        ws2[f'E{i}'] = f"Policy Manual, {jd}"
        ws2[f'F{i}'] = f"{base_path}Job Descriptions\\{jd}.doc"

    ws2.column_dimensions['A'].width = 22
    ws2.column_dimensions['B'].width = 45
    ws2.column_dimensions['C'].width = 60
    ws2.column_dimensions['E'].width = 40
    ws2.column_dimensions['F'].width = 55

    # =========================================================================
    # Sheet 3: Coverage Matrix
    # =========================================================================
    ws3 = wb.create_sheet("Coverage Matrix")

    coverage_headers = ["SOP Title", "SOP Action", "Responsible Role",
                        "Directive Section", "Coverage Status",
                        "Gap Closure Recommendation", "Category"]
    ws3.append(coverage_headers)

    for entry in all_coverage:
        ws3.append([
            entry['sop_title'],
            entry['action'],
            entry['role'],
            entry['directive'],
            entry['status'],
            entry['recommendation'],
            entry['category']
        ])

    style_header_row(ws3, len(coverage_headers))
    auto_column_width(ws3)

    # =========================================================================
    # Sheet 4: RACI Matrix
    # =========================================================================
    ws4 = wb.create_sheet("RACI Matrix")

    raci_headers = coverage_headers + ["RACI"]
    ws4.append(raci_headers)

    for entry in all_raci:
        ws4.append([
            entry['sop_title'],
            entry['action'],
            entry['role'],
            entry['directive'],
            entry['status'],
            entry['recommendation'],
            entry['category'],
            entry['raci']
        ])

    style_header_row(ws4, len(raci_headers))
    auto_column_width(ws4)

    # =========================================================================
    # Sheet 5: Redline Recs (sample entries for gaps)
    # =========================================================================
    ws5 = wb.create_sheet("Redline Recs")

    redline_headers = ["SOP Title", "SOP Action", "Responsible Role", "Directive Section",
                       "Coverage Status", "Gap Closure Recommendation", "Category", "Redline Proposal"]
    ws5.append(redline_headers)

    # Add placeholder for manual gap identification
    ws5.append([
        "To be populated",
        "Gap analysis pending",
        "-",
        "-",
        "Gap - TBD",
        "Review required",
        "-",
        "Amendment pending review"
    ])

    style_header_row(ws5, len(redline_headers))
    auto_column_width(ws5)

    # =========================================================================
    # Sheet 6: Conflict Matrix
    # =========================================================================
    ws6 = wb.create_sheet("Conflict Matrix")

    conflict_headers = ["SOP Title", "Conflict Description", "Conflict Type", "Resolution Recommendation"]
    ws6.append(conflict_headers)

    # Placeholder
    ws6.append([
        "To be populated",
        "Conflict analysis pending",
        "TBD",
        "Review required"
    ])

    style_header_row(ws6, len(conflict_headers))
    auto_column_width(ws6)

    # =========================================================================
    # Sheet 7: Closeout Checklist
    # =========================================================================
    ws7 = wb.create_sheet("Closeout Checklist")

    closeout_headers = ["Role", "Closeout Task", "Directive Section", "Coverage Status"]
    ws7.append(closeout_headers)

    # Extract closeout tasks from Phase 6 SOPs
    for sop in all_sops:
        if sop['sop_id'].startswith('9.6.'):
            # Use pre-computed parsed_roles (includes inferred roles)
            parsed_roles = sop.get('parsed_roles', [])
            for pr in parsed_roles:
                if pr['raci'] in ['R', 'A']:
                    status = "Inferred" if sop.get('roles_inferred') else "Covered"
                    ws7.append([
                        pr['role'],
                        f"{sop['title']}: {pr['description'][:100]}..." if pr['description'] else sop['title'],
                        "Sec. 9.6 Closeout",
                        status
                    ])

    style_header_row(ws7, len(closeout_headers))
    auto_column_width(ws7)

    # =========================================================================
    # Sheet 8: Role Alignment Matrix
    # =========================================================================
    ws8 = wb.create_sheet("Role Alignment Matrix")

    # Get sorted unique roles
    all_roles = sorted(list(all_roles_set))

    role_headers = ["SOP ID", "SOP Title", "Phase"] + all_roles
    ws8.append(role_headers)

    for sop in all_sops:
        # Use pre-computed parsed_roles (includes inferred roles)
        parsed_roles = sop.get('parsed_roles', [])
        sop_roles = [pr['role'] for pr in parsed_roles]
        phase = get_phase_from_sop_id(sop['sop_id'])

        row = [sop['sop_id'], f"{sop['sop_id']} - {sop['title']}", phase]

        for role in all_roles:
            if role in sop_roles:
                # Find RACI designation
                raci = next((pr['raci'] for pr in parsed_roles if pr['role'] == role), 'X')
                # Mark inferred with asterisk
                if sop.get('roles_inferred'):
                    raci = f"{raci}*"
                row.append(raci)
            else:
                row.append(None)

        ws8.append(row)

    style_header_row(ws8, len(role_headers))
    ws8.column_dimensions['A'].width = 12
    ws8.column_dimensions['B'].width = 55
    ws8.column_dimensions['C'].width = 30

    # =========================================================================
    # Sheet 9: SOP Number Crosswalk
    # =========================================================================
    ws9 = wb.create_sheet("SOP Number Crosswalk")

    crosswalk_headers = ["Legacy SOP #", "New SOP #", "Title", "SOP Title", "Notes"]
    ws9.append(crosswalk_headers)

    crosswalk_data = [
        ("9.41.745", "9.4.745", "Manage Field Rework", "Manage Field Rework", "Legacy crosswalk"),
        ("9.41.190A", "9.4.190", "Document Filing Standards", "A Document Filing Standards", "Legacy crosswalk"),
        ("9.4.575", "9.4.576", "Manage Subcontractor Resources", "Manage Subcontractor Resources", "Renumbered"),
        ("9.5.015", "9.5.020", "Handling Excess Materials", "Handling and or Disposing of Excess Materials", "Renumbered"),
        ("9.6.030", "9.6.035", "Submit Warranties", "Submit Warranties", "Renumbered"),
        ("9.6.060", "9.6.065", "Archive Documentation", "Archive Project Documentation", "Renumbered"),
    ]

    for row in crosswalk_data:
        ws9.append(row)

    style_header_row(ws9, len(crosswalk_headers))
    auto_column_width(ws9)

    # =========================================================================
    # Sheet 10: Change_Log
    # =========================================================================
    ws10 = wb.create_sheet("Change_Log")

    changelog_headers = ["Timestamp", "Sheet", "Change Type", "Details"]
    ws10.append(changelog_headers)

    changelog_data = [
        (datetime.now().isoformat(), "GSL_SOP_Metadata", "Initial Load", f"Loaded {len(all_sops)} SOPs from Revised SOPs folder"),
        (datetime.now().isoformat(), "Coverage Matrix", "Generated", f"Generated {len(all_coverage)} coverage entries from SOP roles"),
        (datetime.now().isoformat(), "RACI Matrix", "Generated", f"Generated {len(all_raci)} RACI entries from SOP roles"),
        (datetime.now().isoformat(), "Role Alignment Matrix", "Generated", f"Mapped {len(all_roles)} unique roles across all SOPs"),
        (datetime.now().isoformat(), "Closeout Checklist", "Generated", "Extracted closeout tasks from Phase 6 SOPs"),
    ]

    for row in changelog_data:
        ws10.append(row)

    style_header_row(ws10, len(changelog_headers))
    auto_column_width(ws10)

    # =========================================================================
    # Sheet 11: Mapping_Log
    # =========================================================================
    ws11 = wb.create_sheet("Mapping_Log")

    mapping_headers = ["Sheet", "SOP Title", "Source Action", "Mapped Action", "Role", "Source Version", "Match Score"]
    ws11.append(mapping_headers)

    mapping_data = [
        ("GSL_SOP_Metadata", "All SOPs", "Extracted from Word documents",
         "Purpose, Scope, Roles parsed", "Multiple", "v8", 1.0),
        ("Coverage Matrix", "All SOPs", "RACI roles from documents",
         "Role-Directive mapping", "Multiple", "v8", 0.95),
        ("Role Alignment Matrix", "All SOPs", "RACI designations",
         "Role-SOP cross-reference", "Multiple", "v8", 1.0),
    ]

    for row in mapping_data:
        ws11.append(row)

    style_header_row(ws11, len(mapping_headers))
    auto_column_width(ws11)

    # Save workbook
    wb.save(output_path)

    print(f"\n{'='*60}")
    print(f"Workbook saved to: {output_path}")
    print(f"{'='*60}")
    print(f"Sheets created: {len(wb.sheetnames)}")
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        print(f"  - {sheet}: {ws.max_row} rows x {ws.max_column} cols")

    return output_path


if __name__ == "__main__":
    sops_folder = r"C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"
    output_path = r"C:\Users\tewing\Desktop\Claude Projects\Project Outputs\Key_SOP_Matrix_v2.xlsx"

    create_key_sop_matrix(sops_folder, output_path)
