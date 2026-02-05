<#
.SYNOPSIS
    Fix 5 missing RACI SOPs + rename Field Supervisor to Foreman across all items
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

# RACI assignments for the 5 missing SOPs (already using Foreman, not Field Supervisor)
$MissingSOPs = @{
    "9.4.045" = @{
        R = "Project Manager"
        A = "Project Manager"
        C = @("Estimator", "General Superintendent", "Prefab Lead")
        I = @()
    }
    "9.4.055" = @{
        R = "Purchasing"
        A = "Project Manager"
        C = @("General Superintendent")
        I = @("Foreman")
    }
    "9.4.576" = @{
        R = "Project Manager"
        A = "Project Manager"
        C = @("General Superintendent")
        I = @()
    }
    "9.6.015" = @{
        R = "Project Manager"
        A = "Project Manager"
        C = @("General Superintendent", "Site Administrator")
        I = @()
    }
    "9.6.035" = @{
        R = "Project Manager"
        A = "Project Manager"
        C = @("Purchasing")
        I = @()
    }
}

# Connect
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue -ErrorAction Stop
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected.`n" -ForegroundColor Green

# Get field internal names - use Select-Object -First 1 to avoid array issue
$spFields = Get-PnPField -List $LibraryName
$rField = ($spFields | Where-Object { $_.Title -eq "(RACI) Responsible" } | Select-Object -First 1).InternalName
$aField = ($spFields | Where-Object { $_.Title -eq "(RACI) Accountable" } | Select-Object -First 1).InternalName
$cField = ($spFields | Where-Object { $_.Title -eq "(RACI) Consulted" } | Select-Object -First 1).InternalName
$iField = ($spFields | Where-Object { $_.Title -eq "(RACI) Informed" } | Select-Object -First 1).InternalName

Write-Host "Field mappings:" -ForegroundColor Gray
Write-Host "  R = $rField" -ForegroundColor Gray
Write-Host "  A = $aField" -ForegroundColor Gray
Write-Host "  C = $cField" -ForegroundColor Gray
Write-Host "  I = $iField`n" -ForegroundColor Gray

if (-not $rField -or -not $aField -or -not $cField -or -not $iField) {
    Write-Host "ERROR: One or more RACI columns not found. Aborting." -ForegroundColor Red
    Disconnect-PnPOnline
    exit 1
}

# Get all items
$items = Get-PnPListItem -List $LibraryName -PageSize 500
Write-Host "Loaded $($items.Count) items from library.`n" -ForegroundColor Gray

# ============================================
# PART 1: Fix 5 missing SOPs
# ============================================
Write-Host "--- PART 1: Fixing 5 missing SOPs ---`n" -ForegroundColor Yellow

$fixCount = 0
foreach ($item in $items) {
    $sopId = $item.FieldValues["SOPID"]
    if (-not $sopId) {
        $fn = $item.FieldValues["FileLeafRef"]
        if ($fn -match '^(\d+\.\d+\.\d+)') { $sopId = $Matches[1] }
    }
    if (-not $sopId) { continue }
    $sopId = $sopId.Trim()

    if (-not $MissingSOPs.ContainsKey($sopId)) { continue }

    $raci = $MissingSOPs[$sopId]
    $values = @{}

    if ($raci.R) { $values[$rField] = $raci.R }
    if ($raci.A) { $values[$aField] = $raci.A }
    if ($raci.C -and $raci.C.Count -gt 0) { $values[$cField] = $raci.C }
    if ($raci.I -and $raci.I.Count -gt 0) { $values[$iField] = $raci.I }

    try {
        Set-PnPListItem -List $LibraryName -Identity $item.Id -Values $values | Out-Null
        $fixCount++
        Write-Host "  OK: $sopId | R=$($raci.R) A=$($raci.A)" -ForegroundColor Green
    } catch {
        Write-Host "  ERROR: $sopId | $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n  Fixed $fixCount of $($MissingSOPs.Count) missing SOPs.`n" -ForegroundColor Cyan

# ============================================
# PART 2: Rename Field Supervisor -> Foreman
# ============================================
Write-Host "--- PART 2: Renaming 'Field Supervisor' to 'Foreman' ---`n" -ForegroundColor Yellow

$renameCount = 0
foreach ($item in $items) {
    $sopId = $item.FieldValues["SOPID"]
    if (-not $sopId) {
        $fn = $item.FieldValues["FileLeafRef"]
        if ($fn -match '^(\d+\.\d+\.\d+)') { $sopId = $Matches[1] }
    }

    $rVal = $item.FieldValues[$rField]
    $aVal = $item.FieldValues[$aField]

    # For multi-choice fields, value comes as a string collection
    $cVal = $item.FieldValues[$cField]
    $iVal = $item.FieldValues[$iField]

    $needsUpdate = $false
    $updates = @{}

    # Check Responsible (single choice)
    if ($rVal -eq "Field Supervisor") {
        $updates[$rField] = "Foreman"
        $needsUpdate = $true
    }

    # Check Accountable (single choice)
    if ($aVal -eq "Field Supervisor") {
        $updates[$aField] = "Foreman"
        $needsUpdate = $true
    }

    # Check Consulted (multi choice)
    if ($cVal) {
        $cList = @()
        $cChanged = $false
        foreach ($v in $cVal) {
            if ($v -eq "Field Supervisor") {
                $cList += "Foreman"
                $cChanged = $true
            } else {
                $cList += $v
            }
        }
        if ($cChanged) {
            # Deduplicate in case Foreman already exists
            $updates[$cField] = @($cList | Select-Object -Unique)
            $needsUpdate = $true
        }
    }

    # Check Informed (multi choice)
    if ($iVal) {
        $iList = @()
        $iChanged = $false
        foreach ($v in $iVal) {
            if ($v -eq "Field Supervisor") {
                $iList += "Foreman"
                $iChanged = $true
            } else {
                $iList += $v
            }
        }
        if ($iChanged) {
            $updates[$iField] = @($iList | Select-Object -Unique)
            $needsUpdate = $true
        }
    }

    if ($needsUpdate) {
        try {
            Set-PnPListItem -List $LibraryName -Identity $item.Id -Values $updates | Out-Null
            $renameCount++
            $changedFields = ($updates.Keys | ForEach-Object {
                $fieldName = $_
                if ($fieldName -eq $rField) { "R" }
                elseif ($fieldName -eq $aField) { "A" }
                elseif ($fieldName -eq $cField) { "C" }
                elseif ($fieldName -eq $iField) { "I" }
            }) -join ", "
            Write-Host "  RENAMED: $sopId | Fields: $changedFields" -ForegroundColor Green
        } catch {
            Write-Host "  ERROR: $sopId | $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

Write-Host "`n  Renamed Field Supervisor -> Foreman in $renameCount items.`n" -ForegroundColor Cyan

# ============================================
# SUMMARY
# ============================================
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Missing SOPs fixed:    $fixCount" -ForegroundColor Green
Write-Host "  Field Supervisor renamed: $renameCount" -ForegroundColor Green
Write-Host ""

Disconnect-PnPOnline
Write-Host "Disconnected.`n" -ForegroundColor Gray
