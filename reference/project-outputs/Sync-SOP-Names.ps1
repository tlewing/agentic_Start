<#
.SYNOPSIS
    Sync SOP names to the authoritative list
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

$enDash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Sync SOP Names to Authoritative List" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Authoritative list of SOP names (ID -> Title)
$targetSOPs = @{
    "9.1.050" = "Prepare Construction Takeoff"
    "9.2.010" = "Team Selection"
    "9.2.015" = "Project Turnover Meeting"
    "9.2.020" = "Procurement of Large Feeder Wire"
    "9.2.030" = "Review Contract for Unfavorable or High-Risk Clauses"
    "9.2.040" = "Project Manager Reviews Plans, Specifications & Schedule"
    "9.2.050" = "Field Supervisor Reviews Plans, Specifications & Schedule"
    "9.2.055" = "Compare Est. vs. Planned"
    "9.2.057" = "Identify Value Engineering & Prefabrication Opportunities"
    "9.2.060" = "Create List of Issues & Begin RFI Process"
    "9.2.070" = "Conduct Site Visit"
    "9.2.080" = "Prepare Material Handling Plan"
    "9.2.090" = "Develop Labor Budget"
    "9.2.100" = "Prepare Layout & Sequencing Plan"
    "9.2.110" = "Develop Project Schedule"
    "9.2.120" = "Establish Tracking & Control Systems"
    "9.2.130" = "Construction Execution Kickoff Meeting"
    "9.2.140" = "Develop Project Budget"
    "9.2.160" = "Develop Procurement Plan"
    "9.3.010" = "Setup Office Trailer"
    "9.3.020" = "Setup Storage Trailer"
    "9.3.030" = "Setup Site Fencing and Access Control"
    "9.3.040" = "Setup Temporary Power"
    "9.3.050" = "Setup Temporary Water"
    "9.3.060" = "Setup Sanitary Facilities"
    "9.3.070" = "Setup Temporary Lighting"
    "9.3.080" = "Setup Signage"
    "9.3.090" = "Setup Security"
    "9.3.100" = "Setup Laydown Area"
    "9.3.110" = "Setup Equipment Staging"
    "9.3.120" = "Setup Parking"
    "9.3.470" = "Develop Site-Specific Safety Plan"
    "9.4.010" = "Conduct Coordination Meetings"
    "9.4.020" = "Conduct Subcontractor Coordination Meetings"
    "9.4.030" = "Conduct Client/Owner Meetings"
    "9.4.040" = "Conduct Safety Meetings"
    "9.4.050" = "Conduct Prefabrication Coordination Meetings"
    "9.4.060" = "Conduct Quality Meetings"
    "9.4.190" = "Document Filing Standards"
    "9.4.195" = "Manage Project Documentation System"
    "9.4.200" = "Manage Submittals"
    "9.4.205" = "Manage RFIs (Requests for Information)"
    "9.4.210" = "Manage Meeting Minutes"
    "9.4.215" = "Manage Daily Reports"
    "9.4.220" = "Manage Drawing Logs"
    "9.4.225" = "Manage Specifications"
    "9.4.230" = "Manage Correspondence"
    "9.4.235" = "Manage Permits"
    "9.4.240" = "Manage Inspection Reports"
    "9.4.270" = "Manage Project Communications"
    "9.4.275" = "Manage Internal Communications"
    "9.4.280" = "Manage External Communications"
    "9.4.285" = "Manage Client/Owner Communications"
    "9.4.290" = "Manage Subcontractor Communications"
    "9.4.295" = "Manage Vendor/Supplier Communications"
    "9.4.300" = "Manage Architect/Engineer Communications"
    "9.4.305" = "Manage Regulatory/Authority Communications"
    "9.4.310" = "Manage General Contractor Communications"
    "9.4.315" = "Develop Project Schedule"
    "9.4.320" = "Update Project Schedule"
    "9.4.325" = "Monitor Schedule Performance"
    "9.4.330" = "Develop Schedule Recovery Plans"
    "9.4.335" = "Prepare Lookahead Schedules"
    "9.4.340" = "Manage Resource-Loaded Schedules"
    "9.4.345" = "Conduct Schedule Review Meetings"
    "9.4.350" = "Manage Schedule Change Requests"
    "9.4.355" = "Manage Project Scope"
    "9.4.360" = "Manage Change Orders"
    "9.4.365" = "Manage Potential Change Orders (PCOs)"
    "9.4.370" = "Manage Owner Directives"
    "9.4.375" = "Manage Scope Clarifications"
    "9.4.380" = "Manage Backcharges"
    "9.4.385" = "Manage Force Account Work"
    "9.4.390" = "Manage Claims"
    "9.4.400" = "Monitor Project Costs"
    "9.4.405" = "Manage Cost Forecasts"
    "9.4.410" = "Manage Cost Codes"
    "9.4.415" = "Manage Committed Costs"
    "9.4.420" = "Manage Actual Costs"
    "9.4.425" = "Manage Job Cost Reports"
    "9.4.430" = "Manage Profit Projections"
    "9.4.435" = "Manage Cost-to-Complete"
    "9.4.440" = "Prepare Billing Schedule"
    "9.4.445" = "Prepare Monthly Pay Applications"
    "9.4.450" = "Track Accounts Receivable"
    "9.4.455" = "Manage Lien Waivers"
    "9.4.460" = "Manage Retainage"
    "9.4.465" = "Manage Final Invoicing"
    "9.4.475" = "Conduct Safety Orientation"
    "9.4.480" = "Conduct Safety Inspections"
    "9.4.485" = "Conduct Safety Meetings"
    "9.4.490" = "Report Safety Incidents"
    "9.4.495" = "Investigate Accidents"
    "9.4.500" = "Conduct Emergency Preparedness"
    "9.4.505" = "Conduct Safety Compliance Audits"
    "9.4.510" = "Provide Safety Training"
    "9.4.515" = "Develop Quality Management Plan"
    "9.4.520" = "Conduct Quality Meetings"
    "9.4.525" = "Conduct Quality Inspections"
    "9.4.530" = "Manage Quality Testing"
    "9.4.535" = "Manage Nonconformance Reports (NCRs)"
    "9.4.540" = "Manage Quality Records"
    "9.4.545" = "Manage Punch List Quality"
    "9.4.560" = "Manage Manpower Allocation"
    "9.4.565" = "Manage Equipment Allocation"
    "9.4.570" = "Manage Material Allocation"
    "9.4.575" = "Manage Subcontractor Resources"
    "9.4.580" = "Manage Vendor Resources"
    "9.4.585" = "Plan Prefabrication Resources"
    "9.4.590" = "Manage Specialty Contractor Resources"
    "9.4.595" = "Prepare Resource Reports"
    "9.4.605" = "Issue Purchase Orders"
    "9.4.610" = "Manage Vendor Prequalification"
    "9.4.615" = "Manage Vendor Evaluations"
    "9.4.620" = "Manage Expediting"
    "9.4.625" = "Manage Delivery Tracking"
    "9.4.630" = "Manage Material Receiving"
    "9.4.631" = "Release of Large Feeder Wire"
    "9.4.635" = "Manage Material Inspection"
    "9.4.640" = "Manage Storage and Logistics"
    "9.4.645" = "Manage Material Handling"
    "9.4.650" = "Manage Inventory"
    "9.4.655" = "Prepare Procurement Reports"
    "9.4.660" = "Manage Procurement Closeout"
    "9.4.665" = "Reconcile Procurement Accounts"
    "9.4.670" = "Manage Vendor Closeout"
    "9.4.675" = "Conduct Daily Huddles"
    "9.4.680" = "Conduct Weekly Foreman Meetings"
    "9.4.690" = "Track Manpower Utilization"
    "9.4.695" = "Track Production Quantities"
    "9.4.700" = "Track Equipment Utilization"
    "9.4.705" = "Manage Work Packaging"
    "9.4.710" = "Manage Workface Planning"
    "9.4.715" = "Manage Field Coordination"
    "9.4.720" = "Conduct Productivity Analysis"
    "9.4.725" = "Resolve Field Problems"
    "9.4.735" = "Perform Field Quality Verifications"
    "9.4.745" = "Manage Field Rework"
    "9.4.755" = "Implement Field Productivity Improvements"
    "9.5.015" = "Conduct Commissioning Meetings"
    "9.5.550" = "Manage Commissioning Activities"
    "9.6.005" = "Prepare for Turnover (Field Perspective)"
    "9.6.010" = "Conduct Closeout Meetings"
    "9.6.015" = "Manage Project Turnover Documentation"
    "9.6.020" = "Manage Punch List Closeout"
    "9.6.030" = "Manage As-Built Drawings"
    "9.6.035" = "Submit Warranties"
    "9.6.040" = "Submit O&M Manuals"
    "9.6.050" = "Provide Owner Training"
    "9.6.055" = "Manage Warranties"
    "9.6.060" = "Archive Project Documentation"
    "9.6.070" = "Conduct Post-Project Review"
    "9.6.080" = "Capture Client Feedback"
    "9.6.085" = "Document Lessons Learned"
}

# Connect to SharePoint
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
Write-Host "Found $($items.Count) files in SharePoint`n" -ForegroundColor Cyan

# Build list of current files by SOP ID
$currentFiles = @{}
foreach ($item in $items) {
    $fileName = $item.FieldValues["FileLeafRef"]
    # Extract SOP ID from filename
    if ($fileName -match "^([\d\.]+)") {
        $sopId = $Matches[1].TrimEnd('.')
        if (-not $currentFiles.ContainsKey($sopId)) {
            $currentFiles[$sopId] = @()
        }
        $currentFiles[$sopId] += @{
            Item = $item
            FileName = $fileName
        }
    }
}

# Compare and report
$toRename = @()
$toDelete = @()
$conflicts = @()
$correct = @()

foreach ($sopId in ($targetSOPs.Keys | Sort-Object)) {
    $targetTitle = $targetSOPs[$sopId]
    $expectedFileName = "$sopId $enDash $targetTitle.docx"

    if ($currentFiles.ContainsKey($sopId)) {
        $files = $currentFiles[$sopId]
        if ($files.Count -gt 1) {
            # Multiple files with same SOP ID - conflict
            $conflicts += @{
                SOPID = $sopId
                TargetTitle = $targetTitle
                Files = $files
            }
        } else {
            $currentFileName = $files[0].FileName
            # Normalize for comparison (handle different dash types)
            $normalizedCurrent = $currentFileName -replace "[$enDash-]", "-"
            $normalizedExpected = $expectedFileName -replace "[$enDash-]", "-"

            if ($normalizedCurrent -ne $normalizedExpected) {
                $toRename += @{
                    SOPID = $sopId
                    CurrentFileName = $currentFileName
                    NewFileName = $expectedFileName
                    Item = $files[0].Item
                }
            } else {
                $correct += $sopId
            }
        }
    }
}

# Find files to delete (not in target list)
foreach ($sopId in $currentFiles.Keys) {
    if (-not $targetSOPs.ContainsKey($sopId)) {
        foreach ($file in $currentFiles[$sopId]) {
            $toDelete += @{
                SOPID = $sopId
                FileName = $file.FileName
                Item = $file.Item
            }
        }
    }
}

# Report
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  REPORT" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "CORRECT: $($correct.Count) files" -ForegroundColor Green

Write-Host "`nTO RENAME: $($toRename.Count) files" -ForegroundColor Yellow
foreach ($r in $toRename) {
    Write-Host "  $($r.SOPID): $($r.CurrentFileName)" -ForegroundColor Gray
    Write-Host "       -> $($r.NewFileName)" -ForegroundColor White
}

Write-Host "`nCONFLICTS (multiple files with same ID): $($conflicts.Count)" -ForegroundColor Magenta
foreach ($c in $conflicts) {
    Write-Host "  $($c.SOPID) - Target: $($c.TargetTitle)" -ForegroundColor Magenta
    foreach ($f in $c.Files) {
        Write-Host "       - $($f.FileName)" -ForegroundColor Gray
    }
}

Write-Host "`nTO DELETE (not in target list): $($toDelete.Count) files" -ForegroundColor Red
foreach ($d in $toDelete) {
    Write-Host "  $($d.SOPID): $($d.FileName)" -ForegroundColor Red
}

# Prompt to proceed
Write-Host "`n========================================" -ForegroundColor Yellow
$proceed = Read-Host "Proceed with renames and deletions? (y/n)"

if ($proceed -eq 'y') {
    # Perform renames
    Write-Host "`nRenaming files..." -ForegroundColor Yellow
    $renamedCount = 0
    foreach ($r in $toRename) {
        try {
            $serverRelativeUrl = $r.Item.FieldValues["FileRef"]
            Rename-PnPFile -ServerRelativeUrl $serverRelativeUrl -TargetFileName $r.NewFileName -Force -ErrorAction Stop

            # Update metadata
            $title = $targetSOPs[$r.SOPID]
            $sopFileName = "$($r.SOPID) $enDash $title"
            Set-PnPListItem -List $LibraryName -Identity $r.Item.Id -Values @{
                "Title" = $title
                "SOPID" = $r.SOPID
                "SOPFileName" = $sopFileName
            } -ErrorAction SilentlyContinue | Out-Null

            Write-Host "  [RENAMED] $($r.SOPID)" -ForegroundColor Green
            $renamedCount++
        }
        catch {
            Write-Host "  [FAILED] $($r.SOPID): $($_.Exception.Message)" -ForegroundColor Red
        }
    }

    # Perform deletions
    Write-Host "`nDeleting files not in target list..." -ForegroundColor Yellow
    $deletedCount = 0
    foreach ($d in $toDelete) {
        try {
            Remove-PnPListItem -List $LibraryName -Identity $d.Item.Id -Force -ErrorAction Stop
            Write-Host "  [DELETED] $($d.FileName)" -ForegroundColor Green
            $deletedCount++
        }
        catch {
            Write-Host "  [FAILED] $($d.FileName): $($_.Exception.Message)" -ForegroundColor Red
        }
    }

    Write-Host "`nRenamed: $renamedCount, Deleted: $deletedCount" -ForegroundColor Cyan
}

Disconnect-PnPOnline

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Read-Host "Press Enter to close"
