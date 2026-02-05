# GSL Electric SOP Manager - Quick Reference

## Installation

```powershell
# Install PnP.PowerShell (one-time)
Install-Module PnP.PowerShell -Scope CurrentUser
```

## Basic Commands

### Download Template
```powershell
.\GSL-SOPManager.ps1 -Action Template
```

### View Column Configuration
```powershell
.\GSL-SOPManager.ps1 -Action Columns
```

### Validate Metadata
```powershell
.\GSL-SOPManager.ps1 -Action Validate -MetadataPath ".\my-sop-metadata.json"
```

### Create New SOP
```powershell
# Create only (no upload)
.\GSL-SOPManager.ps1 -Action New -SOPName "9.2.025 - Project Change Order Process" -MetadataPath ".\9.2.025-metadata.json"

# Create and upload to SharePoint
.\GSL-SOPManager.ps1 -Action New -SOPName "9.2.025 - Project Change Order Process" -MetadataPath ".\9.2.025-metadata.json" -Upload

# Remove sections during creation
.\GSL-SOPManager.ps1 -Action New -SOPName "9.2.025 - Change Order" -MetadataPath ".\metadata.json" -RemoveSections "Appendix","Requirements" -Upload
```

### Batch Process Multiple SOPs
```powershell
# Process all *-metadata.json files in working folder
.\GSL-SOPManager.ps1 -Action Batch -Upload
```

---

## Metadata JSON Structure

### Minimum Required Fields
```json
{
  "Title": "Project Change Order Process",
  "SOPID": "9.2.025",
  "DocumentType": "SOP",
  "Status": "Draft"
}
```

### Full Example
```json
{
  "Title": "Project Change Order Process",
  "SOPID": "9.2.025",
  "SOPFileName": "9.2.025 - Project Change Order Process.docx",
  "DocumentType": "SOP",
  "Status": "Draft",
  "DepartmentDivision": "Operations",
  "Description": "Description of the SOP...",
  "Purpose": "Purpose statement for the document...",
  "TagsKeywords": "change order, PCO, scope, budget",
  "CategoryCCCTag": ["160 Scope & Change Control", "170 Cost Control & Billing"],
  "RolesRACI": ["PM", "APM", "Foreman"],
  "AssignedDate": "2026-02-01",
  "LastReviewedDate": "2026-01-19",
  "Appendix": ["Form A", "Checklist B"],
  "Steps": [
    {"Name": "Step Name", "Description": "What happens in this step..."}
  ],
  "RACIMatrix": {
    "Roles": ["PM", "APM", "Foreman"],
    "Responsibilities": [
      {"Name": "Task name", "R": [0], "A": [1], "C": [2], "I": []}
    ]
  }
}
```

---

## Valid Field Values

### DocumentType (Required)
- SOP
- Form
- Checklist
- Template

### Status (Required)
- Draft
- Under Review
- Approved
- Retired

### DepartmentDivision
- Operations
- Safety
- Prefab
- Accounting
- Engineering
- Administration

### CategoryCCCTag (Multi-select)
- 110 Mobilization
- 120 Coordination
- 130 Documentation Mgmt
- 140 Communication
- 150 Scheduling
- 160 Scope & Change Control
- 165 Accounting
- 170 Cost Control & Billing
- 180 Subcontractor Mgmt
- 190 Materials Mgmt
- 191 Tools Mgmt
- 192 Labor Mgmt
- 193 Safety Mgmt
- 194 Quality Control
- 195 Project Closeout
- 210 Pricing & Cost Control
- 220 Materials & Installation Planning
- 230 Submittals
- 240 Field Involvement/BIM
- 250 Labor Planning

### RolesRACI (Multi-select)
- PM
- APM
- Foreman
- Purchasing
- QC
- Safety
- Prefab Lead
- Accounting
- Project Coordinator
- Branch Manager
- Engineer
- Scheduler
- Business Manager
- General Superintendent

---

## Sections That Can Be Removed

Use `-RemoveSections` parameter:
- Purpose
- Scope
- RolesResponsibilities
- Requirements
- Procedure
- Appendix

---

## RACI Matrix Format

The `RACIMatrix` object has two parts:

### Roles (column headers)
Array of role names - max 10 roles

### Responsibilities (rows)
Array of objects with:
- `Name`: The responsibility/task name
- `R`: Array of role indices (0-based) that are **Responsible**
- `A`: Array of role indices that are **Accountable**
- `C`: Array of role indices that are **Consulted**
- `I`: Array of role indices that are **Informed**

Example:
```json
{
  "Roles": ["PM", "APM", "Foreman"],
  "Responsibilities": [
    {
      "Name": "Create PCO form",
      "R": [0],      
      "A": [0],      
      "C": [1, 2],   
      "I": []        
    }
  ]
}
```
This means: PM is Responsible and Accountable, APM and Foreman are Consulted.

---

## File Naming Convention

For batch processing, name your metadata files:
```
[SOPName]-metadata.json
```

Examples:
- `9.2.025 - Project Change Order Process-metadata.json`
- `9.1.010 - Safety Meeting Protocol-metadata.json`

The script will create documents named:
- `9.2.025 - Project Change Order Process.docx`
- `9.1.010 - Safety Meeting Protocol.docx`

---

## Working Folder

Default location:
```
C:\Users\tewing\Desktop\Claude Projects\SOPs For Review
```

Place your metadata JSON files here for batch processing.

---

## Troubleshooting

### "PnP.PowerShell not found"
```powershell
Install-Module PnP.PowerShell -Scope CurrentUser -Force
```

### Connection fails
- Make sure you have access to the SharePoint site
- Try: `Disconnect-PnPOnline` then run the script again

### Metadata validation errors
Run validation first:
```powershell
.\GSL-SOPManager.ps1 -Action Validate -MetadataPath ".\metadata.json"
```

### Skip validation (use with caution)
```powershell
.\GSL-SOPManager.ps1 -Action New -SOPName "..." -MetadataPath "..." -SkipValidation
```
