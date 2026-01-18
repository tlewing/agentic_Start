"""
Update Job Descriptions with SOP References
Uses pywin32 to manipulate Word documents
"""

import os
import win32com.client as win32

# Paths
input_folder = r"C:\Users\tewing\Desktop\Claude Projects\Job Descriptions"
output_folder = r"C:\Users\tewing\Desktop\Claude Projects\Revised Job Descriptions"

# Create output folder
os.makedirs(output_folder, exist_ok=True)

# SOP Reference blocks
sop_blocks = {
    "7.2.4 Foreman": {
        "file": "Policy Manual, 7.2.4 Foreman.doc",
        "search": "Essential Duties and Responsibilities:",
        "block": """
================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role is responsible for executing the following SOPs:

- Section 1.1: Team Selection and Estimator Turnover
- Section 1.3: Scope and Contract Review
- Section 1.5: Material Handling Plan
- Section 1.6: Layout and Sequencing Plan
- Section 1.7: Schedule Development and Tracking
- SOP 9.4.631: Release of Large Feeder Wire
- SOP OPS-CO-001: Change Order Management

CRITICAL REQUIREMENTS:
- Per OPS-CO-001/MD 9.3: NEVER perform changed work without PM authorization
- Per Section 1.7/MD 9.3: Document in daily reports any scheduling delays
- Per SOP 9.4.631/MD 9.3: Complete timecards daily with installed quantities

Training Reference: Foreman Training Binder Tabs 2-14, 22, 38, 41, 49, 57
Skill Level: L7 per GSL Academy Target Skill Rules
================================================================================

"""
    },
    "7.3.1 Operations Management": {
        "file": "Policy Manual, 7.3.1 Operations Management.doc",
        "search": "Essential Job Functions",
        "block": """
================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

Project Managers are accountable for executing ALL pre-construction SOPs:

- Section 1.1: Team Selection and Estimator Turnover (A/R)
- Section 1.2: Administrative Setup (A/R)
- Section 1.3: Scope and Contract Review (A/R)
- Section 1.4: Buyout Process (A/R)
- Section 1.5: Material Handling Plan (A)
- Section 1.6: Layout and Sequencing Plan (A)
- Section 1.7: Schedule Development and Tracking (A/R)
- SOP 9.4.631: Release of Large Feeder Wire (A)
- SOP Procurement Large Feeder Wire (A/R)
- SOP OPS-CO-001: Change Order Management (A/R)

CRITICAL REQUIREMENTS (Per Management Directives 9.3/9.5):
- Buy out 80-90% of project
- Formal subcontracts required for amounts over $50,000
- Utilize Pull Planning by milestone during the project
- Only accept scope changes from the party directly contracted with
- Always request time extensions when liquidated damages provisions exist

Training Reference: Foreman Training Binder (all tabs), GSL Academy PM modules
================================================================================

"""
    },
    "7.2.5 Superintendent": {
        "file": "Policy Manual, 7.2.5 Project Superintendent (General Foreman).doc",
        "search": "Essential Duties and Responsibilities:",
        "block": """
================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role supervises foremen in executing the following SOPs:

- Section 1.1: Team Selection and Estimator Turnover (C)
- Section 1.3: Scope and Contract Review (C)
- Section 1.6: Layout and Sequencing Plan (A)
- Section 1.7: Schedule Development and Tracking (C)
- SOP OPS-CO-001: Change Order Management (R)

CRITICAL REQUIREMENTS:
- Ensure all foremen comply with SOP OPS-CO-001 authorization requirements
- Monitor critical path items per Section 1.7
- Coordinate change order integration per OPS-CO-001

Training Reference: Foreman Training Binder (all tabs)
Skill Level: L8 per GSL Academy Target Skill Rules
================================================================================

"""
    },
    "7.3.3 Estimating": {
        "file": "Policy Manual, 7.3.3 Estimating.doc",
        "search": "ESTIMATING JOB DESCRIPTIONS",
        "block": """
================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role provides input to the following SOPs:

- Section 1.1: Team Selection and Estimator Turnover (C)
- Section 1.3: Scope and Contract Review (C)
- SOP OPS-CO-001: Change Order Management (C)

CRITICAL REQUIREMENTS (Per Management Directive 9.7):
- Participate in Project Turn-Over Meeting
- Review all value engineering options
- Discuss all major vendors and subcontractors at turnover

Training Reference: Foreman Training Tabs 3, 11
================================================================================

"""
    },
    "7.2.3 Lead Journeyman": {
        "file": "Policy Manual, 7.2.3 Lead Journeyman.doc",
        "search": "Essential Duties and Responsibilities:",
        "block": """
================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role executes and provides input to the following SOPs:

- Section 1.5: Material Handling Plan (R)
- Section 1.6: Layout and Sequencing Plan (R)
- Section 1.7: Schedule Development and Tracking (C)
- SOP 9.4.631: Release of Large Feeder Wire (R)
- SOP OPS-CO-001: Change Order Management (I)

CRITICAL REQUIREMENT:
- Per OPS-CO-001/MD 9.3: Report changed conditions to Foreman immediately

Training Reference: Foreman Training Tabs 2, 4, 6, 7, 41
Skill Level: L6 per GSL Academy Target Skill Rules
================================================================================

"""
    },
    "7.2.2 Journeyman": {
        "file": "Policy Manual, 7.2.2 Journeyman Electrician.doc",
        "search": "Essential Duties and Responsibilities:",
        "block": """
================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role executes work under the following SOPs:

- Section 1.5: Material Handling Plan (R)
- Section 1.6: Layout and Sequencing Plan (R)
- SOP 9.4.631: Release of Large Feeder Wire (R)

Training Reference: GSL Academy L5 Journeyman modules
Skill Level: L5 per GSL Academy Target Skill Rules
================================================================================

"""
    },
    "7.4.4 Purchasing": {
        "file": "Policy Manual, 7.4.4 Purchasing Manager (Salt Lake Office).doc",
        "search": "Essential Duties and Responsibilities:",
        "block": """
================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role supports the following SOPs:

- Section 1.4: Buyout Process (C)
- SOP Procurement Large Feeder Wire (R)

CRITICAL REQUIREMENTS (Per Management Directive 9.16):
- Coordinate with Project Management per MD 9.5 requirements
- Formal subcontracts required for amounts over $50,000
================================================================================

"""
    },
    "7.3.7 Pre-Fabrication": {
        "file": "Policy Manual, 7.3.7 Pre-Fabrication.doc",
        "search": "7.3.7",
        "block": """
================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role provides input to the following SOPs:

- Section 1.1: Team Selection and Estimator Turnover (C)
- Section 1.3: Scope and Contract Review (C)
- Section 1.6: Layout and Sequencing Plan (C)

CRITICAL REQUIREMENT (Per Management Directive 9.5):
- Review each project to determine scope that can be prefabricated
================================================================================

"""
    }
}

def update_jd(word, jd_name, config):
    """Update a single JD with SOP references"""
    input_path = os.path.join(input_folder, config["file"])
    output_name = config["file"].replace(".doc", " - REVISED.doc").replace(", ", " ")
    output_path = os.path.join(output_folder, output_name)

    try:
        doc = word.Documents.Open(input_path)
        find = doc.Content.Find
        find.ClearFormatting()

        if find.Execute(config["search"]):
            # Insert after the found text
            insert_range = doc.Range(find.Parent.End, find.Parent.End)
            insert_range.InsertAfter(config["block"])

        doc.SaveAs(output_path)
        doc.Close()
        print(f"SUCCESS: {jd_name} -> {output_name}")
        return True
    except Exception as e:
        print(f"ERROR: {jd_name} - {str(e)}")
        try:
            doc.Close(False)
        except:
            pass
        return False

def main():
    print("Starting JD updates...")
    print(f"Input: {input_folder}")
    print(f"Output: {output_folder}")
    print("-" * 60)

    word = win32.gencache.EnsureDispatch('Word.Application')
    word.Visible = False

    success_count = 0
    for jd_name, config in sop_blocks.items():
        if update_jd(word, jd_name, config):
            success_count += 1

    word.Quit()

    print("-" * 60)
    print(f"Complete: {success_count}/{len(sop_blocks)} JDs updated")

if __name__ == "__main__":
    main()
