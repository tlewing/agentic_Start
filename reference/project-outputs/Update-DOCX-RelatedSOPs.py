"""
Update Related SOPs in .docx Documents
=======================================
Finds the 'Related SOPs' section in each SOP document and updates it
with the related SOPs from RelatedSOPs_Mapping.csv.

Handles two document patterns:
  Pattern A: 'Related SOPs:' as standalone paragraph + list items below
  Pattern B: 'Related SOPs:' embedded in a multi-line metadata paragraph
"""

import csv
import os
import re
import copy
from docx import Document
from docx.shared import Pt, RGBColor

# ============================================================
# CONFIG
# ============================================================
BASE_DIR = r"C:\Users\tewing\Desktop\Claude Projects\Project Outputs"
SOP_DIR = r"C:\Users\tewing\Desktop\Claude Projects\Revised SOPs"
CSV_PATH = os.path.join(BASE_DIR, "RelatedSOPs_Mapping.csv")


def load_mapping(csv_path):
    """Load {sopid: related_sops_string} from CSV."""
    mapping = {}
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["SOPID"].strip()
            related = row["RelatedSOPs"].strip()
            if sid and related:
                mapping[sid] = related
    return mapping


def extract_sop_id(filename):
    """Extract SOP ID from filename like '9.2.010 - Team Selection.docx'."""
    match = re.match(r"(\d+\.\d+\.\d+)", filename)
    return match.group(1) if match else None


def format_related_list(related_str):
    """Convert semicolon-delimited string to list of formatted entries."""
    entries = []
    for part in related_str.split(";"):
        part = part.strip()
        if part:
            entries.append(part)
    return entries


def find_related_sops_pattern(doc):
    """Determine which pattern the document uses for Related SOPs.
    Returns: ('A', para_index), ('B', para_index), or ('C', None)
    """
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()

        # Pattern A: standalone 'Related SOPs:' paragraph
        if text in ("Related SOPs:", "Related SOPs"):
            return "A", i

        # Pattern B: embedded in a larger paragraph
        if "Related SOPs" in text and len(text) > 25:
            return "B", i

    return "C", None


def get_run_format(para):
    """Extract font formatting from the first run of a paragraph."""
    if para.runs:
        run = para.runs[0]
        return {
            "name": run.font.name,
            "size": run.font.size,
            "bold": run.font.bold,
            "color": run.font.color.rgb if run.font.color and run.font.color.rgb else None,
        }
    return None


def update_pattern_a(doc, para_idx, related_entries):
    """Update Pattern A: replace list items after the 'Related SOPs:' heading."""
    # Find and remove existing list items (paragraphs after the heading)
    indices_to_clear = []
    for j in range(para_idx + 1, len(doc.paragraphs)):
        text = doc.paragraphs[j].text.strip()
        # Stop at separator lines, section headers, or non-SOP content
        if (text.startswith("===") or
            text.startswith("DOCUMENT") or
            (text and not text.startswith("-") and not text.startswith("\u2022") and
             not re.match(r"^\d+\.\d+\.\d+", text))):
            break
        if text:
            indices_to_clear.append(j)
        elif not text and indices_to_clear:
            # Empty paragraph after list items — stop here
            break

    # Get formatting from existing list items or the heading
    fmt = None
    if indices_to_clear:
        fmt = get_run_format(doc.paragraphs[indices_to_clear[0]])

    # Clear existing list items
    for idx in indices_to_clear:
        doc.paragraphs[idx].clear()

    # Write new entries
    # Reuse cleared paragraphs first, then we can't easily add new paragraphs
    # in the middle of a document, so write into existing slots
    for i, entry in enumerate(related_entries):
        formatted_entry = f"- {entry}"
        if i < len(indices_to_clear):
            para = doc.paragraphs[indices_to_clear[i]]
            para.clear()
            run = para.add_run(formatted_entry)
            if fmt:
                if fmt["name"]:
                    run.font.name = fmt["name"]
                if fmt["size"]:
                    run.font.size = fmt["size"]
        else:
            # Need more paragraphs than we cleared — append text to last used
            if indices_to_clear:
                last_para = doc.paragraphs[indices_to_clear[-1]]
                # Can't insert paragraphs mid-document easily with python-docx
                # So append to the last cleared paragraph
                last_para.text += f"\n{formatted_entry}"
            else:
                # No existing items — write after the heading
                heading_para = doc.paragraphs[para_idx]
                heading_para.text = f"Related SOPs:\n" + "\n".join(
                    f"- {e}" for e in related_entries
                )

    # Clear any remaining old entries beyond what we wrote
    for i in range(len(related_entries), len(indices_to_clear)):
        doc.paragraphs[indices_to_clear[i]].clear()

    return len(related_entries)


def update_pattern_b(doc, para_idx, related_entries):
    """Update Pattern B: replace Related SOPs within embedded metadata paragraph."""
    para = doc.paragraphs[para_idx]
    text = para.text

    # Find the 'Related SOPs:' section in the text
    match = re.search(r"Related SOPs:\s*", text)
    if not match:
        return 0

    start = match.start()
    end_of_related = match.end()

    # Find where Related SOPs content ends
    # It ends at 'Reference:', next metadata field, or end of string
    rest = text[end_of_related:]
    # Look for the next metadata field after Related SOPs
    next_field = re.search(
        r"\n(?:Reference|Training|Job Description|Management Directive|"
        r"Department|Created|Effective|Version|Appendix|Purpose|Scope|"
        r"={3,})", rest
    )

    if next_field:
        content_end = end_of_related + next_field.start()
    else:
        content_end = len(text)

    # Build new Related SOPs content
    new_related = "; ".join(related_entries)

    # Replace in the text
    new_text = text[:end_of_related] + new_related + text[content_end:]

    # Preserve formatting — clear and rewrite with original format
    fmt = get_run_format(para)
    para.clear()
    run = para.add_run(new_text)
    if fmt:
        if fmt["name"]:
            run.font.name = fmt["name"]
        if fmt["size"]:
            run.font.size = fmt["size"]

    return len(related_entries)


def process_documents(sop_dir, mapping):
    """Process all .docx files and update Related SOPs."""
    files = [
        f for f in sorted(os.listdir(sop_dir))
        if f.endswith(".docx") and not f.startswith("~")
    ]

    updated = 0
    skipped = 0
    no_section = 0
    no_mapping = 0
    errors = 0

    pattern_counts = {"A": 0, "B": 0, "C": 0}

    for fname in files:
        sop_id = extract_sop_id(fname)
        if not sop_id:
            skipped += 1
            continue

        if sop_id not in mapping:
            no_mapping += 1
            continue

        related_str = mapping[sop_id]
        related_entries = format_related_list(related_str)

        filepath = os.path.join(sop_dir, fname)

        try:
            doc = Document(filepath)
            pattern, para_idx = find_related_sops_pattern(doc)
            pattern_counts[pattern] += 1

            if pattern == "C":
                no_section += 1
                print(f"  NO SECTION: {sop_id} ({fname[:50]})")
                continue

            if pattern == "A":
                count = update_pattern_a(doc, para_idx, related_entries)
            else:  # Pattern B
                count = update_pattern_b(doc, para_idx, related_entries)

            doc.save(filepath)
            updated += 1
            print(f"  [OK] {sop_id} (pattern {pattern}, {count} related)")

        except Exception as e:
            errors += 1
            print(f"  [ERROR] {sop_id}: {e}")

    return updated, skipped, no_section, no_mapping, errors, pattern_counts


def main():
    print("Loading Related SOPs mapping...")
    mapping = load_mapping(CSV_PATH)
    print(f"  Loaded {len(mapping)} SOPs with relationships\n")

    print(f"Processing documents in {SOP_DIR}...\n")
    updated, skipped, no_section, no_mapping, errors, patterns = process_documents(
        SOP_DIR, mapping
    )

    print(f"\n{'='*50}")
    print(f"  DOCUMENT UPDATE COMPLETE")
    print(f"{'='*50}")
    print(f"  Updated:    {updated} documents")
    print(f"  Skipped:    {skipped} (no SOP ID in filename)")
    print(f"  No section: {no_section} (no Related SOPs section found)")
    print(f"  No mapping: {no_mapping} (SOP not in CSV)")
    print(f"  Errors:     {errors}")
    print(f"\n  Pattern distribution:")
    print(f"    Pattern A (standalone heading): {patterns['A']}")
    print(f"    Pattern B (embedded paragraph): {patterns['B']}")
    print(f"    Pattern C (not found):          {patterns['C']}")


if __name__ == "__main__":
    main()
