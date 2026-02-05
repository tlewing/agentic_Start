<#
.SYNOPSIS
    Fix metadata for 9.2.020 - Procurement of Large Feeder Wire
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }

$item = $items | Where-Object { $_.FieldValues["FileLeafRef"] -eq "9.2.020 - Procurement of Large Feeder Wire.docx" }

if ($item) {
    Write-Host "Found file: $($item.FieldValues['FileLeafRef'])" -ForegroundColor Cyan
    Write-Host "Current SOPFileName: $($item.FieldValues['SOPFileName'])" -ForegroundColor Gray
    Write-Host "Current Title: $($item.FieldValues['Title'])" -ForegroundColor Gray

    # Fix the metadata
    $newTitle = "Procurement of Large Feeder Wire"
    $newSopFileName = "9.2.020 - Procurement of Large Feeder Wire"

    Write-Host "`nUpdating to:" -ForegroundColor Yellow
    Write-Host "  SOPFileName: $newSopFileName" -ForegroundColor Cyan
    Write-Host "  Title: $newTitle" -ForegroundColor Cyan

    try {
        Set-PnPListItem -List $LibraryName -Identity $item.Id -Values @{
            "SOPFileName" = $newSopFileName
            "Title" = $newTitle
        } -ErrorAction Stop | Out-Null
        Write-Host "`n[FIXED]" -ForegroundColor Green
    }
    catch {
        Write-Host "`n[FAILED] $($_.Exception.Message)" -ForegroundColor Red

        # Try just fixing the title
        Write-Host "`nTrying to fix just the Title..." -ForegroundColor Yellow
        try {
            Set-PnPListItem -List $LibraryName -Identity $item.Id -Values @{
                "Title" = $newTitle
            } -ErrorAction Stop | Out-Null
            Write-Host "[TITLE FIXED]" -ForegroundColor Green
        }
        catch {
            Write-Host "[FAILED] $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}
else {
    Write-Host "File not found" -ForegroundColor Red
}

Disconnect-PnPOnline
Read-Host "`nPress Enter to close"
