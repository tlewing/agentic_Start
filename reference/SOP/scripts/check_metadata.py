"""Check if metadata was properly written to revised SOPs."""
import zipfile
from pathlib import Path
import re

REVISED_DIR = Path(r"C:\Users\tewing\Desktop\Holding\SOP\Revised-SOPs")

# Check a few sample files
samples = list(REVISED_DIR.glob("9.2.015*.docx"))[:1] + \
          list(REVISED_DIR.glob("9.4.010*.docx"))[:1] + \
          list(REVISED_DIR.glob("9.6.010*.docx"))[:1]

for sample in samples:
    print(f"\n{'='*60}")
    print(f"FILE: {sample.name}")
    print('='*60)

    with zipfile.ZipFile(sample, 'r') as zf:
        try:
            xml_content = zf.read('customXml/item4.xml').decode('utf-8')

            # Extract key fields
            fields = [
                'SOPID', 'Status', 'SOPFileName',
                'RACI_Responsible', 'RACI_Accountable',
                'RACI_Consulted', 'RACI_Informed',
                'Department', 'Description'
            ]

            for field in fields:
                # Look for field value
                pattern = rf'<[^>]*{field}[^>]*>([^<]*)</[^>]*>'
                match = re.search(pattern, xml_content, re.IGNORECASE)
                if match and match.group(1).strip():
                    print(f"  {field}: {match.group(1)[:60]}")
                else:
                    # Check for nil
                    nil_pattern = rf'<[^>]*{field}[^>]*xsi:nil="true"'
                    if re.search(nil_pattern, xml_content, re.IGNORECASE):
                        print(f"  {field}: [EMPTY - nil]")
                    else:
                        print(f"  {field}: [NOT FOUND]")

        except Exception as e:
            print(f"  Error reading metadata: {e}")
