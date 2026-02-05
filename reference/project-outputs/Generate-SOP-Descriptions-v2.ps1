<#
.SYNOPSIS
    Generate descriptions for each SOP by reading document content
#>

$LocalSOPPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"
$OutputFile = "C:\Users\tewing\Desktop\Claude Projects\Project Outputs\SOP_Descriptions_Full.csv"

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

        # Get text content (first 3000 characters for better context)
        $fullText = $doc.Content.Text
        $preview = if ($fullText.Length -gt 3000) { $fullText.Substring(0, 3000) } else { $fullText }

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
        $title = $file.BaseName
        $enDash = [char]0x2013
        $normalized = $title.Replace($enDash, '-')
        $parts = $normalized -split ' - ', 2
        if ($parts.Count -gt 1) {
            $title = $parts[1].Trim()
        }

        # Try to find purpose/description in the document
        $description = ""

        # Look for Purpose section (various formats)
        if ($fullText -match "Purpose\s*[:\-]?\s*([^\.]+\.[^\.]*\.?)") {
            $description = $Matches[1].Trim()
        }
        elseif ($fullText -match "PURPOSE\s*[:\-]?\s*([^\.]+\.[^\.]*\.?)") {
            $description = $Matches[1].Trim()
        }
        elseif ($fullText -match "Overview\s*[:\-]?\s*([^\.]+\.[^\.]*\.?)") {
            $description = $Matches[1].Trim()
        }
        elseif ($fullText -match "Objective\s*[:\-]?\s*([^\.]+\.[^\.]*\.?)") {
            $description = $Matches[1].Trim()
        }
        elseif ($fullText -match "This (?:SOP|procedure|document)\s+([^\.]+\.)") {
            $description = "This procedure " + $Matches[1].Trim()
        }
        else {
            # Use first meaningful sentence after header content
            $sentences = $preview -split '\.' | Where-Object {
                $_.Trim().Length -gt 30 -and
                $_ -notmatch "^[\d\s\-]+$" -and
                $_ -notmatch "Department:" -and
                $_ -notmatch "Version:" -and
                $_ -notmatch "Effective Date:" -and
                $_ -notmatch "Created by:" -and
                $_ -notmatch "Related SOPs:"
            }
            if ($sentences.Count -gt 0) {
                $description = $sentences[0].Trim() + "."
            }
        }

        # Clean up description
        $description = $description -replace "\s+", " "
        $description = $description -replace "^[\s\-:]+", ""
        $description = $description.Trim()

        # Limit description length to 255 characters (SharePoint single line limit)
        if ($description.Length -gt 250) {
            $description = $description.Substring(0, 247) + "..."
        }

        $doc.Close($false)

        $results += [PSCustomObject]@{
            SOPID = $sopId
            Title = $title
            FileName = $file.Name
            Description = $description
        }

        # Show preview of description
        $shortDesc = if ($description.Length -gt 70) { $description.Substring(0, 67) + "..." } else { $description }
        Write-Host "  -> $shortDesc" -ForegroundColor Gray
    }
    catch {
        Write-Host "  [ERROR] $($_.Exception.Message)" -ForegroundColor Red
        $results += [PSCustomObject]@{
            SOPID = $sopId
            Title = $file.BaseName
            FileName = $file.Name
            Description = "Error reading file"
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

Read-Host "Press Enter to close"
