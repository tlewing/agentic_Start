<#
.SYNOPSIS
    Test uploading a single SOP to SharePoint
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "SOP Library"
$TestFile = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs\9.2.005 Review Contract for High-Risk Clauses - REVISED.docx"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Test Single SOP Upload" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check file exists
if (Test-Path $TestFile) {
    Write-Host "File exists: $TestFile" -ForegroundColor Green
    $fileInfo = Get-Item $TestFile
    Write-Host "  Size: $($fileInfo.Length) bytes" -ForegroundColor Gray
}
else {
    Write-Host "ERROR: File not found!" -ForegroundColor Red
    exit 1
}

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "`nConnecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Check current permissions
Write-Host "Checking permissions..." -ForegroundColor Yellow
$web = Get-PnPWeb -Includes EffectiveBasePermissions
$perms = $web.EffectiveBasePermissions
Write-Host "  Can add items: $($perms.Has([Microsoft.SharePoint.Client.PermissionKind]::AddListItems))" -ForegroundColor White
Write-Host "  Can edit items: $($perms.Has([Microsoft.SharePoint.Client.PermissionKind]::EditListItems))" -ForegroundColor White

# Prepare metadata
$metadata = @{
    "Title" = "9.2.005 - Review Contract for High-Risk Clauses"
    "SOPID" = "9.2.005"
    "DocumentType" = "SOP"
    "Status" = "Draft"
    "Department_x002f_Division" = "Operations"
}

Write-Host "`nMetadata:" -ForegroundColor Yellow
$metadata.GetEnumerator() | ForEach-Object {
    Write-Host "  $($_.Key): $($_.Value)" -ForegroundColor White
}

Write-Host "`nAttempting upload..." -ForegroundColor Yellow
try {
    $result = Add-PnPFile -Path $TestFile -Folder $LibraryName -Values $metadata
    Write-Host "`nSUCCESS!" -ForegroundColor Green
    Write-Host "  Server Relative URL: $($result.ServerRelativeUrl)" -ForegroundColor White
    Write-Host "  Unique ID: $($result.UniqueId)" -ForegroundColor White
}
catch {
    Write-Host "`nFAILED!" -ForegroundColor Red
    Write-Host "  Error Type: $($_.Exception.GetType().FullName)" -ForegroundColor Red
    Write-Host "  Message: $($_.Exception.Message)" -ForegroundColor Red

    if ($_.Exception.InnerException) {
        Write-Host "  Inner: $($_.Exception.InnerException.Message)" -ForegroundColor Red
    }
}

# Verify upload
Write-Host "`nVerifying upload..." -ForegroundColor Yellow
$items = Get-PnPListItem -List $LibraryName -PageSize 100 | Where-Object {
    $_.FieldValues["FileLeafRef"] -like "*9.2.005*"
}
Write-Host "  Items matching '9.2.005': $($items.Count)" -ForegroundColor Cyan

Write-Host ""
Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
