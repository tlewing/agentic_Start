<#
.SYNOPSIS
    Delete files with triple dashes in SharePoint
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

$enDash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Delete Triple-Dash Files" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

Write-Host "Getting all items..." -ForegroundColor Yellow
$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
Write-Host "Found $($items.Count) files`n" -ForegroundColor Cyan

# Patterns to look for (triple dashes)
$tripleHyphen = " - - - "
$tripleEnDash = " $enDash $enDash $enDash "

# Also check for double dashes
$doubleHyphen = " - - "
$doubleEnDash = " $enDash $enDash "

# Find files with multiple dashes
$filesToDelete = @()

foreach ($item in $items) {
    $fileName = $item.FieldValues["FileLeafRef"]

    $hasTriple = $fileName.Contains($tripleHyphen) -or $fileName.Contains($tripleEnDash)
    $hasDouble = $fileName.Contains($doubleHyphen) -or $fileName.Contains($doubleEnDash)

    if ($hasTriple -or $hasDouble) {
        $filesToDelete += @{
            FileName = $fileName
            ServerRelativeUrl = $item.FieldValues["FileRef"]
            Id = $item.Id
            Type = if ($hasTriple) { "Triple" } else { "Double" }
        }
    }
}

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Found $($filesToDelete.Count) files with extra dashes" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Yellow

if ($filesToDelete.Count -eq 0) {
    Write-Host "No files with extra dashes found." -ForegroundColor Green
    Disconnect-PnPOnline -ErrorAction SilentlyContinue
    Read-Host "`nPress Enter to close"
    exit
}

# List them
foreach ($file in $filesToDelete) {
    Write-Host "  [$($file.Type)] $($file.FileName)" -ForegroundColor Red
}

Write-Host "`nDeleting files..." -ForegroundColor Yellow

$deleted = 0
$failed = 0

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
