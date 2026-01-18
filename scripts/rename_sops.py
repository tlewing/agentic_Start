"""
Rename SOPs to Official GSL Numbering
"""

import os
import shutil

sops_folder = r"C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"

# Mapping: old filename -> new filename
# Note: Section 1.1 covers two SOPs, so we'll name it after the primary one
rename_map = {
    "Section 1.1 Team Selection and Estimator Turnover - REVISED.docx":
        "9.2.010-015 Team Selection and Project Turnover - REVISED.docx",

    "Section 1.2 Administrative Setup - REVISED.docx":
        "9.2.120 Establish Tracking and Control Systems - REVISED.docx",

    "Section 1.3 Scope and Contract Review - REVISED.docx":
        "9.2.030-070 Scope and Contract Review - REVISED.docx",

    "Section 1.4 Buyout Process - REVISED.docx":
        "9.2.160 Develop Procurement Plan - REVISED.docx",

    "Section 1.5 Material Handling Plan - REVISED.docx":
        "9.2.080 Prepare Material Handling Plan - REVISED.docx",

    "Section 1.6 Layout and Sequencing Plan - REVISED.docx":
        "9.2.100 Prepare Layout and Sequencing Plan - REVISED.docx",

    "Section 1.7 Schedule Development and Tracking - REVISED.docx":
        "9.2.110 Develop Project Schedule - REVISED.docx",

    "SOP 9.4.631 - Release of Large Feeder Wire - REVISED.docx":
        "9.4.631 Release of Large Feeder Wire - REVISED.docx",

    "SOP_Procurement_Large_Feeder_Wire - REVISED.docx":
        "9.2.020 Procurement of Large Feeder Wire - REVISED.docx",

    "SOP OPS-CO-001 Change Order Management - REVISED.docx":
        "9.4.360 Manage Change Orders - REVISED.docx",
}

print("Renaming SOPs to Official GSL Numbers")
print("=" * 60)

renamed = 0
errors = 0

for old_name, new_name in rename_map.items():
    old_path = os.path.join(sops_folder, old_name)
    new_path = os.path.join(sops_folder, new_name)

    if os.path.exists(old_path):
        try:
            os.rename(old_path, new_path)
            print(f"OK: {old_name}")
            print(f"    -> {new_name}")
            renamed += 1
        except Exception as e:
            print(f"ERROR: {old_name}")
            print(f"    {str(e)}")
            errors += 1
    else:
        print(f"NOT FOUND: {old_name}")
        errors += 1

print("=" * 60)
print(f"Renamed: {renamed} files")
print(f"Errors: {errors}")

# List final contents
print("\nFinal folder contents:")
for f in sorted(os.listdir(sops_folder)):
    if f.endswith('.docx'):
        print(f"  {f}")
