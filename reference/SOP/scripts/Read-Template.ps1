# Extract text from template docx file
Add-Type -AssemblyName System.IO.Compression.FileSystem

$DocxPath = "C:\Users\tewing\Desktop\Holding\SOP\Templates\GSL_SOP_Master_Template_SHAREPOINT_ENABLED (v1).docx"
$OutputPath = "C:\Users\tewing\Desktop\Holding\SOP\Templates\template-content.txt"

$zip = [System.IO.Compression.ZipFile]::OpenRead($DocxPath)
$entry = $zip.Entries | Where-Object { $_.FullName -eq 'word/document.xml' }
$stream = $entry.Open()
$reader = New-Object System.IO.StreamReader($stream)
$xmlContent = $reader.ReadToEnd()
$reader.Close()
$zip.Dispose()

# Parse XML and extract text
$xml = [xml]$xmlContent
$text = $xml.document.body.InnerText

# Save to file
$text | Out-File -FilePath $OutputPath -Encoding UTF8

Write-Host "Template content saved to: $OutputPath"
