<#
.SYNOPSIS
    GSL SOP Manager (Legacy) - For PowerShell 5.1
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("Columns", "Test")]
    [string]$Action = "Columns"
)

$SiteUrl = "https://gslelectric8540.sharepoint.com/sites/StandardOperationProcedures"
$LibraryName = "SOP Library"
$OutputPath = "C:\Users\tewing\Desktop\Claude Projects\Project Outputs"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GSL SOP Manager" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check for module
Write-Host "Checking for PnP module..." -ForegroundColor Yellow
$module = Get-Module -ListAvailable -Name "SharePointPnPPowerShellOnline"

if (-not $module) {
    Write-Host "Installing SharePointPnPPowerShellOnline module..." -ForegroundColor Yellow
    Install-Module -Name SharePointPnPPowerShellOnline -Scope CurrentUser -Force -AllowClobber -SkipPublisherCheck
}

Write-Host "Loading module..." -ForegroundColor Yellow
$env:PNPLEGACYMESSAGE = 'false'
Import-Module SharePointPnPPowerShellOnline -WarningAction SilentlyContinue -ErrorAction Stop
Write-Host "Module loaded!" -ForegroundColor Green
Write-Host ""

# Connect to SharePoint using Web Login (supports MFA)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Connecting to SharePoint" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "A BROWSER WINDOW will open for sign-in." -ForegroundColor Yellow
Write-Host "Sign in with your Microsoft 365 account." -ForegroundColor Yellow
Write-Host "This supports MFA (multi-factor auth)." -ForegroundColor Yellow
Write-Host ""

try {
    Connect-PnPOnline -Url $SiteUrl -UseWebLogin -WarningAction SilentlyContinue
    Write-Host ""
    Write-Host "Connected successfully!" -ForegroundColor Green
    Write-Host ""
}
catch {
    Write-Host ""
    Write-Host "CONNECTION FAILED" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Get columns
if ($Action -eq "Columns") {
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "  SOP Library - Column Definitions" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""

    try {
        $fields = Get-PnPField -List $LibraryName | Where-Object { -not $_.Hidden } | Sort-Object Title

        foreach ($field in $fields) {
            Write-Host "----------------------------------------" -ForegroundColor DarkGray
            Write-Host "COLUMN: $($field.Title)" -ForegroundColor Cyan
            Write-Host "  Internal Name: $($field.InternalName)" -ForegroundColor Gray
            Write-Host "  Type: $($field.TypeAsString)" -ForegroundColor Gray
            Write-Host "  Required: $($field.Required)" -ForegroundColor Gray

            if ($field.Choices -and $field.Choices.Count -gt 0) {
                Write-Host "  Valid Choices:" -ForegroundColor Green
                foreach ($choice in $field.Choices) {
                    Write-Host "    - $choice" -ForegroundColor White
                }
            }
        }

        # Export
        $exportPath = "$OutputPath\SOP_Library_Columns.csv"
        $fields | Select-Object Title, InternalName, TypeAsString, Required | Export-Csv -Path $exportPath -NoTypeInformation
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "Exported to: $exportPath" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
    }
    catch {
        Write-Host "Error getting columns: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Disconnect
try {
    Disconnect-PnPOnline -ErrorAction SilentlyContinue
}
catch { }

Write-Host ""
Read-Host "Press Enter to close"
