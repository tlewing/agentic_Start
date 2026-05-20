"""
SCORM Content Extractor
Extracts readable content from SCORM packages for the taxonomy pass.
Handles Rise 360, Storyline, and generic SCORM formats.
"""
import zipfile, os, json, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser


class TextExtractor(HTMLParser):
    """Extract visible text from HTML, ignoring scripts/styles."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_tags = {'script', 'style', 'noscript'}
        self.current_skip = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.skip_tags:
            self.current_skip += 1

    def handle_endtag(self, tag):
        if tag.lower() in self.skip_tags:
            self.current_skip = max(0, self.current_skip - 1)

    def handle_data(self, data):
        if self.current_skip == 0:
            text = data.strip()
            if text and len(text) > 2:
                self.text_parts.append(text)

    def get_text(self):
        return "\n".join(self.text_parts)


def extract_html_text(content):
    """Extract text from HTML content."""
    extractor = TextExtractor()
    try:
        extractor.feed(content)
    except Exception:
        pass
    return extractor.get_text()


def extract_vtt_text(content):
    """Extract plain text and timecodes from WebVTT content."""
    lines = content.split('\n')
    cues = []
    current_time = None
    current_text = []

    for line in lines:
        line = line.strip()
        if '-->' in line:
            if current_time and current_text:
                cues.append({'time': current_time, 'text': ' '.join(current_text)})
            current_time = line.split('-->')[0].strip()
            current_text = []
        elif line and not line.startswith('WEBVTT') and not line.startswith('NOTE') and not re.match(r'^\d+$', line):
            # Strip HTML tags from VTT cues
            clean = re.sub(r'<[^>]+>', '', line)
            if clean.strip():
                current_text.append(clean.strip())

    if current_time and current_text:
        cues.append({'time': current_time, 'text': ' '.join(current_text)})

    full_text = ' '.join(c['text'] for c in cues)
    return {'cues': cues, 'full_text': full_text, 'cue_count': len(cues)}


def extract_rise360_content(zf, names):
    """Extract content from Rise 360 SCORM packages."""
    text_parts = []

    # Rise 360 stores content in HTML files and sometimes data.js
    html_files = sorted([n for n in names if n.lower().endswith(('.html', '.htm'))
                        and 'scormdriver' not in n.lower()
                        and 'scormcontent' not in n.lower()])

    # Check for index.html or story_html5.html (Storyline) or lib/ (Rise)
    is_rise = any('lib/main.bundle' in n.lower() for n in names)
    is_storyline = any('story_content' in n.lower() for n in names)

    # For Rise 360, look for content in the main HTML
    content_files = [n for n in names if n.lower().endswith('.html') and 'index' in n.lower()]
    if not content_files:
        content_files = [n for n in names if n.lower().endswith('.html')]

    for fname in content_files[:5]:
        try:
            with zf.open(fname) as f:
                html = f.read().decode('utf-8', errors='ignore')
                text = extract_html_text(html)
                if len(text) > 50:
                    text_parts.append(f"--- {fname} ---\n{text}")
        except Exception:
            pass

    # Look for JSON data files (Rise 360 lesson content)
    json_files = [n for n in names if n.lower().endswith('.json')
                  and ('lesson' in n.lower() or 'content' in n.lower() or 'course' in n.lower())]
    for fname in json_files[:5]:
        try:
            with zf.open(fname) as f:
                data = json.loads(f.read().decode('utf-8', errors='ignore'))
                text = json.dumps(data, indent=2)
                # Extract text values from JSON
                texts = extract_json_texts(data)
                if texts:
                    text_parts.append(f"--- {fname} (JSON texts) ---\n" + "\n".join(texts[:100]))
        except Exception:
            pass

    # Look for data.js (common in Rise/Storyline)
    data_js = [n for n in names if n.lower().endswith('data.js') or n.lower() == 'data.js']
    for fname in data_js[:2]:
        try:
            with zf.open(fname) as f:
                content = f.read().decode('utf-8', errors='ignore')
                # Extract string literals
                strings = re.findall(r'"([^"]{20,500})"', content)
                if strings:
                    text_parts.append(f"--- {fname} (strings) ---\n" + "\n".join(strings[:50]))
        except Exception:
            pass

    return "\n\n".join(text_parts), is_rise, is_storyline


def extract_json_texts(obj, depth=0):
    """Recursively extract text strings from JSON objects."""
    texts = []
    if depth > 10:
        return texts
    if isinstance(obj, str) and len(obj) > 20:
        # Strip HTML
        clean = re.sub(r'<[^>]+>', ' ', obj).strip()
        clean = re.sub(r'\s+', ' ', clean)
        if len(clean) > 20:
            texts.append(clean)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() in ('text', 'title', 'description', 'body', 'content',
                           'heading', 'paragraph', 'label', 'caption', 'alt'):
                texts.extend(extract_json_texts(v, depth + 1))
            elif isinstance(v, (dict, list)):
                texts.extend(extract_json_texts(v, depth + 1))
    elif isinstance(obj, list):
        for item in obj:
            texts.extend(extract_json_texts(item, depth + 1))
    return texts


def extract_content(zip_path):
    """Extract all readable content from a SCORM package."""
    result = {
        'manifest_title': None,
        'manifest_items': [],
        'manifest_metadata': {},
        'content_text': '',
        'vtt_data': [],
        'media_refs': [],
        'format': 'unknown',
        'file_count': 0,
    }

    with zipfile.ZipFile(zip_path, 'r') as zf:
        names = zf.namelist()
        result['file_count'] = len(names)

        # 1. Parse manifest
        manifest_file = None
        for n in names:
            if n.lower().endswith('imsmanifest.xml'):
                manifest_file = n
                break

        if manifest_file:
            with zf.open(manifest_file) as mf:
                tree = ET.parse(mf)
                root = tree.getroot()
                ns = ''
                if root.tag.startswith('{'):
                    ns = root.tag.split('}')[0] + '}'

                # Organization items
                orgs = root.find(f'{ns}organizations')
                if orgs is not None:
                    org = orgs.find(f'{ns}organization')
                    if org is not None:
                        t = org.find(f'{ns}title')
                        if t is not None and t.text:
                            result['manifest_title'] = t.text.strip()
                        for item in org.iter(f'{ns}item'):
                            it = item.find(f'{ns}title')
                            if it is not None and it.text:
                                result['manifest_items'].append(it.text.strip())

                # LOM metadata
                for elem in root.iter():
                    tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                    if tag == 'description':
                        for child in elem:
                            if child.text and child.text.strip():
                                result['manifest_metadata']['description'] = child.text.strip()
                    elif tag == 'keyword':
                        for child in elem:
                            if child.text and child.text.strip():
                                kw = result['manifest_metadata'].get('keywords', [])
                                kw.append(child.text.strip())
                                result['manifest_metadata']['keywords'] = kw

        # 2. Extract VTT transcripts
        vtt_files = [n for n in names if n.lower().endswith('.vtt')]
        for vtt_file in vtt_files:
            try:
                with zf.open(vtt_file) as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    vtt_data = extract_vtt_text(content)
                    vtt_data['file'] = vtt_file
                    result['vtt_data'].append(vtt_data)
            except Exception:
                pass

        # 3. Extract HTML/JS content
        content_text, is_rise, is_storyline = extract_rise360_content(zf, names)
        result['content_text'] = content_text
        if is_rise:
            result['format'] = 'rise360'
        elif is_storyline:
            result['format'] = 'storyline'
        else:
            result['format'] = 'generic'

        # 4. Find video/media references
        for n in names[:50]:
            if any(n.lower().endswith(ext) for ext in ['.html', '.htm', '.js']):
                try:
                    with zf.open(n) as f:
                        content = f.read().decode('utf-8', errors='ignore')
                        # SharePoint/Stream URLs
                        urls = re.findall(r'https://[^\s"\'<>]+(?:sharepoint|microsoftstream|blob\.core\.windows\.net)[^\s"\'<>]+', content, re.I)
                        result['media_refs'].extend(urls)
                except Exception:
                    pass

        result['media_refs'] = list(set(result['media_refs']))[:20]

    return result


if __name__ == '__main__':
    # Test with one file
    if len(sys.argv) > 1:
        path = sys.argv[1]
        result = extract_content(path)
        print(json.dumps({
            'title': result['manifest_title'],
            'items': result['manifest_items'],
            'metadata': result['manifest_metadata'],
            'format': result['format'],
            'files': result['file_count'],
            'vtt_count': len(result['vtt_data']),
            'content_length': len(result['content_text']),
            'media_refs': result['media_refs'][:5],
        }, indent=2))
        if result['content_text']:
            print(f"\n--- Content preview (first 2000 chars) ---")
            print(result['content_text'][:2000])
        if result['vtt_data']:
            for vtt in result['vtt_data']:
                print(f"\n--- VTT: {vtt['file']} ({vtt['cue_count']} cues) ---")
                print(vtt['full_text'][:1000])
