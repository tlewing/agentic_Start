"""
Create Learn365 Skills Matrix Excel
Similar structure to Key_SOP_Matrix.xlsx
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
from datetime import datetime

# Create workbook
wb = openpyxl.Workbook()

# Styles
header_font = Font(bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
alt_fill = PatternFill(start_color="D9E2F3", end_color="D9E2F3", fill_type="solid")
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

def style_header(ws, row=1):
    for cell in ws[row]:
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center', wrap_text=True)

def auto_width(ws):
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column].width = adjusted_width

# ============================================================
# Sheet 1: Skills_Metadata (like GSL_SOP_Metadata)
# ============================================================
ws1 = wb.active
ws1.title = "Skills_Metadata"

headers = [
    "Skill ID", "Skill Title", "Category", "Category ID", "Scale Set",
    "Scale Set ID", "Proficiency Levels", "Description", "Roles (Target)",
    "Primary Role", "Course Count", "Status", "Created Date", "Modified Date",
    "API Created", "Notes"
]
ws1.append(headers)
style_header(ws1)

# Skills data (from our framework)
SKILLS_DATA = [
    # Safety Skills
    ("SKL-001", "Safety Awareness & Culture", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Understanding of safety culture and awareness principles", "All Roles", "Field Employee", 5, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-002", "Accident Prevention", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Techniques for preventing workplace accidents", "All Roles", "Foreman", 3, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-003", "Hazard Recognition", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Identifying workplace hazards before they cause harm", "All Roles", "Foreman", 4, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-004", "Pre-Task Safety Planning", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Planning safety measures before starting work", "Field Roles", "Foreman", 2, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-005", "Safety Inspections", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Conducting workplace safety inspections", "FL, GS", "Foreman", 3, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-006", "Incident Investigation", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Investigating safety incidents and near misses", "FL, GS, PM", "Safety Coordinator", 2, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-007", "First Aid/CPR/AED", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Emergency first aid and life-saving techniques", "All Roles", "All", 2, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-008", "Emergency Response", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Responding to workplace emergencies", "All Roles", "Foreman", 3, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-009", "NFPA 70E Fundamentals", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Electrical safety standards and requirements", "Electrical Roles", "Journeyman", 4, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-010", "Arc Flash Awareness", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Understanding arc flash hazards and protection", "Electrical Roles", "Journeyman", 3, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
    ("SKL-011", "LOTO Fundamentals", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Lockout/Tagout procedures and requirements", "Electrical Roles", "Journeyman", 5, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-012", "Fall Hazard Recognition", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Identifying and mitigating fall hazards", "Field Roles", "Foreman", 4, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-013", "Ladder Safety", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Safe ladder selection and use", "Field Roles", "All Field", 2, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-014", "Scaffold Fundamentals", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Scaffold safety and inspection requirements", "Field Roles", "Foreman", 3, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-015", "HazCom Program Fundamentals", "Safety", "CAT-01", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Hazard communication program requirements", "All Roles", "All", 2, "Active", "2026-01-17", "2026-01-17", "Yes", ""),

    # Lean Construction Skills
    ("SKL-020", "Lean Fundamentals", "Lean Construction", "CAT-02", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Core principles of lean construction", "FL, GS, PM, BM", "Foreman", 4, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
    ("SKL-021", "Lean History", "Lean Construction", "CAT-02", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "History and evolution of lean principles", "FL, GS, PM, BM", "All", 2, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-022", "Eight Wastes Recognition", "Lean Construction", "CAT-02", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Identifying the eight wastes in construction", "FL, GS, PM, BM", "Foreman", 3, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-023", "Continuous Improvement", "Lean Construction", "CAT-02", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Implementing continuous improvement processes", "FL, GS, PM, BM", "Superintendent", 3, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
    ("SKL-024", "Pull Planning", "Lean Construction", "CAT-02", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Collaborative pull planning techniques", "FL, GS, PM", "Superintendent", 2, "Active", "2026-01-17", "2026-01-17", "Yes", ""),

    # Leadership & Field Management Skills
    ("SKL-030", "Foreman Role & Responsibilities", "Leadership & Field Management", "CAT-03", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Understanding foreman duties and expectations", "FL", "Foreman", 8, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-031", "Field Supervision", "Leadership & Field Management", "CAT-03", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Supervising field crews effectively", "FL, GS", "Foreman", 5, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-032", "Crew Planning", "Leadership & Field Management", "CAT-03", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Planning crew assignments and workload", "FL, GS", "Foreman", 4, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-033", "Leadership Fundamentals", "Leadership & Field Management", "CAT-03", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Core leadership principles and practices", "FL, GS, PM, BM", "Foreman", 10, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-034", "Values-Driven Leadership", "Leadership & Field Management", "CAT-03", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Leading with organizational values", "FL, GS, PM, BM", "Superintendent", 17, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-035", "Accountability & Ownership", "Leadership & Field Management", "CAT-03", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Taking ownership and accountability", "FL, GS, PM, BM", "All Leaders", 5, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-036", "Team Building", "Leadership & Field Management", "CAT-03", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Building effective teams", "FL, GS, PM, BM", "Superintendent", 4, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-037", "Extreme Ownership", "Leadership & Field Management", "CAT-03", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Taking full responsibility for outcomes", "FL, GS, PM, BM", "Superintendent", 3, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),

    # Communication & Coaching Skills
    ("SKL-040", "Effective Communication", "Communication & Coaching", "CAT-04", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Clear and effective communication skills", "All Roles", "All", 5, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
    ("SKL-041", "Building Relationships", "Communication & Coaching", "CAT-04", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Developing professional relationships", "All Roles", "All Leaders", 3, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
    ("SKL-042", "Conflict Resolution", "Communication & Coaching", "CAT-04", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Resolving workplace conflicts", "FL, GS, PM, BM", "Superintendent", 2, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
    ("SKL-043", "Handling Resistance", "Communication & Coaching", "CAT-04", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Managing resistance to change", "FL, GS, PM, BM", "Superintendent", 2, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),

    # Emotional Intelligence Skills
    ("SKL-050", "EQ Fundamentals", "Emotional Intelligence", "CAT-05", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Understanding emotional intelligence basics", "All Roles", "All", 3, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
    ("SKL-051", "Self-Awareness", "Emotional Intelligence", "CAT-05", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Developing self-awareness skills", "All Roles", "All Leaders", 2, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
    ("SKL-052", "Empathy", "Emotional Intelligence", "CAT-05", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Understanding and relating to others", "All Roles", "All Leaders", 2, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
    ("SKL-053", "EQ Leadership", "Emotional Intelligence", "CAT-05", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Leading with emotional intelligence", "FL, GS, PM, BM", "Superintendent", 2, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
    ("SKL-054", "Trust Building", "Emotional Intelligence", "CAT-05", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Building trust in teams", "FL, GS, PM, BM", "Superintendent", 2, "Active", "2026-01-17", "2026-01-17", "Yes", ""),

    # Performance Management Skills
    ("SKL-060", "Performance Management Fundamentals", "Performance Management", "CAT-06", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Core performance management principles", "FL, GS, PM, BM", "Superintendent", 3, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-061", "Conducting Evaluations", "Performance Management", "CAT-06", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Conducting employee evaluations", "FL, GS, PM, BM", "Superintendent", 2, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
    ("SKL-062", "Performance Reviews", "Performance Management", "CAT-06", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Delivering effective performance reviews", "FL, GS, PM, BM", "Superintendent", 2, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-063", "Corrective Counseling", "Performance Management", "CAT-06", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Corrective counseling and discipline", "FL, GS, PM, BM", "Superintendent", 2, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
    ("SKL-064", "Career Development", "Performance Management", "CAT-06", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Supporting employee career growth", "FL, GS, PM, BM", "Superintendent", 2, "Active", "2026-01-17", "2026-01-17", "Yes", ""),

    # Construction Software Skills
    ("SKL-070", "Accubid Fundamentals", "Construction Software", "CAT-07", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Basic Accubid estimating software skills", "EST, PM", "Estimator", 4, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-071", "ViewPoint Change Orders", "Construction Software", "CAT-07", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Managing change orders in ViewPoint", "PM, CM", "Project Manager", 3, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-072", "ProCore Fundamentals", "Construction Software", "CAT-07", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Basic ProCore project management skills", "PM, GS", "Project Manager", 2, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-073", "Job Plan Fundamentals", "Construction Software", "CAT-07", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Understanding job plan basics", "FL, GS, PM", "Foreman", 3, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-074", "Excel Skills", "Construction Software", "CAT-07", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Microsoft Excel proficiency", "All Office", "All", 2, "Active", "2026-01-17", "2026-01-17", "Yes", ""),

    # Project Planning & Productivity Skills
    ("SKL-080", "Project Planning", "Project Planning & Productivity", "CAT-08", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Project planning fundamentals", "FL, GS, PM", "Project Manager", 5, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-081", "Scheduling Techniques", "Project Planning & Productivity", "CAT-08", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Construction scheduling methods", "FL, GS, PM", "Project Manager", 4, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
    ("SKL-082", "Productivity Analysis", "Project Planning & Productivity", "CAT-08", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Analyzing and improving productivity", "FL, GS, PM", "Superintendent", 3, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-083", "Time Management", "Project Planning & Productivity", "CAT-08", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Personal time management skills", "All Roles", "All", 2, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),

    # Documentation & Compliance Skills
    ("SKL-090", "Documentation Practices", "Documentation & Compliance", "CAT-09", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Proper documentation practices", "All Roles", "All", 3, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
    ("SKL-091", "Regulatory Inspections", "Documentation & Compliance", "CAT-09", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Managing regulatory inspections", "FL, GS, PM", "Superintendent", 2, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),

    # Professional Development Skills
    ("SKL-100", "Presentation Skills", "Professional Development", "CAT-10", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Effective presentation techniques", "GS, PM, BM", "Branch Manager", 6, "Active", "2026-01-17", "2026-01-17", "Yes", ""),
    ("SKL-101", "Strategic Thinking", "Professional Development", "CAT-10", "GSL Proficiency Scale", "c7b1796f-3716-49fb-86dc-edf176b017dc", "1-5", "Strategic thinking and planning", "GS, PM, BM", "Branch Manager", 2, "Active", "2026-01-17", "2026-01-17", "Yes", "Existed"),
]

for row in SKILLS_DATA:
    ws1.append(row)

auto_width(ws1)

# ============================================================
# Sheet 2: Categories (like Sheet2)
# ============================================================
ws2 = wb.create_sheet("Categories")

ws2.append(["Category ID", "Category Name", "Description", "Skill Count", "Primary Roles", "Learn365 ID"])
style_header(ws2)

CATEGORIES = [
    ("CAT-01", "Safety", "Safety awareness, hazard recognition, and compliance", 40, "All Roles", "New"),
    ("CAT-02", "Lean Construction", "Lean principles and continuous improvement", 12, "FL, GS, PM, BM", "New"),
    ("CAT-03", "Leadership & Field Management", "Leadership skills and field supervision", 20, "FL, GS, PM, BM", "New"),
    ("CAT-04", "Communication & Coaching", "Communication, coaching, and mentoring", 8, "All Roles", "New"),
    ("CAT-05", "Emotional Intelligence", "EQ skills and social awareness", 7, "All Roles", "New"),
    ("CAT-06", "Performance Management", "Employee performance and development", 7, "FL, GS, PM, BM", "New"),
    ("CAT-07", "Construction Software", "Software tools for construction", 14, "EST, PM, FL", "New"),
    ("CAT-08", "Project Planning & Productivity", "Planning and productivity skills", 8, "FL, GS, PM", "New"),
    ("CAT-09", "Documentation & Compliance", "Documentation and regulatory compliance", 4, "All Roles", "New"),
    ("CAT-10", "Professional Development", "Career and professional growth", 3, "GS, PM, BM", "New"),
]

for row in CATEGORIES:
    ws2.append(row)

auto_width(ws2)

# ============================================================
# Sheet 3: Coverage Matrix (Skills to Courses)
# ============================================================
ws3 = wb.create_sheet("Coverage Matrix")

ws3.append(["Skill Title", "Course Title", "Course Type", "Proficiency Level", "Coverage Status", "Gap Recommendation", "Category"])
style_header(ws3)

COVERAGE = [
    ("Safety Awareness & Culture", "New Hire Safety Orientation", "SCORM", "Basic", "Covered", "", "Safety"),
    ("Safety Awareness & Culture", "OSHA Focus Four Hazards", "SCORM", "Basic", "Covered", "", "Safety"),
    ("Hazard Recognition", "Hazard Recognition Training", "SCORM", "Intermediate", "Covered", "", "Safety"),
    ("NFPA 70E Fundamentals", "Safe Electrical Work Practices 2024 NFPA 70E", "SCORM", "Proficient", "Covered", "", "Safety"),
    ("Arc Flash Awareness", "Arc Flash Risk Assessment", "SCORM", "Intermediate", "Covered", "", "Safety"),
    ("LOTO Fundamentals", "Lockout Tagout Series", "SCORM", "Proficient", "Covered", "", "Safety"),
    ("Fall Hazard Recognition", "Fall Protection Training", "SCORM", "Intermediate", "Covered", "", "Safety"),
    ("Scaffold Fundamentals", "Scaffolding Safety Series", "SCORM", "Basic", "Covered", "", "Safety"),
    ("Lean Fundamentals", "What is LEAN", "SCORM", "Awareness", "Covered", "", "Lean Construction"),
    ("Lean Fundamentals", "Chapter 05 - What is Lean?", "SCORM", "Basic", "Covered", "", "Lean Construction"),
    ("Eight Wastes Recognition", "The Eight Wastes of Construction", "SCORM", "Basic", "Covered", "", "Lean Construction"),
    ("Continuous Improvement", "Continuous Improvement Chapters", "SCORM", "Intermediate", "Covered", "", "Lean Construction"),
    ("Leadership Fundamentals", "Introduction to Field Leadership (1-4)", "SCORM", "Proficient", "Covered", "", "Leadership & Field Management"),
    ("Values-Driven Leadership", "Values Driven Leadership Series (1-17)", "SCORM", "Proficient", "Covered", "", "Leadership & Field Management"),
    ("Foreman Role & Responsibilities", "Roles and Responsibilities of a Foreman", "SCORM", "Proficient", "Covered", "", "Leadership & Field Management"),
    ("Extreme Ownership", "Extreme Ownership Training", "SCORM", "Intermediate", "Covered", "", "Leadership & Field Management"),
    ("Effective Communication", "Chapter 8 Introduction to Effective Communication", "SCORM", "Basic", "Covered", "", "Communication & Coaching"),
    ("Conflict Resolution", "Conflict Resolution Training", "SCORM", "Intermediate", "Partial", "Add advanced scenarios", "Communication & Coaching"),
    ("EQ Fundamentals", "What Is Emotional Intelligence?", "SCORM", "Awareness", "Covered", "", "Emotional Intelligence"),
    ("Self-Awareness", "Improving Self-Awareness", "SCORM", "Basic", "Covered", "", "Emotional Intelligence"),
    ("Empathy", "Developing Empathy", "SCORM", "Basic", "Covered", "", "Emotional Intelligence"),
    ("EQ Leadership", "Leading With Emotional Intelligence", "SCORM", "Intermediate", "Covered", "", "Emotional Intelligence"),
    ("Performance Reviews", "Conducting Effective Performance Reviews", "SCORM", "Basic", "Covered", "", "Performance Management"),
    ("Corrective Counseling", "Corrective Counseling and Performance Reviews", "SCORM", "Basic", "Covered", "", "Performance Management"),
    ("Accubid Fundamentals", "Accubid Learning Series", "SCORM", "Basic", "Covered", "", "Construction Software"),
    ("ViewPoint Change Orders", "ViewPoint Change Order Courses", "SCORM", "Basic", "Covered", "", "Construction Software"),
    ("Job Plan Fundamentals", "Chapter 1 Job Plan Theory", "SCORM", "Basic", "Covered", "", "Construction Software"),
    ("Project Planning", "Project Planning Chapters", "SCORM", "Intermediate", "Covered", "", "Project Planning & Productivity"),
    ("Productivity Analysis", "On-Site Productivity", "SCORM", "Basic", "Covered", "", "Project Planning & Productivity"),
    ("Time Management", "Chapter 9 Time Management", "SCORM", "Basic", "Covered", "", "Project Planning & Productivity"),
    ("Documentation Practices", "Chapter 7 Introduction to Documentation", "SCORM", "Awareness", "Covered", "", "Documentation & Compliance"),
    ("Presentation Skills", "The Art of Presenting Series (1-6)", "SCORM", "Intermediate", "Covered", "", "Professional Development"),
]

for row in COVERAGE:
    ws3.append(row)

auto_width(ws3)

# ============================================================
# Sheet 4: RACI Matrix (Skills to Roles)
# ============================================================
ws4 = wb.create_sheet("RACI Matrix")

ws4.append(["Skill Title", "Category", "FE", "FL", "GS", "PM", "BM", "EST", "CM", "PUR"])
style_header(ws4)

RACI = [
    ("Safety Awareness & Culture", "Safety", "R", "A/R", "A", "C", "C", "I", "I", "I"),
    ("Hazard Recognition", "Safety", "R", "A/R", "A", "C", "C", "I", "I", "I"),
    ("NFPA 70E Fundamentals", "Safety", "R", "A/R", "A", "C", "I", "-", "-", "-"),
    ("Arc Flash Awareness", "Safety", "R", "A/R", "A", "C", "I", "-", "-", "-"),
    ("LOTO Fundamentals", "Safety", "R", "A/R", "A", "C", "I", "-", "-", "-"),
    ("Fall Hazard Recognition", "Safety", "R", "A/R", "A", "C", "I", "-", "-", "-"),
    ("Lean Fundamentals", "Lean Construction", "I", "R", "A/R", "R", "A", "I", "I", "-"),
    ("Eight Wastes Recognition", "Lean Construction", "I", "R", "A/R", "R", "A", "I", "I", "-"),
    ("Pull Planning", "Lean Construction", "-", "R", "A/R", "R", "A", "-", "-", "-"),
    ("Leadership Fundamentals", "Leadership & Field Management", "-", "R", "A/R", "R", "A", "-", "-", "-"),
    ("Values-Driven Leadership", "Leadership & Field Management", "-", "R", "A/R", "R", "A", "-", "-", "-"),
    ("Foreman Role & Responsibilities", "Leadership & Field Management", "-", "A/R", "A", "C", "I", "-", "-", "-"),
    ("Extreme Ownership", "Leadership & Field Management", "-", "R", "A/R", "R", "A", "-", "-", "-"),
    ("Effective Communication", "Communication & Coaching", "I", "R", "A/R", "R", "A", "I", "R", "I"),
    ("Conflict Resolution", "Communication & Coaching", "-", "R", "A/R", "R", "A", "-", "R", "-"),
    ("EQ Fundamentals", "Emotional Intelligence", "I", "R", "A/R", "R", "A", "I", "I", "I"),
    ("EQ Leadership", "Emotional Intelligence", "-", "R", "A/R", "R", "A", "-", "-", "-"),
    ("Performance Reviews", "Performance Management", "-", "R", "A/R", "R", "A", "-", "-", "-"),
    ("Corrective Counseling", "Performance Management", "-", "R", "A/R", "R", "A", "-", "-", "-"),
    ("Accubid Fundamentals", "Construction Software", "-", "-", "-", "C", "I", "A/R", "-", "-"),
    ("ViewPoint Change Orders", "Construction Software", "-", "-", "-", "A/R", "C", "C", "R", "-"),
    ("Job Plan Fundamentals", "Construction Software", "-", "R", "A/R", "A", "C", "-", "-", "-"),
    ("Project Planning", "Project Planning & Productivity", "-", "R", "A/R", "A/R", "A", "C", "C", "-"),
    ("Productivity Analysis", "Project Planning & Productivity", "-", "R", "A/R", "R", "A", "-", "-", "-"),
    ("Documentation Practices", "Documentation & Compliance", "I", "R", "A/R", "A/R", "C", "I", "A/R", "R"),
    ("Presentation Skills", "Professional Development", "-", "I", "R", "R", "A/R", "I", "I", "I"),
]

for row in RACI:
    ws4.append(row)

# Add legend
ws4.append([])
ws4.append(["Legend:", "R = Responsible", "A = Accountable", "C = Consulted", "I = Informed", "- = Not Applicable"])

auto_width(ws4)

# ============================================================
# Sheet 5: Training Gaps (like Redline Recs)
# ============================================================
ws5 = wb.create_sheet("Training Gaps")

ws5.append(["Skill Title", "Gap Description", "Priority", "Current Coverage", "Recommendation", "Status"])
style_header(ws5)

GAPS = [
    ("Large Feeder Wire Management", "No dedicated training for large feeder wire procedures", "High", "0%", "Created Tab 41 training module", "Closed"),
    ("Prefabrication Operations", "Minimal prefab training content", "High", "25%", "Expanded Tab 42 training module", "Closed"),
    ("Contract Review", "Limited contract review training", "Medium", "30%", "Created Tab 2 training module", "Closed"),
    ("RFI Management", "No dedicated RFI training", "Medium", "10%", "Created Tab 22 training module", "Closed"),
    ("BIM Coordination", "Limited BIM training for field", "Low", "20%", "Consider adding BIM basics course", "Open"),
    ("Commissioning Procedures", "Commissioning training minimal", "Low", "15%", "Review commissioning requirements", "Open"),
]

for row in GAPS:
    ws5.append(row)

auto_width(ws5)

# ============================================================
# Sheet 6: Conflict Matrix
# ============================================================
ws6 = wb.create_sheet("Conflict Matrix")

ws6.append(["Item", "Conflict Description", "Conflict Type", "Resolution"])
style_header(ws6)

CONFLICTS = [
    ("Skills vs Competencies", "Learn365 has separate Skills and Competencies APIs", "Architecture", "Use Skills for role targeting, Competencies for course completion"),
    ("Duplicate Skill Names", "67 skills already existed with same titles", "Data", "Migrated existing skills to new categories"),
    ("Scale Set Levels", "API doesn't persist scale set levels", "API Limitation", "Configure levels in Learn365 UI"),
    ("Old Categories", "100 old categories can't be deleted (in use)", "Data", "Created new categories alongside old ones"),
    ("SCORM Duplicates", "71 duplicate SCORM courses identified", "Data", "Documented in DUPLICATE_COURSES.csv"),
]

for row in CONFLICTS:
    ws6.append(row)

auto_width(ws6)

# ============================================================
# Sheet 7: Role Checklist (like Closeout Checklist)
# ============================================================
ws7 = wb.create_sheet("Role Checklist")

ws7.append(["Role", "Required Skill Set", "Min Level", "Est. Courses", "Est. Hours", "Target Skill Created"])
style_header(ws7)

ROLES = [
    ("Field Employee (FE)", "Safety, Lean (Awareness), Communication (Awareness), EQ (Awareness)", "Basic", "6-8", "4-6", "Pending"),
    ("Field Leadership (FL)", "Safety (Proficient), Lean (Basic), Leadership (Proficient), All others (Basic)", "Proficient", "35-45", "25-35", "Pending"),
    ("General Superintendent (GS)", "All skills at Proficient/Expert level", "Expert", "80-100", "60-80", "Pending"),
    ("Project Manager (PM)", "Software (Proficient), Planning (Proficient), Leadership (Basic)", "Proficient", "40-50", "30-40", "Pending"),
    ("Branch Manager (BM)", "Leadership (Proficient), Lean (Proficient), EQ (Proficient)", "Proficient", "60-75", "45-60", "Pending"),
    ("Estimator (EST)", "Software (Proficient), Planning (Basic)", "Proficient", "15-20", "10-15", "Pending"),
    ("Contract Manager (CM)", "Documentation (Proficient), Communication (Basic)", "Proficient", "12-18", "8-12", "Pending"),
    ("Purchasing (PUR)", "Documentation (Basic), Software (Basic)", "Basic", "10-15", "6-10", "Pending"),
]

for row in ROLES:
    ws7.append(row)

auto_width(ws7)

# ============================================================
# Sheet 8: Role Alignment Matrix (Skills x Roles)
# ============================================================
ws8 = wb.create_sheet("Role Alignment Matrix")

ws8.append(["Skill Level Set", "FE", "FL", "GS", "PM", "BM", "EST", "CM", "PUR"])
style_header(ws8)

ALIGNMENT = [
    ("1. Safety", "B", "P", "P", "B", "B", "A", "A", "A"),
    ("2. Lean Construction", "A", "B", "P", "B", "P", "A", "A", "-"),
    ("3. Leadership & Field Management", "-", "P", "E", "B", "P", "-", "-", "-"),
    ("4. Communication & Coaching", "A", "B", "P", "B", "P", "A", "B", "A"),
    ("5. Emotional Intelligence", "A", "B", "P", "B", "P", "A", "A", "A"),
    ("6. Performance Management", "-", "B", "P", "B", "P", "-", "-", "-"),
    ("7. Construction Software", "-", "B", "B", "P", "B", "P", "B", "B"),
    ("8. Project Planning & Productivity", "A", "B", "P", "P", "P", "B", "B", "A"),
    ("9. Documentation & Compliance", "A", "B", "P", "P", "B", "A", "P", "B"),
    ("10. Professional Development", "-", "A", "B", "B", "P", "A", "A", "A"),
]

for row in ALIGNMENT:
    ws8.append(row)

ws8.append([])
ws8.append(["Legend:", "A = Awareness", "B = Basic", "P = Proficient", "E = Expert", "- = Not Required"])

auto_width(ws8)

# ============================================================
# Sheet 9: Number Crosswalk (Old to New)
# ============================================================
ws9 = wb.create_sheet("Skills Crosswalk")

ws9.append(["Old Skill Name", "New Skill Name", "Old Category", "New Category", "Action", "Notes"])
style_header(ws9)

CROSSWALK = [
    ("Effective Communication", "Effective Communication", "Communication Skills", "Communication & Coaching", "Migrated", "Updated category"),
    ("Building Relationships", "Building Relationships", "Communication Skills", "Communication & Coaching", "Migrated", "Updated category"),
    ("Lean Fundamentals", "Lean Fundamentals", "Lean Skills", "Lean Construction", "Migrated", "Updated category"),
    ("Continuous Improvement", "Continuous Improvement", "Lean Skills", "Lean Construction", "Migrated", "Updated category"),
    ("EQ Fundamentals", "EQ Fundamentals", "Emotional Intelligence Skills", "Emotional Intelligence", "Migrated", "Updated category"),
    ("Self-Awareness", "Self-Awareness", "Personal Competence", "Emotional Intelligence", "Migrated", "Updated category"),
    ("Extreme Ownership", "Extreme Ownership", "Leadership Skills", "Leadership & Field Management", "Migrated", "Updated category"),
    ("Strategic Thinking", "Strategic Thinking", "Strategic Thinking", "Professional Development", "Migrated", "Updated category"),
    ("Documentation Practices", "Documentation Practices", "Documentation Skills", "Documentation & Compliance", "Migrated", "Updated category"),
    ("Regulatory Inspections", "Regulatory Inspections", "Regulatory Skills", "Documentation & Compliance", "Migrated", "Updated category"),
    ("(New)", "Safety Awareness & Culture", "-", "Safety", "Created", "New skill"),
    ("(New)", "Hazard Recognition", "-", "Safety", "Created", "New skill"),
    ("(New)", "Leadership Fundamentals", "-", "Leadership & Field Management", "Created", "New skill"),
    ("(New)", "Values-Driven Leadership", "-", "Leadership & Field Management", "Created", "New skill"),
]

for row in CROSSWALK:
    ws9.append(row)

auto_width(ws9)

# ============================================================
# Sheet 10: Change Log
# ============================================================
ws10 = wb.create_sheet("Change_Log")

ws10.append(["Timestamp", "Sheet", "Change Type", "Details"])
style_header(ws10)

CHANGES = [
    ("2026-01-17 23:00", "Skills_Metadata", "Initial Creation", "Created 50+ skill entries from GSL framework"),
    ("2026-01-17 23:00", "Categories", "Initial Creation", "Created 10 skill categories"),
    ("2026-01-17 23:00", "Coverage Matrix", "Initial Creation", "Mapped skills to courses"),
    ("2026-01-17 23:00", "RACI Matrix", "Initial Creation", "Defined RACI assignments per skill"),
    ("2026-01-17 23:00", "Training Gaps", "Initial Creation", "Documented 6 training gaps"),
    ("2026-01-17 23:00", "Conflict Matrix", "Initial Creation", "Documented 5 conflicts/resolutions"),
    ("2026-01-17 23:00", "Role Checklist", "Initial Creation", "Defined 8 role training requirements"),
    ("2026-01-17 23:00", "Role Alignment Matrix", "Initial Creation", "Created role-skill level matrix"),
    ("2026-01-17 23:00", "Skills Crosswalk", "Initial Creation", "Mapped old to new skill names"),
    ("2026-01-17 23:00", "Learn365 API", "Integration", "Created skills via Learn365 API"),
]

for row in CHANGES:
    ws10.append(row)

auto_width(ws10)

# ============================================================
# Sheet 11: Mapping Log
# ============================================================
ws11 = wb.create_sheet("Mapping_Log")

ws11.append(["Sheet", "Skill Title", "Source", "Target", "Match Type", "Confidence", "Notes"])
style_header(ws11)

MAPPINGS = [
    ("Coverage Matrix", "Safety Awareness & Culture", "SCORM Catalog", "Learn365 Skill", "Title Match", "High", "Direct mapping"),
    ("Coverage Matrix", "Lean Fundamentals", "SCORM Catalog", "Learn365 Skill", "Title Match", "High", "Direct mapping"),
    ("Coverage Matrix", "Leadership Fundamentals", "SCORM Catalog", "Learn365 Skill", "Content Match", "High", "Mapped via course content"),
    ("RACI Matrix", "All Skills", "TARGET_SKILL_RULES.md", "Role Assignments", "Document Match", "High", "From framework document"),
    ("Role Alignment Matrix", "All Skills", "TARGET_SKILL_RULES.md", "Proficiency Levels", "Document Match", "High", "From framework document"),
    ("Skills Crosswalk", "22 Skills", "Learn365 Existing", "New Categories", "API Migration", "High", "Migrated via API"),
    ("Skills Crosswalk", "56 Skills", "Framework", "Learn365 New", "API Creation", "High", "Created via API"),
]

for row in MAPPINGS:
    ws11.append(row)

auto_width(ws11)

# ============================================================
# Save workbook
# ============================================================
output_path = r"C:\Users\tewing\Desktop\Claude Projects\SOPs For Review\Learn365_Skills_Matrix.xlsx"
wb.save(output_path)
print(f"Created: {output_path}")
print(f"Sheets: {wb.sheetnames}")
