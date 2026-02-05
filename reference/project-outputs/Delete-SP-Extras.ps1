<#
.SYNOPSIS
    Delete extra/duplicate files from SharePoint
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Delete Extra SharePoint Files" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Patterns to delete
$patterns = @(
    "*9.4.010*Procurement*Large Feeder Wire Original*",
    "*9.4.365*Manage Potential Change Orders*PC*Os*",
    "*9.5.010*Conduct Commissioning Meetings*",
    "SOP 9.2.020*Procurement*Large Feeder Wire*"
)

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }

$deleted = 0
foreach ($pattern in $patterns) {
    $targetFiles = $items | Where-Object { $_.FieldValues["FileLeafRef"] -like $pattern }

    if ($targetFiles) {
        foreach ($targetFile in $targetFiles) {
            $fileName = $targetFile.FieldValues["FileLeafRef"]
            Write-Host "Found: $fileName" -ForegroundColor Cyan
            try {
                Remove-PnPListItem -List $LibraryName -Identity $targetFile.Id -Force -ErrorAction Stop
                Write-Host "  [DELETED]" -ForegroundColor Green
                $deleted++
            }
            catch {
                Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    }
    else {
        Write-Host "NOT FOUND: $pattern" -ForegroundColor Yellow
    }
}

Disconnect-PnPOnline

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Deleted $deleted files" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Read-Host "Press Enter to close"
