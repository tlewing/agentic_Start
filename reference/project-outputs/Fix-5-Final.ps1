<#
.SYNOPSIS
    Fix 5 SOPs not in metadata - final pass with canonical names
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

$MissingSOPs = @{
    "9.4.045" = @{
        R = "Project Manager"
        A = "Project Manager"
        C = @("Estimator", "General Superintendent", "Prefab Lead")
        I = @()
        Roles = @("Estimator", "General Superintendent", "Prefab Lead", "Project Manager")
    }
    "9.4.055" = @{
        R = "Purchasing"
        A = "Project Manager"
        C = @("General Superintendent")
        I = @("Foreman")
        Roles = @("Foreman", "General Superintendent", "Project Manager", "Purchasing")
    }
    "9.4.576" = @{
        R = "Project Manager"
        A = "Project Manager"
        C = @("General Superintendent")
        I = @()
        Roles = @("General Superintendent", "Project Manager")
    }
    "9.6.015" = @{
        R = "Project Manager"
        A = "Project Manager"
        C = @("General Superintendent", "Site Administrator")
        I = @()
        Roles = @("General Superintendent", "Project Manager", "Site Administrator")
    }
    "9.6.035" = @{
        R = "Project Manager"
        A = "Project Manager"
        C = @("Purchasing")
        I = @()
        Roles = @("Project Manager", "Purchasing")
    }
}

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue -ErrorAction Stop
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected.`n" -ForegroundColor Green

$spFields = Get-PnPField -List $LibraryName
$rField = ($spFields | Where-Object { $_.Title -eq "(RACI) Responsible" } | Select-Object -First 1).InternalName
$aField = ($spFields | Where-Object { $_.Title -eq "(RACI) Accountable" } | Select-Object -First 1).InternalName
$cField = ($spFields | Where-Object { $_.Title -eq "(RACI) Consulted" } | Select-Object -First 1).InternalName
$iField = ($spFields | Where-Object { $_.Title -eq "(RACI) Informed" } | Select-Object -First 1).InternalName
$rolesField = ($spFields | Where-Object { $_.Title -eq "Roles (RACI)" } | Select-Object -First 1).InternalName

$items = Get-PnPListItem -List $LibraryName -PageSize 500

$fixed = 0
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

    $values[$rField] = $raci.R
    $values[$aField] = $raci.A
    if ($raci.C.Count -gt 0) { $values[$cField] = $raci.C }
    if ($raci.I.Count -gt 0) { $values[$iField] = $raci.I }
    $values[$rolesField] = $raci.Roles

    try {
        Set-PnPListItem -List $LibraryName -Identity $item.Id -Values $values | Out-Null
        $fixed++
        Write-Host "  OK: $sopId | R=$($raci.R) A=$($raci.A) Roles=$($raci.Roles -join ', ')" -ForegroundColor Green
    } catch {
        Write-Host "  ERROR: $sopId | $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nFixed $fixed of $($MissingSOPs.Count).`n" -ForegroundColor Cyan
Disconnect-PnPOnline
Write-Host "Disconnected." -ForegroundColor Gray
