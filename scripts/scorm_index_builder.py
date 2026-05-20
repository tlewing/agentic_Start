"""
SCORM Course Index Builder
Enumerates all SCORM packages, extracts titles and media/transcript info.
Writes canonical JSON index for the taxonomy pass.
"""
import zipfile, os, json, sys, re
import xml.etree.ElementTree as ET
from pathlib import Path

SCORM_DIR = Path(r"C:\Users\tewing\OneDrive - GSL Electric\Projects\training-template\reference\scorm")
OUTPUT_PATH = Path(r"C:\Users\tewing\OneDrive - GSL Electric\Projects\GSL-Operations-Framework\data\scorm_course_index.json")
INBOX_DIR = Path(r"C:\Users\tewing\Desktop\InBox")

def extract_title_from_manifest(zf):
    """Extract course title from imsmanifest.xml inside a zip."""
    names = zf.namelist()
    manifest = None
    for n in names:
        if n.lower().endswith("imsmanifest.xml"):
            manifest = n
            break
    if not manifest:
        return None, "no imsmanifest.xml"

    with zf.open(manifest) as mf:
        tree = ET.parse(mf)
        root = tree.getroot()
        ns = ""
        if root.tag.startswith("{"):
            ns = root.tag.split("}")[0] + "}"

        # Try organization title
        orgs = root.find(f"{ns}organizations")
        if orgs is not None:
            org = orgs.find(f"{ns}organization")
            if org is not None:
                t = org.find(f"{ns}title")
                if t is not None and t.text and t.text.strip():
                    return t.text.strip(), None
                # Try first item title
                item = org.find(f"{ns}item")
                if item is not None:
                    t2 = item.find(f"{ns}title")
                    if t2 is not None and t2.text and t2.text.strip():
                        return t2.text.strip(), None

        # Try LOM metadata
        for elem in root.iter():
            tag_local = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if tag_local == "title":
                # LOM title has <langstring> child
                for child in elem:
                    if child.text and child.text.strip():
                        return child.text.strip(), None
                if elem.text and elem.text.strip():
                    return elem.text.strip(), None

    return None, "title not found in manifest"


def detect_media_and_transcripts(zf):
    """Detect video media and VTT transcripts inside a SCORM package."""
    names = zf.namelist()

    # Find VTT files
    vtt_files = [n for n in names if n.lower().endswith(".vtt")]

    # Find video files (bundled)
    video_exts = {".mp4", ".webm", ".ogv", ".m4v", ".mov"}
    video_files = [n for n in names if any(n.lower().endswith(ext) for ext in video_exts)]

    # Find SharePoint/Stream video references in HTML/JS files
    sp_refs = []
    html_js_files = [n for n in names if any(n.lower().endswith(ext) for ext in [".html", ".htm", ".js", ".json"])]

    # Sample a few key files for video references
    checked = 0
    for fname in html_js_files:
        if checked > 20:
            break
        try:
            with zf.open(fname) as f:
                content = f.read().decode("utf-8", errors="ignore")
                # SharePoint video URLs
                sp_matches = re.findall(r'https://[^\s"\'<>]+sharepoint[^\s"\'<>]+\.(?:mp4|webm)', content, re.IGNORECASE)
                sp_refs.extend(sp_matches)
                # Microsoft Stream
                stream_matches = re.findall(r'https://[^\s"\'<>]*(?:microsoftstream|web\.microsoftstream)[^\s"\'<>]+', content, re.IGNORECASE)
                sp_refs.extend(stream_matches)
                # Azure blob video
                blob_matches = re.findall(r'https://[^\s"\'<>]+blob\.core\.windows\.net[^\s"\'<>]+\.(?:mp4|webm)', content, re.IGNORECASE)
                sp_refs.extend(blob_matches)
                checked += 1
        except Exception:
            pass

    sp_refs = list(set(sp_refs))

    media_location = "none"
    if video_files and sp_refs:
        media_location = "bundled+external"
    elif video_files:
        media_location = "bundled"
    elif sp_refs:
        media_location = "external-reference"

    return {
        "media_location": media_location,
        "bundled_videos": video_files[:10],  # cap list
        "external_refs": sp_refs[:10],
        "vtt_files": vtt_files,
        "vtt_count": len(vtt_files),
        "transcript_status": "found-in-package" if vtt_files else "needs-investigation"
    }


def title_from_filename(filename):
    """Derive a human-readable title from the SCORM zip filename."""
    name = filename.replace(".zip", "")
    # Remove SCORM suffix hash
    name = re.sub(r'-scorm12-[a-zA-Z0-9_-]+$', '', name)
    # Remove trailing (1), (2) etc
    name = re.sub(r'\s*\(\d+\)$', '', name)
    # Replace hyphens with spaces, title case
    name = name.replace("-", " ").strip()
    return name.title() if name else filename


def build_index():
    zips = sorted([f for f in os.listdir(SCORM_DIR) if f.endswith(".zip")])
    print(f"Found {len(zips)} SCORM packages")

    # Load existing index if resuming
    existing = {}
    if OUTPUT_PATH.exists():
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            for rec in data.get("courses", []):
                if rec.get("status") == "done":
                    existing[rec["file"]] = rec

    courses = []
    errors = []

    for i, zf_name in enumerate(zips):
        # Skip already-done courses
        if zf_name in existing:
            courses.append(existing[zf_name])
            continue

        zf_path = os.path.join(SCORM_DIR, zf_name)
        try:
            with zipfile.ZipFile(zf_path, "r") as zf:
                title, err = extract_title_from_manifest(zf)
                media_info = detect_media_and_transcripts(zf)

                if title is None:
                    title = f"[FROM FILENAME] {title_from_filename(zf_name)}"
                    if err:
                        media_info["parse_error"] = err

                # Check if this is a GUID-named file (no descriptive name)
                is_guid = bool(re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', zf_name))

                courses.append({
                    "file": zf_name,
                    "title": title,
                    "is_guid_filename": is_guid,
                    "media_location": media_info["media_location"],
                    "bundled_videos": media_info.get("bundled_videos", []),
                    "external_refs": media_info.get("external_refs", []),
                    "vtt_count": media_info["vtt_count"],
                    "vtt_files": media_info["vtt_files"],
                    "transcript_status": media_info["transcript_status"],
                    "status": "pending",
                    "batch": None,
                    "parse_error": media_info.get("parse_error")
                })
        except Exception as e:
            errors.append({"file": zf_name, "error": str(e)})
            courses.append({
                "file": zf_name,
                "title": f"[ERROR] {title_from_filename(zf_name)}",
                "status": "error",
                "error": str(e)
            })

        if (i + 1) % 50 == 0:
            print(f"  Processed {i+1}/{len(zips)}...")

    # Deduplicate by title
    title_groups = {}
    for c in courses:
        t = c["title"]
        if t not in title_groups:
            title_groups[t] = []
        title_groups[t].append(c)

    # Write output
    output = {
        "generated": "2026-05-20",
        "scorm_dir": str(SCORM_DIR),
        "total_packages": len(zips),
        "parsed": len([c for c in courses if c["status"] != "error"]),
        "errors": len(errors),
        "unique_titles": len(title_groups),
        "duplicate_title_groups": {t: [c["file"] for c in cs] for t, cs in title_groups.items() if len(cs) > 1},
        "courses": courses
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nIndex written to {OUTPUT_PATH}")
    print(f"Total: {len(courses)} | Pending: {len([c for c in courses if c['status']=='pending'])} | Errors: {len(errors)}")

    # Summary stats
    media_stats = {}
    transcript_stats = {}
    for c in courses:
        ml = c.get("media_location", "unknown")
        media_stats[ml] = media_stats.get(ml, 0) + 1
        ts = c.get("transcript_status", "unknown")
        transcript_stats[ts] = transcript_stats.get(ts, 0) + 1

    print(f"\nMedia: {media_stats}")
    print(f"Transcripts: {transcript_stats}")

    dupes = output["duplicate_title_groups"]
    if dupes:
        print(f"\nDuplicate titles ({len(dupes)} groups):")
        for t, files in sorted(dupes.items()):
            print(f"  '{t}' x{len(files)}")

    return output


if __name__ == "__main__":
    build_index()
