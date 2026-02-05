<#
.SYNOPSIS
    Fresh connection and upload test
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "SOP Library"
$TestFile = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs\9.2.005 Review Contract for High-Risk Clauses - REVISED.docx"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Fresh Upload Test" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

# Clear any cached connections
Write-Host "Clearing cached connections..." -ForegroundColor Yellow
try { Disconnect-PnPOnline -ErrorAction SilentlyContinue } catch {}
Clear-PnPCredentials -ErrorAction SilentlyContinue

Write-Host "Connecting fresh to SharePoint..." -ForegroundColor Yellow
Write-Host "(Sign in again when prompted)" -ForegroundColor Gray
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Verify admin status
Write-Host "Verifying permissions..." -ForegroundColor Yellow
$web = Get-PnPWeb
$ctx = Get-PnPContext
$ctx.Load($web.CurrentUser)
$ctx.ExecuteQuery()
Write-Host "  User: $($web.CurrentUser.Title)" -ForegroundColor White
Write-Host "  Is Site Admin: $($web.CurrentUser.IsSiteAdmin)" -ForegroundColor White

# Check list permissions directly
Write-Host "`nChecking your effective permissions on library..." -ForegroundColor Yellow
$list = Get-PnPList -Identity $LibraryName
$ctx.Load($list.EffectiveBasePermissions)
$ctx.ExecuteQuery()

$perms = $list.EffectiveBasePermissions
$canAdd = $perms.Has([Microsoft.SharePoint.Client.PermissionKind]::AddListItems)
$canEdit = $perms.Has([Microsoft.SharePoint.Client.PermissionKind]::EditListItems)
$canDelete = $perms.Has([Microsoft.SharePoint.Client.PermissionKind]::DeleteListItems)
$canManage = $perms.Has([Microsoft.SharePoint.Client.PermissionKind]::ManageLists)

Write-Host "  Can Add Items: $canAdd" -ForegroundColor $(if ($canAdd) { "Green" } else { "Red" })
Write-Host "  Can Edit Items: $canEdit" -ForegroundColor $(if ($canEdit) { "Green" } else { "Red" })
Write-Host "  Can Delete Items: $canDelete" -ForegroundColor $(if ($canDelete) { "Green" } else { "Red" })
Write-Host "  Can Manage List: $canManage" -ForegroundColor $(if ($canManage) { "Green" } else { "Red" })

# Check if library requires content approval or checkout
Write-Host "`nLibrary settings:" -ForegroundColor Yellow
Write-Host "  Require Checkout: $($list.ForceCheckout)" -ForegroundColor White
Write-Host "  Enable Moderation: $($list.EnableModeration)" -ForegroundColor White

# Try upload with simple method
Write-Host "`nAttempting upload (simple method)..." -ForegroundColor Yellow
try {
    # Try without metadata first
    $result = Add-PnPFile -Path $TestFile -Folder $LibraryName -NewFileName "TEST_UPLOAD_DELETE_ME.docx"

    if ($result) {
        Write-Host "  SUCCESS!" -ForegroundColor Green
        Write-Host "  URL: $($result.ServerRelativeUrl)" -ForegroundColor White

        # Clean up
        Remove-PnPFile -ServerRelativeUrl $result.ServerRelativeUrl -Force
        Write-Host "  (Test file removed)" -ForegroundColor Gray
    }
    else {
        Write-Host "  No result returned" -ForegroundColor Red
    }
}
catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red

    # Try Documents library
    Write-Host "`nTrying 'Documents' library..." -ForegroundColor Yellow
    try {
        $result = Add-PnPFile -Path $TestFile -Folder "Shared Documents" -NewFileName "TEST_UPLOAD.docx"
        if ($result) {
            Write-Host "  SUCCESS in Documents!" -ForegroundColor Green
            Remove-PnPFile -ServerRelativeUrl $result.ServerRelativeUrl -Force -ErrorAction SilentlyContinue
        }
    }
    catch {
        Write-Host "  Also failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n"
Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
