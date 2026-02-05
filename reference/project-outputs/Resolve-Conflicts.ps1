<#
.SYNOPSIS
    Resolve SOP ID conflicts by renaming and deleting files
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

$enDash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Resolve SOP ID Conflicts" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Define renames: OldPattern -> NewID, NewTitle
$renames = @(
    @{ Pattern = "9.4.575*Subcontractor Resources*"; NewId = "9.4.576"; NewTitle = "Manage Subcontractor Resources" },
    @{ Pattern = "9.5.015*Handling*Excess Materials*"; NewId = "9.5.020"; NewTitle = "Handling and or Disposing of Excess Materials" },
    @{ Pattern = "9.6.010*Project Turnover Documentation*"; NewId = "9.6.015"; NewTitle = "Manage Project Turnover Documentation" },
    @{ Pattern = "9.6.030*Submit Warranties*"; NewId = "9.6.035"; NewTitle = "Submit Warranties" },
    @{ Pattern = "9.6.060*Archive Project Documentation*"; NewId = "9.6.065"; NewTitle = "Archive Project Documentation" }
)

# Define deletions
$deletions = @(
    "9.6.050*Manage Warranties*"
)

# Connect to SharePoint
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }

# Process renames
Write-Host "Processing renames..." -ForegroundColor Yellow
foreach ($rename in $renames) {
    $targetFile = $items | Where-Object { $_.FieldValues["FileLeafRef"] -like $rename.Pattern }

    if ($targetFile) {
        $oldFileName = $targetFile.FieldValues["FileLeafRef"]
        Write-Host "`n  Found: $oldFileName" -ForegroundColor Cyan

        $newFileName = "$($rename.NewId) $enDash $($rename.NewTitle).docx"
        $newSopFileName = "$($rename.NewId) $enDash $($rename.NewTitle)"

        Write-Host "  Renaming to: $newFileName" -ForegroundColor Yellow

        try {
            $serverRelativeUrl = $targetFile.FieldValues["FileRef"]

            Rename-PnPFile -ServerRelativeUrl $serverRelativeUrl -TargetFileName $newFileName -Force -ErrorAction Stop
            Write-Host "  [FILE RENAMED]" -ForegroundColor Green

            Set-PnPListItem -List $LibraryName -Identity $targetFile.Id -Values @{
                "Title" = $rename.NewTitle
                "SOPID" = $rename.NewId
                "SOPFileName" = $newSopFileName
            } -ErrorAction SilentlyContinue | Out-Null
            Write-Host "  [METADATA UPDATED]" -ForegroundColor Green
        }
        catch {
            Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    else {
        Write-Host "`n  NOT FOUND: $($rename.Pattern)" -ForegroundColor Yellow
    }
}

# Process deletions
Write-Host "`n`nProcessing deletions..." -ForegroundColor Yellow
foreach ($pattern in $deletions) {
    $targetFile = $items | Where-Object { $_.FieldValues["FileLeafRef"] -like $pattern }

    if ($targetFile) {
        $fileName = $targetFile.FieldValues["FileLeafRef"]
        Write-Host "`n  Found: $fileName" -ForegroundColor Cyan

        try {
            Remove-PnPListItem -List $LibraryName -Identity $targetFile.Id -Force -ErrorAction Stop
            Write-Host "  [DELETED from SharePoint]" -ForegroundColor Green
        }
        catch {
            Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    else {
        Write-Host "`n  NOT FOUND: $pattern" -ForegroundColor Yellow
    }
}

Disconnect-PnPOnline

# Now process local files
Write-Host "`n`nProcessing local files..." -ForegroundColor Yellow

# Local renames
foreach ($rename in $renames) {
    $localFile = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" | Where-Object { $_.Name -like $rename.Pattern }

    if ($localFile) {
        Write-Host "`n  Found locally: $($localFile.Name)" -ForegroundColor Cyan
        $newLocalName = "$($rename.NewId) $enDash $($rename.NewTitle).docx"

        try {
            Rename-Item -Path $localFile.FullName -NewName $newLocalName -Force -ErrorAction Stop
            Write-Host "  [LOCAL RENAMED] $newLocalName" -ForegroundColor Green
        }
        catch {
            Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Local deletions
foreach ($pattern in $deletions) {
    $localFile = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" | Where-Object { $_.Name -like $pattern }

    if ($localFile) {
        Write-Host "`n  Found locally: $($localFile.Name)" -ForegroundColor Cyan

        try {
            Remove-Item -Path $localFile.FullName -Force -ErrorAction Stop
            Write-Host "  [LOCAL DELETED]" -ForegroundColor Green
        }
        catch {
            Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Read-Host "Press Enter to close"
