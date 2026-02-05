# Update Metadata for ALL SOP Documents in SharePoint Library
Import-Module SharePointPnPPowerShellOnline -ErrorAction Stop -WarningAction SilentlyContinue

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue

Write-Host "`nRetrieving all files from library..." -ForegroundColor Yellow

$items = Get-PnPListItem -List $LibraryName -Fields "FileLeafRef","FileRef","SOPID","Title","Department_x002f_Division" -PageSize 500

# Filter to .docx files only
$files = $items | Where-Object { $_["FileLeafRef"] -like "*.docx" }

Write-Host "Found $($files.Count) .docx files`n"

# Department mapping based on SOP series
function Get-Department($sopId) {
    if ($sopId -match "^9\.1\.") { return "Estimating" }
    if ($sopId -match "^9\.2\.") { return "Project Management" }
    if ($sopId -match "^9\.3\.") { return "Field Operations" }
    if ($sopId -match "^9\.4\.") { return "Project Controls" }
    if ($sopId -match "^9\.5\.") { return "Project Closeout" }
    if ($sopId -match "^9\.6\.") { return "Project Closeout" }
    return "General"
}

$updatedCount = 0
$skippedCount = 0
$errorCount = 0

foreach ($file in $files) {
    $fileName = $file["FileLeafRef"]
    $currentSOPID = $file["SOPID"]
    $currentTitle = $file["Title"]
    $currentDept = $file["Department_x002f_Division"]

    # Skip template and non-SOP files
    if ($fileName -like "*Template*" -or $fileName -like "GSL Release*") {
        Write-Host "  Skipping: $fileName" -ForegroundColor Gray
        $skippedCount++
        continue
    }

    # Extract SOP ID and Title from filename
    # Format: "9.2.060 - Create Issue List and Begin RFI Process.docx"
    if ($fileName -match "^(\d+\.\d+\.\d+)\s*[-\u2013]\s*(.+)\.docx$") {
        $extractedSOPID = $matches[1]
        $extractedTitle = $matches[2].Trim()

        $needsUpdate = $false
        $updates = @{}

        # Check if SOPID needs update
        if ([string]::IsNullOrWhiteSpace($currentSOPID)) {
            $updates["SOPID"] = $extractedSOPID
            $needsUpdate = $true
        }

        # Check if Title needs update
        if ([string]::IsNullOrWhiteSpace($currentTitle)) {
            $updates["Title"] = $extractedTitle
            $needsUpdate = $true
        }

        # Check if Department needs update
        if ([string]::IsNullOrWhiteSpace($currentDept)) {
            $dept = Get-Department $extractedSOPID
            $updates["Department_x002f_Division"] = $dept
            $needsUpdate = $true
        }

        if ($needsUpdate) {
            try {
                Write-Host "  Updating: $fileName" -ForegroundColor Cyan
                Set-PnPListItem -List $LibraryName -Identity $file.Id -Values $updates -ErrorAction Stop | Out-Null
                Write-Host "    Set: SOPID=$($updates['SOPID']), Title=$($updates['Title']), Dept=$($updates['Department_x002f_Division'])" -ForegroundColor Green
                $updatedCount++
            }
            catch {
                Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
                $errorCount++
            }
        }
        else {
            $skippedCount++
        }
    }
    else {
        Write-Host "  Could not parse: $fileName" -ForegroundColor Yellow
        $skippedCount++
    }
}

Write-Host "`n=== Metadata Update Complete ===" -ForegroundColor Green
Write-Host "Updated: $updatedCount files" -ForegroundColor Green
Write-Host "Skipped: $skippedCount files (already had metadata or non-SOP)" -ForegroundColor Gray
if ($errorCount -gt 0) {
    Write-Host "Errors: $errorCount" -ForegroundColor Red
}

Disconnect-PnPOnline
