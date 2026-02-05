# Connect and Upload All Revised SOPs to SharePoint

Import-Module PnP.PowerShell -ErrorAction Stop

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$RevisedPath = "C:\Users\tewing\Desktop\Holding\SOP\Revised-SOPs"

# Connect
Write-Host "`n=== CONNECTING TO SHAREPOINT ===" -ForegroundColor Cyan
Write-Host "A browser window will open - sign in and close it when done." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin

# Get files
$Files = Get-ChildItem -Path $RevisedPath -Filter "*.docx"
Write-Host "`n=== UPLOADING $($Files.Count) SOPs ===" -ForegroundColor Cyan

$success = 0
$failed = 0

foreach ($File in $Files) {
    try {
        Write-Host "  Uploading: $($File.Name)" -ForegroundColor Gray
        Add-PnPFile -Path $File.FullName -Folder $LibraryName -ErrorAction Stop | Out-Null
        $success++
    } catch {
        Write-Host "  FAILED: $($File.Name) - $_" -ForegroundColor Red
        $failed++
    }
}

Write-Host "`n=== COMPLETE ===" -ForegroundColor Green
Write-Host "  Uploaded: $success" -ForegroundColor White
Write-Host "  Failed: $failed" -ForegroundColor White
