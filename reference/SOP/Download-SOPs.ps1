# Download SOP files from SharePoint for revision
Import-Module SharePointPnPPowerShellOnline -ErrorAction Stop -WarningAction SilentlyContinue

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LocalFolder = "C:\Users\tewing\Desktop\Claude Projects\SOP_Revisions"

# Create local folder if not exists
if (-not (Test-Path $LocalFolder)) {
    New-Item -ItemType Directory -Path $LocalFolder -Force | Out-Null
}

# SOP file patterns to download (using the SOP numbers as search patterns)
$SOPPatterns = @(
    "9.2.060",
    "9.2.070",
    "9.2.080",
    "9.2.090",
    "9.2.100",
    "9.2.110",
    "9.2.120",
    "9.2.130",
    "9.2.140",
    "9.3.050",
    "9.3.060",
    "9.3.070",
    "9.3.080",
    "9.3.090",
    "9.3.100",
    "9.3.110",
    "9.3.120",
    "9.3.470",
    "9.4.010"
)

Write-Host "=== Downloading SOP Files from SharePoint ===" -ForegroundColor Cyan
Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow

Connect-PnPOnline -Url $SiteUrl -UseWebLogin

Write-Host "Connected. Getting file list..." -ForegroundColor Green

$downloaded = 0
$errors = @()

# Get all files in the library
$allFiles = Get-PnPFolderItem -FolderSiteRelativeUrl "Standard Operating Procedures" -ItemType File

Write-Host "Found $($allFiles.Count) files in library" -ForegroundColor Gray

foreach ($pattern in $SOPPatterns) {
    # Find file matching the SOP number pattern
    $matchingFile = $allFiles | Where-Object { $_.Name -like "$pattern*" } | Select-Object -First 1

    if ($matchingFile) {
        try {
            Get-PnPFile -Url $matchingFile.ServerRelativeUrl -Path $LocalFolder -Filename $matchingFile.Name -AsFile -Force
            Write-Host "  Downloaded: $($matchingFile.Name)" -ForegroundColor Green
            $downloaded++
        }
        catch {
            Write-Host "  Error downloading $($matchingFile.Name): $_" -ForegroundColor Red
            $errors += $pattern
        }
    }
    else {
        Write-Host "  Not found: $pattern" -ForegroundColor Yellow
        $errors += $pattern
    }
}

Write-Host ""
Write-Host "=== Download Complete ===" -ForegroundColor Cyan
Write-Host "Downloaded: $downloaded files" -ForegroundColor Green
if ($errors.Count -gt 0) {
    Write-Host "Not Found: $($errors.Count)" -ForegroundColor Yellow
    $errors | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
}

# List downloaded files
Write-Host ""
Write-Host "Files in local folder:" -ForegroundColor Cyan
Get-ChildItem $LocalFolder -Filter "*.docx" | Select-Object Name

Disconnect-PnPOnline
