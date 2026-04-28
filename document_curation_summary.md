# Leukemia Drug Discovery — Document Curation Summary

**Date:** April 19–20, 2026 | **Author:** Karthik Ananthakrishnan | **Corpus:** 6,303 scientific papers (195 MB)

---

## Objective

Curate the leukemia drug discovery corpus to retain only documents relevant to 7 target scientific topics, removing noise before LazyGraphRAG (LGR) indexing to improve search quality and reduce costs.

## Approach: Dual-Signal Document Grooming

We used a two-phase classification pipeline combining **keyword analysis** (fast, precise) with **LLM semantic scoring** (comprehensive, contextual), then merged signals into confidence tiers.

| Phase | Method | Cost | Time |
|-------|--------|------|------|
| **1. Keyword Analysis** | Regex matching across 661K text units for 7 topics | Free | 5 min |
| **2. Document Sampling** | 6 representative chunks per doc (abstract + keyword-dense + conclusion) | Free | 3 min |
| **3. LLM Classification** | GPT-5.2 scoring (0–5 per topic) on sampled text | $21.55 | 22 min |
| **4. Combined Grooming** | Merge keyword + LLM signals into confidence tiers | Free | <1 min |

**Total cost: ~$22 | Total time: ~30 minutes**

## Results

| Tier | Count | % | Decision | Criteria |
|------|-------|---|----------|----------|
| **HIGH** | 1,377 | 21.8% | ✅ Include | Both keyword AND LLM agree relevant |
| **MEDIUM** | 1,694 | 26.9% | ✅ Include | LLM relevant, keywords too narrow to catch |
| **LOW** | 500 | 7.9% | ❌ Exclude | Keyword false positives (e.g. "clearance" = renal, not metabolic) |
| **NONE** | 2,732 | 43.3% | ❌ Exclude | Neither method found relevant |

### **Final: 3,071 documents retained (49%) — 3,232 excluded (51%)**

## Topic Coverage in Curated Set

| Topic | Documents | Key Finding |
|-------|-----------|-------------|
| Disease (Leukemia/AML) | 1,126 (37%) | LLM found 2.3× more than keywords alone |
| Drug Discovery | 880 (29%) | Largest overlap between signals |
| Differentiation Therapy | 652 (21%) | LLM found 4.5× more — keywords missed semantic context |
| Solubility | 470 (15%) | Good keyword/LLM agreement |
| Metabolic Stability | 302 (10%) | Keywords over-matched "clearance" in wrong contexts |
| Permeability | 252 (8%) | Moderate enrichment from LLM |
| Cardiac Safety | 191 (6%) | Highest keyword precision (hERG, QT are specific terms) |

## Key Insight

The LLM consistently found **significantly more relevant documents** than keywords — especially for topics with broader vocabulary (Disease: +130%, Differentiation: +350%). Keywords excelled at topics with highly specific terminology (Cardiac Safety: Cohen's κ = 0.59). Combining both signals eliminates 500 keyword false positives while capturing 1,694 documents that keywords missed.

## Infrastructure & Deployment

The 3,071 curated documents (195 MB) were transferred cross-tenant and uploaded to a new Azure storage account for LGR re-indexing:

| Resource | Details |
|----------|---------|
| **Source** | `bkshelfstorconuk/leukemia-drug-discovery/papers/` (LGR tenant) |
| **Destination** | `stlgrevalleukemia/leukemia-groomed/` (Discovery-bookshelf-devslice, UK South) |
| **Supercomputer** | `itsupleukeval` (D4s_v5 system, E64s_v6 nodepool — Medium tier) |
| **Bookshelf** | `bkshlfleukemiaeval2` (UK South, Succeeded) |

## Next Steps

1. **Create knowledgebase** under `bkshlfleukemiaeval2` pointing to the groomed container
2. **Trigger LGR indexing** via workspace `itworktwsv2` / project `itprojtwsv2`
3. **Run BenchmarkQED evaluation** (AutoQ → LGR Search → AutoE → Retrieval Metrics)
4. **Compare recall** between full corpus (6,303 docs) vs curated corpus (3,071 docs)
5. **Validate hypothesis**: curated corpus should yield higher search precision with comparable recall

---

*Artifacts: `recommended_documents.txt` (3,071 filenames), `excluded_documents.txt` (3,232 filenames), `document_grooming_report.md` (full analysis)*
