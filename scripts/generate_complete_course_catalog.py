"""
Generate Complete Course Catalog with Skills Mapping and Descriptions

Includes:
- Complete chain: Course → Tab → SOPs → Roles → MDs → Skill Level Sets → Skills
- Short descriptions (50-75 words) mentioning skills learned
- Long descriptions (200-250 words) with learning objectives tied to skills
- Categories, subcategories, and tags
"""

import csv
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

# =============================================================================
# ROLE DEFINITIONS
# =============================================================================

ROLE_SKILLS = {
    "FE": {"name": "Field Employee (Journeyman/Apprentice)", "md": "MD 9.2"},
    "FL": {"name": "Field Leadership (Foreman)", "md": "MD 9.3"},
    "GS": {"name": "General Superintendent", "md": "MD 9.4"},
    "PM": {"name": "Project Manager", "md": "MD 9.5"},
    "BM": {"name": "Branch Manager", "md": "MD 9.6"},
    "EST": {"name": "Estimator", "md": "MD 9.7"},
    "CM": {"name": "Contract Manager", "md": "MD 9.14"},
    "PUR": {"name": "Purchasing", "md": "MD 9.16"},
}

# =============================================================================
# DESCRIPTION GENERATOR
# =============================================================================

def generate_descriptions(title, mapping):
    """Generate short and long descriptions based on course mapping and skills"""

    skills = mapping.get("skills", [])
    skill_level_sets = mapping.get("skill_level_sets", [])
    roles = mapping.get("roles", [])
    sops = mapping.get("sops", [])
    tab_name = mapping.get("tab_name", "")

    title_lower = title.lower()

    # Build role names for descriptions
    role_names = []
    for r in roles[:3]:  # Limit to 3 roles for readability
        if r in ROLE_SKILLS:
            role_names.append(ROLE_SKILLS[r]["name"].split(" (")[0])  # Just the main name
    roles_text = ", ".join(role_names) if role_names else "field personnel"

    # Build skills text
    skills_text = ", ".join(skills[:4]) if skills else "essential job skills"
    all_skills_text = ", ".join(skills) if skills else "essential skills"

    # =============================================================================
    # SAFETY COURSES
    # =============================================================================

    # Lockout Tagout
    if "lockout" in title_lower or "tagout" in title_lower or "loto" in title_lower:
        if "abnormal" in title_lower:
            short = f"Learn proper abnormal lockout removal procedures for situations when the original lock owner is unavailable. This course develops your {skills_text} competencies required for {roles_text} per GSL SOPs {', '.join(sops[:2])}."
            long = f"""Learn proper abnormal lockout removal procedures for situations when the original lock owner is unavailable. This course develops critical safety competencies required for {roles_text} as defined in Management Directives and SOPs.

This training addresses one of the most dangerous scenarios in electrical safety—removing a lock when the original worker cannot be located. Improper handling can result in serious injury or death.

Skills You Will Learn:
- {chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Understand when abnormal lockout removal is permitted
2. Follow the multi-step verification process before removal
3. Document all abnormal removal activities properly
4. Coordinate with supervision and safety personnel
5. Verify de-energized condition after lock removal
6. Apply lessons learned to prevent future abnormal situations
7. Demonstrate competency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions and contributes to your {', '.join(skill_level_sets)} proficiency."""

        elif "complex" in title_lower:
            short = f"Master complex lockout/tagout procedures for equipment with multiple energy sources. This course builds your {skills_text} skills required for {roles_text} to safely isolate complex systems per GSL safety SOPs."
            long = f"""Master complex lockout/tagout procedures for equipment with multiple energy sources. This course builds critical competencies required for {roles_text} working with sophisticated electrical and mechanical systems.

Complex LOTO situations involve multiple isolation points, various energy types, and coordination between multiple workers. This training ensures you can handle these challenging scenarios safely.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Identify all energy sources in complex equipment
2. Develop comprehensive LOTO procedures for multi-source systems
3. Coordinate lockout activities with multiple workers
4. Verify complete isolation of all energy sources
5. Document complex LOTO procedures properly
6. Communicate effectively with all affected personnel
7. Demonstrate mastery of {skills_text}

Completion of this training satisfies requirements for {roles_text} positions and advances your {', '.join(skill_level_sets)} competency level."""

        elif "simple" in title_lower:
            short = f"Learn fundamental lockout/tagout procedures for single-source energy isolation. This course establishes your {skills_text} foundation required for {roles_text} per GSL safety standards and OSHA requirements."
            long = f"""Learn fundamental lockout/tagout procedures for single-source energy isolation. This course establishes the safety foundation required for all {roles_text} working with electrical equipment.

Simple LOTO procedures form the basis of all energy control activities. Mastering these fundamentals is essential before advancing to complex isolation scenarios.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Understand hazardous energy types and their dangers
2. Apply the six-step LOTO procedure correctly
3. Select and apply appropriate locks and tags
4. Verify de-energized condition before work begins
5. Release equipment from LOTO safely
6. Document all LOTO activities properly
7. Build foundation in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions and establishes your {', '.join(skill_level_sets)} competency baseline."""

        elif "return" in title_lower or "service" in title_lower:
            short = f"Learn proper return-to-service procedures after lockout/tagout completion. This course develops your {skills_text} competencies to safely restore equipment to operation per GSL SOPs."
            long = f"""Learn proper return-to-service procedures after lockout/tagout completion. This course develops competencies required for {roles_text} to safely restore equipment to normal operation.

Return to service is as critical as the initial lockout. Improper procedures can result in unexpected equipment operation and serious injuries.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Verify all work is complete and tools removed
2. Ensure all personnel are clear of equipment
3. Remove locks and tags in proper sequence
4. Restore energy sources safely
5. Verify proper equipment operation
6. Document return-to-service activities
7. Demonstrate proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""

        elif "verif" in title_lower or "de-energiz" in title_lower:
            short = f"Master verification techniques for confirming de-energized conditions. This course builds your {skills_text} competencies essential for {roles_text} to ensure electrically safe work conditions."
            long = f"""Master verification techniques for confirming de-energized conditions. This course builds essential competencies for {roles_text} to ensure safe working conditions before beginning any electrical work.

Verification is the critical step that confirms energy isolation is complete. Never assume equipment is de-energized—always verify.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Select appropriate test equipment for verification
2. Test the tester before and after use
3. Apply proper verification techniques for various voltages
4. Document verification results properly
5. Recognize and respond to unexpected energized conditions
6. Establish electrically safe work conditions
7. Demonstrate competency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""

        else:  # General LOTO
            short = f"Master critical lockout/tagout procedures to protect against hazardous energy. This course develops your {skills_text} competencies required for {roles_text} per OSHA standards and GSL SOPs."
            long = f"""Master critical lockout/tagout procedures to protect yourself and coworkers from hazardous energy. This course develops the safety competencies required for {roles_text} as defined in GSL Management Directives and SOPs.

Lockout/Tagout procedures prevent serious injuries and fatalities from unexpected equipment energization. This training ensures you can properly control hazardous energy.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Identify all types of hazardous energy
2. Apply proper lockout/tagout procedures
3. Verify de-energized conditions
4. Coordinate multi-person LOTO activities
5. Document all energy control activities
6. Respond to abnormal situations appropriately
7. Demonstrate proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions and contributes to your {', '.join(skill_level_sets)} proficiency level."""

        return short, long

    # Arc Flash / NFPA 70E
    if "arc flash" in title_lower or "nfpa 70" in title_lower:
        if "ppe" in title_lower:
            short = f"Learn proper selection and use of arc flash PPE based on incident energy analysis. This course develops your {skills_text} competencies required for {roles_text} working near energized equipment."
            long = f"""Learn proper selection and use of arc flash personal protective equipment based on incident energy analysis. This course develops critical safety competencies for {roles_text} who work near energized electrical equipment.

Arc flash PPE is your last line of defense against thermal injuries. Proper selection and use can mean the difference between life and death.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Understand arc flash incident energy ratings
2. Match PPE to calculated incident energy levels
3. Inspect and maintain arc-rated clothing properly
4. Don and doff PPE correctly
5. Understand PPE limitations and replacement criteria
6. Layer PPE appropriately for protection
7. Demonstrate proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""

        elif "boundar" in title_lower:
            short = f"Understand NFPA 70E approach boundaries and their requirements for electrical safety. This course builds your {skills_text} knowledge essential for {roles_text} working near energized equipment."
            long = f"""Understand NFPA 70E approach boundaries and their requirements for electrical safety. This course builds essential knowledge for {roles_text} who must work near energized electrical equipment.

Approach boundaries define the protective zones around energized equipment. Understanding these boundaries keeps you and your coworkers safe.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Identify the three NFPA 70E approach boundaries
2. Understand shock and arc flash boundary differences
3. Determine boundary distances for various voltage levels
4. Apply boundary requirements in the field
5. Control access to work areas appropriately
6. Document boundary considerations in work planning
7. Demonstrate competency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""

        else:  # General Arc Flash
            short = f"Understand arc flash hazards and NFPA 70E protection requirements. This course develops your {skills_text} competencies required for {roles_text} to assess and control arc flash risks."
            long = f"""Understand arc flash hazards and NFPA 70E protection requirements. This course develops critical safety competencies for {roles_text} who work with or near electrical equipment.

Arc flash incidents release tremendous energy causing severe burns and other injuries. This training ensures you understand the hazards and protective measures.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Understand arc flash physics and consequences
2. Identify approach boundaries and requirements
3. Perform basic arc flash risk assessments
4. Select appropriate PPE for the hazard level
5. Apply safe work practices around energized equipment
6. Recognize when energized work is permitted
7. Build proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions and contributes to your {', '.join(skill_level_sets)} competency."""

        return short, long

    # Fall Protection
    if "fall protection" in title_lower:
        short = f"Learn essential fall protection principles for construction environments. This course develops your {skills_text} competencies required for {roles_text} working at heights."
        long = f"""Learn essential fall protection principles for construction environments. This course develops critical safety competencies for {roles_text} who work at elevated locations.

Falls are the leading cause of death in construction. This training ensures you understand fall hazards and the systems designed to protect you.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Recognize fall hazards in construction environments
2. Understand different fall protection systems
3. Inspect and maintain personal fall protection equipment
4. Calculate fall distances and clearance requirements
5. Set up and use anchor points properly
6. Follow OSHA fall protection requirements
7. Demonstrate proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""
        return short, long

    # Scaffolding
    if "scaffold" in title_lower:
        short = f"Master scaffold safety for construction environments. This course develops your {skills_text} competencies required for {roles_text} working on or around scaffolding systems."
        long = f"""Master scaffold safety for construction environments. This course develops critical competencies for {roles_text} who work on or around scaffolding systems.

Scaffolding provides essential access but creates serious hazards when used improperly. This training ensures you can work safely on scaffolds.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Identify different scaffold types and applications
2. Understand scaffold erection and inspection requirements
3. Access and egress scaffolds safely
4. Know load capacity requirements
5. Work safely on scaffold platforms
6. Recognize and report scaffold hazards
7. Build proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""
        return short, long

    # Safety Coordinator
    if "safety coordinator" in title_lower:
        short = f"Develop safety coordinator competencies for construction projects. This course builds your {skills_text} abilities required for {roles_text} managing jobsite safety programs."
        long = f"""Develop safety coordinator competencies for construction projects. This course builds the professional skills required for {roles_text} who manage safety programs on GSL projects.

Safety coordinators play a vital role in protecting workers. This training provides the knowledge needed to manage safety programs effectively.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Understand safety coordinator responsibilities
2. Conduct effective safety orientations and meetings
3. Perform thorough jobsite inspections
4. Investigate incidents and accidents properly
5. Manage injury cases and documentation
6. Prepare for regulatory inspections
7. Demonstrate competency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions and advances your {', '.join(skill_level_sets)} proficiency."""
        return short, long

    # Safety Orientation / New Hire
    if "new hire" in title_lower or ("safety" in title_lower and "orientation" in title_lower):
        short = f"Complete essential safety orientation for GSL employees. This course establishes your {skills_text} foundation required for all personnel per GSL safety policies and OSHA requirements."
        long = f"""Complete essential safety orientation for GSL employees. This course establishes the safety foundation required for all personnel before beginning work at GSL Electric.

Every employee must understand safety expectations and procedures. This orientation provides the essential knowledge you need from day one.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support GSL safety requirements under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Understand GSL's commitment to safety
2. Recognize common construction hazards
3. Know required personal protective equipment
4. Follow safe work practices
5. Report hazards and unsafe conditions
6. Respond appropriately to emergencies
7. Establish foundation in {skills_text}

This training is required for all new employees within 30 days of hire."""
        return short, long

    # Hazard Communication / GHS
    if "hazard communication" in title_lower or "hazcom" in title_lower or "ghs" in title_lower or "sds" in title_lower or "chemical" in title_lower or "label" in title_lower:
        short = f"Understand hazard communication requirements for chemical safety. This course develops your {skills_text} competencies required for {roles_text} working with hazardous materials."
        long = f"""Understand hazard communication requirements for chemical safety. This course develops essential competencies for {roles_text} who may encounter hazardous materials on construction sites.

Chemical hazards are present on most construction sites. This training ensures you can identify hazards and protect yourself from exposures.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Understand the hazard communication program
2. Read and interpret GHS labels and pictograms
3. Locate and use Safety Data Sheets
4. Identify chemical hazards by type
5. Select appropriate PPE for chemical work
6. Follow proper handling procedures
7. Build proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""
        return short, long

    # Confined Space
    if "confined space" in title_lower:
        short = f"Learn permit-required confined space entry procedures. This course develops your {skills_text} competencies required for {roles_text} entering tanks, manholes, and other confined areas."
        long = f"""Learn permit-required confined space entry procedures. This course develops critical competencies for {roles_text} who may enter confined spaces during construction activities.

Confined spaces present unique hazards including atmospheric dangers and limited egress. This training ensures you understand entry requirements and procedures.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Identify confined spaces and permit requirements
2. Recognize atmospheric and physical hazards
3. Perform atmospheric monitoring
4. Complete entry permits properly
5. Understand entrant and attendant responsibilities
6. Plan for emergency rescue
7. Demonstrate competency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""
        return short, long

    # =============================================================================
    # LEAN CONSTRUCTION
    # =============================================================================

    if "lean" in title_lower or "waste" in title_lower and "construction" in title_lower:
        if "waste" in title_lower:
            short = f"Learn to identify and eliminate the eight wastes of construction. This course develops your {skills_text} competencies required for {roles_text} to improve project productivity."
            long = f"""Learn to identify and eliminate the eight wastes of construction. This course develops Lean competencies for {roles_text} responsible for improving project productivity and efficiency.

Studies show over 50% of construction activity is waste. This training helps you see waste clearly and take action to eliminate it.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Understand the eight wastes and their impact
2. Identify waste in current work processes
3. Apply specific techniques for each waste type
4. Engage your team in waste identification
5. Measure waste reduction results
6. Sustain improvements over time
7. Build proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions and advances your {', '.join(skill_level_sets)} competency."""

        elif "pull planning" in title_lower or "sticky note" in title_lower:
            short = f"Master pull planning techniques for construction scheduling. This course develops your {skills_text} competencies required for {roles_text} to create reliable, collaborative schedules."
            long = f"""Master pull planning techniques for construction scheduling. This course develops planning competencies for {roles_text} responsible for schedule development and coordination.

Pull planning creates reliable schedules through collaborative planning and commitment-based workflow. This approach dramatically improves schedule predictability.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Understand pull vs. push planning principles
2. Facilitate pull planning sessions
3. Identify and resolve constraints collaboratively
4. Use sticky note format for visual planning
5. Make and track reliable commitments
6. Conduct weekly work planning
7. Demonstrate proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""

        else:  # General Lean
            short = f"Discover how Lean principles transform construction project delivery. This course develops your {skills_text} competencies required for {roles_text} to improve efficiency and productivity."
            long = f"""Discover how Lean principles transform construction project delivery. This course develops Lean competencies for {roles_text} seeking to improve project outcomes through systematic waste elimination.

Lean Construction adapts manufacturing principles to construction's unique challenges. This training shows how these principles improve results.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Understand Lean principles and their construction application
2. Identify and eliminate waste in construction
3. Apply pull planning to coordinate work
4. Use visual management for communication
5. Implement continuous improvement practices
6. Engage field teams in problem-solving
7. Build proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions and advances your {', '.join(skill_level_sets)} competency."""

        return short, long

    # =============================================================================
    # VALUES-DRIVEN LEADERSHIP / COACH K
    # =============================================================================

    if "values" in title_lower and "driven" in title_lower or "coach k" in title_lower:
        short = f"Through real-life stories and proven strategies, learn to lead with trust, respect, and accountability. This course develops your {skills_text} competencies required for {roles_text} to build high-performing teams."
        long = f"""Through real-life stories and proven strategies, Coach K teaches how to lead with trust, respect, communication, and responsibility. This course develops leadership competencies for {roles_text} who build and lead teams.

Successful leaders don't just focus on results—they build strong relationships, empower individuals, and create cultures where every person matters.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Lead with integrity and build trust
2. Empower team members to take initiative
3. Cultivate meaningful relationships
4. Define and communicate core values
5. Foster accountability throughout your team
6. Drive purpose and meaning in work
7. Demonstrate proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions and advances your {', '.join(skill_level_sets)} competency level."""
        return short, long

    # =============================================================================
    # EXTREME OWNERSHIP
    # =============================================================================

    if "extreme ownership" in title_lower:
        short = f"Learn the core principles of Extreme Ownership from Navy SEAL leadership methodology. This course develops your {skills_text} competencies required for {roles_text} to take complete responsibility for outcomes."
        long = f"""Learn the core principles of Extreme Ownership from Navy SEAL leadership methodology. This course develops leadership competencies for {roles_text} who must own their team's performance and mission success.

There are no bad teams, only bad leaders. This mindset shift transforms how you approach challenges and lead your people.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Take complete ownership of outcomes
2. Eliminate blame and excuses
3. Build trust through accountability
4. Empower subordinates to make decisions
5. Lead up and down the chain of command
6. Prioritize and execute under pressure
7. Demonstrate mastery of {skills_text}

Completion of this training satisfies requirements for {roles_text} positions and advances your {', '.join(skill_level_sets)} competency."""
        return short, long

    # =============================================================================
    # FIELD LEADERSHIP
    # =============================================================================

    if "field leadership" in title_lower or "foreman" in title_lower:
        short = f"Build essential skills for effective field leadership in construction. This course develops your {skills_text} competencies required for {roles_text} to lead crews successfully."
        long = f"""Build essential skills for effective field leadership in construction. This course develops the core competencies required for {roles_text} to lead crews successfully from mobilization through closeout.

Field leadership requires technical knowledge, people skills, and business awareness. This training provides the comprehensive foundation for field leadership success.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Understand field leadership roles and responsibilities
2. Plan and organize work for productivity
3. Lead and motivate diverse crews
4. Communicate with stakeholders professionally
5. Manage time, priorities, and demands
6. Ensure quality and safety
7. Build proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions and advances your {', '.join(skill_level_sets)} competency level."""
        return short, long

    # =============================================================================
    # EMOTIONAL INTELLIGENCE
    # =============================================================================

    if "emotional intelligence" in title_lower or " eq" in title_lower or "self-awareness" in title_lower or "empathy" in title_lower or "social skills" in title_lower or "self-regulation" in title_lower:
        short = f"Develop emotional intelligence skills essential for effective leadership. This course builds your {skills_text} competencies required for {roles_text} to connect with teams and navigate challenges."
        long = f"""Develop emotional intelligence skills essential for effective leadership. This course builds EQ competencies for {roles_text} who must connect with teams and navigate challenging interpersonal situations.

Emotional Intelligence is often more important than technical skills for leadership success. The ability to understand and manage emotions is fundamental to effective leadership.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Understand emotional intelligence components
2. Develop greater self-awareness
3. Practice self-regulation techniques
4. Build empathy through understanding others
5. Enhance social skills for better relationships
6. Apply EQ in difficult conversations
7. Demonstrate proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions and advances your {', '.join(skill_level_sets)} competency."""
        return short, long

    # =============================================================================
    # PERFORMANCE MANAGEMENT
    # =============================================================================

    if "performance" in title_lower and ("review" in title_lower or "management" in title_lower or "counseling" in title_lower):
        short = f"Learn to conduct effective performance conversations that improve results. This course develops your {skills_text} competencies required for {roles_text} managing employee performance."
        long = f"""Learn to conduct effective performance conversations that improve results. This course develops performance management competencies for {roles_text} who evaluate and develop their team members.

Performance conversations are opportunities to recognize achievements and align employees with goals. Done well, they strengthen relationships and improve results.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Prepare thoroughly for performance conversations
2. Provide specific, balanced feedback
3. Discuss development needs constructively
4. Set meaningful performance goals
5. Handle defensive reactions professionally
6. Document conversations properly
7. Demonstrate proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""
        return short, long

    # =============================================================================
    # COMMUNICATION
    # =============================================================================

    if "communication" in title_lower:
        short = f"Master effective communication skills for construction leadership. This course develops your {skills_text} competencies required for {roles_text} to communicate clearly with all stakeholders."
        long = f"""Master effective communication skills for construction leadership. This course develops communication competencies for {roles_text} who must interact effectively with crews, management, and clients.

Clear communication prevents misunderstandings, improves coordination, and builds strong working relationships across all levels of the organization.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Communicate clearly and concisely
2. Adapt communication style to the audience
3. Listen actively to understand others
4. Provide constructive feedback
5. Handle difficult conversations professionally
6. Document communications appropriately
7. Build proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""
        return short, long

    # =============================================================================
    # PROJECT PLANNING / PRODUCTIVITY
    # =============================================================================

    if "project planning" in title_lower or "productivity" in title_lower or "time management" in title_lower:
        short = f"Learn practical planning and productivity techniques for construction. This course develops your {skills_text} competencies required for {roles_text} to accomplish more effectively."
        long = f"""Learn practical planning and productivity techniques for construction. This course develops planning competencies for {roles_text} responsible for project execution and efficiency.

Effective planning and time management directly impact project success. This training provides practical tools for the construction environment.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Plan work systematically for productivity
2. Prioritize tasks using proven frameworks
3. Manage time effectively
4. Minimize common distractions and waste
5. Delegate appropriately
6. Build sustainable productivity habits
7. Demonstrate proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""
        return short, long

    # =============================================================================
    # CONSTRUCTION SOFTWARE
    # =============================================================================

    if "accubid" in title_lower or "viewpoint" in title_lower or "vista" in title_lower or "procore" in title_lower or "job plan" in title_lower:
        short = f"Learn essential construction software skills for your role. This course develops your {skills_text} competencies required for {roles_text} to use GSL's technology systems effectively."
        long = f"""Learn essential construction software skills for your role. This course develops technology competencies for {roles_text} who must use GSL's software systems for project management and administration.

Construction software streamlines project administration and improves information flow. This training ensures you can use these tools effectively.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Navigate the software interface efficiently
2. Perform core functions for your role
3. Enter and retrieve information accurately
4. Generate required reports
5. Collaborate with others using the system
6. Troubleshoot common issues
7. Build proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""
        return short, long

    # =============================================================================
    # DOCUMENTATION
    # =============================================================================

    if "documentation" in title_lower or "reporting" in title_lower or "document management" in title_lower:
        short = f"Learn essential documentation practices for construction projects. This course develops your {skills_text} competencies required for {roles_text} to maintain proper project records."
        long = f"""Learn essential documentation practices for construction projects. This course develops documentation competencies for {roles_text} who must maintain accurate project records.

Proper documentation protects against claims, supports change orders, and provides information for management decisions. This training covers professional documentation practices.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Understand documentation requirements
2. Write clear, accurate daily reports
3. Manage RFIs and submittals effectively
4. Document changes properly
5. Maintain organized project files
6. Use photos to supplement records
7. Demonstrate proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""
        return short, long

    # =============================================================================
    # PROFESSIONAL DEVELOPMENT / PRESENTING
    # =============================================================================

    if "presenting" in title_lower or "presentation" in title_lower:
        short = f"Master the art of professional presenting. This course develops your {skills_text} competencies required for {roles_text} to communicate ideas effectively to groups."
        long = f"""Master the art of professional presenting. This course develops presentation competencies for {roles_text} who must communicate ideas effectively to teams, management, and clients.

The ability to present clearly and confidently is essential for career advancement. This training provides a systematic approach to effective presentations.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills])}

These skills directly support your responsibilities under SOPs {', '.join(sops)}.

Key Learning Objectives:
1. Plan presentations with clear objectives
2. Structure content for maximum impact
3. Design effective visual aids
4. Prepare to reduce anxiety
5. Deliver with confidence
6. Engage audiences effectively
7. Build proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions."""
        return short, long

    # =============================================================================
    # DEFAULT
    # =============================================================================

    short = f"Build essential construction industry skills through this training module. This course develops your {skills_text} competencies required for {roles_text} to perform effectively in their roles."
    long = f"""Build essential construction industry skills through this training module. This course develops competencies for {roles_text} as defined in GSL Management Directives and SOPs.

This training combines technical knowledge with practical application to improve your effectiveness in field operations.

Skills You Will Learn:
{chr(10).join(['- ' + s for s in skills]) if skills else '- Core job competencies'}

These skills directly support your responsibilities under SOPs {', '.join(sops) if sops else 'applicable to your role'}.

Key Learning Objectives:
1. Understand core concepts and best practices
2. Apply knowledge to real-world situations
3. Develop skills that improve performance
4. Build competency through practice
5. Meet industry standards and requirements
6. Contribute to team and project success
7. Demonstrate proficiency in {skills_text}

Completion of this training satisfies requirements for {roles_text} positions and contributes to your professional development."""

    return short, long


# =============================================================================
# COURSE MAPPING (Same as before but simplified for reference)
# =============================================================================

def get_course_mapping(title):
    """Get course mapping - simplified version calling the main mapping logic"""
    # Import the mapping function from the other script
    import sys
    sys.path.insert(0, r"C:\Users\tewing\Documents\Projects\GSL-Operations-Framework\scripts")
    from build_course_skills_mapping import get_course_mapping as get_mapping
    return get_mapping(title)


def get_role_names(role_codes):
    """Convert role codes to names"""
    return [ROLE_SKILLS[r]["name"] for r in role_codes if r in ROLE_SKILLS]


def get_mds(role_codes):
    """Get management directives for roles"""
    return list(dict.fromkeys([ROLE_SKILLS[r]["md"] for r in role_codes if r in ROLE_SKILLS]))


def process_catalog(input_csv, output_xlsx):
    """Process catalog and generate complete output"""

    # Read catalog
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
    ws.title = "Complete Course Catalog"

    # Headers
    headers = [
        "Course ID",
        "Title",
        "Short Description (50-75 words)",
        "Long Description (200-250 words)",
        "Training Tab",
        "Tab Name",
        "SOPs",
        "Roles",
        "Management Directives",
        "Skill Level Sets",
        "Skills Learned",
        "Proficiency Level",
        "Tags",
        "Filename"
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

    # Process courses
    for idx, course in enumerate(courses, 2):
        title = course.get('title', '')

        # Get mapping
        mapping = get_course_mapping(title)

        # Get MDs
        mds = get_mds(mapping["roles"])

        # Get role names
        role_names = get_role_names(mapping["roles"])

        # Remove duplicates
        unique_skills = list(dict.fromkeys(mapping["skills"]))
        unique_sls = list(dict.fromkeys(mapping["skill_level_sets"]))

        # Generate descriptions
        short_desc, long_desc = generate_descriptions(title, mapping)

        # Generate tags
        tags = set()
        tags.update([s.lower() for s in unique_sls])
        tags.update([s.lower() for s in unique_skills[:5]])
        if mapping["tab_name"]:
            tags.add(mapping["tab_name"].lower())

        # Write row
        row_data = [
            course.get('course_id', ''),
            title,
            short_desc,
            long_desc,
            mapping["training_tab"],
            mapping["tab_name"],
            "; ".join(mapping["sops"]),
            "; ".join(role_names),
            "; ".join(mds),
            "; ".join(unique_sls),
            "; ".join(unique_skills),
            course.get('proficiency_level', ''),
            ", ".join(list(tags)[:12]),
            course.get('filename', '')
        ]

        for col, value in enumerate(row_data, 1):
            cell = ws.cell(row=idx, column=col, value=value)
            cell.border = thin_border
            cell.alignment = Alignment(vertical='top', wrap_text=True)

    # Column widths
    column_widths = [15, 45, 70, 120, 20, 25, 40, 55, 30, 40, 60, 12, 50, 40]
    for col, width in enumerate(column_widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = width

    # Freeze header
    ws.freeze_panes = 'A2'

    # Save
    wb.save(output_xlsx)
    print(f"Created: {output_xlsx}")
    print(f"Total courses: {len(courses)}")

    return len(courses)


if __name__ == "__main__":
    input_file = r"C:\Users\tewing\Documents\Projects\GSL-Operations-Framework\deliverables\scorm-catalog\SCORM_COURSE_CATALOG.csv"
    output_file = r"C:\Users\tewing\Desktop\Claude Projects\SOPs For Review\SCORM_Complete_Course_Catalog.xlsx"

    process_catalog(input_file, output_file)
