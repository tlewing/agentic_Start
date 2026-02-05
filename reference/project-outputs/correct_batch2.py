"""
Batch-correct 10 SOPs (Mobilization + Safety + Coordination) to GSL template compliance.
Rewrites: 9.3.050, 9.3.060, 9.3.070, 9.3.080, 9.3.090, 9.3.100, 9.3.110, 9.3.120, 9.3.470, 9.4.010
"""
import os
import re
from docx import Document
from docx.shared import Pt

SOP_DIR = r"C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

# Legacy-to-new number crosswalk for body text replacement
LEGACY_CROSSWALK = {
    "9.41.100": ("9.3.030", "Setup Site Fencing and Access Control"),
    "9.41.060": ("9.2.080", "Prepare Material Handling Plan"),
    "9.41.105": ("9.3.040", "Setup Temporary Power"),
    "9.41.110": ("9.3.050", "Setup Temporary Water"),
    "9.41.115": ("9.3.060", "Setup Sanitary Facilities"),
    "9.41.120": ("9.3.070", "Setup Temporary Lighting"),
    "9.41.125": ("9.3.080", "Setup Signage"),
    "9.41.130": ("9.3.090", "Setup Security"),
    "9.41.135": ("9.3.100", "Setup Laydown Area"),
    "9.41.140": ("9.3.110", "Setup Equipment Staging"),
    "9.41.145": ("9.3.120", "Setup Parking"),
    "9.41.470": ("9.3.470", "Develop Site-Specific Safety Plan"),
    "9.41.190A": None,  # Cannot crosswalk -> use TBD
    "9.41.155": None,
    "9.41.160": None,
    "9.41.170": None,
}

# ============================================================
# RELATED SOPs from authoritative mapping
# ============================================================
RELATED_SOPS = {
    "9.3.050": [
        "9.3.010 - Setup Office Trailer",
        "9.3.020 - Setup Storage Trailer",
        "9.3.030 - Setup Site Fencing and Access Control",
        "9.3.040 - Setup Temporary Power",
        "9.3.060 - Setup Sanitary Facilities",
        "9.3.070 - Setup Temporary Lighting",
        "9.3.080 - Setup Signage",
        "9.3.090 - Setup Security",
    ],
    "9.3.060": [
        "9.3.010 - Setup Office Trailer",
        "9.3.020 - Setup Storage Trailer",
        "9.3.030 - Setup Site Fencing and Access Control",
        "9.3.040 - Setup Temporary Power",
        "9.3.050 - Setup Temporary Water",
    ],
    "9.3.070": [
        "9.3.010 - Setup Office Trailer",
        "9.3.020 - Setup Storage Trailer",
        "9.3.030 - Setup Site Fencing and Access Control",
        "9.3.040 - Setup Temporary Power",
        "9.3.050 - Setup Temporary Water",
    ],
    "9.3.080": [
        "9.3.010 - Setup Office Trailer",
        "9.3.020 - Setup Storage Trailer",
        "9.3.030 - Setup Site Fencing and Access Control",
        "9.3.040 - Setup Temporary Power",
        "9.3.050 - Setup Temporary Water",
    ],
    "9.3.090": [
        "9.3.010 - Setup Office Trailer",
        "9.3.020 - Setup Storage Trailer",
        "9.3.030 - Setup Site Fencing and Access Control",
        "9.3.040 - Setup Temporary Power",
        "9.3.050 - Setup Temporary Water",
    ],
    "9.3.100": [
        "9.3.010 - Setup Office Trailer",
        "9.3.020 - Setup Storage Trailer",
        "9.3.030 - Setup Site Fencing and Access Control",
        "9.3.040 - Setup Temporary Power",
        "9.3.050 - Setup Temporary Water",
        "9.4.640 - Manage Storage and Logistics",
    ],
    "9.3.110": [
        "9.3.010 - Setup Office Trailer",
        "9.3.020 - Setup Storage Trailer",
        "9.3.030 - Setup Site Fencing and Access Control",
        "9.3.040 - Setup Temporary Power",
        "9.3.050 - Setup Temporary Water",
        "9.4.565 - Manage Equipment Allocation",
        "9.4.700 - Track Equipment Utilization",
    ],
    "9.3.120": [
        "9.3.010 - Setup Office Trailer",
        "9.3.020 - Setup Storage Trailer",
        "9.3.030 - Setup Site Fencing and Access Control",
        "9.3.040 - Setup Temporary Power",
        "9.3.050 - Setup Temporary Water",
    ],
    "9.3.470": [
        "9.2.070 - Conduct Site Visit",
        "9.3.030 - Setup Site Fencing and Access Control",
        "9.4.475 - Conduct Safety Orientation",
        "9.4.480 - Conduct Safety Inspections",
        "9.4.485 - Conduct Safety Meetings",
        "9.4.490 - Report Safety Incidents",
        "9.4.505 - Conduct Safety Compliance Audits",
        "9.4.510 - Provide Safety Training",
    ],
    "9.4.010": [
        "9.4.020 - Conduct Subcontractor Coordination Meetings",
        "9.4.030 - Conduct Client/Owner Meetings",
        "9.4.040 - Conduct Safety Meetings",
        "9.4.045 - Identify Value Engineering & Prefabrication Opportunities",
        "9.4.050 - Conduct Prefabrication Coordination Meetings",
        "9.4.055 - Procurement of Large Feeder Wire",
        "9.4.060 - Conduct Quality Meetings",
        "9.4.345 - Conduct Schedule Review Meetings",
    ],
}

# ============================================================
# SOP DEFINITIONS
# ============================================================
SOP_DEFS = {
    # ----------------------------------------------------------------
    # 9.3.050 – Setup Temporary Water
    # ----------------------------------------------------------------
    "9.3.050": {
        "title": "Setup Temporary Water",
        "department": "Project Management / Field Operations",
        "purpose": (
            "To provide safe, reliable temporary water supply for construction use, "
            "including dust control, concrete work, cleaning, and sanitary needs."
        ),
        "scope": (
            "This SOP applies to Project Managers and Field Supervisors during "
            "mobilization and throughout project execution."
        ),
        "roles": [
            ("Project Manager",
             "Coordinates with owner/utility for temporary water service connection. "
             "Approves water layout plan and budget."),
            ("Field Supervisor",
             "Oversees installation of piping, hoses, and distribution points. "
             "Verifies system functionality."),
            ("Safety Coordinator",
             "Ensures compliance with environmental and safety requirements."),
        ],
        "requirements": [
            "Site logistics plan",
            "Temporary water layout plan",
            "Utility agreements and permits",
            "Safety and environmental compliance forms",
        ],
        "procedure": [
            ("Identify Requirements", [
                "Determine project water needs (e.g., mixing, cleaning, dust control, sanitary).",
                "Estimate volume and flow rate requirements.",
            ]),
            ("Coordinate with Utility/Owner", [
                "Apply for temporary water meter or hydrant connection.",
                "Confirm service availability and connection timeline.",
            ]),
            ("Install Distribution System", [
                "Connect to utility source and install pipes/hoses to distribution points.",
                "Provide shutoff valves and backflow prevention devices.",
            ]),
            ("Verify Functionality", [
                "Test flow and pressure at all distribution points.",
                "Confirm adequate supply for all identified project needs.",
            ]),
            ("Safety and Environmental Review", [
                "Ensure hoses and lines are protected from vehicle and equipment damage.",
                "Verify compliance with stormwater and environmental regulations.",
            ]),
        ],
        "appendix": [
            "Appendix \u2013 Templates & Checklists",
            "",
            "\u2022 Temporary Water Setup Checklist",
            "\u2022 Example Utility Connection Permit",
            "",
            "Appendix \u2013 References & Training Materials",
            "",
            "Training Materials (Foreman Training Binder):",
            "\u2022 Tab 4: Staging & Job Familiarization",
            "\u2022 Tab 22: Document Management",
            "",
            "Job Descriptions (Policy Manual Section 7):",
            "\u2022 7.2.4 Foreman",
            "\u2022 7.2.6 Project Safety Coordinator",
            "\u2022 7.3.1 Operations Management",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.3 Field Leadership",
        ],
    },

    # ----------------------------------------------------------------
    # 9.3.060 – Setup Sanitary Facilities
    # ----------------------------------------------------------------
    "9.3.060": {
        "title": "Setup Sanitary Facilities",
        "department": "Project Management / Safety",
        "purpose": (
            "To provide adequate sanitary facilities (toilets, wash stations) for "
            "workers in compliance with OSHA requirements and project specifications."
        ),
        "scope": (
            "This SOP applies to Project Managers and Safety Coordinators during "
            "site mobilization and throughout the project."
        ),
        "roles": [
            ("Project Manager",
             "Coordinates contracts with sanitary facility vendors. Approves placement plan."),
            ("Field Supervisor",
             "Determines placement for accessibility and logistics. Coordinates delivery and setup."),
            ("Safety Coordinator",
             "Ensures OSHA compliance and maintains the sanitation inspection log."),
        ],
        "requirements": [
            "Site logistics plan",
            "Sanitary facility vendor contract",
            "OSHA sanitation standards (29 CFR 1926.51)",
            "Inspection log template",
        ],
        "procedure": [
            ("Plan Facility Locations", [
                "Identify accessible, evenly distributed locations per the site logistics plan.",
                "Ensure ADA-compliant units are included if required by project or local regulations.",
            ]),
            ("Secure Vendor Services", [
                "Contract portable toilet and wash station vendor.",
                "Establish service and cleaning schedule (frequency based on headcount).",
            ]),
            ("Install Facilities", [
                "Place units per site logistics plan in approved locations.",
                "Anchor units if required for safety (wind, slope, etc.).",
            ]),
            ("Maintain Facilities", [
                "Vendor provides regular cleaning and servicing per contract.",
                "Safety Coordinator inspects facilities weekly and documents findings.",
            ]),
            ("Document Compliance", [
                "Maintain sanitation inspection log with dates, findings, and corrective actions.",
                "Report deficiencies immediately and confirm resolution.",
            ]),
        ],
        "appendix": [
            "Appendix \u2013 Templates & Checklists",
            "",
            "\u2022 Sanitary Facilities Setup Checklist",
            "\u2022 Inspection Log Template",
            "",
            "Appendix \u2013 References & Training Materials",
            "",
            "Training Materials (Foreman Training Binder):",
            "\u2022 Tab 4: Staging & Job Familiarization",
            "\u2022 Tab 22: Document Management",
            "",
            "Job Descriptions (Policy Manual Section 7):",
            "\u2022 7.2.4 Foreman",
            "\u2022 7.2.6 Project Safety Coordinator",
            "\u2022 7.3.1 Operations Management",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.3 Field Leadership",
            "",
            "Reference Documents:",
            "\u2022 OSHA Sanitation Standards (29 CFR 1926.51)",
        ],
    },

    # ----------------------------------------------------------------
    # 9.3.070 – Setup Temporary Lighting
    # ----------------------------------------------------------------
    "9.3.070": {
        "title": "Setup Temporary Lighting",
        "department": "Project Management / Safety",
        "purpose": (
            "To provide adequate temporary lighting for safety, security, and "
            "productivity during construction."
        ),
        "scope": (
            "This SOP applies to Project Managers, Field Supervisors, and Safety "
            "Coordinators during mobilization and project execution."
        ),
        "roles": [
            ("Project Manager",
             "Approves lighting plan and coordinates budget for fixtures and power."),
            ("Field Supervisor",
             "Oversees installation and verifies coverage across all work areas."),
            ("Electrical Subcontractor",
             "Installs temporary lighting systems per the approved plan."),
            ("Safety Coordinator",
             "Inspects lighting for OSHA compliance and safety."),
        ],
        "requirements": [
            "Site logistics plan",
            "Temporary lighting layout",
            "Temporary power connection plan (9.3.040 \u2013 Setup Temporary Power)",
            "OSHA lighting standards",
        ],
        "procedure": [
            ("Assess Lighting Needs", [
                "Identify required light levels for work areas, walkways, and security zones.",
                "Determine fixture types, quantities, and power requirements.",
            ]),
            ("Install Fixtures", [
                "Connect lighting to temporary power sources (9.3.040 \u2013 Setup Temporary Power).",
                "Mount fixtures securely to poles, scaffolding, or structures.",
            ]),
            ("Test Coverage", [
                "Verify adequate illumination in all designated areas.",
                "Adjust placement as needed to eliminate dark zones.",
            ]),
            ("Safety Review", [
                "Confirm compliance with OSHA minimum light level standards.",
                "Ensure cords are secured, protected, and do not create trip hazards.",
            ]),
            ("Maintain System", [
                "Replace failed bulbs and fixtures promptly.",
                "Conduct weekly inspections and document findings.",
            ]),
        ],
        "appendix": [
            "Appendix \u2013 Templates & Checklists",
            "",
            "\u2022 Temporary Lighting Layout Example",
            "\u2022 Inspection Log Template",
            "",
            "Appendix \u2013 References & Training Materials",
            "",
            "Training Materials (Foreman Training Binder):",
            "\u2022 Tab 4: Staging & Job Familiarization",
            "\u2022 Tab 22: Document Management",
            "",
            "Job Descriptions (Policy Manual Section 7):",
            "\u2022 7.2.4 Foreman",
            "\u2022 7.2.6 Project Safety Coordinator",
            "\u2022 7.3.1 Operations Management",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.3 Field Leadership",
            "",
            "Reference Documents:",
            "\u2022 OSHA Lighting Standards",
        ],
    },

    # ----------------------------------------------------------------
    # 9.3.080 – Setup Signage
    # ----------------------------------------------------------------
    "9.3.080": {
        "title": "Setup Signage",
        "department": "Project Management / Safety",
        "purpose": (
            "To install signage that provides safety information, site identification, "
            "and directional guidance for workers, visitors, and the public."
        ),
        "scope": (
            "This SOP applies to Project Managers, Field Supervisors, and Safety "
            "Coordinators during mobilization."
        ),
        "roles": [
            ("Project Manager",
             "Determines signage requirements and coordinates vendor procurement."),
            ("Field Supervisor",
             "Installs signage in designated locations per the site logistics plan."),
            ("Safety Coordinator",
             "Ensures signs meet OSHA and client requirements."),
        ],
        "requirements": [
            "Site logistics plan",
            "Safety and hazard communication plan",
            "Signage package (safety, directional, informational)",
            "OSHA signage standards",
        ],
        "procedure": [
            ("Identify Requirements", [
                "Review OSHA requirements and project-specific signage needs.",
                "Include safety, hazard, PPE, traffic, and directional signage.",
            ]),
            ("Procure Signage", [
                "Order standardized signage per GSL and client requirements.",
                "Confirm delivery timeline aligns with mobilization schedule.",
            ]),
            ("Install Signs", [
                "Place at entrances, work areas, and hazard zones.",
                "Ensure visibility and durability (weather-resistant mounting).",
            ]),
            ("Verify Compliance", [
                "Safety Coordinator inspects signage placement for OSHA compliance.",
                "Replace or repair damaged signs immediately (within 24 hours).",
            ]),
        ],
        "appendix": [
            "Appendix \u2013 Templates & Checklists",
            "",
            "\u2022 Sample Site Signage Package",
            "\u2022 Installation Checklist Template",
            "",
            "Appendix \u2013 References & Training Materials",
            "",
            "Training Materials (Foreman Training Binder):",
            "\u2022 Tab 4: Staging & Job Familiarization",
            "\u2022 Tab 22: Document Management",
            "",
            "Job Descriptions (Policy Manual Section 7):",
            "\u2022 7.2.4 Foreman",
            "\u2022 7.2.6 Project Safety Coordinator",
            "\u2022 7.3.1 Operations Management",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.3 Field Leadership",
            "",
            "Reference Documents:",
            "\u2022 OSHA Signage Standards",
        ],
    },

    # ----------------------------------------------------------------
    # 9.3.090 – Setup Security
    # ----------------------------------------------------------------
    "9.3.090": {
        "title": "Setup Security",
        "department": "Project Management / Safety",
        "purpose": (
            "To establish security measures that protect personnel, equipment, and "
            "materials from theft, vandalism, and unauthorized access."
        ),
        "scope": (
            "This SOP applies to Project Managers, Field Supervisors, and Safety "
            "Coordinators during mobilization and throughout construction."
        ),
        "roles": [
            ("Project Manager",
             "Approves the security plan and contracts vendors if required."),
            ("Field Supervisor",
             "Implements physical security measures and monitors access points."),
            ("Safety Coordinator",
             "Ensures the security plan does not conflict with safety standards."),
            ("Security Personnel (if engaged)",
             "Monitors site and enforces access protocols."),
        ],
        "requirements": [
            "Site security plan",
            "Access control plan",
            "Fencing and signage layouts (9.3.030 \u2013 Setup Site Fencing and Access Control)",
            "Security vendor contract (if applicable)",
        ],
        "procedure": [
            ("Develop Security Plan", [
                "Identify risks (theft, vandalism, trespassing).",
                "Define required measures (guards, cameras, patrols, lighting).",
            ]),
            ("Implement Physical Security", [
                "Secure fencing and access gates (9.3.030 \u2013 Setup Site Fencing and Access Control).",
                "Install locks, lighting, and surveillance systems.",
            ]),
            ("Establish Access Protocols", [
                "Require badges or sign-in logs for all personnel and visitors.",
                "Train site staff on access procedures and enforce them consistently.",
            ]),
            ("Monitor and Adjust", [
                "Conduct daily inspections of access points.",
                "Adjust measures as site conditions and phases change.",
            ]),
            ("Document Security Activities", [
                "Maintain daily security logs and incident reports.",
                "File all security documentation per project filing standards.",
            ]),
        ],
        "appendix": [
            "Appendix \u2013 Templates & Checklists",
            "",
            "\u2022 Security Plan Template",
            "\u2022 Incident Report Template",
            "\u2022 Daily Security Log Example",
            "",
            "Appendix \u2013 References & Training Materials",
            "",
            "Training Materials (Foreman Training Binder):",
            "\u2022 Tab 4: Staging & Job Familiarization",
            "\u2022 Tab 22: Document Management",
            "",
            "Job Descriptions (Policy Manual Section 7):",
            "\u2022 7.2.4 Foreman",
            "\u2022 7.2.6 Project Safety Coordinator",
            "\u2022 7.3.1 Operations Management",
            "\u2022 7.4 Business Administration",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.3 Field Leadership",
        ],
    },

    # ----------------------------------------------------------------
    # 9.3.100 – Setup Laydown Area
    # ----------------------------------------------------------------
    "9.3.100": {
        "title": "Setup Laydown Area",
        "department": "Project Management / Field Operations",
        "purpose": (
            "To establish a designated laydown area for material storage and staging "
            "to support efficient project operations and site safety."
        ),
        "scope": (
            "This SOP applies to Project Managers and Field Supervisors during "
            "mobilization."
        ),
        "roles": [
            ("Project Manager",
             "Approves laydown area location per the site logistics plan."),
            ("Field Supervisor",
             "Sets up and manages the laydown area, including organization and access."),
            ("Safety Coordinator",
             "Reviews for compliance with safety standards and traffic flow."),
        ],
        "requirements": [
            "Site logistics plan",
            "Laydown area setup checklist",
            "Material handling plan (9.2.080 \u2013 Prepare Material Handling Plan)",
        ],
        "procedure": [
            ("Select Location", [
                "Identify flat, accessible ground close to work zones.",
                "Ensure crane/hoist access if required for heavy materials.",
            ]),
            ("Prepare Site", [
                "Clear debris and grade if necessary.",
                "Install ground protection for heavy loads.",
            ]),
            ("Organize Layout", [
                "Separate storage by material type.",
                "Mark access lanes for forklifts and deliveries.",
            ]),
            ("Secure Area", [
                "Fence or barrier the laydown area as required.",
                "Provide lighting if area will be used after hours.",
            ]),
            ("Safety Review", [
                "Confirm materials are stacked properly and comply with fire and hazardous material requirements.",
                "Conduct weekly inspections and document findings.",
            ]),
        ],
        "appendix": [
            "Appendix \u2013 Templates & Checklists",
            "",
            "\u2022 Laydown Area Layout Example",
            "\u2022 Inspection Checklist Template",
            "",
            "Appendix \u2013 References & Training Materials",
            "",
            "Training Materials (Foreman Training Binder):",
            "\u2022 Tab 4: Staging & Job Familiarization",
            "\u2022 Tab 22: Document Management",
            "",
            "Job Descriptions (Policy Manual Section 7):",
            "\u2022 7.2.4 Foreman",
            "\u2022 7.2.6 Project Safety Coordinator",
            "\u2022 7.3.1 Operations Management",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.3 Field Leadership",
        ],
    },

    # ----------------------------------------------------------------
    # 9.3.110 – Setup Equipment Staging
    # ----------------------------------------------------------------
    "9.3.110": {
        "title": "Setup Equipment Staging",
        "department": "Project Management / Field Operations",
        "purpose": (
            "To establish designated areas for equipment staging, ensuring safe and "
            "efficient deployment of construction equipment."
        ),
        "scope": (
            "This SOP applies to Project Managers, Field Supervisors, and Equipment "
            "Operators during mobilization."
        ),
        "roles": [
            ("Project Manager",
             "Approves staging area location based on site logistics."),
            ("Field Supervisor",
             "Directs setup and coordinates equipment deliveries."),
            ("Equipment Operators",
             "Position equipment safely in the staging area."),
            ("Safety Coordinator",
             "Ensures OSHA compliance for equipment storage and staging."),
        ],
        "requirements": [
            "Site logistics plan",
            "Equipment delivery schedule",
            "Material handling plan (9.2.080 \u2013 Prepare Material Handling Plan)",
        ],
        "procedure": [
            ("Select Staging Location", [
                "Identify an accessible area that avoids disrupting traffic flow and active work zones.",
                "Confirm proximity to deployment areas.",
            ]),
            ("Prepare Area", [
                "Clear ground and provide mats if needed for soft conditions.",
                "Mark parking and maneuvering zones.",
            ]),
            ("Position Equipment", [
                "Organize equipment by size and type.",
                "Ensure emergency access is maintained.",
            ]),
            ("Apply Safety Controls", [
                "Provide barriers near public access points.",
                "Apply lockout/tagout to idle equipment.",
                "Install signage for equipment staging zone.",
            ]),
            ("Document", [
                "Maintain log of staged equipment and inspections.",
                "Update site logistics plan to reflect staging layout.",
            ]),
        ],
        "appendix": [
            "Appendix \u2013 Templates & Checklists",
            "",
            "\u2022 Equipment Staging Log Template",
            "\u2022 Site Logistics Plan Example",
            "",
            "Appendix \u2013 References & Training Materials",
            "",
            "Training Materials (Foreman Training Binder):",
            "\u2022 Tab 4: Staging & Job Familiarization",
            "\u2022 Tab 22: Document Management",
            "",
            "Job Descriptions (Policy Manual Section 7):",
            "\u2022 7.2.4 Foreman",
            "\u2022 7.2.6 Project Safety Coordinator",
            "\u2022 7.3.1 Operations Management",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.3 Field Leadership",
        ],
    },

    # ----------------------------------------------------------------
    # 9.3.120 – Setup Parking
    # ----------------------------------------------------------------
    "9.3.120": {
        "title": "Setup Parking",
        "department": "Project Management / Safety",
        "purpose": (
            "To designate and manage parking areas for workers, visitors, and "
            "deliveries, ensuring safety and minimizing disruption to site operations."
        ),
        "scope": (
            "This SOP applies to Project Managers, Field Supervisors, and Safety "
            "Coordinators during mobilization."
        ),
        "roles": [
            ("Project Manager",
             "Approves parking plan per site logistics."),
            ("Field Supervisor",
             "Establishes parking areas and installs signage."),
            ("Safety Coordinator",
             "Ensures traffic flow and pedestrian safety compliance."),
        ],
        "requirements": [
            "Site logistics plan",
            "Parking layout plan",
            "Signage package",
            "Material handling plan (9.2.080 \u2013 Prepare Material Handling Plan)",
        ],
        "procedure": [
            ("Identify Parking Areas", [
                "Assign zones for employees, visitors, and deliveries.",
                "Include ADA-compliant parking spaces as required.",
            ]),
            ("Prepare and Mark Areas", [
                "Grade and mark spaces.",
                "Define driving lanes and pedestrian walkways.",
            ]),
            ("Install Signage", [
                "Provide clear directional and restriction signs.",
                "Designate visitor parking with visible markings.",
            ]),
            ("Safety and Security", [
                "Add barriers near active construction zones.",
                "Install lighting for parking areas used during night shifts.",
            ]),
            ("Maintain Parking", [
                "Inspect weekly, repair damage, and adjust layout as site conditions change.",
                "Update signage as phases and access points shift.",
            ]),
        ],
        "appendix": [
            "Appendix \u2013 Templates & Checklists",
            "",
            "\u2022 Parking Plan Template",
            "\u2022 Inspection Log Example",
            "",
            "Appendix \u2013 References & Training Materials",
            "",
            "Training Materials (Foreman Training Binder):",
            "\u2022 Tab 4: Staging & Job Familiarization",
            "\u2022 Tab 22: Document Management",
            "",
            "Job Descriptions (Policy Manual Section 7):",
            "\u2022 7.2.4 Foreman",
            "\u2022 7.2.6 Project Safety Coordinator",
            "\u2022 7.3.1 Operations Management",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.3 Field Leadership",
        ],
    },

    # ----------------------------------------------------------------
    # 9.3.470 – Develop Site-Specific Safety Plan
    # ----------------------------------------------------------------
    "9.3.470": {
        "title": "Develop Site-Specific Safety Plan",
        "department": "Safety / Project Management",
        "purpose": (
            "To prepare and implement a site-specific safety plan (SSSP) that identifies "
            "hazards, compliance requirements, and procedures to protect workers and "
            "the public."
        ),
        "scope": (
            "This SOP applies to Project Managers, Safety Coordinators, and Field "
            "Supervisors. All safety plan documentation must be filed per Document "
            "Filing Standards SOP (SOP # TBD per crosswalk)."
        ),
        "roles": [
            ("Safety Coordinator",
             "Drafts and maintains the site-specific safety plan."),
            ("Project Manager",
             "Reviews and approves the plan before mobilization."),
            ("Field Supervisor",
             "Implements the safety plan in daily field operations."),
            ("Branch Manager",
             "Audits the safety plan for compliance."),
        ],
        "requirements": [
            "Document Filing Standards SOP (SOP # TBD per crosswalk)",
            "Corporate safety manual",
            "OSHA 29 CFR 1926",
            "Site visit findings (9.2.070 \u2013 Conduct Site Visit)",
            "Project scope and contract documents",
        ],
        "procedure": [
            ("Review Project Scope and Site Conditions", [
                "Review contract documents, project scope, and site visit findings (9.2.070).",
                "Identify project-specific hazards and risk factors.",
            ]),
            ("Identify Hazards and Compliance Requirements", [
                "Conduct a comprehensive hazard assessment for the project site.",
                "Document applicable OSHA, state, and local regulatory requirements.",
            ]),
            ("Draft Site-Specific Safety Plan (SSSP)", [
                "Develop the SSSP using the corporate safety manual as a baseline.",
                "Include site-specific hazards, mitigation measures, emergency procedures, and PPE requirements.",
            ]),
            ("Review and Approve", [
                "PM and Branch Manager review the draft SSSP.",
                "Resolve comments and finalize the plan before mobilization.",
            ]),
            ("Distribute and Implement", [
                "Distribute the approved SSSP to all field personnel and subcontractors.",
                "File per Document Filing Standards SOP (SOP # TBD per crosswalk).",
                "Review and update the plan quarterly or when site conditions change.",
            ]),
        ],
        "appendix": [
            "Appendix \u2013 Templates & Checklists",
            "",
            "\u2022 Safety Plan Template",
            "\u2022 Hazard Assessment Checklist",
            "",
            "Appendix \u2013 References & Training Materials",
            "",
            "Training Materials (Foreman Training Binder):",
            "\u2022 Tab 4: Staging & Job Familiarization",
            "\u2022 Tab 22: Document Management",
            "",
            "Job Descriptions (Policy Manual Section 7):",
            "\u2022 7.2.4 Foreman",
            "\u2022 7.2.6 Project Safety Coordinator",
            "\u2022 7.3.1 Operations Management",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.3 Field Leadership",
            "",
            "Reference Documents:",
            "\u2022 GSL Project Manager Procedures \u2013 Safety Management",
            "\u2022 OSHA 29 CFR 1926",
        ],
    },

    # ----------------------------------------------------------------
    # 9.4.010 – Conduct Coordination Meetings
    # ----------------------------------------------------------------
    "9.4.010": {
        "title": "Conduct Coordination Meetings",
        "department": "Project Management / Field Operations",
        "purpose": (
            "To establish a standard process for conducting project coordination "
            "meetings to ensure alignment between all project stakeholders, resolve "
            "issues, and review progress."
        ),
        "scope": (
            "This SOP applies to Project Managers, Field Supervisors, Subcontractors, "
            "and Design Team representatives. All coordination meeting documentation "
            "must be filed per Document Filing Standards SOP (SOP # TBD per crosswalk)."
        ),
        "roles": [
            ("Project Manager",
             "Schedules and chairs coordination meetings. Sets the agenda and ensures "
             "action items are tracked to completion."),
            ("Field Supervisor",
             "Provides field updates and identifies coordination issues."),
            ("Subcontractors",
             "Share progress updates and upcoming needs."),
            ("Design Team / Consultants",
             "Provide design clarifications as required."),
            ("Site Administrator",
             "Records minutes, action items, and files records per Document Filing "
             "Standards SOP (SOP # TBD per crosswalk)."),
        ],
        "requirements": [
            "Document Filing Standards SOP (SOP # TBD per crosswalk)",
            "Coordination meeting agenda template",
            "Action item log",
            "Previous meeting minutes (for follow-up)",
        ],
        "procedure": [
            ("Schedule Meetings", [
                "Schedule coordination meetings weekly (or as required by project complexity).",
                "Distribute calendar invites to all required attendees.",
            ]),
            ("Prepare and Distribute Agenda", [
                "Prepare meeting agenda at least 24 hours in advance.",
                "Include standing items: safety, progress updates, upcoming activities, coordination issues, and action items.",
            ]),
            ("Conduct Meeting", [
                "Review safety topics and any open incidents.",
                "Discuss progress updates from all trades and disciplines.",
                "Review upcoming activities, coordination issues (site access, deliveries, manpower, conflicts).",
                "Assign and review action items with owners and due dates.",
            ]),
            ("Record and Distribute Minutes", [
                "Record attendance and meeting minutes.",
                "Distribute minutes to all attendees within 48 hours.",
            ]),
            ("Track Action Items and File Records", [
                "Update the action item log with new items and close completed items.",
                "File minutes and action item log per Document Filing Standards SOP (SOP # TBD per crosswalk).",
            ]),
        ],
        "appendix": [
            "Appendix \u2013 Templates & Checklists",
            "",
            "\u2022 Coordination Meeting Agenda Template",
            "\u2022 Action Item Log Example",
            "\u2022 Meeting Minutes Template",
            "",
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
            "\u2022 7.3.1 Operations Management",
            "",
            "Management Directives (Policy Manual Section 9):",
            "\u2022 9.5 Project Management",
            "\u2022 9.3 Field Leadership",
            "\u2022 9.4 General Superintendents",
        ],
    },
}


# ============================================================
# LEGACY NUMBER PATTERN
# ============================================================
LEGACY_PATTERN = re.compile(r"9\.41\.\d{3}[A-Z]?|SOP\s+190A|SOP\s+9\.41\.\d{3}[A-Z]?")


def build_doc(sop_id, sop_def, related_list):
    """Build a template-compliant .docx document."""
    doc = Document()

    style = doc.styles["Normal"]
    font = style.font
    font.name = "Calibri"
    font.size = Pt(11)

    # SOP Title
    p = doc.add_paragraph()
    run = p.add_run(f"SOP: {sop_id} \u2013 {sop_def['title']}")
    run.bold = True
    run.font.size = Pt(14)

    # Department
    doc.add_paragraph(f"Department: {sop_def['department']}")

    # Related SOPs
    p = doc.add_paragraph()
    run = p.add_run("Related SOPs:")
    run.bold = True
    for entry in related_list:
        doc.add_paragraph(f"\u2022 {entry}", style="List Bullet")

    doc.add_paragraph("")

    # Purpose
    p = doc.add_paragraph()
    run = p.add_run("Purpose")
    run.bold = True
    run.font.size = Pt(13)
    doc.add_paragraph(sop_def["purpose"])

    # Scope
    doc.add_paragraph("")
    p = doc.add_paragraph()
    run = p.add_run("Scope")
    run.bold = True
    run.font.size = Pt(13)
    doc.add_paragraph(sop_def["scope"])

    # Roles & Responsibilities
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

    # Requirements
    doc.add_paragraph("")
    p = doc.add_paragraph()
    run = p.add_run("Requirements")
    run.bold = True
    run.font.size = Pt(13)
    for req in sop_def["requirements"]:
        doc.add_paragraph(f"\u2022 {req}", style="List Bullet")

    # Procedure
    doc.add_paragraph("")
    p = doc.add_paragraph()
    run = p.add_run("Procedure")
    run.bold = True
    run.font.size = Pt(13)
    for step_num, (step_title, step_items) in enumerate(sop_def["procedure"], 1):
        doc.add_paragraph("")
        p = doc.add_paragraph()
        run = p.add_run(f"Step {step_num} \u2013 {step_title}")
        run.bold = True
        for item in step_items:
            doc.add_paragraph(f"\u2022 {item}", style="List Bullet")

    # Appendix
    doc.add_paragraph("")
    p = doc.add_paragraph()
    run = p.add_run("Appendix")
    run.bold = True
    run.font.size = Pt(13)
    for line in sop_def["appendix"]:
        doc.add_paragraph(line)

    return doc


def detect_legacy_numbers(text):
    """Find all legacy SOP numbers in the text."""
    found = set()
    for m in LEGACY_PATTERN.finditer(text):
        found.add(m.group())
    # Also check for the segment-reordered format
    for m in re.finditer(r"9\.\d{3}\.41", text):
        found.add(m.group())
    return found


def main():
    all_files = [f for f in os.listdir(SOP_DIR)
                 if f.endswith(".docx") and not f.startswith("~")]

    results = []

    for sop_id, sop_def in SOP_DEFS.items():
        print(f"\n{'='*70}")
        print(f"Processing: {sop_id} \u2013 {sop_def['title']}")
        print(f"{'='*70}")

        matches = [f for f in all_files if f.startswith(sop_id)]
        if not matches:
            print(f"  FILE NOT FOUND for {sop_id}")
            continue

        fname = matches[0]
        filepath = os.path.join(SOP_DIR, fname)

        # Read original
        orig_doc = Document(filepath)
        orig_text = "\n".join(p.text for p in orig_doc.paragraphs)
        for tbl in orig_doc.tables:
            for row in tbl.rows:
                for cell in row.cells:
                    orig_text += "\n" + cell.text

        # Detect legacy numbers
        legacy_found = detect_legacy_numbers(orig_text)

        # Build change summary
        changes = []

        title_line = orig_doc.paragraphs[0].text.strip() if orig_doc.paragraphs else ""
        expected = f"SOP: {sop_id} \u2013 {sop_def['title']}"
        if title_line != expected:
            changes.append(f"Title corrected: '{title_line[:55]}' -> '{expected}'")

        for p in orig_doc.paragraphs:
            if "Created by:" in p.text or "Version:" in p.text:
                changes.append("Front-matter metadata (Created by, Version, Effective Date) removed")
                break

        if any("DOCUMENT REFERENCES" in p.text for p in orig_doc.paragraphs):
            changes.append("DOCUMENT REFERENCES section removed from body; content moved to Appendix")

        if orig_doc.tables:
            changes.append(f"{len(orig_doc.tables)} tables converted to bullet lists")

        for sec in ["Deliverables", "Compliance & Review", "References"]:
            if any(p.text.strip() == sec for p in orig_doc.paragraphs):
                changes.append(f"Non-template section '{sec}' removed")

        if legacy_found:
            changes.append(f"Legacy numbers removed: {', '.join(sorted(legacy_found))}")

        # Check for 9.41.190A / 190A references
        has_190a = "190A" in orig_text or "9.41.190A" in orig_text
        if has_190a:
            changes.append("All '9.41.190A / SOP 190A' references replaced with 'Document Filing Standards SOP (SOP # TBD per crosswalk)'")

        # Check for 9.41.060 reference
        if "9.41.060" in orig_text:
            changes.append("'SOP 9.41.060' replaced with '9.2.080 \u2013 Prepare Material Handling Plan'")

        # Check for 9.41.100 reference
        if "9.41.100" in orig_text:
            changes.append("'SOP 9.41.100' replaced with '9.3.030 \u2013 Setup Site Fencing and Access Control'")

        # Check for 9.41.105 reference
        if "9.41.105" in orig_text:
            changes.append("'SOP 9.41.105' replaced with '9.3.040 \u2013 Setup Temporary Power'")

        changes.append("Section order enforced: SOP Title -> Department -> Related SOPs -> Purpose -> Scope -> Roles -> Requirements -> Procedure -> Appendix")
        changes.append("Procedure reformatted with numbered steps, bold titles, and bullet sub-steps")

        # Related SOPs status
        related_list = RELATED_SOPS.get(sop_id, [])
        tbd_titles = []
        if has_190a:
            tbd_titles.append("Document Filing Standards")

        # Build and save
        new_doc = build_doc(sop_id, sop_def, related_list)
        new_doc.save(filepath)

        # Print summary
        print(f"\nChange Summary:")
        for c in changes:
            print(f"  \u2022 {c}")

        has_legacy = bool(legacy_found)
        print(f"\nLegacy numbers removed: {'YES' if has_legacy else 'YES (none found in original)'}")
        if tbd_titles:
            print(f"Related SOPs updated: PARTIAL ({'; '.join(t + ' (SOP # TBD)' for t in tbd_titles)})")
        else:
            print(f"Related SOPs updated: YES")

        print(f"\nSAVED: {fname}")

        results.append({
            "id": sop_id,
            "title": sop_def["title"],
            "legacy_found": sorted(legacy_found),
            "tbd": tbd_titles,
            "changes": len(changes),
        })

    # Final summary
    print(f"\n{'='*70}")
    print(f"BATCH COMPLETE: {len(results)} / {len(SOP_DEFS)} SOPs processed")
    print(f"{'='*70}")
    for r in results:
        legacy_str = ", ".join(r["legacy_found"]) if r["legacy_found"] else "(none)"
        tbd_str = ", ".join(r["tbd"]) if r["tbd"] else "(none)"
        print(f"  {r['id']}: {r['changes']} changes | Legacy: {legacy_str} | TBD: {tbd_str}")


if __name__ == "__main__":
    main()
