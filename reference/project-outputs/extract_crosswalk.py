import openpyxl

wb = openpyxl.load_workbook(
    r"C:\Users\tewing\Desktop\Claude Projects\Key_SOP_Matrix_RACI_Updated.xlsx",
    data_only=True,
)
ws = wb["GSL_SOP_Metadata"]

print("=== Formerly column (legacy crosswalk) ===")
crosswalk = {}
for row in ws.iter_rows(min_row=2, values_only=False):
    sopid = row[3].value
    title = row[4].value
    formerly = row[20].value

    if sopid:
        sopid = str(sopid).strip()
        title = str(title).strip() if title else ""
        formerly_str = str(formerly).strip() if formerly else ""
        if formerly_str and formerly_str != "None" and formerly_str != "":
            crosswalk[formerly_str] = (sopid, title)
            print(f"  {formerly_str:30s} -> {sopid:10s} | {title}")
        crosswalk[sopid] = (sopid, title)

legacy_count = 0
for k, v in crosswalk.items():
    if k != v[0]:
        legacy_count += 1

print(f"\nTotal legacy entries: {legacy_count}")
print(f"Total SOPs (by new ID): {len(crosswalk) - legacy_count}")
