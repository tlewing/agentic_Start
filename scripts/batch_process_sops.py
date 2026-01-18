"""
Batch Process All SOPs with Cross-References
Adds Training, Job Description, and Management Directive references
"""

import os
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
    "Safety Coordinator": "7.2.6 Project Safety Coordinator",
    "Estimator": "7.3.3 Estimating",
    "Purchasing": "7.4.4 Purchasing Manager",
    "Pre-Fab": "7.3.7 Pre-Fabrication",
    "Prefab Superintendent": "7.3.7 Pre-Fabrication",
    "Accounting": "7.5 Accounting",
    "HR": "7.4.1 Human Resource Manager",
    "IT": "7.4 Business Administration",
    "Contracts Admin": "7.4 Business Administration",
    "Site Administrator": "7.4.5 Administrative Support",
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
    "9.2": [
        "Tab 2: Preplanning & Staging",
        "Tab 3: Kickoff/Project Turnover Meeting",
        "Tab 5: Purchasing Buy out",
        "Tab 6: Scheduling",
        "Tab 7: Job Plans",
    ],
    "9.3": [
        "Tab 4: Staging & Job Familiarization",
        "Tab 22: Document Management",
    ],
    "9.4": [
        "Tab 6: Scheduling",
        "Tab 8: Change Order Process",
        "Tab 9: Submittals",
        "Tab 12: Look Ahead",
        "Tab 14: Daily Reports",
        "Tab 22: Document Management",
        "Tab 41: Material Management & Control",
        "Tab 57: ProCore",
    ],
    "9.5": [
        "Tab 38: Testing",
    ],
    "9.6": [
        "Tab 18: Job Close Out",
        "Tab 22: Document Management",
    ],
}


def get_sop_phase(sop_id):
    """Extract phase from SOP ID (e.g., 9.2.010 -> 9.2)"""
    parts = sop_id.split('.')
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return "9.4"  # Default to construction execution


def get_jds_from_roles(roles_str):
    """Convert roles string to list of JD references"""
    if pd.isna(roles_str) or not roles_str:
        return ["7.3.1 Operations Management"]  # Default

    jds = set()
    for role in str(roles_str).split(';'):
        role = role.strip()
        if role in ROLE_TO_JD:
            jds.add(ROLE_TO_JD[role])
        else:
            # Try partial match
            for key, value in ROLE_TO_JD.items():
                if key.lower() in role.lower():
                    jds.add(value)
                    break

    return sorted(list(jds)) if jds else ["7.3.1 Operations Management"]


def build_reference_block(sop_id, sop_title, roles_str):
    """Build the cross-reference block to insert"""
    phase = get_sop_phase(sop_id)
    jds = get_jds_from_roles(roles_str)
    mds = PHASE_TO_MD.get(phase, ["9.5 Project Management"])
    training = PHASE_TO_TRAINING.get(phase, ["See Foreman Training Binder"])

    block = """

================================================================================
DOCUMENT REFERENCES
================================================================================

Training Materials (Foreman Training Binder):
"""
    for t in training:
        block += f"- {t}\n"

    block += """
Job Descriptions (Policy Manual Section 7):
"""
    for jd in jds:
        block += f"- {jd}\n"

    block += """
Management Directives (Policy Manual Section 9):
"""
    for md in mds:
        block += f"- {md}\n"

    block += """================================================================================

"""
    return block


def process_sop(word, filepath, sop_id, sop_title, roles_str, output_folder):
    """Process a single SOP file"""
    filename = os.path.basename(filepath)

    try:
        doc = word.Documents.Open(filepath)

        # Build reference block
        ref_block = build_reference_block(sop_id, sop_title, roles_str)

        # Try to find insertion point (after "Purpose" or at start)
        find = doc.Content.Find
        find.ClearFormatting()

        inserted = False
        for search_term in ["1. Purpose", "Purpose", "1.0 Purpose", "SCOPE"]:
            if find.Execute(search_term):
                # Insert before this section
                insert_range = doc.Range(find.Parent.Start, find.Parent.Start)
                insert_range.InsertBefore(ref_block)
                inserted = True
                break

        if not inserted:
            # Insert at beginning of document
            doc.Content.InsertBefore(ref_block)

        # Save to output folder with standardized name
        # Clean up filename
        new_filename = filename
        if new_filename.startswith("SOP - "):
            new_filename = new_filename.replace("SOP - ", "")
        if new_filename.startswith("SOP  "):
            new_filename = new_filename.replace("SOP  ", "")
        if not new_filename.endswith(" - REVISED.docx"):
            new_filename = new_filename.replace(".docx", " - REVISED.docx")

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
    print("Batch Processing SOPs with Cross-References")
    print("=" * 70)

    # Load metadata
    df = pd.read_excel(metadata_path, sheet_name='GSL_SOP_Metadata')
    metadata = {}
    for _, row in df.iterrows():
        sop_id = str(row['SOP ID']).strip()
        metadata[sop_id] = {
            'title': row['SOP Title'],
            'roles': row['Roles (RACI)'],
        }

    print(f"Loaded metadata for {len(metadata)} SOPs")

    # Find SOP files to process (new format only)
    sop_files = []
    for f in os.listdir(sops_folder):
        if f.endswith('.docx') and ('SOP - 9.' in f or 'SOP  9.' in f):
            sop_files.append(f)

    print(f"Found {len(sop_files)} SOPs in new format to process")
    print("-" * 70)

    # Initialize Word
    word = win32.gencache.EnsureDispatch('Word.Application')
    word.Visible = False

    success = 0
    errors = 0

    for filename in sorted(sop_files):
        filepath = os.path.join(sops_folder, filename)

        # Extract SOP ID from filename
        sop_id = filename.replace("SOP - ", "").replace("SOP  ", "").split(" ")[0]

        # Get metadata
        meta = metadata.get(sop_id, {})
        sop_title = meta.get('title', filename)
        roles = meta.get('roles', '')

        ok, result = process_sop(word, filepath, sop_id, sop_title, roles, output_folder)

        if ok:
            print(f"OK: {sop_id} -> {result}")
            success += 1
        else:
            print(f"ERROR: {filename} - {result}")
            errors += 1

    word.Quit()

    print("-" * 70)
    print(f"Complete: {success} processed, {errors} errors")
    print(f"Output folder: {output_folder}")


if __name__ == "__main__":
    main()
