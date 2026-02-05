# Upload Revised SOP files to SharePoint
Import-Module SharePointPnPPowerShellOnline -ErrorAction Stop -WarningAction SilentlyContinue

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalFolder = "C:\Users\tewing\Desktop\Claude Projects\SOP_Revisions\Revised"

Write-Host "=== Uploading Revised SOP Files to SharePoint ===" -ForegroundColor Cyan
Write-Host "Source: $LocalFolder"
Write-Host "Destination: $SiteUrl/$LibraryName"
Write-Host ""

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin
Write-Host "Connected." -ForegroundColor Green

$uploaded = 0
$errors = @()

# Get all docx files in the local folder
$files = Get-ChildItem $LocalFolder -Filter "*.docx"
Write-Host "Found $($files.Count) files to upload" -ForegroundColor Gray

foreach ($file in $files) {
    try {
        Write-Host "  Uploading: $($file.Name)..." -ForegroundColor Gray

        # Upload file (will overwrite if exists)
        Add-PnPFile -Path $file.FullName -Folder $LibraryName -ErrorAction Stop | Out-Null

        Write-Host "    Uploaded: $($file.Name)" -ForegroundColor Green
        $uploaded++
    }
    catch {
        Write-Host "    Error: $($file.Name) - $_" -ForegroundColor Red
        $errors += $file.Name
    }
}

Write-Host ""
Write-Host "=== Upload Complete ===" -ForegroundColor Cyan
Write-Host "Uploaded: $uploaded files" -ForegroundColor Green
if ($errors.Count -gt 0) {
    Write-Host "Errors: $($errors.Count)" -ForegroundColor Red
    $errors | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
}

Disconnect-PnPOnline
