<#
.SYNOPSIS
    Deep check of SharePoint SOP Library
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "SOP Library"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Deep Check - SharePoint SOP Library" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Check library settings
Write-Host "Checking library settings..." -ForegroundColor Yellow
$list = Get-PnPList -Identity $LibraryName
Write-Host "  Library: $($list.Title)" -ForegroundColor White
Write-Host "  Item Count: $($list.ItemCount)" -ForegroundColor White
Write-Host "  Enable Versioning: $($list.EnableVersioning)" -ForegroundColor White
Write-Host "  Enable Moderation (Content Approval): $($list.EnableModeration)" -ForegroundColor White
Write-Host "  Base Template: $($list.BaseTemplate)" -ForegroundColor White
Write-Host ""

# Get all items including folders
Write-Host "Getting all items (including pending/draft)..." -ForegroundColor Yellow
try {
    $allItems = Get-PnPListItem -List $LibraryName -PageSize 1000
    Write-Host "  Total items: $($allItems.Count)" -ForegroundColor Cyan
}
catch {
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Check for items with today's date
Write-Host "`nItems created today (Jan 19, 2026):" -ForegroundColor Yellow
$today = Get-Date -Format "yyyy-MM-dd"
$todayItems = $allItems | Where-Object {
    $created = $_.FieldValues["Created"]
    $created -and $created.ToString("yyyy-MM-dd") -eq $today
}
Write-Host "  Found: $($todayItems.Count)" -ForegroundColor Cyan

if ($todayItems.Count -gt 0) {
    $todayItems | ForEach-Object {
        $name = $_.FieldValues["FileLeafRef"]
        $status = $_.FieldValues["_ModerationStatus"]
        Write-Host "  - $name (Status: $status)" -ForegroundColor White
    }
}

# Check folders
Write-Host "`nFolders in library:" -ForegroundColor Yellow
$folders = $allItems | Where-Object { $_.FileSystemObjectType -eq "Folder" }
foreach ($folder in $folders) {
    $name = $folder.FieldValues["FileLeafRef"]
    Write-Host "  - $name" -ForegroundColor White

    # Check items in folder
    $folderItems = Get-PnPListItem -List $LibraryName -FolderServerRelativeUrl "/sites/StandardOperationProcedures/$LibraryName/$name" -PageSize 500 -ErrorAction SilentlyContinue
    if ($folderItems) {
        Write-Host "    Items in folder: $($folderItems.Count)" -ForegroundColor Gray
    }
}

# List all document libraries
Write-Host "`nAll document libraries on site:" -ForegroundColor Yellow
$allLists = Get-PnPList | Where-Object { $_.BaseTemplate -eq 101 }
foreach ($lib in $allLists) {
    Write-Host "  - $($lib.Title) (Items: $($lib.ItemCount))" -ForegroundColor White
}

Write-Host ""
Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
