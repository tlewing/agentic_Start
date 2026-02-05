# Remove Duplicate SOP Files from SharePoint Library
# Keeps files WITH metadata, removes files WITHOUT metadata
Import-Module SharePointPnPPowerShellOnline -ErrorAction Stop -WarningAction SilentlyContinue

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

# IDs of duplicate files to remove (files without SOPID metadata)
$DuplicateIds = @(464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482)

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue

Write-Host "`nRemoving duplicate SOP files..." -ForegroundColor Yellow

$successCount = 0
$errorCount = 0

foreach ($id in $DuplicateIds) {
    try {
        # Get the file info first
        $item = Get-PnPListItem -List $LibraryName -Id $id -ErrorAction Stop
        $fileName = $item["FileLeafRef"]

        Write-Host "  Deleting ID $id : $fileName" -ForegroundColor Cyan

        # Remove the item
        Remove-PnPListItem -List $LibraryName -Identity $id -Force -ErrorAction Stop

        Write-Host "    Deleted successfully" -ForegroundColor Green
        $successCount++
    }
    catch {
        Write-Host "  Error deleting ID $id : $($_.Exception.Message)" -ForegroundColor Red
        $errorCount++
    }
}

Write-Host "`n=== Cleanup Complete ===" -ForegroundColor Green
Write-Host "Deleted: $successCount files" -ForegroundColor Green
if ($errorCount -gt 0) {
    Write-Host "Errors: $errorCount" -ForegroundColor Red
}

Disconnect-PnPOnline
