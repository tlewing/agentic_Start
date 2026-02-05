# SOP Development Project

## Context
Electrical contractor SOP system — ~90 SOPs covering project management from turnover through closeout.

## SharePoint Integration
- **Site:** https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures
- **Library:** Standard Operating Procedures
- **Template:** GSL_SOP_Master_Template_SHAREPOINT_ENABLED (v1)

## Key Files
- `docs/_VISION.md` — Project goals and scope
- `docs/_AGENTS.md` — Work tracking and SOP status
- `SharePoint-SOPs/` — Downloaded SOPs from SharePoint
- `Templates/` — Downloaded SOP template
- `Revised-SOPs/` — Revised SOPs ready for upload
- `scripts/` — PowerShell scripts for SharePoint sync

## Workflow

### 1. Download from SharePoint
```powershell
cd C:\Users\tewing\Desktop\Holding\SOP\scripts
.\1_Connect-SharePoint.ps1   # Authenticate (once per session)
.\2_Download-SOPs.ps1        # Download all SOPs
.\3_Download-Template.ps1    # Download template
```

### 2. Review & Revise
- Read SOPs from `SharePoint-SOPs/`
- Apply template structure
- Save revised versions to `Revised-SOPs/`
- Update status in `docs/_AGENTS.md`

### 3. Upload to SharePoint
```powershell
.\4_Upload-SOP.ps1 -FilePath "path\to\SOP.docx"  # Single file
.\5_Upload-All-Revised.ps1                       # All revised
```

## Quality Checks
- Is the SOP actionable (not theoretical)?
- Does it specify tools/systems (Procore, etc.)?
- Is ownership clear (PM vs Field Supervisor)?
- Are related SOPs cross-referenced?
- Does it follow the GSL template structure?

## Duplicates
Some SOPs exist with old (9.3.xxx) and new (9.41.xxx) numbering. Prefer the 9.41.xxx versions.
