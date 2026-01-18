"""
Batch Process Old Format SOPs (9.41.XXX) and Convert to New Numbers
"""

import os
import re
import pandas as pd
import win32com.client as win32

# Paths
sops_folder = r"C:\Users\tewing\Desktop\Claude Projects\SOPs For Review"
output_folder = r"C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"
metadata_path = r"C:\Users\tewing\Desktop\Claude Projects\SOPs For Review\Key_Sop_Matrix.xlsx"

# Create output folder
os.makedirs(output_folder, exist_ok=True)

# Role to Job Description mapping
ROLE_TO_JD = {
    "PM": "7.3.1 Operations Management",
    "Project Manager": "7.3.1 Operations Management",
    "Assistant PM": "7.3.1 Operations Management",
    "Project Coordinator": "7.3.1 Operations Management",
    "Branch Manager": "7.3.1 Operations Management",
    "General Superintendent": "7.2.5 Project Superintendent",
    "Field Supervisor": "7.2.4 Foreman",
    "Foreman": "7.2.4 Foreman",
    "Lead Journeyman": "7.2.3 Lead Journeyman",
    "Journeyman": "7.2.2 Journeyman Electrician",
    "Safety": "7.2.6 Project Safety Coordinator",
    "Estimator": "7.3.3 Estimating",
    "Purchasing": "7.4.4 Purchasing Manager",
    "Pre-Fab": "7.3.7 Pre-Fabrication",
    "Accounting": "7.5 Accounting",
}

# Phase to Management Directive mapping
PHASE_TO_MD = {
    "9.1": ["9.5 Project Management", "9.7 Estimating"],
    "9.2": ["9.5 Project Management", "9.7 Estimating", "9.3 Field Leadership"],
    "9.3": ["9.5 Project Management", "9.3 Field Leadership"],
    "9.4": ["9.5 Project Management", "9.3 Field Leadership", "9.4 General Superintendents"],
    "9.5": ["9.5 Project Management", "9.3 Field Leadership"],
    "9.6": ["9.5 Project Management", "9.3 Field Leadership"],
}

# Phase to Training Tab mapping
PHASE_TO_TRAINING = {
    "9.1": ["Tab 11: Estimating Take-off Procedures"],
    "9.2": ["Tab 2: Preplanning & Staging", "Tab 3: Kickoff/Project Turnover Meeting", "Tab 5: Purchasing Buy out", "Tab 6: Scheduling", "Tab 7: Job Plans"],
    "9.3": ["Tab 4: Staging & Job Familiarization", "Tab 22: Document Management"],
    "9.4": ["Tab 6: Scheduling", "Tab 8: Change Order Process", "Tab 9: Submittals", "Tab 12: Look Ahead", "Tab 14: Daily Reports", "Tab 22: Document Management", "Tab 41: Material Management", "Tab 57: ProCore"],
    "9.5": ["Tab 38: Testing"],
    "9.6": ["Tab 18: Job Close Out", "Tab 22: Document Management"],
}


def load_number_mapping():
    """Load old-to-new number mapping from Key_Sop_Matrix"""
    df = pd.read_excel(metadata_path, sheet_name='GSL_SOP_Metadata')

    mapping = {}
    metadata = {}

    for _, row in df.iterrows():
        new_id = str(row['SOP ID']).strip()
        formerly = str(row['Formerly']) if pd.notna(row['Formerly']) else ''
        title = str(row['SOP Title']) if pd.notna(row['SOP Title']) else ''
        roles = str(row['Roles (RACI)']) if pd.notna(row['Roles (RACI)']) else ''

        # Extract old number from "Formerly" column
        if 'Formerly' in formerly or '9.41' in formerly:
            # Extract 9.41.XXX pattern
            match = re.search(r'9\.41\.(\d+)', formerly)
            if match:
                old_id = f"9.41.{match.group(1)}"
                mapping[old_id] = new_id

        metadata[new_id] = {'title': title, 'roles': roles}

    return mapping, metadata


def get_sop_phase(sop_id):
    """Extract phase from SOP ID"""
    parts = sop_id.replace('9.41.', '9.4.').split('.')
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return "9.4"


def get_jds_from_roles(roles_str):
    """Convert roles string to list of JD references"""
    if not roles_str or roles_str == 'nan':
        return ["7.3.1 Operations Management"]

    jds = set()
    for role in roles_str.split(';'):
        role = role.strip()
        for key, value in ROLE_TO_JD.items():
            if key.lower() in role.lower():
                jds.add(value)
                break

    return sorted(list(jds)) if jds else ["7.3.1 Operations Management"]


def build_reference_block(sop_id, roles_str):
    """Build the cross-reference block"""
    phase = get_sop_phase(sop_id)
    jds = get_jds_from_roles(roles_str)
    mds = PHASE_TO_MD.get(phase, ["9.5 Project Management"])
    training = PHASE_TO_TRAINING.get(phase, ["See Foreman Training Binder"])

    block = "\n\n" + "=" * 80 + "\n"
    block += "DOCUMENT REFERENCES\n"
    block += "=" * 80 + "\n\n"

    block += "Training Materials (Foreman Training Binder):\n"
    for t in training:
        block += f"- {t}\n"

    block += "\nJob Descriptions (Policy Manual Section 7):\n"
    for jd in jds:
        block += f"- {jd}\n"

    block += "\nManagement Directives (Policy Manual Section 9):\n"
    for md in mds:
        block += f"- {md}\n"

    block += "\n" + "=" * 80 + "\n\n"
    return block


def process_sop(word, filepath, old_id, new_id, roles_str, output_folder):
    """Process a single old-format SOP file"""
    filename = os.path.basename(filepath)

    try:
        doc = word.Documents.Open(filepath)

        # Build reference block
        ref_block = build_reference_block(new_id, roles_str)

        # Try to find insertion point
        find = doc.Content.Find
        find.ClearFormatting()

        inserted = False
        for search_term in ["1. Purpose", "Purpose", "1.0 Purpose", "SCOPE"]:
            if find.Execute(search_term):
                insert_range = doc.Range(find.Parent.Start, find.Parent.Start)
                insert_range.InsertBefore(ref_block)
                inserted = True
                break

        if not inserted:
            doc.Content.InsertBefore(ref_block)

        # Also replace old SOP number with new one in the document
        find2 = doc.Content.Find
        find2.ClearFormatting()
        find2.Replacement.ClearFormatting()
        find2.Execute(FindText=old_id, ReplaceWith=new_id, Replace=2)  # wdReplaceAll

        # Create new filename with new SOP number
        # Extract title from filename
        title_match = re.search(r'9\.41\.\d+[A-Za-z]?\s*-\s*(.+)\.docx', filename)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = filename.replace('.docx', '').replace(old_id, '').strip(' -')

        new_filename = f"{new_id} {title} - REVISED.docx"
        output_path = os.path.join(output_folder, new_filename)

        doc.SaveAs(output_path)
        doc.Close()

        return True, new_filename

    except Exception as e:
        try:
            doc.Close(False)
        except:
            pass
        return False, str(e)


def main():
    print("Batch Processing Old Format SOPs (9.41.XXX)")
    print("=" * 70)

    # Load mapping
    mapping, metadata = load_number_mapping()
    print(f"Loaded {len(mapping)} old-to-new number mappings")

    # Find old format SOP files
    sop_files = []
    for f in os.listdir(sops_folder):
        if f.endswith('.docx') and '9.41.' in f:
            sop_files.append(f)

    print(f"Found {len(sop_files)} old format SOPs to process")
    print("-" * 70)

    # Initialize Word
    word = win32.gencache.EnsureDispatch('Word.Application')
    word.Visible = False

    success = 0
    errors = 0
    skipped = 0

    for filename in sorted(sop_files):
        filepath = os.path.join(sops_folder, filename)

        # Extract old SOP ID
        match = re.search(r'(9\.41\.\d+[A-Za-z]?)', filename)
        if not match:
            print(f"SKIP: Cannot extract ID from {filename}")
            skipped += 1
            continue

        old_id = match.group(1)

        # Get new ID from mapping
        new_id = mapping.get(old_id, old_id.replace('9.41.', '9.4.'))  # Default conversion

        # Get roles from metadata
        meta = metadata.get(new_id, {})
        roles = meta.get('roles', '')

        ok, result = process_sop(word, filepath, old_id, new_id, roles, output_folder)

        if ok:
            print(f"OK: {old_id} -> {new_id}")
            success += 1
        else:
            print(f"ERROR: {filename} - {result}")
            errors += 1

    word.Quit()

    print("-" * 70)
    print(f"Complete: {success} processed, {errors} errors, {skipped} skipped")
    print(f"Output folder: {output_folder}")


if __name__ == "__main__":
    main()
