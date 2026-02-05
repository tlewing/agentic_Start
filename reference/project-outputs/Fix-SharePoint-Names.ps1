<#
.SYNOPSIS
    Fix SharePoint file names and metadata - remove double dashes
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

$enDash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Fix SharePoint Names & Metadata" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

Write-Host "Getting SharePoint items..." -ForegroundColor Yellow
$spItems = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
Write-Host "Found $($spItems.Count) files`n" -ForegroundColor Cyan

function Clean-Text {
    param([string]$text)

    if (-not $text) { return $text }

    $t = $text

    # Replace double/triple dashes with single
    while ($t.Contains(" - - ")) { $t = $t.Replace(" - - ", " - ") }
    while ($t.Contains(" $enDash $enDash ")) { $t = $t.Replace(" $enDash $enDash ", " $enDash ") }

    # Remove leading dashes/spaces from title
    while ($t.Length -gt 0 -and ($t[0] -eq '-' -or $t[0] -eq ' ' -or $t[0] -eq $enDash)) {
        $t = $t.Substring(1)
    }

    return $t.Trim()
}

$renamed = 0
$metadataFixed = 0
$failed = 0

foreach ($item in $spItems) {
    $fileName = $item.FieldValues["FileLeafRef"]
    $sopFileName = $item.FieldValues["SOPFileName"]
    $title = $item.FieldValues["Title"]
    $serverRelUrl = $item.FieldValues["FileRef"]

    # Check if filename has double dashes
    $hasDoubleDash = $fileName.Contains(" - - ") -or $fileName.Contains(" $enDash $enDash ")

    if (-not $hasDoubleDash) { continue }

    Write-Host "----------------------------------------" -ForegroundColor DarkGray
    Write-Host "Current: $fileName" -ForegroundColor White

    # Clean up filename
    $newFileName = Clean-Text -text $fileName

    Write-Host "New:     $newFileName" -ForegroundColor Cyan

    # Clean up metadata
    $newSopFileName = Clean-Text -text $sopFileName
    $newTitle = Clean-Text -text $title

    try {
        # Rename file first
        Rename-PnPFile -ServerRelativeUrl $serverRelUrl -TargetFileName $newFileName -Force -ErrorAction Stop
        Write-Host "  [RENAMED]" -ForegroundColor Green
        $renamed++

        # Update metadata
        $updates = @{
            "SOPFileName" = $newSopFileName
            "Title" = $newTitle
        }
        Set-PnPListItem -List $LibraryName -Identity $item.Id -Values $updates -ErrorAction Stop | Out-Null
        Write-Host "  [METADATA FIXED]" -ForegroundColor Green
        $metadataFixed++
    }
    catch {
        Write-Host "  [FAILED] $($_.Exception.Message)" -ForegroundColor Red
        $failed++
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Files Renamed: $renamed" -ForegroundColor Green
Write-Host "  Metadata Fixed: $metadataFixed" -ForegroundColor Green
Write-Host "  Failed: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "========================================`n" -ForegroundColor Cyan

Disconnect-PnPOnline -ErrorAction SilentlyContinue
Read-Host "Press Enter to close"
