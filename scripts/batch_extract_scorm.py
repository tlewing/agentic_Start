"""Batch extract course content from all SCORM ZIPs in a folder"""
import os
import re
import json
import base64
import zipfile
import html as html_lib
import sys


def strip_html(text):
    if not text or not isinstance(text, str):
        return ""
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = html_lib.unescape(clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


def extract_course_data_from_string(b64_data):
    """Decode base64 course data"""
    decoded = base64.b64decode(b64_data)
    return json.loads(decoded.decode('utf-8'))


def extract_course_data(html_content, zf=None, zip_namelist=None):
    """Try multiple methods to find Rise 360 course data"""
    # Method 1: inline deserialize("base64...")
    match = re.search(r'deserialize\("([A-Za-z0-9+/=]+)"\)', html_content)
    if match:
        return extract_course_data_from_string(match.group(1))

    # Method 2: locales/en.js file (newer Rise 360)
    if zf and zip_namelist:
        locale_files = [n for n in zip_namelist if 'locales/en.js' in n]
        if locale_files:
            locale_content = zf.read(locale_files[0]).decode('utf-8', errors='replace')
            match = re.search(r'__resolveJsonp\([^,]+,"([A-Za-z0-9+/=]+)"\)', locale_content)
            if match:
                return extract_course_data_from_string(match.group(1))

    return None


def extract_text_from_blocks(items, depth=0):
    texts = []
    indent = "  " * depth
    for item in items:
        if not isinstance(item, dict):
            continue
        block_type = item.get('type', '')
        title = strip_html(item.get('title', ''))
        body = strip_html(item.get('body', ''))
        description = strip_html(item.get('description', ''))
        question = strip_html(item.get('question', ''))

        if title:
            texts.append(f"{indent}[{block_type}] {title}")
        if body:
            texts.append(f"{indent}  {body}")
        if description:
            texts.append(f"{indent}  {description}")
        if question:
            texts.append(f"{indent}  Q: {question}")

        for key in ['answers', 'choices', 'options']:
            answers = item.get(key, [])
            if isinstance(answers, list):
                for ans in answers:
                    if isinstance(ans, dict):
                        ans_text = strip_html(ans.get('text', ans.get('title', ans.get('body', ''))))
                        is_correct = ans.get('correct', ans.get('isCorrect', False))
                        marker = " *" if is_correct else ""
                        if ans_text:
                            texts.append(f"{indent}    - {ans_text}{marker}")

        statements = item.get('statements', [])
        if isinstance(statements, list):
            for stmt in statements:
                if isinstance(stmt, dict):
                    stmt_text = strip_html(stmt.get('text', stmt.get('statement', '')))
                    if stmt_text:
                        texts.append(f"{indent}    > {stmt_text}")

        if 'items' in item and isinstance(item['items'], list):
            texts.extend(extract_text_from_blocks(item['items'], depth + 1))

        if 'variants' in item and isinstance(item['variants'], list):
            for variant in item['variants']:
                if not isinstance(variant, dict):
                    continue
                vtitle = strip_html(variant.get('title', ''))
                vbody = strip_html(variant.get('body', ''))
                if vtitle:
                    texts.append(f"{indent}  >> {vtitle}")
                if vbody:
                    texts.append(f"{indent}     {vbody}")
                if 'items' in variant and isinstance(variant['items'], list):
                    texts.extend(extract_text_from_blocks(variant['items'], depth + 2))

        for key in ['markers', 'hotspots', 'labels']:
            markers = item.get(key, [])
            if isinstance(markers, list):
                for m in markers:
                    if isinstance(m, dict):
                        mlabel = strip_html(m.get('label', m.get('title', '')))
                        mbody = strip_html(m.get('body', m.get('description', '')))
                        if mlabel:
                            texts.append(f"{indent}  * {mlabel}")
                        if mbody:
                            texts.append(f"{indent}    {mbody}")
    return texts


def process_zip(zip_path, output_dir):
    filename = os.path.basename(zip_path)
    print(f"\n{'='*70}")
    print(f"FILE: {filename}")
    print(f"{'='*70}")

    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # Find index.html
            html_files = [n for n in zf.namelist() if n.endswith('index.html') and 'scormcontent' in n]
            if not html_files:
                html_files = [n for n in zf.namelist() if n.endswith('index.html')]
            if not html_files:
                print("  ERROR: No index.html found")
                return None

            html_content = zf.read(html_files[0]).decode('utf-8', errors='replace')
            namelist = zf.namelist()

            # Also read imsmanifest.xml for title
            manifest_title = ""
            manifest_files = [n for n in namelist if n.endswith('imsmanifest.xml')]
            if manifest_files:
                manifest = zf.read(manifest_files[0]).decode('utf-8', errors='replace')
                title_match = re.search(r'<title>([^<]+)</title>', manifest)
                if title_match:
                    manifest_title = html_lib.unescape(title_match.group(1))

            data = extract_course_data(html_content, zf, namelist)

    except Exception as e:
        print(f"  ERROR reading ZIP: {e}")
        return None
    if not data:
        print(f"  WARNING: No Rise 360 course data found (may be non-Rise SCORM)")
        print(f"  Manifest title: {manifest_title}")
        return {"filename": filename, "title": manifest_title, "type": "non-rise", "lessons": []}

    course = data.get('course', {})
    title = course.get('title', manifest_title or 'Unknown')
    print(f"  Title: {title}")

    lessons = course.get('lessons', [])
    print(f"  Lessons: {len(lessons)}")

    result = {
        "filename": filename,
        "title": title,
        "type": "rise360",
        "lessons": []
    }

    for i, lesson in enumerate(lessons, 1):
        ltitle = lesson.get('title', 'Untitled')
        items = lesson.get('items', [])
        texts = extract_text_from_blocks(items)

        # Block type summary
        block_types = [item.get('type', '?') for item in items if isinstance(item, dict)]

        lesson_data = {
            "number": i,
            "title": ltitle,
            "block_count": len(items),
            "block_types": block_types,
            "content": texts
        }
        result["lessons"].append(lesson_data)

        print(f"  Lesson {i}: {ltitle} ({len(items)} blocks: {', '.join(set(block_types))})")

    # Write extracted content to file
    safe_name = re.sub(r'[^\w\-]', '_', title)[:80]
    output_path = os.path.join(output_dir, f"{safe_name}.txt")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"COURSE: {title}\n")
        f.write(f"SOURCE: {filename}\n")
        f.write(f"TYPE: {result['type']}\n")
        f.write(f"LESSONS: {len(lessons)}\n")
        f.write("=" * 70 + "\n\n")

        for lesson_data in result["lessons"]:
            f.write(f"LESSON {lesson_data['number']}: {lesson_data['title']}\n")
            f.write(f"Blocks: {lesson_data['block_count']} ({', '.join(set(lesson_data['block_types']))})\n")
            f.write("-" * 50 + "\n")
            for text in lesson_data["content"]:
                f.write(text + "\n")
            f.write("\n")

    print(f"  Saved to: {output_path}")
    return result


def main():
    scorm_dir = r"C:\Users\tewing\Desktop\SCORM Files"
    output_dir = os.path.join(scorm_dir, "extracted")
    os.makedirs(output_dir, exist_ok=True)

    zip_files = [f for f in os.listdir(scorm_dir)
                 if f.endswith('.zip') and os.path.isfile(os.path.join(scorm_dir, f))]

    print(f"Found {len(zip_files)} SCORM packages")
    print(f"Output: {output_dir}")

    results = []
    for zf in sorted(zip_files):
        zip_path = os.path.join(scorm_dir, zf)
        result = process_zip(zip_path, output_dir)
        if result:
            results.append(result)

    # Summary
    print("\n\n" + "=" * 70)
    print("BATCH SUMMARY")
    print("=" * 70)
    print(f"Processed: {len(results)}/{len(zip_files)}")
    for r in results:
        lesson_count = len(r['lessons'])
        print(f"  [{r['type']}] {r['title']} ({lesson_count} lessons) <- {r['filename']}")


if __name__ == "__main__":
    main()
