<#
.SYNOPSIS
    Rename 9.4.575 Manage Feeder Wire Release to 9.4.571
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

$enDash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Rename Manage Feeder Wire Release" -ForegroundColor Cyan
Write-Host "  9.4.575 -> 9.4.571" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# SharePoint
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }

# Find the file
$targetFile = $items | Where-Object {
    $fileName = $_.FieldValues["FileLeafRef"]
    $fileName -like "9.4.575*Feeder Wire Release*"
}

if ($targetFile) {
    $oldFileName = $targetFile.FieldValues["FileLeafRef"]
    Write-Host "Found: $oldFileName" -ForegroundColor Cyan

    $newFileName = "9.4.571 $enDash Manage Feeder Wire Release.docx"
    $newSopFileName = "9.4.571 $enDash Manage Feeder Wire Release"
    $newTitle = "Manage Feeder Wire Release"
    $newSopId = "9.4.571"

    Write-Host "Renaming to: $newFileName" -ForegroundColor Yellow

    try {
        $serverRelativeUrl = $targetFile.FieldValues["FileRef"]

        Rename-PnPFile -ServerRelativeUrl $serverRelativeUrl -TargetFileName $newFileName -Force -ErrorAction Stop
        Write-Host "[FILE RENAMED]" -ForegroundColor Green

        Set-PnPListItem -List $LibraryName -Identity $targetFile.Id -Values @{
            "Title" = $newTitle
            "SOPID" = $newSopId
            "SOPFileName" = $newSopFileName
        } -ErrorAction Stop | Out-Null
        Write-Host "[METADATA UPDATED]" -ForegroundColor Green
    }
    catch {
        Write-Host "[FAILED] $($_.Exception.Message)" -ForegroundColor Red
    }
}
else {
    Write-Host "File not found in SharePoint" -ForegroundColor Yellow

    # List all 9.4.575 files
    Write-Host "`nAll 9.4.575 files:" -ForegroundColor Yellow
    $all = $items | Where-Object { $_.FieldValues["FileLeafRef"] -like "9.4.575*" }
    foreach ($f in $all) {
        Write-Host "  $($f.FieldValues['FileLeafRef'])" -ForegroundColor Gray
    }
}

Disconnect-PnPOnline

# Rename local file
Write-Host "`nChecking local folder..." -ForegroundColor Yellow

$localFile = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" | Where-Object {
    $_.Name -like "9.4.575*Feeder Wire Release*"
}

if ($localFile) {
    Write-Host "Found locally: $($localFile.Name)" -ForegroundColor Cyan
    $newLocalName = "9.4.571 $enDash Manage Feeder Wire Release.docx"

    try {
        Rename-Item -Path $localFile.FullName -NewName $newLocalName -Force -ErrorAction Stop
        Write-Host "[LOCAL RENAMED] $newLocalName" -ForegroundColor Green
    }
    catch {
        Write-Host "[FAILED] $($_.Exception.Message)" -ForegroundColor Red
    }
}
else {
    Write-Host "File not found locally" -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Read-Host "Press Enter to close"
