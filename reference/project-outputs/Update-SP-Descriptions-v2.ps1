<#
.SYNOPSIS
    Update SharePoint SOP metadata with descriptions
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$DescriptionsFile = "C:\Users\tewing\Desktop\Claude Projects\Project Outputs\SOP_Descriptions_Full.csv"

$enDash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Update SharePoint SOP Descriptions" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

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

foreach ($desc in $descriptions) {
    $sopId = $desc.SOPID

    # Find item by SOP ID pattern
    $item = $items | Where-Object {
        $fileName = $_.FieldValues["FileLeafRef"]
        $fileName -like "$sopId*" -or $fileName -like "$sopId -*" -or $fileName -like "$sopId $enDash*"
    } | Select-Object -First 1

    if ($item) {
        # Clean description
        $cleanDesc = $desc.Description -replace "^=+\s*", ""
        $cleanDesc = $cleanDesc.Trim()

        if ($cleanDesc.Length -gt 0 -and $cleanDesc -ne "Error reading file") {
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
            Write-Host "[SKIPPED] $sopId - Empty description" -ForegroundColor Yellow
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
Write-Host "  Failed/Skipped: $failed" -ForegroundColor $(if ($failed -gt 0) { "Yellow" } else { "Green" })
Write-Host "========================================`n" -ForegroundColor Green

Read-Host "Press Enter to close"
