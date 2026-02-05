"""Test processing a single SOP."""
import sys
sys.path.insert(0, r"C:\Users\tewing\Desktop\Holding\SOP\scripts")
from process_sops import process_single_sop, SOURCE_DIR, OUTPUT_DIR
from pathlib import Path

# Test with just one SOP
test_file = SOURCE_DIR / "9.2.015 – Project Turnover Meeting.docx"

if test_file.exists():
    print(f"Testing with: {test_file.name}")
    try:
        process_single_sop(test_file)
        print("\nTest successful!")
        print(f"Check output in: {OUTPUT_DIR}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"Test file not found: {test_file}")
    print("\nAvailable files:")
    for f in sorted(SOURCE_DIR.glob("9.2*.docx"))[:5]:
        print(f"  {f.name}")
