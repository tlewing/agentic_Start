<#
.SYNOPSIS
    Update SharePoint SOP metadata with descriptions - cleaned version
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$DescriptionsFile = "C:\Users\tewing\Desktop\Claude Projects\Project Outputs\SOP_Descriptions_Full.csv"

$enDash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Update SharePoint SOP Descriptions" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Function to clean text of control characters
function Clean-Text {
    param([string]$text)

    if ([string]::IsNullOrEmpty($text)) { return "" }

    # Remove control characters (0x00-0x1F except tab, newline, carriage return)
    $cleaned = $text -replace '[\x00-\x08\x0B\x0C\x0E-\x1F]', ''

    # Remove leading/trailing whitespace and equals signs
    $cleaned = $cleaned -replace "^[=\s]+", ""
    $cleaned = $cleaned -replace "[=\s]+$", ""

    # Replace multiple spaces with single space
    $cleaned = $cleaned -replace '\s+', ' '

    return $cleaned.Trim()
}

# Load descriptions
$descriptions = Import-Csv -Path $DescriptionsFile
Write-Host "Loaded $($descriptions.Count) descriptions`n" -ForegroundColor Cyan

# Connect to SharePoint
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Get all items
$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
Write-Host "Found $($items.Count) files in SharePoint`n" -ForegroundColor Cyan

# Update descriptions
$updated = 0
$failed = 0
$skipped = 0

foreach ($desc in $descriptions) {
    $sopId = $desc.SOPID

    # Find item by SOP ID pattern
    $item = $items | Where-Object {
        $fileName = $_.FieldValues["FileLeafRef"]
        $fileName -like "$sopId*" -or $fileName -like "$sopId -*" -or $fileName -like "$sopId $enDash*"
    } | Select-Object -First 1

    if ($item) {
        # Clean description
        $cleanDesc = Clean-Text $desc.Description

        if ($cleanDesc.Length -gt 5 -and $cleanDesc -ne "Error reading file") {
            # Truncate if too long (SharePoint limit)
            if ($cleanDesc.Length -gt 255) {
                $cleanDesc = $cleanDesc.Substring(0, 252) + "..."
            }

            try {
                Set-PnPListItem -List $LibraryName -Identity $item.Id -Values @{
                    "Description" = $cleanDesc
                } -ErrorAction Stop | Out-Null

                Write-Host "[UPDATED] $sopId" -ForegroundColor Green
                $updated++
            }
            catch {
                Write-Host "[FAILED] $sopId - $($_.Exception.Message)" -ForegroundColor Red
                $failed++
            }
        }
        else {
            Write-Host "[SKIPPED] $sopId - Empty/invalid description" -ForegroundColor Yellow
            $skipped++
        }
    }
    else {
        Write-Host "[NOT FOUND] $sopId" -ForegroundColor Yellow
        $failed++
    }
}

Disconnect-PnPOnline

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Complete!" -ForegroundColor Green
Write-Host "  Updated: $updated" -ForegroundColor Green
Write-Host "  Skipped: $skipped" -ForegroundColor Yellow
Write-Host "  Failed: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "========================================`n" -ForegroundColor Green

Read-Host "Press Enter to close"
