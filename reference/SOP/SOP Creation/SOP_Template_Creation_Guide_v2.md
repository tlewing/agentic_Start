# Detailed Guide: How to Create the GSL SOP Master Template

This document provides a comprehensive, step-by-step guide for recreating the GSL Standard Operating Procedure (SOP) template in Microsoft Word.

---

## Document Overview

The template is a professional SOP document designed for SharePoint integration with the following characteristics:

- **Page Size:** US Letter (8.5" × 11")
- **Margins:** 1 inch on all sides
- **Default Font:** Aptos (theme font) at 12pt
- **Line Spacing:** 1.15 lines with 8pt after paragraphs
- **Total Pages:** 2+ pages (body content + RACI matrix)

---

## 1. Document Setup

### Page Properties

1. Open a new Word document
2. Go to **Layout → Size** and select **Letter (8.5" × 11")**
3. Go to **Layout → Margins** and set:
   - Top: 1"
   - Bottom: 1"
   - Left: 1"
   - Right: 1"
4. Go to **Layout → Page Setup dialog** (click the small arrow) → **Layout** tab:
   - Header from edge: 0.5"
   - Footer from edge: 0.5"

---

## 2. Header Design

The header contains a single branded image spanning the full width.

### Header Image Specifications

| Property | Value |
|----------|-------|
| **File Name** | GSL Header Image.png |
| **Location** | assets folder |
| **Width** | 8.79 inches |
| **Height** | 1.48 inches |
| **Original Size** | 8.41" × 1.33" |
| **Scale** | 105% width × 111% height |

### Header Image Position

| Property | Setting |
|----------|---------|
| **Horizontal** | Absolute position: -1.08" to the right of Column |
| **Vertical** | Absolute position: -0.26" below Paragraph |
| **Move object with text** | ✓ Enabled |
| **Allow overlap** | ✓ Enabled |
| **Lock anchor** | ☐ Disabled |

### Inserting the Header Image

1. Go to **Insert → Header → Edit Header**
2. Click **Insert → Pictures → This Device**
3. Navigate to the assets folder and select **GSL Header Image.png**
4. Right-click the image → **Size and Position**
5. **Size** tab:
   - Width: 8.79"
   - Height: 1.48"
   - ☑ Lock aspect ratio
6. **Position** tab:
   - Horizontal: Absolute position -1.08" to the right of Column
   - Vertical: Absolute position -0.26" below Paragraph
   - ☑ Move object with text
   - ☑ Allow overlap
7. Click **OK**
8. Close header editing

---

## 3. Footer Design

The footer contains dynamic document information.

### Footer Structure

```
[SOP #] – [SOP Title] | Revised: [Auto-Date]
```

### Footer Elements

1. **SOP Identifier:** Bold text showing "[SOP #] – [SOP Title]"
2. **Separator:** " | " (space, pipe, space)
3. **Revision Date:** "Revised: " followed by an auto-updating date field

### Creating the Footer

1. Go to **Insert → Footer → Edit Footer**
2. Set paragraph style to **No Spacing** (Home → Styles → No Spacing)
3. Type `[SOP #] – [SOP Title]` and make it **Bold**
4. Type ` | Revised: ` (with spaces, not bold)
5. Go to **Insert → Quick Parts → Field**
6. Select **SaveDate** from the field list
7. Under **Date formats**, select or type: `M/d/yy`
8. Click **OK**
9. Close footer editing

---

## 4. Paragraph Control Properties

### Overview

To prevent awkward page breaks, apply these paragraph properties throughout the document:

| Property | Purpose | When to Use |
|----------|---------|-------------|
| **Keep with next** | Keeps paragraph on same page as the next paragraph | Section headers, step titles |
| **Keep lines together** | Prevents page break within the paragraph | All content paragraphs |

### How to Apply

1. Select the paragraph(s)
2. Right-click → **Paragraph**
3. Go to **Line and Page Breaks** tab
4. Check the appropriate boxes:
   - ☑ Keep with next
   - ☑ Keep lines together
5. Click **OK**

### Required Settings by Section

| Section/Element | Keep with Next | Keep Lines Together |
|-----------------|:--------------:|:-------------------:|
| SOP Title line | ✓ | ✓ |
| Department line | ✓ | ✓ |
| "Related SOPs:" header | ✓ | ✓ |
| Related SOP items | ✓ | ✓ |
| Horizontal rules | | ✓ |
| "Purpose" header | ✓ | ✓ |
| Purpose content | | ✓ |
| "Scope" header | ✓ | ✓ |
| Scope intro text | ✓ | ✓ |
| Scope bullet items | | ✓ |
| "Roles & Responsibilities" header | ✓ | ✓ |
| Role titles | ✓ | ✓ |
| Responsibility bullet items | ✓ | ✓ |
| "Requirements" header | ✓ | ✓ |
| Requirements intro text | ✓ | ✓ |
| Requirement bullet items | ✓ | ✓ |
| "Procedure" header | ✓ | ✓ |
| Step titles (Step 1, Step 2, etc.) | ✓ | ✓ |
| Step descriptions | ✓ | ✓ |
| "Appendix" header | ✓ | ✓ |
| Appendix bullet items | ✓ | ✓ |

**Key Rule:** Every section header AND its first content paragraph should have "Keep with next" enabled to ensure they stay together.

---

## 5. Content Structure

### Section 1: Document Header Block

#### Title Line
- **Content:** `SOP: [SOP #] – [SOP Title]`
- **Format:** Bold
- **Paragraph:** Keep with next ✓, Keep lines together ✓

#### Department Line
- **Content:** `Department: [Department(s)]`
- **Format:** "Department:" in bold, rest in normal text
- **Paragraph:** Keep with next ✓, Keep lines together ✓

#### Related SOPs Header
- **Content:** `Related SOPs:`
- **Format:** Bold
- **Paragraph:** Keep with next ✓, Keep lines together ✓

#### Related SOP Items
- **Content:** `[SOP #] – [Related SOP Title]` (one per line)
- **Format:** Normal text
- **Paragraph:** Keep with next ✓, Keep lines together ✓
- **Quantity:** 2 placeholder items in template

---

### Horizontal Rules (Section Dividers)

Insert a horizontal rule between each major section.

#### Creating a Horizontal Rule

**Method 1 - Shape:**
1. Go to **Insert → Shapes → Line**
2. Draw a line across the page
3. Format:
   - Color: Gray (#A0A0A0)
   - Weight: 1.5pt
   - Width: Full page width

**Method 2 - Border:**
1. Place cursor on an empty paragraph
2. Go to **Home → Borders → Borders and Shading**
3. Select a bottom border only
4. Color: Gray (#A0A0A0)
5. Width: 1½ pt

**Paragraph Property:** Keep lines together ✓

---

### Section 2: Purpose

#### Header
- **Content:** `Purpose`
- **Format:** Bold
- **Paragraph:** Keep with next ✓, Keep lines together ✓

#### Content
- **Content:** `[Describe the purpose of this SOP in 1–3 sentences.]`
- **Format:** Normal text
- **Paragraph:** Keep lines together ✓

---

### Section 3: Scope

#### Header
- **Content:** `Scope`
- **Format:** Bold
- **Paragraph:** Keep with next ✓, Keep lines together ✓

#### Introductory Text
- **Content:** `Applies to all projects / situations where:`
- **Format:** Normal text
- **Paragraph:** Keep with next ✓, Keep lines together ✓

#### Bullet List
- **Style:** ListParagraph
- **Indentation:** 0.5" left indent, 0.25" hanging indent
- **Items:**
  - `[Condition / trigger #1]`
  - `[Condition / trigger #2]`
  - `[Condition / trigger #3]`
- **Paragraph:** Keep lines together ✓

---

### Section 4: Roles & Responsibilities

#### Header
- **Content:** `Roles & Responsibilities`
- **Format:** Bold
- **Paragraph:** Keep with next ✓, Keep lines together ✓

#### Structure for Each Role

**Role Title:**
- **Content:** `[Role / Title]` or `[Role / Title] (as required)`
- **Format:** Normal text
- **Paragraph:** Keep with next ✓, Keep lines together ✓

**Responsibilities (Bullet List):**
- **Content:** `[Responsibility]` items
- **Format:** ListParagraph style
- **Paragraph:** Keep with next ✓, Keep lines together ✓

#### Template Contains 4 Role Blocks:
1. `[Role / Title]` - 3 responsibilities
2. `[Role / Title]` - 3 responsibilities
3. `[Role / Title] (as required)` - 2 responsibilities
4. `[Role / Title] (as required)` - 2 responsibilities

**Important:** Each role's bullet list uses a SEPARATE numbering definition to prevent lists from continuing across roles.

---

### Section 5: Requirements

#### Header
- **Content:** `Requirements`
- **Format:** Bold
- **Paragraph:** Keep with next ✓, Keep lines together ✓

#### Introductory Text
- **Content:** `[List required inputs, tools, logs, templates, and references.]`
- **Format:** Normal text
- **Paragraph:** Keep with next ✓, Keep lines together ✓

#### Bullet List
- **Items:**
  - `[Requirement #1]`
  - `[Requirement #2]`
  - `[Requirement #3]`
- **Paragraph:** Keep with next ✓, Keep lines together ✓

---

### Section 6: Procedure

#### Header
- **Content:** `Procedure`
- **Format:** Bold
- **Paragraph:** Keep with next ✓, Keep lines together ✓

#### Step Structure

Each procedure step consists of two paragraphs:

**Step Title:**
- **Content:** `Step X – [Step Name]`
- **Format:** Bold
- **Indentation:** 0.25" left indent (360 DXA)
- **Paragraph:** Keep with next ✓, Keep lines together ✓

**Step Description:**
- **Content:** `[Describe what happens in this step. Include who does what and what gets documented.]`
- **Format:** Normal text
- **Indentation:** 0.25" left indent (360 DXA)
- **Paragraph:** Keep with next ✓, Keep lines together ✓

**Blank Line:**
- Empty paragraph with same indentation
- Separates steps visually

#### Template Contains 7 Steps:
- Steps 1-6: Standard placeholder text
- Step 7: Contains sample procedural text as an example

---

### Section 7: Appendix

#### Header
- **Content:** `Appendix`
- **Format:** Bold
- **Paragraph:** Keep with next ✓, Keep lines together ✓

#### Bullet List
- **Items:** 6 placeholders of `[Template / Log / Form Name]`
- **Paragraph:** Keep with next ✓, Keep lines together ✓

---

### Section 8: RACI Matrix (Page 2)

#### Page Break
Insert a **Page Break** before this section:
- Go to **Insert → Page Break** (or press Ctrl+Enter)

#### Table Overview

The RACI matrix is a responsibility assignment table with:
- 12 columns (responsibilities + 10 roles + spacer)
- 16 rows (header rows + 14 responsibility rows)

#### Table Properties

| Property | Value |
|----------|-------|
| **Total Width** | 7.35 inches (10,581 DXA) |
| **Position** | Floating, centered horizontally |
| **Text Wrapping** | Around |

#### Column Widths

| Column | Width | Content |
|--------|-------|---------|
| 1 | 1.49" (2,152 DXA) | "SOP" header / Responsibility names |
| 2-11 | 0.57" each (820-821 DXA) | Role columns |
| 12 | 0.15" (222 DXA) | Spacer column |

#### Creating the Table

1. Go to **Insert → Table → Insert Table**
2. Columns: 12, Rows: 16
3. Right-click table → **Table Properties**
4. **Table** tab:
   - Preferred width: 7.35"
   - Alignment: Center
5. Click **Positioning** button:
   - Horizontal: Center relative to Margin
   - Vertical: 0.15" below Paragraph
   - ☑ Move with text
   - ☑ Allow overlap

#### Header Row Configuration

**Row 1-2 (merged for column headers):**

**Cell A1-A2 (merged vertically):**
- Content: `SOP`
- Font: Aptos Narrow, 20pt, Bold
- Alignment: Center (horizontal and vertical)

**Cells B1-K1 through B2-K2 (each merged vertically):**
- Content: `Role / Title 1` through `Role / Title 10`
- Font: Aptos Narrow, 11pt, Bold
- **Text Direction:** Vertical (bottom to top)
- Alignment: Center

#### Creating Vertical Text in Role Headers

1. Select cells B1 through K1
2. Right-click → **Text Direction**
3. Choose the vertical orientation (text reads bottom to top)
4. Or: **Layout** tab → **Text Direction** button

#### Data Rows (Rows 3-16)

**Column A (Responsibility Names):**
- Content: `List Responsibility 1` through `List Responsibility 14`
- Font: Times New Roman, Bold
- Alignment: Center

**Columns B-K (RACI Indicators):**
- Content: Empty (to be filled with R, A, C, or I)
- Font: Aptos Narrow, 11pt
- Alignment: Center

#### Cell Formatting

**All Cells:**
- Borders: Single line, 1pt, Black
- Vertical alignment: Center

**To apply borders:**
1. Select entire table
2. Go to **Table Design → Borders**
3. Choose **All Borders**
4. Set border style to single line, 1pt

---

## 6. Styles Summary

### Paragraph Styles Used

| Style Name | Purpose | Key Properties |
|------------|---------|----------------|
| Normal | Default body text | Aptos, 12pt, 1.15 line spacing |
| ListParagraph | Bulleted items | 0.5" left indent, 0.25" hanging |
| NoSpacing | Footer text | No spacing after paragraph |
| Header | Header area | Default header formatting |

### Text Formatting

| Element | Formatting |
|---------|------------|
| Section headers | Bold |
| Step titles | Bold |
| Role titles | Normal (not bold) |
| "Department:" label | Bold |
| Body text | Normal |

---

## 7. Bullet List Configuration

### Bullet Properties
- **Symbol:** • (standard bullet)
- **Left Indent:** 0.5" (720 DXA)
- **Hanging Indent:** 0.25" (360 DXA)

### Important: Independent Numbering

Each section's bullet list must use a separate numbering definition. This prevents bullets from one section affecting another.

**To create independent lists:**
1. Create the first bullet list normally
2. For subsequent lists in different sections:
   - Select the text
   - Go to **Home → Numbering dropdown → Define New Number Format**
   - Or right-click the list → **Restart at 1**

---

## 8. Final Assembly Checklist

### Document Setup
- [ ] Page size: Letter (8.5" × 11")
- [ ] Margins: 1" all sides
- [ ] Header distance: 0.5"
- [ ] Footer distance: 0.5"

### Header
- [ ] GSL Header Image inserted
- [ ] Image sized to 8.79" × 1.48"
- [ ] Position: -1.08" horizontal, -0.26" vertical

### Footer
- [ ] SOP identifier in bold
- [ ] Separator: " | "
- [ ] "Revised: " text
- [ ] SAVEDATE field (M/d/yy format)

### Content Sections
- [ ] Title block with placeholders
- [ ] Horizontal rule
- [ ] Purpose section
- [ ] Horizontal rule
- [ ] Scope section with 3 bullet items
- [ ] Horizontal rule
- [ ] Roles & Responsibilities with 4 role blocks
- [ ] Horizontal rule
- [ ] Requirements section with 3 bullet items
- [ ] Horizontal rule
- [ ] Procedure section with 7 steps
- [ ] Horizontal rule
- [ ] Appendix section with 6 bullet items
- [ ] Horizontal rule
- [ ] Page break

### RACI Matrix
- [ ] Table created (12 columns × 16 rows)
- [ ] Column widths set correctly
- [ ] Header cells merged vertically
- [ ] Vertical text in role columns
- [ ] All borders applied

### Paragraph Properties
- [ ] All section headers: Keep with next ✓, Keep lines together ✓
- [ ] All content paragraphs: Keep lines together ✓
- [ ] Step titles and descriptions: Keep with next ✓, Keep lines together ✓
- [ ] Bullet items in critical sections: Keep with next ✓, Keep lines together ✓

### Document Properties (SharePoint Metadata)
- [ ] Status: Set to "Draft"
- [ ] Document Type: Set to "SOP"
- [ ] Company: Set to your company name
- [ ] SOP ID: Placeholder or blank
- [ ] Department / Division: Configured for dropdown
- [ ] RACI properties: Configured
- [ ] Related SOPs: Configured for multi-value
- [ ] Appendix: Configured for multi-value
- [ ] Effective Date: Blank (to be filled per SOP)
- [ ] Last Reviewed Date: Blank (to be filled per SOP)

### Final Steps
- [ ] Save as .docx
- [ ] Test print/PDF to verify no awkward page breaks
- [ ] Place in skills folder for Claude Code

---

## 9. SharePoint Document Properties (Metadata)

The template includes custom document properties that sync with the SharePoint SOP library. These must be configured in Word for proper library integration.

### Accessing Document Properties

1. Go to **File → Info**
2. On the right side, click **Properties → Show All Properties**
3. Or click **Show Fewer Properties** / **Show More Properties** to toggle

### Required Properties

#### Standard Properties

| Property | Default Value | Description |
|----------|---------------|-------------|
| Title | (Add a title) | Full SOP title |
| Tags | (Add a tag) | Keywords for search |
| Comments | (Add comments) | Brief description |
| Subject | (Specify the subject) | Topic area |
| Company | (Specify the company) | Organization name |
| Status | (Add text) | Document status |
| Categories | (Add a category) | Classification |

#### Custom SharePoint Properties

| Property | Default Value | Description |
|----------|---------------|-------------|
| **Status** * | Draft | Document workflow status (Draft, In Review, Approved, etc.) |
| **Document Type** * | SOP | Always "SOP" for this template |
| SOP File Name | (Add text) | Filename without extension |
| Description | (Add text) | Detailed description of the SOP |
| SOP ID | (Add text) | Unique identifier (e.g., SOP-PM-001) |
| Tags / Keywords | (Add text) | Search terms |
| Department / Division | (Select...) | Dropdown selection |

*Properties marked with * are required fields in SharePoint

#### RACI Properties

| Property | Type | Description |
|----------|------|-------------|
| (RACI) Responsible | Select... | Person(s) who do the work |
| (RACI) Accountable | Select... | Person who approves/owns |
| (RACI) Consulted | [Show Details] | People providing input |
| (RACI) Informed | [Show Details] | People kept updated |
| Roles (RACI) | [Show Details] | All roles involved |

#### Related Information

| Property | Type | Description |
|----------|------|-------------|
| Related SOPs | [Show Details] | Links to related procedures |
| Appendix | [Show Details] | Associated templates/forms |
| Category (CCC Tag) | [Show Details] | Category classification |

#### Date Properties

| Property | Default Value | Description |
|----------|---------------|-------------|
| Last Reviewed Date | (Add a date) | Date of last review |
| Effective Date | (Add a date) | Date SOP becomes effective |

#### People Properties

| Property | Default Value | Description |
|----------|---------------|-------------|
| Manager | (Specify the manager) | Responsible manager |
| Author | (Auto-populated) | Document creator |

### Setting Properties in Word

#### For Text Properties:
1. Click in the property field
2. Type the value
3. Press Enter or click away

#### For Selection Properties (Select...):
1. Click **Select...**
2. Choose from the dropdown list
3. Click OK

#### For Multi-Value Properties ([Show Details]):
1. Click **Show Details**
2. Add multiple values as needed
3. Click OK

### Template Default Values

Set these defaults in the template so they appear for all new SOPs:

| Property | Template Default |
|----------|------------------|
| Status | Draft |
| Document Type | SOP |
| Company | GSL (or your company name) |

### Adding Custom Properties Manually

If a property is missing:
1. Go to **File → Info → Properties → Advanced Properties**
2. Click the **Custom** tab
3. Enter the property **Name**
4. Select the **Type** (Text, Date, Number, Yes/No)
5. Enter a **Value**
6. Click **Add**
7. Click **OK**

### Property-to-SharePoint Column Mapping

When uploaded to SharePoint, these Word properties map to library columns:

| Word Property | SharePoint Column |
|---------------|-------------------|
| Title | Title |
| Status (custom) | Status |
| Document Type | Document Type |
| SOP ID | SOP ID |
| Department / Division | Department / Division |
| Effective Date | Effective Date |
| (RACI) Responsible | RACI Responsible |
| (RACI) Accountable | RACI Accountable |
| (RACI) Consulted | RACI Consulted |
| (RACI) Informed | RACI Informed |

---

## 10. File Storage for Claude Code

### Folder Structure

```
C:\Users\tewing\Desktop\Claude Projects\SOP Creation\
├── SKILL.md                              ← Instructions for Claude Code
├── GSL_SOP_Master_Template.docx          ← The completed template
└── assets\
    └── GSL Header Image.png              ← Source image (backup)
```

### Notes

- The header image is embedded in the .docx file, so the assets folder is only needed as a backup or for recreating the template
- The SKILL.md file must be plain text (not a Word document)
- Claude Code will copy and edit the template, preserving all formatting and images

---

## 11. Technical Specifications

| Property | Value |
|----------|-------|
| File Format | Office Open XML (.docx) |
| Page Width | 12,240 DXA (8.5 inches) |
| Page Height | 15,840 DXA (11 inches) |
| Margins | 1,440 DXA (1 inch) each |
| Header Distance | 720 DXA (0.5 inch) |
| Footer Distance | 720 DXA (0.5 inch) |
| Default Font Size | 24 half-points (12pt) |
| Line Spacing | 278 twentieths of a line (≈1.15) |
| Paragraph Spacing After | 160 twentieths of a point (8pt) |
| Bullet Indent | 720 DXA (0.5 inch) |
| Hanging Indent | 360 DXA (0.25 inch) |
| Step Indent | 360 DXA (0.25 inch) |

---

*This guide incorporates the single GSL header image configuration and comprehensive paragraph control properties to ensure text groupings stay together without page breaks.*
