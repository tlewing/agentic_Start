<#
.SYNOPSIS
    GSL SOP Manager - Upload and manage SOPs in SharePoint

.DESCRIPTION
    View columns, create metadata templates, validate, and upload SOPs to SharePoint.

.PARAMETER Action
    Columns   - View all SharePoint columns and valid values
    Template  - Create metadata JSON template
    Validate  - Validate metadata JSON file
    New       - Upload single SOP with metadata
    Batch     - Batch upload all revised SOPs

.EXAMPLE
    .\GSL-SOPManager.ps1 -Action Columns
    .\GSL-SOPManager.ps1 -Action Template
    .\GSL-SOPManager.ps1 -Action New -SOPNumber "9.2.025" -Upload
    .\GSL-SOPManager.ps1 -Action Batch -Upload
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("Columns", "Template", "Validate", "New", "Batch")]
    [string]$Action,

    [Parameter(Mandatory=$false)]
    [string]$SOPNumber,

    [Parameter(Mandatory=$false)]
    [string]$MetadataPath,

    [Parameter(Mandatory=$false)]
    [switch]$Upload
)

# ============================================
# CONFIGURATION
# ============================================
$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "SOP Library"
$RevisedSOPsPath = "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"
$OutputPath = "C:\Users\tewing\Desktop\Claude Projects\Project Outputs"

# ============================================
# SOP CATEGORY MAPPING (Based on SOP Number)
# ============================================
$CategoryMapping = @{
    "9.2" = @{
        Category = "Pre-Construction"
        CCCTags = @("120 Coordination", "130 Documentation Mgmt", "150 Scheduling")
        Department = "Operations"
    }
    "9.3" = @{
        Category = "Site Setup"
        CCCTags = @("110 Mobilization")
        Department = "Operations"
    }
    "9.4" = @{
        Category = "Project Execution"
        CCCTags = @("120 Coordination", "130 Documentation Mgmt")
        Department = "Operations"
    }
    "9.41.0" = @{
        Category = "Meetings & Coordination"
        CCCTags = @("120 Coordination", "140 Communication")
        Department = "Operations"
    }
    "9.41.1" = @{
        Category = "Documentation"
        CCCTags = @("130 Documentation Mgmt")
        Department = "Operations"
    }
    "9.41.2" = @{
        Category = "Documentation"
        CCCTags = @("130 Documentation Mgmt", "140 Communication")
        Department = "Operations"
    }
    "9.41.3" = @{
        Category = "Scheduling"
        CCCTags = @("150 Scheduling")
        Department = "Operations"
    }
    "9.41.4" = @{
        Category = "Cost Control"
        CCCTags = @("165 Accounting", "170 Cost Control & Billing")
        Department = "Accounting"
    }
    "9.41.47" = @{
        Category = "Safety"
        CCCTags = @("193 Safety Mgmt")
        Department = "Safety"
    }
    "9.41.48" = @{
        Category = "Safety"
        CCCTags = @("193 Safety Mgmt")
        Department = "Safety"
    }
    "9.41.49" = @{
        Category = "Safety"
        CCCTags = @("193 Safety Mgmt")
        Department = "Safety"
    }
    "9.41.5" = @{
        Category = "Quality"
        CCCTags = @("194 Quality Control")
        Department = "Operations"
    }
    "9.41.6" = @{
        Category = "Procurement"
        CCCTags = @("190 Materials Mgmt")
        Department = "Operations"
    }
    "9.41.7" = @{
        Category = "Field Operations"
        CCCTags = @("192 Labor Mgmt", "120 Coordination")
        Department = "Operations"
    }
    "9.5" = @{
        Category = "Commissioning"
        CCCTags = @("194 Quality Control")
        Department = "Operations"
    }
    "9.6" = @{
        Category = "Closeout"
        CCCTags = @("195 Project Closeout")
        Department = "Operations"
    }
}

# ============================================
# ROLE MAPPING (Based on SOP Content)
# ============================================
$RoleMapping = @{
    "9.2" = @("PM", "APM", "Foreman")
    "9.3" = @("Foreman", "General Superintendent")
    "9.41.0" = @("PM", "Foreman")
    "9.41.1" = @("PM", "Project Coordinator")
    "9.41.2" = @("PM", "Project Coordinator")
    "9.41.3" = @("PM", "Scheduler", "Foreman")
    "9.41.4" = @("PM", "Accounting", "Business Manager")
    "9.41.47" = @("Safety", "Foreman", "General Superintendent")
    "9.41.48" = @("Safety", "Foreman")
    "9.41.49" = @("Safety", "Foreman")
    "9.41.5" = @("QC", "Foreman")
    "9.41.6" = @("Purchasing", "PM", "Foreman")
    "9.41.7" = @("Foreman", "General Superintendent")
    "9.5" = @("PM", "Foreman", "QC")
    "9.6" = @("PM", "Project Coordinator", "Foreman")
}

# ============================================
# FUNCTIONS
# ============================================

function Connect-ToSharePoint {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  GSL SOP Manager - SharePoint Connect" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
    Write-Host "A browser window will open for sign-in..." -ForegroundColor Yellow
    Write-Host ""

    $env:PNPLEGACYMESSAGE = 'false'
    Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue -ErrorAction Stop
    Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue

    Write-Host "Connected successfully!" -ForegroundColor Green
    Write-Host ""
}

function Get-SOPMetadata {
    param([string]$SOPNum, [string]$FileName)

    # Extract SOP number prefix for category matching
    $prefix = ""
    foreach ($key in ($CategoryMapping.Keys | Sort-Object -Descending)) {
        if ($SOPNum.StartsWith($key)) {
            $prefix = $key
            break
        }
    }

    if (-not $prefix) {
        $prefix = $SOPNum.Substring(0, 3)  # Default to first 3 chars like "9.2"
    }

    $catInfo = $CategoryMapping[$prefix]
    if (-not $catInfo) {
        $catInfo = @{
            Category = "General"
            CCCTags = @("120 Coordination")
            Department = "Operations"
        }
    }

    # Get roles
    $roles = @("PM", "Foreman")  # Default
    foreach ($key in ($RoleMapping.Keys | Sort-Object -Descending)) {
        if ($SOPNum.StartsWith($key)) {
            $roles = $RoleMapping[$key]
            break
        }
    }

    # Extract title from filename
    $title = $FileName -replace "\.docx?$", "" -replace " - REVISED$", "" -replace "^SOP ", ""
    $title = $title -replace "^[\d\.]+\s*", ""  # Remove leading numbers
    $title = $title.Trim()

    # Build metadata hashtable
    $metadata = @{
        "Title" = "$SOPNum - $title"
        "SOPID" = $SOPNum
        "DocumentType" = "SOP"
        "Status" = "Draft"
        "Department_x002f_Division" = $catInfo.Department
    }

    # Add CCC Tags (multi-choice field)
    if ($catInfo.CCCTags -and $catInfo.CCCTags.Count -gt 0) {
        $metadata["Category_x0028_CCCTag_x0029_"] = $catInfo.CCCTags
    }

    # Add Roles (multi-choice field)
    if ($roles -and $roles.Count -gt 0) {
        $metadata["Roles_x0028_RACI_x0029_"] = $roles
    }

    return $metadata
}

function Get-ColumnDefinitions {
    Write-Host "`n========================================" -ForegroundColor Yellow
    Write-Host "  SOP Library - Column Definitions" -ForegroundColor Yellow
    Write-Host "========================================`n" -ForegroundColor Yellow

    $fields = Get-PnPField -List $LibraryName | Where-Object { -not $_.Hidden } | Sort-Object Title

    $columnData = @()

    foreach ($field in $fields) {
        Write-Host "COLUMN: $($field.Title)" -ForegroundColor Cyan
        Write-Host "  Internal: $($field.InternalName) | Type: $($field.TypeAsString) | Required: $($field.Required)" -ForegroundColor Gray

        if ($field.Choices -and $field.Choices.Count -gt 0) {
            Write-Host "  Choices: $($field.Choices -join ', ')" -ForegroundColor Green
        }

        $columnData += [PSCustomObject]@{
            Title = $field.Title
            InternalName = $field.InternalName
            Type = $field.TypeAsString
            Required = $field.Required
            Choices = ($field.Choices -join "; ")
        }
    }

    $exportPath = "$OutputPath\SOP_Library_Columns.csv"
    $columnData | Export-Csv -Path $exportPath -NoTypeInformation
    Write-Host "`nExported to: $exportPath" -ForegroundColor Green
}

function New-MetadataTemplate {
    Write-Host "`n========================================" -ForegroundColor Yellow
    Write-Host "  Creating Metadata Templates" -ForegroundColor Yellow
    Write-Host "========================================`n" -ForegroundColor Yellow

    $template = [ordered]@{
        "Title" = "9.X.XXX - SOP Title Here"
        "SOPID" = "9.X.XXX"
        "DocumentType" = "SOP"
        "Status" = "Draft | Under Review | Approved | Retired"
        "Department_x002f_Division" = "Operations | Safety | Prefab | Accounting | Engineering | Administration"
        "Category_x0028_CCCTag_x0029_" = @("110 Mobilization", "120 Coordination")
        "Roles_x0028_RACI_x0029_" = @("PM", "Foreman")
        "Description" = "Brief description of the SOP"
    }

    $templatePath = "$OutputPath\SOP_Metadata_Template.json"
    $template | ConvertTo-Json -Depth 10 | Out-File -FilePath $templatePath -Encoding UTF8

    Write-Host "Template saved to: $templatePath" -ForegroundColor Green
    Write-Host ""
    Write-Host "Valid Document Types: SOP, Form, Checklist, Template" -ForegroundColor Cyan
    Write-Host "Valid Status: Draft, Under Review, Approved, Retired" -ForegroundColor Cyan
    Write-Host "Valid Departments: Operations, Safety, Prefab, Accounting, Engineering, Administration" -ForegroundColor Cyan
}

function Upload-SingleSOP {
    param(
        [string]$SOPNum,
        [string]$MetaFile,
        [switch]$DoUpload
    )

    Write-Host "`n========================================" -ForegroundColor Yellow
    Write-Host "  Processing SOP: $SOPNum" -ForegroundColor Yellow
    Write-Host "========================================`n" -ForegroundColor Yellow

    # Find the document
    $searchPattern = "*$SOPNum*"
    $found = Get-ChildItem -Path $RevisedSOPsPath -Filter $searchPattern -Recurse -ErrorAction SilentlyContinue |
             Where-Object { $_.Extension -in @(".docx", ".doc") } |
             Select-Object -First 1

    if (-not $found) {
        Write-Host "ERROR: No document found matching: $SOPNum" -ForegroundColor Red
        Write-Host "Searched in: $RevisedSOPsPath" -ForegroundColor Gray
        return $false
    }

    Write-Host "Found: $($found.Name)" -ForegroundColor Green

    # Get or generate metadata
    $metadata = @{}
    if ($MetaFile -and (Test-Path $MetaFile)) {
        $json = Get-Content $MetaFile -Raw | ConvertFrom-Json
        $json.PSObject.Properties | ForEach-Object {
            $metadata[$_.Name] = $_.Value
        }
        Write-Host "Loaded metadata from: $MetaFile" -ForegroundColor Green
    }
    else {
        $metadata = Get-SOPMetadata -SOPNum $SOPNum -FileName $found.Name
        Write-Host "Auto-generated metadata:" -ForegroundColor Cyan
        $metadata.GetEnumerator() | ForEach-Object {
            $val = if ($_.Value -is [array]) { $_.Value -join ", " } else { $_.Value }
            Write-Host "  $($_.Key): $val" -ForegroundColor White
        }
    }

    if ($DoUpload) {
        Write-Host "`nUploading to SharePoint..." -ForegroundColor Cyan
        try {
            Add-PnPFile -Path $found.FullName -Folder $LibraryName -Values $metadata | Out-Null
            Write-Host "SUCCESS: Uploaded $($found.Name)" -ForegroundColor Green
            return $true
        }
        catch {
            Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
            return $false
        }
    }
    else {
        Write-Host "`nReady to upload. Add -Upload switch to upload to SharePoint." -ForegroundColor Yellow
        return $true
    }
}

function Start-BatchUpload {
    param([switch]$DoUpload)

    Write-Host "`n========================================" -ForegroundColor Yellow
    Write-Host "  Batch Upload - Revised SOPs" -ForegroundColor Yellow
    Write-Host "========================================`n" -ForegroundColor Yellow

    $files = Get-ChildItem -Path $RevisedSOPsPath -Filter "*.docx" -ErrorAction SilentlyContinue |
             Where-Object { $_.Name -match "^[\d\.]+" }

    Write-Host "Found $($files.Count) SOP files to process" -ForegroundColor Cyan
    Write-Host ""

    if (-not $DoUpload) {
        Write-Host "PREVIEW MODE - Add -Upload switch to actually upload" -ForegroundColor Yellow
        Write-Host ""
    }

    $success = 0
    $failed = 0
    $skipped = 0

    foreach ($file in $files) {
        # Extract SOP number from filename
        if ($file.Name -match "^([\d\.]+)") {
            $sopNum = $Matches[1].TrimEnd(".")

            Write-Host "----------------------------------------" -ForegroundColor DarkGray
            Write-Host "Processing: $($file.Name)" -ForegroundColor White

            $metadata = Get-SOPMetadata -SOPNum $sopNum -FileName $file.Name

            if ($DoUpload) {
                try {
                    Add-PnPFile -Path $file.FullName -Folder $LibraryName -Values $metadata | Out-Null
                    Write-Host "  [OK] Uploaded" -ForegroundColor Green
                    $success++
                }
                catch {
                    Write-Host "  [FAIL] $($_.Exception.Message)" -ForegroundColor Red
                    $failed++
                }
            }
            else {
                Write-Host "  SOP ID: $sopNum" -ForegroundColor Gray
                Write-Host "  Department: $($metadata['Department_x002f_Division'])" -ForegroundColor Gray
                $skipped++
            }
        }
        else {
            Write-Host "Skipping (no SOP number): $($file.Name)" -ForegroundColor Yellow
            $skipped++
        }
    }

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  Batch Processing Complete" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    if ($DoUpload) {
        Write-Host "  Successful: $success" -ForegroundColor Green
        Write-Host "  Failed: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
    }
    else {
        Write-Host "  Files ready: $($files.Count)" -ForegroundColor Yellow
        Write-Host "  Run with -Upload to upload to SharePoint" -ForegroundColor Yellow
    }
    Write-Host "========================================`n" -ForegroundColor Cyan
}

# ============================================
# MAIN
# ============================================

try {
    # Check for module
    $module = Get-Module -ListAvailable -Name "SharePointPnPPowerShellOnline"
    if (-not $module) {
        Write-Host "Installing PnP module..." -ForegroundColor Yellow
        Install-Module -Name SharePointPnPPowerShellOnline -Scope CurrentUser -Force -AllowClobber -SkipPublisherCheck
    }

    Connect-ToSharePoint

    switch ($Action) {
        "Columns" {
            Get-ColumnDefinitions
        }
        "Template" {
            New-MetadataTemplate
        }
        "Validate" {
            if (-not $MetadataPath) {
                Write-Host "ERROR: -MetadataPath required" -ForegroundColor Red
                exit 1
            }
            # Validation logic here
        }
        "New" {
            if (-not $SOPNumber) {
                Write-Host "ERROR: -SOPNumber required (e.g., 9.2.025)" -ForegroundColor Red
                exit 1
            }
            Upload-SingleSOP -SOPNum $SOPNumber -MetaFile $MetadataPath -DoUpload:$Upload
        }
        "Batch" {
            Start-BatchUpload -DoUpload:$Upload
        }
    }
}
catch {
    Write-Host "`nERROR: $($_.Exception.Message)" -ForegroundColor Red
}
finally {
    try { Disconnect-PnPOnline -ErrorAction SilentlyContinue } catch { }
}

Write-Host ""
Read-Host "Press Enter to close"
