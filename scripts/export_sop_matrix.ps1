Connect-PnPOnline -Url 'https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures' -UseWebLogin
$items = Get-PnPListItem -List 'Key_SOP_Matrix' -PageSize 100
$data = $items | ForEach-Object { $_.FieldValues }
$data | ConvertTo-Json -Depth 3 | Out-File -FilePath 'C:\Users\tewing\Documents\Projects\GSL-Operations-Framework\data\Key_SOP_Matrix.json' -Encoding UTF8
Write-Host "Exported $($items.Count) items to Key_SOP_Matrix.json"
