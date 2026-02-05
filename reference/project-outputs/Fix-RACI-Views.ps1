<#
.SYNOPSIS
    Check if RACI columns exist and add them to the default view
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue -ErrorAction Stop
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected.`n" -ForegroundColor Green

# ============================================
# STEP 1: Check if columns exist on the library
# ============================================
Write-Host "--- STEP 1: Checking if RACI columns exist ---`n" -ForegroundColor Yellow

$spFields = Get-PnPField -List $LibraryName
$raciTitles = @(
    "(RACI) Responsible",
    "(RACI) Accountable",
    "(RACI) Consulted",
    "(RACI) Informed",
    "Roles (RACI)"
)

$foundFields = @{}
foreach ($title in $raciTitles) {
    $field = $spFields | Where-Object { $_.Title -eq $title } | Select-Object -First 1
    if ($field) {
        $foundFields[$title] = $field.InternalName
        Write-Host "  EXISTS: '$title' -> $($field.InternalName) ($($field.TypeAsString))" -ForegroundColor Green
    } else {
        Write-Host "  MISSING: '$title'" -ForegroundColor Red
    }
}

Write-Host ""

# ============================================
# STEP 2: List all views and their fields
# ============================================
Write-Host "--- STEP 2: Checking views ---`n" -ForegroundColor Yellow

$ctx = Get-PnPContext
$list = Get-PnPList -Identity $LibraryName
$ctx.Load($list.Views)
$ctx.ExecuteQuery()

foreach ($view in $list.Views) {
    $ctx.Load($view)
    $ctx.Load($view.ViewFields)
    $ctx.ExecuteQuery()

    $viewFieldNames = @($view.ViewFields)
    $hasRaci = $false
    foreach ($title in $raciTitles) {
        $intName = $foundFields[$title]
        if ($intName -and $viewFieldNames -contains $intName) {
            $hasRaci = $true
            break
        }
    }

    $marker = if ($view.DefaultView) { " [DEFAULT]" } else { "" }
    $raciStatus = if ($hasRaci) { "(has RACI)" } else { "(no RACI)" }
    Write-Host "  View: '$($view.Title)'$marker $raciStatus" -ForegroundColor Gray

    if ($view.DefaultView) {
        Write-Host "    Current fields:" -ForegroundColor DarkGray
        foreach ($vf in $viewFieldNames) {
            Write-Host "      - $vf" -ForegroundColor DarkGray
        }
    }
}

Write-Host ""

# ============================================
# STEP 3: Add RACI columns to default view
# ============================================
Write-Host "--- STEP 3: Adding RACI columns to default view ---`n" -ForegroundColor Yellow

$defaultView = $list.Views | Where-Object { $_.DefaultView -eq $true } | Select-Object -First 1

if (-not $defaultView) {
    Write-Host "  No default view found! Listing all views:" -ForegroundColor Red
    foreach ($v in $list.Views) {
        Write-Host "    '$($v.Title)' DefaultView=$($v.DefaultView)" -ForegroundColor Yellow
    }
} else {
    $ctx.Load($defaultView.ViewFields)
    $ctx.ExecuteQuery()

    $currentViewFields = @($defaultView.ViewFields)

    foreach ($title in $raciTitles) {
        $intName = $foundFields[$title]
        if (-not $intName) {
            Write-Host "  SKIP: '$title' not found in library" -ForegroundColor Red
            continue
        }

        if ($currentViewFields -contains $intName) {
            Write-Host "  ALREADY IN VIEW: '$title' ($intName)" -ForegroundColor Gray
        } else {
            try {
                $defaultView.ViewFields.Add($intName)
                Write-Host "  ADDED TO VIEW: '$title' ($intName)" -ForegroundColor Green
            } catch {
                Write-Host "  ERROR adding '$title': $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    }

    $defaultView.Update()
    $ctx.ExecuteQuery()
    Write-Host "`n  Default view updated." -ForegroundColor Green
}

Write-Host ""

# ============================================
# STEP 4: Also add to "All Items" / "All Documents" view if different
# ============================================
Write-Host "--- STEP 4: Adding to All Documents view (if separate) ---`n" -ForegroundColor Yellow

$allDocsView = $list.Views | Where-Object { $_.Title -eq "All Documents" -and $_.DefaultView -ne $true } | Select-Object -First 1

if ($allDocsView) {
    $ctx.Load($allDocsView.ViewFields)
    $ctx.ExecuteQuery()

    $adFields = @($allDocsView.ViewFields)

    foreach ($title in $raciTitles) {
        $intName = $foundFields[$title]
        if (-not $intName) { continue }

        if ($adFields -contains $intName) {
            Write-Host "  ALREADY IN VIEW: '$title'" -ForegroundColor Gray
        } else {
            try {
                $allDocsView.ViewFields.Add($intName)
                Write-Host "  ADDED: '$title' ($intName)" -ForegroundColor Green
            } catch {
                Write-Host "  ERROR: $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    }

    $allDocsView.Update()
    $ctx.ExecuteQuery()
    Write-Host "  All Documents view updated." -ForegroundColor Green
} else {
    Write-Host "  No separate 'All Documents' view found (default view is All Documents)." -ForegroundColor Gray
}

# ============================================
# STEP 5: Verify item data still exists
# ============================================
Write-Host "`n--- STEP 5: Spot-checking item data ---`n" -ForegroundColor Yellow

$items = Get-PnPListItem -List $LibraryName -PageSize 10
$checked = 0
$hasData = 0

foreach ($item in $items) {
    $sopId = $item.FieldValues["SOPID"]
    if (-not $sopId) {
        $fn = $item.FieldValues["FileLeafRef"]
        if ($fn -match '^(\d+\.\d+\.\d+)') { $sopId = $Matches[1] }
    }
    if (-not $sopId) { continue }

    $rVal = $item.FieldValues[$foundFields["(RACI) Responsible"]]
    $aVal = $item.FieldValues[$foundFields["(RACI) Accountable"]]

    $checked++
    if ($rVal -or $aVal) {
        $hasData++
        Write-Host "  $sopId | R=$rVal | A=$aVal" -ForegroundColor Green
    } else {
        Write-Host "  $sopId | R=(empty) | A=(empty)" -ForegroundColor Yellow
    }

    if ($checked -ge 5) { break }
}

Write-Host "`n  $hasData of $checked spot-checked items have RACI data.`n" -ForegroundColor Gray

# ============================================
# SUMMARY
# ============================================
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VIEW FIX COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Columns found: $($foundFields.Count) of $($raciTitles.Count)" -ForegroundColor Green
Write-Host "  Columns added to view(s)" -ForegroundColor Green
Write-Host ""

Disconnect-PnPOnline
Write-Host "Disconnected.`n" -ForegroundColor Gray
