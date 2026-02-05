import pandas as pd
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

output_dir = 'C:/Users/tewing/Desktop/Claude Projects/Project Outputs'

# ============================================
# MASTER CROSS-REFERENCE DOCUMENT
# ============================================

# Read existing files
training_df = pd.read_excel(f'{output_dir}/1_Training_Module_Inventory.xlsx')
skill_rules_df = pd.read_excel(f'{output_dir}/5_Target_Skill_Rules_Master_List.xlsx')
sop_training_df = pd.read_excel(f'{output_dir}/6_SOP_Training_Cross_Reference_Matrix.xlsx')
sop_job_df = pd.read_excel(f'{output_dir}/7_SOP_Job_Description_Cross_Reference_Matrix.xlsx')
sop_md_df = pd.read_excel(f'{output_dir}/8_SOP_Management_Directive_Cross_Reference_Matrix.xlsx')

# Create comprehensive role-based view
role_matrix = [
    # APPRENTICE ELECTRICIAN
    {"Role": "Apprentice Electrician", "Policy Ref": "7.2.1",
     "Management Directives": "MD 9.2 (Field Employees)",
     "Key SOPs": "Safety SOPs (9.41.470-510); Tool Control; Site Work Requirements",
     "Required Training": "New Hire Safety Orientation; NFPA 70E Fundamentals; Arc Flash Awareness; LOTO Fundamentals; Fall Protection; Ladder Safety; HazCom; Confined Space",
     "Skill Level Sets": "Safety (Foundational); Leadership & Field Management (Foundational)",
     "Target Rules": "Apprentice Year 1 Onboarding; Apprentice Safety Fundamentals; Apprentice Field Operations",
     "Progression Path": "4-year apprenticeship -> Journeyman License"},

    # JOURNEYMAN ELECTRICIAN
    {"Role": "Journeyman Electrician", "Policy Ref": "7.2.2",
     "Management Directives": "MD 9.2 (Field Employees)",
     "Key SOPs": "All Apprentice SOPs + Quality Control; Trade Coordination; Simple LOTO",
     "Required Training": "All Apprentice Training + Leadership Introduction; Mentoring & Coaching; Job Plan Fundamentals",
     "Skill Level Sets": "Safety (Intermediate); Communication & Coaching (Intermediate); Project Planning (Intermediate)",
     "Target Rules": "Journeyman Core Competencies; Journeyman Leadership Introduction; Journeyman Technical Advancement",
     "Progression Path": "Journeyman -> Lead Journeyman -> Foreman"},

    # LEAD JOURNEYMAN
    {"Role": "Lead Journeyman", "Policy Ref": "7.2.3",
     "Management Directives": "MD 9.2; MD 9.3 (Field Leadership)",
     "Key SOPs": "All Journeyman SOPs + Crew Planning; Field Coordination",
     "Required Training": "All Journeyman Training + Leadership Fundamentals; Field Supervision; Team Building",
     "Skill Level Sets": "Leadership & Field Management (Intermediate)",
     "Target Rules": "Lead Journeyman Leadership; Lead Journeyman Coordination",
     "Progression Path": "Lead Journeyman -> Foreman"},

    # FOREMAN
    {"Role": "Foreman", "Policy Ref": "7.2.4",
     "Management Directives": "MD 9.3 (Field Leadership)",
     "Key SOPs": "9.2.050 Plans Review; 9.41.470-510 Safety; 9.41.675-725 Field Operations; 9.41.215 Daily Reports; All Site Setup SOPs",
     "Required Training": "Safety Coordinator Certification (1-11); Introduction to Field Leadership (all sections); Foreman Role & Responsibilities; Job Plan Setup; Performance Management; Lean Construction; Emotional Intelligence",
     "Skill Level Sets": "Safety (Advanced); Leadership & Field Management (Advanced); Project Planning (Advanced); Performance Management (Advanced); Lean Construction (Intermediate); Emotional Intelligence (Intermediate)",
     "Target Rules": "Foreman Safety Certification; Foreman Leadership Essentials; Foreman Operations Management; Foreman Performance Management; Foreman Lean Construction; Foreman Emotional Intelligence",
     "Progression Path": "Foreman (3-5 years) -> Project Superintendent"},

    # PROJECT SUPERINTENDENT
    {"Role": "Project Superintendent", "Policy Ref": "7.2.5",
     "Management Directives": "MD 9.3 (Field Leadership); MD 9.4 (General Superintendents)",
     "Key SOPs": "All Foreman SOPs + Multi-crew coordination; Schedule management; Change order integration",
     "Required Training": "All Foreman Training + Values-Driven Leadership; Extreme Ownership; EQ Leadership; Project Planning; Scheduling; Productivity Analysis; Career Development",
     "Skill Level Sets": "Leadership & Field Management (Expert); Project Planning & Productivity (Expert); Performance Management (Expert)",
     "Target Rules": "Superintendent Advanced Leadership; Superintendent Project Oversight; Superintendent Team Development",
     "Progression Path": "Project Superintendent -> Operations Management"},

    # SAFETY COORDINATOR
    {"Role": "Project Safety Coordinator", "Policy Ref": "7.2.6",
     "Management Directives": "MD 9.2; MD 9.3; MD 9.4",
     "Key SOPs": "9.41.470 Site-Specific Safety Plan; 9.41.475 Safety Orientation; 9.41.480 Safety Inspections; 9.41.485 Safety Meetings; 9.41.490-510 Incident Response",
     "Required Training": "Safety Coordinator (all 11 modules); OSHA Focus Four; All Safety Training at Expert Level",
     "Skill Level Sets": "Safety (Expert); Documentation & Compliance (Expert)",
     "Target Rules": "Safety Coordinator Core; Safety Coordinator Training",
     "Progression Path": "Dedicated Safety Role"},

    # ESTIMATOR
    {"Role": "Estimator", "Policy Ref": "7.3.3",
     "Management Directives": "MD 9.7 (Estimating)",
     "Key SOPs": "Project Turnover Meeting participation; Bid document management; Value engineering",
     "Required Training": "Accubid Fundamentals; Accubid Data Export; Job Plan Analysis; Excel Skills; Documentation Practices",
     "Skill Level Sets": "Construction Software (Foundational to Intermediate)",
     "Target Rules": "Estimator Level I Foundation; Estimator Standard Competencies",
     "Progression Path": "Estimator Assistant -> Estimator -> Lead Estimator -> Project Manager"},

    # PROJECT MANAGER
    {"Role": "Project Manager", "Policy Ref": "7.3.1",
     "Management Directives": "MD 9.5 (Project Management)",
     "Key SOPs": "9.2.xxx Pre-Construction SOPs; 9.41.xxx Execution SOPs; 9.6.xxx Closeout SOPs; All scheduling, documentation, change order SOPs",
     "Required Training": "Project Planning; Scheduling; Productivity Analysis; ProCore Fundamentals; ViewPoint Change Orders; Values-Driven Leadership; Extreme Ownership; Strategic Thinking; Presentation Skills",
     "Skill Level Sets": "Project Planning & Productivity (Expert); Construction Software (Advanced); Professional Development (Expert)",
     "Target Rules": "Project Manager Core; Project Manager Software; Project Manager Leadership",
     "Progression Path": "Project Manager -> Operations Manager -> Branch Manager"},

    # OPERATIONS MANAGER
    {"Role": "Operations Manager", "Policy Ref": "7.3.1",
     "Management Directives": "MD 9.5; MD 9.6 (Branch Management)",
     "Key SOPs": "All Project Manager SOPs + Strategic oversight",
     "Required Training": "All PM Training + Industry Leadership; Strategic Thinking; Presentation Skills",
     "Skill Level Sets": "Professional Development (Expert)",
     "Target Rules": "Operations Manager Leadership",
     "Progression Path": "Operations Manager -> Executive Leadership"},

    # HR MANAGER
    {"Role": "Human Resource Manager", "Policy Ref": "7.4.1",
     "Management Directives": "All MDs (compliance oversight)",
     "Key SOPs": "Performance review SOPs; Policy compliance SOPs",
     "Required Training": "Documentation & Compliance; Performance Management Fundamentals",
     "Skill Level Sets": "Documentation & Compliance (Expert)",
     "Target Rules": "HR Manager Compliance",
     "Progression Path": "HR Manager -> VP HR"},

    # ADMINISTRATIVE SUPPORT
    {"Role": "Administrative Support", "Policy Ref": "7.4.5",
     "Management Directives": "MD 9.5 (support functions)",
     "Key SOPs": "Document management SOPs; Filing standards",
     "Required Training": "Excel Skills; Outlook; Teams; Documentation Practices; Time Management",
     "Skill Level Sets": "Construction Software (Foundational)",
     "Target Rules": "Admin Support Foundation",
     "Progression Path": "Admin Support -> Specialized Admin Roles"},

    # ALL EMPLOYEES
    {"Role": "All Employees", "Policy Ref": "9.2",
     "Management Directives": "MD 9.2 (Field Employees) - General Requirements",
     "Key SOPs": "General site work requirements; Safety orientation",
     "Required Training": "Safety Awareness & Culture; Emergency Response; HazCom Program Fundamentals",
     "Skill Level Sets": "Safety (Foundational)",
     "Target Rules": "All Employee Orientation",
     "Progression Path": "Role-specific progression"},
]

role_matrix_df = pd.DataFrame(role_matrix)

# Create SOP Category Summary
sop_categories = [
    {"Category": "9.2.xxx Pre-Construction", "SOP Count": 19,
     "Key Processes": "Contract review, Team selection, Turnover meeting, Plans review, Site visit, Material planning, Budget, Schedule, Kickoff",
     "Primary Roles": "Project Manager; Estimator; Field Supervisor",
     "Management Directives": "MD 9.5; MD 9.7",
     "EPMP/GSL Alignment": "GSL Pre-Construction Planning Process (10 categories, 46 activities)"},

    {"Category": "9.3.xxx Site Setup", "SOP Count": 17,
     "Key Processes": "Office trailer, Storage, Fencing, Power, Water, Sanitary, Lighting, Signage, Security, Laydown, Staging, Parking",
     "Primary Roles": "Foreman; Project Superintendent",
     "Management Directives": "MD 9.3",
     "EPMP/GSL Alignment": "EPMP Mobilization (7 activities)"},

    {"Category": "9.4.xxx Project Execution", "SOP Count": 159,
     "Key Processes": "Meetings, Documentation, Communication, Scheduling, Scope control, Cost control, Safety, Quality, Resources, Procurement, Field operations",
     "Primary Roles": "Project Manager; Foreman; Safety Coordinator",
     "Management Directives": "MD 9.3; MD 9.5",
     "EPMP/GSL Alignment": "EPMP Project Management (14 categories, 81 activities)"},

    {"Category": "9.5.xxx Commissioning", "SOP Count": 2,
     "Key Processes": "Commissioning meetings, Commissioning activities",
     "Primary Roles": "Project Manager; Foreman",
     "Management Directives": "MD 9.5",
     "EPMP/GSL Alignment": "EPMP Quality Control/Management"},

    {"Category": "9.6.xxx Closeout", "SOP Count": 10,
     "Key Processes": "Turnover prep, Closeout meetings, Punch lists, As-builts, O&M manuals, Warranties, Documentation, Post-project review, Lessons learned",
     "Primary Roles": "Project Manager; Foreman; Admin Support",
     "Management Directives": "MD 9.5 (Project Closeout)",
     "EPMP/GSL Alignment": "EPMP Project Closeout"},
]

sop_categories_df = pd.DataFrame(sop_categories)

# Training Gap Analysis
training_gaps = [
    {"Foreman Training Tab": "TAB 10 - Job Setup-Schedule of Values", "Has SCORM": "No", "Gap Priority": "High", "Recommendation": "Create SCORM module for Schedule of Values setup"},
    {"Foreman Training Tab": "TAB 12 - Look Ahead", "Has SCORM": "No", "Gap Priority": "High", "Recommendation": "Create SCORM module for Look Ahead scheduling"},
    {"Foreman Training Tab": "TAB 14 - Daily Reports", "Has SCORM": "No", "Gap Priority": "High", "Recommendation": "Create SCORM module for Daily Report completion"},
    {"Foreman Training Tab": "TAB 15 - Integrating Schedule and Daily Reports", "Has SCORM": "No", "Gap Priority": "High", "Recommendation": "Create SCORM module on schedule/report integration"},
    {"Foreman Training Tab": "TAB 17 - Creating Budgets", "Has SCORM": "No", "Gap Priority": "High", "Recommendation": "Create SCORM module for budget creation"},
    {"Foreman Training Tab": "TAB 18 - Job Close Out", "Has SCORM": "No", "Gap Priority": "High", "Recommendation": "Create SCORM module for job closeout procedures"},
    {"Foreman Training Tab": "TAB 20 - Job Cost Projections", "Has SCORM": "No", "Gap Priority": "High", "Recommendation": "Create SCORM module for cost projections"},
    {"Foreman Training Tab": "TAB 9 - Submittals", "Has SCORM": "No", "Gap Priority": "High", "Recommendation": "Create SCORM module for submittal management"},
    {"Foreman Training Tab": "TAB 41 - Material Management & Control", "Has SCORM": "No", "Gap Priority": "High", "Recommendation": "Create SCORM module for material management"},
    {"Foreman Training Tab": "Tab 42 - Prefab", "Has SCORM": "No", "Gap Priority": "Medium", "Recommendation": "Create SCORM module for prefabrication"},
    {"Foreman Training Tab": "TAB 49 - Bluebeam", "Has SCORM": "No", "Gap Priority": "Medium", "Recommendation": "Create SCORM module for Bluebeam software"},
    {"Foreman Training Tab": "TAB 57 - ProCore", "Has SCORM": "No", "Gap Priority": "High", "Recommendation": "Create SCORM module for ProCore (referenced in SOPs)"},
    {"Foreman Training Tab": "Tab 28 - Ethics in the Workplace", "Has SCORM": "No", "Gap Priority": "Medium", "Recommendation": "Create SCORM module for workplace ethics"},
    {"Foreman Training Tab": "Tab 35 - Conflict Resolution", "Has SCORM": "No", "Gap Priority": "Medium", "Recommendation": "Create SCORM module for conflict resolution"},
    {"Foreman Training Tab": "Tab 34 - Excel Lessons", "Has SCORM": "No", "Gap Priority": "Low", "Recommendation": "Create SCORM module for Excel skills"},
]

training_gaps_df = pd.DataFrame(training_gaps)

# Write Master Cross-Reference Document
with pd.ExcelWriter(f'{output_dir}/9_Master_Cross_Reference_Document.xlsx', engine='openpyxl') as writer:
    role_matrix_df.to_excel(writer, sheet_name='Role-Based Matrix', index=False)
    sop_categories_df.to_excel(writer, sheet_name='SOP Category Summary', index=False)
    training_gaps_df.to_excel(writer, sheet_name='Training Gap Analysis', index=False)
    sop_training_df.to_excel(writer, sheet_name='SOP-Training Details', index=False)
    sop_job_df.to_excel(writer, sheet_name='SOP-Job Description Details', index=False)
    sop_md_df.to_excel(writer, sheet_name='SOP-Management Directive Details', index=False)

print(f'Created: {output_dir}/9_Master_Cross_Reference_Document.xlsx')
print()
print('Sheets included:')
print('  1. Role-Based Matrix - Complete view by job role')
print('  2. SOP Category Summary - SOPs by category with EPMP alignment')
print('  3. Training Gap Analysis - Missing SCORM content priorities')
print('  4. SOP-Training Details - Detailed SOP to training mappings')
print('  5. SOP-Job Description Details - Detailed SOP to role mappings')
print('  6. SOP-Management Directive Details - Detailed SOP to MD mappings')
print()
print(f'Total roles documented: {len(role_matrix_df)}')
print(f'Total SOP categories: {len(sop_categories_df)}')
print(f'Training gaps identified: {len(training_gaps_df)}')
