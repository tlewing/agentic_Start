<#
.SYNOPSIS
    Fix RACI column choice lists - delete and recreate with correct choices
.DESCRIPTION
    Since CSOM Choices.Clear() appended instead of replacing, this script
    removes each RACI column and recreates it with the correct canonical choices.
    Item data is preserved by reading values first, deleting the column,
    recreating it, then writing values back.
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

# Canonical choice lists
$SingleChoices = @(
    "Accounting",
    "Asst. Project Manager",
    "Branch Manager",
    "Business Development",
    "Chief Estimator",
    "Estimator",
    "Foreman",
    "General Superintendent",
    "Lead Estimator",
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

$MultiChoices = @(
    "Accounting",
    "All Employees",
    "Asst. Project Manager",
    "Branch Manager",
    "Business Development",
    "Chief Estimator",
    "Client/Owner",
    "Design Team / Consultants",
    "Equipment Operators",
    "Estimator",
    "Foreman",
    "General Superintendent",
    "IT/Communications",
    "Lead Estimator",
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

# Column definitions: Title, Type, Choices
$Columns = @(
    @{ Title = "(RACI) Responsible"; InternalName = "RACI_Responsible"; Type = "Choice";      Choices = $SingleChoices },
    @{ Title = "(RACI) Accountable"; InternalName = "RACI_Accountable"; Type = "Choice";      Choices = $SingleChoices },
    @{ Title = "(RACI) Consulted";   InternalName = "RACI_Consulted";   Type = "MultiChoice";  Choices = $MultiChoices },
    @{ Title = "(RACI) Informed";    InternalName = "RACI_Informed";    Type = "MultiChoice";  Choices = $MultiChoices },
    @{ Title = "Roles (RACI)";       InternalName = "Roles_RACI";       Type = "MultiChoice";  Choices = $MultiChoices }
)

# Connect
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue -ErrorAction Stop
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected.`n" -ForegroundColor Green

# ============================================
# STEP 1: Read all current values into memory
# ============================================
Write-Host "--- STEP 1: Reading all item values ---`n" -ForegroundColor Yellow

$spFields = Get-PnPField -List $LibraryName
$fieldMap = @{}
foreach ($col in $Columns) {
    $match = $spFields | Where-Object { $_.Title -eq $col.Title } | Select-Object -First 1
    if ($match) {
        $fieldMap[$col.Title] = $match.InternalName
        Write-Host "  Found: '$($col.Title)' -> $($match.InternalName)" -ForegroundColor Gray
    } else {
        Write-Host "  NOT FOUND: '$($col.Title)'" -ForegroundColor Red
        $fieldMap[$col.Title] = $null
    }
}

$items = Get-PnPListItem -List $LibraryName -PageSize 500
Write-Host "`n  Loaded $($items.Count) items" -ForegroundColor Gray

# Store all values: { itemId: { columnTitle: value } }
$savedData = @{}
foreach ($item in $items) {
    $itemValues = @{}
    foreach ($col in $Columns) {
        $intName = $fieldMap[$col.Title]
        if ($intName) {
            $val = $item.FieldValues[$intName]
            if ($val) {
                # Convert multi-choice to array
                if ($col.Type -eq "MultiChoice") {
                    $itemValues[$col.Title] = @($val | ForEach-Object { $_ })
                } else {
                    $itemValues[$col.Title] = $val
                }
            }
        }
    }
    $savedData[$item.Id] = $itemValues
}

$itemsWithData = ($savedData.Values | Where-Object { $_.Count -gt 0 }).Count
Write-Host "  Saved values from $itemsWithData items`n" -ForegroundColor Gray

# ============================================
# STEP 2: Delete old columns
# ============================================
Write-Host "--- STEP 2: Deleting old columns ---`n" -ForegroundColor Yellow

foreach ($col in $Columns) {
    $intName = $fieldMap[$col.Title]
    if (-not $intName) {
        Write-Host "  SKIP (not found): '$($col.Title)'" -ForegroundColor DarkGray
        continue
    }

    try {
        Remove-PnPField -List $LibraryName -Identity $intName -Force
        Write-Host "  DELETED: '$($col.Title)' ($intName)" -ForegroundColor Green
    } catch {
        Write-Host "  ERROR deleting '$($col.Title)': $($_.Exception.Message)" -ForegroundColor Red
    }
}

Start-Sleep -Seconds 3
Write-Host ""

# ============================================
# STEP 3: Recreate columns with correct choices
# ============================================
Write-Host "--- STEP 3: Creating columns with correct choices ---`n" -ForegroundColor Yellow

foreach ($col in $Columns) {
    $choicesXml = ""
    foreach ($choice in $col.Choices) {
        $escapedChoice = $choice.Replace("&", "&amp;").Replace("/", "/")
        $choicesXml += "<CHOICE>$escapedChoice</CHOICE>"
    }

    if ($col.Type -eq "Choice") {
        $fieldXml = "<Field Type='Choice' DisplayName='$($col.Title)' " +
                    "Name='$($col.InternalName)' Format='Dropdown' FillInChoice='FALSE'>" +
                    "<CHOICES>$choicesXml</CHOICES></Field>"
    } else {
        $fieldXml = "<Field Type='MultiChoice' DisplayName='$($col.Title)' " +
                    "Name='$($col.InternalName)' FillInChoice='FALSE'>" +
                    "<CHOICES>$choicesXml</CHOICES></Field>"
    }

    try {
        Add-PnPFieldFromXml -List $LibraryName -FieldXml $fieldXml
        Write-Host "  CREATED: '$($col.Title)' ($($col.Type), $($col.Choices.Count) choices)" -ForegroundColor Green
    } catch {
        Write-Host "  ERROR creating '$($col.Title)': $($_.Exception.Message)" -ForegroundColor Red
    }
}

Start-Sleep -Seconds 2

# Get new internal names
$spFields = Get-PnPField -List $LibraryName
$newFieldMap = @{}
foreach ($col in $Columns) {
    $match = $spFields | Where-Object { $_.Title -eq $col.Title } | Select-Object -First 1
    if ($match) {
        $newFieldMap[$col.Title] = $match.InternalName
        Write-Host "  Mapped: '$($col.Title)' -> $($match.InternalName)" -ForegroundColor Gray
    }
}

Write-Host ""

# ============================================
# STEP 4: Restore all values
# ============================================
Write-Host "--- STEP 4: Restoring item values ---`n" -ForegroundColor Yellow

# Re-fetch items to get current IDs
$items = Get-PnPListItem -List $LibraryName -PageSize 500

$restored = 0
$skipped = 0

foreach ($item in $items) {
    $itemId = $item.Id

    if (-not $savedData.ContainsKey($itemId)) {
        $skipped++
        continue
    }

    $itemValues = $savedData[$itemId]
    if ($itemValues.Count -eq 0) {
        $skipped++
        continue
    }

    $updateValues = @{}
    foreach ($col in $Columns) {
        $newIntName = $newFieldMap[$col.Title]
        if (-not $newIntName) { continue }

        $val = $itemValues[$col.Title]
        if (-not $val) { continue }

        if ($col.Type -eq "MultiChoice") {
            $updateValues[$newIntName] = @($val)
        } else {
            $updateValues[$newIntName] = $val
        }
    }

    if ($updateValues.Count -eq 0) {
        $skipped++
        continue
    }

    try {
        Set-PnPListItem -List $LibraryName -Identity $itemId -Values $updateValues | Out-Null
        $restored++

        $sopId = $item.FieldValues["SOPID"]
        if (-not $sopId) {
            $fn = $item.FieldValues["FileLeafRef"]
            if ($fn -match '^(\d+\.\d+\.\d+)') { $sopId = $Matches[1] }
        }
        Write-Host "  OK: $sopId" -ForegroundColor Green
    } catch {
        $sopId = $item.FieldValues["SOPID"]
        Write-Host "  ERROR: $sopId | $($_.Exception.Message)" -ForegroundColor Red
    }
}

# ============================================
# VERIFY
# ============================================
Write-Host "`n--- Verifying choice lists ---`n" -ForegroundColor Yellow

$spFields = Get-PnPField -List $LibraryName
foreach ($col in $Columns) {
    $match = $spFields | Where-Object { $_.Title -eq $col.Title } | Select-Object -First 1
    if ($match -and $match.Choices) {
        $choiceCount = $match.Choices.Count
        $color = if ($choiceCount -eq $col.Choices.Count) { "Green" } else { "Yellow" }
        Write-Host "  '$($col.Title)': $choiceCount choices (expected $($col.Choices.Count))" -ForegroundColor $color
    }
}

# ============================================
# SUMMARY
# ============================================
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  CHOICE LIST FIX COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Items restored: $restored" -ForegroundColor Green
Write-Host "  Items skipped:  $skipped" -ForegroundColor Yellow
Write-Host ""

Disconnect-PnPOnline
Write-Host "Disconnected.`n" -ForegroundColor Gray
