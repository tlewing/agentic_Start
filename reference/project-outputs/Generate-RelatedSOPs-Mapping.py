"""
Generate Related SOPs Mapping
=============================
Scores all SOP pairs across 4 weighted layers and outputs a CSV
with 2-8 related SOPs per SOP for use in SharePoint and .docx updates.
"""

import csv
import os
import re
from collections import defaultdict
from itertools import combinations

# ============================================================
# CONFIG
# ============================================================
BASE_DIR = r"C:\Users\tewing\Desktop\Claude Projects\Project Outputs"
INPUT_CSV = os.path.join(BASE_DIR, "Authoritative_SOP_List.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "RelatedSOPs_Mapping.csv")

MIN_RELATED = 2
MAX_RELATED = 8
SCORE_THRESHOLD = 1.5
MAX_SAME_SUBCAT = 5

# ============================================================
# LAYER 1: FUNCTIONAL SUBCATEGORIES (weight 3.0)
# ============================================================
SUBCAT_WEIGHT = 3.0

SUBCATEGORIES = {
    "preconstruction": ["9.1.050"],
    "project_planning": [
        "9.2.005", "9.2.010", "9.2.015", "9.2.020", "9.2.030", "9.2.040",
        "9.2.050", "9.2.055", "9.2.057", "9.2.060", "9.2.070", "9.2.080",
        "9.2.090", "9.2.100", "9.2.110", "9.2.120", "9.2.130", "9.2.140",
        "9.2.160",
    ],
    "site_setup": [
        "9.3.010", "9.3.020", "9.3.030", "9.3.040", "9.3.050", "9.3.060",
        "9.3.070", "9.3.080", "9.3.090", "9.3.100", "9.3.110", "9.3.120",
        "9.3.470",
    ],
    "coordination_meetings": [
        "9.4.010", "9.4.020", "9.4.030", "9.4.040", "9.4.045",
        "9.4.050", "9.4.055", "9.4.060",
    ],
    "documentation_mgmt": [
        "9.4.190", "9.4.195", "9.4.200", "9.4.205", "9.4.210",
        "9.4.215", "9.4.220", "9.4.225", "9.4.230", "9.4.235", "9.4.240",
    ],
    "communications_mgmt": [
        "9.4.270", "9.4.275", "9.4.280", "9.4.285", "9.4.290",
        "9.4.295", "9.4.300", "9.4.305", "9.4.310",
    ],
    "schedule_mgmt": [
        "9.4.315", "9.4.320", "9.4.325", "9.4.330", "9.4.335",
        "9.4.340", "9.4.345", "9.4.350",
    ],
    "change_mgmt": [
        "9.4.355", "9.4.360", "9.4.365", "9.4.370", "9.4.375",
        "9.4.380", "9.4.385", "9.4.390",
    ],
    "cost_billing": [
        "9.4.400", "9.4.405", "9.4.410", "9.4.415", "9.4.420",
        "9.4.425", "9.4.430", "9.4.435", "9.4.440", "9.4.445",
        "9.4.450", "9.4.455", "9.4.460", "9.4.465",
    ],
    "safety_mgmt": [
        "9.3.470", "9.4.475", "9.4.480", "9.4.485", "9.4.490",
        "9.4.495", "9.4.500", "9.4.505", "9.4.510",
    ],
    "quality_mgmt": [
        "9.4.515", "9.4.520", "9.4.525", "9.4.530", "9.4.535",
        "9.4.540", "9.4.545",
    ],
    "resource_mgmt": [
        "9.4.560", "9.4.565", "9.4.570", "9.4.576", "9.4.580",
        "9.4.585", "9.4.590", "9.4.595",
    ],
    "procurement_mgmt": [
        "9.4.605", "9.4.610", "9.4.615", "9.4.620", "9.4.625",
        "9.4.630", "9.4.631", "9.4.635", "9.4.640", "9.4.645",
        "9.4.650", "9.4.655", "9.4.660", "9.4.665", "9.4.670",
    ],
    "field_operations": [
        "9.4.675", "9.4.680", "9.4.690", "9.4.695", "9.4.700",
        "9.4.705", "9.4.710", "9.4.715", "9.4.720", "9.4.725",
        "9.4.735", "9.4.745", "9.4.755",
    ],
    "commissioning": ["9.5.020", "9.5.550"],
    "closeout": [
        "9.6.005", "9.6.010", "9.6.015", "9.6.020", "9.6.030",
        "9.6.035", "9.6.040", "9.6.050", "9.6.065", "9.6.070",
        "9.6.080", "9.6.085",
    ],
}

# Build reverse lookup: sop_id -> list of subcategories
def build_subcat_lookup():
    lookup = defaultdict(list)
    for subcat, sop_ids in SUBCATEGORIES.items():
        for sid in sop_ids:
            lookup[sid].append(subcat)
    return lookup

# ============================================================
# LAYER 2: WORKFLOW DEPENDENCIES (weight 4.0)
# ============================================================
WORKFLOW_WEIGHT = 4.0

WORKFLOW_LINKS = [
    # Pre-construction flows
    ("9.1.050", "9.2.055"),
    ("9.1.050", "9.2.090"),
    ("9.1.050", "9.2.160"),

    # Project planning sequence
    ("9.2.005", "9.2.030"),
    ("9.2.010", "9.2.015"),
    ("9.2.015", "9.2.040"),
    ("9.2.015", "9.2.050"),
    ("9.2.040", "9.2.060"),
    ("9.2.050", "9.2.100"),
    ("9.2.055", "9.2.090"),
    ("9.2.057", "9.4.050"),
    ("9.2.070", "9.3.470"),
    ("9.2.080", "9.4.645"),
    ("9.2.090", "9.2.140"),
    ("9.2.090", "9.4.560"),
    ("9.2.100", "9.2.110"),
    ("9.2.110", "9.4.315"),
    ("9.2.120", "9.4.195"),
    ("9.2.120", "9.4.400"),
    ("9.2.130", "9.3.010"),
    ("9.2.140", "9.4.400"),
    ("9.2.160", "9.4.605"),

    # Site setup -> execution transitions
    ("9.3.020", "9.4.640"),
    ("9.3.100", "9.4.640"),
    ("9.3.110", "9.4.565"),
    ("9.3.470", "9.4.475"),

    # Documentation chain
    ("9.4.190", "9.4.195"),
    ("9.4.195", "9.4.200"),
    ("9.4.195", "9.4.205"),
    ("9.4.195", "9.4.210"),
    ("9.4.195", "9.4.215"),
    ("9.4.195", "9.4.220"),

    # Communications parent-child
    ("9.4.270", "9.4.275"),
    ("9.4.270", "9.4.280"),
    ("9.4.280", "9.4.285"),
    ("9.4.280", "9.4.290"),
    ("9.4.280", "9.4.295"),
    ("9.4.280", "9.4.300"),
    ("9.4.280", "9.4.305"),
    ("9.4.280", "9.4.310"),

    # Schedule chain
    ("9.4.315", "9.4.320"),
    ("9.4.320", "9.4.325"),
    ("9.4.325", "9.4.330"),
    ("9.4.335", "9.4.345"),
    ("9.4.340", "9.4.560"),
    ("9.4.325", "9.4.335"),
    ("9.4.340", "9.4.345"),
    ("9.4.350", "9.4.360"),

    # Change management chain
    ("9.4.355", "9.4.360"),
    ("9.4.360", "9.4.365"),
    ("9.4.370", "9.4.360"),
    ("9.4.375", "9.4.365"),
    ("9.4.360", "9.4.400"),
    ("9.4.380", "9.4.360"),
    ("9.4.385", "9.4.360"),
    ("9.4.390", "9.4.360"),

    # Cost chain
    ("9.4.400", "9.4.405"),
    ("9.4.410", "9.4.420"),
    ("9.4.415", "9.4.420"),
    ("9.4.420", "9.4.425"),
    ("9.4.425", "9.4.430"),
    ("9.4.430", "9.4.435"),
    ("9.4.440", "9.4.445"),
    ("9.4.445", "9.4.450"),
    ("9.4.445", "9.4.455"),
    ("9.4.460", "9.4.465"),
    ("9.4.400", "9.4.410"),

    # Safety chain
    ("9.4.475", "9.4.480"),
    ("9.4.480", "9.4.485"),
    ("9.4.490", "9.4.495"),
    ("9.4.500", "9.4.490"),
    ("9.4.505", "9.4.480"),
    ("9.4.475", "9.4.510"),

    # Quality chain
    ("9.4.515", "9.4.525"),
    ("9.4.515", "9.4.520"),
    ("9.4.525", "9.4.535"),
    ("9.4.535", "9.4.745"),
    ("9.4.530", "9.4.540"),
    ("9.4.545", "9.6.020"),

    # Resource chain
    ("9.4.560", "9.4.595"),
    ("9.4.565", "9.4.595"),
    ("9.4.570", "9.4.595"),
    ("9.4.576", "9.4.595"),
    ("9.4.580", "9.4.595"),

    # Procurement chain
    ("9.4.605", "9.4.620"),
    ("9.4.610", "9.4.605"),
    ("9.4.615", "9.4.610"),
    ("9.4.620", "9.4.625"),
    ("9.4.625", "9.4.630"),
    ("9.4.630", "9.4.635"),
    ("9.4.635", "9.4.640"),
    ("9.4.640", "9.4.650"),
    ("9.4.650", "9.4.655"),
    ("9.4.660", "9.4.665"),
    ("9.4.665", "9.4.670"),
    ("9.2.020", "9.4.055"),
    ("9.4.055", "9.4.631"),
    ("9.4.631", "9.4.630"),

    # Field operations chain
    ("9.4.675", "9.4.215"),
    ("9.4.675", "9.4.695"),
    ("9.4.680", "9.4.675"),
    ("9.4.705", "9.4.710"),
    ("9.4.710", "9.4.715"),
    ("9.4.690", "9.4.720"),
    ("9.4.695", "9.4.720"),
    ("9.4.720", "9.4.755"),
    ("9.4.725", "9.4.745"),
    ("9.4.735", "9.4.525"),

    # Execution -> Commissioning -> Closeout
    ("9.4.650", "9.5.020"),
    ("9.5.550", "9.6.005"),
    ("9.6.005", "9.6.010"),
    ("9.6.010", "9.6.015"),
    ("9.6.020", "9.6.030"),
    ("9.6.030", "9.6.040"),
    ("9.6.035", "9.6.040"),
    ("9.6.040", "9.6.050"),
    ("9.6.065", "9.4.195"),
    ("9.6.070", "9.6.085"),
    ("9.6.070", "9.6.080"),
    ("9.6.015", "9.6.065"),

    # Cost closeout
    ("9.4.465", "9.6.015"),
    ("9.4.660", "9.6.015"),
]

# ============================================================
# LAYER 3: CROSS-PHASE TOPIC CONNECTIONS (weight 2.0)
# ============================================================
TOPIC_WEIGHT = 2.0

CROSS_PHASE_TOPICS = {
    "scheduling": [
        "9.2.110", "9.4.315", "9.4.320", "9.4.325", "9.4.330",
        "9.4.335", "9.4.340", "9.4.345", "9.4.350",
    ],
    "budgeting_cost": [
        "9.2.090", "9.2.140", "9.4.400", "9.4.405", "9.4.425",
        "9.4.430", "9.4.435",
    ],
    "procurement": [
        "9.2.020", "9.2.160", "9.4.055", "9.4.605", "9.4.620",
        "9.4.625", "9.4.630", "9.4.631", "9.4.660",
    ],
    "safety": [
        "9.2.070", "9.3.470", "9.4.040", "9.4.475", "9.4.480",
        "9.4.485", "9.4.490", "9.4.495", "9.4.500", "9.4.505", "9.4.510",
    ],
    "quality": [
        "9.4.060", "9.4.515", "9.4.520", "9.4.525", "9.4.530",
        "9.4.535", "9.4.540", "9.4.545", "9.4.735", "9.4.745",
        "9.6.020",
    ],
    "prefabrication": ["9.2.057", "9.4.045", "9.4.050", "9.4.585"],
    "feeder_wire": ["9.2.020", "9.4.055", "9.4.631"],
    "materials": [
        "9.2.080", "9.4.570", "9.4.630", "9.4.635", "9.4.640",
        "9.4.645", "9.4.650", "9.5.020",
    ],
    "subcontractors": ["9.4.020", "9.4.290", "9.4.576"],
    "client_owner": ["9.4.030", "9.4.285", "9.6.050", "9.6.080"],
    "daily_reporting": ["9.4.215", "9.4.675", "9.4.695"],
    "lessons_learned": ["9.6.070", "9.6.080", "9.6.085"],
    "document_management": ["9.2.120", "9.4.190", "9.4.195", "9.6.065"],
    "meetings_general": [
        "9.2.130", "9.4.010", "9.4.020", "9.4.030", "9.4.040",
        "9.4.050", "9.4.060", "9.4.345", "9.4.520", "9.4.680",
        "9.6.010",
    ],
    "manpower": ["9.2.090", "9.4.560", "9.4.690"],
    "equipment": ["9.3.110", "9.4.565", "9.4.700"],
    "punch_list": ["9.4.545", "9.6.020"],
    "closeout_docs": ["9.6.015", "9.6.030", "9.6.035", "9.6.040", "9.6.065"],
    "contract_review": ["9.2.005", "9.2.030", "9.4.355"],
    "vendors": ["9.4.295", "9.4.580", "9.4.610", "9.4.615", "9.4.670"],
    "rfi": ["9.2.060", "9.4.205"],
    "scope_review": ["9.2.040", "9.2.050", "9.2.055", "9.2.057"],
    "tracking_controls": ["9.2.120", "9.4.400", "9.4.690", "9.4.695", "9.4.700"],
    "turnover": ["9.2.015", "9.6.005", "9.6.010", "9.6.015"],
}

# ============================================================
# LAYER 4: TITLE KEYWORD SIMILARITY (weight 1.0)
# ============================================================
KEYWORD_WEIGHT = 1.0
KEYWORD_CAP = 2.0

STOP_WORDS = {
    "manage", "conduct", "prepare", "develop", "review", "establish",
    "create", "track", "update", "monitor", "report", "submit",
    "provide", "identify", "perform", "implement", "resolve",
    "setup", "the", "and", "for", "of", "or", "a", "an", "in",
    "to", "vs", "sop", "&", "1", "handling", "begin",
}


# ============================================================
# SCORING FUNCTIONS
# ============================================================

def load_catalog(csv_path):
    """Load {sopid: title} from Authoritative_SOP_List.csv."""
    catalog = {}
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["SOPID"].strip()
            title = row["Title"].strip()
            if sid:
                catalog[sid] = title
    return catalog


def extract_keywords(title):
    """Extract meaningful keywords from an SOP title."""
    words = re.findall(r"[a-zA-Z]+", title.lower())
    return {w for w in words if w not in STOP_WORDS and len(w) > 2}


def sop_num(sid):
    """Parse SOP ID into a sortable numeric tuple."""
    parts = sid.split(".")
    return tuple(int(p) for p in parts)


def score_subcategory(sop_a, sop_b, subcat_lookup):
    """Layer 1: Score based on shared subcategory membership."""
    cats_a = set(subcat_lookup.get(sop_a, []))
    cats_b = set(subcat_lookup.get(sop_b, []))
    shared = cats_a & cats_b
    if not shared:
        return 0.0
    return SUBCAT_WEIGHT


def score_workflow(sop_a, sop_b, workflow_set):
    """Layer 2: Score based on workflow dependency links."""
    if (sop_a, sop_b) in workflow_set or (sop_b, sop_a) in workflow_set:
        return WORKFLOW_WEIGHT
    return 0.0


def score_cross_phase(sop_a, sop_b, topic_lookup, subcat_lookup):
    """Layer 3: Score based on cross-phase topic overlap.
    Only scored if SOPs are in different primary subcategories."""
    cats_a = set(subcat_lookup.get(sop_a, []))
    cats_b = set(subcat_lookup.get(sop_b, []))

    topics_a = set(topic_lookup.get(sop_a, []))
    topics_b = set(topic_lookup.get(sop_b, []))
    shared_topics = topics_a & topics_b

    if not shared_topics:
        return 0.0

    # If they share a subcategory, reduce the cross-phase score
    # (they already get subcategory credit)
    if cats_a & cats_b:
        return TOPIC_WEIGHT * 0.25  # small bonus for extra topic overlap
    return TOPIC_WEIGHT


def score_keywords(sop_a, sop_b, keyword_cache):
    """Layer 4: Score based on keyword overlap in titles."""
    kw_a = keyword_cache[sop_a]
    kw_b = keyword_cache[sop_b]
    if not kw_a or not kw_b:
        return 0.0
    shared = len(kw_a & kw_b)
    return min(shared * KEYWORD_WEIGHT, KEYWORD_CAP)


def compute_all_scores(catalog):
    """Build {(sop_a, sop_b): total_score} for all pairs."""
    subcat_lookup = build_subcat_lookup()

    # Build topic reverse lookup
    topic_lookup = defaultdict(list)
    for topic, sop_ids in CROSS_PHASE_TOPICS.items():
        for sid in sop_ids:
            topic_lookup[sid].append(topic)

    # Build workflow set
    workflow_set = set(WORKFLOW_LINKS)

    # Build keyword cache
    keyword_cache = {sid: extract_keywords(title) for sid, title in catalog.items()}

    # Score all pairs
    all_sops = sorted(catalog.keys(), key=sop_num)
    scores = {}

    for i, sop_a in enumerate(all_sops):
        for j in range(i + 1, len(all_sops)):
            sop_b = all_sops[j]
            total = 0.0
            total += score_subcategory(sop_a, sop_b, subcat_lookup)
            total += score_workflow(sop_a, sop_b, workflow_set)
            total += score_cross_phase(sop_a, sop_b, topic_lookup, subcat_lookup)
            total += score_keywords(sop_a, sop_b, keyword_cache)

            if total > 0:
                scores[(sop_a, sop_b)] = total

    return scores, subcat_lookup


def select_related(sop_id, scores, catalog, subcat_lookup):
    """Select top-N related SOPs for a given SOP."""
    candidates = []
    for (a, b), score in scores.items():
        if a == sop_id:
            candidates.append((b, score))
        elif b == sop_id:
            candidates.append((a, score))

    # Sort by score descending, then by SOP number for stability
    candidates.sort(key=lambda x: (-x[1], sop_num(x[0])))

    # Apply selection with subcategory cap
    selected = []
    subcat_count = defaultdict(int)
    my_subcats = set(subcat_lookup.get(sop_id, []))

    for cand_id, cand_score in candidates:
        if len(selected) >= MAX_RELATED:
            break
        if cand_score < SCORE_THRESHOLD and len(selected) >= MIN_RELATED:
            break

        # Check subcategory cap
        cand_subcats = set(subcat_lookup.get(cand_id, []))
        shared_subcats = my_subcats & cand_subcats
        if shared_subcats:
            subcat_key = sorted(shared_subcats)[0]
            if subcat_count[subcat_key] >= MAX_SAME_SUBCAT:
                continue
            subcat_count[subcat_key] += 1

        selected.append((cand_id, cand_score))

    # If we still need more, lower the threshold
    if len(selected) < MIN_RELATED:
        for cand_id, cand_score in candidates:
            if cand_id in {s[0] for s in selected}:
                continue
            if len(selected) >= MIN_RELATED:
                break
            selected.append((cand_id, cand_score))

    return selected


def enforce_bidirectional(relationships, catalog, subcat_lookup, scores):
    """Ensure all relationships are bidirectional, then trim to MAX_RELATED."""
    additions = defaultdict(list)

    for sop_a, related_list in relationships.items():
        for sop_b, score in related_list:
            b_ids = {r[0] for r in relationships.get(sop_b, [])}
            if sop_a not in b_ids:
                additions[sop_b].append((sop_a, score))

    added = 0
    for sop_b, new_rels in additions.items():
        current = relationships.get(sop_b, [])
        current_ids = {r[0] for r in current}
        for sop_a, score in sorted(new_rels, key=lambda x: -x[1]):
            if sop_a not in current_ids:
                current.append((sop_a, score))
                current_ids.add(sop_a)
                added += 1
        # Re-sort by score desc
        current.sort(key=lambda x: (-x[1], sop_num(x[0])))
        relationships[sop_b] = current

    # Trim all lists to MAX_RELATED
    trimmed = 0
    for sid in relationships:
        if len(relationships[sid]) > MAX_RELATED:
            trimmed += len(relationships[sid]) - MAX_RELATED
            relationships[sid] = relationships[sid][:MAX_RELATED]

    print(f"  Trimmed {trimmed} excess entries to cap at {MAX_RELATED}")
    return added


def format_related(related_list, catalog):
    """Format related SOPs as semicolon-delimited 'ID - Title' string."""
    parts = []
    for sid, score in sorted(related_list, key=lambda x: sop_num(x[0])):
        title = catalog.get(sid, "Unknown")
        parts.append(f"{sid} - {title}")
    return "; ".join(parts)


def generate_csv(relationships, catalog, output_path):
    """Write the final CSV output."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["SOPID", "Title", "RelatedSOPs", "RelatedCount"])

        for sid in sorted(catalog.keys(), key=sop_num):
            title = catalog[sid]
            related = relationships.get(sid, [])
            related_str = format_related(related, catalog)
            writer.writerow([sid, title, related_str, len(related)])


def print_stats(relationships, catalog):
    """Print distribution stats."""
    counts = [len(v) for v in relationships.values()]
    orphans = [sid for sid in catalog if sid not in relationships or len(relationships[sid]) == 0]

    print(f"\n{'='*50}")
    print(f"  RELATED SOPs MAPPING STATISTICS")
    print(f"{'='*50}")
    print(f"  Total SOPs:          {len(catalog)}")
    print(f"  SOPs with relations: {len(relationships)}")
    print(f"  Orphans (0 rels):    {len(orphans)}")
    if orphans:
        for o in orphans:
            print(f"    - {o}: {catalog[o]}")
    print(f"  Min related:         {min(counts) if counts else 0}")
    print(f"  Max related:         {max(counts) if counts else 0}")
    print(f"  Average related:     {sum(counts)/len(counts):.1f}" if counts else "  Average: N/A")
    print(f"  Median related:      {sorted(counts)[len(counts)//2]}" if counts else "  Median: N/A")

    # Distribution
    dist = defaultdict(int)
    for c in counts:
        dist[c] += 1
    print(f"\n  Distribution:")
    for k in sorted(dist.keys()):
        bar = "#" * dist[k]
        print(f"    {k} related: {dist[k]:3d} SOPs  {bar}")

    # Sample output
    print(f"\n  Sample relationships:")
    samples = ["9.2.010", "9.4.315", "9.4.525", "9.6.070", "9.1.050"]
    for sid in samples:
        if sid in relationships:
            related = relationships[sid]
            ids = [r[0] for r in sorted(related, key=lambda x: sop_num(x[0]))]
            print(f"    {sid} ({catalog[sid]})")
            for r_id, r_score in sorted(related, key=lambda x: (-x[1], sop_num(x[0]))):
                print(f"      -> {r_id} - {catalog.get(r_id, '?')} (score: {r_score:.1f})")


# ============================================================
# MAIN
# ============================================================

def main():
    print("Loading SOP catalog...")
    catalog = load_catalog(INPUT_CSV)
    print(f"  Loaded {len(catalog)} SOPs\n")

    print("Computing relationship scores...")
    scores, subcat_lookup = compute_all_scores(catalog)
    print(f"  Scored {len(scores)} SOP pairs with positive scores\n")

    print("Selecting related SOPs per SOP...")
    relationships = {}
    for sid in sorted(catalog.keys(), key=sop_num):
        related = select_related(sid, scores, catalog, subcat_lookup)
        relationships[sid] = related

    print("Enforcing bidirectional relationships...")
    added = enforce_bidirectional(relationships, catalog, subcat_lookup, scores)
    print(f"  Added {added} reverse links\n")

    print_stats(relationships, catalog)

    print(f"\nWriting output to {OUTPUT_CSV}...")
    generate_csv(relationships, catalog, OUTPUT_CSV)
    print("Done.")


if __name__ == "__main__":
    main()
