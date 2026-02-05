<#
.SYNOPSIS
    Rename 9.4.010 Procurement Large Feeder Wire Original to 9.2.020 Procurement Large Feeder Wire
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

$enDash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Rename Procurement Large Feeder Wire" -ForegroundColor Cyan
Write-Host "  9.4.010 -> 9.2.020" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# SharePoint rename
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }

# Find the file
$targetFile = $items | Where-Object {
    $fileName = $_.FieldValues["FileLeafRef"]
    $fileName -like "9.4.010*Procurement*Large Feeder Wire*Original*"
}

if ($targetFile) {
    $oldFileName = $targetFile.FieldValues["FileLeafRef"]
    Write-Host "Found: $oldFileName" -ForegroundColor Cyan

    $newFileName = "9.2.020 $enDash Procurement of Large Feeder Wire.docx"
    $newSopFileName = "9.2.020 $enDash Procurement of Large Feeder Wire"
    $newTitle = "Procurement of Large Feeder Wire"
    $newSopId = "9.2.020"

    Write-Host "`nRenaming to: $newFileName" -ForegroundColor Yellow

    # Rename file
    try {
        $serverRelativeUrl = $targetFile.FieldValues["FileRef"]
        $folderPath = $serverRelativeUrl.Substring(0, $serverRelativeUrl.LastIndexOf('/'))
        $newServerRelativeUrl = "$folderPath/$newFileName"

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
    Write-Host "File not found in SharePoint" -ForegroundColor Yellow

    # List all 9.4.010 files for debugging
    Write-Host "`nLooking for any 9.4.010 files:" -ForegroundColor Yellow
    $all9410 = $items | Where-Object { $_.FieldValues["FileLeafRef"] -like "9.4.010*" }
    foreach ($f in $all9410) {
        Write-Host "  $($f.FieldValues['FileLeafRef'])" -ForegroundColor Gray
    }
}

Disconnect-PnPOnline

# Rename local file
Write-Host "`nChecking local folder..." -ForegroundColor Yellow

$localFile = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" | Where-Object {
    $_.Name -like "9.4.010*Procurement*Large Feeder Wire*Original*"
}

if ($localFile) {
    Write-Host "Found locally: $($localFile.Name)" -ForegroundColor Cyan
    $newLocalName = "9.2.020 $enDash Procurement of Large Feeder Wire.docx"
    $newLocalPath = Join-Path $LocalSOPPath $newLocalName

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
