<#
.SYNOPSIS
    Delete duplicate 9.2.020 - Project Turnover Meeting
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Delete 9.2.020 Project Turnover Meeting" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# SharePoint
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }

$targetFile = $items | Where-Object {
    $_.FieldValues["FileLeafRef"] -like "9.2.020*Project Turnover Meeting*"
}

if ($targetFile) {
    $fileName = $targetFile.FieldValues["FileLeafRef"]
    Write-Host "Found: $fileName" -ForegroundColor Cyan

    try {
        Remove-PnPListItem -List $LibraryName -Identity $targetFile.Id -Force -ErrorAction Stop
        Write-Host "[DELETED from SharePoint]" -ForegroundColor Green
    }
    catch {
        Write-Host "[FAILED] $($_.Exception.Message)" -ForegroundColor Red
    }
}
else {
    Write-Host "File not found in SharePoint" -ForegroundColor Yellow
}

Disconnect-PnPOnline

# Local
Write-Host "`nChecking local folder..." -ForegroundColor Yellow
$localFile = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" | Where-Object {
    $_.Name -like "9.2.020*Project Turnover Meeting*"
}

if ($localFile) {
    Write-Host "Found locally: $($localFile.Name)" -ForegroundColor Cyan
    try {
        Remove-Item -Path $localFile.FullName -Force -ErrorAction Stop
        Write-Host "[DELETED from local]" -ForegroundColor Green
    }
    catch {
        Write-Host "[FAILED] $($_.Exception.Message)" -ForegroundColor Red
    }
}
else {
    Write-Host "File not found locally" -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Read-Host "Press Enter to close"
