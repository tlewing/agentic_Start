<#
.SYNOPSIS
    Rename 9.5.010 Handling and or Disposing of Excess Materials to 9.5.015
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

$enDash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Rename Handling Excess Materials" -ForegroundColor Cyan
Write-Host "  9.5.010 -> 9.5.015" -ForegroundColor Cyan
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
    $fileName -like "9.5.010*Excess Materials*"
}

if ($targetFile) {
    $oldFileName = $targetFile.FieldValues["FileLeafRef"]
    Write-Host "Found: $oldFileName" -ForegroundColor Cyan

    $newFileName = "9.5.015 $enDash Handling and or Disposing of Excess Materials.docx"
    $newSopFileName = "9.5.015 $enDash Handling and or Disposing of Excess Materials"
    $newTitle = "Handling and or Disposing of Excess Materials"
    $newSopId = "9.5.015"

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
}

Disconnect-PnPOnline

# Rename local file
Write-Host "`nChecking local folder..." -ForegroundColor Yellow

$localFile = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" | Where-Object {
    $_.Name -like "9.5.010*Excess Materials*"
}

if ($localFile) {
    Write-Host "Found locally: $($localFile.Name)" -ForegroundColor Cyan
    $newLocalName = "9.5.015 $enDash Handling and or Disposing of Excess Materials.docx"

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
