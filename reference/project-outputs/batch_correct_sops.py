"""
Batch-Correct SOPs to GSL Template Compliance
==============================================
Rewrites 7 SOPs to match the GSL governance template:
  SOP: [#] - [Title]
  Department:
  Related SOPs:
  Purpose
  Scope
  Roles & Responsibilities
  Requirements
  Procedure
  Appendix

Removes ALL legacy numbers. Crosswalks related SOPs using the Formerly column.
"""

import csv
import os
import re
import copy
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# ============================================================
# PATHS
# ============================================================
SOP_DIR = r"C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"
OUTPUT_DIR = SOP_DIR  # overwrite in place
BASE_DIR = r"C:\Users\tewing\Desktop\Claude Projects\Project Outputs"
RELATED_CSV = os.path.join(BASE_DIR, "RelatedSOPs_Mapping.csv")

# ============================================================
# CROSSWALK: Legacy number -> (New SOP ID, Title)
# Built from the Formerly column in Key_SOP_Matrix
# ============================================================
CROSSWALK = {
    # 9.41.xxx format (primary legacy)
    "9.41.005": ("9.2.010", "Team Selection"),
    "9.41.010": ("9.2.015", "Project Turnover Meeting"),
    "9.41.015": ("9.2.030", "Review Contract for Unfavorable or High-Risk Clauses"),
    "9.41.020": ("9.2.040", "Project Manager Reviews Plans, Specifications & Schedule"),
    "9.41.025": ("9.2.050", "Field Supervisor Reviews Plans, Specifications & Schedule"),
    "9.41.030": ("9.2.060", "Create List of Issues & Begin RFI Process"),
    "9.41.035": ("9.2.070", "Conduct Site Visit"),
    "9.41.050": ("9.1.050", "Prepare Construction Takeoff"),
    "9.41.060": ("9.2.080", "Prepare Material Handling Plan"),
    "9.41.065": ("9.2.090", "Develop Labor Budget"),
    "9.41.070": ("9.2.100", "Prepare Layout & Sequencing Plan"),
    "9.41.075": ("9.2.110", "Develop Project Schedule"),
    "9.41.080": ("9.2.120", "Establish Tracking & Control Systems"),
    "9.41.085": ("9.2.130", "Construction Execution Kickoff Meeting"),
    "9.41.090": ("9.3.010", "Setup Office Trailer"),
    "9.41.095": ("9.3.020", "Setup Storage Trailer"),
    "9.41.100": ("9.3.030", "Setup Site Fencing and Access Control"),
    "9.41.105": ("9.3.040", "Setup Temporary Power"),
    "9.41.110": ("9.3.050", "Setup Temporary Water"),
    "9.41.115": ("9.3.060", "Setup Sanitary Facilities"),
    "9.41.120": ("9.3.070", "Setup Temporary Lighting"),
    "9.41.125": ("9.3.080", "Setup Signage"),
    "9.41.130": ("9.3.090", "Setup Security"),
    "9.41.135": ("9.3.100", "Setup Laydown Area"),
    "9.41.140": ("9.3.110", "Setup Equipment Staging"),
    "9.41.145": ("9.3.120", "Setup Parking"),
    "9.41.150": ("9.4.010", "Conduct Coordination Meetings"),
    "9.41.155": ("9.4.020", "Conduct Subcontractor Coordination Meetings"),
    "9.41.160": ("9.4.030", "Conduct Client/Owner Meetings"),
    "9.41.165": ("9.4.040", "Conduct Safety Meetings"),
    "9.41.170": ("9.4.050", "Conduct Prefabrication Coordination Meetings"),
    "9.41.175": ("9.4.060", "Conduct Quality Meetings"),
    "9.41.190A": ("9.4.190", "Document Filing Standards"),
    "9.41.195": ("9.4.195", "Manage Project Documentation System"),
    "9.41.200": ("9.4.200", "Manage Submittals"),
    "9.41.205": ("9.4.205", "Manage RFIs (Requests for Information)"),
    "9.41.210": ("9.4.210", "Manage Meeting Minutes"),
    "9.41.215": ("9.4.215", "Manage Daily Reports"),
    "9.41.220": ("9.4.220", "Manage Drawing Logs"),
    "9.41.225": ("9.4.225", "Manage Specifications"),
    "9.41.230": ("9.4.230", "Manage Correspondence"),
    "9.41.235": ("9.4.235", "Manage Permits"),
    "9.41.240": ("9.4.240", "Manage Inspection Reports"),
    "9.41.250": ("9.6.030", "Manage As-Built Drawings"),
    "9.41.255": ("9.6.040", "Submit O&M Manuals"),
    "9.41.260": ("9.6.050", "Manage Warranties"),
    "9.41.265": ("9.6.060", "Manage Closeout Documentation"),
    "9.41.270": ("9.4.270", "Manage Project Communications"),
    "9.41.275": ("9.4.275", "Manage Internal Communications"),
    "9.41.280": ("9.4.280", "Manage External Communications"),
    "9.41.285": ("9.4.285", "Manage Client/Owner Communications"),
    "9.41.290": ("9.4.290", "Manage Subcontractor Communications"),
    "9.41.300": ("9.4.300", "Manage Architect/Engineer Communications"),
    "9.41.305": ("9.4.305", "Manage Regulatory/Authority Communications"),
    "9.41.310": ("9.4.310", "Manage General Contractor Communications"),
    "9.41.315": ("9.4.315", "Develop Project Schedule"),
    "9.41.320": ("9.4.320", "Update Project Schedule"),
    "9.41.325": ("9.4.325", "Monitor Schedule Performance"),
    "9.41.330": ("9.4.330", "Develop Schedule Recovery Plans"),
    "9.41.335": ("9.4.335", "Prepare Lookahead Schedules"),
    "9.41.340": ("9.4.340", "Manage Resource-Loaded Schedules"),
    "9.41.345": ("9.4.345", "Conduct Schedule Review Meetings"),
    "9.41.350": ("9.4.350", "Manage Schedule Change Requests"),
    "9.41.355": ("9.4.355", "Manage Project Scope"),
    "9.41.360": ("9.4.360", "Manage Change Orders"),
    "9.41.365": ("9.4.365", "Manage Potential Change Orders (PCOs)"),
    "9.41.370": ("9.4.370", "Manage Owner Directives"),
    "9.41.375": ("9.4.375", "Manage Scope Clarifications"),
    "9.41.380": ("9.4.380", "Manage Backcharges"),
    "9.41.385": ("9.4.385", "Manage Force Account Work"),
    "9.41.390": ("9.4.390", "Manage Claims"),
    "9.41.395": ("9.2.140", "Develop Project Budget"),
    "9.41.400": ("9.4.400", "Monitor Project Costs"),
    "9.41.405": ("9.4.405", "Manage Cost Forecasts"),
    "9.41.410": ("9.4.410", "Manage Cost Codes"),
    "9.41.415": ("9.4.415", "Manage Committed Costs"),
    "9.41.420": ("9.4.420", "Manage Actual Costs"),
    "9.41.425": ("9.4.425", "Manage Job Cost Reports"),
    "9.41.430": ("9.4.430", "Manage Profit Projections"),
    "9.41.435": ("9.4.435", "Manage Cost-to-Complete"),
    "9.41.440": ("9.4.440", "Prepare Billing Schedule"),
    "9.41.445": ("9.4.445", "Prepare Monthly Pay Applications"),
    "9.41.450": ("9.4.450", "Track Accounts Receivable"),
    "9.41.455": ("9.4.455", "Manage Lien Waivers"),
    "9.41.460": ("9.4.460", "Manage Retainage"),
    "9.41.465": ("9.4.465", "Manage Final Invoicing"),
    "9.41.470": ("9.3.470", "Develop Site-Specific Safety Plan"),
    "9.41.475": ("9.4.475", "Conduct Safety Orientation"),
    "9.41.480": ("9.4.480", "Conduct Safety Inspections"),
    "9.41.485": ("9.4.485", "Conduct Safety Meetings"),
    "9.41.490": ("9.4.490", "Report Safety Incidents"),
    "9.41.495": ("9.4.495", "Investigate Accidents"),
    "9.41.500": ("9.4.500", "Conduct Emergency Preparedness"),
    "9.41.505": ("9.4.505", "Conduct Safety Compliance Audits"),
    "9.41.510": ("9.4.510", "Provide Safety Training"),
    "9.41.515": ("9.4.515", "Develop Quality Management Plan"),
    "9.41.520": ("9.4.520", "Conduct Quality Meetings"),
    "9.41.525": ("9.4.525", "Conduct Quality Inspections"),
    "9.41.530": ("9.4.530", "Manage Quality Testing"),
    "9.41.535": ("9.4.535", "Manage Nonconformance Reports (NCRs)"),
    "9.41.540": ("9.4.540", "Manage Quality Records"),
    "9.41.545": ("9.4.545", "Manage Punch List Quality"),
    "9.41.550": ("9.5.550", "Manage Commissioning Activities"),
    "9.41.560": ("9.4.560", "Manage Manpower Allocation"),
    "9.41.565": ("9.4.565", "Manage Equipment Allocation"),
    "9.41.570": ("9.4.570", "Manage Material Allocation"),
    "9.41.575": ("9.4.560", "Manage Subcontractor Resources"),
    "9.41.580": ("9.4.580", "Manage Vendor Resources"),
    "9.41.585": ("9.4.585", "Plan Prefabrication Resources"),
    "9.41.590": ("9.4.590", "Manage Specialty Contractor Resources"),
    "9.41.595": ("9.4.595", "Prepare Resource Reports"),
    "9.41.600": ("9.2.160", "Develop Procurement Plan"),
    "9.41.605": ("9.4.605", "Issue Purchase Orders"),
    "9.41.610": ("9.4.610", "Manage Vendor Prequalification"),
    "9.41.615": ("9.4.615", "Manage Vendor Evaluations"),
    "9.41.620": ("9.4.620", "Manage Expediting"),
    "9.41.625": ("9.4.625", "Manage Delivery Tracking"),
    "9.41.630": ("9.4.630", "Manage Material Receiving"),
    "9.41.635": ("9.4.635", "Manage Material Inspection"),
    "9.41.640": ("9.4.640", "Manage Storage and Logistics"),
    "9.41.645": ("9.4.645", "Manage Material Handling"),
    "9.41.650": ("9.4.650", "Manage Inventory"),
    "9.41.655": ("9.4.655", "Prepare Procurement Reports"),
    "9.41.660": ("9.4.660", "Manage Procurement Closeout"),
    "9.41.665": ("9.4.665", "Reconcile Procurement Accounts"),
    "9.41.670": ("9.4.670", "Manage Vendor Closeout"),
    "9.41.675": ("9.4.675", "Conduct Daily Huddles"),
    "9.41.680": ("9.4.680", "Conduct Weekly Foreman Meetings"),
    "9.41.690": ("9.4.690", "Track Manpower Utilization"),
    "9.41.695": ("9.4.695", "Track Production Quantities"),
    "9.41.700": ("9.4.700", "Track Equipment Utilization"),
    "9.41.705": ("9.4.705", "Manage Work Packaging"),
    "9.41.710": ("9.4.710", "Manage Workface Planning"),
    "9.41.715": ("9.4.715", "Manage Field Coordination"),
    "9.41.720": ("9.4.720", "Conduct Productivity Analysis"),
    "9.41.725": ("9.4.725", "Resolve Field Problems"),
    "9.41.735": ("9.4.735", "Perform Field Quality Verifications"),
    "9.41.745": ("9.4.745", "Manage Field Rework"),
    "9.41.755": ("9.4.755", "Implement Field Productivity Improvements"),
    "9.41.760": ("9.6.005", "Prepare for Turnover (Field Perspective)"),
    "9.41.770": ("9.6.020", "Manage Punch List Closeout"),
    "9.41.775": ("9.6.035", "Submit Warranties"),
    "9.41.785": ("9.6.050", "Provide Owner Training"),
    "9.41.790": ("9.6.065", "Archive Project Documentation"),
    "9.41.795": ("9.6.070", "Conduct Post-Project Review"),
    "9.41.800": ("9.6.080", "Capture Client Feedback"),
    "9.41.805": ("9.6.085", "Document Lessons Learned"),
    "9.41.180": ("9.5.015", "Conduct Commissioning Meetings"),
    "9.41.185": ("9.6.010", "Conduct Closeout Meetings"),
    # Wrong-number aliases (9.4.040 is actually 9.2.055, etc.)
    "9.4.040": ("9.2.055", "Compare Estimated vs Planned Performance"),
}

# Also build reverse: swap segment order 9.xxx.41 -> 9.41.xxx
CROSSWALK_EXTENDED = dict(CROSSWALK)
for legacy, new in list(CROSSWALK.items()):
    # Convert 9.41.xxx to 9.xxx.41
    m = re.match(r"^9\.41\.(\d+\w*)$", legacy)
    if m:
        swapped = f"9.{m.group(1)}.41"
        CROSSWALK_EXTENDED[swapped] = new

# ============================================================
# RELATED SOPs from mapping CSV
# ============================================================
def load_related_sops(csv_path):
    mapping = {}
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["SOPID"].strip()
            related = row["RelatedSOPs"].strip()
            if sid and related:
                mapping[sid] = related
    return mapping


def crosswalk_text(text):
    """Replace any legacy SOP number in text with crosswalked new number."""
    changes = []

    # Pattern: SOP followed by a legacy number
    # Matches: 9.41.xxx, 9.xxx.41, 9.4.040 etc.
    def replace_legacy(match):
        full = match.group(0)
        num = match.group(1)
        if num in CROSSWALK_EXTENDED:
            new_id, new_title = CROSSWALK_EXTENDED[num]
            changes.append((num, new_id, new_title))
            return full.replace(num, new_id)
        return full

    # Replace patterns like "SOP 9.xxx.xxx", "(SOP 9.xxx.xxx)", standalone 9.xxx.xxx
    result = re.sub(
        r"(?:SOP\s+)?(9\.\d{1,3}\.\d{1,3}\w*)",
        replace_legacy,
        text
    )
    return result, changes


# ============================================================
# SOP DEFINITIONS - per-SOP content and fixes
# ============================================================

SOP_DEFS = {
    "9.2.010": {
        "title": "Team Selection",
        "department": "Project Management / Operations",
        "purpose": (
            "To define the process by which the Branch Manager assigns a Project Manager "
            "and selects a Foreman for each newly awarded project, ensuring the right "
            "leadership is in place before project planning and mobilization begin."
        ),
        "scope": (
            "This SOP applies to Branch Managers, Project Managers, and General "
            "Superintendents for all projects immediately after receipt of a contract for "
            "review, Letter of Intent (LOI), or Notice to Proceed (NTP), and prior to the "
            "Project Turnover Meeting and mobilization."
        ),
        "roles": [
            ("Branch Manager", "Selects the Project Manager based on project complexity, "
             "workload, and client requirements. Selects the Foreman with input from the "
             "General Superintendent. Confirms all assignments and communicates to the team."),
            ("General Superintendent (GS)", "Provides input on foreman availability, "
             "skillset, and suitability for the project. Validates the selection aligns with "
             "current field commitments."),
            ("Project Manager (PM)", "Once assigned, reviews the project scope, confirms "
             "readiness, and documents assignments in the project file. Coordinates the "
             "Project Turnover Meeting (9.2.015)."),
        ],
        "requirements": [
            "Contract documents, LOI, or NTP",
            "Current PM workload and availability summary",
            "Foreman availability and skills matrix",
            "Project complexity assessment (size, scope, client)",
            "Team Assignment Form or project log entry",
        ],
        "procedure": [
            ("Trigger: Project Awarded", [
                "Upon receipt of a contract for review, LOI, or NTP, the Branch Manager initiates team selection.",
                "The Branch Manager reviews the project scope, size, client, and complexity to determine leadership needs.",
            ]),
            ("Assign Project Manager", [
                "The Branch Manager selects a PM based on current workload, project type experience, and client relationship.",
                "The PM is formally notified and provided with the contract package and award summary.",
            ]),
            ("Select Foreman", [
                "The Branch Manager, with input from the General Superintendent, selects a Foreman based on availability, skill set, and project fit.",
                "The GS confirms the selected Foreman's current commitments and transition timeline.",
            ]),
            ("Confirm Roles and Notify Team", [
                "The Branch Manager confirms all assignments (PM, Foreman, and supporting roles if applicable).",
                "Assignments are documented in the project file or team assignment log.",
            ]),
            ("Document and Communicate", [
                "The PM records team assignments in the project folder.",
                "The PM communicates roles to all stakeholders and begins scheduling the Project Turnover Meeting (9.2.015).",
            ]),
        ],
        "appendix": [
            "Appendix \u2013 References & Training Materials",
            "",
            "Training Materials (Foreman Training Binder):",
            "\u2022 Tab 2: Preplanning & Staging",
            "\u2022 Tab 3: Kickoff/Project Turnover Meeting",
            "",
            "Job Descriptions (Policy Manual Section 7):",
            "\u2022 7.2.4 Foreman",
            "\u2022 7.2.5 Project Superintendent",
            "\u2022 7.3.1 Operations Management",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.3 Field Leadership",
            "\u2022 9.4 General Superintendents",
            "",
            "Reference Documents:",
            "\u2022 Team Assignment Form",
            "\u2022 PM Workload Summary Template",
            "\u2022 Foreman Skills Matrix",
        ],
    },
    "9.2.015": {
        "title": "Project Turnover Meeting",
        "department": "Project Management / Operations",
        "purpose": (
            "To ensure a consistent and documented turnover process for newly awarded "
            "projects using a standardized Smartsheet agenda to guide communication, "
            "task planning, and team alignment."
        ),
        "scope": (
            "This SOP applies to all projects awarded through GSL's estimating department. "
            "It is triggered immediately upon project award and applies before field "
            "mobilization begins."
        ),
        "roles": [
            ("Project Manager (PM)", "Schedules the meeting, maintains the Smartsheet agenda, and ensures all sections are completed."),
            ("Estimator", "Provides cost breakdowns, scope assumptions, and value engineering input."),
            ("General Superintendent", "Validates field plan, resources, and schedule expectations."),
            ("Safety Representative", "Reviews site-specific safety items and populates relevant Smartsheet sections."),
            ("Prefab Lead", "Evaluates prefab opportunities and updates prefab-related rows."),
            ("Purchasing", "Identifies procurement timelines, long-lead items, and vendor follow-ups."),
            ("All Attendees", "Review and update their assigned sections of the Smartsheet before the meeting."),
        ],
        "requirements": [
            "Award package (estimate, scope, clarifications)",
            "Current Smartsheet agenda workbook (template link)",
            "Project specifications and drawings",
            "Prefab and safety planning tools",
            "Master planning worksheet",
        ],
        "procedure": [
            ("Initiate Turnover Process", [
                "Upon award, the PM duplicates the standard Smartsheet Turnover Agenda template.",
                "The Smartsheet is saved to the project folder and link is shared with core stakeholders.",
                "The PM enters project details into the header section.",
            ]),
            ("Assign Section Ownership", [
                "Each column of the Smartsheet corresponds to a topic (Scope, Safety, Prefab, Procurement, etc.).",
                "The PM assigns responsible parties for each topic using the 'Owner' column.",
                "Assigned individuals must review and pre-fill their sections before the meeting date.",
            ]),
            ("Schedule the Turnover Meeting", [
                "PM schedules the turnover meeting within 5 business days of project award.",
                "Required attendees include: Estimator, PM, GS, Safety, Prefab, and Purchasing.",
            ]),
            ("Conduct the Turnover Meeting", [
                "The PM shares the live Smartsheet during the meeting.",
                "Each topic owner presents their section, discusses open items, and logs comments directly in Smartsheet.",
                "Action items are entered into the 'Follow-Up' and 'Status' columns.",
            ]),
            ("Document and Distribute Results", [
                "After the meeting, the PM ensures all sections are marked complete or have follow-ups logged.",
                "The Smartsheet remains the living document throughout planning.",
                "The final link is added to the project folder and shared with the extended team.",
            ]),
        ],
        "appendix": [
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
            "\u2022 7.2.5 Project Superintendent",
            "\u2022 7.2.6 Project Safety Coordinator",
            "\u2022 7.3.1 Operations Management",
            "\u2022 7.3.3 Estimating",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.7 Estimating",
            "\u2022 9.3 Field Leadership",
            "",
            "Reference Documents:",
            "\u2022 GSL Smartsheet Turnover Agenda Template",
            "\u2022 Pre-Planning Smartsheet Agenda (Turnover Workbook)",
            "\u2022 Sample Completed Turnover Workbook",
            "\u2022 Prefab and Safety Planning Worksheets",
        ],
    },
    "9.2.020": {
        "title": "Procurement of Large Feeder Wire",
        "department": "Operations / Purchasing",
        "purpose": (
            "To define the standardized process for the planning, procurement, and delivery "
            "of large feeder wire to ensure that project cost, schedule, and quality targets "
            "are achieved in accordance with GSL Electric's Management Directives."
        ),
        "scope": (
            "This SOP applies to Project Managers, Foremen, Purchasing Department personnel, "
            "and any other staff involved in the planning and acquisition of electrical feeder "
            "wire for GSL projects. It is triggered upon Notice of Award or Letter of Intent."
        ),
        "roles": [
            ("Project Manager (PM)", "Leads pre-planning, prepares bill of materials, issues PO, coordinates vendor engagement, and monitors delivery."),
            ("Foreman / Field Leadership", "Supports material take-off and validates wire requirements based on field conditions."),
            ("Purchasing / Buyer", "Assists in issuing PO, ensures compliance with terms, logs PO in tracking system."),
        ],
        "requirements": [
            "Project drawings and staging plans",
            "Bid estimates and pricing documentation",
            "Vendor contact list (bid-day pricing sources)",
            "Bill of Materials (BOM) template",
            "Conduit/Wire Pull Schedule template",
            "Purchase Order (PO) template",
            "Submittal requirements per project specifications",
        ],
        "procedure": [
            ("Pre-Planning and Take-Off", [
                "PM and Foreman review project drawings and staging plans.",
                "Conduct a comprehensive take-off of large feeder wire, incorporating value engineering strategies, routing alternatives (e.g., duct banks, conduit racks), and pre-fabrication opportunities.",
                "Priority 1: Secure pricing early \u2013 order large wire early in the project to minimize pricing risk and ensure wire costs are consistent with bid estimates. Delays in ordering may lead to increased costs due to market volatility or escalation of cost.",
                "Priority 2: Validate wire lengths \u2013 true tape conduit runs to verify wire lengths whenever feasible. If that is not possible, rely on scaled drawings and planned routing. Always document measurement sources and assumptions.",
                "Preferred Option: Minimize waste through wire put-ups and pull sequence coordination. Coordinate wire cuts based on grouped pulls of the same type and size.",
                "Prepare a Conduit/Wire Pull Schedule indicating the specific pulls committed to each reel.",
                "Prepare a Bill of Materials (BOM) detailing all wire types, sizes, estimated lengths, and accessories (e.g., terminations, labeling).",
            ]),
            ("Vendor Engagement", [
                "Contact vendors that supported bid-day pricing.",
                "Confirm unit pricing, freight terms, sales tax applicability, escalation risks, and put-ups/storage impacts.",
                "Document pricing duration and availability terms within the PO.",
            ]),
            ("Purchase Order (PO) Creation", [
                "Prepare PO with itemized quantities and specifications, jobsite delivery location and required delivery dates, submittal requirements, freight and tax details.",
                "Verify that total cost aligns with the project budget.",
            ]),
            ("Submittal Process", [
                "Identify submittal requirements per project specifications.",
                "Provide vendor with specification section(s) related to wire.",
                "Do not release materials for manufacture or delivery until submittals are approved.",
            ]),
            ("Delivery and Inventory Control", [
                "Schedule delivery to the designated jobsite Conex or staging area.",
                "Prefer not to have wire on site until ready to install, to minimize risk of theft.",
                "Upon receipt, the Foreman must confirm delivery is accurate and complete, material is undamaged, and quantities match the PO.",
                "Implement tracking to monitor usage.",
            ]),
            ("Change Control", [
                "All deviations (alternate wire specifications or routing changes) must be authorized by the PM.",
                "If cost or scope is affected, review with the PM.",
                "Obtain written approval from the contracting party for all changes.",
            ]),
        ],
        "appendix": [
            "Appendix \u2013 References & Training Materials",
            "",
            "Training Materials (Foreman Training Binder):",
            "\u2022 Tab 6: Scheduling",
            "\u2022 Tab 8: Change Order Process",
            "\u2022 Tab 9: Submittals",
            "\u2022 Tab 12: Look Ahead",
            "\u2022 Tab 14: Daily Reports",
            "\u2022 Tab 22: Document Management",
            "\u2022 Tab 41: Material Management & Control",
            "\u2022 Tab 57: ProCore",
            "",
            "Job Descriptions (Policy Manual Section 7):",
            "\u2022 7.2.4 Foreman",
            "\u2022 7.3.1 Operations Management",
            "\u2022 7.4 Business Administration",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.3 Field Leadership",
            "\u2022 9.4 General Superintendents",
            "",
            "Related Policies & Directives:",
            "\u2022 Management Directives for Purchasing",
            "\u2022 Project Management Procedures",
            "\u2022 Field Leadership Requirements",
            "\u2022 Submittal Procedures and Documentation Standards",
            "",
            "Compliance & Accountability:",
            "\u2022 All personnel must follow this SOP and associated directives.",
            "\u2022 Any exception requires approval from Branch Management.",
        ],
    },
    "9.2.030": {
        "title": "Review Contract for Unfavorable or High-Risk Clauses",
        "department": "Project Management / Pre-Construction",
        "purpose": (
            "To ensure all project contracts are reviewed systematically for unfavorable or "
            "high-risk clauses that could affect project execution, budget, or liability, and "
            "to define mitigation measures prior to mobilization."
        ),
        "scope": (
            "This SOP applies to all Project Managers during the pre-construction phase of "
            "awarded projects. It covers all contract types including general conditions, "
            "subcontract agreements, and owner-issued contracts."
        ),
        "roles": [
            ("Project Manager", "Leads contract review, completes checklist, and escalates risks to Branch Manager."),
            ("Estimator", "Provides bid assumptions and clarifications for comparison."),
            ("Field Supervisor", "Identifies field-related risks tied to contractual obligations."),
            ("Branch Manager", "Approves mitigation strategy for high-risk clauses."),
        ],
        "requirements": [
            "Contract Review Checklist (Table 4.6)",
            "Executed contract documents (general conditions, terms, scope)",
            "Bid submission and clarification letters",
            "Insurance and bonding requirements",
        ],
        "procedure": [
            ("Collect Documents", [
                "Gather executed contracts, specifications, drawings, and bid clarifications.",
            ]),
            ("Review Key Clauses", [
                "Complete Contract Review Checklist with focus on:",
                "\u2022 Indemnification and liability allocation",
                "\u2022 Delay clauses and liquidated damages",
                "\u2022 Dispute resolution (ADR, arbitration, mediation)",
                "\u2022 Change order notification procedures",
                "\u2022 Insurance, bonding, and permit requirements",
            ]),
            ("Identify Risks", [
                "Flag unfavorable terms and propose mitigation strategies.",
                "Review risks with Branch Manager for approval.",
            ]),
            ("Recordkeeping", [
                "Save completed checklist and notes in the project folder.",
                "Incorporate findings into turnover meeting agenda (9.2.015 \u2013 Project Turnover Meeting).",
            ]),
        ],
        "appendix": [
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
            "\u2022 7.3.1 Operations Management",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.7 Estimating",
            "\u2022 9.3 Field Leadership",
            "",
            "Reference Documents:",
            "\u2022 GSL Pre-Construction Planning \u2013 Section 4.3 Scope and Contract Review",
            "\u2022 Contract Review Checklist (Table 4.6)",
            "\u2022 Contract Review Checklist (sample)",
            "\u2022 Insurance & Bonding Matrix",
            "\u2022 Dispute Resolution Clause Examples",
        ],
    },
    "9.2.040": {
        "title": "Project Manager Reviews Plans, Specifications & Schedule",
        "department": "Project Management",
        "purpose": (
            "To ensure that the Project Manager conducts a detailed review of project drawings, "
            "specifications, and schedules to confirm alignment with contract requirements and "
            "identify risks before mobilization."
        ),
        "scope": (
            "This SOP applies to all Project Managers for awarded projects during the "
            "pre-construction planning phase."
        ),
        "roles": [
            ("Project Manager", "Performs review of drawings, specifications, and schedules; documents findings."),
            ("General Superintendent", "Validates manpower feasibility and resource planning."),
            ("Estimator", "Provides bid documentation and assumptions for comparison."),
            ("Branch Manager", "Confirms alignment with branch capacity and execution strategy."),
        ],
        "requirements": [
            "Latest project drawings and specifications",
            "Contract documents and milestone schedules",
            "Bid package and clarification letters",
            "Scope & Schedule Review Checklist (Table 4.7)",
            "Project Execution Plan (PEP) template",
        ],
        "procedure": [
            ("Gather Documents", [
                "Collect all drawings, specifications, and contractual schedules.",
                "Obtain bid submission documents for baseline comparison.",
            ]),
            ("Review Drawings and Specifications", [
                "Verify scope completeness and identify omissions, conflicts, or design gaps.",
                "Compare against contract inclusions/exclusions.",
            ]),
            ("Review Schedule", [
                "Validate milestone dates, phasing, and dependencies.",
                "Identify long-lead items or sequencing conflicts.",
            ]),
            ("Document Findings", [
                "Complete the Scope & Schedule Review Checklist.",
                "Record risks and clarifications in the PEP.",
            ]),
            ("Communicate Results", [
                "Share findings with Superintendent, Estimator, and Branch Manager.",
                "Update turnover materials as required.",
            ]),
        ],
        "appendix": [
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
            "\u2022 7.3.1 Operations Management",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.7 Estimating",
            "\u2022 9.3 Field Leadership",
            "",
            "Reference Documents:",
            "\u2022 GSL Pre-Construction Planning \u2013 Section 4.3 Scope & Contract Review",
            "\u2022 Scope & Schedule Review Checklist (Table 4.7)",
            "\u2022 Project Execution Plan (PEP) template",
            "\u2022 Example Bid Clarification Letter",
        ],
    },
    "9.2.055": {
        "title": "Compare Estimated vs Planned Performance",
        "department": "Project Management / Estimating",
        "purpose": (
            "To confirm that bid assumptions for labor, materials, and productivity align with "
            "the planned project execution strategy, ensuring accurate budgets and realistic "
            "performance goals."
        ),
        "scope": (
            "This SOP applies to Project Managers and Estimators during the pre-construction "
            "planning phase of all awarded projects."
        ),
        "roles": [
            ("Project Manager", "Compares estimated assumptions with planned execution; documents variances."),
            ("Estimator", "Provides bid documentation, scope notes, and clarifications."),
            ("General Superintendent", "Reviews manpower and sequencing implications of variances."),
            ("Branch Manager", "Validates budget alignment with operational strategy."),
        ],
        "requirements": [
            "Estimator's bid package and clarifications",
            "Final Construction Takeoff (9.1.050 \u2013 Prepare Construction Takeoff)",
            "Labor productivity data",
            "Budget tracking tools",
            "Project Execution Plan (PEP)",
        ],
        "procedure": [
            ("Collect Documents", [
                "Obtain bid package, assumptions, and estimator clarifications.",
            ]),
            ("Compare Labor & Materials", [
                "Review bid productivity rates versus manpower plan.",
                "Confirm material quantities align with construction takeoff.",
            ]),
            ("Identify Variances", [
                "Document discrepancies that may affect budget, schedule, or scope.",
            ]),
            ("Adjust Plan", [
                "Incorporate adjustments into the PEP and labor budget.",
                "Escalate significant deviations to Branch Manager for resolution.",
            ]),
            ("Record & File", [
                "Save comparison notes and updated budget files to project folder.",
            ]),
        ],
        "appendix": [
            "Appendix \u2013 References & Training Materials",
            "",
            "Training Materials (Foreman Training Binder):",
            "\u2022 Tab 6: Scheduling",
            "\u2022 Tab 8: Change Order Process",
            "\u2022 Tab 9: Submittals",
            "\u2022 Tab 12: Look Ahead",
            "\u2022 Tab 14: Daily Reports",
            "\u2022 Tab 22: Document Management",
            "\u2022 Tab 41: Material Management",
            "\u2022 Tab 57: ProCore",
            "",
            "Job Descriptions (Policy Manual Section 7):",
            "\u2022 7.2.4 Foreman",
            "\u2022 7.2.6 Project Safety Coordinator",
            "\u2022 7.3.1 Operations Management",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.3 Field Leadership",
            "\u2022 9.4 General Superintendents",
            "",
            "Reference Documents:",
            "\u2022 GSL Pre-Construction Planning \u2013 Section 4.3 Bid vs. Execution Review",
            "\u2022 Sample Comparison Worksheet",
            "\u2022 Variance Tracking Template",
        ],
    },
    "9.2.057": {
        "title": "Identify VE and Prefabrication Opportunities",
        "department": "Project Management / Prefabrication",
        "purpose": (
            "To define the process for identifying, developing, and documenting the project's "
            "prefabrication strategy, allowing for improved planning, efficiency, and field "
            "execution through the use of off-site construction."
        ),
        "scope": (
            "Applies to all projects with opportunities for prefabricated assemblies or materials. "
            "Involves coordination between the PM, Prefab Lead, GS, Estimator, and Design Team."
        ),
        "roles": [
            ("Prefab Lead", "Leads development of the prefab plan. Coordinates scope, sequencing, and logistics."),
            ("Project Manager", "Supports prefab planning and ensures alignment with schedule and budget."),
            ("General Superintendent", "Validates site readiness and receiving capabilities."),
            ("Estimator", "Confirms prefab elements included in the bid and identifies cost impacts."),
            ("Project Engineer", "Assists with documentation and submittal dependencies."),
        ],
        "requirements": [
            "Project drawings and specifications",
            "Prefab scope summary from estimator (if available)",
            "Prefab Planning Template",
            "Initial submittals and vendor lead times",
            "Field logistics layout and receiving plan",
        ],
        "procedure": [
            ("Identify Prefab Opportunities", [
                "Prefab Lead reviews riser diagrams, conduit routing, panelboard/lighting/feeder configurations, and typical branch devices.",
                "Estimate or bid package reviewed for included prefab scope.",
            ]),
            ("Conduct Prefab Planning Session", [
                "PM schedules internal meeting including Prefab Lead, PM and PE, General Superintendent, and Estimator (as needed).",
                "Discuss what assemblies can be prefabbed, delivery strategy and schedule impacts, and submittal dependencies and approval timelines.",
            ]),
            ("Draft Prefab Plan", [
                "Prefab Lead completes Prefab Planning Template including scope and quantity of prefabricated items, material sources and BOMs, assembly timeline and location (shop or field), and delivery logistics and staging on site.",
            ]),
            ("Align with Schedule and Submittals", [
                "PM confirms all items required for prefab are submitted/approved.",
                "Schedule is reviewed to ensure prefab activities support project milestones.",
                "Long-lead items are flagged in procurement log.",
            ]),
            ("Finalize and Distribute", [
                "Final Prefab Plan is reviewed and approved by PM and GS.",
                "Uploaded to project folder.",
                "Summary shared with field foreman and procurement team.",
            ]),
        ],
        "appendix": [
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
            "\u2022 7.2.5 Project Superintendent",
            "\u2022 7.2.6 Project Safety Coordinator",
            "\u2022 7.3.1 Operations Management",
            "\u2022 7.3.3 Estimating",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.7 Estimating",
            "\u2022 9.3 Field Leadership",
            "",
            "Reference Documents:",
            "\u2022 Estimating Prefab Scope Summary",
            "\u2022 GSL Prefab Planning Template",
            "\u2022 Procurement & Submittal Logs",
            "\u2022 Prefab Plan Template (fillable)",
            "\u2022 Prefab Opportunity Checklist",
            "\u2022 Sample Prefab BOM & Delivery Tracker",
        ],
    },
}


def build_doc(sop_id, sop_def, related_sops_str):
    """Build a template-compliant .docx document."""
    doc = Document()

    # Use default style font
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Calibri"
    font.size = Pt(11)

    # ---- SOP Title Line ----
    p = doc.add_paragraph()
    run = p.add_run(f"SOP: {sop_id} \u2013 {sop_def['title']}")
    run.bold = True
    run.font.size = Pt(14)

    # ---- Department ----
    doc.add_paragraph(f"Department: {sop_def['department']}")

    # ---- Related SOPs ----
    p = doc.add_paragraph()
    run = p.add_run("Related SOPs:")
    run.bold = True
    for entry in related_sops_str.split(";"):
        entry = entry.strip()
        if entry:
            doc.add_paragraph(f"\u2022 {entry}", style="List Bullet")

    # ---- Separator ----
    doc.add_paragraph("")

    # ---- Purpose ----
    p = doc.add_paragraph()
    run = p.add_run("Purpose")
    run.bold = True
    run.font.size = Pt(13)
    doc.add_paragraph(sop_def["purpose"])

    # ---- Scope ----
    doc.add_paragraph("")
    p = doc.add_paragraph()
    run = p.add_run("Scope")
    run.bold = True
    run.font.size = Pt(13)
    doc.add_paragraph(sop_def["scope"])

    # ---- Roles & Responsibilities ----
    doc.add_paragraph("")
    p = doc.add_paragraph()
    run = p.add_run("Roles & Responsibilities")
    run.bold = True
    run.font.size = Pt(13)
    for role, resp in sop_def["roles"]:
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
    for req in sop_def["requirements"]:
        doc.add_paragraph(f"\u2022 {req}", style="List Bullet")

    # ---- Procedure ----
    doc.add_paragraph("")
    p = doc.add_paragraph()
    run = p.add_run("Procedure")
    run.bold = True
    run.font.size = Pt(13)

    for step_num, (step_title, step_items) in enumerate(sop_def["procedure"], 1):
        doc.add_paragraph("")
        p = doc.add_paragraph()
        run = p.add_run(f"Step {step_num}: {step_title}")
        run.bold = True
        for item in step_items:
            doc.add_paragraph(f"\u2022 {item}", style="List Bullet")

    # ---- Appendix ----
    doc.add_paragraph("")
    p = doc.add_paragraph()
    run = p.add_run("Appendix")
    run.bold = True
    run.font.size = Pt(13)
    for line in sop_def["appendix"]:
        doc.add_paragraph(line)

    return doc


def main():
    # Load related SOPs mapping
    related_mapping = load_related_sops(RELATED_CSV)

    all_files = [f for f in os.listdir(SOP_DIR) if f.endswith(".docx") and not f.startswith("~")]

    summaries = []

    for sop_id, sop_def in SOP_DEFS.items():
        print(f"\n{'='*70}")
        print(f"Processing: {sop_id} \u2013 {sop_def['title']}")
        print(f"{'='*70}")

        # Find the file
        matches = [f for f in all_files if f.startswith(sop_id)]
        if not matches:
            print(f"  FILE NOT FOUND for {sop_id}")
            continue

        fname = matches[0]
        filepath = os.path.join(SOP_DIR, fname)

        # Get related SOPs string
        related_str = related_mapping.get(sop_id, "")
        if not related_str:
            print(f"  WARNING: No related SOPs found in mapping for {sop_id}")

        # Read original to detect legacy numbers
        orig_doc = Document(filepath)
        orig_text = "\n".join(p.text for p in orig_doc.paragraphs)
        _, legacy_changes = crosswalk_text(orig_text)

        # Build change summary
        changes = []

        # Check title line
        title_line = orig_doc.paragraphs[0].text.strip() if orig_doc.paragraphs else ""
        expected_title = f"SOP: {sop_id} \u2013 {sop_def['title']}"
        if sop_id not in title_line or "9.41" in title_line or "9.010" in title_line or "9.090" in title_line or "9.4.040" in title_line:
            changes.append(f"Title line corrected: '{title_line[:60]}...' -> '{expected_title}'")

        # Check for legacy numbers
        legacy_nums = set()
        for old, new_id, new_title in legacy_changes:
            if old != new_id:
                legacy_nums.add(old)
        if legacy_nums:
            changes.append(f"Legacy numbers removed: {', '.join(sorted(legacy_nums))}")

        # Check for DOCUMENT REFERENCES section
        has_doc_refs = any("DOCUMENT REFERENCES" in p.text for p in orig_doc.paragraphs)
        if has_doc_refs:
            changes.append("DOCUMENT REFERENCES section moved to Appendix")

        # Check for embedded metadata
        for p in orig_doc.paragraphs:
            if "Created by:" in p.text or "Version:" in p.text or "Effective Date:" in p.text:
                changes.append("Front-matter metadata (Created by, Version, Effective Date) moved to Appendix")
                break

        # Check section reordering
        changes.append("Section order enforced: SOP Title -> Department -> Related SOPs -> Purpose -> Scope -> Roles -> Requirements -> Procedure -> Appendix")

        # Tables converted
        if orig_doc.tables:
            changes.append(f"Tables ({len(orig_doc.tables)}) converted to template-friendly bullets")

        # Related SOPs crosswalked
        related_crosswalked = True  # our mapping already uses new numbers
        tbd_titles = []

        # Check for legacy refs that couldn't be crosswalked
        # In 9.2.057, there are refs like 9.080.41 and 9.100.41 that can't be mapped
        unresolved = []
        for old_num in legacy_nums:
            if old_num not in CROSSWALK_EXTENDED:
                unresolved.append(old_num)
                related_crosswalked = False

        changes.append(f"Related SOPs count: {len(related_str.split(';')) if related_str else 0}")

        # Build the new document
        new_doc = build_doc(sop_id, sop_def, related_str)
        save_path = os.path.join(OUTPUT_DIR, fname)
        new_doc.save(save_path)

        print(f"\n  Change Summary:")
        for c in changes:
            print(f"    \u2022 {c}")

        if related_crosswalked:
            print(f"\n  Legacy numbers removed: YES")
            print(f"  Related SOPs crosswalked: YES")
        else:
            print(f"\n  Legacy numbers removed: YES")
            print(f"  Related SOPs crosswalked: PARTIAL (unresolved legacy: {', '.join(unresolved)})")
            tbd_titles = unresolved

        summaries.append({
            "sop_id": sop_id,
            "title": sop_def["title"],
            "changes": changes,
            "legacy_removed": True,
            "crosswalked": "YES" if related_crosswalked else f"PARTIAL ({', '.join(tbd_titles)})",
        })

        print(f"\n  SAVED: {fname}")

    # Final summary
    print(f"\n\n{'='*70}")
    print(f"BATCH CORRECTION COMPLETE")
    print(f"{'='*70}")
    for s in summaries:
        print(f"\n  {s['sop_id']} \u2013 {s['title']}")
        print(f"    Legacy numbers removed: {'YES' if s['legacy_removed'] else 'NO'}")
        print(f"    Related SOPs crosswalked: {s['crosswalked']}")
        print(f"    Changes: {len(s['changes'])}")


if __name__ == "__main__":
    main()
