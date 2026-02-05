# Download SOP Template from SharePoint
# Run 1_Connect-SharePoint.ps1 first

$LibraryName = "Standard Operating Procedures"
$TemplatePath = "/sites/StandardOperationProcedures/Standard Operating Procedures/Templates"
$LocalPath = "C:\Users\tewing\Desktop\Holding\SOP\Templates"

# Create local folder if it doesn't exist
if (-not (Test-Path $LocalPath)) {
    New-Item -ItemType Directory -Path $LocalPath -Force | Out-Null
    Write-Host "Created folder: $LocalPath" -ForegroundColor Green
}

Write-Host "Downloading template from SharePoint..." -ForegroundColor Cyan

# Get files from Templates folder
$Files = Get-PnPFolderItem -FolderSiteRelativeUrl "Standard Operating Procedures/Templates" -ItemType File

foreach ($File in $Files) {
    $FileName = $File.Name
    Write-Host "  Downloading: $FileName" -ForegroundColor Gray
    Get-PnPFile -Url $File.ServerRelativeUrl -Path $LocalPath -FileName $FileName -AsFile -Force
}

Write-Host "`nTemplate download complete!" -ForegroundColor Green
Write-Host "  $LocalPath" -ForegroundColor White
