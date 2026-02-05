<#
.SYNOPSIS
    Compare SharePoint files with local folder
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Compare SharePoint vs Local" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Get local files
$localFiles = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" | Select-Object -ExpandProperty Name
Write-Host "Local files: $($localFiles.Count)" -ForegroundColor Cyan

# Get SharePoint files
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

$spItems = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
$spFiles = $spItems | ForEach-Object { $_.FieldValues["FileLeafRef"] }
Write-Host "SharePoint files: $($spFiles.Count)" -ForegroundColor Cyan

Disconnect-PnPOnline

# Normalize file names for comparison (handle dash variations)
$enDash = [char]0x2013
function Normalize-Name($name) {
    return $name.Replace($enDash, '-').ToLower()
}

$localNormalized = @{}
foreach ($f in $localFiles) {
    $localNormalized[(Normalize-Name $f)] = $f
}

$spNormalized = @{}
foreach ($f in $spFiles) {
    $spNormalized[(Normalize-Name $f)] = $f
}

# Find differences
$inLocalOnly = @()
$inSPOnly = @()
$matched = 0

foreach ($key in $localNormalized.Keys) {
    if ($spNormalized.ContainsKey($key)) {
        $matched++
    } else {
        $inLocalOnly += $localNormalized[$key]
    }
}

foreach ($key in $spNormalized.Keys) {
    if (-not $localNormalized.ContainsKey($key)) {
        $inSPOnly += $spNormalized[$key]
    }
}

# Report
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  RESULTS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Matched: $matched files" -ForegroundColor Green

if ($inLocalOnly.Count -gt 0) {
    Write-Host "`nIn LOCAL only ($($inLocalOnly.Count) files):" -ForegroundColor Yellow
    foreach ($f in ($inLocalOnly | Sort-Object)) {
        Write-Host "  $f" -ForegroundColor Yellow
    }
} else {
    Write-Host "`nNo files in LOCAL only" -ForegroundColor Green
}

if ($inSPOnly.Count -gt 0) {
    Write-Host "`nIn SHAREPOINT only ($($inSPOnly.Count) files):" -ForegroundColor Magenta
    foreach ($f in ($inSPOnly | Sort-Object)) {
        Write-Host "  $f" -ForegroundColor Magenta
    }
} else {
    Write-Host "`nNo files in SHAREPOINT only" -ForegroundColor Green
}

if ($inLocalOnly.Count -eq 0 -and $inSPOnly.Count -eq 0) {
    Write-Host "`n*** SharePoint and Local are in SYNC! ***" -ForegroundColor Green
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Read-Host "Press Enter to close"
