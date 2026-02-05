# Connect to SharePoint and Download SOPs + Template
# Run this script in PowerShell

Import-Module PnP.PowerShell -ErrorAction Stop

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$SOPPath = "C:\Users\tewing\Desktop\Holding\SOP\SharePoint-SOPs"
$TemplatePath = "C:\Users\tewing\Desktop\Holding\SOP\Templates"

# Create folders
if (-not (Test-Path $SOPPath)) { New-Item -ItemType Directory -Path $SOPPath -Force | Out-Null }
if (-not (Test-Path $TemplatePath)) { New-Item -ItemType Directory -Path $TemplatePath -Force | Out-Null }

# Connect
Write-Host "`n=== CONNECTING TO SHAREPOINT ===" -ForegroundColor Cyan
Write-Host "A browser window will open - sign in and close it when done." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin

# Download SOPs
Write-Host "`n=== DOWNLOADING SOPs ===" -ForegroundColor Cyan
$Files = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object {
    $_["FileLeafRef"] -like "*.docx" -and $_["FileDirRef"] -notlike "*Templates*"
}

Write-Host "Found $($Files.Count) Word documents" -ForegroundColor Yellow

foreach ($File in $Files) {
    $FileName = $File["FileLeafRef"]
    $ServerRelativeUrl = $File["FileRef"]
    Write-Host "  Downloading: $FileName" -ForegroundColor Gray
    Get-PnPFile -Url $ServerRelativeUrl -Path $SOPPath -FileName $FileName -AsFile -Force
}

# Download Templates
Write-Host "`n=== DOWNLOADING TEMPLATES ===" -ForegroundColor Cyan
try {
    $TemplateFiles = Get-PnPFolderItem -FolderSiteRelativeUrl "Standard Operating Procedures/Templates" -ItemType File
    foreach ($File in $TemplateFiles) {
        Write-Host "  Downloading: $($File.Name)" -ForegroundColor Gray
        Get-PnPFile -Url $File.ServerRelativeUrl -Path $TemplatePath -FileName $File.Name -AsFile -Force
    }
} catch {
    Write-Host "  Could not access Templates folder: $_" -ForegroundColor Yellow
}

Write-Host "`n=== COMPLETE ===" -ForegroundColor Green
Write-Host "SOPs saved to: $SOPPath" -ForegroundColor White
Write-Host "Templates saved to: $TemplatePath" -ForegroundColor White
Write-Host "`nFile counts:" -ForegroundColor Cyan
Write-Host "  SOPs: $((Get-ChildItem $SOPPath -Filter *.docx).Count)" -ForegroundColor White
Write-Host "  Templates: $((Get-ChildItem $TemplatePath -Filter *.docx).Count)" -ForegroundColor White
