<#
.SYNOPSIS
    Test uploading to different folders in SharePoint
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "SOP Library"
$TestFile = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs\9.2.005 Review Contract for High-Risk Clauses - REVISED.docx"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Test Folder Upload Permissions" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Get your account info
Write-Host "Current user info:" -ForegroundColor Yellow
$me = Get-PnPProperty -ClientObject (Get-PnPWeb) -Property CurrentUser
Write-Host "  Logged in as: $($me.Title) ($($me.Email))" -ForegroundColor White

# Check library role assignments
Write-Host "`nLibrary permissions:" -ForegroundColor Yellow
$list = Get-PnPList -Identity $LibraryName -Includes RoleAssignments, HasUniqueRoleAssignments
Write-Host "  Has unique permissions: $($list.HasUniqueRoleAssignments)" -ForegroundColor White

# Try different locations
$locations = @(
    "$LibraryName",
    "$LibraryName/Templates",
    "$LibraryName/ARCHIVE",
    "Documents"
)

foreach ($loc in $locations) {
    Write-Host "`n----------------------------------------" -ForegroundColor DarkGray
    Write-Host "Testing upload to: $loc" -ForegroundColor Yellow

    try {
        $result = Add-PnPFile -Path $TestFile -Folder $loc -ErrorAction Stop
        if ($result -and $result.ServerRelativeUrl) {
            Write-Host "  SUCCESS! URL: $($result.ServerRelativeUrl)" -ForegroundColor Green
            # Delete test file
            Remove-PnPFile -ServerRelativeUrl $result.ServerRelativeUrl -Force -ErrorAction SilentlyContinue
            Write-Host "  (Test file removed)" -ForegroundColor Gray
        }
        else {
            Write-Host "  FAILED - No result returned" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n"
Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
