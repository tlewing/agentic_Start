"""Merge Batch 2 taxonomy recommendations into the main recommendations file."""
import json, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DATA_DIR = r'C:\Users\tewing\OneDrive - GSL Electric\Projects\GSL-Operations-Framework\data'
RECS_PATH = os.path.join(DATA_DIR, 'scorm_taxonomy_recommendations.json')
INDEX_PATH = os.path.join(DATA_DIR, 'scorm_course_index.json')

with open(RECS_PATH, 'r', encoding='utf-8') as f:
    recs = json.load(f)

batch2 = [
    {
        "batch": 2, "status": "done",
        "course": "1.0 Coach K Teaches Values-Driven Leadership",
        "source_file": "1-0-coach-k-teaches-values-driven-leadership-scorm12-xpvxgbur.zip",
        "content_summary": "Opening lesson of the Values-Driven Leadership series based on Coach K (Mike Krzyzewski). Introduces leading through personal values. No transcript or video in package.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "SharePoint/Stream — no video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Begin your values-driven leadership journey with Coach K's foundational lesson on leading through personal values and conviction.",
        "long_description": "This course is the opening lesson in the Values-Driven Leadership series, inspired by Coach Mike Krzyzewski's leadership philosophy. It introduces the core principle that effective leadership begins with knowing and living your personal values.\n\nThe lesson sets the stage for the complete VDL series, which covers topics from team building to talent retention. Designed for all field leaders and anyone developing their leadership identity. On completion, you earn the skill Values-Driven Leadership.\n\nThis is a Foundational-level course with no prerequisites.",
        "category": {"value": "Leadership > Leadership Fundamentals", "label": "EXISTING", "rationale": "Opening lesson of a foundational leadership series."},
        "tags": [
            {"value": "Values-Driven", "label": "EXISTING"},
            {"value": "Leadership", "label": "EXISTING"},
            {"value": "Values", "label": "EXISTING"},
            {"value": "Mission-Focused", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [
            {"skill": "Values-Driven Leadership", "skill_category": "Leadership", "scale_set": "Leadership", "level": "[LEVEL NEEDED \u2014 Leadership scale set has no levels defined]", "label": "EXISTING", "rationale": "Opening lesson of the VDL series. Existing skill."}
        ],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Introductory lesson. No prerequisites."},
        "target_roles_draft": [
            {"fragment": "Academy/Values-Driven Leadership/[level TBD]", "roles": ["Leadman", "Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders developing their leadership philosophy."}
        ],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video. Description based on title, series context, and asset filenames.",
        "open_questions": ["Part of VDL series \u2014 verify this is the intended series opener."]
    },
    {
        "batch": 2, "status": "done",
        "course": "11.1 Recruit & Retain All-Star Talent",
        "source_file": "11-1-recruit-retain-all-star-talent-scorm12-ap0eangm.zip",
        "content_summary": "Lesson 11.1 of the Values-Driven Leadership series. Covers strategies for recruiting top talent and retaining high performers. No transcript or video.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "SharePoint/Stream \u2014 no video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Learn strategies for recruiting top talent and retaining your best performers to build a winning team.",
        "long_description": "This course is lesson 11.1 of the Values-Driven Leadership series. It covers how leaders can attract and recruit talented individuals, create an environment where high performers want to stay, and build a culture that naturally retains its best people.\n\nDesigned for foremen, superintendents, and project managers involved in hiring and retention decisions. On completion, you earn the skill Values-Driven Leadership.\n\nThis is an Intermediate-level lesson that builds on the earlier VDL series foundations.",
        "category": {"value": "Leadership > Workforce Management", "label": "EXISTING", "rationale": "Talent recruitment and retention is a workforce management function."},
        "tags": [
            {"value": "Values-Driven", "label": "EXISTING"},
            {"value": "Leadership", "label": "EXISTING"},
            {"value": "Succession Planning", "label": "EXISTING"},
            {"value": "Team Building", "label": "EXISTING"},
            {"value": "Difficulty: Intermediate", "label": "PROPOSED"}
        ],
        "skills_awarded": [
            {"skill": "Values-Driven Leadership", "skill_category": "Leadership", "scale_set": "Leadership", "level": "[LEVEL NEEDED \u2014 Leadership scale set has no levels defined]", "label": "EXISTING", "rationale": "Part of the VDL series. Existing skill."}
        ],
        "level_of_difficulty": {"value": "Intermediate", "rationale": "Lesson 11 of a series \u2014 assumes prior VDL content exposure."},
        "target_roles_draft": [
            {"fragment": "Academy/Values-Driven Leadership/[level TBD]", "roles": ["Foreman", "Superintendent", "Project Manager", "General Superintendent", "Branch Manager"], "scope": "Role-scoped", "note": "Leaders with hiring/retention influence."}
        ],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video. Description based on title and VDL series context.",
        "open_questions": ["Duplicate exists: values-driven-leadership-11-recruit-and-retain-all-stars-scorm12-dqqkpaaj.zip"]
    },
    {
        "batch": 2, "status": "done",
        "course": "A Commitment to Zero Broken Lives- New Hire Safety Orientation",
        "source_file": "3c1c9fac-b95f-4fad-b859-fe5a6a84824e.zip",
        "content_summary": "GSL Electric's new hire safety orientation. 'Zero Broken Lives' is GSL's safety commitment. Covers safety culture, expectations, and initial safety protocols. GUID filename.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "SharePoint/Stream \u2014 no video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "GSL Electric's safety orientation for new hires, built around our commitment to zero broken lives on every jobsite.",
        "long_description": "This course is GSL Electric's new hire safety orientation. It introduces new employees to GSL's safety culture and the 'Zero Broken Lives' commitment \u2014 the belief that every worker goes home safe every day. Topics include safety expectations, reporting procedures, personal protective equipment basics, and your role in maintaining a safe work environment.\n\nRequired for all new hires before their first day on a jobsite. On completion, you earn the skill Safety Responsibility.\n\nThis is a Foundational-level mandatory orientation course.",
        "category": {"value": "Employee Orientation", "label": "EXISTING", "rationale": "New hire orientation course."},
        "tags": [
            {"value": "Safety", "label": "EXISTING"},
            {"value": "safety culture", "label": "EXISTING"},
            {"value": "expectations & onboarding", "label": "EXISTING"},
            {"value": "safety protocols", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [
            {"skill": "Safety Responsibility", "skill_category": "Safety", "scale_set": "Safety", "level": "[LEVEL NEEDED \u2014 Safety scale set has no levels defined]", "label": "EXISTING", "rationale": "New hire safety orientation establishes safety responsibility. Existing skill."}
        ],
        "level_of_difficulty": {"value": "Foundational", "rationale": "New hire orientation \u2014 no prerequisites."},
        "target_roles_draft": [
            {"fragment": "Academy/Safety Responsibility/[level TBD]", "roles": ["Apprentice", "Journeyman", "Leadman", "Foreman", "Superintendent"], "scope": "Global", "note": "Mandatory for all new hires across all field roles."}
        ],
        "topic_timestamp_index": [],
        "confidence": "MEDIUM \u2014 no transcript, but title is specific to GSL's safety program. 'Zero Broken Lives' is a known GSL initiative.",
        "open_questions": ["GUID filename suggests older version. Verify this is the current active orientation course."]
    },
    {
        "batch": 2, "status": "done",
        "course": "Advanced Trimble Accubid Classic Pro",
        "source_file": "6900d60b-d412-4bc1-aab7-d068f5c8eb0e (1).zip",
        "content_summary": "Advanced estimating software training for Trimble Accubid Classic Pro. 17 bundled video tutorials covering: audit trail breakdowns, copy/paste between estimates, database switching, temporary assemblies, typical takeoffs, sort/filter, alarm function, item substitution, reverse takeoff, master/sub jobs, cost allocations, quote pad, supplier link/pricing, final price screen/crosschecks. No VTT transcripts.",
        "media": {"location": "bundled", "videos": ["1. Complete estimates with advanced features in Accubid.mp4", "2. What you should know.mp4", "3. Understanding and using audit trail breakdowns.mp4", "4. Audio and trial breakdownsTakeoff.mp4", "5. Copy and pasting from another estimate (1).mp4", "6. Switching between databases.mp4", "7. Creating temporary assemblies.mp4", "08. Creating and using typical takeoffs.mp4", "09. Using the sort and filter functions (1).mp4", "10. Using the alarm function.mp4", "11. Substituting items Electrical.mp4", "12. Understanding and using reverse takeoff.mp4", "13. Creating master and sub jobs.mp4", "14. Using cost allocations.mp4", "quote pad advanced.mp4", "16. Using supplier link and pricing your items.mp4", "17. Understanding the final price screen and crosschecks (1).mp4"]},
        "transcript": {"status": "needs-retrieval", "source": "17 bundled MP4s have no VTT \u2014 AI captions could be generated", "video_count": 17, "vtt_count": 0},
        "short_description": "Master advanced Accubid Classic Pro features including audit trail breakdowns, reverse takeoff, master/sub jobs, cost allocations, and supplier pricing.",
        "long_description": "This course covers advanced features of Trimble Accubid Classic Pro estimating software. Through 17 video tutorials, you will learn audit trail breakdowns, copying between estimates, database switching, temporary assemblies, typical takeoffs, the sort/filter and alarm functions, item substitution, reverse takeoff, creating master and sub jobs, cost allocations, using the quote pad, supplier link and pricing, and the final price screen with crosschecks.\n\nDesigned for estimators who have completed basic Accubid training and need to leverage advanced features for complex bids. On completion, you earn the skill Estimating.\n\nThis is an Advanced-level course that requires working knowledge of Accubid basics.",
        "category": {"value": "Estimating > Accubid", "label": "EXISTING", "rationale": "Advanced Accubid software training under Estimating."},
        "tags": [
            {"value": "Accubid", "label": "EXISTING"},
            {"value": "Estimating", "label": "EXISTING"},
            {"value": "Takeoff", "label": "EXISTING"},
            {"value": "Pricing", "label": "EXISTING"},
            {"value": "sub-jobs", "label": "EXISTING"},
            {"value": "cost", "label": "EXISTING"},
            {"value": "software", "label": "EXISTING"},
            {"value": "Difficulty: Advanced", "label": "PROPOSED"}
        ],
        "skills_awarded": [
            {"skill": "Estimating", "skill_category": "Estimating", "scale_set": "Estimating", "level": "[LEVEL NEEDED \u2014 Estimating scale set has no levels defined]", "label": "EXISTING", "rationale": "Advanced Accubid directly develops estimating expertise. Existing skill."}
        ],
        "level_of_difficulty": {"value": "Advanced", "rationale": "Title says 'Advanced'. Requires working knowledge of basic Accubid. Covers complex features."},
        "target_roles_draft": [
            {"fragment": "Academy/Estimating/[level TBD]", "roles": ["Project Manager"], "scope": "Role-scoped", "note": "Estimators and PMs who use Accubid for bidding. [ROLE-UNVERIFIED] for dedicated estimator role."}
        ],
        "topic_timestamp_index": [],
        "confidence": "MEDIUM-HIGH \u2014 no VTT, but 17 descriptively named video tutorials. Title is unambiguous.",
        "open_questions": ["VTTs could be generated from the 17 bundled MP4s. GUID filename with (1) suffix suggests re-upload."]
    },
    {
        "batch": 2, "status": "done",
        "course": "Building and Maintaining Team Morale",
        "source_file": "building-and-maintaining-team-morale-introduction-to-field-leadership-section-1-scorm12-qbritjmd.zip",
        "content_summary": "Part of Introduction to Field Leadership Section 1. Covers strategies for building and sustaining team morale on the jobsite. No transcript or video.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "SharePoint/Stream \u2014 no video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Learn practical strategies for building and maintaining team morale to keep your crew motivated and productive.",
        "long_description": "This course is part of the Introduction to Field Leadership series (Section 1). It covers the leader's role in building team morale \u2014 recognizing good work, creating a positive work environment, addressing morale problems early, and sustaining motivation through challenging project phases.\n\nDesigned for foremen, leadmen, and anyone stepping into a field leadership role. On completion, you earn the skill Team Motivation Fundamentals.\n\nThis is a Foundational-level course with no prerequisites.",
        "category": {"value": "Leadership > Skills, Traits, & Responsibilities", "label": "EXISTING", "rationale": "Part of the Field Leadership series on leadership fundamentals."},
        "tags": [
            {"value": "morale", "label": "EXISTING"},
            {"value": "Motivation", "label": "EXISTING"},
            {"value": "Field Leadership", "label": "EXISTING"},
            {"value": "Team Building", "label": "EXISTING"},
            {"value": "Recognition", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [
            {"skill": "Team Motivation Fundamentals", "skill_category": "Leadership", "scale_set": "Leadership", "level": "[LEVEL NEEDED \u2014 Leadership scale set has no levels defined]", "label": "EXISTING", "rationale": "Directly addresses team motivation and morale. Existing skill."}
        ],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Introductory field leadership content."},
        "target_roles_draft": [
            {"fragment": "Academy/Team Motivation Fundamentals/[level TBD]", "roles": ["Leadman", "Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders responsible for crew morale."}
        ],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video. Description based on title and series membership.",
        "open_questions": []
    },
    {
        "batch": 2, "status": "done",
        "course": "Chapter 0 - Introduction to Critical Leadership Training",
        "source_file": "chapter-0-introduction-to-critical-leadership-training-scorm12-qolorhhv.zip",
        "content_summary": "Introductory chapter of the Critical Leadership Training series. Sets the stage for the leadership development program. NBIC logo present in assets.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "SharePoint/Stream \u2014 no video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Get oriented to GSL's Critical Leadership Training program and understand what you will learn throughout the series.",
        "long_description": "This course is the introductory chapter (Chapter 0) of the Critical Leadership Training series. It provides an overview of the leadership development program \u2014 why leadership matters in electrical construction, what topics the series covers, and how to get the most from your training.\n\nDesigned for all employees beginning the Critical Leadership Training track. On completion, you earn the skill Leadership.\n\nThis is a Foundational-level orientation course with no prerequisites.",
        "category": {"value": "Leadership > Leadership Fundamentals", "label": "EXISTING", "rationale": "Introductory chapter of a leadership fundamentals series."},
        "tags": [
            {"value": "Leadership", "label": "EXISTING"},
            {"value": "Leadership Basics", "label": "EXISTING"},
            {"value": "fundamentals", "label": "EXISTING"},
            {"value": "training", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [
            {"skill": "Leadership", "skill_category": "Leadership", "scale_set": "Leadership", "level": "[LEVEL NEEDED \u2014 Leadership scale set has no levels defined]", "label": "EXISTING", "rationale": "Introductory leadership course. Existing skill."}
        ],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Chapter 0 \u2014 the introduction. No prerequisites."},
        "target_roles_draft": [
            {"fragment": "Academy/Leadership/[level TBD]", "roles": ["Apprentice", "Journeyman", "Leadman", "Foreman", "Superintendent"], "scope": "Global", "note": "All employees can benefit. Primary audience is those entering field leadership."}
        ],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video. Description based on title and series position.",
        "open_questions": ["Which series does this belong to \u2014 same as 'Chapter 4 - Building an Effective Team' from Batch 1?"]
    },
    {
        "batch": 2, "status": "done",
        "course": "Chapter 01 - What Is Emotional Intelligence (EQ)?",
        "source_file": "chapter-01-what-is-emotional-intelligence-eq-scorm12-byirin-l.zip",
        "content_summary": "First chapter of the Emotional Intelligence series (LDRSHP-EQ-01). Defines EQ and its two categories: personal competence (self-awareness, self-regulation, self-motivation) and social competence (empathy, social skills). Covers four leadership benefits of high EQ: objective decisions, fewer blind spots, effective communication, improved workplace morale. Full VTT transcript available.",
        "media": {"location": "bundled", "videos": ["Leading with Emotional Intelligence (3).mp4", "MXP7aNiXXuCcsSXZ_LDRSHP-EQ-01.mp4"]},
        "transcript": {"status": "found-in-package", "source": "LDRSHP-EQ-01.vtt + duplicate", "video_count": 2, "vtt_count": 2},
        "short_description": "Discover the two categories of emotional intelligence \u2014 personal competence and social competence \u2014 and why they are essential for leadership success.",
        "long_description": "This course is Chapter 01 of the Emotional Intelligence series. It introduces emotional intelligence (EQ) and explains its two categories: personal competence (self-awareness, self-regulation, self-motivation) and social competence (empathy, social skills).\n\nYou will learn four key leadership benefits of high EQ: making more objective decisions, having fewer blind spots, communicating more effectively, and improving workplace morale. The course provides practical guidance on tuning into your emotions, practicing self-regulation, cultivating internal motivation, developing empathy, and improving social skills.\n\nDesigned for all employees, especially those in leadership or supervisory roles. On completion, you earn the skill EQ Fundamentals.\n\nThis is a Foundational-level course that introduces EQ concepts from scratch.",
        "category": {"value": "Soft Skills > Emotional Intelligence", "label": "EXISTING", "rationale": "Directly covers emotional intelligence fundamentals."},
        "tags": [
            {"value": "Emotional Intelligence", "label": "EXISTING"},
            {"value": "Self-awareness", "label": "EXISTING"},
            {"value": "Empathy", "label": "EXISTING"},
            {"value": "Social Skills", "label": "EXISTING"},
            {"value": "Self-Control", "label": "EXISTING"},
            {"value": "Leadership", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [
            {"skill": "EQ Fundamentals", "skill_category": "Emotional Intelligence", "scale_set": "Emotional Intelligence", "level": "[LEVEL NEEDED \u2014 Emotional Intelligence scale set has no levels defined]", "label": "EXISTING", "rationale": "Introductory EQ course. Existing skill."}
        ],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Introduces EQ concepts from scratch. Chapter 01 of the series."},
        "target_roles_draft": [
            {"fragment": "Academy/EQ Fundamentals/[level TBD]", "roles": ["Apprentice", "Journeyman", "Leadman", "Foreman", "Superintendent"], "scope": "Global", "note": "EQ benefits all employees. Especially important for leaders managing teams."}
        ],
        "topic_timestamp_index": [
            {"video": "Leading with Emotional Intelligence (3).mp4", "vtt": "LDRSHP-EQ-01.vtt", "topic": "Introduction \u2014 handling emotions as a leader", "timecode": "00:00:00.000"},
            {"video": "Leading with Emotional Intelligence (3).mp4", "vtt": "LDRSHP-EQ-01.vtt", "topic": "Personal competence: self-awareness, self-regulation, self-motivation", "timecode": "[TIMECODE NEEDED]"},
            {"video": "Leading with Emotional Intelligence (3).mp4", "vtt": "LDRSHP-EQ-01.vtt", "topic": "Social competence: empathy and social skills", "timecode": "[TIMECODE NEEDED]"},
            {"video": "Leading with Emotional Intelligence (3).mp4", "vtt": "LDRSHP-EQ-01.vtt", "topic": "Four leadership benefits of high EQ", "timecode": "[TIMECODE NEEDED]"},
            {"video": "Leading with Emotional Intelligence (3).mp4", "vtt": "LDRSHP-EQ-01.vtt", "topic": "Practical tips for developing EQ", "timecode": "[TIMECODE NEEDED]"}
        ],
        "confidence": "HIGH \u2014 full VTT transcript available; clear EQ content with well-defined topics.",
        "open_questions": ["Second VTT is a duplicate. Timecodes need extraction from raw VTT cues."]
    },
    {
        "batch": 2, "status": "done",
        "course": "Chapter 02 - What You Need to Know",
        "source_file": "chapter-02-what-you-need-to-know-scorm12-n-qj69jo (1).zip",
        "content_summary": "Chapter 2 of the Lean Construction series. Covers essential background knowledge for understanding lean in construction. No transcript or video.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "SharePoint/Stream \u2014 no video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Learn the essential background concepts you need before diving into lean construction principles and practices.",
        "long_description": "This course is Chapter 02 of the Lean Construction series. It covers the foundational knowledge needed to understand lean construction \u2014 key terminology, basic concepts, and the mindset shift required to think in lean terms.\n\nDesigned for field leaders beginning the lean construction curriculum. On completion, you earn the skill Lean Fundamentals.\n\nThis is a Foundational-level course.",
        "category": {"value": "Lean Principals > Lean Fundamentals", "label": "EXISTING", "rationale": "Early chapter covering foundational lean concepts."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "fundamentals", "label": "EXISTING"},
            {"value": "basics", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [
            {"skill": "Lean Fundamentals", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": "[LEVEL NEEDED \u2014 Lean Principles scale set has no levels defined]", "label": "EXISTING", "rationale": "Foundational lean chapter. Existing skill."}
        ],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Chapter 2 \u2014 still building foundational concepts."},
        "target_roles_draft": [
            {"fragment": "Academy/Lean Fundamentals/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Lean adoption targeted at field leadership."}
        ],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video. Description based on title and series position.",
        "open_questions": ["Filename has (1) suffix suggesting re-upload."]
    },
    {
        "batch": 2, "status": "done",
        "course": "Chapter 03 - Productivity in Construction",
        "source_file": "chapter-03-productivity-in-construction-scorm12-imnm9mxy.zip",
        "content_summary": "Chapter 3 of the Lean Construction series. Focuses on productivity measurement and challenges specific to construction. No transcript or video.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "SharePoint/Stream \u2014 no video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Understand how productivity is measured in construction and the unique challenges that affect it on the jobsite.",
        "long_description": "This course is Chapter 03 of the Lean Construction series. It examines productivity in the construction industry \u2014 how it is measured, why construction productivity has historically lagged other industries, and what factors affect jobsite productivity.\n\nDesigned for field leaders learning to think about work in lean terms. On completion, you earn the skill Productivity Benefits.\n\nThis is a Foundational-level course continuing the lean series.",
        "category": {"value": "Lean Principals > Lean Fundamentals", "label": "EXISTING", "rationale": "Productivity in construction is a core lean fundamentals topic."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "productivity", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "Construction", "label": "EXISTING"},
            {"value": "Efficiency", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [
            {"skill": "Productivity Benefits", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": "[LEVEL NEEDED \u2014 Lean Principles scale set has no levels defined]", "label": "EXISTING", "rationale": "Covers productivity concepts. Existing skill."}
        ],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Chapter 3 \u2014 continues building foundational lean concepts."},
        "target_roles_draft": [
            {"fragment": "Academy/Productivity Benefits/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders focused on crew productivity."}
        ],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video. Description based on title and series position.",
        "open_questions": []
    },
    {
        "batch": 2, "status": "done",
        "course": "Chapter 05 - What is Lean?",
        "source_file": "chapter-05-what-is-lean-scorm12-pvxdpabr.zip",
        "content_summary": "Chapter 5 of the Lean Construction series. Formally defines lean \u2014 its origins, core principles, and what it means in a construction context. No transcript or video.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "SharePoint/Stream \u2014 no video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Learn the formal definition of lean, its core principles, and how lean thinking applies to the construction industry.",
        "long_description": "This course is Chapter 05 of the Lean Construction series. It provides the formal definition of lean \u2014 where it came from, what its core principles are, and how it differs from traditional construction management approaches.\n\nDesigned for field leaders developing their lean thinking foundation. On completion, you earn the skill Lean Fundamentals.\n\nThis is a Foundational-level course.",
        "category": {"value": "Lean Principals > Lean Fundamentals", "label": "EXISTING", "rationale": "Formal definition of lean is core lean fundamentals."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "Lean Principles ", "label": "EXISTING"},
            {"value": "fundamentals", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [
            {"skill": "Lean Fundamentals", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": "[LEVEL NEEDED \u2014 Lean Principles scale set has no levels defined]", "label": "EXISTING", "rationale": "Defines lean \u2014 foundational content. Existing skill."}
        ],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Chapter 5 \u2014 still building foundational understanding."},
        "target_roles_draft": [
            {"fragment": "Academy/Lean Fundamentals/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders learning lean principles."}
        ],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video. Description based on title and series position.",
        "open_questions": ["Chapter 04 missing from lean series \u2014 may exist elsewhere."]
    },
    {
        "batch": 2, "status": "done",
        "course": "Chapter 06 - A Brief History",
        "source_file": "chapter-06-a-brief-history-scorm12-d1yinukr.zip",
        "content_summary": "Chapter 6 of the Lean Construction series. Covers the history of lean from Toyota Production System through construction adoption. Assets include industry leader references.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "SharePoint/Stream \u2014 no video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Trace the history of lean from its manufacturing origins through its adoption in the construction industry.",
        "long_description": "This course is Chapter 06 of the Lean Construction series. It covers the history of lean \u2014 from its origins in the Toyota Production System through its evolution and adoption in the construction industry.\n\nDesigned for field leaders building their lean knowledge foundation. On completion, you earn the skill Lean History Understanding.\n\nThis is a Foundational-level course.",
        "category": {"value": "Lean Principals > Industry Transformation", "label": "EXISTING", "rationale": "History of lean adoption is industry transformation content."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "Industry Change", "label": "EXISTING"},
            {"value": "Lean Adoption", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [
            {"skill": "Lean History Understanding", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": "[LEVEL NEEDED \u2014 Lean Principles scale set has no levels defined]", "label": "EXISTING", "rationale": "Covers lean history. Existing skill."}
        ],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Historical overview \u2014 no technical prerequisites."},
        "target_roles_draft": [
            {"fragment": "Academy/Lean History Understanding/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders developing lean context."}
        ],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video. Description based on title and series position.",
        "open_questions": []
    },
    {
        "batch": 2, "status": "done",
        "course": "Chapter 07 - How Does Lean Apply to Construction?",
        "source_file": "chapter-07-how-does-lean-apply-to-construction-scorm12-wji5bpej.zip",
        "content_summary": "Chapter 7 of the Lean Construction series. Bridges lean theory to construction practice. Assets include conduit images. No transcript or video.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "SharePoint/Stream \u2014 no video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "See how lean principles translate from theory to practice on the construction jobsite.",
        "long_description": "This course is Chapter 07 of the Lean Construction series. It bridges the gap between lean theory and construction practice \u2014 showing how flow, pull, waste elimination, and continuous improvement apply to real jobsite situations.\n\nDesigned for field leaders ready to apply lean thinking. On completion, you earn the skill Lean Fundamentals.\n\nThis is a Foundational-level course.",
        "category": {"value": "Lean Principals > Lean Fundamentals", "label": "EXISTING", "rationale": "Applying lean to construction is core lean fundamentals."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "Construction", "label": "EXISTING"},
            {"value": "Process Improvement", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [
            {"skill": "Lean Fundamentals", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": "[LEVEL NEEDED \u2014 Lean Principles scale set has no levels defined]", "label": "EXISTING", "rationale": "Applying lean to construction \u2014 foundational application. Existing skill."}
        ],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Application of foundational concepts. Still introductory-level."},
        "target_roles_draft": [
            {"fragment": "Academy/Lean Fundamentals/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders who will implement lean practices."}
        ],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video. Description based on title and series position.",
        "open_questions": []
    },
    {
        "batch": 2, "status": "done",
        "course": "Chapter 08 - What Processes Need to Change?",
        "source_file": "chapter-08-what-processes-need-to-change-scorm12-said6ikm.zip",
        "content_summary": "Chapter 8 of the Lean Construction series. Identifies construction processes that need to change for lean adoption. No transcript or video.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "SharePoint/Stream \u2014 no video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Identify which construction processes need to change and how lean thinking transforms traditional approaches.",
        "long_description": "This course is Chapter 08 of the Lean Construction series. It examines which traditional construction processes need to change for lean adoption \u2014 comparing conventional approaches to lean alternatives in planning, scheduling, material handling, and communication.\n\nDesigned for field leaders evaluating their current practices. On completion, you earn the skill Lean Mindset.\n\nThis is a Foundational-level course.",
        "category": {"value": "Lean Principals > Process Management", "label": "EXISTING", "rationale": "Identifying process changes is process management within lean."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "Process Improvement", "label": "EXISTING"},
            {"value": "Process", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "Continuous Improvement", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [
            {"skill": "Lean Mindset", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": "[LEVEL NEEDED \u2014 Lean Principles scale set has no levels defined]", "label": "EXISTING", "rationale": "Evaluating processes for lean change requires lean mindset. Existing skill."}
        ],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Chapter 8 \u2014 still introductory level despite series position."},
        "target_roles_draft": [
            {"fragment": "Academy/Lean Mindset/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders who will drive process changes."}
        ],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video. Description based on title and series position.",
        "open_questions": []
    },
    {
        "batch": 2, "status": "done",
        "course": "Chapter 09 - The Adoption of a New Production Theory",
        "source_file": "chapter-09-the-adoption-of-a-new-production-theory-scorm12-ypg1zg6x.zip",
        "content_summary": "Chapter 9 (likely final chapter) of the Lean Construction series. Covers adoption of lean as a new production theory for construction. No transcript or video.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "SharePoint/Stream \u2014 no video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Understand how adopting lean as a new production theory can transform construction project delivery.",
        "long_description": "This course is Chapter 09 of the Lean Construction series \u2014 likely the concluding chapter. It covers the adoption of lean as a complete production theory for construction, moving beyond individual tools to a systemic approach.\n\nDesigned for field leaders completing the lean curriculum. On completion, you earn the skill Lean Mindset.\n\nThis is a Foundational-level course.",
        "category": {"value": "Lean Principals > Industry Transformation", "label": "EXISTING", "rationale": "Adopting a new production theory is industry transformation."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "Lean Adoption", "label": "EXISTING"},
            {"value": "Industry Change", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [
            {"skill": "Lean Mindset", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": "[LEVEL NEEDED \u2014 Lean Principles scale set has no levels defined]", "label": "EXISTING", "rationale": "Adopting lean as production theory is the lean mindset outcome. Existing skill."}
        ],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Concluding chapter but still accessible introductory content."},
        "target_roles_draft": [
            {"fragment": "Academy/Lean Mindset/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders completing the lean series."}
        ],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video. Description based on title and series position.",
        "open_questions": ["Confirm this is the final chapter of the lean series."]
    },
    {
        "batch": 2, "status": "done",
        "course": "[FROM FILENAME] Untitled",
        "source_file": "untitled-scorm12-xrofbisj.zip",
        "content_summary": "UNKNOWN CONTENT. Title not found in manifest. One bundled video 'Glen 7 (2).mp4' and asset '4_financial.jpg'. Insufficient information to determine course content.",
        "media": {"location": "bundled", "videos": ["Glen 7 (2).mp4"]},
        "transcript": {"status": "needs-retrieval", "source": "Bundled MP4 has no VTT", "video_count": 1, "vtt_count": 0},
        "short_description": "[NEEDS INVESTIGATION \u2014 content unknown. Video 'Glen 7' and financial imagery suggest leadership or business topic.]",
        "long_description": "[NEEDS INVESTIGATION \u2014 this course has no title in its manifest, no transcript, and insufficient metadata to generate a reliable description. The video 'Glen 7 (2).mp4' and asset '4_financial.jpg' suggest possible leadership or financial content. Needs manual review in Learn365.]",
        "category": {"value": "[UNKNOWN \u2014 needs investigation]", "label": "NEEDS-REVIEW", "rationale": "Cannot determine category from available metadata."},
        "tags": [],
        "skills_awarded": [],
        "level_of_difficulty": {"value": "[UNKNOWN]", "rationale": "Cannot determine difficulty without knowing the content."},
        "target_roles_draft": [],
        "topic_timestamp_index": [],
        "confidence": "VERY LOW \u2014 no manifest title, no transcript, no descriptive metadata.",
        "open_questions": [
            "What is this course? No manifest title found.",
            "'Glen 7' may refer to a person or series \u2014 needs manual identification.",
            "Should this course be removed from the catalog or properly titled?",
            "VTT could be generated from the bundled MP4 to identify content."
        ]
    }
]

# Merge
recs['courses'].extend(batch2)
recs['meta']['last_updated'] = '2026-05-20'
recs['meta']['status'] = 'In Progress \u2014 Batch 2 complete'

with open(RECS_PATH, 'w', encoding='utf-8') as f:
    json.dump(recs, f, indent=2, ensure_ascii=False)

# Update index
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    idx = json.load(f)
for c in idx['courses']:
    if c.get('batch') == 2:
        c['status'] = 'done'
with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    json.dump(idx, f, indent=2, ensure_ascii=False)

print(f'Batch 2: {len(batch2)} courses added')
print(f'Total recommendations: {len(recs["courses"])}')

# QC summary
conf = {}
for c in batch2:
    level = c['confidence'].split(' ')[0]
    conf[level] = conf.get(level, 0) + 1
print(f'Confidence: {conf}')
new_skills = [c for c in batch2 if any(s['label'] != 'EXISTING' for s in c.get('skills_awarded', []))]
new_tags = [t for c in batch2 for t in c.get('tags', []) if t['label'] not in ('EXISTING', 'PROPOSED')]
print(f'New skills proposed: {len(new_skills)}')
print(f'New tags (non-EXISTING/PROPOSED): {len(new_tags)}')
print(f'Vocabulary sprawl: NONE' if not new_skills and not new_tags else f'ALERT: vocabulary sprawl detected')
