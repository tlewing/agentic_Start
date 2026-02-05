# SOP Creation Skill

## Overview

Use this skill to create Standard Operating Procedures (SOPs) based on the GSL master template. The template includes a branded header, structured sections, a RACI responsibility matrix, and SharePoint metadata properties.

## Files

- **Template:** `GSL_SOP_Master_Template.docx`
- **Header Image:** `assets/GSL Header Image.png` (already embedded in template)

---

## SOP Numbering System

**Format:** `9.[Phase].[NNN] – SOP Title`

| Phase | Title |
|-------|-------|
| 9.1 | Procurement, Design & Estimating |
| 9.2 | Pre-Construction |
| 9.3 | Mobilization & Jobsite Setup |
| 9.4 | Construction |
| 9.5 | Testing & Commissioning |
| 9.6 | Project Closeout |

**Examples:**
- `9.1.001 – Bid Package Review`
- `9.3.001 – Equipment Checkout`
- `9.4.015 – Daily Progress Reporting`
- `9.6.003 – Final Documentation Turnover`

---

## Workflow

### Step 1: Copy the Template

```bash
cp "/mnt/skills/user/sop-creation/GSL_SOP_Master_Template.docx" "/home/claude/new_sop.docx"
```

### Step 2: Unpack the Document

```bash
python /mnt/skills/public/docx/scripts/office/unpack.py /home/claude/new_sop.docx /home/claude/unpacked/
```

### Step 3: Edit the Document Content

Edit `/home/claude/unpacked/word/document.xml` using the str_replace tool.

**Replace all placeholders with actual content:**

| Placeholder | Replace With | Example |
|-------------|--------------|---------|
| `[SOP #]` | SOP identifier (see numbering system below) | 9.4.001 |
| `[SOP Title]` | Descriptive title | Equipment Checkout |
| `[Department(s)]` | Applicable departments | Operations, Field Services |
| `[Related SOP Title]` | Related procedure titles | Equipment Maintenance |
| `[Condition / trigger #1]` | Scope conditions | An employee needs equipment for a field assignment |
| `[Role / Title]` | Job titles/roles | Project Manager |
| `[Responsibility]` | Specific responsibilities | Reviews and validates change requests |
| `[Requirement #1]` | Required inputs/tools | Equipment Checkout Log (ECL-01) |
| `[Step Name]` | Procedure step titles | Submit Request |
| `[Describe what happens...]` | Step descriptions | The requestor completes the form... |
| `[Template / Log / Form Name]` | Appendix items | Equipment Checkout Log (ECL-01) |

### Step 4: Update the Footer

The template has multiple footer files. **Edit `/home/claude/unpacked/word/footer2.xml`** (this is the default footer):

Find and replace the placeholder text:
```xml
<w:t>[SOP #] – [SOP Title]</w:t>
```

Replace with the actual SOP identifier and title:
```xml
<w:t>9.3.001 – Equipment Checkout</w:t>
```

**Note:** The footer uses a SAVEDATE field that auto-updates. The cached date value may also need updating.

**Final footer format:** `[SOP #] – [SOP Title] | Revised: [M/D/YY]`

Example: `9.3.001 – Equipment Checkout | Revised: 1/29/26`

### Step 5: Update the RACI Matrix

In `document.xml`, update the RACI table:

1. Replace `SOP` in the header cell with `SOP: [SOP #] – [SOP Title]`
2. Replace `Role / Title 1` through `Role / Title 10` with actual role names
3. Replace `List Responsibility 1` through `List Responsibility 14` with actual tasks
4. Add R, A, C, or I in the appropriate cells

**RACI Legend:**
- **R** = Responsible (performs the work)
- **A** = Accountable (approves/owns the outcome)
- **C** = Consulted (provides input)
- **I** = Informed (kept updated)

**Important:** Only ONE person can be Accountable. Only ONE person should be Responsible (though some orgs allow multiple).

### Step 6: Update SharePoint Document Properties

#### Standard Properties (core.xml)

Edit `/home/claude/unpacked/docProps/core.xml`:

```xml
<dc:title>[SOP #] – [SOP Title]</dc:title>
<dc:subject>[Department]</dc:subject>
<dc:description>[Brief description of the SOP]</dc:description>
<cp:keywords>[comma-separated keywords]</cp:keywords>
<cp:category>[Category]</cp:category>
```

#### Custom Properties (custom.xml)

Edit `/home/claude/unpacked/docProps/custom.xml`:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="2" name="ContentTypeId">
    <vt:lpwstr>0x010100833BF49B810F6D48A71C348926804DAC</vt:lpwstr>
  </property>
  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="3" name="Status">
    <vt:lpwstr>Draft</vt:lpwstr>
  </property>
  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="4" name="Document Type">
    <vt:lpwstr>SOP</vt:lpwstr>
  </property>
  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="5" name="SOP ID">
    <vt:lpwstr>[9.X.NNN]</vt:lpwstr>
  </property>
  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="6" name="SOP File Name">
    <vt:lpwstr>[SOP #] – [SOP Title]</vt:lpwstr>
  </property>
  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="7" name="Department / Division">
    <vt:lpwstr>[Department]</vt:lpwstr>
  </property>
  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="8" name="Category (CCC Tag)">
    <vt:lpwstr>[Category Code]</vt:lpwstr>
  </property>
  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="9" name="RACI_Accountable">
    <vt:lpwstr>[Role]</vt:lpwstr>
  </property>
  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="10" name="RACI_Responsible">
    <vt:lpwstr>[Role]</vt:lpwstr>
  </property>
  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="11" name="RACI_Consulted">
    <vt:lpwstr>[Role1; Role2]</vt:lpwstr>
  </property>
  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="12" name="RACI_Informed">
    <vt:lpwstr>[Role1; Role2]</vt:lpwstr>
  </property>
  <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="13" name="Appendix">
    <vt:lpwstr>• [Item 1]
• [Item 2]
• [Item 3]</vt:lpwstr>
  </property>
</Properties>
```

### Step 7: Repack the Document

```bash
python /mnt/skills/public/docx/scripts/office/pack.py /home/claude/unpacked/ "/mnt/user-data/outputs/[9.X.NNN – SOP_Title].docx" --original /home/claude/new_sop.docx
```

---

## SharePoint Metadata Reference

### Required Fields

| Field | Type | Valid Options | Default |
|-------|------|---------------|---------|
| **Status** | Single choice | `Draft`, `Under Review`, `Approved`, `Retired` | Draft |
| **Document Type** | Single choice | `SOP`, `Form`, `Checklist`, `Template` | SOP |

### Department / Division (Single Choice)

Valid options:
- Operations
- Field Operations
- Safety
- Prefab
- Accounting
- Design / Engineering
- Administration
- Low Voltage Systems
- Human Resources
- Legal / Finance
- Marketing / Business Development
- Estimating

### Category (CCC Tag) (Multi-Choice)

Valid options:
- 100 Estimating
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
- 191 Tools and Equipment Mgmt
- 192 Labor Mgmt
- 193 Safety Mgmt
- 194 Quality Control
- 195 Project Closeout
- 210 Pricing & Cost Control
- 220 Materials & Installation Planning
- 230 Submittals
- 240 Field Involvement/BIM
- 250 Labor Planning

### RACI Role Options

These roles apply to all RACI fields:
- Accounting
- Asst. Project Manager
- Branch Manager
- Business Development
- Chief Estimator
- Estimator
- Foreman
- Superintendent
- General Superintendent
- Lead Estimator
- Prefab Lead
- Project Coordinator
- Project Manager
- Purchasing
- Quality Inspector
- Safety Coordinator
- Scheduler
- Site Administrator
- Subcontractors
- Journeyman
- Apprentice
- Leadman
- Equipment Operator
- Branch Safety Superintendent

### RACI Field Types

| Field | Selection Type | Notes |
|-------|----------------|-------|
| **(RACI) Accountable** | Single choice | Only ONE person can be accountable |
| **(RACI) Responsible** | Single choice | Only ONE person should be responsible |
| **(RACI) Consulted** | Multi-choice | Separate multiple values with semicolons |
| **(RACI) Informed** | Multi-choice | Separate multiple values with semicolons |
| **Roles (RACI)** | Multi-choice | All roles involved in the SOP |

### Text Fields

| Field | Description |
|-------|-------------|
| **SOP ID** | Unique identifier (format: 9.[Phase].[NNN]) |
| **SOP File Name** | Document title format: [SOP #] – [SOP Title] |
| **Title** | Full document title |
| **Description** | Brief description of the SOP purpose |
| **Tags / Keywords** | Search keywords, comma-separated |
| **Appendix** | Related templates, forms, logs (use bullet points with • character) |

### Viewing Document Properties in Word

To verify custom properties were set correctly:
1. Open the document in Word
2. Go to **File → Info**
3. On the right side, click **Properties → Advanced Properties**
4. Select the **Custom** tab to see all custom properties

Alternatively: **File → Info → Show All Properties** (at bottom of properties panel)

---

## Template Structure

The template contains these sections (in order):

1. **Title Block** - SOP #, Title, Department, Related SOPs
2. **Horizontal Rule**
3. **Purpose** - 1-3 sentence description
4. **Horizontal Rule**
5. **Scope** - Conditions/triggers (bullet list)
6. **Horizontal Rule**
7. **Roles & Responsibilities** - 4 role blocks with bulleted responsibilities
8. **Horizontal Rule**
9. **Requirements** - Required inputs, tools, references (bullet list)
10. **Horizontal Rule**
11. **Procedure** - 7 numbered steps with descriptions
12. **Horizontal Rule**
13. **Appendix** - Templates, logs, forms (bullet list)
14. **Page Break**
15. **RACI Matrix** - Responsibility assignment table
16. **RACI Legend** - Explanation of R, A, C, I

---

## XML Editing Guidelines

### Preserve Paragraph Properties

**Critical:** Do not remove these tags that control page breaks:
- `<w:keepNext/>` - Keeps paragraph with next paragraph
- `<w:keepLines/>` - Prevents page break within paragraph

These ensure:
- Section headers stay with their content
- Role titles stay with their responsibilities
- Step names stay with their descriptions

### Preserve Formatting

- Keep `<w:b/>` and `<w:bCs/>` tags for bold text
- Maintain `<w:pStyle w:val="ListParagraph"/>` for bullet items
- Preserve indentation tags: `<w:ind w:left="360"/>` for procedure steps

### Adding/Removing List Items

To add a bullet item, copy an existing `<w:p>` block that contains:
```xml
<w:pStyle w:val="ListParagraph"/>
<w:numPr>
  <w:ilvl w:val="0"/>
  <w:numId w:val="XX"/>
</w:numPr>
```

To remove items, delete the entire `<w:p>...</w:p>` block.

### Adding/Removing Procedure Steps

Each step consists of two paragraphs:
1. Bold step header: `Step X – [Step Name]`
2. Description paragraph

Copy or delete both paragraphs together. Ensure both have `<w:keepNext/>` and `<w:keepLines/>` tags.

### Adding/Removing RACI Rows

Each table row is a `<w:tr>...</w:tr>` block. Copy an existing data row and modify the responsibility label and RACI indicators.

---

## Output

Save final documents to `/mnt/user-data/outputs/` with a descriptive filename:
- Format: `9.X.NNN – [SOP_Title].docx`
- Example: `9.3.001 – Equipment Checkout.docx`

---

## Checklist Before Delivery

### Document Content
- [ ] All placeholder text replaced with actual content
- [ ] Footer shows: `[SOP #] – [SOP Title] | Revised: [M/D/YY]` (edit footer2.xml)
- [ ] RACI matrix header shows `SOP: [SOP #] – [SOP Title]`
- [ ] RACI matrix roles and responsibilities filled in
- [ ] RACI matrix has R, A, C, I indicators in cells
- [ ] RACI legend appears below the matrix

### Paragraph Properties
- [ ] Role titles have `<w:keepNext/>` to stay with responsibilities
- [ ] All `<w:keepLines/>` tags preserved

### SharePoint Properties
- [ ] Status set to "Draft"
- [ ] Document Type set to "SOP"
- [ ] SOP ID matches document content
- [ ] SOP File Name includes .docx extension
- [ ] Department / Division is valid option from list
- [ ] Category (CCC Tag) is valid option from list
- [ ] RACI Accountable has exactly ONE role
- [ ] RACI Responsible has exactly ONE role
- [ ] RACI Consulted/Informed use semicolons for multiple roles
