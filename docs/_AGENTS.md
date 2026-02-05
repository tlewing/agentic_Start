# Agents

Source of truth for "where are we?" Agents read this at session start. Update it when finishing work.

---

## Active Terminals

| Terminal | Role | Working On | Files Touching | Last Update |
|----------|------|------------|----------------|-------------|
| 1 | Chief of Staff | Morning routine / status | docs/_AGENTS.md | Feb 3 |

Update when starting a terminal. Clear your row on wrap.

---

## Active

| Workstream | Working On | Status |
|------------|------------|--------|
| WS1: Learn365 | Skills Framework setup | Blocked — waiting on SharePoint MCP |
| WS2: SOPs | Procedure extraction from Pre-Con manual | Ready to start |
| WS3: AI Training | Architecture planning | Blocked — needs WS1 skills + WS2 SOPs |

---

## Cross-Agent Notes

*Leave notes here for other agents. Check this section when you activate.*

**For Operations Manager:**
- Phase 1-4 deliverables complete in `deliverables/` folder
- SOP metadata CSV ready at `deliverables/phase2/sop_metadata.csv`
- Scripts for batch processing SOPs in `scripts/`

**For Technical Writer:**
- SOP template: `C:\Users\tewing\Documents\Projects\Templates\GSL_SOP_Master_Template_SHAREPOINT_ENABLED (v1).docx`
- Naming convention: SOP-PC-### (Pre-Con), SOP-PM-### (Project Mgmt), SOP-SF-### (Safety)

---

## Blockers

| Blocker | Waiting On | Impact |
|---------|------------|--------|
| SharePoint MCP | IT (Chad) — Azure AD credentials | Can't access SharePoint lists programmatically |
| Anthropic API key | Provisioning | Can't build WS3 grading system |
| Learn365 user properties | Admin setup | Can't test Target Skill Rules |

---

## Handoffs

### Feb 3 — Chief of Staff

**Done:**
- Phase 1-4 deliverables (Skills, SOPs, JD mapping, MD mapping, Training mapping)
- Learn365 API scripts for skill level sets and target rules
- Jebidiah morning routine documentation
- Created _AGENTS.md for coordination

**Why it's built this way:**
- Three workstreams (WS1, WS2, WS3) are interdependent
- WS3 can't start until WS1 skills and WS2 SOPs exist
- SharePoint MCP will enable automation once credentials arrive

**Next:**
- WS2: Begin extracting procedures from Pre-Con Planning manual (can start now)
- WS1: Wait for SharePoint MCP or work manually in browser

---

## Decisions Needed

| Question | Options | Blocking? |
|----------|---------|-----------|
| SharePoint access method | Manual browser vs wait for MCP | No — can use manual for now |
| SOP extraction priority | Pre-Con first vs EPMP first | No |

---

## Recently Completed

| What | When | Notes |
|------|------|-------|
| Phase 5: Training-SOP mapping | Feb 3 | deliverables/phase5/ |
| Phase 4: MD-SOP mapping | Feb 3 | deliverables/phase4/ |
| Phase 3: JD-SOP mapping | Feb 3 | deliverables/phase3/ |
| Phase 2: SOP analysis & numbering | Feb 3 | deliverables/phase2/ |
| Phase 1: Skills framework | Feb 3 | deliverables/phase1/ |
| Learn365 API integration | Feb 3 | scripts/ |

---

## Standing Decisions

Decisions already made. Agents should follow these.

- **SOP Naming:** SOP-PC-### (Pre-Con), SOP-PM-### (Project Mgmt), SOP-SF-### (Safety)
- **Cross-references:** SOP changes MUST update SOP-Training Cross-Reference list
- **Skill changes:** Must reflect in SOPs, Target Skill Rules, and course configs
- **JD changes:** Never modify without flagging for HR review
- **Learn365:** Target Skill Rule changes take 15+ min to propagate

---

## Key Resources

| Resource | Location |
|----------|----------|
| Big Picture Strategy | `docs/GSL_Big_Picture_Strategy.md` |
| Pre-Con Manual | `C:\Users\tewing\OneDrive - GSL Electric\TrainingAndResourceMaterials\PreConPlanning` |
| EPMP Manual | `C:\Users\tewing\OneDrive - GSL Electric\TrainingAndResourceMaterials\ProjectManagement` |
| GSL Academy | https://gslelectric8540.sharepoint.com/sites/GSLAcademy |
| SOP Site | https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures |

---

## Notes

- SharePoint MCP server: [sekops-ch/sharepoint-mcp-server](https://github.com/sekops-ch/sharepoint-mcp-server)
- IT contact for Azure AD credentials: Chad
- CSV import format for Target Skill Rules: `CatalogName/SkillName/SkillLevel`
