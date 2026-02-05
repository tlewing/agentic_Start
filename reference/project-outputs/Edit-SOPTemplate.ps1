<#
.SYNOPSIS
    Manages SOP documents in SharePoint SOP Library.

.DESCRIPTION
    Create, validate, and upload SOP documents to SharePoint with metadata.

.PARAMETER Action
    The action to perform: Columns, Validate, New

.PARAMETER SOPName
    The name of the SOP (e.g., "9.2.025 - Change Order")

.PARAMETER MetadataPath
    Path to the metadata JSON file

.PARAMETER Upload
    Switch to upload the document to SharePoint

.EXAMPLE
    .\Edit-SOPTemplate.ps1 -Action Columns

.EXAMPLE
    .\Edit-SOPTemplate.ps1 -Action Validate -MetadataPath ".\metadata.json"

.EXAMPLE
    .\Edit-SOPTemplate.ps1 -Action New -SOPName "9.2.025 - Change Order" -MetadataPath ".\metadata.json" -Upload
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("Columns", "Validate", "New")]
    [string]$Action,

    [Parameter(Mandatory=$false)]
    [string]$SOPName,

    [Parameter(Mandatory=$false)]
    [string]$MetadataPath,

    [Parameter(Mandatory=$false)]
    [switch]$Upload,

    [Parameter(Mandatory=$false)]
    [string]$DocumentPath
)

# Configuration
$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "SOP Library"
$ClientId = "31359c7f-bd7e-475c-86db-fdb8c937548e"

# Import PnP Module
Import-Module PnP.PowerShell -ErrorAction Stop

function Connect-ToSharePoint {
    Write-Host "Connecting to SharePoint..." -ForegroundColor Cyan
    Write-Host "A code will appear - go to https://microsoft.com/devicelogin and enter it" -ForegroundColor Yellow
    Connect-PnPOnline -Url $SiteUrl -DeviceLogin -ClientId $ClientId -Tenant "gslelectric8540.onmicrosoft.com"
    Write-Host "Connected successfully!" -ForegroundColor Green
}

function Get-ColumnDefinitions {
    Write-Host "`n=== SOP Library Column Definitions ===" -ForegroundColor Yellow
    Write-Host ""

    $fields = Get-PnPField -List $LibraryName | Where-Object { -not $_.Hidden }

    foreach ($field in $fields | Sort-Object Title) {
        Write-Host "----------------------------------------" -ForegroundColor DarkGray
        Write-Host "Column: " -NoNewline -ForegroundColor Cyan
        Write-Host $field.Title
        Write-Host "Internal Name: " -NoNewline -ForegroundColor Gray
        Write-Host $field.InternalName
        Write-Host "Type: " -NoNewline -ForegroundColor Gray
        Write-Host $field.TypeAsString
        Write-Host "Required: " -NoNewline -ForegroundColor Gray
        Write-Host $field.Required

        # Get choices for Choice fields
        if ($field.TypeAsString -eq "Choice" -or $field.TypeAsString -eq "MultiChoice") {
            if ($field.Choices -and $field.Choices.Count -gt 0) {
                Write-Host "Valid Choices:" -ForegroundColor Green
                foreach ($choice in $field.Choices) {
                    Write-Host "  - $choice" -ForegroundColor White
                }
            }
        }

        # Get lookup values for Lookup fields
        if ($field.TypeAsString -eq "Lookup") {
            Write-Host "Lookup List: " -NoNewline -ForegroundColor Gray
            Write-Host $field.LookupList
        }

        Write-Host ""
    }

    # Export to CSV for reference
    $exportPath = Join-Path (Split-Path $PSScriptRoot) "SOP_Library_Columns.csv"
    $fields | Select-Object Title, InternalName, TypeAsString, Required |
        Export-Csv -Path $exportPath -NoTypeInformation
    Write-Host "Column definitions exported to: $exportPath" -ForegroundColor Green
}

function Test-MetadataFile {
    param([string]$Path)

    Write-Host "`n=== Validating Metadata File ===" -ForegroundColor Yellow
    Write-Host "File: $Path" -ForegroundColor Cyan
    Write-Host ""

    if (-not (Test-Path $Path)) {
        Write-Host "ERROR: File not found: $Path" -ForegroundColor Red
        return $false
    }

    try {
        $metadata = Get-Content $Path -Raw | ConvertFrom-Json
        Write-Host "JSON syntax: VALID" -ForegroundColor Green
    }
    catch {
        Write-Host "ERROR: Invalid JSON syntax" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        return $false
    }

    # Get field definitions for validation
    $fields = Get-PnPField -List $LibraryName | Where-Object { -not $_.Hidden }
    $fieldLookup = @{}
    foreach ($field in $fields) {
        $fieldLookup[$field.InternalName] = $field
        $fieldLookup[$field.Title] = $field
    }

    $valid = $true
    $metadata.PSObject.Properties | ForEach-Object {
        $key = $_.Name
        $value = $_.Value

        Write-Host "Checking: $key = $value" -ForegroundColor Gray

        if ($fieldLookup.ContainsKey($key)) {
            $field = $fieldLookup[$key]

            # Validate choice fields
            if ($field.TypeAsString -eq "Choice" -and $field.Choices) {
                if ($value -notin $field.Choices) {
                    Write-Host "  WARNING: '$value' is not a valid choice for $key" -ForegroundColor Yellow
                    Write-Host "  Valid choices: $($field.Choices -join ', ')" -ForegroundColor Yellow
                    $valid = $false
                }
                else {
                    Write-Host "  VALID" -ForegroundColor Green
                }
            }
            elseif ($field.TypeAsString -eq "MultiChoice" -and $field.Choices) {
                $values = $value -split ";"
                foreach ($v in $values) {
                    $v = $v.Trim()
                    if ($v -notin $field.Choices) {
                        Write-Host "  WARNING: '$v' is not a valid choice for $key" -ForegroundColor Yellow
                        $valid = $false
                    }
                }
                if ($valid) {
                    Write-Host "  VALID" -ForegroundColor Green
                }
            }
            else {
                Write-Host "  VALID (field exists)" -ForegroundColor Green
            }
        }
        else {
            Write-Host "  WARNING: Column '$key' not found in SOP Library" -ForegroundColor Yellow
            $valid = $false
        }
    }

    Write-Host ""
    if ($valid) {
        Write-Host "VALIDATION PASSED" -ForegroundColor Green
    }
    else {
        Write-Host "VALIDATION COMPLETED WITH WARNINGS" -ForegroundColor Yellow
    }

    return $valid
}

function New-SOPDocument {
    param(
        [string]$Name,
        [string]$MetadataFile,
        [string]$DocPath,
        [switch]$UploadToSharePoint
    )

    Write-Host "`n=== Creating SOP Document ===" -ForegroundColor Yellow
    Write-Host "SOP Name: $Name" -ForegroundColor Cyan
    Write-Host ""

    # Load metadata
    $metadata = @{}
    if ($MetadataFile -and (Test-Path $MetadataFile)) {
        $metadata = Get-Content $MetadataFile -Raw | ConvertFrom-Json
        Write-Host "Loaded metadata from: $MetadataFile" -ForegroundColor Green
    }

    # Find the document
    if (-not $DocPath) {
        # Search for the document in Revised SOPs folder
        $searchPaths = @(
            "C:\Users\tewing\Desktop\Claude Projects\Revised SOPs",
            "C:\Users\tewing\Desktop\Claude Projects\Project Outputs"
        )

        foreach ($searchPath in $searchPaths) {
            $found = Get-ChildItem -Path $searchPath -Filter "*$Name*" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($found) {
                $DocPath = $found.FullName
                Write-Host "Found document: $DocPath" -ForegroundColor Green
                break
            }
        }
    }

    if (-not $DocPath -or -not (Test-Path $DocPath)) {
        Write-Host "ERROR: Document not found for SOP: $Name" -ForegroundColor Red
        Write-Host "Please specify -DocumentPath parameter" -ForegroundColor Yellow
        return
    }

    if ($UploadToSharePoint) {
        Write-Host "`nUploading to SharePoint..." -ForegroundColor Cyan

        # Convert metadata to hashtable
        $metadataHash = @{}
        if ($metadata) {
            $metadata.PSObject.Properties | ForEach-Object {
                $metadataHash[$_.Name] = $_.Value
            }
        }

        # Upload document
        try {
            $fileName = Split-Path $DocPath -Leaf

            if ($metadataHash.Count -gt 0) {
                Add-PnPFile -Path $DocPath -Folder $LibraryName -Values $metadataHash
            }
            else {
                Add-PnPFile -Path $DocPath -Folder $LibraryName
            }

            Write-Host "SUCCESS: Uploaded $fileName to $LibraryName" -ForegroundColor Green

            if ($metadataHash.Count -gt 0) {
                Write-Host "Applied metadata:" -ForegroundColor Cyan
                $metadataHash.GetEnumerator() | ForEach-Object {
                    Write-Host "  $($_.Key): $($_.Value)" -ForegroundColor White
                }
            }
        }
        catch {
            Write-Host "ERROR: Failed to upload document" -ForegroundColor Red
            Write-Host $_.Exception.Message -ForegroundColor Red
        }
    }
    else {
        Write-Host "`nDocument ready for upload: $DocPath" -ForegroundColor Yellow
        Write-Host "Add -Upload switch to upload to SharePoint" -ForegroundColor Yellow
    }
}

# Main execution
try {
    Connect-ToSharePoint

    switch ($Action) {
        "Columns" {
            Get-ColumnDefinitions
        }
        "Validate" {
            if (-not $MetadataPath) {
                Write-Host "ERROR: -MetadataPath is required for Validate action" -ForegroundColor Red
                exit 1
            }
            Test-MetadataFile -Path $MetadataPath
        }
        "New" {
            if (-not $SOPName) {
                Write-Host "ERROR: -SOPName is required for New action" -ForegroundColor Red
                exit 1
            }
            New-SOPDocument -Name $SOPName -MetadataFile $MetadataPath -DocPath $DocumentPath -UploadToSharePoint:$Upload
        }
    }
}
catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
finally {
    # Disconnect if connected
    if (Get-PnPConnection -ErrorAction SilentlyContinue) {
        Disconnect-PnPOnline
    }
}
