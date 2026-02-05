<#
.SYNOPSIS
    Find duplicate SOPs in SharePoint
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Find Duplicate SOPs" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

Write-Host "Getting all items..." -ForegroundColor Yellow
$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
Write-Host "Found $($items.Count) files`n" -ForegroundColor Cyan

# Group by SOP ID
$sopGroups = @{}

foreach ($item in $items) {
    $fileName = $item.FieldValues["FileLeafRef"]

    if ($fileName -match "^([\d\.]+)") {
        $sopId = $Matches[1].TrimEnd('.')

        if (-not $sopGroups.ContainsKey($sopId)) {
            $sopGroups[$sopId] = @()
        }

        $sopGroups[$sopId] += @{
            FileName = $fileName
            Id = $item.Id
            ServerRelativeUrl = $item.FieldValues["FileRef"]
            Created = $item.FieldValues["Created"]
            Modified = $item.FieldValues["Modified"]
        }
    }
}

# Find duplicates
$duplicates = $sopGroups.GetEnumerator() | Where-Object { $_.Value.Count -gt 1 } | Sort-Object Name

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  DUPLICATE SOPs FOUND: $($duplicates.Count)" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Yellow

$report = @()

foreach ($dup in $duplicates) {
    $sopId = $dup.Name
    $files = $dup.Value | Sort-Object Modified -Descending

    Write-Host "SOP ID: $sopId ($($files.Count) files)" -ForegroundColor Cyan

    $isFirst = $true
    foreach ($file in $files) {
        if ($isFirst) {
            Write-Host "  [KEEP?] $($file.FileName)" -ForegroundColor Green
            Write-Host "          Modified: $($file.Modified)" -ForegroundColor Gray
            $isFirst = $false
        }
        else {
            Write-Host "  [DELETE?] $($file.FileName)" -ForegroundColor Red
            Write-Host "            Modified: $($file.Modified)" -ForegroundColor Gray
        }

        $report += [PSCustomObject]@{
            SOPID = $sopId
            FileName = $file.FileName
            Modified = $file.Modified
            ServerRelativeUrl = $file.ServerRelativeUrl
            ItemId = $file.Id
        }
    }
    Write-Host ""
}

# Export to CSV
$csvPath = "C:\Users\tewing\Desktop\Claude Projects\Project Outputs\Duplicate_SOPs.csv"
$report | Export-Csv -Path $csvPath -NoTypeInformation
Write-Host "========================================" -ForegroundColor Green
Write-Host "Report saved to: $csvPath" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Total SOP IDs with duplicates: $($duplicates.Count)" -ForegroundColor White
Write-Host "  Total duplicate files: $(($report | Measure-Object).Count)" -ForegroundColor White

Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "`nPress Enter to close"
