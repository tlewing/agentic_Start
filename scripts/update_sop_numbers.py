"""
Update SOP internal numbers to match new filenames
Uses pywin32 to manipulate Word documents
"""

import os
import win32com.client as win32

sops_folder = r"C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

# Mapping: filename -> (old_text_to_find, new_text_to_replace)
updates = {
    "9.2.010-015 Team Selection and Project Turnover - REVISED.docx": [
        ("Section 1.1:", "SOP 9.2.010/9.2.015:"),
        ("Section 1.1 Team Selection", "9.2.010/9.2.015 Team Selection and Project Turnover"),
    ],
    "9.2.020 Procurement of Large Feeder Wire - REVISED.docx": [
        ("SOP_Procurement_Large_Feeder_Wire", "SOP 9.2.020"),
        ("Procurement of Large Feeder Wire", "9.2.020 Procurement of Large Feeder Wire"),
    ],
    "9.2.030-070 Scope and Contract Review - REVISED.docx": [
        ("Section 1.3:", "SOP 9.2.030-070:"),
        ("Section 1.3 Scope and Contract Review", "9.2.030-070 Scope and Contract Review"),
    ],
    "9.2.080 Prepare Material Handling Plan - REVISED.docx": [
        ("Section 1.5:", "SOP 9.2.080:"),
        ("Section 1.5 Material Handling Plan", "9.2.080 Prepare Material Handling Plan"),
    ],
    "9.2.100 Prepare Layout and Sequencing Plan - REVISED.docx": [
        ("Section 1.6:", "SOP 9.2.100:"),
        ("Section 1.6 Layout and Sequencing Plan", "9.2.100 Prepare Layout and Sequencing Plan"),
    ],
    "9.2.110 Develop Project Schedule - REVISED.docx": [
        ("Section 1.7:", "SOP 9.2.110:"),
        ("Section 1.7 Schedule Development", "9.2.110 Develop Project Schedule"),
    ],
    "9.2.120 Establish Tracking and Control Systems - REVISED.docx": [
        ("Section 1.2:", "SOP 9.2.120:"),
        ("Section 1.2 Administrative Setup", "9.2.120 Establish Tracking and Control Systems"),
    ],
    "9.2.160 Develop Procurement Plan - REVISED.docx": [
        ("Section 1.4:", "SOP 9.2.160:"),
        ("Section 1.4 Buyout Process", "9.2.160 Develop Procurement Plan"),
    ],
    "9.4.360 Manage Change Orders - REVISED.docx": [
        ("SOP No.: OPS-CO-001", "SOP No.: 9.4.360"),
        ("OPS-CO-001", "9.4.360"),
        ("Change Order Management", "Manage Change Orders"),
    ],
    "9.4.631 Release of Large Feeder Wire - REVISED.docx": [
        # Already has correct number, just standardize format
        ("SOP Template 9.4.631", "SOP 9.4.631"),
    ],
}

print("Updating SOP Internal Numbers")
print("=" * 60)

word = win32.gencache.EnsureDispatch('Word.Application')
word.Visible = False

updated = 0
errors = 0

for filename, replacements in updates.items():
    filepath = os.path.join(sops_folder, filename)

    if not os.path.exists(filepath):
        print(f"NOT FOUND: {filename}")
        errors += 1
        continue

    try:
        doc = word.Documents.Open(filepath)
        changes_made = 0

        for old_text, new_text in replacements:
            find = doc.Content.Find
            find.ClearFormatting()
            find.Replacement.ClearFormatting()

            # Execute find and replace
            replaced = find.Execute(
                FindText=old_text,
                ReplaceWith=new_text,
                Replace=2,  # wdReplaceAll
                Forward=True,
                Wrap=1,  # wdFindContinue
                MatchCase=False,
                MatchWholeWord=False
            )
            if replaced:
                changes_made += 1

        doc.Save()
        doc.Close()

        if changes_made > 0:
            print(f"OK: {filename} ({changes_made} replacements)")
            updated += 1
        else:
            print(f"NO CHANGES: {filename}")

    except Exception as e:
        print(f"ERROR: {filename}")
        print(f"    {str(e)}")
        errors += 1
        try:
            doc.Close(False)
        except:
            pass

word.Quit()

print("=" * 60)
print(f"Updated: {updated} files")
print(f"Errors: {errors}")
