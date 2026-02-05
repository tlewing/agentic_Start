<#
.SYNOPSIS
    Check for Project Turnover Documentation in SharePoint
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }

Write-Host "Files with 'Turnover' in name:" -ForegroundColor Cyan
$turnoverFiles = $items | Where-Object { $_.FieldValues["FileLeafRef"] -like "*Turnover*" }
foreach ($f in $turnoverFiles) {
    Write-Host "  $($f.FieldValues['FileLeafRef'])" -ForegroundColor White
}

Write-Host "`nFiles starting with 9.6.01:" -ForegroundColor Cyan
$files96 = $items | Where-Object { $_.FieldValues["FileLeafRef"] -like "9.6.01*" }
foreach ($f in $files96) {
    Write-Host "  $($f.FieldValues['FileLeafRef'])" -ForegroundColor White
}

Disconnect-PnPOnline
