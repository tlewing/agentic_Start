import docx
import os

folder = r"C:\Users\tewing\Desktop\Claude Projects\SOP_Revisions\Revised"
pattern = "9.2.060"

files = [f for f in os.listdir(folder) if pattern in f and f.endswith('.docx')]
if files:
    filepath = os.path.join(folder, files[0])
    print(f"Reading: {files[0]}")
    print("=" * 70)

    doc = docx.Document(filepath)
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if text:
            style = para.style.name if para.style else "None"
            is_bold = any(run.bold for run in para.runs if run.text.strip())
            bold_mark = "[BOLD]" if is_bold else ""
            print(f"[{i:3}] ({style:20}) {bold_mark:7} {text[:70]}{'...' if len(text) > 70 else ''}")
