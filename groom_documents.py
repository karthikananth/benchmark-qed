"""Produce groomed document list using combined keyword + LLM signals."""
import json
from collections import defaultdict

TOPICS = ["Disease", "Differentiation", "Cardiac_safety", "Solubility",
          "Permeability", "Metabolic_stability", "Drug_discovery"]
LLM_THRESHOLD = 3
KW_HIT_THRESHOLD = 3
KW_DENSITY_THRESHOLD = 0.10

# Load data
llm_data = json.load(open("llm_topic_scores.json"))
kw_data = json.load(open("topic_analysis.json"))
filenames = json.load(open("doc_id_to_filename.json"))

llm_scores = llm_data["scores"]
doc_topic_hits = kw_data["doc_topic_hits"]
doc_tu_counts = kw_data.get("doc_tu_counts", {})

results = []
for doc_id in llm_scores:
    fn_info = filenames.get(doc_id, {})
    fn = fn_info.get("filename", "unknown")
    llm = llm_scores[doc_id]

    llm_topics = [t for t in TOPICS if llm.get(t, 0) >= LLM_THRESHOLD]
    max_llm = max(llm.get(t, 0) for t in TOPICS)

    hits_data = doc_topic_hits.get(doc_id, {})
    tu_count = doc_tu_counts.get(doc_id, 1)
    kw_topics = []
    for t in TOPICS:
        h = hits_data.get(t, 0)
        d = h / tu_count if tu_count > 0 else 0
        if h >= KW_HIT_THRESHOLD and d >= KW_DENSITY_THRESHOLD:
            kw_topics.append(t)

    both_topics = [t for t in llm_topics if t in kw_topics]

    if both_topics:
        tier = "HIGH"
    elif llm_topics:
        tier = "MEDIUM"
    elif kw_topics:
        tier = "LOW"
    else:
        tier = "NONE"

    results.append({
        "doc_id": doc_id,
        "filename": fn,
        "tier": tier,
        "max_llm_score": max_llm,
        "llm_topics": llm_topics,
        "kw_topics": kw_topics,
        "both_topics": both_topics,
        "scores": {t: llm.get(t, 0) for t in TOPICS},
    })

tier_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "NONE": 3}
results.sort(key=lambda x: (tier_order[x["tier"]], -x["max_llm_score"]))

tiers = defaultdict(int)
for r in results:
    tiers[r["tier"]] += 1

print("=" * 60)
print("GROOMED DOCUMENT LIST")
print("=" * 60)
print(f"Total documents: {len(results)}")
print(f"HIGH  (both keyword + LLM agree):    {tiers['HIGH']:>5}")
print(f"MEDIUM (LLM only, score >= 3):        {tiers['MEDIUM']:>5}")
print(f"LOW   (keyword only, LLM disagrees):  {tiers['LOW']:>5}")
print(f"NONE  (neither relevant):             {tiers['NONE']:>5}")
print()
print(f"Recommended for LGR indexing (HIGH + MEDIUM): {tiers['HIGH'] + tiers['MEDIUM']}")
print(f"Excluded (LOW + NONE): {tiers['LOW'] + tiers['NONE']}")
print()

recommended = [r for r in results if r["tier"] in ("HIGH", "MEDIUM")]
topic_counts = defaultdict(int)
for r in recommended:
    for t in r["llm_topics"]:
        topic_counts[t] += 1

print("Topic coverage in recommended docs:")
for t in TOPICS:
    print(f"  {t:25s}: {topic_counts[t]:>5}")

print()
print("Confidence tier breakdown by topic:")
for t in TOPICS:
    high = sum(1 for r in results if r["tier"] == "HIGH" and t in r["both_topics"])
    med = sum(1 for r in results if r["tier"] == "MEDIUM" and t in r["llm_topics"])
    low = sum(1 for r in results if r["tier"] == "LOW" and t in r["kw_topics"])
    print(f"  {t:25s}: HIGH={high:>4}  MEDIUM={med:>4}  LOW={low:>4}")

# Save outputs
with open("groomed_document_list.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved groomed_document_list.json")

rec_filenames = [r["filename"] for r in recommended]
with open("recommended_documents.txt", "w") as f:
    for fn in rec_filenames:
        f.write(fn + "\n")
print(f"Saved recommended_documents.txt ({len(rec_filenames)} files)")

exc_filenames = [r["filename"] for r in results if r["tier"] in ("LOW", "NONE")]
with open("excluded_documents.txt", "w") as f:
    for fn in exc_filenames:
        f.write(fn + "\n")
print(f"Saved excluded_documents.txt ({len(exc_filenames)} files)")
