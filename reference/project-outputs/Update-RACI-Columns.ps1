<#
.SYNOPSIS
    Update RACI columns in SharePoint SOP Library

.DESCRIPTION
    Creates 4 RACI columns (if they don't exist) and populates them from CSV data:
      - (RACI) Responsible  (Single Choice)
      - (RACI) Accountable  (Single Choice)
      - (RACI) Consulted    (Multi Choice)
      - (RACI) Informed     (Multi Choice)

.PARAMETER Action
    CreateColumns - Create the 4 RACI columns in SharePoint
    Update        - Populate RACI values from CSV
    Full          - Create columns + Update (both steps)
    Audit         - Read current RACI values and report coverage

.EXAMPLE
    .\Update-RACI-Columns.ps1 -Action Full
    .\Update-RACI-Columns.ps1 -Action Audit
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("CreateColumns", "Update", "Full", "Audit")]
    [string]$Action
)

# ============================================
# CONFIGURATION
# ============================================
$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$CsvPath = "C:\Users\tewing\Desktop\Claude Projects\Project Outputs\RACI_SharePoint_Update.csv"

# ============================================
# COLUMN DEFINITIONS
# ============================================

# Choice values for each RACI column
$ResponsibleChoices = @(
    "Accounting",
    "Asst. Project Manager",
    "Business Development",
    "Field Supervisor",
    "Foreman",
    "General Superintendent",
    "Prefab Lead",
    "Project Manager",
    "Purchasing",
    "Quality Inspector",
    "Safety Coordinator",
    "Site Administrator",
    "Subcontractors"
)

$AccountableChoices = @(
    "Branch Manager",
    "Project Manager"
)

$ConsultedChoices = @(
    "Asst. Project Manager",
    "Branch Manager",
    "Client/Owner",
    "Estimator",
    "Field Supervisor",
    "Foreman",
    "General Superintendent",
    "Legal Counsel",
    "Prefab Lead",
    "Project Manager",
    "Purchasing",
    "Quality Inspector",
    "Safety Coordinator",
    "Site Administrator"
)

$InformedChoices = @(
    "Accounting",
    "All Employees",
    "Asst. Project Manager",
    "Branch Manager",
    "Crew",
    "Design Team / Consultants",
    "Equipment Operators",
    "Foreman",
    "General Superintendent",
    "IT/Communications",
    "Prefab Lead",
    "Project Manager",
    "Quality Inspector",
    "Regulatory Authorities",
    "Safety Coordinator",
    "Security Personnel"
)

# Column specs: DisplayName, InternalName, Type, Choices
$RACIColumns = @(
    @{
        DisplayName  = "(RACI) Responsible"
        InternalName = "RACI_Responsible"
        Type         = "Choice"
        Choices      = $ResponsibleChoices
        CsvColumn    = "RACI_Responsible"
    },
    @{
        DisplayName  = "(RACI) Accountable"
        InternalName = "RACI_Accountable"
        Type         = "Choice"
        Choices      = $AccountableChoices
        CsvColumn    = "RACI_Accountable"
    },
    @{
        DisplayName  = "(RACI) Consulted"
        InternalName = "RACI_Consulted"
        Type         = "MultiChoice"
        Choices      = $ConsultedChoices
        CsvColumn    = "RACI_Consulted"
    },
    @{
        DisplayName  = "(RACI) Informed"
        InternalName = "RACI_Informed"
        Type         = "MultiChoice"
        Choices      = $InformedChoices
        CsvColumn    = "RACI_Informed"
    }
)

# ============================================
# FUNCTIONS
# ============================================

function Connect-ToSharePoint {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  RACI Column Updater - SharePoint" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
    Write-Host "A browser window will open for sign-in..." -ForegroundColor Yellow
    Write-Host ""

    $env:PNPLEGACYMESSAGE = 'false'
    Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue -ErrorAction Stop
    Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue

    Write-Host "Connected successfully!" -ForegroundColor Green
    Write-Host ""
}

function New-RACIColumns {
    Write-Host "`n--- Creating RACI Columns ---`n" -ForegroundColor Yellow

    # Get existing fields to check what already exists
    $existingFields = Get-PnPField -List $LibraryName | Select-Object -ExpandProperty InternalName

    foreach ($col in $RACIColumns) {
        if ($existingFields -contains $col.InternalName) {
            Write-Host "  SKIP: '$($col.DisplayName)' already exists (internal: $($col.InternalName))" -ForegroundColor Gray
            continue
        }

        Write-Host "  CREATING: '$($col.DisplayName)' ($($col.Type))..." -ForegroundColor Cyan

        # Build the choices XML
        $choicesXml = ""
        foreach ($choice in $col.Choices) {
            $choicesXml += "<CHOICE>$choice</CHOICE>"
        }

        if ($col.Type -eq "Choice") {
            $fieldXml = "<Field Type='Choice' DisplayName='$($col.DisplayName)' " +
                        "Name='$($col.InternalName)' Format='Dropdown' FillInChoice='FALSE'>" +
                        "<CHOICES>$choicesXml</CHOICES></Field>"
        } else {
            # MultiChoice
            $fieldXml = "<Field Type='MultiChoice' DisplayName='$($col.DisplayName)' " +
                        "Name='$($col.InternalName)' FillInChoice='FALSE'>" +
                        "<CHOICES>$choicesXml</CHOICES></Field>"
        }

        try {
            Add-PnPFieldFromXml -List $LibraryName -FieldXml $fieldXml
            Write-Host "  OK: Created '$($col.DisplayName)'" -ForegroundColor Green
        } catch {
            Write-Host "  ERROR: Failed to create '$($col.DisplayName)': $($_.Exception.Message)" -ForegroundColor Red
        }
    }

    Write-Host "`nColumn creation complete." -ForegroundColor Green
}

function Update-RACIValues {
    Write-Host "`n--- Updating RACI Values from CSV ---`n" -ForegroundColor Yellow

    # Verify CSV exists
    if (-not (Test-Path $CsvPath)) {
        Write-Host "ERROR: CSV not found at $CsvPath" -ForegroundColor Red
        return
    }

    # Load CSV
    $csvData = Import-Csv -Path $CsvPath -Encoding UTF8
    Write-Host "  Loaded $($csvData.Count) SOPs from CSV" -ForegroundColor Gray

    # Build lookup by SOP ID
    $raciLookup = @{}
    foreach ($row in $csvData) {
        $sopId = $row.SOPID.Trim()
        if ($sopId) {
            $raciLookup[$sopId] = $row
        }
    }
    Write-Host "  RACI data for $($raciLookup.Count) unique SOP IDs" -ForegroundColor Gray

    # Get all items from SharePoint library
    Write-Host "  Loading SharePoint library items..." -ForegroundColor Gray
    $items = Get-PnPListItem -List $LibraryName -PageSize 500 -Fields "SOPID","Title","FileLeafRef"

    Write-Host "  Found $($items.Count) items in library`n" -ForegroundColor Gray

    # Get actual internal names for RACI columns
    $spFields = Get-PnPField -List $LibraryName
    $fieldNameMap = @{}
    foreach ($col in $RACIColumns) {
        $match = $spFields | Where-Object {
            $_.InternalName -eq $col.InternalName -or $_.Title -eq $col.DisplayName
        } | Select-Object -First 1

        if ($match) {
            $fieldNameMap[$col.CsvColumn] = $match.InternalName
            Write-Host "  Mapped: $($col.DisplayName) -> $($match.InternalName)" -ForegroundColor Gray
        } else {
            Write-Host "  WARNING: Column '$($col.DisplayName)' not found in SharePoint!" -ForegroundColor Red
            Write-Host "  Run with -Action CreateColumns first." -ForegroundColor Yellow
            return
        }
    }

    Write-Host ""

    # Process each item
    $updated = 0
    $skipped = 0
    $notFound = 0

    foreach ($item in $items) {
        $sopId = $item.FieldValues["SOPID"]
        $title = $item.FieldValues["Title"]
        $fileName = $item.FieldValues["FileLeafRef"]

        if (-not $sopId) {
            # Try to extract SOP ID from title or filename
            if ($title -match '^(\d+\.\d+\.\d+)') {
                $sopId = $Matches[1]
            } elseif ($fileName -match '^(\d+\.\d+\.\d+)') {
                $sopId = $Matches[1]
            }
        }

        if (-not $sopId) {
            $skipped++
            continue
        }

        $sopId = $sopId.Trim()

        if (-not $raciLookup.ContainsKey($sopId)) {
            $notFound++
            Write-Host "  NO DATA: $sopId ($fileName)" -ForegroundColor DarkGray
            continue
        }

        $raciRow = $raciLookup[$sopId]

        # Build update values
        $updateValues = @{}

        # Responsible (single choice)
        $rVal = $raciRow.RACI_Responsible.Trim()
        if ($rVal) {
            $internalName = $fieldNameMap["RACI_Responsible"]
            $updateValues[$internalName] = $rVal
        }

        # Accountable (single choice)
        $aVal = $raciRow.RACI_Accountable.Trim()
        if ($aVal) {
            $internalName = $fieldNameMap["RACI_Accountable"]
            $updateValues[$internalName] = $aVal
        }

        # Consulted (multi choice - semicolon separated)
        $cVal = $raciRow.RACI_Consulted.Trim()
        if ($cVal) {
            $internalName = $fieldNameMap["RACI_Consulted"]
            $cArray = @($cVal -split ";" | ForEach-Object { $_.Trim() } | Where-Object { $_ })
            $updateValues[$internalName] = $cArray
        }

        # Informed (multi choice - semicolon separated)
        $iVal = $raciRow.RACI_Informed.Trim()
        if ($iVal) {
            $internalName = $fieldNameMap["RACI_Informed"]
            $iArray = @($iVal -split ";" | ForEach-Object { $_.Trim() } | Where-Object { $_ })
            $updateValues[$internalName] = $iArray
        }

        if ($updateValues.Count -eq 0) {
            $skipped++
            continue
        }

        # Apply update
        try {
            Set-PnPListItem -List $LibraryName -Identity $item.Id -Values $updateValues
            $updated++

            $rDisplay = if ($rVal) { "R=$rVal" } else { "" }
            $aDisplay = if ($aVal) { "A=$aVal" } else { "" }
            $parts = @($rDisplay, $aDisplay) | Where-Object { $_ }
            Write-Host "  OK: $sopId | $($parts -join ' | ')" -ForegroundColor Green
        } catch {
            Write-Host "  ERROR: $sopId | $($_.Exception.Message)" -ForegroundColor Red
        }
    }

    # Summary
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  UPDATE COMPLETE" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Updated:   $updated items" -ForegroundColor Green
    Write-Host "  Skipped:   $skipped items (no SOP ID or no values)" -ForegroundColor Yellow
    Write-Host "  No data:   $notFound items (SOP ID not in CSV)" -ForegroundColor DarkGray
    Write-Host ""
}

function Get-RACIAudit {
    Write-Host "`n--- RACI Coverage Audit ---`n" -ForegroundColor Yellow

    # Get all items
    $items = Get-PnPListItem -List $LibraryName -PageSize 500

    # Get field internal names
    $spFields = Get-PnPField -List $LibraryName
    $raciFields = @{}
    foreach ($col in $RACIColumns) {
        $match = $spFields | Where-Object {
            $_.InternalName -eq $col.InternalName -or $_.Title -eq $col.DisplayName
        } | Select-Object -First 1

        if ($match) {
            $raciFields[$col.DisplayName] = $match.InternalName
        } else {
            Write-Host "  Column '$($col.DisplayName)' NOT FOUND" -ForegroundColor Red
            $raciFields[$col.DisplayName] = $null
        }
    }

    $total = $items.Count
    $coverage = @{}
    foreach ($col in $RACIColumns) {
        $coverage[$col.DisplayName] = 0
    }

    $emptyAll = 0

    foreach ($item in $items) {
        $hasAny = $false

        foreach ($col in $RACIColumns) {
            $internalName = $raciFields[$col.DisplayName]
            if (-not $internalName) { continue }

            $val = $item.FieldValues[$internalName]
            if ($val -and $val.ToString().Trim()) {
                $coverage[$col.DisplayName]++
                $hasAny = $true
            }
        }

        if (-not $hasAny) {
            $emptyAll++
            $sopId = $item.FieldValues["SOPID"]
            $title = $item.FieldValues["Title"]
            if ($sopId) {
                Write-Host "  EMPTY: $sopId - $title" -ForegroundColor DarkGray
            }
        }
    }

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  RACI COVERAGE REPORT" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Total items: $total`n"

    foreach ($col in $RACIColumns) {
        $count = $coverage[$col.DisplayName]
        $pct = if ($total -gt 0) { [math]::Round(($count / $total) * 100) } else { 0 }
        $color = if ($pct -ge 80) { "Green" } elseif ($pct -ge 50) { "Yellow" } else { "Red" }
        Write-Host "  $($col.DisplayName): $count / $total ($pct%)" -ForegroundColor $color
    }

    Write-Host "`n  Items with NO RACI data: $emptyAll" -ForegroundColor $(if ($emptyAll -eq 0) { "Green" } else { "Yellow" })
    Write-Host ""
}

# ============================================
# MAIN
# ============================================

Connect-ToSharePoint

switch ($Action) {
    "CreateColumns" {
        New-RACIColumns
    }
    "Update" {
        Update-RACIValues
    }
    "Full" {
        New-RACIColumns
        Update-RACIValues
    }
    "Audit" {
        Get-RACIAudit
    }
}

Disconnect-PnPOnline
Write-Host "Disconnected from SharePoint.`n" -ForegroundColor Gray
