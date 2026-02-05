# Extract text from a docx file
param([string]$DocxPath, [string]$OutputPath)

Add-Type -AssemblyName System.IO.Compression.FileSystem

$zip = [System.IO.Compression.ZipFile]::OpenRead($DocxPath)
$entry = $zip.Entries | Where-Object { $_.FullName -eq 'word/document.xml' }
$stream = $entry.Open()
$reader = New-Object System.IO.StreamReader($stream)
$xmlContent = $reader.ReadToEnd()
$reader.Close()
$zip.Dispose()

$xml = [xml]$xmlContent
$text = $xml.document.body.InnerText
$text | Out-File -FilePath $OutputPath -Encoding UTF8
