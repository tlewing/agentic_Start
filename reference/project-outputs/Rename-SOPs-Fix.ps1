<#
.SYNOPSIS
    Fix SOP names - remove extra dashes and clean up formatting
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

$dash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Fix SOP Names" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

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

$RoleMapping = @{
    "9.2" = @("PM", "APM", "Foreman"); "9.3" = @("Foreman", "General Superintendent")
    "9.41.0" = @("PM", "Foreman"); "9.41.1" = @("PM", "Project Coordinator")
    "9.41.2" = @("PM", "Project Coordinator"); "9.41.3" = @("PM", "Scheduler", "Foreman")
    "9.41.4" = @("PM", "Accounting", "Business Manager")
    "9.41.47" = @("Safety", "Foreman", "General Superintendent")
    "9.41.48" = @("Safety", "Foreman"); "9.41.49" = @("Safety", "Foreman")
    "9.41.5" = @("QC", "Foreman"); "9.41.6" = @("Purchasing", "PM", "Foreman")
    "9.41.7" = @("Foreman", "General Superintendent")
    "9.5" = @("PM", "Foreman", "QC"); "9.6" = @("PM", "Project Coordinator", "Foreman")
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

function Clean-SOPTitle {
    param([string]$rawText)

    $title = $rawText

    # Remove common suffixes
    $title = $title -replace "REVISED", ""

    # Remove SOP prefix
    $title = $title -replace "SOP", ""

    # Replace all dash types with standard hyphen temporarily
    $title = $title -replace "[\x{2013}\x{2014}]", "-"

    # Remove leading/trailing dashes and spaces (multiple passes)
    for ($i = 0; $i -lt 5; $i++) {
        $title = $title -replace "^[\s\-_]+", ""
        $title = $title -replace "[\s\-_]+$", ""
    }

    # Add spaces to camelCase
    $title = $title -creplace '([a-z])([A-Z])', '$1 $2'
    $title = $title -creplace '([A-Z]+)([A-Z][a-z])', '$1 $2'

    # Replace underscores with spaces
    $title = $title -replace "_", " "

    # Clean up multiple spaces
    $title = $title -replace "\s+", " "

    # Final trim
    $title = $title.Trim()

    return $title
}

# Get SharePoint items
Write-Host "Getting SharePoint items..." -ForegroundColor Yellow
$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
Write-Host "Found $($items.Count) files`n" -ForegroundColor Cyan

$spRenamed = 0
$spUpdated = 0
$spFailed = 0

foreach ($item in $items) {
    $currentName = $item.FieldValues["FileLeafRef"]

    if ($currentName -notmatch "^[\d\.]+") { continue }

    Write-Host "----------------------------------------" -ForegroundColor DarkGray
    Write-Host "Current: $currentName" -ForegroundColor White

    # Remove .docx
    $baseName = $currentName -replace "\.docx$", ""

    # Extract SOP number
    if ($baseName -match "^([\d\.]+)(.*)$") {
        $sopId = $Matches[1].TrimEnd(".")
        $rawTitle = $Matches[2]
    }
    else {
        Write-Host "  Cannot parse" -ForegroundColor Yellow
        continue
    }

    $title = Clean-SOPTitle -rawText $rawTitle

    if ([string]::IsNullOrWhiteSpace($title)) {
        Write-Host "  Empty title" -ForegroundColor Yellow
        continue
    }

    # Build new name with en-dash
    $newName = "$sopId $dash $title"
    $newFileName = "$newName.docx"

    Write-Host "  New: $newFileName" -ForegroundColor Cyan
    Write-Host "  Title: $title" -ForegroundColor Gray

    $catInfo = Get-CategoryInfo -SOPNum $sopId
    $roles = Get-Roles -SOPNum $sopId

    $metadata = @{
        "Title" = $title
        "SOPFileName" = $newName
        "Department_x002f_Division" = $catInfo.Department
        "DocumentType" = "SOP"
        "Status" = "Draft"
    }

    if ($catInfo.CCCTags) { $metadata["Category_x0028_CCCTag_x0029_"] = $catInfo.CCCTags }
    if ($roles) { $metadata["Roles_x0028_RACI_x0029_"] = $roles }

    try {
        if ($currentName -ne $newFileName) {
            $serverRelUrl = $item.FieldValues["FileRef"]
            Rename-PnPFile -ServerRelativeUrl $serverRelUrl -TargetFileName $newFileName -Force -ErrorAction Stop
            Write-Host "  [RENAMED]" -ForegroundColor Green
            $spRenamed++
        }

        Set-PnPListItem -List $LibraryName -Identity $item.Id -Values $metadata -ErrorAction Stop | Out-Null
        Write-Host "  [OK]" -ForegroundColor Green
        $spUpdated++
    }
    catch {
        Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
        $spFailed++
    }
}

# Now process local files
Write-Host "`n========================================" -ForegroundColor Yellow
Write-Host "  Processing Local Files" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Yellow

$localFiles = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" -ErrorAction SilentlyContinue
$localRenamed = 0
$localSkipped = 0

foreach ($file in $localFiles) {
    $currentName = $file.Name

    if ($currentName -notmatch "^[\d\.]+") { continue }

    Write-Host "----------------------------------------" -ForegroundColor DarkGray
    Write-Host "Current: $currentName" -ForegroundColor White

    $baseName = $currentName -replace "\.docx$", ""

    if ($baseName -match "^([\d\.]+)(.*)$") {
        $sopId = $Matches[1].TrimEnd(".")
        $rawTitle = $Matches[2]
    }
    else {
        continue
    }

    $title = Clean-SOPTitle -rawText $rawTitle

    if ([string]::IsNullOrWhiteSpace($title)) { continue }

    $newFileName = "$sopId $dash $title.docx"

    if ($currentName -eq $newFileName) {
        Write-Host "  Already correct" -ForegroundColor Gray
        continue
    }

    Write-Host "  New: $newFileName" -ForegroundColor Cyan

    $newPath = Join-Path $LocalSOPPath $newFileName

    if (Test-Path $newPath) {
        Write-Host "  [SKIP] Already exists" -ForegroundColor Yellow
        $localSkipped++
        continue
    }

    try {
        Rename-Item -Path $file.FullName -NewName $newFileName -ErrorAction Stop
        Write-Host "  [RENAMED]" -ForegroundColor Green
        $localRenamed++
    }
    catch {
        Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SharePoint: Renamed=$spRenamed, Updated=$spUpdated, Failed=$spFailed" -ForegroundColor White
Write-Host "  Local: Renamed=$localRenamed, Skipped=$localSkipped" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
