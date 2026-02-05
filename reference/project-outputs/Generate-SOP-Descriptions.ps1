<#
.SYNOPSIS
    Generate descriptions for each SOP by reading document content
#>

$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"
$OutputFile = "C:\Users\tewing\Desktop\Claude Projects\Project Outputs\SOP_Descriptions.csv"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Generate SOP Descriptions" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Get all SOP files
$files = Get-ChildItem -Path $LocalSOPPath -Filter "*.docx" | Sort-Object Name
Write-Host "Found $($files.Count) SOP files`n" -ForegroundColor Cyan

# Create Word application
Write-Host "Starting Word application..." -ForegroundColor Yellow
$word = New-Object -ComObject Word.Application
$word.Visible = $false

$results = @()
$count = 0

foreach ($file in $files) {
    $count++
    Write-Host "[$count/$($files.Count)] Processing: $($file.Name)" -ForegroundColor White

    try {
        # Open document
        $doc = $word.Documents.Open($file.FullName, $false, $true)

        # Get text content (first 2000 characters)
        $fullText = $doc.Content.Text
        $preview = if ($fullText.Length -gt 2000) { $fullText.Substring(0, 2000) } else { $fullText }

        # Clean up text
        $preview = $preview -replace "`r`n", " "
        $preview = $preview -replace "`n", " "
        $preview = $preview -replace "`r", " "
        $preview = $preview -replace "\s+", " "
        $preview = $preview.Trim()

        # Extract SOP ID from filename
        $sopId = ""
        if ($file.Name -match "^([\d\.]+)") {
            $sopId = $Matches[1].TrimEnd('.')
        }

        # Extract title from filename
        $title = $file.BaseName -replace "^[\d\.]+ - ", ""

        # Try to find purpose/description in the document
        $description = ""

        # Look for Purpose section
        if ($fullText -match "Purpose[:\s]*([^\.]+\.)" ) {
            $description = $Matches[1].Trim()
        }
        elseif ($fullText -match "Overview[:\s]*([^\.]+\.)") {
            $description = $Matches[1].Trim()
        }
        elseif ($fullText -match "Objective[:\s]*([^\.]+\.)") {
            $description = $Matches[1].Trim()
        }
        else {
            # Use first meaningful sentence
            $sentences = $preview -split '\.' | Where-Object { $_.Trim().Length -gt 20 }
            if ($sentences.Count -gt 0) {
                $description = $sentences[0].Trim() + "."
            }
        }

        # Limit description length
        if ($description.Length -gt 500) {
            $description = $description.Substring(0, 497) + "..."
        }

        $doc.Close($false)

        $results += [PSCustomObject]@{
            SOPID = $sopId
            Title = $title
            FileName = $file.Name
            Description = $description
            ContentPreview = $preview.Substring(0, [Math]::Min(500, $preview.Length))
        }

        Write-Host "  Description: $($description.Substring(0, [Math]::Min(80, $description.Length)))..." -ForegroundColor Gray
    }
    catch {
        Write-Host "  [ERROR] $($_.Exception.Message)" -ForegroundColor Red
        $results += [PSCustomObject]@{
            SOPID = $sopId
            Title = $file.BaseName
            FileName = $file.Name
            Description = "Error reading file"
            ContentPreview = ""
        }
    }
}

# Close Word
$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null

# Export to CSV
Write-Host "`nExporting to CSV..." -ForegroundColor Yellow
$results | Export-Csv -Path $OutputFile -NoTypeInformation -Encoding UTF8

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Complete!" -ForegroundColor Green
Write-Host "  Output: $OutputFile" -ForegroundColor Green
Write-Host "  Total SOPs: $($results.Count)" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

# Also display summary
Write-Host "SOP Descriptions Summary:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$results | ForEach-Object {
    Write-Host "`n$($_.SOPID) - $($_.Title)" -ForegroundColor Yellow
    Write-Host "  $($_.Description)" -ForegroundColor White
}

Read-Host "`nPress Enter to close"
