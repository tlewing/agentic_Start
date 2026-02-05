<#
.SYNOPSIS
    Full RACI Audit - Export all SharePoint SOP data for analysis
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$OutputCsv = "C:\Users\tewing\Desktop\Claude Projects\Project Outputs\SP_RACI_Audit.csv"

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue -ErrorAction Stop
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected.`n" -ForegroundColor Green

# Get field internal names
$spFields = Get-PnPField -List $LibraryName
$rField = ($spFields | Where-Object { $_.Title -eq "(RACI) Responsible" } | Select-Object -First 1).InternalName
$aField = ($spFields | Where-Object { $_.Title -eq "(RACI) Accountable" } | Select-Object -First 1).InternalName
$cField = ($spFields | Where-Object { $_.Title -eq "(RACI) Consulted" } | Select-Object -First 1).InternalName
$iField = ($spFields | Where-Object { $_.Title -eq "(RACI) Informed" } | Select-Object -First 1).InternalName
$rolesField = ($spFields | Where-Object { $_.Title -eq "Roles (RACI)" } | Select-Object -First 1).InternalName

Write-Host "Field mappings:" -ForegroundColor Gray
Write-Host "  Roles (RACI) = $rolesField" -ForegroundColor Gray
Write-Host "  R = $rField" -ForegroundColor Gray
Write-Host "  A = $aField" -ForegroundColor Gray
Write-Host "  C = $cField" -ForegroundColor Gray
Write-Host "  I = $iField`n" -ForegroundColor Gray

# Also get choice values for each RACI column
foreach ($col in @("(RACI) Responsible", "(RACI) Accountable", "(RACI) Consulted", "(RACI) Informed", "Roles (RACI)")) {
    $field = $spFields | Where-Object { $_.Title -eq $col } | Select-Object -First 1
    if ($field -and $field.Choices) {
        Write-Host "  $col choices: $($field.Choices -join ', ')" -ForegroundColor DarkGray
    }
}

Write-Host ""

# Get all items
$items = Get-PnPListItem -List $LibraryName -PageSize 500
Write-Host "Loaded $($items.Count) items.`n" -ForegroundColor Gray

# Export to CSV
$results = @()
foreach ($item in $items) {
    $sopId = $item.FieldValues["SOPID"]
    $title = $item.FieldValues["Title"]
    $fileName = $item.FieldValues["FileLeafRef"]
    $status = $item.FieldValues["Status"]
    $dept = $item.FieldValues["Department_x002f_Division"]

    if (-not $sopId) {
        if ($fileName -match '^(\d+\.\d+\.\d+)') { $sopId = $Matches[1] }
    }

    # Get RACI values
    $rolesVal = $item.FieldValues[$rolesField]
    $rVal = $item.FieldValues[$rField]
    $aVal = $item.FieldValues[$aField]
    $cVal = $item.FieldValues[$cField]
    $iVal = $item.FieldValues[$iField]

    # Format multi-choice as semicolon-separated
    $rolesStr = if ($rolesVal) { ($rolesVal | ForEach-Object { $_ }) -join "; " } else { "" }
    $cStr = if ($cVal) { ($cVal | ForEach-Object { $_ }) -join "; " } else { "" }
    $iStr = if ($iVal) { ($iVal | ForEach-Object { $_ }) -join "; " } else { "" }

    $results += [PSCustomObject]@{
        SOPID          = $sopId
        Title          = $title
        FileName       = $fileName
        Status         = $status
        Department     = $dept
        Roles_RACI     = $rolesStr
        RACI_R         = $rVal
        RACI_A         = $aVal
        RACI_C         = $cStr
        RACI_I         = $iStr
    }
}

$results | Export-Csv -Path $OutputCsv -NoTypeInformation -Encoding UTF8
Write-Host "Exported $($results.Count) items to: $OutputCsv" -ForegroundColor Green

Disconnect-PnPOnline
Write-Host "Disconnected.`n" -ForegroundColor Gray
