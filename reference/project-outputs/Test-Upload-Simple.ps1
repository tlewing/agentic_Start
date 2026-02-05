<#
.SYNOPSIS
    Simple upload test to multiple locations
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$TestFile = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs\9.2.005 Review Contract for High-Risk Clauses - REVISED.docx"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Simple Upload Test" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Get current user info
$web = Get-PnPWeb
Write-Host "User: $((Get-PnPProperty -ClientObject $web -Property CurrentUser).Title)" -ForegroundColor White
Write-Host "Site Admin: $((Get-PnPProperty -ClientObject $web -Property CurrentUser).IsSiteAdmin)" -ForegroundColor White

# List all document libraries
Write-Host "`nDocument libraries on this site:" -ForegroundColor Yellow
$libs = Get-PnPList | Where-Object { $_.BaseTemplate -eq 101 }
foreach ($lib in $libs) {
    Write-Host "  - $($lib.Title) (Items: $($lib.ItemCount))" -ForegroundColor White
}

# Test upload to each library
Write-Host "`n----------------------------------------" -ForegroundColor DarkGray
Write-Host "Testing uploads to each library..." -ForegroundColor Yellow

foreach ($lib in $libs) {
    Write-Host "`nTrying: $($lib.Title)" -ForegroundColor Cyan
    try {
        $result = Add-PnPFile -Path $TestFile -Folder $lib.Title -NewFileName "TEST_DELETE_ME.docx" -ErrorAction Stop
        if ($result) {
            Write-Host "  SUCCESS!" -ForegroundColor Green
            Write-Host "  URL: $($result.ServerRelativeUrl)" -ForegroundColor Gray
            Remove-PnPFile -ServerRelativeUrl $result.ServerRelativeUrl -Force -ErrorAction SilentlyContinue
            Write-Host "  (cleaned up)" -ForegroundColor Gray
        }
    }
    catch {
        Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Also try creating a new folder and uploading there
Write-Host "`n----------------------------------------" -ForegroundColor DarkGray
Write-Host "Trying to create a test folder in SOP Library..." -ForegroundColor Yellow
try {
    $folder = Add-PnPFolder -Name "TEST_FOLDER_DELETE" -Folder "SOP Library" -ErrorAction Stop
    Write-Host "  Folder created!" -ForegroundColor Green

    Write-Host "  Uploading to new folder..." -ForegroundColor Yellow
    $result = Add-PnPFile -Path $TestFile -Folder "SOP Library/TEST_FOLDER_DELETE" -NewFileName "TEST.docx" -ErrorAction Stop
    if ($result) {
        Write-Host "  SUCCESS in new folder!" -ForegroundColor Green
        Remove-PnPFile -ServerRelativeUrl $result.ServerRelativeUrl -Force -ErrorAction SilentlyContinue
    }

    # Clean up folder
    Remove-PnPFolder -Name "TEST_FOLDER_DELETE" -Folder "SOP Library" -Force -ErrorAction SilentlyContinue
    Write-Host "  (cleaned up)" -ForegroundColor Gray
}
catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n"
Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
