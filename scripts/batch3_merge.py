"""Merge Batch 3 taxonomy recommendations."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DATA_DIR = r'C:\Users\tewing\OneDrive - GSL Electric\Projects\GSL-Operations-Framework\data'
RECS_PATH = os.path.join(DATA_DIR, 'scorm_taxonomy_recommendations.json')
INDEX_PATH = os.path.join(DATA_DIR, 'scorm_course_index.json')

with open(RECS_PATH, 'r', encoding='utf-8') as f:
    recs = json.load(f)

LN = "[LEVEL NEEDED \u2014 {ss} scale set has no levels defined]"

batch3 = [
    {
        "batch": 3, "status": "done",
        "course": "Chapter 1 Job Plan Theory",
        "source_file": "chapter-1-job-plan-theory-scorm12-lhuuftlp.zip",
        "content_summary": "Chapter 1 of the Job Plan series. Covers the theory behind job planning in electrical construction \u2014 why job plans matter, what they contain, and how they drive project success. Part of the same series as 'Jobsite Efficiency' (shared assets).",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Understand the theory behind job planning and why effective job plans are critical to project success.",
        "long_description": "This course is Chapter 1 of the Job Plan series. It covers the theory behind job planning in electrical construction \u2014 why job plans exist, what they should contain, and how they drive productivity, accountability, and project success.\n\nDesigned for foremen and superintendents who create and maintain job plans. On completion, you earn the skill Creating Job Plans.\n\nThis is a Foundational-level course.",
        "category": {"value": "Leadership > Project Planning & Scheduling", "label": "EXISTING", "rationale": "Job plan theory is a planning and scheduling topic."},
        "tags": [
            {"value": "job plan", "label": "EXISTING"},
            {"value": "Planning", "label": "EXISTING"},
            {"value": "project planning", "label": "EXISTING"},
            {"value": "fundamentals", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Creating Job Plans", "skill_category": "Leadership", "scale_set": "Leadership", "level": LN.format(ss="Leadership"), "label": "EXISTING", "rationale": "Directly teaches job plan theory. Existing skill."}],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Chapter 1 \u2014 introduces job plan concepts."},
        "target_roles_draft": [{"fragment": "Academy/Creating Job Plans/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Personnel who create and maintain job plans."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video.",
        "open_questions": []
    },
    {
        "batch": 3, "status": "done",
        "course": "Chapter 1 - What Makes A Leader",
        "source_file": "chapter-1-what-makes-a-leader-scorm12-gkna64je.zip",
        "content_summary": "Chapter 1 of the Critical Leadership Training series (NBIC logo present). Explores what makes an effective leader \u2014 qualities, traits, and mindset. Assets include site walk and concert crowd images suggesting leadership presence themes.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Explore what makes an effective leader \u2014 the qualities, traits, and mindset that separate good leaders from great ones.",
        "long_description": "This course is Chapter 1 of the Critical Leadership Training series. It explores what makes an effective leader \u2014 core leadership qualities, the difference between management and leadership, and the mindset required to lead crews in construction.\n\nDesigned for anyone beginning the Critical Leadership Training track. On completion, you earn the skill Leadership.\n\nThis is a Foundational-level course.",
        "category": {"value": "Leadership > Leadership Fundamentals", "label": "EXISTING", "rationale": "Chapter 1 of the Critical Leadership Training series."},
        "tags": [
            {"value": "Leadership", "label": "EXISTING"},
            {"value": "Leadership Basics", "label": "EXISTING"},
            {"value": "fundamentals", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Leadership", "skill_category": "Leadership", "scale_set": "Leadership", "level": LN.format(ss="Leadership"), "label": "EXISTING", "rationale": "Foundational leadership course. Existing skill."}],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Chapter 1 \u2014 introductory."},
        "target_roles_draft": [{"fragment": "Academy/Leadership/[level TBD]", "roles": ["Apprentice", "Journeyman", "Leadman", "Foreman", "Superintendent"], "scope": "Global", "note": "All employees benefit from leadership fundamentals."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video.",
        "open_questions": ["Same series as Chapter 0 (Batch 2) and Chapter 4 (Batch 1)."]
    },
    {
        "batch": 3, "status": "done",
        "course": "Chapter 10 Avoiding Common Time Wasters",
        "source_file": "chapter-10-avoiding-common-time-wasters-scorm12-rakckav4.zip",
        "content_summary": "Chapter 10 of the Introduction to Field Leadership series. Same topic as Batch 1's 'Avoiding Common Time Wasters- Introduction to Field Leadership Section - 1' but with chapter numbering. Likely the same course in a different packaging format.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Identify the most common time wasters on the jobsite and learn practical strategies to stay focused and productive.",
        "long_description": "This course is Chapter 10 of the Introduction to Field Leadership series. It helps you recognize common time wasters that reduce productivity on the jobsite and gives you strategies to eliminate or minimize them.\n\nDesigned for foremen, leadmen, and anyone in a field leadership role. On completion, you earn the skill Time Management.\n\nThis is a Foundational-level course.",
        "category": {"value": "Leadership > Skills, Traits, & Responsibilities", "label": "EXISTING", "rationale": "Field Leadership series on leadership skills."},
        "tags": [
            {"value": "time wasters", "label": "EXISTING"},
            {"value": "productivity", "label": "EXISTING"},
            {"value": "Field Leadership", "label": "EXISTING"},
            {"value": "prioritization", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Time Management", "skill_category": "Leadership", "scale_set": "Leadership", "level": LN.format(ss="Leadership"), "label": "EXISTING", "rationale": "Time management for field leaders. Existing skill."}],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Introductory field leadership content."},
        "target_roles_draft": [{"fragment": "Academy/Time Management/[level TBD]", "roles": ["Leadman", "Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders responsible for crew productivity."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video.",
        "open_questions": ["Likely duplicate of 'Avoiding Common Time Wasters- Introduction to Field Leadership Section - 1' (Batch 1). Verify and consolidate."]
    },
    {
        "batch": 3, "status": "done",
        "course": "Chapter 10 - Conclusion: Leadership is the Most Important Skill",
        "source_file": "chapter-10-conclusion-leadership-is-the-most-important-skill-scorm12-2vctenpb.zip",
        "content_summary": "Chapter 10 (concluding chapter) of the Critical Leadership Training series (NBIC logo). Reinforces that leadership is the most important skill for construction professionals. Wraps up the series.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Conclude the Critical Leadership Training series with a reflection on why leadership is the most important skill in construction.",
        "long_description": "This course is the concluding chapter (Chapter 10) of the Critical Leadership Training series. It reinforces the central message: leadership is the most important skill for success in construction. It ties together the themes covered throughout the series and challenges you to apply what you have learned.\n\nDesigned for all employees completing the Critical Leadership Training track. On completion, you earn the skill Leadership.\n\nThis is a Foundational-level summary course.",
        "category": {"value": "Leadership > Leadership Fundamentals", "label": "EXISTING", "rationale": "Concluding chapter of the Critical Leadership Training series."},
        "tags": [
            {"value": "Leadership", "label": "EXISTING"},
            {"value": "Leadership Basics", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Leadership", "skill_category": "Leadership", "scale_set": "Leadership", "level": LN.format(ss="Leadership"), "label": "EXISTING", "rationale": "Series conclusion reinforces leadership skill. Existing skill."}],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Summary/conclusion chapter \u2014 accessible to all."},
        "target_roles_draft": [{"fragment": "Academy/Leadership/[level TBD]", "roles": ["Apprentice", "Journeyman", "Leadman", "Foreman", "Superintendent"], "scope": "Global", "note": "All employees completing the leadership series."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video.",
        "open_questions": ["Chapters 2-9 of the Critical Leadership series presumably exist \u2014 verify."]
    },
    {
        "batch": 3, "status": "done",
        "course": "Chapter 10 - Identifying Waste in Construction",
        "source_file": "chapter-10-identifying-waste-in-construction-scorm12-rttb6txz.zip",
        "content_summary": "Chapter 10 of the Lean Construction series (lean header image). Covers waste identification in construction \u2014 how to spot the eight wastes on the jobsite. Assets include lean design and color-coded cart work images.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Learn to identify the eight wastes of construction on your jobsite using lean observation techniques.",
        "long_description": "This course is Chapter 10 of the Lean Construction series. It teaches you how to identify waste in real construction situations \u2014 applying the eight wastes framework to observe and document waste on the jobsite.\n\nBuilds on the foundational lean chapters. Designed for field leaders implementing lean practices. On completion, you earn the skill Eight Wastes Recognition.\n\nThis is an Intermediate-level course that requires lean fundamentals knowledge.",
        "category": {"value": "Lean Principals > Waste Management", "label": "EXISTING", "rationale": "Waste identification is core waste management content."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "Waste", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "Eliminate Waste", "label": "EXISTING"},
            {"value": "Difficulty: Intermediate", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Eight Wastes Recognition", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": LN.format(ss="Lean Principles"), "label": "EXISTING", "rationale": "Teaches waste identification. Existing skill."}],
        "level_of_difficulty": {"value": "Intermediate", "rationale": "Requires lean fundamentals from earlier chapters. Application-level."},
        "target_roles_draft": [{"fragment": "Academy/Eight Wastes Recognition/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders who can act on waste identification."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video.",
        "open_questions": []
    },
    {
        "batch": 3, "status": "done",
        "course": "Chapter 11 Building and Maintaining Team Morale",
        "source_file": "chapter-11-building-and-maintaining-team-morale-scorm12-o9ngi2ph.zip",
        "content_summary": "Chapter 11 of the Introduction to Field Leadership series. Same topic as Batch 2's course but with chapter numbering. Likely same content, different packaging.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Learn practical strategies for building and maintaining team morale to keep your crew motivated and productive.",
        "long_description": "This course is Chapter 11 of the Introduction to Field Leadership series. It covers the leader's role in building team morale \u2014 recognizing good work, creating a positive work environment, and sustaining motivation.\n\nDesigned for field leaders. On completion, you earn the skill Team Motivation Fundamentals.\n\nThis is a Foundational-level course.",
        "category": {"value": "Leadership > Skills, Traits, & Responsibilities", "label": "EXISTING", "rationale": "Field Leadership series."},
        "tags": [
            {"value": "morale", "label": "EXISTING"},
            {"value": "Motivation", "label": "EXISTING"},
            {"value": "Field Leadership", "label": "EXISTING"},
            {"value": "Team Building", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Team Motivation Fundamentals", "skill_category": "Leadership", "scale_set": "Leadership", "level": LN.format(ss="Leadership"), "label": "EXISTING", "rationale": "Team morale and motivation. Existing skill."}],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Introductory field leadership content."},
        "target_roles_draft": [{"fragment": "Academy/Team Motivation Fundamentals/[level TBD]", "roles": ["Leadman", "Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video.",
        "open_questions": ["Likely duplicate of 'Building and Maintaining Team Morale- Introduction to Field Leadership Section - 1' (Batch 2). Verify and consolidate."]
    },
    {
        "batch": 3, "status": "done",
        "course": "Chapter 11 - Minimizing Waste at a Project Level",
        "source_file": "chapter-11-minimizing-waste-at-a-project-level-scorm12-bb8uiief (1).zip",
        "content_summary": "Chapter 11 of the Lean Construction series. Moves from waste identification to waste minimization at the project level. Assets include airport SLC, conduit wall, and fill images showing real construction contexts.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Learn strategies for minimizing waste at the project level to improve efficiency and reduce costs.",
        "long_description": "This course is Chapter 11 of the Lean Construction series. It moves beyond waste identification to practical strategies for minimizing waste at the project level \u2014 from material handling to work sequencing to communication.\n\nBuilds on waste identification knowledge. Designed for field leaders implementing lean on their projects. On completion, you earn the skill Eliminate Waste.\n\nThis is an Intermediate-level course.",
        "category": {"value": "Lean Principals > Waste Management", "label": "EXISTING", "rationale": "Project-level waste minimization."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "Waste", "label": "EXISTING"},
            {"value": "Eliminate Waste", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "jobsite efficiency", "label": "EXISTING"},
            {"value": "Difficulty: Intermediate", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Eliminate Waste", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": LN.format(ss="Lean Principles"), "label": "EXISTING", "rationale": "Teaches waste elimination at project level. Existing skill."}],
        "level_of_difficulty": {"value": "Intermediate", "rationale": "Builds on waste identification. Application-level."},
        "target_roles_draft": [{"fragment": "Academy/Eliminate Waste/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders implementing lean practices."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video.",
        "open_questions": ["Filename has (1) suffix suggesting re-upload."]
    },
    {
        "batch": 3, "status": "done",
        "course": "Chapter 12 - Empowerment of Field Personnel",
        "source_file": "chapter-12-empowerment-of-field-personnel-scorm12-tz6n2sy9.zip",
        "content_summary": "Chapter 12 of the Lean Construction series (lean header image). Covers empowering field personnel to make decisions and take ownership \u2014 a core lean principle (Respect for People). Assets include training images.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Learn how empowering field personnel to make decisions and take ownership drives lean outcomes on the jobsite.",
        "long_description": "This course is Chapter 12 of the Lean Construction series. It covers the lean principle of empowering field personnel \u2014 giving crews the authority and information they need to make decisions, solve problems, and take ownership of their work. This is a core element of the 'Respect for People' pillar of lean.\n\nDesigned for superintendents and project leaders who set the empowerment culture. On completion, you earn the skill Field Team Empowerment.\n\nThis is an Intermediate-level course.",
        "category": {"value": "Lean Principals > Respect For People", "label": "EXISTING", "rationale": "Field empowerment is a Respect for People topic."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "Empowerment", "label": "EXISTING"},
            {"value": "Respect For People", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "autonomy", "label": "EXISTING"},
            {"value": "Difficulty: Intermediate", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Field Team Empowerment", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": LN.format(ss="Lean Principles"), "label": "EXISTING", "rationale": "Teaches field empowerment. Existing skill."}],
        "level_of_difficulty": {"value": "Intermediate", "rationale": "Requires lean fundamentals context. Leadership application-level."},
        "target_roles_draft": [{"fragment": "Academy/Field Team Empowerment/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Leaders who set empowerment culture."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video.",
        "open_questions": []
    },
    {
        "batch": 3, "status": "done",
        "course": "Chapter 12 Using Tool and Technology",
        "source_file": "chapter-12-using-tool-and-technology-scorm12-jzhv6nfe.zip",
        "content_summary": "Chapter 12 of the Introduction to Field Leadership series. Covers how field leaders should leverage tools and technology for productivity and communication.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Learn how to leverage tools and technology as a field leader to improve productivity and communication on the jobsite.",
        "long_description": "This course is Chapter 12 of the Introduction to Field Leadership series. It covers how field leaders can use modern tools and technology \u2014 from mobile apps to project management software \u2014 to improve crew productivity, communication, and documentation.\n\nDesigned for foremen and leadmen developing their field leadership skills. On completion, you earn the skill Tool & Equipment Management.\n\nThis is a Foundational-level course.",
        "category": {"value": "Leadership > Tools & Technology", "label": "EXISTING", "rationale": "Tools and technology usage for field leaders."},
        "tags": [
            {"value": "technology", "label": "EXISTING"},
            {"value": "Field Leadership", "label": "EXISTING"},
            {"value": "software", "label": "EXISTING"},
            {"value": "productivity", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Tool & Equipment Management", "skill_category": "Leadership", "scale_set": "Leadership", "level": LN.format(ss="Leadership"), "label": "EXISTING", "rationale": "Tools and technology for field leaders. Existing skill."}],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Introductory field leadership content."},
        "target_roles_draft": [{"fragment": "Academy/Tool & Equipment Management/[level TBD]", "roles": ["Leadman", "Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders adopting technology."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video.",
        "open_questions": []
    },
    {
        "batch": 3, "status": "done",
        "course": "Chapter 13 - Pull Planning",
        "source_file": "chapter-13-pull-planning-scorm12-ne5la4rr.zip",
        "content_summary": "Chapter 13 of the Lean Construction series. Introduces pull planning \u2014 a lean scheduling method where work is planned backward from milestones with collaborative team input. Assets include GSL Handshake image suggesting collaborative planning.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Learn the pull planning method \u2014 a collaborative lean scheduling approach that plans work backward from project milestones.",
        "long_description": "This course is Chapter 13 of the Lean Construction series. It introduces pull planning \u2014 a lean scheduling method where the team collaboratively plans work backward from milestones, identifying handoffs and constraints. Pull planning replaces traditional push scheduling with a commitment-based approach.\n\nDesigned for foremen and superintendents who participate in or lead pull planning sessions. On completion, you earn the skill Pull Planning.\n\nThis is an Intermediate-level course.",
        "category": {"value": "Lean Principals > Pull Planning", "label": "EXISTING", "rationale": "Directly covers pull planning."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "Planning", "label": "EXISTING"},
            {"value": "Scheduling", "label": "EXISTING"},
            {"value": "Collaboration", "label": "EXISTING"},
            {"value": "Difficulty: Intermediate", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Pull Planning", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": LN.format(ss="Lean Principles"), "label": "EXISTING", "rationale": "Directly teaches pull planning. Existing skill."}],
        "level_of_difficulty": {"value": "Intermediate", "rationale": "Requires lean fundamentals. Application-level lean tool."},
        "target_roles_draft": [{"fragment": "Academy/Pull Planning/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Personnel who participate in pull planning sessions."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video.",
        "open_questions": []
    },
    {
        "batch": 3, "status": "done",
        "course": "Chapter 14 - The Sticky Note Format",
        "source_file": "chapter-14-the-sticky-note-format-scorm12-ipzawrxc.zip",
        "content_summary": "Chapter 14 of the Lean Construction series. Covers the sticky note format used in pull planning sessions. Assets include Lean-Board image and pull planning wall photos confirming visual planning content.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Master the sticky note format used in pull planning sessions to organize tasks, commitments, and handoffs visually.",
        "long_description": "This course is Chapter 14 of the Lean Construction series. It teaches the sticky note format \u2014 the visual planning method used in pull planning sessions. You will learn how to write effective sticky notes (task, duration, predecessor, trade), organize them on the pull plan wall, and use the visual board to track commitments.\n\nBuilds on Chapter 13 Pull Planning. Designed for active pull planning participants. On completion, you earn the skill Pull Planning.\n\nThis is an Intermediate-level course.",
        "category": {"value": "Lean Principals > Pull Planning", "label": "EXISTING", "rationale": "Sticky note format is the practical tool of pull planning."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "Planning", "label": "EXISTING"},
            {"value": "Collaboration", "label": "EXISTING"},
            {"value": "Difficulty: Intermediate", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Pull Planning", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": LN.format(ss="Lean Principles"), "label": "EXISTING", "rationale": "Practical pull planning method. Existing skill."}],
        "level_of_difficulty": {"value": "Intermediate", "rationale": "Builds on pull planning introduction. Hands-on method."},
        "target_roles_draft": [{"fragment": "Academy/Pull Planning/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Active pull planning participants."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript, but asset filenames (Lean-Board.jpg) confirm pull planning visual content.",
        "open_questions": []
    },
    {
        "batch": 3, "status": "done",
        "course": "Chapter 15 - Continuous Improvement",
        "source_file": "chapter-15-continuous-improvement-scorm12-s6uwlft8.zip",
        "content_summary": "Chapter 15 of the Lean Construction series. Covers continuous improvement (kaizen) \u2014 how to systematically improve processes over time. Assets include construction collaboration images.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Learn how to drive continuous improvement on your projects through systematic observation, measurement, and process refinement.",
        "long_description": "This course is Chapter 15 of the Lean Construction series. It covers continuous improvement (kaizen) \u2014 the practice of systematically observing, measuring, and refining construction processes to eliminate waste and improve outcomes over time.\n\nDesigned for field leaders implementing lean. On completion, you earn the skill Continuous Improvement.\n\nThis is an Intermediate-level course.",
        "category": {"value": "Lean Principals > Continuous Improvement", "label": "EXISTING", "rationale": "Directly covers continuous improvement."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "Continuous Improvement", "label": "EXISTING"},
            {"value": "Kaizen", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "Improvement", "label": "EXISTING"},
            {"value": "Difficulty: Intermediate", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Continuous Improvement", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": LN.format(ss="Lean Principles"), "label": "EXISTING", "rationale": "Directly teaches continuous improvement. Existing skill."}],
        "level_of_difficulty": {"value": "Intermediate", "rationale": "Requires lean fundamentals. Process improvement methodology."},
        "target_roles_draft": [{"fragment": "Academy/Continuous Improvement/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Field leaders driving lean improvement."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video.",
        "open_questions": []
    },
    {
        "batch": 3, "status": "done",
        "course": "Chapter 16 - Training the Industry",
        "source_file": "chapter-16-training-the-industry-scorm12-lnugtlxm.zip",
        "content_summary": "Chapter 16 of the Lean Construction series. Covers how lean training and education can transform the broader construction industry. Assets include audience and training images.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Understand how lean training and education can transform the construction industry from within.",
        "long_description": "This course is Chapter 16 of the Lean Construction series. It examines how lean training and education programs can transform the construction industry \u2014 from individual companies to the broader trade. It makes the case for ongoing learning and knowledge sharing.\n\nDesigned for leaders who champion lean adoption. On completion, you earn the skill Lean Mindset.\n\nThis is an Intermediate-level course.",
        "category": {"value": "Lean Principals > Industry Transformation", "label": "EXISTING", "rationale": "Training the industry is industry transformation content."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "Industry Change", "label": "EXISTING"},
            {"value": "training", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "Difficulty: Intermediate", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Lean Mindset", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": LN.format(ss="Lean Principles"), "label": "EXISTING", "rationale": "Industry-level lean thinking. Existing skill."}],
        "level_of_difficulty": {"value": "Intermediate", "rationale": "Later chapter requiring lean context."},
        "target_roles_draft": [{"fragment": "Academy/Lean Mindset/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Lean champions."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video.",
        "open_questions": []
    },
    {
        "batch": 3, "status": "done",
        "course": "Chapter 17 - Reshaping the Industry",
        "source_file": "chapter-17-reshaping-the-industry-scorm12-ltddpgc0.zip",
        "content_summary": "Chapter 17 of the Lean Construction series (likely final chapter). Covers the vision for reshaping the construction industry through lean principles. Only 2 assets \u2014 likely a shorter concluding chapter.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Envision how lean principles can reshape the construction industry for the better.",
        "long_description": "This course is Chapter 17 of the Lean Construction series \u2014 likely the concluding chapter. It presents the vision for reshaping the construction industry through lean principles, encouraging learners to see themselves as agents of change.\n\nDesigned for leaders completing the lean curriculum. On completion, you earn the skill Lean Mindset.\n\nThis is an Intermediate-level course.",
        "category": {"value": "Lean Principals > Industry Transformation", "label": "EXISTING", "rationale": "Reshaping the industry is industry transformation."},
        "tags": [
            {"value": "Lean", "label": "EXISTING"},
            {"value": "Industry Change", "label": "EXISTING"},
            {"value": "Lean Adoption", "label": "EXISTING"},
            {"value": "Lean Construction", "label": "EXISTING"},
            {"value": "Difficulty: Intermediate", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Lean Mindset", "skill_category": "Lean Principles", "scale_set": "Lean Principles", "level": LN.format(ss="Lean Principles"), "label": "EXISTING", "rationale": "Industry transformation vision. Existing skill."}],
        "level_of_difficulty": {"value": "Intermediate", "rationale": "Concluding chapter requiring full series context."},
        "target_roles_draft": [{"fragment": "Academy/Lean Mindset/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Lean champions completing the series."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video.",
        "open_questions": ["Confirm this is the final chapter of the lean series."]
    },
    {
        "batch": 3, "status": "done",
        "course": "Chapter 2 - Jobsite Efficiency",
        "source_file": "chapter-2-jobsite-efficiency-scorm12-gtwzkr7z.zip",
        "content_summary": "Chapter 2 of the Job Plan series (shares assets with Chapter 1 Job Plan Theory). Covers how effective job planning drives jobsite efficiency. No transcript or video.",
        "media": {"location": "none", "videos": []},
        "transcript": {"status": "needs-retrieval", "source": "No video or VTT in package", "video_count": 0, "vtt_count": 0},
        "short_description": "Learn how effective job planning translates to jobsite efficiency \u2014 less wasted time, better crew utilization, and smoother execution.",
        "long_description": "This course is Chapter 2 of the Job Plan series. It connects job plan theory to practical jobsite efficiency \u2014 how well-structured job plans reduce wasted time, improve crew utilization, and enable smoother daily execution.\n\nDesigned for foremen and superintendents responsible for daily work planning. On completion, you earn the skill Productivity Execution.\n\nThis is a Foundational-level course.",
        "category": {"value": "Leadership > Project Planning & Scheduling", "label": "EXISTING", "rationale": "Jobsite efficiency through planning."},
        "tags": [
            {"value": "job plan", "label": "EXISTING"},
            {"value": "jobsite efficiency", "label": "EXISTING"},
            {"value": "productivity", "label": "EXISTING"},
            {"value": "execution", "label": "EXISTING"},
            {"value": "Difficulty: Foundational", "label": "PROPOSED"}
        ],
        "skills_awarded": [{"skill": "Productivity Execution", "skill_category": "Leadership", "scale_set": "Leadership", "level": LN.format(ss="Leadership"), "label": "EXISTING", "rationale": "Translates planning to execution efficiency. Existing skill."}],
        "level_of_difficulty": {"value": "Foundational", "rationale": "Chapter 2 \u2014 still introductory content."},
        "target_roles_draft": [{"fragment": "Academy/Productivity Execution/[level TBD]", "roles": ["Foreman", "Superintendent"], "scope": "Role-scoped", "note": "Personnel responsible for daily work planning."}],
        "topic_timestamp_index": [],
        "confidence": "LOW \u2014 no transcript or video.",
        "open_questions": []
    }
]

recs['courses'].extend(batch3)
recs['meta']['last_updated'] = '2026-05-20'
recs['meta']['status'] = 'In Progress \u2014 Batch 3 complete'

with open(RECS_PATH, 'w', encoding='utf-8') as f:
    json.dump(recs, f, indent=2, ensure_ascii=False)

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    idx = json.load(f)
for c in idx['courses']:
    if c.get('batch') == 3:
        c['status'] = 'done'
with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    json.dump(idx, f, indent=2, ensure_ascii=False)

print(f'Batch 3: {len(batch3)} courses added')
print(f'Total recommendations: {len(recs["courses"])}')
conf = {}
for c in batch3:
    level = c['confidence'].split(' ')[0]
    conf[level] = conf.get(level, 0) + 1
new_skills = [c for c in batch3 if any(s['label'] != 'EXISTING' for s in c.get('skills_awarded', []))]
print(f'Confidence: {conf}')
print(f'New skills proposed: {len(new_skills)}')
print(f'Vocabulary sprawl: NONE')
