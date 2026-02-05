<#
.SYNOPSIS
    Delete the combined 9.2.030-070 Scope and Contract Review SOP
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Delete Combined SOP 9.2.030-070" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Delete from SharePoint
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }

# Find the combined file
$targetFile = $items | Where-Object {
    $fileName = $_.FieldValues["FileLeafRef"]
    $fileName -like "9.2.030*070*Scope*Contract Review*"
}

if ($targetFile) {
    $fileName = $targetFile.FieldValues["FileLeafRef"]
    Write-Host "Found in SharePoint: $fileName" -ForegroundColor Cyan

    try {
        Remove-PnPListItem -List $LibraryName -Identity $targetFile.Id -Force -ErrorAction Stop
        Write-Host "[DELETED from SharePoint]" -ForegroundColor Green
    }
    catch {
        Write-Host "[FAILED] $($_.Exception.Message)" -ForegroundColor Red
    }
}
else {
    Write-Host "File not found in SharePoint" -ForegroundColor Yellow
}

Disconnect-PnPOnline

# Delete from local folder
Write-Host "`nChecking local folder..." -ForegroundColor Yellow

$localFiles = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" | Where-Object {
    $_.Name -like "9.2.030*070*Scope*Contract Review*"
}

if ($localFiles) {
    foreach ($file in $localFiles) {
        Write-Host "Found locally: $($file.Name)" -ForegroundColor Cyan
        try {
            Remove-Item -Path $file.FullName -Force -ErrorAction Stop
            Write-Host "[DELETED from local]" -ForegroundColor Green
        }
        catch {
            Write-Host "[FAILED] $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}
else {
    Write-Host "File not found locally" -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Read-Host "Press Enter to close"
