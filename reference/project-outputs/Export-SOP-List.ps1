<#
.SYNOPSIS
    Export list of all SOP file names to Excel/CSV
#>

$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"
$OutputFile = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs\SOP_File_List.csv"

$enDash = [char]0x2013

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Export SOP File List" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Get all SOP files
$files = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" | Sort-Object Name

Write-Host "Found $($files.Count) SOP files`n" -ForegroundColor Cyan

# Create results array
$results = @()

foreach ($file in $files) {
    # Extract SOP ID from filename
    $sopId = ""
    if ($file.Name -match "^([\d\.]+)") {
        $sopId = $Matches[1].TrimEnd('.')
    }

    # Extract title (everything after the dash)
    $title = $file.BaseName
    # Replace en-dash with regular dash for splitting
    $normalized = $title.Replace($enDash, '-')
    $parts = $normalized -split ' - ', 2
    if ($parts.Count -gt 1) {
        $title = $parts[1].Trim()
    }

    $results += [PSCustomObject]@{
        "SOP ID" = $sopId
        "File Name" = $file.Name
        "Title" = $title
    }
}

# Export to CSV
$results | Export-Csv -Path $OutputFile -NoTypeInformation -Encoding UTF8

Write-Host "Exported to: $OutputFile" -ForegroundColor Green
Write-Host "Total SOPs: $($results.Count)" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

# Display preview
Write-Host "Preview:" -ForegroundColor Yellow
$results | Select-Object -First 20 | Format-Table -AutoSize

Read-Host "`nPress Enter to close"
