# Sync Excel Coverage Matrix to SharePoint List
# Uses Legacy SharePointPnPPowerShellOnline module (supports web login)

param(
    [string]$ExcelPath = "C:\Users\tewing\Desktop\Claude Projects\Key_SOP_Matrix_RACI_Updated.xlsx",
    [string]$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures",
    [string]$ListName = "Key_SOP_Matrix"
)

# Import required module
Import-Module SharePointPnPPowerShellOnline -ErrorAction Stop -WarningAction SilentlyContinue

Write-Host "=== Excel to SharePoint Sync ===" -ForegroundColor Cyan
Write-Host "Source: $ExcelPath"
Write-Host "Destination: $SiteUrl"
Write-Host "List: $ListName"
Write-Host ""

# Read Excel file using COM object
Write-Host "Reading Excel file..." -ForegroundColor Yellow
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false

try {
    $workbook = $excel.Workbooks.Open($ExcelPath)
    $worksheet = $workbook.Worksheets.Item("Coverage Matrix")

    # Get the used range
    $usedRange = $worksheet.UsedRange
    $rowCount = $usedRange.Rows.Count
    $colCount = $usedRange.Columns.Count

    Write-Host "Found $($rowCount - 1) data rows in Coverage Matrix" -ForegroundColor Green

    # Read headers (row 1)
    $headers = @{}
    for ($col = 1; $col -le $colCount; $col++) {
        $headerValue = $worksheet.Cells.Item(1, $col).Text
        $headers[$headerValue] = $col
    }

    Write-Host "Columns found: $($headers.Keys -join ', ')"

    # Build data array
    $data = @()
    for ($row = 2; $row -le $rowCount; $row++) {
        $item = @{
            Title = $worksheet.Cells.Item($row, $headers["SOP Title"]).Text
            field_1 = $worksheet.Cells.Item($row, $headers["SOP Action"]).Text
            field_2 = $worksheet.Cells.Item($row, $headers["Responsible Role"]).Text
            field_3 = $worksheet.Cells.Item($row, $headers["Directive Section"]).Text
            field_4 = $worksheet.Cells.Item($row, $headers["Coverage Status"]).Text
            field_5 = $worksheet.Cells.Item($row, $headers["Gap Closure Recommendation"]).Text
            field_6 = $worksheet.Cells.Item($row, $headers["Category"]).Text
        }
        $data += $item

        if ($row % 50 -eq 0) {
            Write-Host "  Read $row rows..." -ForegroundColor Gray
        }
    }

    Write-Host "Read $($data.Count) items from Excel" -ForegroundColor Green
}
finally {
    $workbook.Close($false)
    $excel.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($worksheet) | Out-Null
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($workbook) | Out-Null
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}

# Connect to SharePoint using web login (browser-based auth with MFA support)
Write-Host ""
Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
Write-Host "A browser window will open - please sign in to your SharePoint account" -ForegroundColor Magenta

Connect-PnPOnline -Url $SiteUrl -UseWebLogin

# Verify connection
$web = Get-PnPWeb
Write-Host "Connected to: $($web.Title)" -ForegroundColor Green

# Clear existing list items
Write-Host ""
Write-Host "Clearing existing list items..." -ForegroundColor Yellow

$existingItems = Get-PnPListItem -List $ListName -PageSize 500
$existingCount = ($existingItems | Measure-Object).Count

if ($existingCount -gt 0) {
    Write-Host "Removing $existingCount existing items..."

    $removeCount = 0
    foreach ($item in $existingItems) {
        Remove-PnPListItem -List $ListName -Identity $item.Id -Force
        $removeCount++
        if ($removeCount % 50 -eq 0) {
            Write-Host "  Removed $removeCount items..." -ForegroundColor Gray
        }
    }
    Write-Host "Existing items removed" -ForegroundColor Green
} else {
    Write-Host "List is empty, nothing to clear" -ForegroundColor Gray
}

# Add new items
Write-Host ""
Write-Host "Adding $($data.Count) items to SharePoint list..." -ForegroundColor Yellow

$addedCount = 0
$errorCount = 0

foreach ($item in $data) {
    try {
        # Create hash table for the list item values
        $values = @{
            "Title" = if ($item.Title) { $item.Title.Substring(0, [Math]::Min(255, $item.Title.Length)) } else { "" }
            "field_1" = $item.field_1
            "field_2" = $item.field_2
            "field_3" = $item.field_3
            "field_4" = $item.field_4
            "field_5" = $item.field_5
            "field_6" = $item.field_6
        }

        Add-PnPListItem -List $ListName -Values $values | Out-Null
        $addedCount++

        if ($addedCount % 25 -eq 0) {
            Write-Host "  Added $addedCount items..." -ForegroundColor Gray
        }
    }
    catch {
        $errorCount++
        if ($errorCount -le 5) {
            Write-Host "  Error adding item '$($item.Title)': $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Summary
Write-Host ""
Write-Host "=== Sync Complete ===" -ForegroundColor Cyan
Write-Host "Items added: $addedCount" -ForegroundColor Green
if ($errorCount -gt 0) {
    Write-Host "Errors: $errorCount" -ForegroundColor Red
}

# Disconnect
Disconnect-PnPOnline
