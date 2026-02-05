# Connect to SharePoint SOP Site
# Run this first to authenticate

Import-Module PnP.PowerShell -ErrorAction Stop

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"

Write-Host "Connecting to SharePoint SOP site..." -ForegroundColor Cyan
Write-Host "A browser window will open - sign in and close it when done." -ForegroundColor Yellow

Connect-PnPOnline -Url $SiteUrl -UseWebLogin

Write-Host "Connected successfully!" -ForegroundColor Green
