"""Extract and display the full SharePoint metadata schema from the template."""
import zipfile
from pathlib import Path

TEMPLATE_PATH = Path(r"C:\Users\tewing\Desktop\Holding\SOP\Templates\GSL_SOP_Master_Template_SHAREPOINT_ENABLED (v1).docx")

with zipfile.ZipFile(TEMPLATE_PATH, 'r') as zf:
    # Get the SharePoint properties XML
    print("=== SHAREPOINT PROPERTIES (customXml/item4.xml) ===\n")
    content = zf.read('customXml/item4.xml').decode('utf-8')
    # Pretty print
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(content)
    print(dom.toprettyxml(indent="  "))

    print("\n\n=== CONTENT TYPE SCHEMA (customXml/item2.xml) ===\n")
    schema = zf.read('customXml/item2.xml').decode('utf-8')
    dom = xml.dom.minidom.parseString(schema)
    print(dom.toprettyxml(indent="  "))
