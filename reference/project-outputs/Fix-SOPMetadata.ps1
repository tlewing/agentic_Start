<#
.SYNOPSIS
    Fix SOP metadata for all uploaded documents
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Fix SOP Metadata" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Category mapping based on SOP number prefix
$CategoryMapping = @{
    "9.2" = @{ Category = "Pre-Construction"; CCCTags = @("120 Coordination", "130 Documentation Mgmt", "150 Scheduling"); Department = "Operations" }
    "9.3" = @{ Category = "Site Setup"; CCCTags = @("110 Mobilization"); Department = "Operations" }
    "9.4" = @{ Category = "Project Execution"; CCCTags = @("120 Coordination", "130 Documentation Mgmt"); Department = "Operations" }
    "9.41.0" = @{ Category = "Meetings & Coordination"; CCCTags = @("120 Coordination", "140 Communication"); Department = "Operations" }
    "9.41.1" = @{ Category = "Documentation"; CCCTags = @("130 Documentation Mgmt"); Department = "Operations" }
    "9.41.2" = @{ Category = "Documentation"; CCCTags = @("130 Documentation Mgmt", "140 Communication"); Department = "Operations" }
    "9.41.3" = @{ Category = "Scheduling"; CCCTags = @("150 Scheduling"); Department = "Operations" }
    "9.41.4" = @{ Category = "Cost Control"; CCCTags = @("165 Accounting", "170 Cost Control & Billing"); Department = "Accounting" }
    "9.41.47" = @{ Category = "Safety"; CCCTags = @("193 Safety Mgmt"); Department = "Safety" }
    "9.41.48" = @{ Category = "Safety"; CCCTags = @("193 Safety Mgmt"); Department = "Safety" }
    "9.41.49" = @{ Category = "Safety"; CCCTags = @("193 Safety Mgmt"); Department = "Safety" }
    "9.41.5" = @{ Category = "Quality"; CCCTags = @("194 Quality Control"); Department = "Operations" }
    "9.41.6" = @{ Category = "Procurement"; CCCTags = @("190 Materials Mgmt"); Department = "Operations" }
    "9.41.7" = @{ Category = "Field Operations"; CCCTags = @("192 Labor Mgmt", "120 Coordination"); Department = "Operations" }
    "9.5" = @{ Category = "Commissioning"; CCCTags = @("194 Quality Control"); Department = "Operations" }
    "9.6" = @{ Category = "Closeout"; CCCTags = @("195 Project Closeout"); Department = "Operations" }
}

# Role mapping based on SOP number prefix
$RoleMapping = @{
    "9.2" = @("PM", "APM", "Foreman")
    "9.3" = @("Foreman", "General Superintendent")
    "9.41.0" = @("PM", "Foreman")
    "9.41.1" = @("PM", "Project Coordinator")
    "9.41.2" = @("PM", "Project Coordinator")
    "9.41.3" = @("PM", "Scheduler", "Foreman")
    "9.41.4" = @("PM", "Accounting", "Business Manager")
    "9.41.47" = @("Safety", "Foreman", "General Superintendent")
    "9.41.48" = @("Safety", "Foreman")
    "9.41.49" = @("Safety", "Foreman")
    "9.41.5" = @("QC", "Foreman")
    "9.41.6" = @("Purchasing", "PM", "Foreman")
    "9.41.7" = @("Foreman", "General Superintendent")
    "9.5" = @("PM", "Foreman", "QC")
    "9.6" = @("PM", "Project Coordinator", "Foreman")
}

function Get-CategoryInfo {
    param([string]$SOPNum)

    foreach ($key in ($CategoryMapping.Keys | Sort-Object -Descending { $_.Length })) {
        if ($SOPNum.StartsWith($key)) {
            return $CategoryMapping[$key]
        }
    }
    return @{ Category = "General"; CCCTags = @("120 Coordination"); Department = "Operations" }
}

function Get-Roles {
    param([string]$SOPNum)

    foreach ($key in ($RoleMapping.Keys | Sort-Object -Descending { $_.Length })) {
        if ($SOPNum.StartsWith($key)) {
            return $RoleMapping[$key]
        }
    }
    return @("PM", "Foreman")
}

# Get all items
Write-Host "Getting all items from library..." -ForegroundColor Yellow
$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
Write-Host "Found $($items.Count) files`n" -ForegroundColor Cyan

$updated = 0
$failed = 0

foreach ($item in $items) {
    $fileName = $item.FieldValues["FileLeafRef"]

    # Skip non-SOP files
    if ($fileName -notmatch "^[\d\.]+") {
        continue
    }

    Write-Host "----------------------------------------" -ForegroundColor DarkGray
    Write-Host "Processing: $fileName" -ForegroundColor White

    # Parse filename: "9.2.080 Prepare Material Handling Plan - REVISED.docx"
    $baseName = $fileName -replace "\.docx?$", ""
    $baseName = $baseName -replace "\s*-\s*REVISED\s*$", ""
    $baseName = $baseName -replace "\s*REVISED\s*$", ""

    # Extract SOP number (digits and dots at start)
    $sopId = ""
    $sopTitle = ""

    if ($baseName -match "^([\d\.]+)\s*[_\-]+\s*(.+)$") {
        $sopId = $Matches[1].TrimEnd(".")
        $sopTitle = $Matches[2].Trim()
    }
    elseif ($baseName -match "^([\d\.]+)\s+(.+)$") {
        $sopId = $Matches[1].TrimEnd(".")
        $sopTitle = $Matches[2].Trim()
    }
    else {
        Write-Host "  Could not parse: $baseName" -ForegroundColor Yellow
        continue
    }

    # Clean up title - remove "SOP" prefix if present
    $sopTitle = $sopTitle -replace "^SOP\s*[_\-]*\s*", ""
    $sopTitle = $sopTitle.Trim()

    # Build the proper Name format using en-dash
    $dash = [char]0x2013
    $properName = "$sopId $dash $sopTitle"

    # Get category info
    $catInfo = Get-CategoryInfo -SOPNum $sopId
    $roles = Get-Roles -SOPNum $sopId

    Write-Host "  SOP ID: $sopId" -ForegroundColor Gray
    Write-Host "  Title: $sopTitle" -ForegroundColor Gray
    Write-Host "  Name: $properName" -ForegroundColor Gray
    Write-Host "  Department: $($catInfo.Department)" -ForegroundColor Gray

    # Build metadata update
    $metadata = @{
        "Title" = $sopTitle
        "SOPID" = $sopId
        "SOPFileName" = $properName
        "Department_x002f_Division" = $catInfo.Department
        "DocumentType" = "SOP"
        "Status" = "Draft"
    }

    # Add CCC Tags if available
    if ($catInfo.CCCTags -and $catInfo.CCCTags.Count -gt 0) {
        $metadata["Category_x0028_CCCTag_x0029_"] = $catInfo.CCCTags
    }

    # Add Roles if available
    if ($roles -and $roles.Count -gt 0) {
        $metadata["Roles_x0028_RACI_x0029_"] = $roles
    }

    try {
        Set-PnPListItem -List $LibraryName -Identity $item.Id -Values $metadata | Out-Null
        Write-Host "  [OK] Updated" -ForegroundColor Green
        $updated++
    }
    catch {
        Write-Host "  [FAIL] $($_.Exception.Message)" -ForegroundColor Red
        $failed++
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Metadata Update Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Updated: $updated" -ForegroundColor Green
Write-Host "  Failed: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "========================================`n" -ForegroundColor Cyan

Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
