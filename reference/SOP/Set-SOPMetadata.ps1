# Set Metadata for SOP Documents in SharePoint Library
Import-Module SharePointPnPPowerShellOnline -ErrorAction Stop -WarningAction SilentlyContinue

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "Standard Operating Procedures"

# SOP Metadata - ID, Title, Department
$SOPMetadata = @(
    @{ FileName = "9.2.060"; SOPID = "9.2.060"; Title = "Create Issue List and Begin RFI Process"; Department = "Project Management" }
    @{ FileName = "9.2.070"; SOPID = "9.2.070"; Title = "Conduct Site Visit"; Department = "Project Management" }
    @{ FileName = "9.2.080"; SOPID = "9.2.080"; Title = "Prepare Material Handling Plan"; Department = "Project Management" }
    @{ FileName = "9.2.090"; SOPID = "9.2.090"; Title = "Develop Labor Budget"; Department = "Project Management" }
    @{ FileName = "9.2.100"; SOPID = "9.2.100"; Title = "Prepare Layout and Sequencing Plan"; Department = "Project Management" }
    @{ FileName = "9.2.110"; SOPID = "9.2.110"; Title = "Develop Project Schedule"; Department = "Project Management" }
    @{ FileName = "9.2.120"; SOPID = "9.2.120"; Title = "Establish Tracking and Control Systems"; Department = "Project Management" }
    @{ FileName = "9.2.130"; SOPID = "9.2.130"; Title = "Construction Execution Kickoff Meeting"; Department = "Project Management" }
    @{ FileName = "9.2.140"; SOPID = "9.2.140"; Title = "Develop Project Budget"; Department = "Project Management" }
    @{ FileName = "9.3.050"; SOPID = "9.3.050"; Title = "Pre-Task Planning"; Department = "Field Operations" }
    @{ FileName = "9.3.060"; SOPID = "9.3.060"; Title = "Jobsite Mobilization"; Department = "Field Operations" }
    @{ FileName = "9.3.070"; SOPID = "9.3.070"; Title = "Tool and Equipment Management"; Department = "Field Operations" }
    @{ FileName = "9.3.080"; SOPID = "9.3.080"; Title = "Daily Huddles"; Department = "Field Operations" }
    @{ FileName = "9.3.090"; SOPID = "9.3.090"; Title = "Work-in-Place Tracking"; Department = "Field Operations" }
    @{ FileName = "9.3.100"; SOPID = "9.3.100"; Title = "Field Documentation"; Department = "Field Operations" }
    @{ FileName = "9.3.110"; SOPID = "9.3.110"; Title = "Quality Control Inspections"; Department = "Field Operations" }
    @{ FileName = "9.3.120"; SOPID = "9.3.120"; Title = "Jobsite Demobilization"; Department = "Field Operations" }
    @{ FileName = "9.3.470"; SOPID = "9.3.470"; Title = "Develop Site-Specific Safety Plan"; Department = "Field Operations" }
    @{ FileName = "9.4.010"; SOPID = "9.4.010"; Title = "Change Order Management"; Department = "Project Controls" }
)

Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue

Write-Host "`nSetting metadata for SOP documents..." -ForegroundColor Yellow

$successCount = 0
$errorCount = 0

foreach ($sop in $SOPMetadata) {
    # Find the file in the library
    $searchPattern = "*$($sop.FileName)*"

    try {
        # Get all files and find matching one
        $files = Get-PnPListItem -List $LibraryName -Fields "FileLeafRef", "FileRef" |
                 Where-Object { $_["FileLeafRef"] -like $searchPattern }

        if ($files) {
            foreach ($file in $files) {
                $fileName = $file["FileLeafRef"]
                Write-Host "  Updating: $fileName" -ForegroundColor Cyan

                # Set metadata values using correct internal field names
                Set-PnPListItem -List $LibraryName -Identity $file.Id -Values @{
                    "Title" = $sop.Title
                    "SOPID" = $sop.SOPID
                    "Department_x002f_Division" = $sop.Department
                } -ErrorAction Stop

                Write-Host "    Set: SOPID=$($sop.SOPID), Title=$($sop.Title), Dept=$($sop.Department)" -ForegroundColor Green
                $successCount++
            }
        } else {
            Write-Host "  File not found matching: $searchPattern" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "  Error updating $($sop.FileName): $($_.Exception.Message)" -ForegroundColor Red
        $errorCount++
    }
}

Write-Host "`n=== Metadata Update Complete ===" -ForegroundColor Green
Write-Host "Success: $successCount" -ForegroundColor Green
if ($errorCount -gt 0) {
    Write-Host "Errors: $errorCount" -ForegroundColor Red
}

Disconnect-PnPOnline
