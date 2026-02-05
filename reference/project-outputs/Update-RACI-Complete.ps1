<#
.SYNOPSIS
    Complete RACI rewrite - Update column choices and all item values
.DESCRIPTION
    1. Updates choice lists on all 5 RACI columns to canonical role names
    2. Rewrites every item with corrected R, A, C, I, and Roles (RACI) values
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$CsvPath = "C:\Users\tewing\Desktop\Claude Projects\Project Outputs\RACI_SharePoint_Complete.csv"

# Canonical choice list for single-choice R and A columns
$SingleChoices = @(
    "Accounting",
    "Asst. Project Manager",
    "Branch Manager",
    "Business Development",
    "Estimator",
    "Foreman",
    "General Superintendent",
    "Prefab Lead",
    "Project Coordinator",
    "Project Manager",
    "Purchasing",
    "Quality Inspector",
    "Safety Coordinator",
    "Scheduler",
    "Site Administrator",
    "Subcontractors"
)

# Extended choice list for multi-choice C and I columns
$MultiChoices = @(
    "Accounting",
    "All Employees",
    "Asst. Project Manager",
    "Branch Manager",
    "Business Development",
    "Client/Owner",
    "Design Team / Consultants",
    "Equipment Operators",
    "Estimator",
    "Foreman",
    "General Superintendent",
    "IT/Communications",
    "Legal Counsel",
    "Prefab Lead",
    "Project Coordinator",
    "Project Manager",
    "Purchasing",
    "Quality Inspector",
    "Regulatory Authorities",
    "Safety Coordinator",
    "Scheduler",
    "Security Personnel",
    "Site Administrator",
    "Subcontractors"
)

# Connect
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue -ErrorAction Stop
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected.`n" -ForegroundColor Green

# ============================================
# STEP 1: Update column choice lists
# ============================================
Write-Host "--- STEP 1: Updating column choice lists ---`n" -ForegroundColor Yellow

$spFields = Get-PnPField -List $LibraryName

# Map column titles to their objects
$columnMap = @{
    "(RACI) Responsible" = @{ Choices = $SingleChoices }
    "(RACI) Accountable" = @{ Choices = $SingleChoices }
    "(RACI) Consulted"   = @{ Choices = $MultiChoices }
    "(RACI) Informed"    = @{ Choices = $MultiChoices }
    "Roles (RACI)"       = @{ Choices = $MultiChoices }
}

$ctx = Get-PnPContext

foreach ($colTitle in $columnMap.Keys) {
    $field = $spFields | Where-Object { $_.Title -eq $colTitle } | Select-Object -First 1
    if (-not $field) {
        Write-Host "  NOT FOUND: $colTitle" -ForegroundColor Red
        continue
    }

    $newChoices = $columnMap[$colTitle].Choices

    # Load the field with choices
    $ctx.Load($field)
    $ctx.ExecuteQuery()

    # Clear and set choices
    $field.Choices.Clear()
    foreach ($choice in $newChoices) {
        $field.Choices.Add($choice)
    }
    $field.UpdateAndPushChanges($true)
    $ctx.ExecuteQuery()

    Write-Host "  OK: '$colTitle' -> $($newChoices.Count) choices" -ForegroundColor Green
}

Write-Host ""

# ============================================
# STEP 2: Get field internal names
# ============================================
# Refresh fields after update
$spFields = Get-PnPField -List $LibraryName
$rField = ($spFields | Where-Object { $_.Title -eq "(RACI) Responsible" } | Select-Object -First 1).InternalName
$aField = ($spFields | Where-Object { $_.Title -eq "(RACI) Accountable" } | Select-Object -First 1).InternalName
$cField = ($spFields | Where-Object { $_.Title -eq "(RACI) Consulted" } | Select-Object -First 1).InternalName
$iField = ($spFields | Where-Object { $_.Title -eq "(RACI) Informed" } | Select-Object -First 1).InternalName
$rolesField = ($spFields | Where-Object { $_.Title -eq "Roles (RACI)" } | Select-Object -First 1).InternalName

Write-Host "Field internal names:" -ForegroundColor Gray
Write-Host "  R     = $rField" -ForegroundColor Gray
Write-Host "  A     = $aField" -ForegroundColor Gray
Write-Host "  C     = $cField" -ForegroundColor Gray
Write-Host "  I     = $iField" -ForegroundColor Gray
Write-Host "  Roles = $rolesField`n" -ForegroundColor Gray

# ============================================
# STEP 3: Load CSV and build lookup
# ============================================
Write-Host "--- STEP 2: Loading CSV data ---`n" -ForegroundColor Yellow

$csvData = Import-Csv -Path $CsvPath -Encoding UTF8
$lookup = @{}
foreach ($row in $csvData) {
    $sopId = $row.SOPID.Trim()
    if ($sopId) { $lookup[$sopId] = $row }
}
Write-Host "  Loaded $($lookup.Count) SOPs from CSV`n" -ForegroundColor Gray

# ============================================
# STEP 4: Update all items
# ============================================
Write-Host "--- STEP 3: Updating all SharePoint items ---`n" -ForegroundColor Yellow

$items = Get-PnPListItem -List $LibraryName -PageSize 500
Write-Host "  Found $($items.Count) items`n" -ForegroundColor Gray

$updated = 0
$skipped = 0
$noData = 0
$errors = 0

foreach ($item in $items) {
    $sopId = $item.FieldValues["SOPID"]
    $fileName = $item.FieldValues["FileLeafRef"]

    if (-not $sopId) {
        if ($fileName -match '^(\d+\.\d+\.\d+)') {
            $sopId = $Matches[1]
        }
    }

    if (-not $sopId) {
        $skipped++
        continue
    }
    $sopId = $sopId.Trim()

    if (-not $lookup.ContainsKey($sopId)) {
        $noData++
        Write-Host "  NO DATA: $sopId ($fileName)" -ForegroundColor DarkGray
        continue
    }

    $row = $lookup[$sopId]
    $values = @{}

    # Responsible (single)
    $rVal = $row.RACI_Responsible.Trim()
    if ($rVal) { $values[$rField] = $rVal }

    # Accountable (single)
    $aVal = $row.RACI_Accountable.Trim()
    if ($aVal) { $values[$aField] = $aVal }

    # Consulted (multi)
    $cVal = $row.RACI_Consulted.Trim()
    if ($cVal) {
        $values[$cField] = @($cVal -split ";" | ForEach-Object { $_.Trim() } | Where-Object { $_ })
    }

    # Informed (multi)
    $iVal = $row.RACI_Informed.Trim()
    if ($iVal) {
        $values[$iField] = @($iVal -split ";" | ForEach-Object { $_.Trim() } | Where-Object { $_ })
    }

    # Roles (RACI) - union of all roles (multi)
    $rolesVal = $row.Roles_RACI.Trim()
    if ($rolesVal) {
        $values[$rolesField] = @($rolesVal -split ";" | ForEach-Object { $_.Trim() } | Where-Object { $_ })
    }

    if ($values.Count -eq 0) {
        $skipped++
        continue
    }

    try {
        Set-PnPListItem -List $LibraryName -Identity $item.Id -Values $values | Out-Null
        $updated++
        Write-Host "  OK: $sopId | R=$rVal | A=$aVal" -ForegroundColor Green
    } catch {
        $errors++
        Write-Host "  ERROR: $sopId | $($_.Exception.Message)" -ForegroundColor Red
    }
}

# ============================================
# SUMMARY
# ============================================
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  COMPLETE RACI REWRITE DONE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Updated:   $updated items" -ForegroundColor Green
Write-Host "  Skipped:   $skipped items (no SOP ID)" -ForegroundColor Yellow
Write-Host "  No data:   $noData items (not in CSV)" -ForegroundColor DarkGray
Write-Host "  Errors:    $errors items" -ForegroundColor $(if ($errors -eq 0) { "Green" } else { "Red" })
Write-Host ""

Disconnect-PnPOnline
Write-Host "Disconnected.`n" -ForegroundColor Gray
