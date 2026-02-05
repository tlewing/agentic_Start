"""Verify SOPs have content (not blank templates)."""
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

REVISED_DIR = Path(r"C:\Users\tewing\Desktop\Holding\SOP\Revised-SOPs")

samples = [
    "9.2.015",  # Project Turnover Meeting
    "9.4.360",  # Manage Change Orders
    "9.6.010",  # Conduct Closeout Meetings
]

for sample_id in samples:
    matches = list(REVISED_DIR.glob(f"{sample_id}*.docx"))
    if not matches:
        print(f"[NOT FOUND] {sample_id}")
        continue

    sop_file = matches[0]
    print(f"\n{'='*60}")
    print(f"FILE: {sop_file.name}")
    print('='*60)

    with zipfile.ZipFile(sop_file, 'r') as zf:
        xml_content = zf.read('word/document.xml').decode('utf-8')
        root = ET.fromstring(xml_content)

        # Extract text
        text_parts = []
        for elem in root.iter():
            if elem.text and elem.text.strip():
                text_parts.append(elem.text.strip())

        full_text = ' '.join(text_parts)

        # Check for template placeholders vs real content
        has_placeholder = '[SOP #]' in full_text or '[SOP Title]' in full_text
        has_real_content = 'Purpose' in full_text and len(full_text) > 500

        print(f"  Text length: {len(full_text)} chars")
        print(f"  Has placeholders: {has_placeholder}")
        print(f"  Has real content: {has_real_content}")
        print(f"\n  First 300 chars:")
        print(f"  {full_text[:300]}...")
