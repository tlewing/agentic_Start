# Update Job Descriptions with SOP References
# Run with: powershell.exe -ExecutionPolicy Bypass -File update-jds.ps1

$outputPath = "C:\Users\tewing\Desktop\Claude Projects\Revised Job Descriptions"

# Create output folder
if (-not (Test-Path $outputPath)) {
    New-Item -ItemType Directory -Path $outputPath -Force | Out-Null
}

$word = New-Object -ComObject Word.Application
$word.Visible = $false

# SOP Reference blocks for each JD
$foremanSOPs = @"

================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role is responsible for executing the following SOPs:

- Section 1.1: Team Selection and Estimator Turnover (participates in turnover meeting)
- Section 1.3: Scope and Contract Review (execution planning, VE identification)
- Section 1.5: Material Handling Plan (site receiving, storage layout)
- Section 1.6: Layout and Sequencing Plan (develops installation sequence, field instructions)
- Section 1.7: Schedule Development and Tracking (field schedule coordination)
- SOP 9.4.631: Release of Large Feeder Wire (field measurement, receipt verification)
- SOP OPS-CO-001: Change Order Management (field documentation, T&M tracking)

CRITICAL REQUIREMENTS:
- Per OPS-CO-001/MD 9.3: NEVER perform changed work without PM authorization
- Per Section 1.7/MD 9.3: Document in daily reports any scheduling delays or impacts
- Per SOP 9.4.631/MD 9.3: Timecards must be completed daily with installed quantities

Training Reference: Foreman Training Binder Tabs 2-14, 22, 38, 41, 49, 57
Skill Level: L7 per GSL Academy Target Skill Rules
================================================================================

"@

$opsManagementSOPs = @"

================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

Project Managers are accountable for executing ALL pre-construction SOPs:

- Section 1.1: Team Selection and Estimator Turnover (A/R)
- Section 1.2: Administrative Setup (A/R)
- Section 1.3: Scope and Contract Review (A/R)
- Section 1.4: Buyout Process (A/R)
- Section 1.5: Material Handling Plan (A)
- Section 1.6: Layout and Sequencing Plan (A)
- Section 1.7: Schedule Development and Tracking (A/R)
- SOP 9.4.631: Release of Large Feeder Wire (A)
- SOP Procurement Large Feeder Wire (A/R)
- SOP OPS-CO-001: Change Order Management (A/R)

CRITICAL REQUIREMENTS (Per Management Directives 9.3/9.5):
- Buy out 80-90% of project
- Formal subcontracts required for amounts over $50,000
- Utilize Pull Planning by milestone during the project
- Only accept scope changes from the party directly contracted with
- Always request time extensions when liquidated damages provisions exist

Training Reference: Foreman Training Binder (all tabs), GSL Academy PM modules
================================================================================

"@

$superintendentSOPs = @"

================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role supervises foremen in executing the following SOPs:

- Section 1.1: Team Selection and Estimator Turnover (C - selects Field Supervisor)
- Section 1.3: Scope and Contract Review (C - reviews execution planning)
- Section 1.6: Layout and Sequencing Plan (A - reviews/approves sequencing)
- Section 1.7: Schedule Development and Tracking (C - coordinates field schedule)
- SOP OPS-CO-001: Change Order Management (R - field coordination)

CRITICAL REQUIREMENTS:
- Ensure all foremen comply with SOP OPS-CO-001 authorization requirements
- Monitor critical path items per Section 1.7
- Coordinate change order integration per OPS-CO-001

Training Reference: Foreman Training Binder (all tabs)
Skill Level: L8 per GSL Academy Target Skill Rules
================================================================================

"@

$estimatingSOPs = @"

================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role provides input to the following SOPs:

- Section 1.1: Team Selection and Estimator Turnover (C - presents bid strategy)
- Section 1.3: Scope and Contract Review (C - bid vs. execution comparison)
- SOP OPS-CO-001: Change Order Management (C - cost estimating support)

CRITICAL REQUIREMENTS (Per Management Directive 9.7):
- Participate in Project Turn-Over Meeting following the Turn-Over Meeting Agenda
- All value engineering options shall be reviewed
- All major vendors and subcontractors shall be discussed at turnover

Training Reference: Foreman Training Tabs 3, 11
================================================================================

"@

$leadJourneymanSOPs = @"

================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role executes and provides input to the following SOPs:

- Section 1.5: Material Handling Plan (R - directs material staging)
- Section 1.6: Layout and Sequencing Plan (R - layouts daily work for crew)
- Section 1.7: Schedule Development and Tracking (C - provides field input)
- SOP 9.4.631: Release of Large Feeder Wire (R - leads wire pull activities)
- SOP OPS-CO-001: Change Order Management (I - reports changed conditions)

CRITICAL REQUIREMENT:
- Per OPS-CO-001/MD 9.3: Report any changed conditions to Foreman immediately

Training Reference: Foreman Training Tabs 2, 4, 6, 7, 41
Skill Level: L6 per GSL Academy Target Skill Rules
================================================================================

"@

$journeymanSOPs = @"

================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role executes work under the following SOPs:

- Section 1.5: Material Handling Plan (R - receives and stages materials)
- Section 1.6: Layout and Sequencing Plan (R - follows installation sequences)
- SOP 9.4.631: Release of Large Feeder Wire (R - assists with wire pulls)

Training Reference: GSL Academy L5 Journeyman modules
Skill Level: L5 per GSL Academy Target Skill Rules
================================================================================

"@

$purchasingSOPs = @"

================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role supports the following SOPs:

- Section 1.4: Buyout Process (C - supports procurement process)
- SOP Procurement Large Feeder Wire (R - vendor engagement, PO processing)

CRITICAL REQUIREMENTS (Per Management Directive 9.16):
- Coordinate with Project Management per MD 9.5 requirements
- Formal subcontracts required for amounts over $50,000

================================================================================

"@

$prefabSOPs = @"

================================================================================
APPLICABLE STANDARD OPERATING PROCEDURES
================================================================================

This role provides input to the following SOPs:

- Section 1.1: Team Selection and Estimator Turnover (C - identifies prefab opportunities)
- Section 1.3: Scope and Contract Review (C - prefab opportunity identification)
- Section 1.6: Layout and Sequencing Plan (C - develops prefab drawings)

CRITICAL REQUIREMENT (Per Management Directive 9.5):
- Review each project to proactively determine scope that can be prefabricated

================================================================================

"@

# Function to update a JD
function Update-JD {
    param(
        [string]$sourcePath,
        [string]$outputName,
        [string]$searchText,
        [string]$sopBlock
    )

    try {
        $doc = $word.Documents.Open($sourcePath)
        $find = $doc.Content.Find
        $find.ClearFormatting()

        if ($find.Execute($searchText)) {
            $insertRange = $doc.Content.Duplicate
            $insertRange.Start = $find.Parent.End
            $insertRange.End = $find.Parent.End
            $insertRange.InsertAfter($sopBlock)
        }

        $savePath = Join-Path $outputPath $outputName
        $doc.SaveAs($savePath)
        $doc.Close()
        Write-Host "Updated: $outputName"
        return $true
    }
    catch {
        Write-Host "Error updating $outputName : $_"
        return $false
    }
}

# Update each JD
$results = @()

$results += Update-JD `
    -sourcePath "C:\Users\tewing\Desktop\Claude Projects\Job Descriptions\Policy Manual, 7.2.4 Foreman.doc" `
    -outputName "Policy Manual 7.2.4 Foreman - REVISED.doc" `
    -searchText "Essential Duties and Responsibilities:" `
    -sopBlock $foremanSOPs

$results += Update-JD `
    -sourcePath "C:\Users\tewing\Desktop\Claude Projects\Job Descriptions\Policy Manual, 7.3.1 Operations Management.doc" `
    -outputName "Policy Manual 7.3.1 Operations Management - REVISED.doc" `
    -searchText "Essential Job Functions" `
    -sopBlock $opsManagementSOPs

$results += Update-JD `
    -sourcePath "C:\Users\tewing\Desktop\Claude Projects\Job Descriptions\Policy Manual, 7.2.5 Project Superintendent (General Foreman).doc" `
    -outputName "Policy Manual 7.2.5 Project Superintendent - REVISED.doc" `
    -searchText "Essential Duties and Responsibilities:" `
    -sopBlock $superintendentSOPs

$results += Update-JD `
    -sourcePath "C:\Users\tewing\Desktop\Claude Projects\Job Descriptions\Policy Manual, 7.3.3 Estimating.doc" `
    -outputName "Policy Manual 7.3.3 Estimating - REVISED.doc" `
    -searchText "ESTIMATING JOB DESCRIPTIONS" `
    -sopBlock $estimatingSOPs

$results += Update-JD `
    -sourcePath "C:\Users\tewing\Desktop\Claude Projects\Job Descriptions\Policy Manual, 7.2.3 Lead Journeyman.doc" `
    -outputName "Policy Manual 7.2.3 Lead Journeyman - REVISED.doc" `
    -searchText "Essential Duties and Responsibilities:" `
    -sopBlock $leadJourneymanSOPs

$results += Update-JD `
    -sourcePath "C:\Users\tewing\Desktop\Claude Projects\Job Descriptions\Policy Manual, 7.2.2 Journeyman Electrician.doc" `
    -outputName "Policy Manual 7.2.2 Journeyman Electrician - REVISED.doc" `
    -searchText "Essential Duties and Responsibilities:" `
    -sopBlock $journeymanSOPs

$results += Update-JD `
    -sourcePath "C:\Users\tewing\Desktop\Claude Projects\Job Descriptions\Policy Manual, 7.4.4 Purchasing Manager (Salt Lake Office).doc" `
    -outputName "Policy Manual 7.4.4 Purchasing Manager - REVISED.doc" `
    -searchText "Essential Duties and Responsibilities:" `
    -sopBlock $purchasingSOPs

$results += Update-JD `
    -sourcePath "C:\Users\tewing\Desktop\Claude Projects\Job Descriptions\Policy Manual, 7.3.7 Pre-Fabrication.doc" `
    -outputName "Policy Manual 7.3.7 Pre-Fabrication - REVISED.doc" `
    -searchText "7.3.7" `
    -sopBlock $prefabSOPs

$word.Quit()

Write-Host ""
Write-Host "JD Update Complete"
Write-Host "Files saved to: $outputPath"
$successCount = ($results | Where-Object { $_ -eq $true }).Count
Write-Host "Successfully updated: $successCount files"
