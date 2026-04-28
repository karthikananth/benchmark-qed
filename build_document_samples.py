"""Build keyword-guided document samples for LLM topic classification.

For each of the 6,303 documents, selects 6 representative text units:
- Chunks 1-2: First two text units (intro/abstract)
- Chunks 3-5: Top 3 text units by total keyword hits across all 7 topics
- Chunk 6: Last text unit (conclusion)

Input: lgr_text_units.parquet, topic_analysis.json
Output: document_samples.json
"""
import json
import re
import pandas as pd
from collections import defaultdict

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

# Compile all topic patterns into one combined pattern for scoring
compiled = {}
for topic, patterns in TOPICS.items():
    compiled[topic] = re.compile("|".join(patterns), re.IGNORECASE)

ALL_PATTERN = re.compile(
    "|".join(p for patterns in TOPICS.values() for p in patterns),
    re.IGNORECASE,
)


def score_text_unit(text: str) -> int:
    """Count total keyword matches across all topics."""
    return len(ALL_PATTERN.findall(text))


def select_chunks(text_units: list[dict], max_chunks: int = 6) -> list[dict]:
    """Select representative chunks using keyword-guided sampling."""
    n = len(text_units)
    if n <= max_chunks:
        return text_units

    # Always include first 2 and last 1
    selected_indices = {0, 1, n - 1}

    # Score each text unit by keyword hits
    scores = [(i, score_text_unit(tu["text"])) for i, tu in enumerate(text_units)]

    # Sort by score descending, pick top 3 not already selected
    scores.sort(key=lambda x: -x[1])
    for idx, _score in scores:
        if idx not in selected_indices:
            selected_indices.add(idx)
            if len(selected_indices) >= max_chunks:
                break

    # Return in document order
    return [text_units[i] for i in sorted(selected_indices)]


def build_sample_text(chunks: list[dict], total_chunks: int) -> str:
    """Build the concatenated sample text with section markers."""
    if total_chunks <= 6:
        return "\n\n".join(c["text"] for c in chunks)

    # First 2 = intro, middle = key sections, last = conclusion
    intro = chunks[:2]
    conclusion = [chunks[-1]]
    key_sections = chunks[2:-1] if len(chunks) > 3 else []

    parts = []
    parts.append("[INTRO]")
    parts.extend(c["text"] for c in intro)

    if key_sections:
        parts.append("\n[KEY SECTIONS]")
        parts.extend(c["text"] for c in key_sections)

    parts.append("\n[CONCLUSION]")
    parts.extend(c["text"] for c in conclusion)

    return "\n\n".join(parts)


def main():
    print("Loading parquet...")
    df = pd.read_parquet("lgr_text_units.parquet")
    print(f"Loaded {len(df):,} text units across {df.document_id.nunique():,} documents")

    # Group by document, preserving row order (sequential in parquet)
    print("Building document samples...")
    samples = {}
    doc_groups = df.groupby("document_id", sort=False)

    for i, (doc_id, group) in enumerate(doc_groups):
        text_units = [
            {"text": row.text, "n_tokens": row.n_tokens, "idx": j}
            for j, row in enumerate(group.itertuples())
        ]

        selected = select_chunks(text_units)
        sample_text = build_sample_text(selected, len(text_units))
        sampled_tokens = sum(c["n_tokens"] for c in selected)

        samples[doc_id] = {
            "sampled_text": sample_text,
            "total_chunks": len(text_units),
            "sampled_chunks": len(selected),
            "total_tokens": int(group.n_tokens.sum()),
            "sampled_tokens": int(sampled_tokens),
            "selected_indices": [c["idx"] for c in selected],
        }

        if (i + 1) % 1000 == 0:
            print(f"  Processed {i+1:,}/{len(doc_groups):,} documents...")

    # Stats
    total_sampled_tokens = sum(s["sampled_tokens"] for s in samples.values())
    total_original_tokens = sum(s["total_tokens"] for s in samples.values())
    avg_sampled = total_sampled_tokens / len(samples)
    avg_original = total_original_tokens / len(samples)

    print(f"\n{'='*60}")
    print(f"SAMPLING SUMMARY")
    print(f"{'='*60}")
    print(f"Documents: {len(samples):,}")
    print(f"Avg chunks per doc: {sum(s['total_chunks'] for s in samples.values())/len(samples):.0f} → {sum(s['sampled_chunks'] for s in samples.values())/len(samples):.1f} sampled")
    print(f"Avg tokens per doc: {avg_original:,.0f} → {avg_sampled:,.0f} sampled ({avg_sampled/avg_original*100:.1f}%)")
    print(f"Total tokens: {total_original_tokens:,} → {total_sampled_tokens:,} ({total_sampled_tokens/total_original_tokens*100:.1f}%)")
    print(f"Estimated GPT-5-mini cost: ${(total_sampled_tokens + 300*len(samples)) / 1e6 * 0.15 + 150*len(samples) / 1e6 * 0.60:.2f}")

    # Save
    with open("document_samples.json", "w") as f:
        json.dump(samples, f)
    print(f"\nSaved to document_samples.json ({len(samples):,} documents)")


if __name__ == "__main__":
    main()
