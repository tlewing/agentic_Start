<#
.SYNOPSIS
    Fix SOP metadata - Version 3 (skips SOPID to avoid duplicates)
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Fix SOP Metadata v3" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Category mapping
$CategoryMapping = @{
    "9.2" = @{ CCCTags = @("120 Coordination", "130 Documentation Mgmt", "150 Scheduling"); Department = "Operations" }
    "9.3" = @{ CCCTags = @("110 Mobilization"); Department = "Operations" }
    "9.4" = @{ CCCTags = @("120 Coordination", "130 Documentation Mgmt"); Department = "Operations" }
    "9.41.0" = @{ CCCTags = @("120 Coordination", "140 Communication"); Department = "Operations" }
    "9.41.1" = @{ CCCTags = @("130 Documentation Mgmt"); Department = "Operations" }
    "9.41.2" = @{ CCCTags = @("130 Documentation Mgmt", "140 Communication"); Department = "Operations" }
    "9.41.3" = @{ CCCTags = @("150 Scheduling"); Department = "Operations" }
    "9.41.4" = @{ CCCTags = @("165 Accounting", "170 Cost Control & Billing"); Department = "Accounting" }
    "9.41.47" = @{ CCCTags = @("193 Safety Mgmt"); Department = "Safety" }
    "9.41.48" = @{ CCCTags = @("193 Safety Mgmt"); Department = "Safety" }
    "9.41.49" = @{ CCCTags = @("193 Safety Mgmt"); Department = "Safety" }
    "9.41.5" = @{ CCCTags = @("194 Quality Control"); Department = "Operations" }
    "9.41.6" = @{ CCCTags = @("190 Materials Mgmt"); Department = "Operations" }
    "9.41.7" = @{ CCCTags = @("192 Labor Mgmt", "120 Coordination"); Department = "Operations" }
    "9.5" = @{ CCCTags = @("194 Quality Control"); Department = "Operations" }
    "9.6" = @{ CCCTags = @("195 Project Closeout"); Department = "Operations" }
}

# Role mapping
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
    "9.4" = @("PM", "Foreman")
}

function Get-CategoryInfo {
    param([string]$SOPNum)
    foreach ($key in ($script:CategoryMapping.Keys | Sort-Object -Descending { $_.Length })) {
        if ($SOPNum.StartsWith($key)) { return $script:CategoryMapping[$key] }
    }
    return @{ CCCTags = @("120 Coordination"); Department = "Operations" }
}

function Get-Roles {
    param([string]$SOPNum)
    foreach ($key in ($script:RoleMapping.Keys | Sort-Object -Descending { $_.Length })) {
        if ($SOPNum.StartsWith($key)) { return $script:RoleMapping[$key] }
    }
    return @("PM", "Foreman")
}

function Add-SpacesToCamelCase {
    param([string]$text)
    $result = $text -creplace '([a-z])([A-Z])', '$1 $2'
    $result = $result -creplace '([A-Z]+)([A-Z][a-z])', '$1 $2'
    return $result
}

function Clean-Title {
    param([string]$rawTitle)

    # Remove leading dashes, underscores, spaces
    $title = $rawTitle -replace "^[\s\-_]+", ""

    # Remove "SOP" prefix
    $title = $title -replace "^SOP\s*[\-_]?\s*", ""

    # Add spaces to camelCase
    $title = Add-SpacesToCamelCase -text $title

    # Replace underscores with spaces
    $title = $title -replace "_", " "

    # Clean multiple spaces
    $title = $title -replace "\s+", " "

    return $title.Trim()
}

# Get all items
Write-Host "Getting all items from library..." -ForegroundColor Yellow
$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
Write-Host "Found $($items.Count) files`n" -ForegroundColor Cyan

$updated = 0
$failed = 0
$skipped = 0

foreach ($item in $items) {
    $fileName = $item.FieldValues["FileLeafRef"]

    # Skip non-SOP files
    if ($fileName -notmatch "^[\d\.]+") {
        $skipped++
        continue
    }

    Write-Host "----------------------------------------" -ForegroundColor DarkGray
    Write-Host "Processing: $fileName" -ForegroundColor White

    # Remove extension and "REVISED"
    $baseName = $fileName -replace "\.docx?$", ""
    $baseName = $baseName -replace "\s*-?\s*REVISED\s*$", ""

    # Extract SOP number (everything before first non-digit-dot character or after last dot-digit)
    if ($baseName -match "^([\d\.]+)(.*)$") {
        $sopId = $Matches[1].TrimEnd(".")
        $rawTitle = $Matches[2]

        $sopTitle = Clean-Title -rawTitle $rawTitle
    }
    else {
        Write-Host "  Could not parse" -ForegroundColor Yellow
        $skipped++
        continue
    }

    # Handle empty title - use a generic one
    if ([string]::IsNullOrWhiteSpace($sopTitle)) {
        $sopTitle = "Standard Operating Procedure"
    }

    # Build proper name format
    $properName = "$sopId - $sopTitle"

    # Get category info and roles
    $catInfo = Get-CategoryInfo -SOPNum $sopId
    $roles = Get-Roles -SOPNum $sopId

    Write-Host "  SOP ID: $sopId" -ForegroundColor Gray
    Write-Host "  Title: $sopTitle" -ForegroundColor Gray
    Write-Host "  SOPFileName: $properName" -ForegroundColor Gray

    # Build metadata - DO NOT include SOPID to avoid duplicate errors
    $metadata = @{
        "Title" = $sopTitle
        "SOPFileName" = $properName
        "Department_x002f_Division" = $catInfo.Department
        "DocumentType" = "SOP"
        "Status" = "Draft"
    }

    # Add CCC Tags
    if ($catInfo.CCCTags -and $catInfo.CCCTags.Count -gt 0) {
        $metadata["Category_x0028_CCCTag_x0029_"] = $catInfo.CCCTags
    }

    # Add Roles
    if ($roles -and $roles.Count -gt 0) {
        $metadata["Roles_x0028_RACI_x0029_"] = $roles
    }

    try {
        Set-PnPListItem -List $LibraryName -Identity $item.Id -Values $metadata -ErrorAction Stop | Out-Null
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
Write-Host "  Skipped: $skipped" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
