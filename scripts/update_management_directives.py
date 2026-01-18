"""
Update Management Directive Documents with SOP References
Phase 4 - Management Directive Sync
"""

import os
import win32com.client as win32

# Paths
md_folder = r"C:\Users\tewing\Desktop\Claude Projects\Management Directives"
output_folder = r"C:\Users\tewing\Desktop\Claude Projects\Revised Management Directives"

# Create output folder
os.makedirs(output_folder, exist_ok=True)

# Management Directive to SOP mapping
MD_TO_SOPS = {
    "9.2": {
        "title": "Management Directives for Field Employees",
        "scope": "All field electricians (Apprentice through Journeyman)",
        "sops": {
            "9.4": [
                ("9.4.475", "Conduct Safety Orientation"),
                ("9.4.480", "Conduct Safety Inspections"),
                ("9.4.485", "Conduct Safety Meetings"),
                ("9.4.490", "Report Safety Incidents"),
                ("9.4.675", "Conduct Daily Huddles"),
                ("9.4.695", "Track Production Quantities"),
            ]
        }
    },
    "9.3": {
        "title": "Management Directives for Field Leadership",
        "scope": "Foremen, Lead Journeymen, Field Supervisors",
        "sops": {
            "9.2": [
                ("9.2.050", "Field Supervisor Reviews Plans, Specs and Schedule"),
                ("9.2.055", "Compare Estimated vs Planned"),
                ("9.2.070", "Conduct Site Visit"),
                ("9.2.080", "Prepare Material Handling Plan"),
                ("9.2.090", "Develop Labor Budget"),
                ("9.2.100", "Prepare Layout and Sequencing Plan"),
                ("9.2.110", "Develop Project Schedule"),
                ("9.2.120", "Establish Tracking and Control Systems"),
            ],
            "9.3": [
                ("9.3.010", "Setup Office Trailer"),
                ("9.3.020", "Setup Storage Trailer"),
                ("9.3.030", "Setup Site Fencing and Access Control"),
                ("9.3.040", "Setup Temporary Power"),
                ("9.3.050", "Setup Temporary Water"),
                ("9.3.060", "Setup Sanitary Facilities"),
                ("9.3.070", "Setup Temporary Lighting"),
                ("9.3.080", "Setup Signage"),
                ("9.3.090", "Setup Security"),
                ("9.3.100", "Setup Laydown Area"),
                ("9.3.110", "Setup Equipment Staging"),
                ("9.3.120", "Setup Parking"),
                ("9.3.470", "Develop Site-Specific Safety Plan"),
            ],
            "9.4": [
                ("9.4.040", "Conduct Safety Meetings"),
                ("9.4.215", "Manage Daily Reports"),
                ("9.4.360", "Manage Change Orders"),
                ("9.4.365", "Manage Potential Change Orders (PCOs)"),
                ("9.4.475", "Conduct Safety Orientation"),
                ("9.4.480", "Conduct Safety Inspections"),
                ("9.4.490", "Report Safety Incidents"),
                ("9.4.525", "Conduct Quality Inspections"),
                ("9.4.560", "Manage Manpower Allocation"),
                ("9.4.565", "Manage Equipment Allocation"),
                ("9.4.570", "Manage Material Allocation"),
                ("9.4.630", "Manage Material Receiving"),
                ("9.4.631", "Release of Large Feeder Wire"),
                ("9.4.675", "Conduct Daily Huddles"),
                ("9.4.680", "Conduct Weekly Foreman Meetings"),
                ("9.4.690", "Track Manpower Utilization"),
                ("9.4.695", "Track Production Quantities"),
                ("9.4.700", "Track Equipment Utilization"),
                ("9.4.705", "Manage Work Packaging"),
                ("9.4.710", "Manage Workface Planning"),
                ("9.4.715", "Manage Field Coordination"),
                ("9.4.720", "Conduct Productivity Analysis"),
                ("9.4.725", "Resolve Field Problems"),
                ("9.4.735", "Perform Field Quality Verifications"),
                ("9.4.745", "Manage Field Rework"),
                ("9.4.755", "Implement Field Productivity Improvements"),
            ],
            "9.5": [
                ("9.5.010", "Conduct Commissioning Meetings"),
                ("9.5.550", "Manage Commissioning Activities"),
            ],
            "9.6": [
                ("9.6.005", "Prepare for Turnover (Field Perspective)"),
                ("9.6.010", "Conduct Closeout Meetings"),
                ("9.6.020", "Manage Punch Lists"),
                ("9.6.070", "Conduct Post-Project Review"),
                ("9.6.085", "Document Lessons Learned"),
            ]
        }
    },
    "9.4": {
        "title": "Management Directives for General Superintendents",
        "scope": "General Superintendents, Project Superintendents",
        "sops": {
            "9.2": [
                ("9.2.010", "Team Selection"),
                ("9.2.015", "Project Turnover Meeting"),
                ("9.2.090", "Develop Labor Budget"),
                ("9.2.100", "Prepare Layout and Sequencing Plan"),
                ("9.2.130", "Construction Execution Kickoff Meeting"),
            ],
            "9.4": [
                ("9.4.010", "Conduct Coordination Meetings"),
                ("9.4.020", "Conduct Subcontractor Coordination Meetings"),
                ("9.4.040", "Conduct Safety Meetings"),
                ("9.4.060", "Conduct Quality Meetings"),
                ("9.4.325", "Monitor Schedule Performance"),
                ("9.4.345", "Conduct Schedule Review Meetings"),
                ("9.4.475", "Conduct Safety Orientation"),
                ("9.4.505", "Conduct Safety Compliance Audits"),
                ("9.4.560", "Manage Manpower Allocation"),
                ("9.4.575", "Manage Subcontractor Resources"),
                ("9.4.680", "Conduct Weekly Foreman Meetings"),
                ("9.4.720", "Conduct Productivity Analysis"),
                ("9.4.755", "Implement Field Productivity Improvements"),
            ]
        }
    },
    "9.5": {
        "title": "Management Directives for Project Management",
        "scope": "Project Managers, Assistant PMs, Project Coordinators",
        "sops": {
            "9.2": [
                ("9.2.005", "Review Contract for High-Risk Clauses"),
                ("9.2.010", "Team Selection"),
                ("9.2.015", "Project Turnover Meeting"),
                ("9.2.020", "Procurement of Large Feeder Wire"),
                ("9.2.040", "PM Reviews Plans, Specs and Schedule"),
                ("9.2.055", "Compare Estimated vs Planned"),
                ("9.2.057", "Identify VE and Prefabrication Opportunities"),
                ("9.2.060", "Create Issue List and Begin RFI Process"),
                ("9.2.080", "Prepare Material Handling Plan"),
                ("9.2.090", "Develop Labor Budget"),
                ("9.2.100", "Prepare Layout and Sequencing Plan"),
                ("9.2.110", "Develop Project Schedule"),
                ("9.2.120", "Establish Tracking and Control Systems"),
                ("9.2.130", "Construction Execution Kickoff Meeting"),
                ("9.2.140", "Develop Project Budget"),
                ("9.2.160", "Develop Procurement Plan"),
            ],
            "9.3": [
                "(All Mobilization SOPs - oversight responsibility)",
            ],
            "9.4": [
                "(All Construction Execution SOPs - primary responsibility)",
            ],
            "9.5": [
                ("9.5.010", "Conduct Commissioning Meetings"),
                ("9.5.550", "Manage Commissioning Activities"),
            ],
            "9.6": [
                ("9.6.005", "Prepare for Turnover (Field Perspective)"),
                ("9.6.010", "Conduct Closeout Meetings"),
                ("9.6.015", "Manage Project Turnover Documentation"),
                ("9.6.020", "Manage Punch Lists"),
                ("9.6.030", "Manage As-Built Drawings"),
                ("9.6.040", "Manage O&M Manuals"),
                ("9.6.050", "Manage Warranties"),
                ("9.6.060", "Manage Closeout Documentation"),
                ("9.6.070", "Conduct Post-Project Review"),
                ("9.6.080", "Capture Client Feedback"),
                ("9.6.085", "Document Lessons Learned"),
            ]
        }
    },
    "9.6": {
        "title": "Management Directives for Branch Management",
        "scope": "Branch Managers, Operations Managers",
        "sops": {
            "9.2": [
                ("9.2.005", "Review Contract for High-Risk Clauses"),
                ("9.2.010", "Team Selection"),
                ("9.2.015", "Project Turnover Meeting"),
                ("9.2.130", "Construction Execution Kickoff Meeting"),
                ("9.2.140", "Develop Project Budget"),
            ],
            "9.4": [
                ("9.4.360", "Manage Change Orders"),
                ("9.4.370", "Manage Owner Directives"),
                ("9.4.390", "Manage Claims"),
                ("9.4.400", "Monitor Project Costs"),
                ("9.4.405", "Manage Cost Forecasts"),
                ("9.4.430", "Manage Profit Projections"),
            ]
        }
    },
    "9.7": {
        "title": "Management Directives for Estimating",
        "scope": "Estimators, Chief Estimator",
        "sops": {
            "9.2": [
                ("9.2.010", "Team Selection"),
                ("9.2.015", "Project Turnover Meeting"),
                ("9.2.020", "Procurement of Large Feeder Wire"),
                ("9.2.055", "Compare Estimated vs Planned"),
                ("9.2.057", "Identify VE and Prefabrication Opportunities"),
                ("9.2.140", "Develop Project Budget"),
            ],
            "9.4": [
                ("9.4.360", "Manage Change Orders"),
                ("9.4.365", "Manage Potential Change Orders (PCOs)"),
                ("9.4.385", "Manage Force Account Work"),
            ]
        }
    },
    "9.14": {
        "title": "Management Directives for Contract Managers",
        "scope": "Contract Managers, Contract Administrators",
        "sops": {
            "9.2": [
                ("9.2.005", "Review Contract for High-Risk Clauses"),
                ("9.2.015", "Project Turnover Meeting"),
                ("9.2.060", "Create Issue List and Begin RFI Process"),
            ],
            "9.4": [
                ("9.4.355", "Manage Project Scope"),
                ("9.4.360", "Manage Change Orders"),
                ("9.4.365", "Manage Potential Change Orders (PCOs)"),
                ("9.4.370", "Manage Owner Directives"),
                ("9.4.375", "Manage Scope Clarifications"),
                ("9.4.380", "Manage Backcharges"),
                ("9.4.385", "Manage Force Account Work"),
                ("9.4.390", "Manage Claims"),
            ]
        }
    },
    "9.16": {
        "title": "Management Directives for Purchasing",
        "scope": "Purchasing Manager, Buyers",
        "sops": {
            "9.2": [
                ("9.2.020", "Procurement of Large Feeder Wire"),
                ("9.2.080", "Prepare Material Handling Plan"),
                ("9.2.160", "Develop Procurement Plan"),
            ],
            "9.4": [
                ("9.4.605", "Issue Purchase Orders"),
                ("9.4.610", "Manage Vendor Prequalification"),
                ("9.4.615", "Manage Vendor Evaluations"),
                ("9.4.620", "Manage Expediting"),
                ("9.4.625", "Manage Delivery Tracking"),
                ("9.4.630", "Manage Material Receiving"),
                ("9.4.631", "Release of Large Feeder Wire"),
                ("9.4.635", "Manage Material Inspection"),
                ("9.4.640", "Manage Storage and Logistics"),
                ("9.4.645", "Manage Material Handling"),
                ("9.4.650", "Manage Inventory"),
                ("9.4.655", "Prepare Procurement Reports"),
                ("9.4.660", "Manage Procurement Closeout"),
                ("9.4.665", "Reconcile Procurement Accounts"),
                ("9.4.670", "Manage Vendor Closeout"),
            ]
        }
    },
}

# Phase names
PHASE_NAMES = {
    "9.2": "Pre-Construction Planning",
    "9.3": "Mobilization",
    "9.4": "Construction Execution",
    "9.5": "Commissioning",
    "9.6": "Closeout",
}


def build_sop_reference_block(md_id):
    """Build the SOP reference block for a Management Directive"""
    if md_id not in MD_TO_SOPS:
        return None

    md_info = MD_TO_SOPS[md_id]

    block = "\n\n" + "=" * 80 + "\n"
    block += "APPLICABLE STANDARD OPERATING PROCEDURES\n"
    block += "=" * 80 + "\n\n"
    block += f"The following SOPs implement the requirements of this Management Directive:\n\n"

    for phase_id in ["9.2", "9.3", "9.4", "9.5", "9.6"]:
        if phase_id in md_info["sops"]:
            sops = md_info["sops"][phase_id]
            phase_name = PHASE_NAMES.get(phase_id, phase_id)
            block += f"{phase_name} ({phase_id}.XXX):\n"

            for sop in sops:
                if isinstance(sop, tuple):
                    block += f"  - {sop[0]} {sop[1]}\n"
                else:
                    block += f"  - {sop}\n"

            block += "\n"

    block += "For complete SOP details, refer to the GSL SOP Library.\n"
    block += "=" * 80 + "\n\n"

    return block


def get_md_id_from_filename(filename):
    """Extract MD ID (9.X) from filename"""
    import re
    match = re.search(r'9\.(\d+)', filename)
    if match:
        return f"9.{match.group(1)}"
    return None


def process_md_document(word, filepath, md_id, output_folder):
    """Process a single Management Directive document"""
    filename = os.path.basename(filepath)

    try:
        doc = word.Documents.Open(filepath)

        # Build reference block
        ref_block = build_sop_reference_block(md_id)

        if ref_block:
            # Try to find insertion point at end of document
            # For MDs, we'll insert at the end before any existing appendices
            doc.Content.InsertAfter(ref_block)

        # Save to output folder
        new_filename = filename.replace('.doc', ' - REVISED.doc')
        if new_filename == filename:
            new_filename = filename.replace('.docx', ' - REVISED.docx')

        output_path = os.path.join(output_folder, new_filename)

        # Save in appropriate format
        if filename.endswith('.docx'):
            doc.SaveAs(output_path, FileFormat=16)  # wdFormatXMLDocument
        else:
            doc.SaveAs(output_path, FileFormat=0)  # wdFormatDocument

        doc.Close()

        return True, new_filename

    except Exception as e:
        try:
            doc.Close(False)
        except:
            pass
        return False, str(e)


def main():
    print("Updating Management Directive Documents with SOP References")
    print("=" * 70)

    # Files to process
    files_to_process = [
        ("Policy Manual, 9.2 Management Directives for Field Employees.doc", "9.2"),
        ("Policy Manual, 9.3 Management Directives for Field Leadership.doc", "9.3"),
        ("Policy Manual, 9.4 Management Directives for General Superintendents.doc", "9.4"),
        ("Policy Manual, 9.5 Management Directives for Project Management.doc", "9.5"),
        ("Policy Manual, 9.6 Management Directives for Branch Management.doc", "9.6"),
        ("Policy Manual, 9.7 Management Directives for Estimating.doc", "9.7"),
        ("Policy Manual, 9.14 Management Directives for Contract Managers.doc", "9.14"),
        ("Policy Manual, 9.16 Management Directives for Purchasing.docx", "9.16"),
    ]

    print(f"Processing {len(files_to_process)} Management Directive documents")
    print("-" * 70)

    # Initialize Word
    word = win32.gencache.EnsureDispatch('Word.Application')
    word.Visible = False

    success = 0
    errors = 0
    skipped = 0

    for filename, md_id in files_to_process:
        filepath = os.path.join(md_folder, filename)

        if not os.path.exists(filepath):
            print(f"SKIP: File not found - {filename}")
            skipped += 1
            continue

        ok, result = process_md_document(word, filepath, md_id, output_folder)

        if ok:
            print(f"OK: {md_id} -> {result}")
            success += 1
        else:
            print(f"ERROR: {filename} - {result}")
            errors += 1

    word.Quit()

    print("-" * 70)
    print(f"Complete: {success} processed, {errors} errors, {skipped} skipped")
    print(f"Output folder: {output_folder}")

    # Note about files not processed
    print("\nNOTE: The following files were not processed (manual review needed):")
    print("  - Policy Manual, 9.0 Management Directives Index.doc (index only)")
    print("  - Policy Manual, 9.1 Introduction to Management Directicves.doc (intro only)")
    print("  - Policy Manual, 9.8 Management Directives for Design Build.mht (.mht format)")
    print("  - Policy Manual, 9.9 Management Directives - Continued.doc (review for content)")


if __name__ == "__main__":
    main()
