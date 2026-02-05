# Download SOPs from SharePoint
# Run 1_Connect-SharePoint.ps1 first

$LibraryName = "Standard Operating Procedures"
$LocalPath = "C:\Users\tewing\Desktop\Holding\SOP\SharePoint-SOPs"

# Create local folder if it doesn't exist
if (-not (Test-Path $LocalPath)) {
    New-Item -ItemType Directory -Path $LocalPath -Force | Out-Null
    Write-Host "Created folder: $LocalPath" -ForegroundColor Green
}

Write-Host "Downloading SOPs from SharePoint..." -ForegroundColor Cyan

# Get all files from the library
$Files = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_["FileLeafRef"] -like "*.docx" }

Write-Host "Found $($Files.Count) Word documents" -ForegroundColor Yellow

foreach ($File in $Files) {
    $FileName = $File["FileLeafRef"]
    $ServerRelativeUrl = $File["FileRef"]
    $LocalFilePath = Join-Path $LocalPath $FileName

    Write-Host "  Downloading: $FileName" -ForegroundColor Gray
    Get-PnPFile -Url $ServerRelativeUrl -Path $LocalPath -FileName $FileName -AsFile -Force
}

Write-Host "`nDownload complete! Files saved to:" -ForegroundColor Green
Write-Host "  $LocalPath" -ForegroundColor White
