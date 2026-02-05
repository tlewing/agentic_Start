Import-Module PnP.PowerShell -ErrorAction Stop

# Use Device Login authentication
Connect-PnPOnline -Url "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures" -DeviceLogin -ClientId "31359c7f-bd7e-475c-86db-fdb8c937548e"

Get-PnPField -List "SOP Library" |
    Where-Object { -not $_.Hidden } |
    Select-Object Title, InternalName, TypeAsString, Required |
    Sort-Object Title |
    Format-Table -AutoSize
