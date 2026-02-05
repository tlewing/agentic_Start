"""
Validate SOPs against Policy Manual (Job Descriptions & Management Directives)
Generates an issues log for any SOPs that don't align with scope.
"""
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import json
import re
from datetime import datetime

BASE_DIR = Path(r"C:\Users\tewing\Desktop\Holding\SOP")
SOURCE_DIR = BASE_DIR / "SharePoint-SOPs"
REFERENCE_FILE = BASE_DIR / "docs" / "policy_reference.json"
ISSUES_LOG = BASE_DIR / "docs" / "sop_validation_issues.md"
VALIDATION_REPORT = BASE_DIR / "docs" / "sop_validation_report.json"


def load_reference():
    """Load the policy reference data."""
    with open(REFERENCE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_text_from_docx(docx_path):
    """Extract plain text from a docx file."""
    try:
        with zipfile.ZipFile(docx_path, 'r') as zf:
            xml_content = zf.read('word/document.xml').decode('utf-8')
            root = ET.fromstring(xml_content)
            text_parts = []
            for elem in root.iter():
                if elem.text:
                    text_parts.append(elem.text)
            return ' '.join(text_parts)
    except Exception as e:
        return f"[ERROR: {e}]"


def extract_sop_info(text, filename):
    """Extract SOP ID, title, roles, and keywords from SOP text."""
    info = {
        'filename': filename,
        'sop_id': '',
        'title': '',
        'phase': '',
        'roles_mentioned': [],
        'keywords': [],
        'has_purpose': False,
        'has_scope': False,
        'has_roles': False,
        'has_procedure': False,
        'has_appendix': False
    }

    # Extract SOP ID from filename or content
    id_match = re.search(r'(9\.\d+\.?\d*)', filename)
    if id_match:
        info['sop_id'] = id_match.group(1)
        # Determine phase
        phase_match = re.match(r'9\.(\d)', info['sop_id'])
        if phase_match:
            info['phase'] = f"9.{phase_match.group(1)}"

    # Extract title
    title_match = re.search(r'9\.\d+\.?\d*\s*[–-]\s*(.+?)(?:\.docx|$)', filename)
    if title_match:
        info['title'] = title_match.group(1).strip()

    text_lower = text.lower()

    # Check for required sections
    info['has_purpose'] = 'purpose' in text_lower
    info['has_scope'] = 'scope' in text_lower
    info['has_roles'] = 'roles' in text_lower or 'responsibilities' in text_lower
    info['has_procedure'] = 'procedure' in text_lower or 'step' in text_lower
    info['has_appendix'] = 'appendix' in text_lower

    # Extract mentioned roles
    # Note: Field Supervisor = Foreman (same role)
    role_patterns = {
        'Project Manager': r'project\s*manager|PM\b',
        'General Superintendent': r'general\s*superintendent|GS\b',
        'Foreman': r'foreman|field\s*supervisor',
        'Safety': r'safety\s*(rep|coordinator|officer)?',
        'Estimator': r'estimator|estimating',
        'Purchasing': r'purchas(ing|er)|buyer',
        'Prefab': r'prefab|pre-fab',
        'Admin': r'admin|administrative',
        'Lead Journeyman': r'lead\s*journeyman',
    }

    for role, pattern in role_patterns.items():
        if re.search(pattern, text_lower):
            info['roles_mentioned'].append(role)

    # Extract activity keywords
    activity_keywords = ['schedule', 'budget', 'cost', 'billing', 'change order',
                        'submittal', 'rfi', 'coordination', 'meeting', 'procurement',
                        'material', 'labor', 'safety', 'quality', 'documentation',
                        'closeout', 'commissioning', 'testing', 'inspection']

    for kw in activity_keywords:
        if kw in text_lower:
            info['keywords'].append(kw)

    return info


def validate_sop(sop_info, reference):
    """Validate an SOP against the policy reference."""
    issues = []
    warnings = []

    phase = sop_info['phase']
    phase_mapping = reference.get('sop_phase_mapping', {})

    # Check 1: Valid phase
    if phase not in phase_mapping:
        issues.append(f"Unknown phase: {phase}")
        return issues, warnings

    phase_info = phase_mapping[phase]
    expected_roles = phase_info['roles']

    # Check 2: Roles mentioned should align with phase
    for role in sop_info['roles_mentioned']:
        # Normalize role names for comparison
        role_normalized = role.replace(' ', '').lower()
        expected_normalized = [r.replace(' ', '').lower() for r in expected_roles]

        # Check if role is expected for this phase
        role_found = False
        for exp in expected_normalized:
            if role_normalized in exp or exp in role_normalized:
                role_found = True
                break

        if not role_found:
            warnings.append(f"Role '{role}' mentioned but not typically associated with phase {phase} ({phase_info['name']})")

    # Check 3: Required sections
    if not sop_info['has_purpose']:
        issues.append("Missing 'Purpose' section")
    if not sop_info['has_scope']:
        issues.append("Missing 'Scope' section")
    if not sop_info['has_roles']:
        issues.append("Missing 'Roles & Responsibilities' section")
    if not sop_info['has_procedure']:
        issues.append("Missing 'Procedure' section")

    # Check 4: No roles mentioned at all
    if not sop_info['roles_mentioned']:
        warnings.append("No specific roles mentioned in the SOP")

    # Check 5: Cross-reference with management directives
    for directive in reference.get('management_directives', []):
        directive_scope = directive.get('scope', [])

        # Map phase to scope keywords
        phase_scope_map = {
            '9.1': ['estimating', 'bidding'],
            '9.2': ['pre-construction'],
            '9.3': ['mobilization'],
            '9.4': ['execution', 'field'],
            '9.5': ['commissioning'],
            '9.6': ['closeout']
        }

        # Check if SOP keywords align with directive keywords
        sop_keywords = set(sop_info['keywords'])
        directive_keywords = set(directive.get('keywords', []))

        if directive_scope:
            phase_scope = phase_scope_map.get(phase, [])
            scope_overlap = set(directive_scope) & set(phase_scope)

            if scope_overlap and directive_keywords:
                # This directive is relevant to this phase
                keyword_overlap = sop_keywords & directive_keywords
                if not keyword_overlap and len(sop_keywords) > 0:
                    # SOP has keywords but none match the directive
                    pass  # This is okay - not all SOPs need to match all directives

    # Check 6: Activity keywords should align with phase
    phase_expected_keywords = {
        '9.1': ['cost', 'labor', 'material', 'schedule'],
        '9.2': ['schedule', 'budget', 'coordination', 'meeting', 'safety'],
        '9.3': ['coordination', 'material', 'safety'],
        '9.4': ['schedule', 'budget', 'billing', 'change order', 'coordination', 'safety', 'quality'],
        '9.5': ['testing', 'commissioning', 'inspection', 'quality'],
        '9.6': ['closeout', 'documentation', 'quality']
    }

    if phase in phase_expected_keywords:
        expected_kw = set(phase_expected_keywords[phase])
        actual_kw = set(sop_info['keywords'])

        # Check for unexpected keywords that suggest wrong phase
        phase_specific = {
            'estimating': '9.1',
            'bidding': '9.1',
            'commissioning': '9.5',
            'testing': '9.5',
            'closeout': '9.6'
        }

        for kw, expected_phase in phase_specific.items():
            if kw in actual_kw and phase != expected_phase:
                warnings.append(f"Keyword '{kw}' typically belongs in phase {expected_phase}, but this SOP is in {phase}")

    return issues, warnings


def main():
    print("=" * 60)
    print("SOP VALIDATION AGAINST POLICY MANUAL")
    print("=" * 60)

    # Load reference
    reference = load_reference()
    print(f"Loaded reference with {len(reference['job_descriptions'])} job descriptions")
    print(f"and {len(reference['management_directives'])} management directives")

    # Get all SOPs
    sop_files = list(SOURCE_DIR.glob("*.docx"))
    print(f"\nValidating {len(sop_files)} SOPs...")

    results = []
    issues_count = 0
    warnings_count = 0

    for sop_file in sorted(sop_files):
        text = extract_text_from_docx(sop_file)
        sop_info = extract_sop_info(text, sop_file.name)
        issues, warnings = validate_sop(sop_info, reference)

        result = {
            'sop_id': sop_info['sop_id'],
            'title': sop_info['title'],
            'filename': sop_info['filename'],
            'phase': sop_info['phase'],
            'roles_mentioned': sop_info['roles_mentioned'],
            'keywords': sop_info['keywords'],
            'issues': issues,
            'warnings': warnings,
            'status': 'ERROR' if issues else ('WARNING' if warnings else 'OK')
        }
        results.append(result)

        issues_count += len(issues)
        warnings_count += len(warnings)

        # Print progress for items with issues
        if issues or warnings:
            status = "ERROR" if issues else "WARNING"
            print(f"  [{status}] {sop_info['sop_id']} - {sop_info['title'][:40]}")

    # Generate issues log (Markdown)
    print(f"\nGenerating issues log...")

    with open(ISSUES_LOG, 'w', encoding='utf-8') as f:
        f.write(f"# SOP Validation Issues Log\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**Summary:**\n")
        f.write(f"- Total SOPs: {len(results)}\n")
        f.write(f"- SOPs with errors: {sum(1 for r in results if r['issues'])}\n")
        f.write(f"- SOPs with warnings: {sum(1 for r in results if r['warnings'] and not r['issues'])}\n")
        f.write(f"- SOPs OK: {sum(1 for r in results if r['status'] == 'OK')}\n\n")

        f.write("---\n\n")

        # Errors first
        errors = [r for r in results if r['issues']]
        if errors:
            f.write("## Errors (Must Fix)\n\n")
            for r in errors:
                f.write(f"### {r['sop_id']} – {r['title']}\n\n")
                f.write(f"**Phase:** {r['phase']}\n\n")
                f.write("**Issues:**\n")
                for issue in r['issues']:
                    f.write(f"- ❌ {issue}\n")
                if r['warnings']:
                    f.write("\n**Warnings:**\n")
                    for warning in r['warnings']:
                        f.write(f"- ⚠️ {warning}\n")
                f.write("\n---\n\n")

        # Warnings
        warnings = [r for r in results if r['warnings'] and not r['issues']]
        if warnings:
            f.write("## Warnings (Review Recommended)\n\n")
            for r in warnings:
                f.write(f"### {r['sop_id']} – {r['title']}\n\n")
                f.write(f"**Phase:** {r['phase']}\n\n")
                f.write("**Warnings:**\n")
                for warning in r['warnings']:
                    f.write(f"- ⚠️ {warning}\n")
                f.write("\n---\n\n")

        # Summary by phase
        f.write("## Summary by Phase\n\n")
        for phase in ['9.1', '9.2', '9.3', '9.4', '9.5', '9.6']:
            phase_results = [r for r in results if r['phase'] == phase]
            phase_errors = sum(1 for r in phase_results if r['issues'])
            phase_warnings = sum(1 for r in phase_results if r['warnings'] and not r['issues'])
            phase_ok = sum(1 for r in phase_results if r['status'] == 'OK')
            phase_name = reference['sop_phase_mapping'].get(phase, {}).get('name', 'Unknown')

            f.write(f"| {phase} | {phase_name} | {len(phase_results)} | {phase_errors} | {phase_warnings} | {phase_ok} |\n")

    # Save detailed JSON report
    with open(VALIDATION_REPORT, 'w', encoding='utf-8') as f:
        json.dump({
            'generated': datetime.now().isoformat(),
            'summary': {
                'total': len(results),
                'errors': sum(1 for r in results if r['issues']),
                'warnings': sum(1 for r in results if r['warnings'] and not r['issues']),
                'ok': sum(1 for r in results if r['status'] == 'OK')
            },
            'results': results
        }, f, indent=2)

    print(f"\n--- VALIDATION COMPLETE ---")
    print(f"Total SOPs: {len(results)}")
    print(f"Errors: {sum(1 for r in results if r['issues'])}")
    print(f"Warnings: {sum(1 for r in results if r['warnings'] and not r['issues'])}")
    print(f"OK: {sum(1 for r in results if r['status'] == 'OK')}")
    print(f"\nIssues log: {ISSUES_LOG}")
    print(f"Full report: {VALIDATION_REPORT}")


if __name__ == "__main__":
    main()
