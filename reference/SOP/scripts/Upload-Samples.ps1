# Upload 3 Sample SOPs to SharePoint

Import-Module PnP.PowerShell -ErrorAction Stop

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$RevisedPath = "C:\Users\tewing\Desktop\Holding\SOP\Revised-SOPs"

Write-Host "`n=== CONNECTING TO SHAREPOINT ===" -ForegroundColor Cyan
Connect-PnPOnline -Url $SiteUrl -UseWebLogin

# Get 3 specific sample files
$samples = @("9.2.010", "9.2.015", "9.4.360")

Write-Host "`n=== UPLOADING 3 SAMPLE SOPs ===" -ForegroundColor Cyan
foreach ($sample in $samples) {
    $file = Get-ChildItem -Path $RevisedPath -Filter "$sample*" | Select-Object -First 1
    if ($file) {
        try {
            Add-PnPFile -Path $file.FullName -Folder $LibraryName -ErrorAction Stop | Out-Null
            Write-Host "  [OK] $($file.Name)" -ForegroundColor Green
        } catch {
            Write-Host "  [FAILED] $($file.Name) - $_" -ForegroundColor Red
        }
    } else {
        Write-Host "  [NOT FOUND] $sample" -ForegroundColor Yellow
    }
}

Write-Host "`n=== COMPLETE ===" -ForegroundColor Green
