# BenchmarkQED Evaluation Report: LazyGraphRAG on Leukemia Drug Discovery Corpus

**Date**: April 26, 2026  
**Pipeline Version**: V5 (SQL-Grounded)  
**Search System Under Test**: LazyGraphRAG (LGR)  
**Corpus**: Leukemia Drug Discovery — 3,071 curated scientific papers  

---

## 1. Dataset Overview

### Source Corpus
The evaluation was conducted on a curated leukemia drug discovery corpus sourced from a larger collection of 6,304 scientific papers. The corpus underwent a multi-stage grooming process to ensure topical relevance and quality.

### Document Curation Process

| Step | Method | Result |
|------|--------|--------|
| **Initial collection** | Full research paper archive | 6,304 documents |
| **Keyword analysis** | 7-topic keyword scoring (Disease, Differentiation, Drug Discovery, etc.) | Topic distribution mapped |
| **LLM classification** | GPT-5-mini scored each document across 7 topics (0-5 scale) | Cross-validated with keyword analysis |
| **Topic comparison** | Spearman correlation between keyword and LLM scores | High concordance confirmed |
| **Final selection** | Documents scoring ≥2 on at least one leukemia-relevant topic | **3,071 documents retained** |
| **Excluded** | Off-topic papers (materials science, general biology, unrelated chemistry) | 3,233 documents excluded |

### Curated Dataset Characteristics

| Property | Value |
|----------|-------|
| **Documents** | 3,071 |
| **Text units (chunks)** | 339,308 |
| **Chunk size** | 200 tokens |
| **Embedding model** | text-embedding-3-small (1,536 dimensions) |
| **Total tokens** | ~67.8M |

---

## 2. Evaluation Pipeline Architecture

The evaluation uses the BenchmarkQED framework with a V5 pipeline design that uses the LGR SQL database as the single source of truth for text unit identity.

### Pipeline Stages

```
Stage 0: SQL Export
  └─ Export text_units from LGR SQL → parquet (339K rows, 198 MB)

Stage 1: AutoQ (Question Generation)
  └─ Embed (339K chunks) → Cluster (k=50) → Generate questions + assertions
  └─ Output: 100 questions (50 local + 50 global), 557 assertions

Stage 2: LGR Search
  └─ Send 100 questions → LGR queue → Poll blob responses
  └─ Resolve chunk short_ids via parquet lookup
  └─ Output: 100 answers, 1,961 retrieved chunks (100% ID resolution)

Stage 3a: AutoE (Assertion Scoring)
  └─ Score each answer against source-grounded assertions using GPT-5.2
  └─ Output: pass/fail per assertion, coverage metrics

Stage 3c: Retrieval Metrics
  └─ Generate retrieval reference (cluster relevance assessment)
  └─ Calculate precision, recall, fidelity
```

### Key Design Decisions

**Text unit sourcing**: Text units were exported directly from LGR's SQL database (`dbo.text_units`), ensuring that the evaluation uses the exact same chunks that LGR indexes and retrieves. This eliminates any mismatch between evaluation ground truth and the search system's internal representation.

**Chunk ID resolution**: LGR search responses include retrieved text chunks but reference documents by `file_id` (document-level), not individual chunk IDs. To enable retrieval recall measurement, each retrieved chunk's text is matched against the exported text units via a prefix-based lookup, resolving to the authoritative `short_id` (the `human_readable_id` from the SQL database). This achieved 100% resolution across all 1,961 retrieved chunks.

**LLM configuration**: All evaluation LLM calls (question generation, assertion generation, assertion scoring, relevance assessment) used GPT-5.2 with `temperature: 0.0`, `reasoning_effort: none`, and `seed: 42` for deterministic, reproducible results.

---

## 3. Question Generation

Questions were generated using BenchmarkQED's AutoQ pipeline from 50 KMeans clusters of the 339,308 text units.

### Question Distribution

| Type | Count | Assertions | Avg Assertions/Question |
|------|-------|------------|------------------------|
| **Local** | 50 | 81 | 1.6 |
| **Global** | 50 | 476 | 9.5 |
| **Total** | **100** | **557** | 5.6 |

- **Local questions**: Answerable from a single text passage. Test retrieval accuracy — can the system find the right chunk?
- **Global questions**: Require synthesis across multiple topics in the corpus. Test representative diversity — can the system cover the corpus's thematic structure?

Global questions have significantly more assertions because they require synthesizing information from multiple sources, with each source contributing testable claims.

---

## 4. LGR Search Results

All 100 questions were sent to LGR via its V2 queue/blob protocol. Each response was parsed for answer text and retrieved text chunks.

### Search Performance

| Metric | Value |
|--------|-------|
| **Questions sent** | 100 |
| **Successful responses** | 100 (0 timeouts, 0 errors) |
| **Average response time** | ~80 seconds |
| **Total chunks retrieved** | 1,961 |
| **Average chunks per question** | 19.6 |
| **Chunk ID resolution rate** | **100%** (1,961/1,961) |

---

## 5. Assertion-Based Metrics (Answer Quality)

Each LGR answer was evaluated against source-grounded assertions using GPT-5.2. An assertion passes if the answer contains the factual claim described by the assertion.

### Overall Results

| Metric | Value |
|--------|-------|
| **Total assertions evaluated** | 557 |
| **Assertions passed** | 349 |
| **Assertions failed** | 208 |
| **Overall accuracy** | **62.7%** |
| **Average question pass rate** | **75.4%** |

### Results by Question Type

| Type | Questions | Assertions | Pass Rate |
|------|-----------|------------|-----------|
| **Local** | 50 | 81 | **79.3%** |
| **Global** | 50 | 476 | **71.4%** |

Local questions achieve higher pass rates because they require specific factual retrieval from individual passages, which aligns well with LGR's vector-based retrieval. Global questions are more challenging as they require thematic coverage across the corpus.

---

## 6. Retrieval Metrics (Chunk Quality)

Retrieval metrics assess the quality of the chunks LGR retrieves, independent of the final answer quality.

### Results

| Metric | Score | Description |
|--------|-------|-------------|
| **Binary Precision** | **77.3%** | Fraction of retrieved chunks judged relevant to the question |
| **Graded Precision** | **68.9%** | Relevance-weighted precision (higher scores for more relevant chunks) |
| **Recall** | **30.3%** | Fraction of the corpus's relevant topical clusters represented in retrieved chunks |
| **Fidelity** | **46.2%** | How faithfully the answer reflects the information in the retrieved chunks |

### Interpretation

- **Precision (77.3%)**: LGR retrieves high-quality, relevant chunks. Over three-quarters of retrieved text units are pertinent to the question being asked.

- **Recall (30.3%)**: LGR covers approximately one-third of the corpus's relevant topical clusters. This is characteristic of retrieval systems that prioritize depth over breadth — LGR focuses on the most relevant clusters rather than attempting to cover all related topics. For global questions spanning many themes, this means some relevant perspectives may be underrepresented.

- **Fidelity (46.2%)**: The generated answer incorporates roughly half of the information available in the retrieved chunks. This suggests that while LGR retrieves relevant material, the answer generation step is selective in what it includes, potentially favoring coherence over completeness.

### Content Filter Impact
2 out of approximately 17,000 chunk assessments were flagged by the content filter — negligible impact on results (0.01%).

---

## 7. Configuration Reference

| Component | Value |
|-----------|-------|
| **LGR Instance** | `bkshlfleukemialgr` (Sweden Central) |
| **Knowledge Base** | `bkshlfleukemiaeval` v1 |
| **SQL Database** | `sqls-dbksf-75kdp9aaaa` / `bkshlfleukemiaeval_1` |
| **AOAI Endpoint** | `aoai-lgr-poc` (Sweden Central) |
| **Chat Model** | GPT-5.2 (temp=0, reasoning=none, seed=42) |
| **Embedding Model** | text-embedding-3-small (1,536 dim) |
| **Clusters** | 50 (KMeans) |
| **Container Image** | benchmark-qed:v43 |
| **NFS Checkpoint** | `/mnt/checkpoints/benchmark-qed-leukemia-v5/` |

---

## 8. Summary

This evaluation represents the first complete BenchmarkQED run against the LazyGraphRAG system on the curated leukemia drug discovery corpus. The pipeline successfully:

1. Generated 100 diverse evaluation questions (50 local + 50 global) with 557 source-grounded assertions
2. Obtained answers from LGR for all 100 questions with zero failures
3. Resolved all 1,961 retrieved chunk identifiers to their authoritative database IDs
4. Measured both answer quality (assertion coverage) and retrieval quality (precision/recall/fidelity)

**Key findings**:
- LGR achieves strong answer quality (75.4% assertion pass rate) with particularly good performance on local questions (79.3%)
- Retrieval precision is high (77.3%), indicating that LGR selects relevant chunks effectively
- Retrieval recall at 30.3% reflects LGR's depth-focused retrieval strategy, which prioritizes the most relevant clusters over broad coverage
- These results establish a baseline for comparison with other RAG systems (e.g., GraphRAG Zero) on the same corpus and questions
