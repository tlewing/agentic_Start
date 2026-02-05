# Download GSL SOP Master Template from SharePoint
Import-Module SharePointPnPPowerShellOnline -ErrorAction Stop -WarningAction SilentlyContinue

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$TemplatePath = "/sites/StandardOperationProcedures/Standard Operating Procedures/Templates/GSL_SOP_Master_Template_SHAREPOINT_ENABLED (v1).docx"
$LocalFolder = "C:\Users\tewing\Desktop\Claude Projects"

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin

Write-Host "Downloading template..." -ForegroundColor Yellow
Get-PnPFile -Url $TemplatePath -Path $LocalFolder -Filename "GSL_SOP_Template.docx" -AsFile -Force
Write-Host "Downloaded template successfully!" -ForegroundColor Green

Disconnect-PnPOnline
