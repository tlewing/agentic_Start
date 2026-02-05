# List all SOP files in SharePoint Library
Import-Module SharePointPnPPowerShellOnline -ErrorAction Stop -WarningAction SilentlyContinue

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue

Write-Host "`nListing all .docx files in library..." -ForegroundColor Yellow

$items = Get-PnPListItem -List $LibraryName -Fields "FileLeafRef","FileRef","SOPID","Title","Created" -PageSize 500

$files = $items | Where-Object { $_["FileLeafRef"] -like "*.docx" } | ForEach-Object {
    [PSCustomObject]@{
        Id = $_.Id
        FileName = $_["FileLeafRef"]
        SOPID = $_["SOPID"]
        Title = $_["Title"]
        Created = $_["Created"]
    }
} | Sort-Object FileName

Write-Host "`nTotal files found: $($files.Count)`n"

$files | Format-Table Id, FileName, SOPID, Title -AutoSize

Disconnect-PnPOnline
