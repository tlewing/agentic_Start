"""
Generate Course Descriptions for SCORM Catalog - Version 2

Includes:
- Short descriptions (50-75 words)
- Long descriptions (200-250 words)
- Categories/Subcategories
- Search tags
- SKILLS mapping (multiple skills per course)
- Multiple Skill Level Sets per course
"""

import csv
import re
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from datetime import datetime

# Full Skills Framework from Learn365
SKILL_FRAMEWORK = {
    "Safety": [
        "Safety Awareness & Culture",
        "Accident Prevention",
        "Hazard Recognition",
        "Pre-Task Safety Planning",
        "Safety Inspections",
        "Incident Investigation",
        "Injury Management",
        "First Aid/CPR/AED",
        "Emergency Response",
        "NFPA 70E Fundamentals",
        "Approach Boundary Management",
        "Arc Flash Awareness",
        "Arc Flash Risk Assessment",
        "Arc Flash PPE Selection",
        "Energized Work Practices",
        "Energized Work Permitting",
        "Electrical Hazard Recognition",
        "Electrically Safe Work Condition",
        "LOTO Fundamentals",
        "Simple LOTO Procedures",
        "Complex LOTO Procedures",
        "Abnormal Lock Removal",
        "De-Energization Verification",
        "Return to Service",
        "Fall Hazard Recognition",
        "Personal Fall Arrest Systems",
        "Ladder Safety",
        "Scaffold Fundamentals",
        "Scaffold Access & Egress",
        "Scaffold Assembly & Inspection",
        "Fall Protection on Scaffolds",
        "HazCom Program Fundamentals",
        "GHS System Understanding",
        "Container Label Use",
        "SDS Use & Access",
        "Chemical Hazard Identification",
        "Pictogram Interpretation",
        "Confined Space Program",
        "Atmospheric Hazard Detection",
        "Entry Permit Management",
    ],
    "Lean Construction": [
        "Lean Fundamentals",
        "Lean History",
        "Lean Application",
        "Eight Wastes Recognition",
        "Eliminate Waste",
        "Focus on Flow",
        "Generate Value",
        "Optimize the Whole",
        "Continuous Improvement",
        "Respect for People",
        "Pull Planning",
        "Field Team Empowerment",
    ],
    "Leadership & Field Management": [
        "Foreman Role & Responsibilities",
        "Field Supervision",
        "Crew Planning",
        "Trade Coordination",
        "Jobsite Efficiency",
        "Quality Control",
        "Tool & Equipment Management",
        "Manpower Projection",
        "Job Closeout",
        "Field Empowerment",
        "Leadership Fundamentals",
        "Values-Driven Leadership",
        "Accountability & Ownership",
        "Team Building",
        "Team Management",
        "Delegation & Empowerment",
        "Employee Motivation",
        "Team Morale",
        "Organizational Structuring",
        "Extreme Ownership",
    ],
    "Communication & Coaching": [
        "Effective Communication",
        "Building Relationships",
        "Conducting One-on-Ones",
        "Mentoring & Coaching",
        "Conflict Resolution",
        "Handling Resistance",
        "Setting Expectations",
        "Using the GROW Model",
    ],
    "Emotional Intelligence": [
        "EQ Fundamentals",
        "Self-Awareness",
        "Self-Regulation",
        "Empathy",
        "Social Skills",
        "EQ Leadership",
        "Trust Building",
    ],
    "Performance Management": [
        "Performance Management Fundamentals",
        "Conducting Evaluations",
        "Performance Reviews",
        "Corrective Counseling",
        "Escalation & Termination",
        "Career Development",
        "Identifying Strengths",
    ],
    "Construction Software": [
        "Accubid Fundamentals",
        "Accubid Data Export",
        "ViewPoint Change Orders",
        "ProCore Fundamentals",
        "ProCore Job Setup",
        "ProCore Job Plans",
        "Job Plan Fundamentals",
        "Job Plan Setup",
        "Job Plan Maintenance",
        "Excel Skills",
        "Vista",
        "Teams",
        "Outlook",
        "Word",
    ],
    "Project Planning & Productivity": [
        "Project Planning",
        "Job Plan Analysis",
        "Scheduling Techniques",
        "Productivity Analysis",
        "Productivity Improvement",
        "Time Management",
        "Construction Project Lifecycle",
        "Process Improvement",
    ],
    "Documentation & Compliance": [
        "Documentation Practices",
        "Documentation & Reporting",
        "Regulatory Inspections",
        "Documentation & Compliance",
    ],
    "Professional Development": [
        "Presentation Skills",
        "Strategic Thinking",
        "Industry Leadership",
    ],
}

# Course to Skills Mapping Rules
def get_skills_for_course(title, existing_category):
    """Map specific skills to a course based on title and category"""
    title_lower = title.lower()
    skills = []
    skill_level_sets = set()

    # === SAFETY COURSES ===

    # Lockout/Tagout courses
    if "lockout" in title_lower or "tagout" in title_lower or "loto" in title_lower:
        skill_level_sets.add("Safety")
        skills.append("LOTO Fundamentals")
        if "simple" in title_lower:
            skills.append("Simple LOTO Procedures")
        elif "complex" in title_lower:
            skills.append("Complex LOTO Procedures")
        elif "abnormal" in title_lower:
            skills.append("Abnormal Lock Removal")
        elif "return" in title_lower or "service" in title_lower:
            skills.append("Return to Service")
        elif "verif" in title_lower or "de-energiz" in title_lower:
            skills.append("De-Energization Verification")
            skills.append("Electrically Safe Work Condition")
        elif "hazardous energy" in title_lower:
            skills.append("Simple LOTO Procedures")
            skills.append("Electrically Safe Work Condition")
        else:
            # General LOTO
            skills.extend(["Simple LOTO Procedures", "De-Energization Verification"])

    # Arc Flash / NFPA 70E courses
    if "arc flash" in title_lower or "nfpa 70" in title_lower:
        skill_level_sets.add("Safety")
        skills.append("NFPA 70E Fundamentals")
        skills.append("Arc Flash Awareness")
        if "ppe" in title_lower:
            skills.append("Arc Flash PPE Selection")
        if "risk" in title_lower or "assessment" in title_lower:
            skills.append("Arc Flash Risk Assessment")
        if "boundar" in title_lower:
            skills.append("Approach Boundary Management")

    # Energized Work
    if "energized" in title_lower and "work" in title_lower:
        skill_level_sets.add("Safety")
        skills.append("Energized Work Practices")
        if "permit" in title_lower:
            skills.append("Energized Work Permitting")
        if "precaution" in title_lower or "practice" in title_lower:
            skills.append("Electrical Hazard Recognition")

    # Fall Protection
    if "fall protection" in title_lower or "fall hazard" in title_lower:
        skill_level_sets.add("Safety")
        skills.extend(["Fall Hazard Recognition", "Personal Fall Arrest Systems"])

    # Scaffolding
    if "scaffold" in title_lower:
        skill_level_sets.add("Safety")
        skills.append("Scaffold Fundamentals")
        if "access" in title_lower or "egress" in title_lower:
            skills.append("Scaffold Access & Egress")
        if "assembl" in title_lower or "inspect" in title_lower:
            skills.append("Scaffold Assembly & Inspection")
        if "osha" in title_lower or "regulation" in title_lower:
            skills.append("Scaffold Fundamentals")
        skills.append("Fall Protection on Scaffolds")

    # Ladder Safety
    if "ladder" in title_lower:
        skill_level_sets.add("Safety")
        skills.append("Ladder Safety")
        skills.append("Fall Hazard Recognition")

    # Hazard Communication / GHS / SDS
    if "hazard communication" in title_lower or "hazcom" in title_lower:
        skill_level_sets.add("Safety")
        skills.extend(["HazCom Program Fundamentals", "GHS System Understanding"])
    if "ghs" in title_lower:
        skill_level_sets.add("Safety")
        skills.append("GHS System Understanding")
    if "sds" in title_lower or "safety data sheet" in title_lower:
        skill_level_sets.add("Safety")
        skills.append("SDS Use & Access")
    if "container label" in title_lower or "label" in title_lower and "chemical" in title_lower:
        skill_level_sets.add("Safety")
        skills.append("Container Label Use")
    if "chemical hazard" in title_lower or "types of chemical" in title_lower:
        skill_level_sets.add("Safety")
        skills.append("Chemical Hazard Identification")
    if "pictogram" in title_lower:
        skill_level_sets.add("Safety")
        skills.append("Pictogram Interpretation")

    # Confined Space
    if "confined space" in title_lower:
        skill_level_sets.add("Safety")
        skills.append("Confined Space Program")
        if "atmospher" in title_lower:
            skills.append("Atmospheric Hazard Detection")
        if "permit" in title_lower or "entry" in title_lower:
            skills.append("Entry Permit Management")

    # Safety Coordinator series
    if "safety coordinator" in title_lower:
        skill_level_sets.add("Safety")
        skills.append("Safety Awareness & Culture")
        if "orientation" in title_lower:
            skills.append("Safety Awareness & Culture")
        if "task training" in title_lower:
            skills.append("Pre-Task Safety Planning")
        if "meeting" in title_lower:
            skills.append("Safety Awareness & Culture")
        if "planning" in title_lower or "hazard" in title_lower:
            skills.extend(["Hazard Recognition", "Pre-Task Safety Planning"])
        if "inspection" in title_lower:
            skills.append("Safety Inspections")
        if "disciplin" in title_lower:
            skill_level_sets.add("Performance Management")
            skills.append("Corrective Counseling")
        if "accident" in title_lower or "incident" in title_lower:
            skills.append("Incident Investigation")
        if "injury" in title_lower or "case management" in title_lower:
            skills.append("Injury Management")
        if "osha" in title_lower or "msha" in title_lower:
            skills.append("Regulatory Inspections")
            skill_level_sets.add("Documentation & Compliance")

    # General Safety / New Hire
    if "new hire" in title_lower or "safety orientation" in title_lower:
        skill_level_sets.add("Safety")
        skills.extend(["Safety Awareness & Culture", "Hazard Recognition"])
        if "commitment" in title_lower or "zero" in title_lower:
            skills.append("Accident Prevention")

    # OSHA Focus Four
    if "focus four" in title_lower:
        skill_level_sets.add("Safety")
        skills.extend(["Hazard Recognition", "Fall Hazard Recognition", "Electrical Hazard Recognition"])

    # Slips, Trips, Falls
    if "slip" in title_lower or "trip" in title_lower:
        skill_level_sets.add("Safety")
        skills.extend(["Hazard Recognition", "Accident Prevention"])

    # T.R.A.C.K. methodology
    if "track" in title_lower and ("hazard" in title_lower or "planning" in title_lower):
        skill_level_sets.add("Safety")
        skills.extend(["Hazard Recognition", "Pre-Task Safety Planning"])

    # Safety Management introduction
    if "safety management" in title_lower:
        skill_level_sets.add("Safety")
        skills.extend(["Safety Awareness & Culture", "Safety Inspections", "Hazard Recognition"])

    # === LEAN CONSTRUCTION COURSES ===

    if "lean" in title_lower:
        skill_level_sets.add("Lean Construction")
        if "what is lean" in title_lower or "introduction" in title_lower:
            skills.append("Lean Fundamentals")
        if "history" in title_lower or "brief history" in title_lower:
            skills.append("Lean History")
        if "apply" in title_lower or "construction" in title_lower:
            skills.append("Lean Application")
        if "waste" in title_lower:
            skills.append("Eight Wastes Recognition")
            skills.append("Eliminate Waste")
        if "pull planning" in title_lower:
            skills.append("Pull Planning")
        if "continuous improvement" in title_lower:
            skills.append("Continuous Improvement")
        if "productivity" in title_lower:
            skills.append("Lean Application")
            skill_level_sets.add("Project Planning & Productivity")
            skills.append("Productivity Improvement")
        if "process" in title_lower:
            skills.append("Focus on Flow")
        if "production theory" in title_lower:
            skills.append("Optimize the Whole")
        if "training the industry" in title_lower or "reshaping" in title_lower:
            skills.append("Lean Application")
            skill_level_sets.add("Professional Development")
            skills.append("Industry Leadership")

    # Eight Wastes
    if "eight waste" in title_lower or "waste" in title_lower and "construction" in title_lower:
        skill_level_sets.add("Lean Construction")
        skills.extend(["Eight Wastes Recognition", "Eliminate Waste"])

    # Pull Planning / Sticky Note
    if "pull planning" in title_lower or "sticky note" in title_lower:
        skill_level_sets.add("Lean Construction")
        skills.append("Pull Planning")
        skill_level_sets.add("Project Planning & Productivity")
        skills.append("Scheduling Techniques")

    # === LEADERSHIP COURSES ===

    # Values-Driven Leadership / Coach K
    if "values" in title_lower and "driven" in title_lower or "coach k" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Values-Driven Leadership")
        skills.append("Leadership Fundamentals")
        if "core values" in title_lower or "define" in title_lower:
            skills.append("Values-Driven Leadership")
        if "team" in title_lower or "winning" in title_lower:
            skills.append("Team Building")
        if "own your team" in title_lower:
            skills.append("Accountability & Ownership")
        if "read" in title_lower or "people" in title_lower:
            skill_level_sets.add("Emotional Intelligence")
            skills.append("Empathy")
        if "communication" in title_lower:
            skill_level_sets.add("Communication & Coaching")
            skills.append("Effective Communication")
        if "emotion" in title_lower:
            skill_level_sets.add("Emotional Intelligence")
            skills.append("EQ Leadership")
        if "planning" in title_lower or "next play" in title_lower:
            skill_level_sets.add("Project Planning & Productivity")
            skills.append("Project Planning")
        if "recruit" in title_lower or "retain" in title_lower:
            skills.append("Team Building")
            skill_level_sets.add("Performance Management")
            skills.append("Career Development")
        if "performance" in title_lower:
            skill_level_sets.add("Performance Management")
            skills.append("Performance Management Fundamentals")
        if "feedback" in title_lower:
            skill_level_sets.add("Communication & Coaching")
            skills.append("Setting Expectations")
        if "develop" in title_lower and "leader" in title_lower:
            skills.append("Leadership Fundamentals")
            skill_level_sets.add("Performance Management")
            skills.append("Career Development")
        if "legacy" in title_lower:
            skills.append("Leadership Fundamentals")
        if "motivation" in title_lower or "habit" in title_lower:
            skills.append("Employee Motivation")
        if "bounce back" in title_lower or "loss" in title_lower:
            skill_level_sets.add("Emotional Intelligence")
            skills.append("Self-Regulation")

    # Extreme Ownership
    if "extreme ownership" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.extend(["Extreme Ownership", "Accountability & Ownership", "Leadership Fundamentals"])

    # Leadership Laws (Cover and Move, Keep it Simple, etc.)
    if "leadership law" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Leadership Fundamentals")
        if "cover and move" in title_lower:
            skills.append("Team Building")
        if "simple" in title_lower:
            skill_level_sets.add("Communication & Coaching")
            skills.append("Effective Communication")
        if "prioritize" in title_lower or "execute" in title_lower:
            skill_level_sets.add("Project Planning & Productivity")
            skills.append("Project Planning")
        if "decentralize" in title_lower:
            skills.append("Delegation & Empowerment")

    # Team Management / Team Building
    if "team management" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Team Management")
    if "building" in title_lower and "team" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Team Building")

    # Team Morale
    if "morale" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.extend(["Team Morale", "Employee Motivation"])

    # Motivation
    if "motivat" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Employee Motivation")

    # Field Leadership
    if "field leadership" in title_lower or "introduction to field" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Field Supervision")
        if "skills" in title_lower and "traits" in title_lower:
            skills.append("Foreman Role & Responsibilities")
        if "anatomy" in title_lower or "project" in title_lower:
            skill_level_sets.add("Project Planning & Productivity")
            skills.append("Construction Project Lifecycle")

    # Foreman
    if "foreman" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.extend(["Foreman Role & Responsibilities", "Field Supervision"])

    # Empowerment
    if "empowerment" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.extend(["Field Empowerment", "Delegation & Empowerment"])

    # What Makes a Leader
    if "what makes a leader" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Leadership Fundamentals")

    # Human Interaction
    if "human interaction" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Leadership Fundamentals")
        skill_level_sets.add("Communication & Coaching")
        skills.append("Building Relationships")

    # New Manager 101
    if "new manager" in title_lower or "manager 101" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.extend(["Leadership Fundamentals", "Team Management"])

    # Critical Leadership Training
    if "critical leadership" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.extend(["Leadership Fundamentals", "Accountability & Ownership"])

    # Sub-contractors
    if "sub-contractor" in title_lower or "subcontractor" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Trade Coordination")

    # === COMMUNICATION & COACHING ===

    if "communication" in title_lower:
        skill_level_sets.add("Communication & Coaching")
        skills.append("Effective Communication")
        if "feedback" in title_lower:
            skills.append("Setting Expectations")

    # === EMOTIONAL INTELLIGENCE ===

    if "emotional intelligence" in title_lower or "eq" in title_lower.split():
        skill_level_sets.add("Emotional Intelligence")
        skills.append("EQ Fundamentals")

    if "self-awareness" in title_lower or "self awareness" in title_lower:
        skill_level_sets.add("Emotional Intelligence")
        skills.append("Self-Awareness")

    if "self-regulation" in title_lower or "self regulation" in title_lower:
        skill_level_sets.add("Emotional Intelligence")
        skills.append("Self-Regulation")

    if "empathy" in title_lower:
        skill_level_sets.add("Emotional Intelligence")
        skills.append("Empathy")

    if "social skills" in title_lower:
        skill_level_sets.add("Emotional Intelligence")
        skills.append("Social Skills")

    if "leading with emotional" in title_lower:
        skill_level_sets.add("Emotional Intelligence")
        skills.extend(["EQ Fundamentals", "EQ Leadership"])

    # === PERFORMANCE MANAGEMENT ===

    if "performance review" in title_lower or "performance evaluation" in title_lower:
        skill_level_sets.add("Performance Management")
        skills.extend(["Performance Reviews", "Conducting Evaluations"])

    if "performance management" in title_lower:
        skill_level_sets.add("Performance Management")
        skills.append("Performance Management Fundamentals")

    if "corrective counseling" in title_lower:
        skill_level_sets.add("Performance Management")
        skills.append("Corrective Counseling")

    # === PROJECT PLANNING & PRODUCTIVITY ===

    if "project planning" in title_lower or "planning and execution" in title_lower:
        skill_level_sets.add("Project Planning & Productivity")
        skills.append("Project Planning")

    if "time management" in title_lower:
        skill_level_sets.add("Project Planning & Productivity")
        skills.append("Time Management")

    if "time wasters" in title_lower:
        skill_level_sets.add("Project Planning & Productivity")
        skills.extend(["Time Management", "Productivity Improvement"])

    if "productivity" in title_lower:
        skill_level_sets.add("Project Planning & Productivity")
        skills.append("Productivity Improvement")
        if "on-site" in title_lower or "onsite" in title_lower:
            skills.append("Productivity Analysis")

    if "job plan" in title_lower:
        skill_level_sets.add("Construction Software")
        skills.append("Job Plan Fundamentals")
        if "theory" in title_lower:
            skills.append("Job Plan Analysis")

    # === CONSTRUCTION SOFTWARE ===

    if "accubid" in title_lower:
        skill_level_sets.add("Construction Software")
        skills.append("Accubid Fundamentals")
        if "advanced" in title_lower:
            skills.append("Accubid Data Export")

    if "viewpoint" in title_lower or "vista" in title_lower:
        skill_level_sets.add("Construction Software")
        skills.append("Vista")
        if "change order" in title_lower:
            skills.append("ViewPoint Change Orders")

    if "procore" in title_lower:
        skill_level_sets.add("Construction Software")
        skills.append("ProCore Fundamentals")
        if "setup" in title_lower or "job setup" in title_lower:
            skills.append("ProCore Job Setup")

    # === DOCUMENTATION ===

    if "documentation" in title_lower:
        skill_level_sets.add("Documentation & Compliance")
        skills.append("Documentation Practices")
        if "reporting" in title_lower:
            skills.append("Documentation & Reporting")

    if "document management" in title_lower:
        skill_level_sets.add("Documentation & Compliance")
        skills.append("Documentation Practices")

    # === PROFESSIONAL DEVELOPMENT ===

    if "presenting" in title_lower or "presentation" in title_lower:
        skill_level_sets.add("Professional Development")
        skills.append("Presentation Skills")

    # === FIELD OPERATIONS ===

    if "jobsite efficiency" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Jobsite Efficiency")

    if "coordinating" in title_lower and "trade" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Trade Coordination")

    if "quality control" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Quality Control")

    if "manpower projection" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Manpower Projection")

    if "job closeout" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Job Closeout")

    if "tool" in title_lower and "technology" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Tool & Equipment Management")

    # === HR / POLICY ===

    if "harassment" in title_lower or "discrimination" in title_lower or "retaliation" in title_lower:
        skill_level_sets.add("Documentation & Compliance")
        skills.append("Documentation & Compliance")
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Leadership Fundamentals")

    if "fmla" in title_lower:
        skill_level_sets.add("Documentation & Compliance")
        skills.append("Documentation & Compliance")

    if "substance abuse" in title_lower:
        skill_level_sets.add("Safety")
        skills.append("Safety Awareness & Culture")
        skill_level_sets.add("Documentation & Compliance")
        skills.append("Documentation & Compliance")

    if "eap" in title_lower or "employee assistance" in title_lower or "mental health" in title_lower:
        skill_level_sets.add("Leadership & Field Management")
        skills.append("Team Morale")

    if "nevada" in title_lower and "rights" in title_lower:
        skill_level_sets.add("Safety")
        skills.append("Safety Awareness & Culture")

    # === INSPECTIONS ===

    if "inspection" in title_lower:
        if "safety" in title_lower:
            skill_level_sets.add("Safety")
            skills.append("Safety Inspections")
        if "osha" in title_lower or "msha" in title_lower:
            skill_level_sets.add("Documentation & Compliance")
            skills.append("Regulatory Inspections")
        if "pre-task" in title_lower:
            skill_level_sets.add("Safety")
            skills.append("Pre-Task Safety Planning")

    # === FALLBACK: Use existing category ===
    if not skills:
        if existing_category:
            skill_level_sets.add(existing_category)
            # Add first few skills from that category
            if existing_category in SKILL_FRAMEWORK:
                skills.extend(SKILL_FRAMEWORK[existing_category][:2])

    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in skills:
        if skill not in seen:
            seen.add(skill)
            unique_skills.append(skill)

    return list(skill_level_sets), unique_skills


# Course description templates (shortened version - full templates would be here)
DESCRIPTION_TEMPLATES = {
    "extreme_ownership": {
        "short": "Learn the core principles of Extreme Ownership from Navy SEAL leadership methodology. This course teaches how leaders must own everything in their world—taking full responsibility for outcomes, team performance, and mission success while eliminating excuses and blame.",
        "long": """Learn the core principles of Extreme Ownership from Navy SEAL leadership methodology. This course teaches how leaders must own everything in their world—taking full responsibility for outcomes, team performance, and mission success while eliminating excuses and blame.

Based on battle-tested principles, this training emphasizes that there are no bad teams, only bad leaders. You'll learn to check your ego, take responsibility for failures, and empower your team to succeed.

Key Learning Objectives:
1. Take complete ownership of your team's performance and outcomes
2. Eliminate blame and excuses from your leadership approach
3. Build trust through accountability and transparent communication
4. Empower subordinates to make decisions within their scope
5. Lead up and down the chain of command effectively
6. Prioritize and execute under pressure
7. Apply decentralized command principles to your work environment

This mindset shift transforms how you approach challenges, turning obstacles into opportunities for growth and improvement.""",
        "tags": ["leadership", "accountability", "ownership", "team management", "navy seal", "decision making", "responsibility"]
    },
    "values_driven": {
        "short": "Through real-life stories, proven strategies, and decades of experience, Coach K teaches how to lead with trust, respect, communication, and responsibility. He emphasizes that successful leaders don't just focus on results—they build strong relationships, empower individuals, and create cultures where every person matters.",
        "long": """Through real-life stories, proven strategies, and decades of experience, Coach K teaches how to lead with trust, respect, communication, and responsibility. He emphasizes that successful leaders don't just focus on results—they build strong relationships, empower individuals, and create cultures where every person matters.

This course is not just about coaching or sports—it's about how to lead people effectively in any environment. Whether you're managing a team in the field or guiding a department in the office, you'll learn to build unity, drive purpose, and lead with integrity.

This chapter highlights the importance of relationships, empowerment, and accountability in fostering a positive and effective team culture.

Key Learning Objectives:
1. Lead with integrity. Build trust and respect within your team to create a strong foundation.
2. Empower individuals. Encourage team members to take initiative and contribute meaningfully.
3. Cultivate relationships. Prioritize connections to foster a supportive and collaborative environment.
4. Define core values. Understanding and aligning actions with values strengthens leadership.
5. Foster accountability. Promote an ownership mindset to enhance trust and reliability.
6. Drive purpose. Ensure every team member understands their role and its significance.
7. Lead with empathy. Support your team during challenges to build resilience and trust.""",
        "tags": ["leadership", "values", "coaching", "team building", "motivation", "culture", "relationships", "Coach K"]
    },
    "lockout_tagout": {
        "short": "Master critical lockout/tagout procedures to protect yourself and coworkers from hazardous energy. This course covers proper isolation techniques, verification methods, and regulatory requirements essential for electrical safety in construction and industrial environments.",
        "long": """Master critical lockout/tagout procedures to protect yourself and coworkers from hazardous energy. This course covers proper isolation techniques, verification methods, and regulatory requirements essential for electrical safety in construction and industrial environments.

Lockout/Tagout (LOTO) procedures are among the most important safety protocols in electrical work. Failure to properly control hazardous energy results in serious injuries and fatalities every year.

Key Learning Objectives:
1. Understand types of hazardous energy and their dangers
2. Apply proper lockout/tagout procedures step-by-step
3. Verify de-energized conditions before beginning work
4. Coordinate with multiple workers and energy sources
5. Handle complex LOTO scenarios with multiple isolation points
6. Follow abnormal lockout removal procedures safely
7. Return equipment to service properly after maintenance

Completing this training demonstrates your commitment to safety and prepares you to work safely on energized systems.""",
        "tags": ["safety", "lockout tagout", "LOTO", "electrical safety", "OSHA", "hazardous energy", "de-energization"]
    },
    "default": {
        "short": "Build essential construction industry skills through this comprehensive training module. This course provides practical knowledge and techniques that can be immediately applied to improve your effectiveness in field operations.",
        "long": """Build essential construction industry skills through this comprehensive training module. This course provides practical knowledge and techniques that can be immediately applied to improve your effectiveness in field operations.

Construction industry training combines technical knowledge with practical application. This module addresses key competencies needed for success in today's construction environment.

Key Learning Objectives:
1. Understand core concepts and best practices
2. Apply knowledge to real-world situations
3. Develop skills that improve performance
4. Build competency through practical application
5. Meet industry standards and requirements
6. Contribute to team and project success
7. Continue professional development

Complete this training to enhance your capabilities and advance your construction career.""",
        "tags": ["construction", "training", "professional development", "skills"]
    }
}


def get_template_key(title, category):
    """Determine which template to use based on title and category"""
    title_lower = title.lower()

    if "extreme ownership" in title_lower:
        return "extreme_ownership"
    elif "values" in title_lower and ("driven" in title_lower or "coach k" in title_lower):
        return "values_driven"
    elif "lockout" in title_lower or "tagout" in title_lower:
        return "lockout_tagout"
    else:
        return "default"


def generate_short_description(title, template_key):
    """Generate a short description (50-75 words)"""
    if template_key in DESCRIPTION_TEMPLATES:
        return DESCRIPTION_TEMPLATES[template_key]["short"]
    return DESCRIPTION_TEMPLATES["default"]["short"]


def generate_long_description(title, template_key):
    """Generate a long description (200-250 words)"""
    if template_key in DESCRIPTION_TEMPLATES:
        return DESCRIPTION_TEMPLATES[template_key]["long"]
    return DESCRIPTION_TEMPLATES["default"]["long"]


def generate_tags(title, category, skill_level_sets, skills):
    """Generate search tags from skills and categories"""
    tags = set()

    # Add skill level sets
    for sls in skill_level_sets:
        tags.add(sls.lower())

    # Add skills (shortened for tags)
    for skill in skills:
        tags.add(skill.lower())

    # Add category
    if category:
        tags.add(category.lower())

    return list(tags)[:15]  # Limit to 15 tags


def process_catalog(input_csv, output_xlsx):
    """Process the catalog and generate descriptions with skills"""

    # Read existing catalog
    courses = []
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('title'):
                courses.append(row)

    print(f"Processing {len(courses)} courses...")

    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Course Catalog"

    # Define headers
    headers = [
        "Course ID", "Filename", "Title",
        "Short Description", "Long Description",
        "Primary Category", "Sub Category",
        "Skill Level Sets", "Skills",
        "Proficiency Level",
        "Series Name", "Series Order",
        "Tags"
    ]

    # Style headers
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # Process each course
    for idx, course in enumerate(courses, 2):
        title = course.get('title', '')
        existing_category = course.get('skill_level_set', '')

        # Get skills for this course
        skill_level_sets, skills = get_skills_for_course(title, existing_category)

        # Determine template
        template_key = get_template_key(title, existing_category)

        # Generate descriptions
        short_desc = generate_short_description(title, template_key)
        long_desc = generate_long_description(title, template_key)

        # Generate tags
        tags = generate_tags(title, existing_category, skill_level_sets, skills)

        # Primary/Sub category
        primary_cat = skill_level_sets[0] if skill_level_sets else existing_category
        sub_cat = existing_category

        # Write row
        row_data = [
            course.get('course_id', ''),
            course.get('filename', ''),
            title,
            short_desc,
            long_desc,
            primary_cat,
            sub_cat,
            "; ".join(skill_level_sets),  # Multiple skill level sets
            "; ".join(skills),             # Multiple skills
            course.get('proficiency_level', ''),
            course.get('series_name', ''),
            course.get('series_order', ''),
            ", ".join(tags)
        ]

        for col, value in enumerate(row_data, 1):
            cell = ws.cell(row=idx, column=col, value=value)
            cell.border = thin_border
            cell.alignment = Alignment(vertical='top', wrap_text=True)

    # Adjust column widths
    column_widths = [15, 40, 40, 60, 100, 25, 25, 40, 60, 15, 30, 10, 50]
    for col, width in enumerate(column_widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = width

    # Freeze top row
    ws.freeze_panes = 'A2'

    # Save workbook
    wb.save(output_xlsx)
    print(f"Created: {output_xlsx}")
    print(f"Total courses processed: {len(courses)}")

    # Print skill statistics
    all_skills = set()
    all_sls = set()
    for course in courses:
        title = course.get('title', '')
        existing_cat = course.get('skill_level_set', '')
        sls_list, skill_list = get_skills_for_course(title, existing_cat)
        all_skills.update(skill_list)
        all_sls.update(sls_list)

    print(f"Unique Skill Level Sets used: {len(all_sls)}")
    print(f"Unique Skills assigned: {len(all_skills)}")

    return len(courses)


if __name__ == "__main__":
    input_file = r"C:\Users\tewing\Documents\Projects\GSL-Operations-Framework\deliverables\scorm-catalog\SCORM_COURSE_CATALOG.csv"
    output_file = r"C:\Users\tewing\Desktop\Claude Projects\SOPs For Review\SCORM_Course_Descriptions.xlsx"

    process_catalog(input_file, output_file)
