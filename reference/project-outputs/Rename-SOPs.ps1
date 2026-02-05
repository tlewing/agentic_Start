<#
.SYNOPSIS
    Rename SOPs in SharePoint and locally with consistent naming
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

# En-dash character for proper formatting
$dash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Rename SOPs - SharePoint & Local" -ForegroundColor Cyan
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

function Get-CleanSOPName {
    param([string]$fileName)

    # Remove extension
    $baseName = $fileName -replace "\.docx?$", ""

    # Remove REVISED (with various dash formats)
    $baseName = $baseName -replace "\s*[\-\x{2013}\x{2014}]\s*REVISED\s*$", ""
    $baseName = $baseName -replace "\s*REVISED\s*$", ""

    # Extract SOP number and raw title
    if ($baseName -match "^([\d\.]+)(.*)$") {
        $sopId = $Matches[1].TrimEnd(".")
        $rawTitle = $Matches[2]
    }
    else {
        return $null
    }

    # Clean the title
    $title = $rawTitle

    # Remove SOP prefix
    $title = $title -replace "\s*SOP\s*", " "

    # Remove all types of dashes at the start
    $title = $title -replace "^\s*[\-\x{2013}\x{2014}_]+\s*", ""
    $title = $title -replace "^\s*[\-\x{2013}\x{2014}_]+\s*", ""

    # Add spaces to camelCase
    $title = $title -creplace '([a-z])([A-Z])', '$1 $2'
    $title = $title -creplace '([A-Z]+)([A-Z][a-z])', '$1 $2'

    # Replace underscores with spaces
    $title = $title -replace "_", " "

    # Clean up multiple spaces
    $title = $title -replace "\s+", " "

    # Remove any remaining leading dashes
    $title = $title -replace "^[\s\-\x{2013}\x{2014}]+", ""

    $title = $title.Trim()

    if ([string]::IsNullOrWhiteSpace($title)) {
        return $null
    }

    # Build clean name using en-dash
    $cleanName = $sopId + " " + $script:dash + " " + $title

    return @{
        SOPId = $sopId
        Title = $title
        CleanName = $cleanName
    }
}

# Get all items from SharePoint
Write-Host "Getting all items from SharePoint library..." -ForegroundColor Yellow
$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
Write-Host "Found $($items.Count) files in SharePoint`n" -ForegroundColor Cyan

# Get all local files
Write-Host "Getting local files..." -ForegroundColor Yellow
$localFiles = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" -ErrorAction SilentlyContinue
Write-Host "Found $($localFiles.Count) local files`n" -ForegroundColor Cyan

$spRenamed = 0
$spUpdated = 0
$spFailed = 0
$localRenamed = 0
$localFailed = 0

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Processing SharePoint Files" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Yellow

foreach ($item in $items) {
    $currentName = $item.FieldValues["FileLeafRef"]

    if ($currentName -notmatch "^[\d\.]+") {
        continue
    }

    Write-Host "----------------------------------------" -ForegroundColor DarkGray
    Write-Host "Current: $currentName" -ForegroundColor White

    $parsed = Get-CleanSOPName -fileName $currentName

    if (-not $parsed) {
        Write-Host "  Could not parse - skipping" -ForegroundColor Yellow
        continue
    }

    $sopId = $parsed.SOPId
    $title = $parsed.Title
    $newFileName = $parsed.CleanName + ".docx"

    Write-Host "  New Name: $newFileName" -ForegroundColor Cyan
    Write-Host "  Title: $title" -ForegroundColor Gray

    $catInfo = Get-CategoryInfo -SOPNum $sopId
    $roles = Get-Roles -SOPNum $sopId

    $metadata = @{
        "Title" = $title
        "SOPFileName" = $parsed.CleanName
        "Department_x002f_Division" = $catInfo.Department
        "DocumentType" = "SOP"
        "Status" = "Draft"
    }

    if ($catInfo.CCCTags -and $catInfo.CCCTags.Count -gt 0) {
        $metadata["Category_x0028_CCCTag_x0029_"] = $catInfo.CCCTags
    }

    if ($roles -and $roles.Count -gt 0) {
        $metadata["Roles_x0028_RACI_x0029_"] = $roles
    }

    try {
        if ($currentName -ne $newFileName) {
            $serverRelativeUrl = $item.FieldValues["FileRef"]
            Rename-PnPFile -ServerRelativeUrl $serverRelativeUrl -TargetFileName $newFileName -Force -ErrorAction Stop
            Write-Host "  [RENAMED]" -ForegroundColor Green
            $spRenamed++
        }

        Set-PnPListItem -List $LibraryName -Identity $item.Id -Values $metadata -ErrorAction Stop | Out-Null
        Write-Host "  [METADATA OK]" -ForegroundColor Green
        $spUpdated++
    }
    catch {
        Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
        $spFailed++
    }
}

Write-Host "`n========================================" -ForegroundColor Yellow
Write-Host "  Processing Local Files" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Yellow

foreach ($file in $localFiles) {
    $currentName = $file.Name

    if ($currentName -notmatch "^[\d\.]+") {
        continue
    }

    Write-Host "----------------------------------------" -ForegroundColor DarkGray
    Write-Host "Current: $currentName" -ForegroundColor White

    $parsed = Get-CleanSOPName -fileName $currentName

    if (-not $parsed) {
        Write-Host "  Could not parse - skipping" -ForegroundColor Yellow
        continue
    }

    $newFileName = $parsed.CleanName + ".docx"

    if ($currentName -eq $newFileName) {
        Write-Host "  Already correct name" -ForegroundColor Gray
        continue
    }

    Write-Host "  New Name: $newFileName" -ForegroundColor Cyan

    $newPath = Join-Path $LocalSOPPath $newFileName

    if (Test-Path $newPath) {
        Write-Host "  [SKIP] Target file already exists" -ForegroundColor Yellow
        continue
    }

    try {
        Rename-Item -Path $file.FullName -NewName $newFileName -ErrorAction Stop
        Write-Host "  [RENAMED]" -ForegroundColor Green
        $localRenamed++
    }
    catch {
        Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
        $localFailed++
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Rename Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SharePoint:" -ForegroundColor White
Write-Host "    Renamed: $spRenamed" -ForegroundColor Green
Write-Host "    Metadata Updated: $spUpdated" -ForegroundColor Green
Write-Host "    Failed: $spFailed" -ForegroundColor $(if ($spFailed -gt 0) { "Red" } else { "Green" })
Write-Host "  Local Files:" -ForegroundColor White
Write-Host "    Renamed: $localRenamed" -ForegroundColor Green
Write-Host "    Failed: $localFailed" -ForegroundColor $(if ($localFailed -gt 0) { "Red" } else { "Green" })
Write-Host "========================================`n" -ForegroundColor Cyan

Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
