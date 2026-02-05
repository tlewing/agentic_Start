"""
Generate Course Descriptions for SCORM Catalog

This script generates:
- Short descriptions (50-75 words)
- Long descriptions (200-250 words)
- Categories/Subcategories
- Search tags

Based on course titles and domain knowledge of:
- Construction industry
- Electrical trade
- Leadership development
- Safety training
"""

import csv
import re
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from datetime import datetime

# Course description templates by category/topic
DESCRIPTION_TEMPLATES = {
    # Leadership & Management
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

    "team_management": {
        "short": "Master essential team management skills for field leadership. This course covers building effective teams, managing diverse personalities, delegating responsibilities, and maintaining high performance under challenging project conditions.",
        "long": """Master essential team management skills for field leadership. This course covers building effective teams, managing diverse personalities, delegating responsibilities, and maintaining high performance under challenging project conditions.

Effective team management is the cornerstone of successful project execution. Whether you're a foreman leading a crew or a superintendent overseeing multiple teams, this training provides practical strategies for getting the best from your people.

This course explores the human side of construction leadership—understanding what motivates your team, how to communicate expectations clearly, and how to address performance issues constructively.

Key Learning Objectives:
1. Build cohesive teams that work well together under pressure
2. Understand different personality types and communication styles
3. Delegate effectively while maintaining accountability
4. Provide constructive feedback that improves performance
5. Handle conflicts and difficult conversations professionally
6. Recognize and reward good performance appropriately
7. Develop team members for advancement and succession planning

Apply these skills to create a positive work environment that attracts and retains top talent.""",
        "tags": ["team management", "leadership", "delegation", "communication", "performance", "field leadership", "supervision"]
    },

    "team_morale": {
        "short": "Learn proven techniques for building and maintaining high team morale in construction environments. This course covers recognition strategies, communication practices, and leadership behaviors that create engaged, motivated crews who take pride in their work.",
        "long": """Learn proven techniques for building and maintaining high team morale in construction environments. This course covers recognition strategies, communication practices, and leadership behaviors that create engaged, motivated crews who take pride in their work.

High morale directly impacts productivity, safety, and quality. When workers feel valued and connected to their team, they perform better and stay longer. This training provides practical tools for creating that positive environment.

The construction industry presents unique morale challenges—physically demanding work, weather conditions, tight deadlines, and rotating crews. This course addresses these specific challenges with field-tested solutions.

Key Learning Objectives:
1. Understand the connection between morale and performance
2. Recognize individual and team contributions effectively
3. Communicate openly and build trust with your crew
4. Address concerns and complaints constructively
5. Create a sense of purpose and pride in the work
6. Handle stress and pressure without damaging morale
7. Build team cohesion through shared experiences and goals

Implement these strategies to reduce turnover, improve safety, and build a reputation as a leader people want to work for.""",
        "tags": ["morale", "motivation", "team building", "leadership", "recognition", "engagement", "retention"]
    },

    # Safety
    "lockout_tagout": {
        "short": "Master critical lockout/tagout procedures to protect yourself and coworkers from hazardous energy. This course covers proper isolation techniques, verification methods, and regulatory requirements essential for electrical safety in construction and industrial environments.",
        "long": """Master critical lockout/tagout procedures to protect yourself and coworkers from hazardous energy. This course covers proper isolation techniques, verification methods, and regulatory requirements essential for electrical safety in construction and industrial environments.

Lockout/Tagout (LOTO) procedures are among the most important safety protocols in electrical work. Failure to properly control hazardous energy results in serious injuries and fatalities every year. This training ensures you understand both the procedures and the reasoning behind them.

This course addresses OSHA requirements, company-specific procedures, and best practices developed through decades of industry experience. You'll learn to recognize hazards, implement controls, and verify safe conditions.

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

    "arc_flash": {
        "short": "Understand arc flash hazards and protection requirements based on NFPA 70E standards. This course covers risk assessment, approach boundaries, PPE selection, and safe work practices essential for electrical workers exposed to arc flash dangers.",
        "long": """Understand arc flash hazards and protection requirements based on NFPA 70E standards. This course covers risk assessment, approach boundaries, PPE selection, and safe work practices essential for electrical workers exposed to arc flash dangers.

Arc flash incidents release tremendous energy in the form of heat, light, pressure, and sound—causing severe burns, hearing loss, and other injuries. This training provides the knowledge needed to recognize, assess, and control arc flash hazards.

Based on the latest NFPA 70E requirements, this course ensures you understand your responsibilities and the protective measures required when working near energized equipment.

Key Learning Objectives:
1. Understand arc flash physics and incident energy
2. Identify approach boundaries and their requirements
3. Select appropriate PPE based on hazard analysis
4. Perform arc flash risk assessments properly
5. Apply safe work practices around energized equipment
6. Understand when energized work is permitted
7. Respond appropriately to arc flash incidents

This essential training protects you, your coworkers, and your company from the devastating consequences of arc flash incidents.""",
        "tags": ["safety", "arc flash", "NFPA 70E", "PPE", "electrical safety", "risk assessment", "energized work"]
    },

    "fall_protection": {
        "short": "Learn essential fall protection principles for construction environments. This course covers hazard recognition, protection systems, equipment inspection, and regulatory requirements to prevent falls—the leading cause of construction fatalities.",
        "long": """Learn essential fall protection principles for construction environments. This course covers hazard recognition, protection systems, equipment inspection, and regulatory requirements to prevent falls—the leading cause of construction fatalities.

Falls from height remain the number one killer in construction. This training provides comprehensive knowledge of fall hazards and the systems designed to protect workers—from guardrails and safety nets to personal fall arrest systems.

Whether you're working on scaffolds, ladders, roofs, or elevated structures, understanding fall protection is essential for your safety and the safety of those around you.

Key Learning Objectives:
1. Recognize fall hazards in construction environments
2. Understand different fall protection systems and their applications
3. Inspect and maintain personal fall protection equipment
4. Calculate fall distances and clearance requirements
5. Set up and use anchor points properly
6. Follow OSHA fall protection requirements
7. Respond to fall incidents appropriately

Completing this training demonstrates your understanding of fall hazards and your commitment to working safely at heights.""",
        "tags": ["safety", "fall protection", "OSHA", "construction safety", "harness", "heights", "scaffolding"]
    },

    "scaffolding": {
        "short": "Master scaffold safety for construction environments. This course covers scaffold types, erection procedures, inspection requirements, load capacities, and safe access methods to prevent injuries while working on or around scaffolding systems.",
        "long": """Master scaffold safety for construction environments. This course covers scaffold types, erection procedures, inspection requirements, load capacities, and safe access methods to prevent injuries while working on or around scaffolding systems.

Scaffolding provides essential access for construction work at height, but improper setup or use creates serious hazards. This training ensures you understand how to work safely on scaffolds and recognize potential dangers.

From supported scaffolds to suspended systems, this course covers the variety of scaffolding used in construction and the specific requirements for each type.

Key Learning Objectives:
1. Identify different scaffold types and their applications
2. Understand scaffold erection and dismantling procedures
3. Inspect scaffolds before use and identify deficiencies
4. Know load capacity requirements and limitations
5. Access and egress scaffolds safely
6. Work safely on scaffold platforms
7. Recognize and report scaffold hazards

This training prepares you to work confidently on scaffolding while maintaining the highest safety standards.""",
        "tags": ["safety", "scaffolding", "construction safety", "OSHA", "fall protection", "access", "inspection"]
    },

    "safety_coordinator": {
        "short": "Develop the skills needed to serve as a project safety coordinator. This course covers safety program management, inspections, training responsibilities, incident investigation, and regulatory compliance essential for maintaining safe construction sites.",
        "long": """Develop the skills needed to serve as a project safety coordinator. This course covers safety program management, inspections, training responsibilities, incident investigation, and regulatory compliance essential for maintaining safe construction sites.

Safety coordinators play a vital role in protecting workers and ensuring compliance. This training provides the comprehensive knowledge needed to manage safety programs effectively and create a culture of safety on your projects.

From conducting inspections to investigating incidents, this course covers the full range of safety coordinator responsibilities and best practices.

Key Learning Objectives:
1. Understand the safety coordinator role and responsibilities
2. Conduct effective safety orientations for new employees
3. Plan and lead safety meetings that engage workers
4. Perform thorough jobsite safety inspections
5. Investigate accidents and incidents properly
6. Manage injury cases and return-to-work programs
7. Prepare for and respond to regulatory inspections

This training prepares you to lead safety efforts and make a real difference in protecting workers on your projects.""",
        "tags": ["safety", "safety coordinator", "OSHA", "inspections", "training", "incident investigation", "compliance"]
    },

    "hazard_communication": {
        "short": "Understand hazard communication requirements for chemical safety. This course covers the GHS labeling system, Safety Data Sheets, container labels, and employee rights essential for working safely with hazardous materials in construction.",
        "long": """Understand hazard communication requirements for chemical safety. This course covers the GHS labeling system, Safety Data Sheets, container labels, and employee rights essential for working safely with hazardous materials in construction.

Chemical hazards are present on most construction sites—from adhesives and sealants to cleaning products and fuels. This training ensures you can identify hazards, understand warnings, and protect yourself from chemical exposures.

The Globally Harmonized System (GHS) standardizes chemical hazard communication worldwide. This course explains how to interpret labels, pictograms, and Safety Data Sheets to work safely with any chemical product.

Key Learning Objectives:
1. Understand the purpose of hazard communication programs
2. Read and interpret GHS labels and pictograms
3. Locate and use Safety Data Sheets effectively
4. Identify chemical hazards by type (health, physical, environmental)
5. Select appropriate PPE for chemical work
6. Follow proper handling and storage procedures
7. Respond to chemical spills and exposures appropriately

This essential training protects you from chemical hazards you may encounter on any construction project.""",
        "tags": ["safety", "hazard communication", "GHS", "SDS", "chemicals", "labels", "PPE"]
    },

    "confined_space": {
        "short": "Learn permit-required confined space entry procedures to work safely in tanks, manholes, and other confined areas. This course covers hazard recognition, atmospheric testing, entry permits, and rescue planning essential for confined space work.",
        "long": """Learn permit-required confined space entry procedures to work safely in tanks, manholes, and other confined areas. This course covers hazard recognition, atmospheric testing, entry permits, and rescue planning essential for confined space work.

Confined spaces present unique hazards—atmospheric dangers, engulfment, entrapment, and limited access for rescue. This training provides the knowledge needed to recognize these hazards and control them through proper procedures.

From electrical vaults to storage tanks, construction workers frequently encounter confined spaces. Understanding entry requirements and your role in the entry process is essential for survival.

Key Learning Objectives:
1. Identify confined spaces and permit-required confined spaces
2. Recognize atmospheric and physical hazards in confined spaces
3. Perform atmospheric monitoring and interpret results
4. Complete entry permits and follow permit requirements
5. Understand entrant, attendant, and supervisor responsibilities
6. Plan for emergency rescue and response
7. Follow company confined space entry procedures

This critical training prepares you to work safely in confined spaces and potentially save lives.""",
        "tags": ["safety", "confined space", "permit required", "atmospheric testing", "rescue", "entry permit", "OSHA"]
    },

    # Lean Construction
    "lean_construction": {
        "short": "Discover how Lean principles transform construction project delivery. This course covers waste elimination, value stream mapping, pull planning, and continuous improvement methods that increase productivity and reduce costs in construction.",
        "long": """Discover how Lean principles transform construction project delivery. This course covers waste elimination, value stream mapping, pull planning, and continuous improvement methods that increase productivity and reduce costs in construction.

Lean Construction adapts manufacturing principles to the unique challenges of construction—complex projects, variable conditions, and multiple stakeholders. This training shows how these principles improve outcomes while respecting the craft traditions of the industry.

From reducing material waste to optimizing workflow, Lean methods address the inefficiencies that plague traditional construction approaches.

Key Learning Objectives:
1. Understand Lean principles and their application to construction
2. Identify and eliminate the eight wastes in construction
3. Apply pull planning to coordinate work sequences
4. Use visual management to improve communication
5. Implement continuous improvement practices
6. Engage field teams in problem-solving
7. Measure and sustain Lean improvements

Join the growing movement of construction professionals who are transforming how we build through Lean thinking.""",
        "tags": ["lean construction", "productivity", "waste elimination", "pull planning", "continuous improvement", "efficiency"]
    },

    "waste_elimination": {
        "short": "Learn to identify and eliminate the eight wastes of construction. This course provides practical techniques for reducing transportation, inventory, motion, waiting, overprocessing, overproduction, defects, and underutilized talent on your projects.",
        "long": """Learn to identify and eliminate the eight wastes of construction. This course provides practical techniques for reducing transportation, inventory, motion, waiting, overprocessing, overproduction, defects, and underutilized talent on your projects.

Studies show that over 50% of construction activity is waste—work that adds cost but not value. This training helps you see waste clearly and take action to eliminate it from your daily work.

Each type of waste has specific causes and solutions. Understanding these connections enables you to make immediate improvements while building long-term capability for continuous improvement.

Key Learning Objectives:
1. Understand the eight wastes and their impact on productivity
2. Identify waste in your current work processes
3. Apply specific techniques for each waste type
4. Engage your team in waste identification and elimination
5. Measure waste reduction results
6. Sustain improvements over time
7. Create a culture of continuous improvement

Start seeing waste where others see normal operations—and transform your project performance.""",
        "tags": ["lean", "waste elimination", "productivity", "eight wastes", "construction", "efficiency", "continuous improvement"]
    },

    "pull_planning": {
        "short": "Master pull planning techniques for construction scheduling. This course teaches how to develop reliable schedules through collaborative planning, constraint identification, and commitment-based workflow that improves predictability and coordination.",
        "long": """Master pull planning techniques for construction scheduling. This course teaches how to develop reliable schedules through collaborative planning, constraint identification, and commitment-based workflow that improves predictability and coordination.

Traditional push scheduling creates unreliable plans that quickly become obsolete. Pull planning reverses this approach—starting from milestones and working backward to create plans that reflect actual workflow dependencies and constraints.

This collaborative approach engages all trades in the planning process, creating ownership and commitment that leads to better plan reliability.

Key Learning Objectives:
1. Understand the difference between push and pull planning
2. Facilitate pull planning sessions with multiple trades
3. Identify constraints and develop solutions collaboratively
4. Use the sticky note format for visual planning
5. Make and track reliable commitments
6. Conduct weekly work planning sessions
7. Measure and improve plan reliability over time

Transform your scheduling approach from wishful thinking to reliable planning that delivers results.""",
        "tags": ["lean", "pull planning", "scheduling", "collaboration", "constraint management", "reliability", "Last Planner"]
    },

    # Emotional Intelligence
    "emotional_intelligence": {
        "short": "Develop emotional intelligence skills essential for effective leadership. This course covers self-awareness, self-regulation, empathy, and social skills that enable leaders to connect with their teams and navigate challenging interpersonal situations.",
        "long": """Develop emotional intelligence skills essential for effective leadership. This course covers self-awareness, self-regulation, empathy, and social skills that enable leaders to connect with their teams and navigate challenging interpersonal situations.

Emotional Intelligence (EQ) is often more important than technical skills for leadership success. The ability to understand and manage your own emotions while recognizing and influencing the emotions of others is fundamental to effective leadership.

This training provides practical techniques for developing each component of emotional intelligence and applying them in workplace situations.

Key Learning Objectives:
1. Understand emotional intelligence and its components
2. Develop greater self-awareness of your emotions and triggers
3. Practice self-regulation techniques for stressful situations
4. Build empathy by understanding others' perspectives
5. Enhance social skills for better workplace relationships
6. Apply EQ principles in difficult conversations
7. Create an emotionally intelligent team culture

Elevate your leadership effectiveness by developing the emotional intelligence skills that matter most.""",
        "tags": ["emotional intelligence", "EQ", "leadership", "self-awareness", "empathy", "social skills", "communication"]
    },

    # Professional Development
    "presenting": {
        "short": "Master the art of professional presenting to communicate ideas effectively. This course covers presentation structure, slide design, delivery techniques, and audience engagement strategies that transform nervous speakers into confident presenters.",
        "long": """Master the art of professional presenting to communicate ideas effectively. This course covers presentation structure, slide design, delivery techniques, and audience engagement strategies that transform nervous speakers into confident presenters.

Whether presenting safety toolbox talks, project updates, or training sessions, the ability to present clearly and confidently is essential for career advancement. This training provides a systematic approach to preparing and delivering presentations that achieve results.

From understanding your audience to handling questions, this course covers every aspect of effective presenting in professional settings.

Key Learning Objectives:
1. Plan presentations with clear objectives and audience focus
2. Structure content for maximum impact and retention
3. Design slides that support rather than distract
4. Prepare effectively to reduce anxiety
5. Deliver with confidence and authentic presence
6. Engage audiences through interaction and storytelling
7. Handle questions and challenges professionally

Develop presentation skills that enhance your professional presence and advance your career.""",
        "tags": ["presentation", "public speaking", "communication", "slides", "professional development", "delivery", "audience"]
    },

    # Project Planning & Productivity
    "time_management": {
        "short": "Learn practical time management techniques for construction professionals. This course covers prioritization methods, scheduling strategies, and productivity habits that help you accomplish more in less time while reducing stress.",
        "long": """Learn practical time management techniques for construction professionals. This course covers prioritization methods, scheduling strategies, and productivity habits that help you accomplish more in less time while reducing stress.

Construction leaders face constant demands—multiple projects, urgent issues, meetings, and administrative tasks. Without effective time management, important work gets crowded out by whatever seems most urgent at the moment.

This training provides practical tools specifically designed for the construction environment, where interruptions are frequent and flexibility is essential.

Key Learning Objectives:
1. Assess how you currently spend your time
2. Prioritize tasks using proven frameworks
3. Plan your day and week for maximum productivity
4. Minimize time wasted on common distractions
5. Delegate effectively to multiply your impact
6. Handle interruptions without losing focus
7. Build sustainable productivity habits

Take control of your time and accomplish what matters most while maintaining work-life balance.""",
        "tags": ["time management", "productivity", "prioritization", "efficiency", "planning", "focus", "professional development"]
    },

    "project_planning": {
        "short": "Master project planning fundamentals for construction execution. This course covers work breakdown, scheduling techniques, resource planning, and tracking methods that ensure projects start strong and stay on track.",
        "long": """Master project planning fundamentals for construction execution. This course covers work breakdown, scheduling techniques, resource planning, and tracking methods that ensure projects start strong and stay on track.

Effective planning is the foundation of project success. This training provides the knowledge and tools needed to break down work, sequence activities, allocate resources, and establish controls that keep projects on schedule and budget.

From initial mobilization through closeout, proper planning anticipates challenges and creates the framework for execution.

Key Learning Objectives:
1. Break down project scope into manageable work packages
2. Develop realistic schedules using proven techniques
3. Identify resources needed and plan their allocation
4. Establish tracking systems for progress monitoring
5. Anticipate risks and develop contingency plans
6. Coordinate with other trades and stakeholders
7. Adjust plans as conditions change while maintaining objectives

Build the planning skills that separate successful projects from troubled ones.""",
        "tags": ["project planning", "scheduling", "construction", "work breakdown", "resources", "tracking", "execution"]
    },

    # Documentation
    "documentation": {
        "short": "Learn essential documentation practices for construction projects. This course covers daily reports, RFIs, submittals, change orders, and record-keeping requirements that protect your company and support successful project delivery.",
        "long": """Learn essential documentation practices for construction projects. This course covers daily reports, RFIs, submittals, change orders, and record-keeping requirements that protect your company and support successful project delivery.

Construction documentation creates the official record of what happened on a project. Proper documentation protects against claims, supports change order recovery, and provides the information needed for project management decisions.

From daily reports to closeout packages, this training covers the documentation systems and practices that professional contractors use to manage risk and deliver quality projects.

Key Learning Objectives:
1. Understand the importance of construction documentation
2. Write clear, complete, and accurate daily reports
3. Manage RFIs and submittals effectively
4. Document changes and support change order recovery
5. Maintain organized project files and records
6. Use photos and video to supplement written records
7. Prepare complete closeout documentation packages

Protect your company and your career through professional documentation practices.""",
        "tags": ["documentation", "daily reports", "RFI", "submittals", "change orders", "records", "construction"]
    },

    # Performance Management
    "performance_reviews": {
        "short": "Learn to conduct effective performance reviews that motivate employees and improve results. This course covers preparation, feedback delivery, goal setting, and follow-up practices that make performance conversations productive and positive.",
        "long": """Learn to conduct effective performance reviews that motivate employees and improve results. This course covers preparation, feedback delivery, goal setting, and follow-up practices that make performance conversations productive and positive.

Performance reviews are opportunities to recognize achievements, address concerns, and align employees with organizational goals. Done well, they strengthen relationships and improve performance. Done poorly, they damage morale and waste time.

This training provides a practical framework for conducting reviews that employees actually value and that produce meaningful improvement.

Key Learning Objectives:
1. Prepare thoroughly for performance review conversations
2. Provide specific, balanced feedback on performance
3. Discuss development needs constructively
4. Set meaningful goals for the coming period
5. Handle defensive reactions professionally
6. Document conversations properly
7. Follow up to ensure agreed actions happen

Transform performance reviews from dreaded obligations to valuable leadership opportunities.""",
        "tags": ["performance management", "reviews", "feedback", "goals", "development", "leadership", "HR"]
    },

    "corrective_counseling": {
        "short": "Learn to address performance issues effectively through corrective counseling. This course covers documentation, conversation techniques, and progressive discipline practices that give employees the opportunity to improve while protecting the organization.",
        "long": """Learn to address performance issues effectively through corrective counseling. This course covers documentation, conversation techniques, and progressive discipline practices that give employees the opportunity to improve while protecting the organization.

Addressing performance problems is one of the most challenging aspects of leadership. This training provides a structured approach that treats employees fairly while maintaining standards and protecting the company from liability.

From verbal warnings to termination decisions, this course covers the full spectrum of corrective action with practical guidance for each step.

Key Learning Objectives:
1. Recognize when corrective action is needed
2. Document performance issues properly
3. Conduct difficult conversations professionally
4. Follow progressive discipline procedures
5. Set clear expectations and follow-up plans
6. Know when to involve HR or management
7. Handle terminations appropriately when necessary

Address performance issues early and effectively to build a high-performing team.""",
        "tags": ["corrective action", "discipline", "counseling", "performance", "documentation", "HR", "leadership"]
    },

    # Construction Software
    "procore": {
        "short": "Learn to use Procore construction management software effectively. This course covers project setup, document management, daily logs, RFIs, submittals, and collaboration features that streamline construction project administration.",
        "long": """Learn to use Procore construction management software effectively. This course covers project setup, document management, daily logs, RFIs, submittals, and collaboration features that streamline construction project administration.

Procore has become the industry standard for construction project management. This training ensures you can use its features effectively to manage information, collaborate with stakeholders, and maintain organized project records.

From initial setup through project closeout, this course covers the Procore features most used by field personnel and project managers.

Key Learning Objectives:
1. Navigate the Procore interface efficiently
2. Set up and configure projects properly
3. Manage documents and drawings in Procore
4. Create and track RFIs and submittals
5. Record daily logs and observations
6. Use collaboration and communication features
7. Generate reports and access project analytics

Master Procore to improve your efficiency and collaboration on construction projects.""",
        "tags": ["Procore", "construction software", "project management", "document control", "RFI", "submittals", "collaboration"]
    },

    "viewpoint": {
        "short": "Learn ViewPoint Vista for construction accounting and project management. This course covers change order processing, cost tracking, and financial workflows that keep projects profitable and properly documented.",
        "long": """Learn ViewPoint Vista for construction accounting and project management. This course covers change order processing, cost tracking, and financial workflows that keep projects profitable and properly documented.

ViewPoint Vista integrates accounting, project management, and operations data into a single system. This training ensures you can use Vista features relevant to your role while understanding how your work connects to the financial picture.

From change order approvals to cost coding, this course covers the Vista functions most used by field and project personnel.

Key Learning Objectives:
1. Navigate Vista interface and find information
2. Process and approve change orders properly
3. Enter time and cost data accurately
4. Track project costs against budget
5. Manage vendor and subcontractor information
6. Generate reports for project monitoring
7. Understand how Vista connects to other systems

Use Vista effectively to support project financial management and cost control.""",
        "tags": ["ViewPoint", "Vista", "construction accounting", "change orders", "cost tracking", "project management", "financial"]
    },

    # Field Leadership
    "field_leadership": {
        "short": "Build the essential skills for effective field leadership in construction. This course covers the core competencies, responsibilities, and mindset needed to lead crews successfully from mobilization through project closeout.",
        "long": """Build the essential skills for effective field leadership in construction. This course covers the core competencies, responsibilities, and mindset needed to lead crews successfully from mobilization through project closeout.

Field leadership requires a unique combination of technical knowledge, people skills, and business awareness. This training provides a comprehensive foundation for anyone stepping into a leadership role or wanting to improve their effectiveness.

From the foreman's daily responsibilities to the superintendent's strategic perspective, this course covers the full scope of field leadership.

Key Learning Objectives:
1. Understand field leadership roles and responsibilities
2. Plan and organize work for maximum productivity
3. Lead and motivate diverse crews effectively
4. Communicate with multiple stakeholders professionally
5. Manage time, priorities, and competing demands
6. Ensure quality and safety on your projects
7. Document and report project status accurately

Develop the leadership skills that will advance your construction career and enable project success.""",
        "tags": ["field leadership", "foreman", "superintendent", "construction", "crew management", "project execution", "leadership"]
    },

    "trade_coordination": {
        "short": "Master multi-trade coordination for smooth project execution. This course covers scheduling coordination, conflict resolution, communication protocols, and collaboration practices that keep all trades working productively together.",
        "long": """Master multi-trade coordination for smooth project execution. This course covers scheduling coordination, conflict resolution, communication protocols, and collaboration practices that keep all trades working productively together.

Construction projects require dozens of trades to work in the same space, often simultaneously. Without effective coordination, productivity suffers, conflicts arise, and schedules slip. This training provides the skills to orchestrate multiple trades effectively.

From coordination meetings to field problem-solving, this course covers the practices that enable smooth multi-trade operations.

Key Learning Objectives:
1. Plan and sequence work across multiple trades
2. Facilitate effective coordination meetings
3. Identify and resolve conflicts before they escalate
4. Communicate schedule changes promptly
5. Manage shared resources and access fairly
6. Build collaborative relationships with other trades
7. Escalate issues appropriately when needed

Become the coordinator that other trades want to work with—and deliver projects on schedule.""",
        "tags": ["coordination", "multi-trade", "scheduling", "collaboration", "construction", "conflict resolution", "communication"]
    },

    "jobsite_efficiency": {
        "short": "Learn to maximize jobsite efficiency through better planning and organization. This course covers work area setup, material staging, tool management, and workflow optimization that eliminates wasted time and motion.",
        "long": """Learn to maximize jobsite efficiency through better planning and organization. This course covers work area setup, material staging, tool management, and workflow optimization that eliminates wasted time and motion.

Studies show construction workers spend significant time on non-productive activities—waiting, walking, searching for materials, and other activities that don't add value. This training provides practical techniques to reduce that waste.

From morning startup to end-of-day closeout, efficient practices compound into significant productivity gains over a project's duration.

Key Learning Objectives:
1. Set up work areas for maximum productivity
2. Plan material deliveries and staging effectively
3. Organize tools and equipment for quick access
4. Sequence work to minimize rework and waiting
5. Coordinate with other trades to reduce interference
6. Identify and eliminate common time wasters
7. Create systems that sustain efficiency over time

Transform your project's productivity through disciplined attention to efficiency.""",
        "tags": ["efficiency", "productivity", "jobsite", "organization", "material staging", "workflow", "construction"]
    },

    "quality_control": {
        "short": "Implement effective quality control practices on construction projects. This course covers inspection protocols, defect prevention, documentation requirements, and quality management systems that deliver projects meeting specifications.",
        "long": """Implement effective quality control practices on construction projects. This course covers inspection protocols, defect prevention, documentation requirements, and quality management systems that deliver projects meeting specifications.

Quality problems are expensive—rework consumes time and money while damaging relationships with owners. This training provides the systematic approach needed to build quality into the work rather than inspecting defects out afterward.

From first-work inspections to final punch lists, effective quality control requires consistent attention throughout the project lifecycle.

Key Learning Objectives:
1. Understand quality requirements from plans and specifications
2. Establish quality standards and communicate expectations
3. Conduct inspections at appropriate hold points
4. Document quality observations properly
5. Address defects promptly and prevent recurrence
6. Coordinate with inspectors and owners professionally
7. Close out projects with complete quality records

Build quality into your projects and protect your company's reputation.""",
        "tags": ["quality control", "QC", "inspections", "defects", "specifications", "construction", "documentation"]
    },

    # HR/Policy
    "workplace_policy": {
        "short": "Understand important workplace policies and legal requirements. This course covers harassment prevention, discrimination, substance abuse, FMLA, and other policies that protect employees and ensure compliance with regulations.",
        "long": """Understand important workplace policies and legal requirements. This course covers harassment prevention, discrimination, substance abuse, FMLA, and other policies that protect employees and ensure compliance with regulations.

Workplace policies exist to protect employees, create fair working conditions, and ensure the company complies with legal requirements. Understanding these policies is essential for all employees, especially those in leadership positions.

This training covers the key policies that apply to construction workplaces and the responsibilities of supervisors in enforcing them.

Key Learning Objectives:
1. Understand harassment and discrimination prevention policies
2. Know employee rights and company obligations
3. Recognize situations requiring policy enforcement
4. Report concerns through appropriate channels
5. Maintain confidentiality when handling sensitive issues
6. Support employees accessing benefits and assistance
7. Create an inclusive workplace environment

Protect yourself, your team, and your company through policy awareness and compliance.""",
        "tags": ["HR", "policy", "harassment", "discrimination", "compliance", "workplace", "FMLA", "EAP"]
    },

    # New Hire Orientation
    "safety_orientation": {
        "short": "Complete essential safety orientation for new construction employees. This course covers company safety policies, hazard recognition, emergency procedures, and your responsibilities for maintaining a safe workplace from day one.",
        "long": """Complete essential safety orientation for new construction employees. This course covers company safety policies, hazard recognition, emergency procedures, and your responsibilities for maintaining a safe workplace from day one.

Every new employee needs to understand safety expectations before starting work. This orientation provides the foundation of safety knowledge required to work safely and contribute to a culture of safety.

From personal protective equipment to emergency response, this training covers the essentials that every construction worker needs to know.

Key Learning Objectives:
1. Understand company safety commitment and policies
2. Recognize common construction hazards
3. Know required personal protective equipment
4. Follow safe work practices for your tasks
5. Report hazards and unsafe conditions
6. Respond appropriately to emergencies
7. Understand your rights and responsibilities

Start your employment with the safety knowledge that protects you and your coworkers.""",
        "tags": ["safety", "orientation", "new hire", "construction", "PPE", "hazards", "emergency"]
    },
}


def get_template_key(title, category):
    """Determine which template to use based on title and category"""
    title_lower = title.lower()
    category_lower = category.lower() if category else ""

    # Check for specific course patterns
    if "extreme ownership" in title_lower:
        return "extreme_ownership"
    elif "values" in title_lower and ("driven" in title_lower or "coach k" in title_lower):
        return "values_driven"
    elif "team morale" in title_lower or "morale" in title_lower:
        return "team_morale"
    elif "team management" in title_lower or "building an effective team" in title_lower:
        return "team_management"
    elif "lockout" in title_lower or "tagout" in title_lower or "loto" in title_lower:
        return "lockout_tagout"
    elif "arc flash" in title_lower or "nfpa 70" in title_lower:
        return "arc_flash"
    elif "fall protection" in title_lower:
        return "fall_protection"
    elif "scaffold" in title_lower:
        return "scaffolding"
    elif "safety coordinator" in title_lower:
        return "safety_coordinator"
    elif "hazard communication" in title_lower or "ghs" in title_lower or "sds" in title_lower or "container label" in title_lower:
        return "hazard_communication"
    elif "confined space" in title_lower:
        return "confined_space"
    elif "lean" in title_lower and ("construction" in title_lower or "productivity" in title_lower):
        return "lean_construction"
    elif "waste" in title_lower and ("elimination" in title_lower or "eight" in title_lower or "construction" in title_lower):
        return "waste_elimination"
    elif "pull planning" in title_lower or "sticky note" in title_lower:
        return "pull_planning"
    elif "emotional intelligence" in title_lower or "eq" in title_lower or "self-awareness" in title_lower or "empathy" in title_lower or "self-regulation" in title_lower or "social skills" in title_lower:
        return "emotional_intelligence"
    elif "present" in title_lower and ("art" in title_lower or "delivering" in title_lower or "slides" in title_lower):
        return "presenting"
    elif "time management" in title_lower or "time wasters" in title_lower:
        return "time_management"
    elif "project planning" in title_lower or "execution" in title_lower:
        return "project_planning"
    elif "documentation" in title_lower or "reporting" in title_lower:
        return "documentation"
    elif "performance review" in title_lower or "performance management" in title_lower:
        return "performance_reviews"
    elif "corrective counseling" in title_lower or "disciplinary" in title_lower:
        return "corrective_counseling"
    elif "procore" in title_lower:
        return "procore"
    elif "viewpoint" in title_lower or "vista" in title_lower or "change order" in title_lower:
        return "viewpoint"
    elif "field leadership" in title_lower or "foreman" in title_lower:
        return "field_leadership"
    elif "coordinat" in title_lower and "trade" in title_lower:
        return "trade_coordination"
    elif "jobsite efficiency" in title_lower or "productivity" in title_lower:
        return "jobsite_efficiency"
    elif "quality control" in title_lower or "quality" in title_lower:
        return "quality_control"
    elif "harassment" in title_lower or "discrimination" in title_lower or "fmla" in title_lower or "eap" in title_lower or "substance abuse" in title_lower or "policy" in title_lower:
        return "workplace_policy"
    elif "orientation" in title_lower or "new hire" in title_lower:
        return "safety_orientation"

    # Category-based defaults
    if "safety" in category_lower:
        return "safety_orientation"
    elif "lean" in category_lower:
        return "lean_construction"
    elif "leadership" in category_lower:
        return "field_leadership"
    elif "emotional" in category_lower:
        return "emotional_intelligence"
    elif "performance" in category_lower:
        return "performance_reviews"
    elif "software" in category_lower:
        return "procore"
    elif "planning" in category_lower or "productivity" in category_lower:
        return "project_planning"
    elif "documentation" in category_lower:
        return "documentation"
    elif "professional" in category_lower:
        return "presenting"
    elif "communication" in category_lower:
        return "team_management"

    return "field_leadership"  # Default


def generate_short_description(title, template_key):
    """Generate a short description (50-75 words)"""
    if template_key in DESCRIPTION_TEMPLATES:
        base = DESCRIPTION_TEMPLATES[template_key]["short"]
    else:
        base = DESCRIPTION_TEMPLATES["field_leadership"]["short"]

    # Customize with course title context
    return base


def generate_long_description(title, template_key):
    """Generate a long description (200-250 words)"""
    if template_key in DESCRIPTION_TEMPLATES:
        base = DESCRIPTION_TEMPLATES[template_key]["long"]
    else:
        base = DESCRIPTION_TEMPLATES["field_leadership"]["long"]

    return base


def generate_tags(title, category, template_key):
    """Generate search tags"""
    tags = set()

    # Add template tags
    if template_key in DESCRIPTION_TEMPLATES:
        tags.update(DESCRIPTION_TEMPLATES[template_key]["tags"])

    # Add category-based tags
    if category:
        tags.add(category.lower())

    # Add title-derived tags
    title_words = title.lower().split()
    important_words = {"leadership", "safety", "management", "construction", "electrical",
                       "planning", "quality", "training", "team", "project", "communication",
                       "lean", "procore", "viewpoint", "documentation", "coordination"}
    for word in title_words:
        if word in important_words:
            tags.add(word)

    return list(tags)


def generate_categories(title, existing_category):
    """Generate primary and sub categories"""
    title_lower = title.lower()

    # Define category hierarchy
    category_map = {
        "Safety": {
            "primary": "Safety & Compliance",
            "subcategories": ["Electrical Safety", "Fall Protection", "Hazard Communication", "Lockout/Tagout", "General Safety"]
        },
        "Leadership & Field Management": {
            "primary": "Leadership Development",
            "subcategories": ["Field Leadership", "Team Management", "Values & Culture", "Communication"]
        },
        "Lean Construction": {
            "primary": "Lean & Productivity",
            "subcategories": ["Lean Principles", "Waste Elimination", "Pull Planning", "Continuous Improvement"]
        },
        "Emotional Intelligence": {
            "primary": "Professional Skills",
            "subcategories": ["Emotional Intelligence", "Self-Awareness", "Communication", "Relationships"]
        },
        "Professional Development": {
            "primary": "Professional Skills",
            "subcategories": ["Presentation Skills", "Career Development", "Business Skills"]
        },
        "Construction Software": {
            "primary": "Technology & Tools",
            "subcategories": ["Procore", "ViewPoint", "Software Training"]
        },
        "Project Planning & Productivity": {
            "primary": "Project Management",
            "subcategories": ["Planning", "Scheduling", "Time Management", "Productivity"]
        },
        "Documentation & Compliance": {
            "primary": "Project Management",
            "subcategories": ["Documentation", "Compliance", "Reporting"]
        },
        "Performance Management": {
            "primary": "Leadership Development",
            "subcategories": ["Performance Reviews", "Coaching", "Feedback"]
        },
        "Communication & Coaching": {
            "primary": "Professional Skills",
            "subcategories": ["Communication", "Coaching", "Mentoring"]
        }
    }

    # Get mapping based on existing category
    if existing_category and existing_category in category_map:
        mapping = category_map[existing_category]
        primary = mapping["primary"]

        # Determine subcategory from title
        subcategory = mapping["subcategories"][0]  # Default to first
        for sub in mapping["subcategories"]:
            if sub.lower() in title_lower:
                subcategory = sub
                break
    else:
        primary = existing_category or "General"
        subcategory = "Training"

    return primary, subcategory


def process_catalog(input_csv, output_xlsx):
    """Process the catalog and generate descriptions"""

    # Read existing catalog
    courses = []
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('title'):  # Skip empty rows
                courses.append(row)

    print(f"Processing {len(courses)} courses...")

    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Course Catalog"

    # Define headers
    headers = [
        "Course ID", "Filename", "Title",
        "Short Description (50-75 words)", "Long Description (200-250 words)",
        "Primary Category", "Sub Category",
        "Skill Level Set", "Proficiency Level",
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

        # Determine template
        template_key = get_template_key(title, existing_category)

        # Generate descriptions
        short_desc = generate_short_description(title, template_key)
        long_desc = generate_long_description(title, template_key)

        # Generate categories
        primary_cat, sub_cat = generate_categories(title, existing_category)

        # Generate tags
        tags = generate_tags(title, existing_category, template_key)

        # Write row
        row_data = [
            course.get('course_id', ''),
            course.get('filename', ''),
            title,
            short_desc,
            long_desc,
            primary_cat,
            sub_cat,
            existing_category,
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
    column_widths = [15, 40, 40, 60, 100, 20, 20, 25, 15, 30, 10, 50]
    for col, width in enumerate(column_widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = width

    # Freeze top row
    ws.freeze_panes = 'A2'

    # Save workbook
    wb.save(output_xlsx)
    print(f"Created: {output_xlsx}")
    print(f"Total courses processed: {len(courses)}")

    return len(courses)


if __name__ == "__main__":
    input_file = r"C:\Users\tewing\Documents\Projects\GSL-Operations-Framework\deliverables\scorm-catalog\SCORM_COURSE_CATALOG.csv"
    output_file = r"C:\Users\tewing\Desktop\Claude Projects\SOPs For Review\SCORM_Course_Descriptions.xlsx"

    process_catalog(input_file, output_file)
