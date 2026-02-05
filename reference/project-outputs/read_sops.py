"""Read all 6 SOP documents and dump their full text content."""
from docx import Document
import os

SOP_DIR = r"C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

FILES = [
    "9.2.015",
    "9.2.020",
    "9.2.030",
    "9.2.040",
    "9.2.055",
    "9.2.057",
]

all_files = [f for f in os.listdir(SOP_DIR) if f.endswith(".docx") and not f.startswith("~")]

for target_id in FILES:
    match = [f for f in all_files if f.startswith(target_id)]
    if not match:
        print(f"\n{'='*80}")
        print(f"FILE NOT FOUND: {target_id}")
        continue

    fname = match[0]
    filepath = os.path.join(SOP_DIR, fname)
    doc = Document(filepath)

    print(f"\n{'='*80}")
    print(f"FILE: {fname}")
    print(f"{'='*80}")

    # Print all paragraphs with their style
    for i, para in enumerate(doc.paragraphs):
        text = para.text
        style = para.style.name if para.style else "None"
        if text.strip():
            print(f"[{i:3d}|{style:20s}] {text}")

    # Print tables
    for ti, table in enumerate(doc.tables):
        print(f"\n  --- TABLE {ti} ({len(table.rows)} rows x {len(table.columns)} cols) ---")
        for ri, row in enumerate(table.rows):
            cells = [c.text.strip()[:60] for c in row.cells]
            print(f"  Row {ri}: {' | '.join(cells)}")
