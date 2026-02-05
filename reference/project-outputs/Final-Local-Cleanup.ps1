<#
.SYNOPSIS
    Final cleanup - delete local duplicates that don't match SharePoint exactly
#>

$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"
$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Final Local Cleanup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Get all SharePoint file names
Write-Host "Getting SharePoint file names..." -ForegroundColor Yellow
$spItems = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
$spFileNames = @{}
foreach ($item in $spItems) {
    $fileName = $item.FieldValues["FileLeafRef"]
    $spFileNames[$fileName] = $true
}
Write-Host "Found $($spFileNames.Count) files in SharePoint`n" -ForegroundColor Cyan

Disconnect-PnPOnline

# Get local files
$localFiles = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx"
Write-Host "Found $($localFiles.Count) local files`n" -ForegroundColor Cyan

# Find local files that don't exist in SharePoint
$toDelete = @()
foreach ($file in $localFiles) {
    if (-not $spFileNames.ContainsKey($file.Name)) {
        $toDelete += $file
    }
}

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Files to delete (not in SharePoint): $($toDelete.Count)" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Yellow

foreach ($file in $toDelete) {
    Write-Host "  $($file.Name)" -ForegroundColor Red
}

if ($toDelete.Count -gt 0) {
    Write-Host "`nDeleting..." -ForegroundColor Yellow
    $deleted = 0
    foreach ($file in $toDelete) {
        try {
            Remove-Item -Path $file.FullName -Force -ErrorAction Stop
            Write-Host "  [DELETED] $($file.Name)" -ForegroundColor Green
            $deleted++
        }
        catch {
            Write-Host "  [FAILED] $($file.Name): $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    Write-Host "`nDeleted: $deleted files" -ForegroundColor Green
}

# Count remaining
$remaining = (Get-ChildItem -Path $LocalSOPPath -Filter "*.docx").Count
Write-Host "`nLocal files remaining: $remaining" -ForegroundColor Cyan

Read-Host "`nPress Enter to close"
