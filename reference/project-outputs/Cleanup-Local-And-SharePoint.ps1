<#
.SYNOPSIS
    1. Delete local duplicate files
    2. Fix SharePoint SOP File Name metadata (remove double dashes)
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

$enDash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Cleanup Local Files & SharePoint" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# ========================================
# PART 1: Delete local duplicate files
# ========================================

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Part 1: Delete Local Duplicates" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Yellow

$localFiles = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" -ErrorAction SilentlyContinue
Write-Host "Found $($localFiles.Count) local files" -ForegroundColor Cyan

# Find files to delete (triple dashes, double dashes, or known duplicates)
$localToDelete = @()

foreach ($file in $localFiles) {
    $name = $file.Name

    # Check for triple or double dashes
    $hasTriple = $name.Contains(" - - - ") -or $name.Contains(" $enDash $enDash $enDash ")
    $hasDouble = $name.Contains(" - - ") -or $name.Contains(" $enDash $enDash ")

    if ($hasTriple -or $hasDouble) {
        $localToDelete += $file
    }
}

Write-Host "Found $($localToDelete.Count) files with extra dashes to delete`n" -ForegroundColor Yellow

$localDeleted = 0
foreach ($file in $localToDelete) {
    Write-Host "Deleting: $($file.Name)" -ForegroundColor Red
    try {
        Remove-Item -Path $file.FullName -Force -ErrorAction Stop
        Write-Host "  [DELETED]" -ForegroundColor Green
        $localDeleted++
    }
    catch {
        Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nLocal files deleted: $localDeleted" -ForegroundColor Green

# ========================================
# PART 2: Fix SharePoint SOP File Name
# ========================================

Write-Host "`n========================================" -ForegroundColor Yellow
Write-Host "  Part 2: Fix SharePoint Metadata" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Yellow

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

Write-Host "Getting SharePoint items..." -ForegroundColor Yellow
$spItems = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
Write-Host "Found $($spItems.Count) files`n" -ForegroundColor Cyan

$spFixed = 0

foreach ($item in $spItems) {
    $fileName = $item.FieldValues["FileLeafRef"]
    $sopFileName = $item.FieldValues["SOPFileName"]
    $title = $item.FieldValues["Title"]

    $needsUpdate = $false
    $newSopFileName = $sopFileName
    $newTitle = $title

    # Fix SOPFileName - remove double/triple dashes
    if ($sopFileName) {
        $fixed = $sopFileName
        # Replace double dashes with single
        while ($fixed.Contains(" - - ") -or $fixed.Contains(" $enDash $enDash ")) {
            $fixed = $fixed.Replace(" - - ", " - ").Replace(" $enDash $enDash ", " $enDash ")
        }
        if ($fixed -ne $sopFileName) {
            $newSopFileName = $fixed
            $needsUpdate = $true
        }
    }

    # Fix Title - remove any leading dashes
    if ($title) {
        $fixedTitle = $title
        # Remove leading dashes and spaces
        while ($fixedTitle.StartsWith("-") -or $fixedTitle.StartsWith(" ") -or $fixedTitle.StartsWith($enDash)) {
            $fixedTitle = $fixedTitle.TrimStart('-', ' ', $enDash)
        }
        if ($fixedTitle -ne $title) {
            $newTitle = $fixedTitle
            $needsUpdate = $true
        }
    }

    if ($needsUpdate) {
        Write-Host "----------------------------------------" -ForegroundColor DarkGray
        Write-Host "File: $fileName" -ForegroundColor White
        if ($newSopFileName -ne $sopFileName) {
            Write-Host "  SOPFileName: '$sopFileName' -> '$newSopFileName'" -ForegroundColor Cyan
        }
        if ($newTitle -ne $title) {
            Write-Host "  Title: '$title' -> '$newTitle'" -ForegroundColor Cyan
        }

        try {
            $updates = @{}
            if ($newSopFileName -ne $sopFileName) { $updates["SOPFileName"] = $newSopFileName }
            if ($newTitle -ne $title) { $updates["Title"] = $newTitle }

            Set-PnPListItem -List $LibraryName -Identity $item.Id -Values $updates -ErrorAction Stop | Out-Null
            Write-Host "  [FIXED]" -ForegroundColor Green
            $spFixed++
        }
        catch {
            Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Local files deleted: $localDeleted" -ForegroundColor Green
Write-Host "  SharePoint items fixed: $spFixed" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
