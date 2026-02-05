<#
.SYNOPSIS
    Upload missing SOP to SharePoint
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

$enDash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Upload Missing SOP to SharePoint" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Find and upload the file
$localFile = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" | Where-Object { $_.Name -like "9.4.365*PCOs*" }

if ($localFile) {
    Write-Host "Found: $($localFile.Name)" -ForegroundColor Cyan

    try {
        # Upload file
        Add-PnPFile -Path $localFile.FullName -Folder $LibraryName -ErrorAction Stop | Out-Null
        Write-Host "[UPLOADED]" -ForegroundColor Green

        # Set metadata
        $sopId = "9.4.365"
        $title = "Manage Potential Change Orders (PCOs)"
        $sopFileName = "9.4.365 $enDash Manage Potential Change Orders (PCOs)"

        $items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object {
            $_.FileSystemObjectType -eq "File" -and $_.FieldValues["FileLeafRef"] -like "9.4.365*PCOs*"
        }

        if ($items) {
            Set-PnPListItem -List $LibraryName -Identity $items.Id -Values @{
                "Title" = $title
                "SOPID" = $sopId
                "SOPFileName" = $sopFileName
            } -ErrorAction SilentlyContinue | Out-Null
            Write-Host "[METADATA SET]" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "[FAILED] $($_.Exception.Message)" -ForegroundColor Red
    }
}
else {
    Write-Host "File not found locally" -ForegroundColor Yellow
}

Disconnect-PnPOnline

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Read-Host "Press Enter to close"
