<#
.SYNOPSIS
    Delete duplicate SOPs - keep specified versions
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Delete Duplicate SOPs" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Files to delete (keep the other version)
$toDelete = @(
    "9.2.055*Compare Est vs Planned.docx",
    "9.2.060*Create List of Issues*"
)

# SharePoint
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }

Write-Host "Deleting from SharePoint..." -ForegroundColor Yellow
foreach ($pattern in $toDelete) {
    $targetFile = $items | Where-Object { $_.FieldValues["FileLeafRef"] -like $pattern }

    if ($targetFile) {
        $fileName = $targetFile.FieldValues["FileLeafRef"]
        Write-Host "  Found: $fileName" -ForegroundColor Cyan

        try {
            Remove-PnPListItem -List $LibraryName -Identity $targetFile.Id -Force -ErrorAction Stop
            Write-Host "  [DELETED]" -ForegroundColor Green
        }
        catch {
            Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    else {
        Write-Host "  NOT FOUND: $pattern" -ForegroundColor Yellow
    }
}

Disconnect-PnPOnline

# Local
Write-Host "`nDeleting from local folder..." -ForegroundColor Yellow
foreach ($pattern in $toDelete) {
    $localFile = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" | Where-Object { $_.Name -like $pattern }

    if ($localFile) {
        Write-Host "  Found: $($localFile.Name)" -ForegroundColor Cyan
        try {
            Remove-Item -Path $localFile.FullName -Force -ErrorAction Stop
            Write-Host "  [DELETED]" -ForegroundColor Green
        }
        catch {
            Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    else {
        Write-Host "  NOT FOUND: $pattern" -ForegroundColor Yellow
    }
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Read-Host "Press Enter to close"
