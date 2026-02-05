<#
.SYNOPSIS
    Grant permissions to SOP Library as SharePoint Admin
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "SOP Library"
$UserEmail = "tewing@gslelectric.com"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Fix SOP Library Permissions" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Check current site permissions
Write-Host "Current site collection admins:" -ForegroundColor Yellow
try {
    $admins = Get-PnPSiteCollectionAdmin
    foreach ($admin in $admins) {
        Write-Host "  - $($admin.Title) ($($admin.Email))" -ForegroundColor White
    }
}
catch {
    Write-Host "  Could not retrieve admins: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Check if user is site collection admin
Write-Host "`nChecking your admin status..." -ForegroundColor Yellow
$web = Get-PnPWeb -Includes CurrentUser
$currentUser = $web.CurrentUser
Write-Host "  You are: $($currentUser.Title)" -ForegroundColor White

# Try to add yourself as site collection admin
Write-Host "`nAttempting to add you as Site Collection Admin..." -ForegroundColor Yellow
try {
    Add-PnPSiteCollectionAdmin -Owners $UserEmail
    Write-Host "  SUCCESS: Added as Site Collection Admin" -ForegroundColor Green
}
catch {
    Write-Host "  Note: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Grant Full Control on the library
Write-Host "`nGranting Full Control on SOP Library..." -ForegroundColor Yellow
try {
    # Break inheritance if needed
    $list = Get-PnPList -Identity $LibraryName

    # Add permission
    Set-PnPListPermission -Identity $LibraryName -User $UserEmail -AddRole "Full Control"
    Write-Host "  SUCCESS: Granted Full Control" -ForegroundColor Green
}
catch {
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red

    Write-Host "`nTrying alternative method..." -ForegroundColor Yellow
    try {
        # Try site level
        Set-PnPWebPermission -User $UserEmail -AddRole "Full Control"
        Write-Host "  SUCCESS: Granted Full Control at site level" -ForegroundColor Green
    }
    catch {
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Test upload again
Write-Host "`n----------------------------------------" -ForegroundColor DarkGray
Write-Host "Testing upload permission..." -ForegroundColor Yellow
$TestFile = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs\9.2.005 Review Contract for High-Risk Clauses - REVISED.docx"

try {
    $result = Add-PnPFile -Path $TestFile -Folder $LibraryName -ErrorAction Stop
    if ($result -and $result.ServerRelativeUrl) {
        Write-Host "  UPLOAD WORKS! URL: $($result.ServerRelativeUrl)" -ForegroundColor Green
        # Remove test file
        Remove-PnPFile -ServerRelativeUrl $result.ServerRelativeUrl -Force -ErrorAction SilentlyContinue
        Write-Host "  (Test file cleaned up)" -ForegroundColor Gray
    }
}
catch {
    Write-Host "  Still failing: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "`n  You may need to use SharePoint Admin Center:" -ForegroundColor Yellow
    Write-Host "  1. Go to: https://gslelectric8540-admin.sharepoint.com" -ForegroundColor White
    Write-Host "  2. Sites > Active sites > StandardOperationProcedures" -ForegroundColor White
    Write-Host "  3. Permissions > Site admins > Add yourself" -ForegroundColor White
}

Write-Host "`n"
Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
