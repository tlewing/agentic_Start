import pandas as pd
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

output_dir = 'C:/Users/tewing/Desktop/Claude Projects/Project Outputs'

target_skill_rules = [
    # APPRENTICE ELECTRICIAN (7.2.1)
    {"Rule Name": "Apprentice Year 1 Onboarding", "Target Role": "Apprentice Electrician", "Policy Ref": "7.2.1",
     "Required Skills": "Safety Awareness & Culture; Hazard Recognition; First Aid/CPR/AED; Emergency Response",
     "Skill Level Set": "Safety", "Proficiency Level": "Foundational", "Timeframe": "First 30 days", "Prerequisites": "None"},
    {"Rule Name": "Apprentice Safety Fundamentals", "Target Role": "Apprentice Electrician", "Policy Ref": "7.2.1",
     "Required Skills": "NFPA 70E Fundamentals; Arc Flash Awareness; LOTO Fundamentals; Fall Hazard Recognition; Ladder Safety; HazCom Program Fundamentals",
     "Skill Level Set": "Safety", "Proficiency Level": "Foundational", "Timeframe": "First 90 days", "Prerequisites": "Apprentice Year 1 Onboarding"},
    {"Rule Name": "Apprentice Field Operations", "Target Role": "Apprentice Electrician", "Policy Ref": "7.2.1",
     "Required Skills": "Tool & Equipment Management; Documentation Practices; Effective Communication",
     "Skill Level Set": "Leadership & Field Management", "Proficiency Level": "Foundational", "Timeframe": "First 6 months", "Prerequisites": "Apprentice Safety Fundamentals"},

    # JOURNEYMAN ELECTRICIAN (7.2.2)
    {"Rule Name": "Journeyman Core Competencies", "Target Role": "Journeyman Electrician", "Policy Ref": "7.2.2",
     "Required Skills": "All Apprentice Skills; Simple LOTO Procedures; Personal Fall Arrest Systems; Scaffold Fundamentals; Confined Space Program",
     "Skill Level Set": "Safety", "Proficiency Level": "Intermediate", "Timeframe": "Upon promotion", "Prerequisites": "Journeyman License"},
    {"Rule Name": "Journeyman Leadership Introduction", "Target Role": "Journeyman Electrician", "Policy Ref": "7.2.2",
     "Required Skills": "Building Relationships; Mentoring & Coaching; Effective Communication",
     "Skill Level Set": "Communication & Coaching", "Proficiency Level": "Intermediate", "Timeframe": "First year as Journeyman", "Prerequisites": "Journeyman Core Competencies"},
    {"Rule Name": "Journeyman Technical Advancement", "Target Role": "Journeyman Electrician", "Policy Ref": "7.2.2",
     "Required Skills": "Job Plan Fundamentals; Quality Control; Trade Coordination",
     "Skill Level Set": "Project Planning & Productivity", "Proficiency Level": "Intermediate", "Timeframe": "Ongoing", "Prerequisites": "Journeyman Leadership Introduction"},

    # LEAD JOURNEYMAN (7.2.3)
    {"Rule Name": "Lead Journeyman Leadership", "Target Role": "Lead Journeyman", "Policy Ref": "7.2.3",
     "Required Skills": "Leadership Fundamentals; Field Supervision; Crew Planning; Team Building",
     "Skill Level Set": "Leadership & Field Management", "Proficiency Level": "Intermediate", "Timeframe": "Upon promotion", "Prerequisites": "All Journeyman training"},
    {"Rule Name": "Lead Journeyman Coordination", "Target Role": "Lead Journeyman", "Policy Ref": "7.2.3",
     "Required Skills": "Trade Coordination; Field Team Empowerment; Setting Expectations",
     "Skill Level Set": "Leadership & Field Management", "Proficiency Level": "Intermediate", "Timeframe": "First 6 months", "Prerequisites": "Lead Journeyman Leadership"},

    # FOREMAN (7.2.4)
    {"Rule Name": "Foreman Safety Certification", "Target Role": "Foreman", "Policy Ref": "7.2.4",
     "Required Skills": "Safety Inspections; Incident Investigation; Pre-Task Safety Planning; Complex LOTO Procedures; Arc Flash Risk Assessment",
     "Skill Level Set": "Safety", "Proficiency Level": "Advanced", "Timeframe": "Before or upon promotion", "Prerequisites": "GSL Safety Coordinator Certification"},
    {"Rule Name": "Foreman Leadership Essentials", "Target Role": "Foreman", "Policy Ref": "7.2.4",
     "Required Skills": "Foreman Role & Responsibilities; Field Supervision; Team Management; Delegation & Empowerment; Employee Motivation; Accountability & Ownership",
     "Skill Level Set": "Leadership & Field Management", "Proficiency Level": "Advanced", "Timeframe": "First 90 days", "Prerequisites": "Foreman Safety Certification"},
    {"Rule Name": "Foreman Operations Management", "Target Role": "Foreman", "Policy Ref": "7.2.4",
     "Required Skills": "Job Plan Setup; Job Plan Maintenance; Manpower Projection; Jobsite Efficiency; Documentation & Reporting",
     "Skill Level Set": "Project Planning & Productivity", "Proficiency Level": "Advanced", "Timeframe": "First 6 months", "Prerequisites": "Foreman Leadership Essentials"},
    {"Rule Name": "Foreman Performance Management", "Target Role": "Foreman", "Policy Ref": "7.2.4",
     "Required Skills": "Performance Management Fundamentals; Conducting Evaluations; Performance Reviews; Corrective Counseling",
     "Skill Level Set": "Performance Management", "Proficiency Level": "Advanced", "Timeframe": "First year", "Prerequisites": "Foreman Operations Management"},
    {"Rule Name": "Foreman Lean Construction", "Target Role": "Foreman", "Policy Ref": "7.2.4",
     "Required Skills": "Lean Fundamentals; Eight Wastes Recognition; Eliminate Waste; Focus on Flow; Pull Planning; Continuous Improvement",
     "Skill Level Set": "Lean Construction", "Proficiency Level": "Intermediate", "Timeframe": "First year", "Prerequisites": "Foreman Leadership Essentials"},
    {"Rule Name": "Foreman Emotional Intelligence", "Target Role": "Foreman", "Policy Ref": "7.2.4",
     "Required Skills": "EQ Fundamentals; Self-Awareness; Self-Regulation; Empathy; Social Skills",
     "Skill Level Set": "Emotional Intelligence", "Proficiency Level": "Intermediate", "Timeframe": "First year", "Prerequisites": "Foreman Leadership Essentials"},

    # PROJECT SUPERINTENDENT / GENERAL FOREMAN (7.2.5)
    {"Rule Name": "Superintendent Advanced Leadership", "Target Role": "Project Superintendent", "Policy Ref": "7.2.5",
     "Required Skills": "Values-Driven Leadership; Extreme Ownership; EQ Leadership; Trust Building",
     "Skill Level Set": "Leadership & Field Management", "Proficiency Level": "Expert", "Timeframe": "Upon promotion", "Prerequisites": "3-5 years Foreman experience"},
    {"Rule Name": "Superintendent Project Oversight", "Target Role": "Project Superintendent", "Policy Ref": "7.2.5",
     "Required Skills": "Project Planning; Scheduling Techniques; Productivity Analysis; Productivity Improvement; Construction Project Lifecycle",
     "Skill Level Set": "Project Planning & Productivity", "Proficiency Level": "Expert", "Timeframe": "First 6 months", "Prerequisites": "Superintendent Advanced Leadership"},
    {"Rule Name": "Superintendent Team Development", "Target Role": "Project Superintendent", "Policy Ref": "7.2.5",
     "Required Skills": "Career Development; Identifying Strengths; Escalation & Termination",
     "Skill Level Set": "Performance Management", "Proficiency Level": "Expert", "Timeframe": "First year", "Prerequisites": "Superintendent Project Oversight"},

    # SAFETY COORDINATOR (7.2.6)
    {"Rule Name": "Safety Coordinator Core", "Target Role": "Project Safety Coordinator", "Policy Ref": "7.2.6",
     "Required Skills": "All Safety Skills at Advanced Level; Safety Inspections; Incident Investigation; Emergency Response",
     "Skill Level Set": "Safety", "Proficiency Level": "Expert", "Timeframe": "Upon assignment", "Prerequisites": "OSHA 30, First Aid, CPR"},
    {"Rule Name": "Safety Coordinator Training", "Target Role": "Project Safety Coordinator", "Policy Ref": "7.2.6",
     "Required Skills": "Conducting Safety Orientation; Safety Meetings; Documentation & Compliance",
     "Skill Level Set": "Documentation & Compliance", "Proficiency Level": "Expert", "Timeframe": "First 90 days", "Prerequisites": "Safety Coordinator Core"},

    # ESTIMATOR (7.3.3)
    {"Rule Name": "Estimator Level I Foundation", "Target Role": "Estimator Assistant", "Policy Ref": "7.3.3",
     "Required Skills": "Accubid Fundamentals; Excel Skills; Documentation Practices; Effective Communication",
     "Skill Level Set": "Construction Software", "Proficiency Level": "Foundational", "Timeframe": "First 90 days", "Prerequisites": "None"},
    {"Rule Name": "Estimator Standard Competencies", "Target Role": "Estimator", "Policy Ref": "7.3.3",
     "Required Skills": "Accubid Fundamentals; Accubid Data Export; Job Plan Analysis; Time Management",
     "Skill Level Set": "Construction Software", "Proficiency Level": "Intermediate", "Timeframe": "First year", "Prerequisites": "Estimator Level I Foundation"},

    # PROJECT MANAGER (7.3.1 / 7.5)
    {"Rule Name": "Project Manager Core", "Target Role": "Project Manager", "Policy Ref": "7.3.1",
     "Required Skills": "Project Planning; Scheduling Techniques; Productivity Analysis; Documentation & Reporting",
     "Skill Level Set": "Project Planning & Productivity", "Proficiency Level": "Expert", "Timeframe": "Upon promotion", "Prerequisites": "Field or Estimating experience"},
    {"Rule Name": "Project Manager Software", "Target Role": "Project Manager", "Policy Ref": "7.3.1",
     "Required Skills": "ProCore Fundamentals; ProCore Job Setup; ViewPoint Change Orders; Vista",
     "Skill Level Set": "Construction Software", "Proficiency Level": "Advanced", "Timeframe": "First 90 days", "Prerequisites": "Project Manager Core"},
    {"Rule Name": "Project Manager Leadership", "Target Role": "Project Manager", "Policy Ref": "7.3.1",
     "Required Skills": "Values-Driven Leadership; Extreme Ownership; Strategic Thinking; Presentation Skills",
     "Skill Level Set": "Professional Development", "Proficiency Level": "Expert", "Timeframe": "Ongoing", "Prerequisites": "Project Manager Software"},

    # OPERATIONS MANAGER (7.3.1)
    {"Rule Name": "Operations Manager Leadership", "Target Role": "Operations Manager", "Policy Ref": "7.3.1",
     "Required Skills": "All PM Skills; Industry Leadership; Strategic Thinking; Presentation Skills",
     "Skill Level Set": "Professional Development", "Proficiency Level": "Expert", "Timeframe": "Upon promotion", "Prerequisites": "PM experience"},

    # ADMINISTRATIVE ROLES
    {"Rule Name": "Admin Support Foundation", "Target Role": "Administrative Support", "Policy Ref": "7.4.5",
     "Required Skills": "Excel Skills; Outlook; Teams; Documentation Practices; Time Management",
     "Skill Level Set": "Construction Software", "Proficiency Level": "Foundational", "Timeframe": "First 30 days", "Prerequisites": "None"},
    {"Rule Name": "HR Manager Compliance", "Target Role": "Human Resource Manager", "Policy Ref": "7.4.1",
     "Required Skills": "Documentation & Compliance; Regulatory Inspections; Performance Management Fundamentals",
     "Skill Level Set": "Documentation & Compliance", "Proficiency Level": "Expert", "Timeframe": "Ongoing", "Prerequisites": "HR Certification"},

    # NEW HIRE (ALL EMPLOYEES)
    {"Rule Name": "All Employee Orientation", "Target Role": "All Employees", "Policy Ref": "9.2",
     "Required Skills": "Safety Awareness & Culture; Emergency Response; HazCom Program Fundamentals",
     "Skill Level Set": "Safety", "Proficiency Level": "Foundational", "Timeframe": "First 7 days", "Prerequisites": "None"},
]

df_rules = pd.DataFrame(target_skill_rules)
df_rules.to_excel(f'{output_dir}/5_Target_Skill_Rules_Master_List.xlsx', index=False)

print(f'Created: {output_dir}/5_Target_Skill_Rules_Master_List.xlsx')
print(f'Total Target Skill Rules: {len(target_skill_rules)}')
print()
print('Rules by Target Role:')
role_counts = df_rules['Target Role'].value_counts()
for role, count in role_counts.items():
    print(f'  {role}: {count} rules')
