<#
.SYNOPSIS
    Test upload using correct library URL name
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryUrlName = "Standard Operating Procedures"
$TestFile = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs\9.2.005 Review Contract for High-Risk Clauses - REVISED.docx"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Upload Test - Correct Library Name" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Check user
$web = Get-PnPWeb
$user = Get-PnPProperty -ClientObject $web -Property CurrentUser
Write-Host "User: $($user.Title)" -ForegroundColor White
Write-Host "Site Admin: $($user.IsSiteAdmin)" -ForegroundColor White

# Get library info
Write-Host "`nLibrary info:" -ForegroundColor Yellow
$lib = Get-PnPList -Identity $LibraryUrlName -ErrorAction SilentlyContinue
if ($lib) {
    Write-Host "  Title: $($lib.Title)" -ForegroundColor White
    Write-Host "  Item Count: $($lib.ItemCount)" -ForegroundColor White
    Write-Host "  Root Folder: $($lib.RootFolder.ServerRelativeUrl)" -ForegroundColor White
}
else {
    Write-Host "  Library '$LibraryUrlName' not found, trying variations..." -ForegroundColor Yellow

    # List all libraries
    $allLibs = Get-PnPList | Where-Object { $_.BaseTemplate -eq 101 }
    foreach ($l in $allLibs) {
        $rootFolder = Get-PnPProperty -ClientObject $l -Property RootFolder
        Write-Host "  - Title: '$($l.Title)' | URL: '$($rootFolder.Name)'" -ForegroundColor Gray
    }
}

# Try upload with URL name
Write-Host "`nAttempting upload to '$LibraryUrlName'..." -ForegroundColor Yellow
try {
    $result = Add-PnPFile -Path $TestFile -Folder $LibraryUrlName -NewFileName "TEST_DELETE_ME.docx" -ErrorAction Stop
    if ($result) {
        Write-Host "SUCCESS!" -ForegroundColor Green
        Write-Host "URL: $($result.ServerRelativeUrl)" -ForegroundColor White
        Remove-PnPFile -ServerRelativeUrl $result.ServerRelativeUrl -Force -ErrorAction SilentlyContinue
        Write-Host "(cleaned up)" -ForegroundColor Gray
    }
}
catch {
    Write-Host "FAILED with '$LibraryUrlName': $($_.Exception.Message)" -ForegroundColor Red

    # Try with server relative URL
    Write-Host "`nTrying with full server relative path..." -ForegroundColor Yellow
    try {
        $folderPath = "/sites/StandardOperationProcedures/Standard Operating Procedures"
        $result = Add-PnPFile -Path $TestFile -Folder $folderPath -NewFileName "TEST_DELETE_ME.docx" -ErrorAction Stop
        if ($result) {
            Write-Host "SUCCESS with full path!" -ForegroundColor Green
            Write-Host "URL: $($result.ServerRelativeUrl)" -ForegroundColor White
            Remove-PnPFile -ServerRelativeUrl $result.ServerRelativeUrl -Force -ErrorAction SilentlyContinue
            Write-Host "(cleaned up)" -ForegroundColor Gray
        }
    }
    catch {
        Write-Host "FAILED with full path: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n"
Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
