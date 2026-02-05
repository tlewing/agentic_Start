$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue
Connect-PnPOnline -Url 'https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures' -UseWebLogin -WarningAction SilentlyContinue
$lib = Get-PnPList -Identity 'Standard Operating Procedures'
Write-Host "Library: $($lib.Title)"
Write-Host "Item Count: $($lib.ItemCount)"
Disconnect-PnPOnline
