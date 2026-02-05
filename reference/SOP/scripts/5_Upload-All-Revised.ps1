# Upload all revised SOPs back to SharePoint
# Run 1_Connect-SharePoint.ps1 first

$LibraryName = "Standard Operating Procedures"
$RevisedPath = "C:\Users\tewing\Desktop\Holding\SOP\Revised-SOPs"

if (-not (Test-Path $RevisedPath)) {
    Write-Host "ERROR: Revised folder not found: $RevisedPath" -ForegroundColor Red
    Write-Host "Create this folder and place revised SOPs there before running." -ForegroundColor Yellow
    exit 1
}

$Files = Get-ChildItem -Path $RevisedPath -Filter "*.docx"

if ($Files.Count -eq 0) {
    Write-Host "No .docx files found in $RevisedPath" -ForegroundColor Yellow
    exit 0
}

Write-Host "Uploading $($Files.Count) revised SOPs to SharePoint..." -ForegroundColor Cyan

foreach ($File in $Files) {
    Write-Host "  Uploading: $($File.Name)" -ForegroundColor Gray
    Add-PnPFile -Path $File.FullName -Folder $LibraryName -ErrorAction Stop
}

Write-Host "`nUpload complete!" -ForegroundColor Green
