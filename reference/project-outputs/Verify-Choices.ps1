<#
.SYNOPSIS
    Verify actual choice values on all 5 RACI columns
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue -ErrorAction Stop
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected.`n" -ForegroundColor Green

$ColumnTitles = @(
    "(RACI) Responsible",
    "(RACI) Accountable",
    "(RACI) Consulted",
    "(RACI) Informed",
    "Roles (RACI)"
)

$spFields = Get-PnPField -List $LibraryName

foreach ($title in $ColumnTitles) {
    $field = $spFields | Where-Object { $_.Title -eq $title } | Select-Object -First 1
    if (-not $field) {
        Write-Host "NOT FOUND: $title" -ForegroundColor Red
        continue
    }

    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Column: $title" -ForegroundColor Cyan
    Write-Host "InternalName: $($field.InternalName)" -ForegroundColor Gray
    Write-Host "Type: $($field.TypeAsString)" -ForegroundColor Gray

    if ($field.Choices) {
        Write-Host "Choice count: $($field.Choices.Count)" -ForegroundColor Yellow
        Write-Host "Choices:" -ForegroundColor Yellow
        $i = 1
        foreach ($choice in $field.Choices) {
            Write-Host "  $i. '$choice'" -ForegroundColor White
            $i++
        }
    } else {
        Write-Host "No Choices property found" -ForegroundColor Red
    }
    Write-Host ""
}

Disconnect-PnPOnline
Write-Host "Disconnected." -ForegroundColor Gray
