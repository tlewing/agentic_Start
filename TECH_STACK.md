# Tech Stack - GSL Electric L&D Platform

## Platforms
- SharePoint Online (Microsoft 365)
- Learn365 by Zensai (LMS, runs in SharePoint)
- Microsoft Forms (learner intake)
- Microsoft Lists (Learner_Registry)

## Automation & Integration
- Power Automate (Forms > SharePoint, SOP review reminders)
- Anthropic Messages API (Claude AI for grading + roadmap generation)
- Model: claude-sonnet-4-5-20250929 (grading) or claude-opus-4-5-20251101 (roadmaps)

## Scripting
- Node.js (document generation, API integrations)
- PowerShell / PnP PowerShell (SharePoint automation)
- Python (data processing, CSV generation)

## Document Formats
- SOPs: Word (.docx) stored in SharePoint document library
- Training content: Learn365 native (e-learning, ILT, training plans)
- Cross-references: SharePoint lists with hyperlink columns

## MCP Servers
- SharePoint MCP: sekops-ch/sharepoint-mcp-server (pending - waiting on IT for Azure AD credentials)
- Home Assistant MCP: homeassistant-mcp (configured)

## Key URLs
| Resource | URL |
|----------|-----|
| GSL Academy | https://gslelectric8540.sharepoint.com/sites/GSLAcademy |
| SOP Site | https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures |
| Learner_Registry | https://gslelectric8540.sharepoint.com/sites/GSLAcademy/Lists/Learner_Registry |

## Local Paths
| Resource | Path |
|----------|------|
| Pre-Con Manual | `C:\Users\tewing\OneDrive - GSL Electric\TrainingAndResourceMaterials\PreConPlanning` |
| EPMP Manual | `C:\Users\tewing\OneDrive - GSL Electric\TrainingAndResourceMaterials\ProjectManagement` |
