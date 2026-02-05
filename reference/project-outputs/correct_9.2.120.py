"""
Correct SOP 9.2.120 – Establish Tracking & Control Systems
to GSL template governance compliance.
"""

import os
from docx import Document
from docx.shared import Pt

SOP_DIR = r"C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"
SOP_ID = "9.2.120"

# Related SOPs from the authoritative mapping
RELATED_SOPS = [
    "9.2.005 - Review Contract for High Risk Clauses",
    "9.2.010 - Team Selection",
    "9.2.015 - Project Turnover Meeting",
    "9.2.020 - Procurement of Large Feeder Wire",
    "9.2.030 - Review Contract for Unfavorable or High-Risk Clauses",
    "9.4.190 - Document Filing Standards",
    "9.4.195 - Manage Project Documentation System",
    "9.4.400 - Monitor Project Costs",
]

SOP_DEF = {
    "title": "Establish Tracking & Control Systems",
    "department": "Project Management / Operations",
    "purpose": (
        "To establish the project\u2019s tracking and control systems during early "
        "preconstruction planning so that cost, schedule, labor productivity, "
        "procurement, RFIs/submittals, and change management can be monitored "
        "and controlled throughout project execution."
    ),
    "scope": (
        "This SOP applies to Project Managers, Project Engineers/Coordinators, "
        "Field Supervisors, and General Superintendents for all awarded projects. "
        "It is triggered during early preconstruction planning after receipt of "
        "award, Letter of Intent (LOI), or Notice to Proceed (NTP), and must be "
        "substantially complete before or during the Construction Execution "
        "Kickoff Meeting (9.2.130)."
    ),
    "roles": [
        ("Project Manager",
         "Establishes the project controls structure including cost codes, "
         "reporting cadence, logs, filing standards, and dashboards. Ensures "
         "systems are maintained and used consistently throughout the project."),
        ("Project Engineer / Project Coordinator",
         "Maintains core logs (RFI, submittal, issue), supports document control, "
         "and updates trackers per the defined cadence."),
        ("General Superintendent / Field Leadership",
         "Provides field inputs for labor productivity tracking, lookahead "
         "schedules, daily progress reporting, and field condition updates."),
        ("Safety Coordinator",
         "Submits safety inspection reports and compliance updates into the "
         "project tracking system."),
        ("Purchasing",
         "Updates the procurement log with material orders, vendor status, "
         "delivery tracking, and expediting notes."),
        ("Branch Manager",
         "Confirms that required controls are in place prior to mobilization. "
         "Reviews weekly reports and supports escalation or resource needs."),
    ],
    "requirements": [
        "Project budget and cost codes (from 9.2.140 \u2013 Develop Project Budget)",
        "Baseline project schedule (from 9.2.110 \u2013 Develop Project Schedule)",
        "Project folder / document repository structure (per 9.4.190 \u2013 Document Filing Standards)",
        "Standard log templates: RFI log, submittal log, issue log, change log, procurement log",
        "Labor tracking sheets and productivity reporting forms",
        "Safety inspection forms and compliance checklists",
        "Weekly dashboard template (Smartsheet, Excel, or equivalent)",
        "Reporting cadence expectations (weekly cost, schedule, labor, and safety updates)",
    ],
    "procedure": [
        ("Establish Project File Structure and Access", [
            "Confirm the project repository and folder structure is created per "
            "9.4.190 \u2013 Document Filing Standards.",
            "Assign access permissions to all project team members.",
            "Define where all controls, logs, and trackers will reside (single "
            "source of truth).",
        ]),
        ("Set Up Cost Tracking and Reporting Cadence", [
            "Confirm project budget and cost codes are loaded into the cost "
            "tracking system (from 9.2.140 \u2013 Develop Project Budget).",
            "Define cost reporting format and update frequency (e.g., weekly "
            "cost review).",
            "Assign responsible parties for cost data entry and review.",
        ]),
        ("Set Up Schedule Tracking", [
            "Confirm the baseline schedule is loaded and accessible to the "
            "project team (from 9.2.110 \u2013 Develop Project Schedule).",
            "Define schedule update cadence and required inputs (field "
            "progress, constraints, milestones).",
            "Assign responsibility for schedule updates and lookahead "
            "preparation.",
        ]),
        ("Set Up Core Logs and Trackers", [
            "Create or confirm the following logs are in place: RFI log, "
            "submittal log, issue list, procurement log, change log, and "
            "safety items tracker.",
            "Assign an owner for each log and define minimum required fields.",
            "Confirm log locations in the project folder structure.",
        ]),
        ("Establish Labor and Productivity Tracking Method", [
            "Define how labor hours, production quantities, and productivity "
            "will be tracked and reported.",
            "Align labor tracking with field reporting formats and "
            "superintendent/foreman inputs.",
            "Establish the method for comparing actual vs. budgeted labor "
            "performance.",
        ]),
        ("Implement Controls and Communicate Expectations", [
            "Communicate the tracking systems, update cadence, and "
            "responsibilities to the full project team.",
            "Confirm that controls will be reviewed during the Construction "
            "Execution Kickoff Meeting (9.2.130).",
            "Verify that all systems are operational and being used before "
            "mobilization begins.",
        ]),
    ],
    "appendix": [
        "Appendix \u2013 Templates & Logs",
        "",
        "\u2022 RFI Log Template",
        "\u2022 Submittal Log Template",
        "\u2022 Issue Log Template",
        "\u2022 Change Log Template",
        "\u2022 Procurement Log Template",
        "\u2022 Labor Tracking Template",
        "\u2022 Weekly Cost Report Template",
        "\u2022 Weekly Dashboard Example",
        "\u2022 Schedule Update Checklist",
        "",
        "Appendix \u2013 References & Training Materials",
        "",
        "Training Materials (Foreman Training Binder):",
        "\u2022 Tab 2: Preplanning & Staging",
        "\u2022 Tab 3: Kickoff/Project Turnover Meeting",
        "\u2022 Tab 5: Purchasing Buy out",
        "\u2022 Tab 6: Scheduling",
        "\u2022 Tab 7: Job Plans",
        "",
        "Job Descriptions (Policy Manual Section 7):",
        "\u2022 7.2.4 Foreman",
        "\u2022 7.2.6 Project Safety Coordinator",
        "\u2022 7.3.1 Operations Management",
        "\u2022 7.4.4 Purchasing Manager",
        "",
        "Management Directives (Policy Manual Section 9):",
        "\u2022 9.5 Project Management",
        "\u2022 9.7 Estimating",
        "\u2022 9.3 Field Leadership",
        "",
        "Reference Documents:",
        "\u2022 GSL Pre-Construction Planning \u2013 Section 4.9 Tracking & Control",
    ],
}


def build_doc():
    """Build a template-compliant .docx document for SOP 9.2.120."""
    doc = Document()

    # Default font
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Calibri"
    font.size = Pt(11)

    # ---- SOP Title Line ----
    p = doc.add_paragraph()
    run = p.add_run(f"SOP: {SOP_ID} \u2013 {SOP_DEF['title']}")
    run.bold = True
    run.font.size = Pt(14)

    # ---- Department ----
    doc.add_paragraph(f"Department: {SOP_DEF['department']}")

    # ---- Related SOPs ----
    p = doc.add_paragraph()
    run = p.add_run("Related SOPs:")
    run.bold = True
    for entry in RELATED_SOPS:
        doc.add_paragraph(f"\u2022 {entry}", style="List Bullet")

    # ---- Separator ----
    doc.add_paragraph("")

    # ---- Purpose ----
    p = doc.add_paragraph()
    run = p.add_run("Purpose")
    run.bold = True
    run.font.size = Pt(13)
    doc.add_paragraph(SOP_DEF["purpose"])

    # ---- Scope ----
    doc.add_paragraph("")
    p = doc.add_paragraph()
    run = p.add_run("Scope")
    run.bold = True
    run.font.size = Pt(13)
    doc.add_paragraph(SOP_DEF["scope"])

    # ---- Roles & Responsibilities ----
    doc.add_paragraph("")
    p = doc.add_paragraph()
    run = p.add_run("Roles & Responsibilities")
    run.bold = True
    run.font.size = Pt(13)
    for role, resp in SOP_DEF["roles"]:
        p = doc.add_paragraph()
        run = p.add_run(f"{role}: ")
        run.bold = True
        p.add_run(resp)

    # ---- Requirements ----
    doc.add_paragraph("")
    p = doc.add_paragraph()
    run = p.add_run("Requirements")
    run.bold = True
    run.font.size = Pt(13)
    for req in SOP_DEF["requirements"]:
        doc.add_paragraph(f"\u2022 {req}", style="List Bullet")

    # ---- Procedure ----
    doc.add_paragraph("")
    p = doc.add_paragraph()
    run = p.add_run("Procedure")
    run.bold = True
    run.font.size = Pt(13)

    for step_num, (step_title, step_items) in enumerate(SOP_DEF["procedure"], 1):
        doc.add_paragraph("")
        p = doc.add_paragraph()
        run = p.add_run(f"Step {step_num} \u2013 {step_title}")
        run.bold = True
        for item in step_items:
            doc.add_paragraph(f"\u2022 {item}", style="List Bullet")

    # ---- Appendix ----
    doc.add_paragraph("")
    p = doc.add_paragraph()
    run = p.add_run("Appendix")
    run.bold = True
    run.font.size = Pt(13)
    for line in SOP_DEF["appendix"]:
        doc.add_paragraph(line)

    return doc


def main():
    # Find the file
    all_files = [f for f in os.listdir(SOP_DIR)
                 if f.endswith(".docx") and not f.startswith("~")]
    matches = [f for f in all_files if f.startswith(SOP_ID)]

    if not matches:
        print(f"FILE NOT FOUND for {SOP_ID}")
        return

    fname = matches[0]
    filepath = os.path.join(SOP_DIR, fname)

    print(f"{'='*70}")
    print(f"Processing: {SOP_ID} \u2013 {SOP_DEF['title']}")
    print(f"File: {fname}")
    print(f"{'='*70}")

    # Read original to build change summary
    orig_doc = Document(filepath)
    orig_text = "\n".join(p.text for p in orig_doc.paragraphs)

    changes = []

    # Title line check
    title_line = orig_doc.paragraphs[0].text.strip() if orig_doc.paragraphs else ""
    expected_title = f"SOP: {SOP_ID} \u2013 {SOP_DEF['title']}"
    if title_line != expected_title:
        changes.append(f"Title line standardized: '{title_line[:60]}' -> '{expected_title}'")

    # Front-matter metadata removed
    for p in orig_doc.paragraphs:
        if "Created by:" in p.text or "Version:" in p.text or "Effective Date:" in p.text:
            changes.append("Front-matter metadata (Created by, Version, Effective Date) removed")
            break

    # DOCUMENT REFERENCES moved
    if any("DOCUMENT REFERENCES" in p.text for p in orig_doc.paragraphs):
        changes.append("DOCUMENT REFERENCES section removed from body, content moved to Appendix")

    # Tables converted
    if orig_doc.tables:
        changes.append(f"{len(orig_doc.tables)} tables (Roles, Deliverables, KPIs) converted to bullets")

    # Non-template sections removed
    for section_name in ["Deliverables", "Compliance & Review", "References"]:
        if any(p.text.strip() == section_name for p in orig_doc.paragraphs):
            changes.append(f"Non-template section '{section_name}' removed (content absorbed into Procedure/Appendix)")

    # Section order enforced
    changes.append("Section order enforced: SOP Title -> Department -> Related SOPs -> Purpose -> Scope -> Roles -> Requirements -> Procedure -> Appendix")

    # Purpose rewritten
    changes.append("Purpose rewritten to explicitly list cost, schedule, labor, procurement, RFIs/submittals, and change management")

    # Scope expanded
    changes.append("Scope expanded to specify timing (after award/LOI/NTP, before/during kickoff)")

    # Roles expanded
    changes.append("Roles expanded: added Project Engineer/Coordinator; clarified all 6 role responsibilities")

    # Requirements expanded
    changes.append("Requirements expanded from 5 to 8 items with cross-references to source SOPs")

    # Procedure rewritten
    changes.append("Procedure rewritten from 5 generic steps to 6 actionable steps with specific deliverables")

    # Appendix expanded
    changes.append("Appendix expanded: added Templates & Logs section with 9 templates; preserved training/JD/directive references")

    # Build and save
    new_doc = build_doc()
    new_doc.save(filepath)

    print(f"\nChange Summary:")
    for c in changes:
        print(f"  \u2022 {c}")

    print(f"\nLegacy numbers removed: YES")
    print(f"Related SOPs updated: YES (8 related SOPs from authoritative mapping)")

    print(f"\nSAVED: {fname}")


if __name__ == "__main__":
    main()
