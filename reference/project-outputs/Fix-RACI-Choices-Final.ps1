<#
.SYNOPSIS
    Fix RACI column choices by replacing SchemaXml on existing fields
.DESCRIPTION
    Updates the 4 RACI columns to use canonical role names by modifying
    the field SchemaXml directly via CSOM. Also checks for and removes
    any orphaned duplicate columns with "0" suffix.
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

# Column definitions
$Columns = @(
    @{ Title = "(RACI) Responsible"; Type = "Choice";      Choices = $SingleChoices },
    @{ Title = "(RACI) Accountable"; Type = "Choice";      Choices = $SingleChoices },
    @{ Title = "(RACI) Consulted";   Type = "MultiChoice";  Choices = $MultiChoices },
    @{ Title = "(RACI) Informed";    Type = "MultiChoice";  Choices = $MultiChoices }
)

# Connect
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue -ErrorAction Stop
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected.`n" -ForegroundColor Green

# ============================================
# STEP 0: Check for orphaned "0" suffix columns
# ============================================
Write-Host "--- STEP 0: Checking for orphaned duplicate columns ---`n" -ForegroundColor Yellow

$allFields = Get-PnPField -List $LibraryName
$raciFields = $allFields | Where-Object { $_.InternalName -match "RACI" -or $_.Title -match "RACI" }

Write-Host "  All RACI-related fields:" -ForegroundColor Gray
foreach ($f in $raciFields) {
    Write-Host "    '$($f.Title)' | Internal: $($f.InternalName) | Type: $($f.TypeAsString)" -ForegroundColor Gray
}

# Remove any "0" suffix duplicates
$orphans = $raciFields | Where-Object { $_.InternalName -match "0$" -and $_.InternalName -match "RACI" }
if ($orphans.Count -gt 0) {
    Write-Host "`n  Found $($orphans.Count) orphaned columns:" -ForegroundColor Yellow
    foreach ($orphan in $orphans) {
        try {
            Remove-PnPField -List $LibraryName -Identity $orphan.InternalName -Force
            Write-Host "    DELETED orphan: '$($orphan.Title)' ($($orphan.InternalName))" -ForegroundColor Green
        } catch {
            Write-Host "    ERROR deleting orphan '$($orphan.Title)': $($_.Exception.Message)" -ForegroundColor Red
        }
    }
} else {
    Write-Host "`n  No orphaned columns found." -ForegroundColor Green
}

Write-Host ""

# ============================================
# STEP 1: Update SchemaXml on each column
# ============================================
Write-Host "--- STEP 1: Updating column choices via SchemaXml ---`n" -ForegroundColor Yellow

$ctx = Get-PnPContext
$list = Get-PnPList -Identity $LibraryName
$ctx.Load($list)
$ctx.Load($list.Fields)
$ctx.ExecuteQuery()

foreach ($col in $Columns) {
    $field = $list.Fields | Where-Object { $_.Title -eq $col.Title } | Select-Object -First 1
    if (-not $field) {
        Write-Host "  NOT FOUND: '$($col.Title)'" -ForegroundColor Red
        continue
    }

    Write-Host "  Processing: '$($col.Title)' ($($field.InternalName))" -ForegroundColor Gray

    # Parse current schema XML
    $schemaXml = $field.SchemaXml
    Write-Host "    Current schema length: $($schemaXml.Length)" -ForegroundColor DarkGray

    # Build new CHOICES XML
    $choicesXml = "<CHOICES>"
    foreach ($choice in $col.Choices) {
        $escaped = $choice.Replace("&", "&amp;")
        $choicesXml += "<CHOICE>$escaped</CHOICE>"
    }
    $choicesXml += "</CHOICES>"

    # Replace CHOICES block in schema using XML parsing
    $xml = [xml]$schemaXml
    $existingChoices = $xml.Field.SelectSingleNode("CHOICES")
    if ($existingChoices) {
        $xml.Field.RemoveChild($existingChoices) | Out-Null
    }

    # Add new CHOICES node
    $newChoicesNode = $xml.CreateDocumentFragment()
    $newChoicesNode.InnerXml = $choicesXml
    $xml.Field.AppendChild($newChoicesNode) | Out-Null

    $newSchema = $xml.OuterXml

    # Apply the updated schema
    $field.SchemaXml = $newSchema
    $field.UpdateAndPushChanges($true)

    try {
        $ctx.ExecuteQuery()
        Write-Host "    OK: Updated to $($col.Choices.Count) choices" -ForegroundColor Green
    } catch {
        Write-Host "    ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""

# ============================================
# STEP 2: Verify the changes
# ============================================
Write-Host "--- STEP 2: Verifying choices ---`n" -ForegroundColor Yellow

# Re-fetch fields
$spFields = Get-PnPField -List $LibraryName

$allGood = $true
foreach ($col in $Columns) {
    $field = $spFields | Where-Object { $_.Title -eq $col.Title } | Select-Object -First 1
    if ($field -and $field.Choices) {
        $actual = $field.Choices.Count
        $expected = $col.Choices.Count
        if ($actual -eq $expected) {
            Write-Host "  OK: '$($col.Title)' = $actual choices (expected $expected)" -ForegroundColor Green
        } else {
            Write-Host "  MISMATCH: '$($col.Title)' = $actual choices (expected $expected)" -ForegroundColor Red
            $allGood = $false
        }
    }
}

# Also check Roles (RACI)
$rolesField = $spFields | Where-Object { $_.Title -eq "Roles (RACI)" } | Select-Object -First 1
if ($rolesField -and $rolesField.Choices) {
    Write-Host "  OK: 'Roles (RACI)' = $($rolesField.Choices.Count) choices" -ForegroundColor Green
}

Write-Host ""

# ============================================
# STEP 3: Fix item values using old->new role name mapping
# ============================================
Write-Host "--- STEP 3: Fixing item values with legacy role names ---`n" -ForegroundColor Yellow

$RenameMap = @{
    "Assistant Project Manager" = "Asst. Project Manager"
    "Purchasing Manager"        = "Purchasing"
    "QC"                        = "Quality Inspector"
    "Safety Superintendent"     = "Safety Coordinator"
    "Prefab Superintendent"     = "Prefab Lead"
    "Engineer"                  = "Estimator"
    "Business Manager"          = "Branch Manager"
}

$spFields = Get-PnPField -List $LibraryName
$rField = ($spFields | Where-Object { $_.Title -eq "(RACI) Responsible" } | Select-Object -First 1).InternalName
$aField = ($spFields | Where-Object { $_.Title -eq "(RACI) Accountable" } | Select-Object -First 1).InternalName
$cField = ($spFields | Where-Object { $_.Title -eq "(RACI) Consulted" } | Select-Object -First 1).InternalName
$iField = ($spFields | Where-Object { $_.Title -eq "(RACI) Informed" } | Select-Object -First 1).InternalName

Write-Host "  Field names: R=$rField, A=$aField, C=$cField, I=$iField" -ForegroundColor Gray

$items = Get-PnPListItem -List $LibraryName -PageSize 500
Write-Host "  Loaded $($items.Count) items`n" -ForegroundColor Gray

$fixedItems = 0
$fixedValues = 0

foreach ($item in $items) {
    $sopId = $item.FieldValues["SOPID"]
    if (-not $sopId) {
        $fn = $item.FieldValues["FileLeafRef"]
        if ($fn -match '^(\d+\.\d+\.\d+)') { $sopId = $Matches[1] }
    }
    if (-not $sopId) { continue }

    $updateValues = @{}
    $changed = $false

    # Fix single-choice fields (R, A)
    foreach ($fieldName in @($rField, $aField)) {
        $val = $item.FieldValues[$fieldName]
        if ($val -and $RenameMap.ContainsKey($val)) {
            $updateValues[$fieldName] = $RenameMap[$val]
            $fixedValues++
            $changed = $true
        }
    }

    # Fix multi-choice fields (C, I)
    foreach ($fieldName in @($cField, $iField)) {
        $vals = $item.FieldValues[$fieldName]
        if ($vals) {
            $newVals = @()
            $fieldChanged = $false
            foreach ($v in $vals) {
                if ($RenameMap.ContainsKey($v)) {
                    $newVals += $RenameMap[$v]
                    $fieldChanged = $true
                    $fixedValues++
                } else {
                    $newVals += $v
                }
            }
            if ($fieldChanged) {
                $updateValues[$fieldName] = $newVals
                $changed = $true
            }
        }
    }

    if ($changed) {
        try {
            Set-PnPListItem -List $LibraryName -Identity $item.Id -Values $updateValues | Out-Null
            $fixedItems++
            Write-Host "  FIXED: $sopId" -ForegroundColor Green
        } catch {
            Write-Host "  ERROR: $sopId | $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# ============================================
# SUMMARY
# ============================================
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  RACI CHOICE FIX COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Items with renamed values: $fixedItems" -ForegroundColor Green
Write-Host "  Total values renamed:      $fixedValues" -ForegroundColor Green
if (-not $allGood) {
    Write-Host "  WARNING: Some column choice counts still mismatched!" -ForegroundColor Red
}
Write-Host ""

Disconnect-PnPOnline
Write-Host "Disconnected.`n" -ForegroundColor Gray
