"""Analyze the GSL SOP template structure and metadata fields."""
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

TEMPLATE_PATH = Path(r"C:\Users\tewing\Desktop\Holding\SOP\Templates\GSL_SOP_Master_Template_SHAREPOINT_ENABLED (v1).docx")

def analyze_template():
    print("=" * 60)
    print("TEMPLATE ANALYSIS")
    print("=" * 60)

    with zipfile.ZipFile(TEMPLATE_PATH, 'r') as zf:
        # List all files in the docx
        print("\n1. FILES IN DOCX:")
        for name in sorted(zf.namelist()):
            print(f"   {name}")

        # Check for custom XML parts
        print("\n2. CUSTOM XML PARTS:")
        custom_xml_files = [n for n in zf.namelist() if 'customXml' in n]
        for cxf in custom_xml_files:
            print(f"\n   --- {cxf} ---")
            try:
                content = zf.read(cxf).decode('utf-8', errors='ignore')
                if content.strip():
                    print(f"   {content[:500]}...")
            except Exception as e:
                print(f"   Error: {e}")

        # Check docProps for metadata
        print("\n3. CORE PROPERTIES (docProps/core.xml):")
        try:
            core = zf.read('docProps/core.xml').decode('utf-8')
            print(f"   {core[:1000]}")
        except Exception as e:
            print(f"   Error: {e}")

        print("\n4. CUSTOM PROPERTIES (docProps/custom.xml):")
        try:
            custom = zf.read('docProps/custom.xml').decode('utf-8')
            print(f"   {custom}")
        except Exception as e:
            print(f"   Not found or error: {e}")

        # Check content types
        print("\n5. CONTENT TYPES ([Content_Types].xml):")
        try:
            ct = zf.read('[Content_Types].xml').decode('utf-8')
            # Parse and show custom content types
            root = ET.fromstring(ct)
            for child in root:
                if 'custom' in str(child.attrib).lower():
                    print(f"   {child.attrib}")
        except Exception as e:
            print(f"   Error: {e}")

if __name__ == "__main__":
    analyze_template()
