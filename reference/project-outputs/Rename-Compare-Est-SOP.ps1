<#
.SYNOPSIS
    Rename 9.4.040 Compare Estimated vs. Planned Performance to 9.2.055
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

$enDash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Rename Compare Estimated vs Planned" -ForegroundColor Cyan
Write-Host "  9.4.040 -> 9.2.055" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# SharePoint rename
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }

# Check if 9.2.055 already exists
Write-Host "Checking for existing 9.2.055 files..." -ForegroundColor Yellow
$existing9205 = $items | Where-Object { $_.FieldValues["FileLeafRef"] -like "9.2.055*" }
if ($existing9205) {
    foreach ($f in $existing9205) {
        Write-Host "  EXISTS: $($f.FieldValues['FileLeafRef'])" -ForegroundColor Magenta
    }
}

# Find the 9.4.040 file
$targetFile = $items | Where-Object {
    $fileName = $_.FieldValues["FileLeafRef"]
    $fileName -like "9.4.040*Compare*Estimated*Planned*"
}

if ($targetFile) {
    $oldFileName = $targetFile.FieldValues["FileLeafRef"]
    Write-Host "`nFound: $oldFileName" -ForegroundColor Cyan

    $newFileName = "9.2.055 $enDash Compare Estimated vs Planned Performance.docx"
    $newSopFileName = "9.2.055 $enDash Compare Estimated vs Planned Performance"
    $newTitle = "Compare Estimated vs Planned Performance"
    $newSopId = "9.2.055"

    Write-Host "Renaming to: $newFileName" -ForegroundColor Yellow

    # Rename file
    try {
        $serverRelativeUrl = $targetFile.FieldValues["FileRef"]

        Rename-PnPFile -ServerRelativeUrl $serverRelativeUrl -TargetFileName $newFileName -Force -ErrorAction Stop
        Write-Host "[FILE RENAMED]" -ForegroundColor Green

        # Update metadata
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
    Write-Host "9.4.040 Compare Estimated file not found in SharePoint" -ForegroundColor Yellow
}

Disconnect-PnPOnline

# Rename local file
Write-Host "`nChecking local folder..." -ForegroundColor Yellow

$localFile = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" | Where-Object {
    $_.Name -like "9.4.040*Compare*Estimated*Planned*"
}

if ($localFile) {
    Write-Host "Found locally: $($localFile.Name)" -ForegroundColor Cyan
    $newLocalName = "9.2.055 $enDash Compare Estimated vs Planned Performance.docx"

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
