"""Analyze topic category distribution across documents."""
import json
from collections import Counter

with open('llm_topic_scores.json') as f:
    data = json.load(f)

all_scores = data['scores']
topics = ['Disease', 'Differentiation', 'Cardiac_safety', 'Solubility',
          'Permeability', 'Metabolic_stability', 'Drug_discovery']

# For each document, find which topics it's relevant to (score >= 3)
num_cats = Counter()
combo_counts = Counter()

for doc_id, doc in all_scores.items():
    relevant = tuple(sorted([t for t in topics if doc.get(t, 0) >= 3]))
    num_cats[len(relevant)] += 1
    if len(relevant) > 0:
        combo_counts[relevant] += 1

total = len(all_scores)
print("=== Distribution by Number of Categories (score >= 3) ===")
for n in range(8):
    count = num_cats[n]
    pct = count / total * 100
    bar = "#" * int(pct / 2)
    print(f"  {n} categories: {count:>5} papers ({pct:5.1f}%) {bar}")

print(f"\nTotal: {total} | With >= 1 topic: {total - num_cats[0]} | 0 topics: {num_cats[0]}")

# Top 25 combos
print("\n=== Top 25 Category Combinations ===")
for combo, count in combo_counts.most_common(25):
    label = " + ".join(combo)
    print(f"  {count:>4}: {label}")

print(f"\nUnique combinations observed: {len(combo_counts)} of 127 possible")

# Cumulative from bottom
print("\n=== Cumulative (could we cut more?) ===")
cumul = 0
for n in range(8):
    cumul += num_cats[n]
    print(f"  <= {n} categories: {cumul:>5} papers ({cumul/total*100:.1f}%)")

# Group by macro bucket (1-cat, 2-cat, etc) with paper counts per combo
print("\n=== Detailed: Papers per combination, grouped by # categories ===")
for n in range(1, 8):
    combos_at_n = [(c, cnt) for c, cnt in combo_counts.items() if len(c) == n]
    combos_at_n.sort(key=lambda x: -x[1])
    if combos_at_n:
        total_at_n = sum(cnt for _, cnt in combos_at_n)
        print(f"\n--- {n} category/ies ({total_at_n} papers, {len(combos_at_n)} unique combos) ---")
        for combo, count in combos_at_n:
            label = " + ".join(combo)
            print(f"    {count:>4}: {label}")
