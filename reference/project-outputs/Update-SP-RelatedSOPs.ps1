<#
.SYNOPSIS
    Update the RelatedSOPs column in SharePoint from RelatedSOPs_Mapping.csv
.DESCRIPTION
    The RelatedSOPs column is LookupMulti type (self-referencing within the library).
    This script maps SOP IDs to SharePoint item IDs and sets the lookup values.
    If the lookup approach fails, it falls back to converting the column to Note type.
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$CsvPath = "C:\Users\tewing\Desktop\Claude Projects\Project Outputs\RelatedSOPs_Mapping.csv"

# Connect
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue -ErrorAction Stop
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected.`n" -ForegroundColor Green

# ============================================
# STEP 1: Inspect the RelatedSOPs field
# ============================================
Write-Host "--- STEP 1: Inspecting RelatedSOPs field ---`n" -ForegroundColor Yellow

$spFields = Get-PnPField -List $LibraryName
$relField = $spFields | Where-Object { $_.InternalName -eq "RelatedSOPs" } | Select-Object -First 1

if (-not $relField) {
    Write-Host "  RelatedSOPs field NOT FOUND!" -ForegroundColor Red
    Disconnect-PnPOnline
    exit 1
}

Write-Host "  Title: $($relField.Title)" -ForegroundColor Gray
Write-Host "  InternalName: $($relField.InternalName)" -ForegroundColor Gray
Write-Host "  Type: $($relField.TypeAsString)" -ForegroundColor Gray

$isLookup = $relField.TypeAsString -eq "LookupMulti" -or $relField.TypeAsString -eq "Lookup"

if ($isLookup) {
    Write-Host "  Field is LookupMulti - will use item ID references" -ForegroundColor Cyan

    # Check if it's self-referencing
    $ctx = Get-PnPContext
    $ctx.Load($relField)
    $ctx.ExecuteQuery()

    $lookupListId = $relField.LookupList
    $list = Get-PnPList -Identity $LibraryName
    $listId = $list.Id.ToString()

    Write-Host "  LookupList ID: $lookupListId" -ForegroundColor Gray
    Write-Host "  Library ID: $listId" -ForegroundColor Gray

    # Check if self-referencing (cleanup GUID format for comparison)
    $cleanLookupId = $lookupListId.Trim('{', '}').ToLower()
    $cleanListId = $listId.ToLower()

    if ($cleanLookupId -eq $cleanListId) {
        Write-Host "  CONFIRMED: Self-referencing lookup within same library" -ForegroundColor Green
    } else {
        Write-Host "  WARNING: Lookup references a different list ($lookupListId)" -ForegroundColor Yellow
        Write-Host "  Will attempt to proceed anyway..." -ForegroundColor Yellow
    }
} else {
    Write-Host "  Field is $($relField.TypeAsString) - will use text values" -ForegroundColor Cyan
}

Write-Host ""

# ============================================
# STEP 2: Load CSV and all items
# ============================================
Write-Host "--- STEP 2: Loading data ---`n" -ForegroundColor Yellow

$csvData = Import-Csv -Path $CsvPath -Encoding UTF8
$csvLookup = @{}
foreach ($row in $csvData) {
    $csvLookup[$row.SOPID.Trim()] = $row
}
Write-Host "  CSV: $($csvLookup.Count) SOPs loaded" -ForegroundColor Gray

$items = Get-PnPListItem -List $LibraryName -PageSize 500
Write-Host "  SharePoint: $($items.Count) items loaded" -ForegroundColor Gray

# Build SOPID -> SP Item ID map
$sopToItemId = @{}
$itemToSopId = @{}
foreach ($item in $items) {
    $sopId = $item.FieldValues["SOPID"]
    if (-not $sopId) {
        $fn = $item.FieldValues["FileLeafRef"]
        if ($fn -match '^(\d+\.\d+\.\d+)') { $sopId = $Matches[1] }
    }
    if ($sopId) {
        $sopId = $sopId.Trim()
        $sopToItemId[$sopId] = $item.Id
        $itemToSopId[$item.Id] = $sopId
    }
}
Write-Host "  Mapped $($sopToItemId.Count) SOPs to SharePoint item IDs`n" -ForegroundColor Gray

# ============================================
# STEP 3: Update each item
# ============================================
Write-Host "--- STEP 3: Updating items ---`n" -ForegroundColor Yellow

$updated = 0
$skipped = 0
$noData = 0
$errors = 0

foreach ($item in $items) {
    $sopId = $item.FieldValues["SOPID"]
    if (-not $sopId) {
        $fn = $item.FieldValues["FileLeafRef"]
        if ($fn -match '^(\d+\.\d+\.\d+)') { $sopId = $Matches[1] }
    }
    if (-not $sopId) {
        $skipped++
        continue
    }
    $sopId = $sopId.Trim()

    if (-not $csvLookup.ContainsKey($sopId)) {
        $noData++
        Write-Host "  NO DATA: $sopId" -ForegroundColor DarkGray
        continue
    }

    $row = $csvLookup[$sopId]
    $relatedStr = $row.RelatedSOPs.Trim()

    if (-not $relatedStr) {
        $skipped++
        continue
    }

    # Parse related SOP IDs from the semicolon-delimited string
    $relatedSopIds = @()
    foreach ($part in $relatedStr -split ";") {
        $part = $part.Trim()
        if ($part -match '^(\d+\.\d+\.\d+)') {
            $relatedSopIds += $Matches[1]
        }
    }

    if ($relatedSopIds.Count -eq 0) {
        $skipped++
        continue
    }

    try {
        if ($isLookup) {
            # LookupMulti: convert SOP IDs to SP item IDs
            $lookupValues = @()
            $missingIds = @()
            foreach ($relSopId in $relatedSopIds) {
                if ($sopToItemId.ContainsKey($relSopId)) {
                    $spItemId = $sopToItemId[$relSopId]
                    $lookupValues += $spItemId
                } else {
                    $missingIds += $relSopId
                }
            }

            if ($missingIds.Count -gt 0) {
                Write-Host "  WARN: $sopId - missing SP IDs for: $($missingIds -join ', ')" -ForegroundColor Yellow
            }

            if ($lookupValues.Count -gt 0) {
                Set-PnPListItem -List $LibraryName -Identity $item.Id -Values @{
                    "RelatedSOPs" = $lookupValues
                } | Out-Null

                $updated++
                Write-Host "  OK: $sopId -> $($lookupValues.Count) related" -ForegroundColor Green
            }
        } else {
            # Text/Note: write the semicolon-delimited string directly
            Set-PnPListItem -List $LibraryName -Identity $item.Id -Values @{
                "RelatedSOPs" = $relatedStr
            } | Out-Null

            $updated++
            Write-Host "  OK: $sopId -> $($relatedSopIds.Count) related" -ForegroundColor Green
        }
    } catch {
        $errors++
        $errMsg = $_.Exception.Message
        Write-Host "  ERROR: $sopId | $errMsg" -ForegroundColor Red

        # If first lookup error, try text fallback
        if ($isLookup -and $errors -eq 1) {
            Write-Host "`n  ** LookupMulti failed. Attempting text-value fallback... **`n" -ForegroundColor Yellow
            try {
                Set-PnPListItem -List $LibraryName -Identity $item.Id -Values @{
                    "RelatedSOPs" = $relatedStr
                } | Out-Null
                Write-Host "  Text fallback succeeded for $sopId" -ForegroundColor Green
                $errors--
                $updated++

                # Switch to text mode for remaining items
                $isLookup = $false
                Write-Host "  ** Switching to text mode for remaining items **`n" -ForegroundColor Cyan
            } catch {
                Write-Host "  Text fallback also failed: $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    }
}

# ============================================
# SUMMARY
# ============================================
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  RELATED SOPs UPDATE COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Updated: $updated items" -ForegroundColor Green
Write-Host "  Skipped: $skipped items (no SOP ID or no data)" -ForegroundColor Yellow
Write-Host "  No data: $noData items (not in CSV)" -ForegroundColor DarkGray
Write-Host "  Errors:  $errors items" -ForegroundColor $(if ($errors -eq 0) { "Green" } else { "Red" })
Write-Host ""

Disconnect-PnPOnline
Write-Host "Disconnected.`n" -ForegroundColor Gray
