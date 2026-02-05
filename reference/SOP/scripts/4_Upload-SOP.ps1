# Upload a revised SOP back to SharePoint
# Run 1_Connect-SharePoint.ps1 first
#
# Usage: .\4_Upload-SOP.ps1 -FilePath "C:\path\to\SOP.docx"

param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

$LibraryName = "Standard Operating Procedures"

if (-not (Test-Path $FilePath)) {
    Write-Host "ERROR: File not found: $FilePath" -ForegroundColor Red
    exit 1
}

$FileName = Split-Path $FilePath -Leaf
Write-Host "Uploading: $FileName" -ForegroundColor Cyan

Add-PnPFile -Path $FilePath -Folder $LibraryName -ErrorAction Stop

Write-Host "Upload complete!" -ForegroundColor Green
