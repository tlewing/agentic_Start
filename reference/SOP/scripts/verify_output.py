"""Verify the processed SOP output."""
import zipfile
from pathlib import Path
from docx import Document

OUTPUT_DIR = Path(r"C:\Users\tewing\Desktop\Holding\SOP\Revised-SOPs")

# Find the test output
output_files = list(OUTPUT_DIR.glob("9.2.015*.docx"))
if not output_files:
    print("No output file found")
    exit(1)

output_file = output_files[0]
print(f"Checking: {output_file.name}\n")

# Check content
print("=== DOCUMENT CONTENT ===")
doc = Document(output_file)
for i, para in enumerate(doc.paragraphs[:20]):
    if para.text.strip():
        print(f"{i}: {para.text[:100]}")

# Check SharePoint metadata
print("\n=== SHAREPOINT METADATA ===")
with zipfile.ZipFile(output_file, 'r') as zf:
    xml_content = zf.read('customXml/item4.xml').decode('utf-8')
    # Extract key values
    import re
    fields = ['Status', 'SOPID', 'SOPFileName', 'Description', 'Department', 'RACI_Responsible']
    for field in fields:
        match = re.search(f'<{field}[^>]*>([^<]*)</{field}>', xml_content)
        if match:
            print(f"  {field}: {match.group(1)[:80]}")
        else:
            match = re.search(f'<[^>]*{field}[^>]*>([^<]*)</[^>]*{field}[^>]*>', xml_content)
            if match and match.group(1).strip():
                print(f"  {field}: {match.group(1)[:80]}")
