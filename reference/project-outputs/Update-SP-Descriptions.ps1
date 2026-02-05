<#
.SYNOPSIS
    Update SharePoint SOP metadata with descriptions
#>

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"
$DescriptionsFile = "C:\Users\tewing\Desktop\Claude Projects\Project Outputs\SOP_Descriptions_Full.csv"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Update SharePoint SOP Descriptions" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Load descriptions
$descriptions = Import-Csv -Path $DescriptionsFile
Write-Host "Loaded $($descriptions.Count) descriptions`n" -ForegroundColor Cyan

# Clean up descriptions (remove leading ===)
foreach ($d in $descriptions) {
    $d.Description = $d.Description -replace "^=+\s*", ""
    $d.Description = $d.Description.Trim()
}

# Connect to SharePoint
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
Write-Host "Connected!`n" -ForegroundColor Green

# Get list fields to check for Description field
Write-Host "Checking for Description field..." -ForegroundColor Yellow
$fields = Get-PnPField -List $LibraryName
$descField = $fields | Where-Object { $_.InternalName -eq "Description" -or $_.Title -eq "Description" }

if (-not $descField) {
    Write-Host "Description field not found. Available fields:" -ForegroundColor Yellow
    $fields | Where-Object { $_.Hidden -eq $false } | Select-Object Title, InternalName, TypeAsString | Format-Table

    Write-Host "`nWould you like to create a Description field? (The script will use 'SOPDescription' as internal name)" -ForegroundColor Yellow
}
else {
    Write-Host "Found Description field: $($descField.InternalName)" -ForegroundColor Green
}

# Get all items
$items = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object { $_.FileSystemObjectType -eq "File" }
Write-Host "Found $($items.Count) files in SharePoint`n" -ForegroundColor Cyan

# Build lookup by filename
$itemLookup = @{}
foreach ($item in $items) {
    $fileName = $item.FieldValues["FileLeafRef"]
    $itemLookup[$fileName] = $item
}

# Update descriptions
$updated = 0
$failed = 0
$notFound = 0

foreach ($desc in $descriptions) {
    $fileName = $desc.FileName

    if ($itemLookup.ContainsKey($fileName)) {
        $item = $itemLookup[$fileName]

        # Clean description
        $cleanDesc = $desc.Description -replace "^=+\s*", ""
        $cleanDesc = $cleanDesc.Trim()

        if ($cleanDesc.Length -gt 0) {
            try {
                # Try updating with different possible field names
                $updateValues = @{}

                # Check which field exists and use it
                if ($descField) {
                    $updateValues[$descField.InternalName] = $cleanDesc
                }
                else {
                    # Try common field names
                    $updateValues["Description0"] = $cleanDesc
                }

                Set-PnPListItem -List $LibraryName -Identity $item.Id -Values $updateValues -ErrorAction Stop | Out-Null
                Write-Host "[UPDATED] $($desc.SOPID) - $($desc.Title)" -ForegroundColor Green
                $updated++
            }
            catch {
                # Try alternate field name
                try {
                    Set-PnPListItem -List $LibraryName -Identity $item.Id -Values @{
                        "Comments" = $cleanDesc
                    } -ErrorAction Stop | Out-Null
                    Write-Host "[UPDATED via Comments] $($desc.SOPID)" -ForegroundColor Green
                    $updated++
                }
                catch {
                    Write-Host "[FAILED] $($desc.SOPID): $($_.Exception.Message)" -ForegroundColor Red
                    $failed++
                }
            }
        }
    }
    else {
        # Try to find by pattern match
        $matchedItem = $items | Where-Object {
            $_.FieldValues["FileLeafRef"] -like "$($desc.SOPID)*"
        } | Select-Object -First 1

        if ($matchedItem) {
            $cleanDesc = $desc.Description -replace "^=+\s*", ""
            $cleanDesc = $cleanDesc.Trim()

            if ($cleanDesc.Length -gt 0) {
                try {
                    if ($descField) {
                        Set-PnPListItem -List $LibraryName -Identity $matchedItem.Id -Values @{
                            $descField.InternalName = $cleanDesc
                        } -ErrorAction Stop | Out-Null
                    }
                    Write-Host "[UPDATED] $($desc.SOPID) (pattern match)" -ForegroundColor Green
                    $updated++
                }
                catch {
                    Write-Host "[FAILED] $($desc.SOPID): $($_.Exception.Message)" -ForegroundColor Red
                    $failed++
                }
            }
        }
        else {
            Write-Host "[NOT FOUND] $fileName" -ForegroundColor Yellow
            $notFound++
        }
    }
}

Disconnect-PnPOnline

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Complete!" -ForegroundColor Green
Write-Host "  Updated: $updated" -ForegroundColor Green
Write-Host "  Failed: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "  Not Found: $notFound" -ForegroundColor $(if ($notFound -gt 0) { "Yellow" } else { "Green" })
Write-Host "========================================`n" -ForegroundColor Green

Read-Host "Press Enter to close"
