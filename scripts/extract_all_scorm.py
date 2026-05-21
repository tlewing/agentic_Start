"""
Job 01 Full Run — Bulk SCORM Extraction Script
Extracts title, description, lesson structure, quiz/KC presence from all SCORM packages.
Outputs consolidated JSON for skill mapping and per-course sheet generation.
"""
import base64, json, re, os, sys, csv, tempfile, zipfile
from html.parser import HTMLParser
from pathlib import Path

SCORM_DIR = r"C:\Users\tewing\OneDrive - GSL Electric\Projects\training-template\reference\scorm"
OUTPUT_DIR = os.path.join(tempfile.gettempdir(), "scorm_full_extract")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
    def handle_data(self, data):
        d = data.strip()
        if d:
            self.text.append(d)
    def get_text(self):
        return " ".join(self.text)

def strip_html(html_str):
    if not html_str:
        return ""
    ext = TextExtractor()
    try:
        ext.feed(str(html_str))
    except:
        return str(html_str)[:200]
    return ext.get_text()

def extract_manifest_title(zf):
    """Read title from imsmanifest.xml inside the zip."""
    try:
        with zf.open("imsmanifest.xml") as f:
            content = f.read().decode("utf-8", errors="replace")
        # Extract organization title
        m = re.search(r"<organization[^>]*>.*?<title>([^<]+)</title>", content, re.DOTALL)
        if m:
            return m.group(1).strip()
    except (KeyError, Exception):
        pass
    return None

def decode_locale(zf):
    """Find and decode Rise 360 locale file from zip."""
    locale_files = [n for n in zf.namelist() if re.match(r"scormcontent/locales/\w+\.js$", n)]
    if not locale_files:
        return None

    for lf in locale_files:
        try:
            content = zf.read(lf).decode("utf-8", errors="replace")
            match = re.search(r'__resolveJsonp\([^,]+,\s*"([^"]+)"\)', content)
            if match:
                decoded = base64.b64decode(match.group(1))
                return json.loads(decoded)
        except Exception:
            continue
    return None

def analyze_course(data):
    """Analyze decoded Rise 360 course data."""
    c = data.get("course", data)
    result = {
        "title": c.get("title", ""),
        "description": strip_html(c.get("description", "")),
        "lesson_count": 0,
        "lesson_titles": [],
        "has_quiz": False,
        "has_knowledge_check": False,
        "has_interactive": False,
        "has_video": False,
        "item_types": set(),
        "video_titles": [],
        "text_snippets": [],
    }

    lessons = c.get("lessons", [])
    result["lesson_count"] = len(lessons)

    for lesson in lessons:
        ltitle = lesson.get("title", "")
        result["lesson_titles"].append(ltitle)

        for item in lesson.get("items", []):
            itype = item.get("type", "")
            result["item_types"].add(itype)

            # Check for quizzes
            if item.get("questions"):
                result["has_quiz"] = True
            if itype == "knowledgeCheck":
                result["has_knowledge_check"] = True
            if itype == "interactive":
                result["has_interactive"] = True

            # Extract text snippets (first 5 meaningful ones)
            sub_items = item.get("items", [])
            for si in sub_items:
                for field in ("heading", "paragraph", "content"):
                    val = si.get(field, "")
                    if val:
                        text = strip_html(val)
                        if len(text) > 20 and len(result["text_snippets"]) < 8:
                            result["text_snippets"].append(text[:300])

                # Videos
                media = si.get("media", {})
                embed = media.get("embed", {})
                if embed.get("src"):
                    result["has_video"] = True
                    title_m = re.search(r'title="([^"]*)"', embed["src"])
                    if title_m:
                        result["video_titles"].append(title_m.group(1))
                if media.get("video"):
                    result["has_video"] = True
                    vname = media["video"].get("originalName", "")
                    if vname:
                        result["video_titles"].append(vname)

    result["item_types"] = list(result["item_types"])
    return result

def process_zip(zip_path):
    """Process a single SCORM zip file."""
    fname = os.path.basename(zip_path)
    slug = fname.rsplit(".zip", 1)[0]

    # Skip (1) duplicates
    if slug.endswith(" (1)"):
        return None

    entry = {
        "filename": fname,
        "slug": slug,
        "is_uuid": bool(re.match(r"^[0-9a-f]{8}-", slug)),
        "manifest_title": None,
        "has_locale": False,
        "course_data": None,
        "error": None,
    }

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            # Get manifest title
            entry["manifest_title"] = extract_manifest_title(zf)

            # Try locale decode
            data = decode_locale(zf)
            if data:
                entry["has_locale"] = True
                entry["course_data"] = analyze_course(data)
            else:
                # Check for embedded video/content without locale
                assets = [n for n in zf.namelist() if "assets/" in n and (n.endswith(".mp4") or n.endswith(".mp3"))]
                entry["course_data"] = {
                    "title": entry["manifest_title"] or slug,
                    "description": "",
                    "lesson_count": 0,
                    "lesson_titles": [],
                    "has_quiz": False,
                    "has_knowledge_check": False,
                    "has_interactive": False,
                    "has_video": bool(assets),
                    "item_types": [],
                    "video_titles": [os.path.basename(a) for a in assets],
                    "text_snippets": [],
                    "note": "No locale file — older Rise 360 or video-only package"
                }
    except Exception as e:
        entry["error"] = str(e)

    return entry

def main():
    zips = sorted(Path(SCORM_DIR).glob("*.zip"))
    print(f"Processing {len(zips)} SCORM packages...")

    results = []
    errors = []
    skipped = 0

    for i, zp in enumerate(zips):
        if i % 25 == 0:
            print(f"  {i}/{len(zips)}...")

        entry = process_zip(str(zp))
        if entry is None:
            skipped += 1
            continue
        if entry.get("error"):
            errors.append(entry)
        else:
            results.append(entry)

    # Save full results
    out_path = os.path.join(OUTPUT_DIR, "scorm_full_extract.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)

    # Summary CSV
    csv_path = os.path.join(OUTPUT_DIR, "scorm_summary.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Slug", "Title", "UUID", "Locale", "Lessons", "Quiz", "KC", "Interactive", "Video", "Description_50"])
        for r in results:
            cd = r.get("course_data", {})
            title = cd.get("title") or r.get("manifest_title") or r["slug"]
            w.writerow([
                r["slug"],
                title,
                "Y" if r["is_uuid"] else "",
                "Y" if r["has_locale"] else "",
                cd.get("lesson_count", 0),
                "Y" if cd.get("has_quiz") else "",
                "Y" if cd.get("has_knowledge_check") else "",
                "Y" if cd.get("has_interactive") else "",
                "Y" if cd.get("has_video") else "",
                cd.get("description", "")[:50],
            ])

    print(f"\nDone. {len(results)} processed, {skipped} skipped (dupes), {len(errors)} errors.")
    print(f"Full JSON: {out_path}")
    print(f"Summary CSV: {csv_path}")

    # Quick stats
    with_locale = sum(1 for r in results if r["has_locale"])
    with_quiz = sum(1 for r in results if r.get("course_data", {}).get("has_quiz"))
    with_kc = sum(1 for r in results if r.get("course_data", {}).get("has_knowledge_check"))
    uuids = sum(1 for r in results if r["is_uuid"])

    print(f"\nStats:")
    print(f"  With locale (content extractable): {with_locale}")
    print(f"  Without locale (video-only/older): {len(results) - with_locale}")
    print(f"  UUID-named (no descriptive slug): {uuids}")
    print(f"  With quiz: {with_quiz}")
    print(f"  With knowledge check: {with_kc}")

    if errors:
        print(f"\nErrors:")
        for e in errors:
            print(f"  {e['slug']}: {e['error']}")

if __name__ == "__main__":
    main()
