<#
.SYNOPSIS
    Delete Type 1 duplicates (same SOP, shorter/abbreviated title)
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Delete Type 1 Duplicates" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Files to delete (abbreviated/shorter versions)
$filesToDelete = @(
    "9.2.040 - PM Reviews Plans Specs and Schedule.docx",
    "9.2.050 - FS Reviews Plans Specs and Schedule.docx",
    "9.2.100 - Prepare Layout and Sequencing Plan.docx",
    "9.2.120 - Establish Tracking and Control Systems.docx",
    "9.6.005 - Prepare for Turnover Field Perspective.docx",
    "9.4.220 - Manage Drawing Logs (Procore).docx",
    "9.6.020 - Manage Punch Lists.docx",
    "9.6.040 - Manage O&M Manuals.docx",
    "9.6.040 - Manage OM Manuals.docx"
)

Write-Host "Files to delete:" -ForegroundColor Yellow
foreach ($f in $filesToDelete) {
    Write-Host "  $f" -ForegroundColor Red
}

Write-Host "`nGetting items from SharePoint..." -ForegroundColor Yellow
$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }

$deleted = 0
$notFound = 0
$failed = 0

Write-Host "`nDeleting files..." -ForegroundColor Yellow

foreach ($fileToDelete in $filesToDelete) {
    $item = $items | Where-Object { $_.FieldValues["FileLeafRef"] -eq $fileToDelete }

    if ($item) {
        Write-Host "Deleting: $fileToDelete" -ForegroundColor White
        try {
            $serverRelUrl = $item.FieldValues["FileRef"]
            Remove-PnPFile -ServerRelativeUrl $serverRelUrl -Force -ErrorAction Stop
            Write-Host "  [DELETED]" -ForegroundColor Green
            $deleted++
        }
        catch {
            Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
            $failed++
        }
    }
    else {
        Write-Host "Not found: $fileToDelete" -ForegroundColor Yellow
        $notFound++
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Deleted: $deleted" -ForegroundColor Green
Write-Host "  Not Found: $notFound" -ForegroundColor Yellow
Write-Host "  Failed: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "========================================`n" -ForegroundColor Cyan

Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
