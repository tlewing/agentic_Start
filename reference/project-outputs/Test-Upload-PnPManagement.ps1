<#
.SYNOPSIS
    Test upload using PnP Management Shell app registration
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$TestFile = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs\9.2.005 Review Contract for High-Risk Clauses - REVISED.docx"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Upload Test - PnP Management Shell" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

# Try with SPO Management Shell client ID (pre-registered multi-tenant app)
$SPOClientId = "9bc3ab49-b65d-410a-85ad-de819febfddc"

Write-Host "Trying SPO Management Shell authentication..." -ForegroundColor Yellow
Write-Host "(A browser window will open - sign in there)" -ForegroundColor Gray

try {
    # Disconnect any existing connection
    Disconnect-PnPOnline -ErrorAction SilentlyContinue

    # Try with SPO Management Shell
    Connect-PnPOnline -Url $SiteUrl -SPOManagementShell -WarningAction SilentlyContinue
    Write-Host "Connected with SPO Management Shell!`n" -ForegroundColor Green
}
catch {
    Write-Host "SPO Management Shell failed: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "`nTrying standard web login..." -ForegroundColor Yellow

    Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
    Write-Host "Connected with web login`n" -ForegroundColor Green
}

# Check user
$web = Get-PnPWeb
$user = Get-PnPProperty -ClientObject $web -Property CurrentUser
Write-Host "User: $($user.Title)" -ForegroundColor White
Write-Host "Site Admin: $($user.IsSiteAdmin)" -ForegroundColor White

# Try upload
Write-Host "`nAttempting upload to SOP Library..." -ForegroundColor Yellow
try {
    $result = Add-PnPFile -Path $TestFile -Folder "SOP Library" -NewFileName "TEST_DELETE.docx" -ErrorAction Stop
    if ($result) {
        Write-Host "SUCCESS!" -ForegroundColor Green
        Write-Host "URL: $($result.ServerRelativeUrl)" -ForegroundColor White
        Remove-PnPFile -ServerRelativeUrl $result.ServerRelativeUrl -Force -ErrorAction SilentlyContinue
        Write-Host "(cleaned up)" -ForegroundColor Gray
    }
}
catch {
    Write-Host "FAILED: $($_.Exception.Message)" -ForegroundColor Red

    Write-Host "`n========================================" -ForegroundColor Yellow
    Write-Host "MANUAL FIX REQUIRED" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "`nThe authentication token doesn't have write permissions." -ForegroundColor White
    Write-Host "Please try uploading manually via browser:" -ForegroundColor White
    Write-Host "`n1. Open: https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures/SOP%20Library" -ForegroundColor Cyan
    Write-Host "2. Click 'Upload' > 'Files'" -ForegroundColor White
    Write-Host "3. If that works, PowerShell needs app registration" -ForegroundColor White
    Write-Host "`nTo fix PowerShell access:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://gslelectric8540-admin.sharepoint.com" -ForegroundColor White
    Write-Host "2. Settings > Site permissions" -ForegroundColor White
    Write-Host "3. Or contact your Microsoft 365 admin about app permissions" -ForegroundColor White
}

Write-Host "`n"
Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
