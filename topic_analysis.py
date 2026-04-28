"""Analyze 6000+ papers by topic keywords with hit-count thresholds."""
import pandas as pd
import re
import json
from collections import defaultdict

print("Loading parquet...")
df = pd.read_parquet('lgr_text_units.parquet')
total_docs = df.document_id.nunique()
print(f"Loaded {len(df):,} text units across {total_docs:,} documents")

# Count text units per document (for density calculation)
doc_tu_counts = df.groupby("document_id").size().to_dict()

# Topic keyword definitions (case-insensitive)
TOPICS = {
    "Disease": [
        r"\bleukemia\b", r"\baml\b", r"\bhematolog", r"\bmetastas",
        r"\bacute myeloid\b", r"\bmyeloid leukemia\b",
    ],
    "Differentiation": [
        r"\bcell differentiation\b", r"\bdifferentiation therapy\b",
        r"\batra\b", r"\ball-trans retinoic\b", r"\bretinoic acid\b",
    ],
    "Cardiac_safety": [
        r"\bherg\b", r"\bqt prolongation\b", r"\barrhythmia\b",
        r"\bcardiotoxic", r"\bqtc\b", r"\btorsade\b", r"\bion channel\b",
    ],
    "Solubility": [
        r"\baqueous solubility\b", r"\bbioavailability\b",
        r"\blogp\b", r"\blogd\b", r"\bsolubility\b",
    ],
    "Permeability": [
        r"\bcell membrane\b", r"\bpampa\b", r"\bcaco-2\b", r"\bcaco2\b",
        r"\bpermeability\b", r"\bmdck\b",
    ],
    "Metabolic_stability": [
        r"\bcyp450\b", r"\bcyp\d", r"\bhalf-life\b", r"\bclearance\b",
        r"\bclint\b", r"\bmicrosom", r"\bmetabolic stability\b",
        r"\bhepatocyt", r"\bfirst.pass\b",
    ],
    "Drug_discovery": [
        r"\bmedicinal chemistry\b", r"\bstructure.activity\b", r"\bsar\b",
        r"\blead optimization\b", r"\blead generation\b",
        r"\bstructure.based drug design\b", r"\blipinski\b",
        r"\bdrug.like", r"\bhit.to.lead\b", r"\bpharmacophore\b",
        r"\bic50\b", r"\bec50\b", r"\binhibitor\b",
    ],
}

# Compile patterns per topic
compiled = {}
for topic, patterns in TOPICS.items():
    compiled[topic] = re.compile("|".join(patterns), re.IGNORECASE)

# Count hits per document per topic
print("Scanning 661K text units (counting hits per doc per topic)...")
doc_topic_hits = defaultdict(lambda: defaultdict(int))  # doc_id -> topic -> hit count
doc_first_text = {}

for idx, row in enumerate(df.itertuples()):
    did = row.document_id
    text = row.text
    if did not in doc_first_text:
        doc_first_text[did] = text[:300]
    for topic, pattern in compiled.items():
        if pattern.search(text):
            doc_topic_hits[did][topic] += 1
    if (idx + 1) % 100000 == 0:
        print(f"  Processed {idx+1:,}/{len(df):,} text units...")

# Compute density for every doc-topic pair
doc_topic_density = {}  # (doc_id, topic) -> density
for did, hits in doc_topic_hits.items():
    for topic, hit_count in hits.items():
        doc_topic_density[(did, topic)] = hit_count / doc_tu_counts[did]

# ============================================================
# MATRIX: Hit count thresholds (rows) × topics (columns)
# ============================================================
HIT_THRESHOLDS = [1, 3, 5, 10]

print(f"\n{'='*80}")
print(f"FILTER 1: HIT COUNT ONLY (>= N text units mention the topic)")
print(f"{'='*80}")
print(f"Total documents: {total_docs:,}\n")
header = f"{'Threshold':>10} | " + " | ".join(f"{t:>12}" for t in TOPICS)
print(header)
print("-" * len(header))
for threshold in HIT_THRESHOLDS:
    counts = []
    for topic in TOPICS:
        n = sum(1 for d, h in doc_topic_hits.items() if h.get(topic, 0) >= threshold)
        counts.append(n)
    row = f"{'>=' + str(threshold) + ' hits':>10} | " + " | ".join(f"{c:>12,}" for c in counts)
    print(row)

# ============================================================
# MATRIX: Density thresholds (rows) × topics (columns)
# ============================================================
DENSITY_THRESHOLDS = [0.05, 0.10, 0.20, 0.30, 0.50]

print(f"\n{'='*80}")
print(f"FILTER 2: HIT DENSITY ONLY (hits / total_text_units >= X%)")
print(f"{'='*80}")
print(f"Total documents: {total_docs:,}\n")
header = f"{'Threshold':>10} | " + " | ".join(f"{t:>12}" for t in TOPICS)
print(header)
print("-" * len(header))
for density_thresh in DENSITY_THRESHOLDS:
    counts = []
    for topic in TOPICS:
        n = sum(1 for d, h in doc_topic_hits.items()
                if h.get(topic, 0) >= 1 and
                h.get(topic, 0) / doc_tu_counts[d] >= density_thresh)
        counts.append(n)
    row = f"{'>=' + str(int(density_thresh*100)) + '%':>10} | " + " | ".join(f"{c:>12,}" for c in counts)
    print(row)

# ============================================================
# COMBINED: Hit count >= 3 AND Density >= X%
# ============================================================
print(f"\n{'='*80}")
print(f"FILTER 3: COMBINED (hits >= 3 AND density >= X%)")
print(f"{'='*80}")
print(f"Total documents: {total_docs:,}\n")
header = f"{'Density':>10} | " + " | ".join(f"{t:>12}" for t in TOPICS)
print(header)
print("-" * len(header))
for density_thresh in DENSITY_THRESHOLDS:
    counts = []
    for topic in TOPICS:
        n = sum(1 for d, h in doc_topic_hits.items()
                if h.get(topic, 0) >= 3 and
                h.get(topic, 0) / doc_tu_counts[d] >= density_thresh)
        counts.append(n)
    row = f"{'>=' + str(int(density_thresh*100)) + '%':>10} | " + " | ".join(f"{c:>12,}" for c in counts)
    print(row)

# ============================================================
# RECOMMENDED: hits >= 3 AND density >= 10%
# ============================================================
REC_HITS = 3
REC_DENSITY = 0.10

print(f"\n{'='*80}")
print(f"RECOMMENDED VIEW (hits >= {REC_HITS} AND density >= {REC_DENSITY:.0%})")
print(f"{'='*80}")

topic_docs_recommended = {}
doc_topics_recommended = defaultdict(set)

for topic in TOPICS:
    docs = []
    for d, h in doc_topic_hits.items():
        hit_count = h.get(topic, 0)
        if hit_count >= REC_HITS and hit_count / doc_tu_counts[d] >= REC_DENSITY:
            docs.append(d)
    topic_docs_recommended[topic] = docs
    for d in docs:
        doc_topics_recommended[d].add(topic)

matched = len(doc_topics_recommended)
unmatched = total_docs - matched
print(f"Documents matching >= 1 topic: {matched:,} ({100*matched/total_docs:.1f}%)")
print(f"Documents matching no topic:   {unmatched:,} ({100*unmatched/total_docs:.1f}%)")

print(f"\nPer-topic:")
for topic in TOPICS:
    count = len(topic_docs_recommended[topic])
    print(f"  {topic:25s}: {count:>5,} docs ({100*count/total_docs:5.1f}%)")

print(f"\nMulti-topic coverage:")
for n in range(1, 8):
    count = sum(1 for topics in doc_topics_recommended.values() if len(topics) == n)
    if count > 0:
        print(f"  Exactly {n} topic(s): {count:,} docs")

# ============================================================
# TOP-5 per topic by COMBINED SCORE (hit_count * density)
# ============================================================
print(f"\n{'='*80}")
print(f"TOP-5 MOST FOCUSED PAPERS PER TOPIC (hits >= 3, ranked by hits × density)")
print(f"{'='*80}")

for topic in TOPICS:
    print(f"\n  [{topic}]")
    scored = []
    for did, hits in doc_topic_hits.items():
        hit_count = hits.get(topic, 0)
        if hit_count >= REC_HITS:
            density = hit_count / doc_tu_counts[did]
            score = hit_count * density
            scored.append((did, hit_count, doc_tu_counts[did], density, score))
    scored.sort(key=lambda x: -x[4])
    for did, hits, total, density, score in scored[:5]:
        snippet = doc_first_text.get(did, "")[:90].replace("\n", " ")
        print(f"    {hits:>4} hits/{total:>4} TUs  density={density:.0%}  score={score:.1f} | {snippet}...")

# ============================================================
# Save full results
# ============================================================
results = {
    "summary": {
        "total_documents": total_docs,
        "recommended_hits_threshold": REC_HITS,
        "recommended_density_threshold": REC_DENSITY,
        "matched_recommended": matched,
        "unmatched_recommended": unmatched,
    },
    "per_topic_recommended": {t: len(d) for t, d in topic_docs_recommended.items()},
    "doc_topic_hits": {d: dict(h) for d, h in doc_topic_hits.items()},
    "doc_tu_counts": doc_tu_counts,
    "doc_first_text": doc_first_text,
    "topic_doc_ids_recommended": {t: d for t, d in topic_docs_recommended.items()},
    "doc_topics_recommended": {d: sorted(t) for d, t in doc_topics_recommended.items()},
}

# Also save per-threshold matrices for reference
results["hit_count_matrix"] = {}
for threshold in HIT_THRESHOLDS:
    results["hit_count_matrix"][str(threshold)] = {
        topic: sum(1 for d, h in doc_topic_hits.items() if h.get(topic, 0) >= threshold)
        for topic in TOPICS
    }
results["density_matrix"] = {}
for dt in DENSITY_THRESHOLDS:
    results["density_matrix"][str(dt)] = {
        topic: sum(1 for d, h in doc_topic_hits.items()
                   if h.get(topic, 0) >= 1 and h.get(topic, 0) / doc_tu_counts[d] >= dt)
        for topic in TOPICS
    }
results["combined_matrix"] = {}
for dt in DENSITY_THRESHOLDS:
    results["combined_matrix"][str(dt)] = {
        topic: sum(1 for d, h in doc_topic_hits.items()
                   if h.get(topic, 0) >= 3 and h.get(topic, 0) / doc_tu_counts[d] >= dt)
        for topic in TOPICS
    }

with open("topic_analysis.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved full results to topic_analysis.json")
