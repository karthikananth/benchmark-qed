# Leukemia Drug Discovery Corpus — Document Grooming Report

**Date:** April 19, 2026  
**Corpus:** 6,303 scientific papers from leukemia drug discovery blob storage  
**Source:** `bkshelfstorconuk.blob.core.windows.net/leukemia-drug-discovery/papers/`  
**Objective:** Identify and retain documents relevant to 7 target topics, removing irrelevant papers before LGR indexing

---

## 1. Corpus Overview

| Metric | Value |
|--------|-------|
| Total documents | 6,303 |
| Total text units (LGR chunks) | 661,411 |
| Avg text units per document | 105 |
| Avg tokens per text unit | 199 |
| Total tokens | 131.8M |

The corpus was originally assembled for leukemia research but contains a broad mix of biomedical and scientific papers. Initial analysis showed only ~22% mention leukemia/AML directly.

---

## 2. Target Topics

| # | Topic | Defining Concepts |
|---|-------|-------------------|
| 1 | **Disease** | Leukemia, AML, hematology, metastases |
| 2 | **Differentiation** | Cell differentiation therapy, ATRA (all-trans retinoic acid) |
| 3 | **Cardiac_safety** | hERG channel, QT prolongation, arrhythmia, cardiotoxicity |
| 4 | **Solubility** | Aqueous solubility, bioavailability, logP, logD |
| 5 | **Permeability** | Cell membrane permeability, PAMPA assay, Caco-2, MDCK |
| 6 | **Metabolic_stability** | CYP450 enzymes, half-life, clearance, CLint, microsomes, hepatocytes |
| 7 | **Drug_discovery** | Medicinal chemistry, SAR, lead optimization, structure-based drug design, Lipinski, IC50, EC50 |

---

## 3. Methodology

### 3.1 Phase 1 — Keyword Analysis

**Approach:** Regex keyword matching across all 661,411 text units for each of the 7 topics.

**Metrics per document per topic:**
- **Hit count:** Number of text units containing at least one keyword match
- **Hit density:** Hit count / total text units in the document

**Threshold for "keyword relevant":** hits ≥ 3 AND density ≥ 10%

This dual threshold ensures a document both has substantive discussion (≥3 chunks) and dedicates a meaningful proportion to the topic.

**Script:** `topic_analysis.py`  
**Output:** `topic_analysis.json`  
**Cost:** Free (local computation)  
**Time:** ~5 minutes

### 3.2 Phase 2 — Keyword-Guided Document Sampling

**Approach:** For each document, select 6 representative text units instead of using the full ~105:

| Slot | Selection Method | Purpose |
|------|-----------------|---------|
| Chunks 1–2 | First two text units | Captures abstract/introduction |
| Chunks 3–5 | Top 3 text units by total keyword hits | Captures where topic discussion is densest |
| Chunk 6 | Last text unit | Captures conclusion/summary |

If a document has ≤6 text units, all are included. Chunks are deduplicated if a keyword-hit chunk is already the first or last.

**Result:**
- Average sampled tokens per document: 1,194 (5.7% of full document)
- Total sampled tokens: 7.5M (down from 131.8M)

**Script:** `build_document_samples.py`  
**Output:** `document_samples.json`  
**Cost:** Free (local computation)  
**Time:** ~3 minutes

### 3.3 Phase 3 — LLM Classification

**Approach:** Send the sampled text for each document to GPT-5.2 with a structured prompt requesting a 0–5 relevance score per topic.

**Scoring rubric:**

| Score | Meaning |
|-------|---------|
| 0 | Not mentioned at all |
| 1 | Tangential mention (a few words) |
| 2 | Brief discussion (a paragraph or two) |
| 3 | Substantive discussion (a full section or repeated throughout) |
| 4 | Major focus (one of the paper's main themes) |
| 5 | Primary subject (the paper is fundamentally about this topic) |

**API configuration:**

| Setting | Value |
|---------|-------|
| Model | GPT-5.2 on Azure OpenAI (`aoai-lgr-poc`, Sweden Central) |
| Temperature | 0 (deterministic) |
| Response format | JSON object |
| Max completion tokens | 200 |
| Concurrency | 30 async calls |
| Authentication | Entra ID (Cognitive Services OpenAI User role) |

**LLM threshold for "relevant":** score ≥ 3

**Script:** `llm_topic_scorer.py`  
**Output:** `llm_topic_scores.json`  
**Cost:** ~$21.55 (9.8M input tokens × $1.75/1M + 319K output tokens × $14.00/1M)  
**Time:** ~22 minutes  
**Errors:** 0 out of 6,303

### 3.4 Phase 4 — Combined Signal Grooming

**Approach:** Combine keyword and LLM signals into confidence tiers:

| Tier | Criteria | Interpretation |
|------|----------|----------------|
| **HIGH** | Both keyword AND LLM agree relevant | Highest confidence — keyword evidence confirms LLM semantic understanding |
| **MEDIUM** | LLM relevant (≥3) but keyword missed | Likely relevant — LLM understood topic semantically, keywords too narrow |
| **LOW** | Keyword flagged but LLM disagrees (<3) | Likely false positive — keywords matched in wrong context |
| **NONE** | Neither method found relevant | Confidently irrelevant to all 7 topics |

**Decision:** Include HIGH + MEDIUM for LGR indexing. Exclude LOW + NONE.

**Script:** `groom_documents.py`

---

## 4. Results

### 4.1 Keyword vs LLM Agreement

| Topic | Keyword Relevant | LLM Relevant | Concordance | Cohen's κ | Spearman ρ |
|-------|-----------------|-------------|-------------|-----------|-----------|
| Disease | 489 | 1,126 | 88.4% | 0.491 | 0.656 |
| Differentiation | 145 | 652 | 90.5% | 0.219 | 0.661 |
| Cardiac_safety | 144 | 191 | 97.9% | 0.592 | 0.520 |
| Solubility | 365 | 470 | 94.3% | 0.543 | 0.772 |
| Permeability | 127 | 252 | 96.2% | 0.352 | 0.636 |
| Metabolic_stability | 396 | 302 | 93.8% | 0.406 | 0.546 |
| Drug_discovery | 674 | 880 | 87.7% | 0.430 | 0.592 |

**Key finding:** The LLM consistently identifies more relevant documents than keywords, especially for Disease (+130%) and Differentiation (+350%). Keywords have highest agreement with LLM for Cardiac_safety (κ=0.592) due to highly specific terminology (hERG, QT).

### 4.2 Groomed Document Tiers

| Tier | Count | % | Action |
|------|-------|---|--------|
| **HIGH** | 1,377 | 21.8% | ✅ Include — both signals agree |
| **MEDIUM** | 1,694 | 26.9% | ✅ Include — LLM semantic match |
| **LOW** | 500 | 7.9% | ❌ Exclude — keyword false positives |
| **NONE** | 2,732 | 43.3% | ❌ Exclude — not relevant |

### 4.3 Final Recommendation

**Include for LGR indexing: 3,071 documents (48.7% of corpus)**  
**Exclude: 3,232 documents (51.3%)**

### 4.4 Topic Coverage in Recommended Documents

| Topic | Documents | % of Recommended | Tier Breakdown |
|-------|----------|-------------------|----------------|
| Disease | 1,126 | 36.7% | HIGH: 441, MEDIUM: 606 |
| Drug_discovery | 880 | 28.6% | HIGH: 388, MEDIUM: 415 |
| Differentiation | 652 | 21.2% | HIGH: 99, MEDIUM: 508 |
| Solubility | 470 | 15.3% | HIGH: 239, MEDIUM: 198 |
| Metabolic_stability | 302 | 9.8% | HIGH: 153, MEDIUM: 98 |
| Permeability | 252 | 8.2% | HIGH: 70, MEDIUM: 123 |
| Cardiac_safety | 191 | 6.2% | HIGH: 101, MEDIUM: 66 |

### 4.5 LLM Score Distribution

| Topic | 0 | 1 | 2 | 3 | 4 | 5 |
|-------|---|---|---|---|---|---|
| Disease | 4,405 | 558 | 214 | 619 | 119 | 388 |
| Differentiation | 4,921 | 410 | 320 | 340 | 234 | 78 |
| Cardiac_safety | 5,826 | 221 | 65 | 58 | 51 | 82 |
| Solubility | 5,012 | 520 | 301 | 182 | 217 | 71 |
| Permeability | 5,359 | 475 | 217 | 133 | 88 | 31 |
| Metabolic_stability | 5,438 | 360 | 203 | 150 | 137 | 15 |
| Drug_discovery | 3,478 | 1,225 | 720 | 367 | 327 | 186 |

---

## 5. Excluded Document Analysis

### 5.1 LOW Tier (500 documents) — Keyword False Positives

These documents were flagged by keyword analysis but rejected by the LLM. Common causes:
- **"clearance"** matching renal clearance, not metabolic clearance (Metabolic_stability: 181 false positives)
- **"SAR"** matching non-chemistry contexts (Drug_discovery: 132 false positives)
- **"solubility"** matching non-pharmaceutical contexts like mineral solubility (Solubility: 87 false positives)
- **"permeability"** matching soil/membrane permeability in non-biomedical contexts (Permeability: 33 false positives)

### 5.2 NONE Tier (2,732 documents) — Irrelevant Papers

Neither keyword analysis nor LLM found these relevant to any of the 7 topics. These include:
- General biomedical papers not related to drug discovery or leukemia
- Materials science, environmental science, and agriculture papers
- Statistical methodology papers
- Unrelated clinical studies

---

## 6. Document ID to Filename Mapping

The document ID → filename mapping was extracted from the LGR SQL database (`dbo.documents` table) via container exec.

**Connection method:** pyodbc with struct-packed managed identity token  
**Database:** `leukemiaresearchkb_1` on `sqls-dbksf-d5ohunaaaa.database.windows.net`  
**Output:** `doc_id_to_filename.json` (6,303 entries, 100% match with parquet)

---

## 7. Output Files

| File | Description | Size |
|------|-------------|------|
| `topic_analysis.json` | Keyword hits/density per doc per topic | 5.1 MB |
| `document_samples.json` | Keyword-guided sampled text per doc | — |
| `llm_topic_scores.json` | GPT-5.2 scores (0–5) per doc per topic | — |
| `doc_id_to_filename.json` | Document ID hash → filename mapping | 1.9 MB |
| `topic_comparison_report.txt` | Keyword vs LLM comparison metrics | — |
| `topic_comparison.json` | Structured comparison data | — |
| `groomed_document_list.json` | Full groomed list with tiers and scores | — |
| `recommended_documents.txt` | 3,071 filenames to include | — |
| `excluded_documents.txt` | 3,232 filenames to exclude | — |

---

## 8. Next Steps

1. **Create new blob container** with only the 3,071 recommended documents
2. **Create new storage container resource and storage asset** pointing to the groomed container
3. **Create new knowledgebase** on the existing Bookshelf (`bkshlfleukemiaresearch`)
4. **Index the groomed knowledgebase** — should be faster with 49% fewer documents
5. **Run BenchmarkQED evaluation** (AutoQ → LGR Search → AutoE → Retrieval Metrics) on the groomed KB
6. **Compare evaluation results** — groomed corpus vs full corpus
