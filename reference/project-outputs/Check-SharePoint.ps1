<#
.SYNOPSIS
    Check what's in the SharePoint SOP Library
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "SOP Library"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Checking SharePoint SOP Library" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

Write-Host "Querying SOP Library..." -ForegroundColor Yellow
$items = Get-PnPListItem -List $LibraryName -PageSize 500

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Results" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Total items in library: $($items.Count)" -ForegroundColor Cyan
Write-Host ""

if ($items.Count -gt 0) {
    Write-Host "Recent items:" -ForegroundColor Yellow
    $items | Select-Object -First 20 | ForEach-Object {
        $name = $_.FieldValues["FileLeafRef"]
        $created = $_.FieldValues["Created"]
        Write-Host "  - $name ($created)" -ForegroundColor White
    }
}

Write-Host ""
Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
