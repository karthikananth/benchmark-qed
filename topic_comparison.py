"""Compare keyword analysis vs LLM classification scores.

Produces concordance, false positives/negatives, Spearman correlation,
and Cohen's kappa per topic.

Input: topic_analysis.json, llm_topic_scores.json, doc_id_to_filename.json
Output: topic_comparison_report.txt
"""
import json
import numpy as np
from scipy.stats import spearmanr
from collections import defaultdict

TOPICS = ["Disease", "Differentiation", "Cardiac_safety", "Solubility",
          "Permeability", "Metabolic_stability", "Drug_discovery"]

# Keyword thresholds for "relevant"
KW_HIT_THRESHOLD = 3
KW_DENSITY_THRESHOLD = 0.10

# LLM threshold for "relevant"
LLM_THRESHOLD = 3


def cohen_kappa(y1, y2):
    """Compute Cohen's kappa between two binary lists."""
    n = len(y1)
    if n == 0:
        return 0
    a = sum(1 for i in range(n) if y1[i] == y2[i])
    p_o = a / n
    p1 = sum(y1) / n
    p2 = sum(y2) / n
    p_e = p1 * p2 + (1 - p1) * (1 - p2)
    if p_e == 1:
        return 1
    return (p_o - p_e) / (1 - p_e)


def main():
    # Load data
    print("Loading data...")
    with open("topic_analysis.json") as f:
        kw_data = json.load(f)
    with open("llm_topic_scores.json") as f:
        llm_data = json.load(f)
    with open("doc_id_to_filename.json") as f:
        filenames = json.load(f)

    doc_topic_hits = kw_data["doc_topic_hits"]
    doc_tu_counts = kw_data.get("doc_tu_counts", {})
    llm_scores = llm_data["scores"]

    # Get common doc IDs
    all_docs = set(llm_scores.keys())
    print(f"Documents: {len(all_docs)}")

    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("TOPIC COMPARISON: Keyword Analysis vs LLM Classification (GPT-5.2)")
    report_lines.append("=" * 70)
    report_lines.append(f"Documents: {len(all_docs)}")
    report_lines.append(f"Keyword threshold: hits >= {KW_HIT_THRESHOLD} AND density >= {KW_DENSITY_THRESHOLD:.0%}")
    report_lines.append(f"LLM threshold: score >= {LLM_THRESHOLD}")
    report_lines.append("")

    summary_data = {}

    for topic in TOPICS:
        kw_relevant = []
        llm_relevant = []
        kw_densities = []
        llm_scores_list = []
        false_positives = []  # keyword says yes, LLM says no
        false_negatives = []  # LLM says yes, keyword says no

        for doc_id in all_docs:
            # Keyword data
            hits = doc_topic_hits.get(doc_id, {}).get(topic, 0)
            tu_count = doc_tu_counts.get(doc_id, 1)
            density = hits / tu_count if tu_count > 0 else 0
            kw_rel = 1 if hits >= KW_HIT_THRESHOLD and density >= KW_DENSITY_THRESHOLD else 0

            # LLM data
            llm_score = llm_scores[doc_id].get(topic, 0)
            llm_rel = 1 if llm_score >= LLM_THRESHOLD else 0

            kw_relevant.append(kw_rel)
            llm_relevant.append(llm_rel)
            kw_densities.append(density)
            llm_scores_list.append(llm_score)

            fn = filenames.get(doc_id, {}).get("filename", doc_id[:20])

            if kw_rel == 1 and llm_rel == 0:
                false_positives.append((fn, hits, density, llm_score))
            elif kw_rel == 0 and llm_rel == 1:
                false_negatives.append((fn, hits, density, llm_score))

        # Metrics
        kw_count = sum(kw_relevant)
        llm_count = sum(llm_relevant)
        agree = sum(1 for i in range(len(kw_relevant)) if kw_relevant[i] == llm_relevant[i])
        concordance = agree / len(kw_relevant) * 100
        kappa = cohen_kappa(kw_relevant, llm_relevant)

        # Spearman correlation (density vs LLM score)
        if len(set(kw_densities)) > 1 and len(set(llm_scores_list)) > 1:
            rho, p_val = spearmanr(kw_densities, llm_scores_list)
        else:
            rho, p_val = 0, 1

        # Sort false pos/neg by LLM score
        false_positives.sort(key=lambda x: x[3])
        false_negatives.sort(key=lambda x: -x[3])

        summary_data[topic] = {
            "kw_relevant": kw_count,
            "llm_relevant": llm_count,
            "concordance": round(concordance, 1),
            "kappa": round(kappa, 3),
            "spearman_rho": round(rho, 3),
            "false_positives": len(false_positives),
            "false_negatives": len(false_negatives),
        }

        report_lines.append(f"--- {topic} ---")
        report_lines.append(f"  Keyword relevant: {kw_count} docs")
        report_lines.append(f"  LLM relevant (>={LLM_THRESHOLD}): {llm_count} docs")
        report_lines.append(f"  Concordance: {concordance:.1f}%")
        report_lines.append(f"  Cohen's kappa: {kappa:.3f}")
        report_lines.append(f"  Spearman rho: {rho:.3f} (p={p_val:.2e})")
        report_lines.append(f"  False positives (keyword only): {len(false_positives)}")
        report_lines.append(f"  False negatives (LLM only): {len(false_negatives)}")

        if false_positives:
            report_lines.append(f"  Top false positives (keyword flagged, LLM score low):")
            for fn, hits, dens, ls in false_positives[:5]:
                report_lines.append(f"    {fn} | hits={hits} dens={dens:.1%} | LLM={ls}")

        if false_negatives:
            report_lines.append(f"  Top false negatives (LLM flagged, keyword missed):")
            for fn, hits, dens, ls in false_negatives[:5]:
                report_lines.append(f"    {fn} | hits={hits} dens={dens:.1%} | LLM={ls}")

        report_lines.append("")

    # Summary table
    report_lines.append("=" * 70)
    report_lines.append("SUMMARY TABLE")
    report_lines.append("=" * 70)
    report_lines.append(f"{'Topic':25s} {'KW':>5s} {'LLM':>5s} {'Conc%':>6s} {'Kappa':>6s} {'Rho':>6s} {'FP':>4s} {'FN':>4s}")
    report_lines.append("-" * 70)
    for topic in TOPICS:
        d = summary_data[topic]
        report_lines.append(f"{topic:25s} {d['kw_relevant']:5d} {d['llm_relevant']:5d} {d['concordance']:6.1f} {d['kappa']:6.3f} {d['spearman_rho']:6.3f} {d['false_positives']:4d} {d['false_negatives']:4d}")

    # LLM score distribution per topic
    report_lines.append("")
    report_lines.append("=" * 70)
    report_lines.append("LLM SCORE DISTRIBUTION")
    report_lines.append("=" * 70)
    for topic in TOPICS:
        dist = defaultdict(int)
        for doc_id in all_docs:
            s = llm_scores[doc_id].get(topic, 0)
            dist[s] += 1
        dist_str = " | ".join(f"{s}:{dist[s]}" for s in range(6))
        report_lines.append(f"  {topic:25s}: {dist_str}")

    # Write report
    report = "\n".join(report_lines)
    print(report)

    with open("topic_comparison_report.txt", "w") as f:
        f.write(report)
    print(f"\nSaved to topic_comparison_report.txt")

    # Save structured data
    with open("topic_comparison.json", "w") as f:
        json.dump(summary_data, f, indent=2)
    print("Saved to topic_comparison.json")


if __name__ == "__main__":
    main()
