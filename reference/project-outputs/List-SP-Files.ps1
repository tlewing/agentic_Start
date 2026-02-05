<#
.SYNOPSIS
    List all SharePoint files to check names
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

$enDash = [char]0x2013

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue

$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }

Write-Host "`nFiles with issues:`n" -ForegroundColor Yellow

foreach ($item in $items) {
    $fileName = $item.FieldValues["FileLeafRef"]
    $sopFileName = $item.FieldValues["SOPFileName"]
    $title = $item.FieldValues["Title"]

    # Check for any dash issues
    $fileIssue = $fileName -match " [-$enDash] [-$enDash] "
    $sopIssue = $sopFileName -and ($sopFileName -match " [-$enDash] [-$enDash] " -or $sopFileName.StartsWith("-") -or $sopFileName.StartsWith($enDash))
    $titleIssue = $title -and ($title.StartsWith("-") -or $title.StartsWith($enDash) -or $title.StartsWith(" "))

    if ($fileIssue -or $sopIssue -or $titleIssue) {
        Write-Host "File: $fileName" -ForegroundColor Red
        Write-Host "  SOPFileName: $sopFileName" -ForegroundColor Gray
        Write-Host "  Title: $title" -ForegroundColor Gray
        Write-Host ""
    }
}

Write-Host "`nChecking for 9.2.020 specifically:" -ForegroundColor Yellow
$item9220 = $items | Where-Object { $_.FieldValues["FileLeafRef"] -like "9.2.020*" }
foreach ($i in $item9220) {
    Write-Host "  File: $($i.FieldValues['FileLeafRef'])" -ForegroundColor Cyan
    Write-Host "  SOPFileName: $($i.FieldValues['SOPFileName'])" -ForegroundColor Gray
    Write-Host "  Title: $($i.FieldValues['Title'])" -ForegroundColor Gray
}

Disconnect-PnPOnline
