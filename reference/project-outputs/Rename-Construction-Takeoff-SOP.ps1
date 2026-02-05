<#
.SYNOPSIS
    Rename 9.4.050 Prepare Construction Takeoff to 9.1.050
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

$enDash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Rename Prepare Construction Takeoff" -ForegroundColor Cyan
Write-Host "  9.4.050 -> 9.1.050" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# SharePoint rename
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }

# Check if 9.1.050 already exists
Write-Host "Checking for existing 9.1.050 files..." -ForegroundColor Yellow
$existing = $items | Where-Object { $_.FieldValues["FileLeafRef"] -like "9.1.050*" }
if ($existing) {
    foreach ($f in $existing) {
        Write-Host "  EXISTS: $($f.FieldValues['FileLeafRef'])" -ForegroundColor Magenta
    }
} else {
    Write-Host "  No existing 9.1.050 files" -ForegroundColor Gray
}

# Find the 9.4.050 Prepare Construction Takeoff file
$targetFile = $items | Where-Object {
    $fileName = $_.FieldValues["FileLeafRef"]
    $fileName -like "9.4.050*Prepare*Construction*Takeoff*"
}

if ($targetFile) {
    $oldFileName = $targetFile.FieldValues["FileLeafRef"]
    Write-Host "`nFound: $oldFileName" -ForegroundColor Cyan

    $newFileName = "9.1.050 $enDash Prepare Construction Takeoff.docx"
    $newSopFileName = "9.1.050 $enDash Prepare Construction Takeoff"
    $newTitle = "Prepare Construction Takeoff"
    $newSopId = "9.1.050"

    Write-Host "Renaming to: $newFileName" -ForegroundColor Yellow

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
    Write-Host "9.4.050 Prepare Construction Takeoff not found in SharePoint" -ForegroundColor Yellow

    # List all 9.4.050 files
    Write-Host "`nAll 9.4.050 files:" -ForegroundColor Yellow
    $all = $items | Where-Object { $_.FieldValues["FileLeafRef"] -like "9.4.050*" }
    foreach ($f in $all) {
        Write-Host "  $($f.FieldValues['FileLeafRef'])" -ForegroundColor Gray
    }
}

Disconnect-PnPOnline

# Rename local file
Write-Host "`nChecking local folder..." -ForegroundColor Yellow

$localFile = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" | Where-Object {
    $_.Name -like "9.4.050*Prepare*Construction*Takeoff*"
}

if ($localFile) {
    Write-Host "Found locally: $($localFile.Name)" -ForegroundColor Cyan
    $newLocalName = "9.1.050 $enDash Prepare Construction Takeoff.docx"

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
