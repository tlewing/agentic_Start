<#
.SYNOPSIS
    Rename local SOP files to match SharePoint SOP File Name exactly
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Rename Local Files to Match SharePoint" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Get all SharePoint items with their metadata
Write-Host "Getting SharePoint items..." -ForegroundColor Yellow
$spItems = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
Write-Host "Found $($spItems.Count) files in SharePoint`n" -ForegroundColor Cyan

# Build a lookup by SOP ID -> SOP File Name
$sopFileNames = @{}

foreach ($item in $spItems) {
    $fileName = $item.FieldValues["FileLeafRef"]
    $sopFileName = $item.FieldValues["SOPFileName"]

    # Extract SOP ID from filename
    if ($fileName -match "^([\d\.]+)") {
        $sopId = $Matches[1].TrimEnd('.')

        if ($sopFileName -and -not $sopFileNames.ContainsKey($sopId)) {
            $sopFileNames[$sopId] = $sopFileName
        }
    }
}

Write-Host "Found $($sopFileNames.Count) unique SOP IDs with file names`n" -ForegroundColor Cyan

# Get local files
Write-Host "Getting local files..." -ForegroundColor Yellow
$localFiles = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" -ErrorAction SilentlyContinue
Write-Host "Found $($localFiles.Count) local files`n" -ForegroundColor Cyan

$renamed = 0
$skipped = 0
$notFound = 0
$alreadyCorrect = 0

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Renaming Local Files" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Yellow

foreach ($file in $localFiles) {
    $currentName = $file.Name

    # Extract SOP ID from current filename
    if ($currentName -match "^([\d\.]+)") {
        $sopId = $Matches[1].TrimEnd('.')

        if ($sopFileNames.ContainsKey($sopId)) {
            $targetName = $sopFileNames[$sopId] + ".docx"

            if ($currentName -eq $targetName) {
                $alreadyCorrect++
                continue
            }

            Write-Host "----------------------------------------" -ForegroundColor DarkGray
            Write-Host "Current: $currentName" -ForegroundColor White
            Write-Host "Target:  $targetName" -ForegroundColor Cyan

            $targetPath = Join-Path $LocalSOPPath $targetName

            if (Test-Path $targetPath) {
                Write-Host "  [SKIP] Target already exists" -ForegroundColor Yellow
                $skipped++
                continue
            }

            try {
                Rename-Item -Path $file.FullName -NewName $targetName -ErrorAction Stop
                Write-Host "  [RENAMED]" -ForegroundColor Green
                $renamed++
            }
            catch {
                Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
            }
        }
        else {
            Write-Host "No SharePoint match for SOP ID: $sopId ($currentName)" -ForegroundColor Yellow
            $notFound++
        }
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Renamed: $renamed" -ForegroundColor Green
Write-Host "  Already Correct: $alreadyCorrect" -ForegroundColor Green
Write-Host "  Skipped (exists): $skipped" -ForegroundColor Yellow
Write-Host "  No SP Match: $notFound" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
