import pandas as pd
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

output_dir = 'C:/Users/tewing/Desktop/Claude Projects/Project Outputs'

# Read the existing SCORM catalog for training courses
scorm_df = pd.read_excel('C:/Users/tewing/Desktop/Claude Projects/SOPs For Review/SCORM_Complete_Course_Catalog.xlsx')

# ============================================
# SOP TO TRAINING CROSS-REFERENCE MATRIX
# ============================================

sop_training_mapping = [
    # Pre-Construction SOPs (9.2.xxx)
    {"SOP Number": "9.2.005", "SOP Title": "Review Contract for High-Risk Clauses",
     "Related Training": "Introduction to Project Planning and Execution; Chapter 3 Introduction to Project Planning and Execution",
     "Training Tab": "Tab 2 - Preplanning", "Skill Level Set": "Project Planning & Productivity"},
    {"SOP Number": "9.2.010", "SOP Title": "Team Selection",
     "Related Training": "Project Structure, Delegation, and Team Development; Chapter 4 Building an Effective Team",
     "Training Tab": "Tab 51 - Leadership", "Skill Level Set": "Leadership & Field Management"},
    {"SOP Number": "9.2.015", "SOP Title": "Project Turnover Meeting",
     "Related Training": "Introduction to Field Leadership Section 1; Chapter 0 Introduction to Critical Leadership Training",
     "Training Tab": "Tab 51 - Leadership", "Skill Level Set": "Leadership & Field Management"},
    {"SOP Number": "9.2.040", "SOP Title": "PM Reviews Plans Specs and Schedule",
     "Related Training": "Introduction to Project Planning and Execution; Job Plan Theory",
     "Training Tab": "Tab 7 - Job Plans", "Skill Level Set": "Project Planning & Productivity"},
    {"SOP Number": "9.2.050", "SOP Title": "FS Reviews Plans Specs and Schedule",
     "Related Training": "Job Plan Theory; Chapter 1 Job Plan Theory; Evaluating the Job Plan",
     "Training Tab": "Tab 7 - Job Plans", "Skill Level Set": "Project Planning & Productivity"},
    {"SOP Number": "9.2.055", "SOP Title": "Compare Est vs Planned",
     "Related Training": "Chapter 10 Avoiding Common Time Wasters; Jobsite Efficiency",
     "Training Tab": "Tab 7 - Job Plans", "Skill Level Set": "Project Planning & Productivity"},
    {"SOP Number": "9.2.057", "SOP Title": "Identify VE and Prefabrication Opportunities",
     "Related Training": "Lean Fundamentals; Eight Wastes of Construction; What is Lean",
     "Training Tab": "Tab 56 - Lean Training", "Skill Level Set": "Lean Construction"},
    {"SOP Number": "9.2.060", "SOP Title": "Create Issue List and Begin RFI Process",
     "Related Training": "Introduction to Documentation and Reporting; Document Management",
     "Training Tab": "Tab 22 - Document Management", "Skill Level Set": "Documentation & Compliance"},
    {"SOP Number": "9.2.070", "SOP Title": "Conduct Site Visit",
     "Related Training": "Introduction to Safety Management; Workplace Inspections Pre-Task Assessments",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},
    {"SOP Number": "9.2.080", "SOP Title": "Prepare Material Handling Plan",
     "Related Training": "Material Management (TAB 41 content needed)",
     "Training Tab": "Tab 41 - Material Management", "Skill Level Set": "Project Planning & Productivity"},
    {"SOP Number": "9.2.090", "SOP Title": "Develop Labor Budget",
     "Related Training": "Manpower Projection; Creating Budgets (TAB 17 content needed)",
     "Training Tab": "Tab 19 - Manpower", "Skill Level Set": "Project Planning & Productivity"},
    {"SOP Number": "9.2.100", "SOP Title": "Prepare Layout and Sequencing Plan",
     "Related Training": "Job Plan Theory; Introduction to Project Planning and Execution",
     "Training Tab": "Tab 7 - Job Plans", "Skill Level Set": "Project Planning & Productivity"},
    {"SOP Number": "9.2.110", "SOP Title": "Develop Project Schedule",
     "Related Training": "Scheduling (TAB 6 content)",
     "Training Tab": "Tab 6 - Scheduling", "Skill Level Set": "Project Planning & Productivity"},
    {"SOP Number": "9.2.120", "SOP Title": "Establish Tracking and Control Systems",
     "Related Training": "Introduction to Documentation and Reporting; ProCore Fundamentals",
     "Training Tab": "Tab 57 - ProCore", "Skill Level Set": "Construction Software"},
    {"SOP Number": "9.2.130", "SOP Title": "Construction Execution Kickoff Meeting",
     "Related Training": "Introduction to Field Leadership; Leadership Essentials",
     "Training Tab": "Tab 51 - Leadership", "Skill Level Set": "Leadership & Field Management"},
    {"SOP Number": "9.2.140", "SOP Title": "Develop Project Budget",
     "Related Training": "Creating Budgets (TAB 17 content needed); Job Cost Projections",
     "Training Tab": "Tab 17 - Creating Budgets", "Skill Level Set": "Project Planning & Productivity"},
    {"SOP Number": "9.2.160", "SOP Title": "Develop Procurement Plan",
     "Related Training": "Purchasing Buyout (TAB 5 content)",
     "Training Tab": "Tab 5 - Purchasing", "Skill Level Set": "Project Planning & Productivity"},

    # Site Setup SOPs (9.3.xxx)
    {"SOP Number": "9.3.010", "SOP Title": "Setup Office Trailer",
     "Related Training": "Staging & Job Familiarization (TAB 4 content)",
     "Training Tab": "Tab 4 - Staging", "Skill Level Set": "Project Planning & Productivity"},
    {"SOP Number": "9.3.020", "SOP Title": "Setup Storage Trailer",
     "Related Training": "Material Management (TAB 41 content); Tool Control",
     "Training Tab": "Tab 1 - Tool Control", "Skill Level Set": "Leadership & Field Management"},
    {"SOP Number": "9.3.040", "SOP Title": "Setup Temporary Power",
     "Related Training": "NFPA 70E; Electrical Safety; Arc Flash PPE",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},
    {"SOP Number": "9.3.470", "SOP Title": "Develop Site-Specific Safety Plan",
     "Related Training": "Safety Coordinator training; Introduction to Safety Management; OSHA Focus Four",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},

    # Safety SOPs
    {"SOP Number": "9.41.470", "SOP Title": "Develop Site-Specific Safety Plan",
     "Related Training": "Safety Coordinator 1-11; Introduction to Safety Management; OSHA Focus Four Workplace Hazards",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},
    {"SOP Number": "9.41.475", "SOP Title": "Conduct Safety Orientation",
     "Related Training": "New Hire Safety Orientation; A Commitment to Zero Broken Lives",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},
    {"SOP Number": "9.41.480", "SOP Title": "Conduct Safety Inspections",
     "Related Training": "Safety Coordinator 7.0 Safety Inspections; Workplace Inspections Pre-Task Assessments",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},
    {"SOP Number": "9.41.485", "SOP Title": "Conduct Safety Meetings",
     "Related Training": "Safety Coordinator 5.0 Safety Meetings; Introduction to Safety Management",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},
    {"SOP Number": "9.41.490", "SOP Title": "Report Safety Incidents",
     "Related Training": "Safety Coordinator 9.0 Accident Incident Investigations",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},
    {"SOP Number": "9.41.495", "SOP Title": "Investigate Accidents",
     "Related Training": "Safety Coordinator 9.0 Accident Incident Investigations; Safety Coordinator 10.0 Injury Case Management",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},
    {"SOP Number": "9.41.500", "SOP Title": "Conduct Emergency Preparedness",
     "Related Training": "Emergency Response training; New Hire Safety Orientation",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},
    {"SOP Number": "9.41.510", "SOP Title": "Provide Safety Training",
     "Related Training": "Safety Coordinator 4.0 Task Training; All Safety training modules",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},

    # Electrical Safety specific
    {"SOP Number": "LOTO", "SOP Title": "Lockout Tagout Procedures",
     "Related Training": "Lockout Tagout Procedures; Simple LOTO; Complex LOTO; Abnormal Lockout Removal",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},
    {"SOP Number": "ARC-FLASH", "SOP Title": "Arc Flash Safety",
     "Related Training": "Arc Flash PPE; 2024 NFPA 70E Required Boundaries; Safe Electrical Work Practices",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},
    {"SOP Number": "FALL-PROTECTION", "SOP Title": "Fall Protection",
     "Related Training": "Fall Protection in Industrial and Construction Environments; Using Portable and Fixed Ladders",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},
    {"SOP Number": "SCAFFOLDING", "SOP Title": "Scaffolding Safety",
     "Related Training": "Supported Scaffolding Safety; Safely Accessing a Scaffold; Working Safely on Scaffolding",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},
    {"SOP Number": "HAZCOM", "SOP Title": "Hazard Communication",
     "Related Training": "Hazard Communication; Safety Data Sheets; Types of Chemical Hazards; Written Hazard Communication Plan",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},
    {"SOP Number": "CONFINED-SPACE", "SOP Title": "Confined Space Entry",
     "Related Training": "Permit Required Confined Spaces",
     "Training Tab": "Tab 40 - Safety", "Skill Level Set": "Safety"},

    # Leadership & Management SOPs
    {"SOP Number": "9.41.675", "SOP Title": "Conduct Daily Huddles",
     "Related Training": "Techniques for Better Communication; Effective Communication; Leadership Essentials",
     "Training Tab": "Tab 51 - Leadership", "Skill Level Set": "Leadership & Field Management"},
    {"SOP Number": "9.41.680", "SOP Title": "Conduct Weekly Foreman Meetings",
     "Related Training": "Leadership Essentials; Team Management; Building and Maintaining Team Morale",
     "Training Tab": "Tab 51 - Leadership", "Skill Level Set": "Leadership & Field Management"},
    {"SOP Number": "9.41.560", "SOP Title": "Manage Manpower Allocation",
     "Related Training": "Manpower Projection; On-Site Productivity",
     "Training Tab": "Tab 19 - Manpower", "Skill Level Set": "Project Planning & Productivity"},
    {"SOP Number": "9.41.720", "SOP Title": "Conduct Productivity Analysis",
     "Related Training": "On-Site Productivity; Productivity Improvement; Lean Construction",
     "Training Tab": "Tab 56 - Lean Training", "Skill Level Set": "Lean Construction"},

    # Performance Management SOPs
    {"SOP Number": "PERF-REVIEW", "SOP Title": "Conducting Performance Reviews",
     "Related Training": "Conducting Effective Performance Reviews; Corrective Counseling and Performance Reviews",
     "Training Tab": "Tab 52 - Performance Reviews", "Skill Level Set": "Performance Management"},

    # Document Management SOPs
    {"SOP Number": "9.41.190A", "SOP Title": "Document Filing Standards",
     "Related Training": "Introduction to Documentation and Reporting; Document Management",
     "Training Tab": "Tab 22 - Document Management", "Skill Level Set": "Documentation & Compliance"},
    {"SOP Number": "9.41.195", "SOP Title": "Manage Project Documentation System",
     "Related Training": "ProCore Fundamentals; Document Management",
     "Training Tab": "Tab 57 - ProCore", "Skill Level Set": "Construction Software"},
    {"SOP Number": "9.41.200", "SOP Title": "Manage Submittals",
     "Related Training": "Submittals (TAB 9 content needed)",
     "Training Tab": "Tab 9 - Submittals", "Skill Level Set": "Documentation & Compliance"},
    {"SOP Number": "9.41.215", "SOP Title": "Manage Daily Reports",
     "Related Training": "Daily Reports (TAB 14 content needed); Introduction to Documentation",
     "Training Tab": "Tab 14 - Daily Reports", "Skill Level Set": "Documentation & Compliance"},

    # Change Order SOPs
    {"SOP Number": "9.41.360", "SOP Title": "Manage Change Orders",
     "Related Training": "Approving Change Orders in ViewPoint; Creating Pending Change Orders in ViewPoint",
     "Training Tab": "Tab 8 - Change Orders", "Skill Level Set": "Construction Software"},

    # Subcontractor Management
    {"SOP Number": "9.41.575", "SOP Title": "Manage Subcontractor Resources",
     "Related Training": "Managing Sub-Contractors",
     "Training Tab": "Tab 50 - Managing Subcontractors", "Skill Level Set": "Leadership & Field Management"},

    # Software Training
    {"SOP Number": "ACCUBID", "SOP Title": "Accubid Estimating Software",
     "Related Training": "Learning Accubid Pro; Advanced Trimble Accubid Classic Pro",
     "Training Tab": "Tab 11 - Estimating", "Skill Level Set": "Construction Software"},
    {"SOP Number": "VIEWPOINT", "SOP Title": "ViewPoint Software",
     "Related Training": "Approving Change Orders in ViewPoint; Creating Pending Change Orders in ViewPoint",
     "Training Tab": "Tab 8 - Change Orders", "Skill Level Set": "Construction Software"},
    {"SOP Number": "PROCORE", "SOP Title": "ProCore Project Management",
     "Related Training": "ProCore Fundamentals (TAB 57 content)",
     "Training Tab": "Tab 57 - ProCore", "Skill Level Set": "Construction Software"},

    # Lean Construction
    {"SOP Number": "LEAN", "SOP Title": "Lean Construction Practices",
     "Related Training": "What is Lean; Eight Wastes of Construction; Lean Fundamentals; Pull Planning; Continuous Improvement",
     "Training Tab": "Tab 56 - Lean Training", "Skill Level Set": "Lean Construction"},

    # Closeout SOPs (9.6.xxx)
    {"SOP Number": "9.6.005", "SOP Title": "Prepare for Turnover Field Perspective",
     "Related Training": "Job Closeout (TAB 18 content)",
     "Training Tab": "Tab 18 - Job Close Out", "Skill Level Set": "Project Planning & Productivity"},
    {"SOP Number": "9.6.010", "SOP Title": "Conduct Closeout Meetings",
     "Related Training": "Job Closeout; Introduction to Field Leadership",
     "Training Tab": "Tab 18 - Job Close Out", "Skill Level Set": "Leadership & Field Management"},
    {"SOP Number": "9.6.020", "SOP Title": "Manage Punch Lists",
     "Related Training": "Quality Control; Job Closeout",
     "Training Tab": "Tab 18 - Job Close Out", "Skill Level Set": "Documentation & Compliance"},
    {"SOP Number": "9.6.030", "SOP Title": "Manage As-Built Drawings",
     "Related Training": "Document Management; Introduction to Documentation",
     "Training Tab": "Tab 22 - Document Management", "Skill Level Set": "Documentation & Compliance"},
    {"SOP Number": "9.6.070", "SOP Title": "Conduct Post-Project Review",
     "Related Training": "Continuous Improvement; Leadership Essentials",
     "Training Tab": "Tab 51 - Leadership", "Skill Level Set": "Leadership & Field Management"},
    {"SOP Number": "9.6.085", "SOP Title": "Document Lessons Learned",
     "Related Training": "Continuous Improvement; Introduction to Documentation",
     "Training Tab": "Tab 22 - Document Management", "Skill Level Set": "Lean Construction"},
]

# Create SOP-Training Cross-Reference DataFrame
sop_training_df = pd.DataFrame(sop_training_mapping)

# ============================================
# SOP TO JOB DESCRIPTION CROSS-REFERENCE
# ============================================

sop_job_mapping = [
    # Pre-Construction SOPs
    {"SOP Number": "9.2.005", "SOP Title": "Review Contract for High-Risk Clauses",
     "Primary Role": "Project Manager", "Supporting Roles": "Contract Manager; Branch Manager",
     "Job Description Ref": "7.3.1; 7.5"},
    {"SOP Number": "9.2.010", "SOP Title": "Team Selection",
     "Primary Role": "Project Manager", "Supporting Roles": "General Superintendent; Branch Manager",
     "Job Description Ref": "7.3.1; 7.2.5"},
    {"SOP Number": "9.2.015", "SOP Title": "Project Turnover Meeting",
     "Primary Role": "Project Manager", "Supporting Roles": "Field Supervisor; Estimator",
     "Job Description Ref": "7.3.1; 7.2.4; 7.3.3"},
    {"SOP Number": "9.2.040", "SOP Title": "PM Reviews Plans Specs and Schedule",
     "Primary Role": "Project Manager", "Supporting Roles": "Estimator",
     "Job Description Ref": "7.3.1; 7.3.3"},
    {"SOP Number": "9.2.050", "SOP Title": "FS Reviews Plans Specs and Schedule",
     "Primary Role": "Field Supervisor (Foreman)", "Supporting Roles": "Project Manager",
     "Job Description Ref": "7.2.4; 7.2.5"},
    {"SOP Number": "9.2.055", "SOP Title": "Compare Est vs Planned",
     "Primary Role": "Project Manager", "Supporting Roles": "Field Supervisor; Estimator",
     "Job Description Ref": "7.3.1; 7.2.4; 7.3.3"},
    {"SOP Number": "9.2.057", "SOP Title": "Identify VE and Prefabrication Opportunities",
     "Primary Role": "Project Manager", "Supporting Roles": "Estimator; Pre-Fab Manager",
     "Job Description Ref": "7.3.1; 7.3.3; 7.3.7"},
    {"SOP Number": "9.2.060", "SOP Title": "Create Issue List and Begin RFI Process",
     "Primary Role": "Project Manager", "Supporting Roles": "Field Supervisor",
     "Job Description Ref": "7.3.1; 7.2.4"},
    {"SOP Number": "9.2.070", "SOP Title": "Conduct Site Visit",
     "Primary Role": "Project Manager", "Supporting Roles": "Field Supervisor; Safety Coordinator",
     "Job Description Ref": "7.3.1; 7.2.4; 7.2.6"},
    {"SOP Number": "9.2.080", "SOP Title": "Prepare Material Handling Plan",
     "Primary Role": "Project Manager", "Supporting Roles": "Field Supervisor; Purchasing",
     "Job Description Ref": "7.3.1; 7.2.4; 7.4.4"},
    {"SOP Number": "9.2.090", "SOP Title": "Develop Labor Budget",
     "Primary Role": "Project Manager", "Supporting Roles": "General Superintendent; Estimator",
     "Job Description Ref": "7.3.1; 7.2.5; 7.3.3"},
    {"SOP Number": "9.2.100", "SOP Title": "Prepare Layout and Sequencing Plan",
     "Primary Role": "Project Manager", "Supporting Roles": "Field Supervisor",
     "Job Description Ref": "7.3.1; 7.2.4; 7.2.5"},
    {"SOP Number": "9.2.110", "SOP Title": "Develop Project Schedule",
     "Primary Role": "Project Manager", "Supporting Roles": "Field Supervisor",
     "Job Description Ref": "7.3.1; 7.2.4; 7.2.5"},
    {"SOP Number": "9.2.120", "SOP Title": "Establish Tracking and Control Systems",
     "Primary Role": "Project Manager", "Supporting Roles": "Admin Support",
     "Job Description Ref": "7.3.1; 7.4.5"},
    {"SOP Number": "9.2.130", "SOP Title": "Construction Execution Kickoff Meeting",
     "Primary Role": "Project Manager", "Supporting Roles": "Field Supervisor; All Team",
     "Job Description Ref": "7.3.1; 7.2.4; 7.2.5"},
    {"SOP Number": "9.2.140", "SOP Title": "Develop Project Budget",
     "Primary Role": "Project Manager", "Supporting Roles": "Estimator; Branch Manager",
     "Job Description Ref": "7.3.1; 7.3.3"},
    {"SOP Number": "9.2.160", "SOP Title": "Develop Procurement Plan",
     "Primary Role": "Project Manager", "Supporting Roles": "Purchasing Manager",
     "Job Description Ref": "7.3.1; 7.4.4"},

    # Site Setup SOPs
    {"SOP Number": "9.3.010-120", "SOP Title": "Site Setup SOPs (Office, Storage, Power, etc.)",
     "Primary Role": "Foreman", "Supporting Roles": "Project Superintendent; Project Manager",
     "Job Description Ref": "7.2.4; 7.2.5; 7.3.1"},
    {"SOP Number": "9.3.470", "SOP Title": "Develop Site-Specific Safety Plan",
     "Primary Role": "Safety Coordinator", "Supporting Roles": "Project Manager; Foreman",
     "Job Description Ref": "7.2.6; 7.4.6; 7.2.4"},

    # Field Operations SOPs
    {"SOP Number": "9.41.470-510", "SOP Title": "Safety Management SOPs",
     "Primary Role": "Safety Coordinator", "Supporting Roles": "Foreman; All Field",
     "Job Description Ref": "7.2.6; 7.4.6; 7.2.4"},
    {"SOP Number": "9.41.515-555", "SOP Title": "Quality Management SOPs",
     "Primary Role": "Foreman", "Supporting Roles": "Project Superintendent; Project Manager",
     "Job Description Ref": "7.2.4; 7.2.5; 7.3.1"},
    {"SOP Number": "9.41.560-595", "SOP Title": "Resource Management SOPs",
     "Primary Role": "Project Manager", "Supporting Roles": "General Superintendent; Foreman",
     "Job Description Ref": "7.3.1; 7.2.5; 7.2.4"},
    {"SOP Number": "9.41.600-670", "SOP Title": "Procurement SOPs",
     "Primary Role": "Project Manager", "Supporting Roles": "Purchasing Manager; Foreman",
     "Job Description Ref": "7.3.1; 7.4.4; 7.2.4"},
    {"SOP Number": "9.41.675-725", "SOP Title": "Field Operations SOPs",
     "Primary Role": "Foreman", "Supporting Roles": "Project Superintendent; Project Manager",
     "Job Description Ref": "7.2.4; 7.2.5; 7.3.1"},

    # Closeout SOPs
    {"SOP Number": "9.6.005-085", "SOP Title": "Project Closeout SOPs",
     "Primary Role": "Project Manager", "Supporting Roles": "Foreman; Admin Support",
     "Job Description Ref": "7.3.1; 7.2.4; 7.4.5"},
]

sop_job_df = pd.DataFrame(sop_job_mapping)

# ============================================
# SOP TO MANAGEMENT DIRECTIVE CROSS-REFERENCE
# ============================================

sop_md_mapping = [
    # Pre-Construction aligned with MD 9.5, 9.7
    {"SOP Number": "9.2.005", "SOP Title": "Review Contract for High-Risk Clauses",
     "Management Directive": "MD 9.5; MD 9.7",
     "MD Section": "Contract Review - Scope (9.5); Post-Contract Award (9.7)",
     "Alignment Notes": "Aligns with PM contract review requirements and Estimating scope verification"},
    {"SOP Number": "9.2.010", "SOP Title": "Team Selection",
     "Management Directive": "MD 9.4; MD 9.5",
     "MD Section": "Work Force Development (9.4); Field Leadership & Manpower (9.5)",
     "Alignment Notes": "Aligns with Gen Supt workforce development and PM staffing responsibilities"},
    {"SOP Number": "9.2.015", "SOP Title": "Project Turnover Meeting",
     "Management Directive": "MD 9.5; MD 9.7",
     "MD Section": "Project Pre-Planning (9.5); Project Turnover Meeting (9.7)",
     "Alignment Notes": "Required by both PM and Estimating directives for project handoff"},
    {"SOP Number": "9.2.040-055", "SOP Title": "Plans/Specs Review SOPs",
     "Management Directive": "MD 9.3; MD 9.5",
     "MD Section": "Pre-Planning (9.3); Job Plans (9.5)",
     "Alignment Notes": "Aligns with Field Leadership pre-planning and PM job monitoring"},
    {"SOP Number": "9.2.057", "SOP Title": "Identify VE and Prefabrication",
     "Management Directive": "MD 9.5; MD 9.7",
     "MD Section": "Prefabrication (9.5); Value Engineering Alternates (9.7)",
     "Alignment Notes": "Aligns with PM prefab requirements and Estimating VE directives"},
    {"SOP Number": "9.2.060", "SOP Title": "Create Issue List/RFI Process",
     "Management Directive": "MD 9.5; MD 9.7",
     "MD Section": "Document Control (9.5); RFI Process (9.7)",
     "Alignment Notes": "Aligns with PM document control and Estimating RFI requirements"},
    {"SOP Number": "9.2.070", "SOP Title": "Conduct Site Visit",
     "Management Directive": "MD 9.5",
     "MD Section": "Job Site Visits (9.5)",
     "Alignment Notes": "Aligns with PM job site visit requirements (minimum twice per month)"},
    {"SOP Number": "9.2.080", "SOP Title": "Material Handling Plan",
     "Management Directive": "MD 9.5",
     "MD Section": "Submittals & Purchasing (9.5)",
     "Alignment Notes": "Aligns with PM coordination with Purchasing Department"},
    {"SOP Number": "9.2.090", "SOP Title": "Develop Labor Budget",
     "Management Directive": "MD 9.4; MD 9.5",
     "MD Section": "Manpower Projections (9.4); Job Plans (9.5)",
     "Alignment Notes": "Aligns with Gen Supt workforce planning and PM labor tracking"},
    {"SOP Number": "9.2.100-110", "SOP Title": "Layout/Sequencing/Schedule SOPs",
     "Management Directive": "MD 9.5",
     "MD Section": "Scheduling (9.5)",
     "Alignment Notes": "Aligns with PM scheduling directives including pull planning"},
    {"SOP Number": "9.2.120", "SOP Title": "Establish Tracking Systems",
     "Management Directive": "MD 9.5",
     "MD Section": "Job Plans; Document Control (9.5)",
     "Alignment Notes": "Aligns with PM tracking and job plan requirements"},
    {"SOP Number": "9.2.130", "SOP Title": "Construction Kickoff Meeting",
     "Management Directive": "MD 9.5; MD 9.7",
     "MD Section": "Project Pre-Planning (9.5); Project Turnover Meeting (9.7)",
     "Alignment Notes": "Transition point from planning to execution per PM and Estimating directives"},

    # Field Operations aligned with MD 9.2, 9.3
    {"SOP Number": "9.3.xxx", "SOP Title": "Site Setup SOPs",
     "Management Directive": "MD 9.3",
     "MD Section": "Execution of the Plan (9.3)",
     "Alignment Notes": "Aligns with Field Leadership plan execution requirements"},
    {"SOP Number": "9.41.470-510", "SOP Title": "Safety SOPs",
     "Management Directive": "MD 9.2; MD 9.3; MD 9.4",
     "MD Section": "Safety Requirements (9.2); Safety Management (9.3); Safety Enforcement (9.4)",
     "Alignment Notes": "Aligns with all safety requirements across field employee, leadership, and superintendent directives"},
    {"SOP Number": "9.41.675", "SOP Title": "Daily Huddles",
     "Management Directive": "MD 9.3",
     "MD Section": "Execution of the Plan (9.3)",
     "Alignment Notes": "Aligns with Field Leadership daily work layout requirements"},
    {"SOP Number": "9.41.680", "SOP Title": "Weekly Foreman Meetings",
     "Management Directive": "MD 9.4",
     "MD Section": "Work Force Development Coordination (9.4)",
     "Alignment Notes": "Aligns with Gen Supt weekly PM meeting attendance requirement"},
    {"SOP Number": "9.41.690-700", "SOP Title": "Tracking SOPs",
     "Management Directive": "MD 9.3; MD 9.5",
     "MD Section": "Reporting (9.3); Job Plans (9.5)",
     "Alignment Notes": "Aligns with Field Leadership reporting and PM job plan tracking"},
    {"SOP Number": "9.41.215", "SOP Title": "Daily Reports",
     "Management Directive": "MD 9.3; MD 9.5",
     "MD Section": "Daily Reports (9.3); Weekly Project Status Reports (9.5)",
     "Alignment Notes": "Aligns with Field Leadership daily reporting and PM weekly status requirements"},
    {"SOP Number": "9.41.360", "SOP Title": "Change Orders",
     "Management Directive": "MD 9.3; MD 9.5",
     "MD Section": "Changed Work (9.3); Change Order Requests (9.5)",
     "Alignment Notes": "Aligns with Field Leadership change authorization and PM change order management"},

    # Closeout aligned with MD 9.5
    {"SOP Number": "9.6.xxx", "SOP Title": "Closeout SOPs",
     "Management Directive": "MD 9.5",
     "MD Section": "Project Closeout - Required Documents (9.5)",
     "Alignment Notes": "Aligns with PM closeout requirements (interviews, O&M, warranty, billing, evaluations, surveys)"},
]

sop_md_df = pd.DataFrame(sop_md_mapping)

# ============================================
# SAVE ALL CROSS-REFERENCE MATRICES
# ============================================

with pd.ExcelWriter(f'{output_dir}/6_SOP_Training_Cross_Reference_Matrix.xlsx', engine='openpyxl') as writer:
    sop_training_df.to_excel(writer, sheet_name='SOP-Training Mapping', index=False)

print(f'Created: {output_dir}/6_SOP_Training_Cross_Reference_Matrix.xlsx')

with pd.ExcelWriter(f'{output_dir}/7_SOP_Job_Description_Cross_Reference_Matrix.xlsx', engine='openpyxl') as writer:
    sop_job_df.to_excel(writer, sheet_name='SOP-Job Description Mapping', index=False)

print(f'Created: {output_dir}/7_SOP_Job_Description_Cross_Reference_Matrix.xlsx')

with pd.ExcelWriter(f'{output_dir}/8_SOP_Management_Directive_Cross_Reference_Matrix.xlsx', engine='openpyxl') as writer:
    sop_md_df.to_excel(writer, sheet_name='SOP-MD Mapping', index=False)

print(f'Created: {output_dir}/8_SOP_Management_Directive_Cross_Reference_Matrix.xlsx')

# Summary
print()
print('=' * 60)
print('CROSS-REFERENCE MATRICES SUMMARY')
print('=' * 60)
print(f'SOP-Training mappings: {len(sop_training_df)}')
print(f'SOP-Job Description mappings: {len(sop_job_df)}')
print(f'SOP-Management Directive mappings: {len(sop_md_df)}')
