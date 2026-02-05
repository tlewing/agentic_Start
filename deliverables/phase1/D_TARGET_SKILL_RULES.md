# GSL Academy - Target Skill Rules

## Overview

Target Skill Rules define which skills are required for each role and the training path to achieve them. These rules drive automatic training assignments in the LMS.

---

## Rule Structure

Each rule follows this pattern:
```
IF [Role] = [X] THEN require [Skills] via [Training Modules]
```

---

## Role: All Employees (Universal Requirements)

### Rule: UNIV-001 - New Hire Requirements

| Field | Value |
|-------|-------|
| **Rule ID** | UNIV-001 |
| **Trigger** | New hire onboarding |
| **Target Audience** | All new employees |
| **Required Skills** | SAF-001, SAF-024, POL-002, POL-003, POL-004 |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | A Commitment to Zero Broken Lives | Day 1 |
| 2 | GSL New Hire Safety Orientation | Day 1 |
| 3 | Harassment Discrimination and Retaliation Prevention | Week 1 |
| 4 | Substance Abuse Policy | Week 1 |
| 5 | EAP and Mental Health Awareness | Week 1 |
| 6 | Preventing Slips Trips and Falls | Week 2 |

### Rule: UNIV-002 - Nevada Employees

| Field | Value |
|-------|-------|
| **Rule ID** | UNIV-002 |
| **Trigger** | Work location = Nevada |
| **Target Audience** | All Nevada employees |
| **Required Skills** | SAF-002 |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | Nevada's Employee Rights and Responsibilities | Day 1 |

---

## Role: Apprentice Electrician (Years 1-4)

### Rule: APP-001 - First Year Apprentice

| Field | Value |
|-------|-------|
| **Rule ID** | APP-001 |
| **Trigger** | Role = Apprentice, Year = 1 |
| **Target Audience** | First year apprentices |
| **Required Skills** | SAF-001, SAF-003, SAF-007, SAF-012, SAF-014, SAF-017, SAF-019, SAF-020, SAF-024, SAF-025 |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | Universal Requirements (UNIV-001) | Week 1 |
| 2 | Arc Flash PPE | Month 1 |
| 3 | Lockout Tagout Procedures (main) | Month 1 |
| 4 | Verifying a De-Energized Condition | Month 1 |
| 5 | Fall Protection (main) | Month 1 |
| 6 | Using Portable and Fixed Ladders | Month 1 |
| 7 | Hazard Communication | Month 2 |
| 8 | Information Found on Container Labels | Month 2 |
| 9 | OSHA Focus Four Workplace Hazards | Month 3 |

### Rule: APP-002 - Second Year Apprentice

| Field | Value |
|-------|-------|
| **Rule ID** | APP-002 |
| **Trigger** | Role = Apprentice, Year = 2 |
| **Target Audience** | Second year apprentices |
| **Required Skills** | SAF-004, SAF-008, SAF-015, SAF-016, SAF-021, SAF-022 |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | 2024 NFPA 70-E Required Boundaries | Month 1 |
| 2 | Simple Lockout Tagout Procedures | Month 1 |
| 3 | Fall Protection - Edges Openings and Guarding | Month 2 |
| 4 | Scaffolding Safety Series (3 modules) | Month 2-3 |
| 5 | Safety Data Sheets | Month 3 |
| 6 | Types of Chemical Hazards | Month 3 |

### Rule: APP-003 - Third Year Apprentice

| Field | Value |
|-------|-------|
| **Rule ID** | APP-003 |
| **Trigger** | Role = Apprentice, Year = 3 |
| **Target Audience** | Third year apprentices |
| **Required Skills** | SAF-005, SAF-009, SAF-011, SAF-013, SAF-018 |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | Complex Lockout Tagout Procedures | Month 1 |
| 2 | Return to Service Procedures | Month 2 |
| 3 | Hazardous Energy Control Lockout Tagout | Month 3 |
| 4 | Permit Required Confined Spaces | Month 4 |
| 5 | Safe Electrical Work Practices 2024 NFPA 70-E | Month 6 |

### Rule: APP-004 - Fourth Year Apprentice

| Field | Value |
|-------|-------|
| **Rule ID** | APP-004 |
| **Trigger** | Role = Apprentice, Year = 4 |
| **Target Audience** | Fourth year apprentices |
| **Required Skills** | FLD-004, FLD-007, LCN-001, LCN-002, EQ-001 |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | Time Management | Month 1 |
| 2 | Introduction to Effective Communication | Month 2 |
| 3 | What is Lean | Month 3 |
| 4 | Introduction to Lean Construction | Month 3 |
| 5 | Eight Wastes of Construction | Month 4 |
| 6 | What is Emotional Intelligence | Month 6 |

---

## Role: Journeyman Electrician

### Rule: JRN-001 - Journeyman Core

| Field | Value |
|-------|-------|
| **Rule ID** | JRN-001 |
| **Trigger** | Role = Journeyman |
| **Target Audience** | All journeyman electricians |
| **Required Skills** | All APP skills + FLD-005, SAF-006, LCN-003, LCN-004 |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | Using Tools and Technology | Month 1 |
| 2 | Electrical Shock Arc Flash Risk Assessments | Month 2 |
| 3 | Embracing Lean Productivity | Month 3 |
| 4 | Productivity in Construction | Month 3 |
| 5 | Construction vs Manufacturing | Month 4 |

---

## Role: Lead Journeyman

### Rule: LEAD-001 - Lead Journeyman Core

| Field | Value |
|-------|-------|
| **Rule ID** | LEAD-001 |
| **Trigger** | Role = Lead Journeyman |
| **Target Audience** | All lead journeymen |
| **Required Skills** | All JRN skills + FLD-002, FLD-003, FLD-013, FLD-014, LDR-001, LDR-002, EQ-002, EQ-003, EQ-004, LCN-010 |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | Avoiding Common Time Wasters | Month 1 |
| 2 | Building and Maintaining Team Morale | Month 1 |
| 3 | Jobsite Efficiency | Month 2 |
| 4 | Coordinating with Other Trades | Month 2 |
| 5 | Leadership Essentials | Month 3 |
| 6 | Techniques for Better Communication and Feedback | Month 3 |
| 7 | Improving Self-Awareness | Month 4 |
| 8 | Boosting Self-Regulation | Month 4 |
| 9 | Increasing Self-Motivation | Month 5 |
| 10 | On-Site Productivity | Month 6 |

---

## Role: Foreman

### Rule: FOR-001 - Foreman Safety Coordinator Certification

| Field | Value |
|-------|-------|
| **Rule ID** | FOR-001 |
| **Trigger** | Role = Foreman (Promotion) |
| **Target Audience** | All foremen |
| **Required Skills** | SCO-001 through SCO-009 |
| **Prerequisite** | Lead Journeyman skills complete |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | Safety Coordinator 3.0 - Employee Safety Orientation | Month 1 |
| 2 | Safety Coordinator 4.0 - Task Training | Month 1 |
| 3 | Safety Coordinator 5.0 - Safety Meetings | Month 2 |
| 4 | Safety Coordinator 6.0 - Project Planning Hazards | Month 2 |
| 5 | Safety Coordinator 7.0 - Safety Inspections | Month 3 |
| 6 | Safety Coordinator 8.0 - Disciplinary Action | Month 3 |
| 7 | Safety Coordinator 9.0 - Accident Investigations | Month 4 |
| 8 | Safety Coordinator 10.0 - Injury Case Management | Month 4 |
| 9 | Safety Coordinator 11.0 - OSHA MSHA Inspections | Month 5 |

### Rule: FOR-002 - Foreman Field Leadership

| Field | Value |
|-------|-------|
| **Rule ID** | FOR-002 |
| **Trigger** | Role = Foreman |
| **Target Audience** | All foremen |
| **Required Skills** | FLD-001, FLD-006, FLD-008, FLD-009, FLD-010, FLD-011, FLD-012, FLD-015, FLD-016, FLD-017 |
| **Training Path** | |

**Section 1: Skills, Traits & Responsibilities**
| Order | Module | Due |
|-------|--------|-----|
| 1 | Introduction to Field Leadership Section 1 | Month 1 |
| 2 | Roles and Responsibilities of a Foreman | Month 1 |
| 3 | Introduction to Documentation and Reporting | Month 2 |
| 4 | Introduction to Project Planning and Execution | Month 2 |
| 5 | Introduction to Quality Control | Month 3 |
| 6 | Introduction to Safety Management | Month 3 |
| 7 | Introduction to Team Management | Month 4 |

**Section 2: Anatomy of a Project**
| Order | Module | Due |
|-------|--------|-----|
| 8 | Job Plan Theory | Month 5 |
| 9 | Document Management | Month 5 |
| 10 | Manpower Projection | Month 6 |
| 11 | Job Closeout | Month 6 |

### Rule: FOR-003 - Foreman Leadership

| Field | Value |
|-------|-------|
| **Rule ID** | FOR-003 |
| **Trigger** | Role = Foreman |
| **Target Audience** | All foremen |
| **Required Skills** | LDR-003, LDR-004, LDR-005, LDR-006, LDR-008, LDR-009, EQ-005, EQ-006 |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | Introduction to Critical Leadership Training | Month 1 |
| 2 | What Makes a Leader | Month 1 |
| 3 | Leadership is About Human Interaction | Month 2 |
| 4 | New Manager 101 | Month 2 |
| 5 | Building an Effective Team | Month 3 |
| 6 | Extreme Ownership | Month 3 |
| 7 | Leadership Law 1 - Cover and Move | Month 4 |
| 8 | Leadership Law 2 - Keep It Simple | Month 4 |
| 9 | Leadership Law 3 - Prioritize and Execute | Month 5 |
| 10 | Developing Empathy | Month 5 |
| 11 | Enhancing Social Skills | Month 6 |

### Rule: FOR-004 - Foreman Lean Construction

| Field | Value |
|-------|-------|
| **Rule ID** | FOR-004 |
| **Trigger** | Role = Foreman |
| **Target Audience** | All foremen |
| **Required Skills** | LCN-005, LCN-006, LCN-007, LCN-008, LCN-009 |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | What Processes Need to Change | Month 1 |
| 2 | Adoption of New Production Theory | Month 2 |
| 3 | Minimizing Waste at Project Level | Month 3 |
| 4 | Empowerment of Field Personnel | Month 4 |
| 5 | Pull Planning | Month 5 |
| 6 | The Sticky Note Format | Month 5 |
| 7 | Continuous Improvement | Month 6 |

### Rule: FOR-005 - Foreman Policy

| Field | Value |
|-------|-------|
| **Rule ID** | FOR-005 |
| **Trigger** | Role = Foreman |
| **Target Audience** | All foremen |
| **Required Skills** | POL-001, SAF-023, SAF-026, SAF-027, PFM-001, PFM-002, PFM-004 |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | Introduction to Field Leadership Part 4 - Policy | Month 1 |
| 2 | FMLA | Month 1 |
| 3 | The Written Hazard Communication Plan | Month 2 |
| 4 | Introduction to Planning and Controlling Hazards (TRACK) | Month 3 |
| 5 | Workplace Inspections Pre-Task Assessments | Month 3 |
| 6 | Conducting Effective Performance Reviews | Month 4 |
| 7 | Corrective Counseling and Performance Reviews | Month 5 |
| 8 | Motivating Your Team | Month 6 |

### Rule: FOR-006 - Foreman Software

| Field | Value |
|-------|-------|
| **Rule ID** | FOR-006 |
| **Trigger** | Role = Foreman |
| **Target Audience** | All foremen |
| **Required Skills** | SFT-002 |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | Approving Change Orders in ViewPoint | Month 2 |
| 2 | Creating Pending Change Orders in ViewPoint | Month 2 |

---

## Role: Project Superintendent (General Foreman)

### Rule: SUP-001 - Superintendent Advanced Leadership

| Field | Value |
|-------|-------|
| **Rule ID** | SUP-001 |
| **Trigger** | Role = Superintendent |
| **Target Audience** | All superintendents |
| **Required Skills** | All Foreman skills + LDR-007, LDR-010, EQ-007, PFM-003, PMG-001, PMG-002 |
| **Prerequisite** | All Foreman rules complete, 3-5 years as Foreman |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | Leadership Law 4 - Decentralize Command | Month 1 |
| 2 | Leadership is the Most Important Skill (Conclusion) | Month 1 |
| 3 | Leading with Emotional Intelligence | Month 2 |
| 4 | Performance Management | Month 3 |
| 5 | Project Structure Delegation and Team Development | Month 4 |
| 6 | Managing Sub-Contractors | Month 5 |
| 7 | Coach K Values-Driven Leadership Series (12 modules) | Month 6-12 |

---

## Role: Project Safety Coordinator

### Rule: PSC-001 - Safety Coordinator Specialist

| Field | Value |
|-------|-------|
| **Rule ID** | PSC-001 |
| **Trigger** | Role = Project Safety Coordinator |
| **Target Audience** | Dedicated safety coordinators |
| **Required Skills** | All Safety Coordinator skills + advanced safety |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | Complete Safety Coordinator Series (3.0-11.0) | Month 1-3 |
| 2 | All Electrical Safety modules | Month 4 |
| 3 | All LOTO modules | Month 5 |
| 4 | All Fall Protection modules | Month 6 |
| 5 | All HazCom modules | Month 6 |

---

## Role: Estimators

### Rule: EST-001 - Estimator Software

| Field | Value |
|-------|-------|
| **Rule ID** | EST-001 |
| **Trigger** | Role = Estimator |
| **Target Audience** | All estimators |
| **Required Skills** | SFT-001 |
| **Training Path** | |

| Order | Module | Due |
|-------|--------|-----|
| 1 | Learning Accubid Pro | Month 1 |

---

## Rules Summary

| Rule ID | Role | Skill Count | Module Count | Duration |
|---------|------|-------------|--------------|----------|
| UNIV-001 | All Employees | 5 | 6 | 2 weeks |
| UNIV-002 | Nevada Employees | 1 | 1 | Day 1 |
| APP-001 | Apprentice Year 1 | 10 | 9 | 3 months |
| APP-002 | Apprentice Year 2 | 6 | 7 | 3 months |
| APP-003 | Apprentice Year 3 | 5 | 5 | 6 months |
| APP-004 | Apprentice Year 4 | 5 | 6 | 6 months |
| JRN-001 | Journeyman | 4 | 5 | 4 months |
| LEAD-001 | Lead Journeyman | 10 | 10 | 6 months |
| FOR-001 | Foreman (Safety) | 9 | 9 | 5 months |
| FOR-002 | Foreman (Field Leadership) | 10 | 11 | 6 months |
| FOR-003 | Foreman (Leadership) | 8 | 11 | 6 months |
| FOR-004 | Foreman (Lean) | 5 | 7 | 6 months |
| FOR-005 | Foreman (Policy) | 7 | 8 | 6 months |
| FOR-006 | Foreman (Software) | 1 | 2 | 2 months |
| SUP-001 | Superintendent | 6 | 18 | 12 months |
| PSC-001 | Safety Coordinator | 15+ | 20+ | 6 months |
| EST-001 | Estimator | 1 | 1 | 1 month |

---

## Implementation Notes

### LMS Configuration

1. Create rule groups by role
2. Set up prerequisite chains
3. Configure automatic enrollment triggers
4. Set due date calculations
5. Enable progress tracking and notifications

### Compliance Tracking

- Annual recertification for safety modules
- Safety Coordinator certification validity: 3 years
- First Aid/CPR: Annual recertification (external)
- OSHA 30: One-time completion (external)

### Gap Analysis

**Training gaps identified:**
- Safety Coordinator 1.0 and 2.0 modules missing
- No formal First Aid/CPR training in LMS (external requirement)
- No OSHA 10/30 in LMS (external certification)
- Technical electrical skills not covered in LMS (apprenticeship classroom)
