<#
.SYNOPSIS
    Delete Type 1 duplicates by SOP ID and partial title match
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

Write-Host "Getting items from SharePoint..." -ForegroundColor Yellow
$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
Write-Host "Found $($items.Count) files`n" -ForegroundColor Cyan

# Patterns to match for deletion (SOP ID and partial title)
$deletePatterns = @(
    @{ SOPID = "9.2.040"; Match = "PM Reviews" },
    @{ SOPID = "9.2.050"; Match = "FS Reviews" },
    @{ SOPID = "9.2.100"; Match = "Layout and Sequencing" },
    @{ SOPID = "9.2.120"; Match = "Tracking and Control" },
    @{ SOPID = "9.6.005"; Match = "Turnover Field Perspective" },
    @{ SOPID = "9.4.220"; Match = "Procore" },
    @{ SOPID = "9.6.020"; Match = "Punch Lists.docx" },
    @{ SOPID = "9.6.040"; Match = "Manage O" },
    @{ SOPID = "9.6.040"; Match = "Manage OM" }
)

$filesToDelete = @()

foreach ($pattern in $deletePatterns) {
    $sopId = $pattern.SOPID
    $matchText = $pattern.Match

    foreach ($item in $items) {
        $fileName = $item.FieldValues["FileLeafRef"]

        if ($fileName -match "^$sopId" -and $fileName -like "*$matchText*") {
            $filesToDelete += @{
                FileName = $fileName
                ServerRelativeUrl = $item.FieldValues["FileRef"]
            }
        }
    }
}

Write-Host "Files to delete:" -ForegroundColor Yellow
foreach ($f in $filesToDelete) {
    Write-Host "  $($f.FileName)" -ForegroundColor Red
}

if ($filesToDelete.Count -eq 0) {
    Write-Host "`nNo matching files found." -ForegroundColor Yellow
    Disconnect-PnPOnline -ErrorAction SilentlyContinue
    Read-Host "`nPress Enter to close"
    exit
}

$deleted = 0
$failed = 0

Write-Host "`nDeleting files..." -ForegroundColor Yellow

foreach ($file in $filesToDelete) {
    Write-Host "Deleting: $($file.FileName)" -ForegroundColor White
    try {
        Remove-PnPFile -ServerRelativeUrl $file.ServerRelativeUrl -Force -ErrorAction Stop
        Write-Host "  [DELETED]" -ForegroundColor Green
        $deleted++
    }
    catch {
        Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
        $failed++
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Deleted: $deleted" -ForegroundColor Green
Write-Host "  Failed: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "========================================`n" -ForegroundColor Cyan

Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
