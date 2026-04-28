#!/bin/bash
# BenchmarkQED Evaluation Pipeline
# Runs AutoQ -> LGR Search -> AutoE -> Retrieval Metrics with full logging
#
# Usage: ./run-eval.sh [options]
#   --fresh     Wipe all checkpoints and start fresh (FRESH_RUN=true)
#   --resume    Resume from checkpoints (default)
#   --pilot     1 global question (default)
#   --full      All configured questions
#
# Environment Variable Controls (discrete skip flags):
#   SKIP_AUTOQ=true               - Skip question generation (use existing questions)
#   SKIP_LGR_SEARCH=true          - Skip LGR search (use existing answers)
#   SKIP_AUTOE=true               - Skip assertion scoring
#   SKIP_RETRIEVAL_METRICS=true   - Skip retrieval reference + scores (default: true)
#   RESTART_FROM=<step>           - Wipe from step onwards: embeddings|clustering|questions|lgr_search|autoe
#   FRESH_RUN=true                - Wipe ALL checkpoints and start fresh
#
# Examples:
#   ./run-eval.sh --fresh                          # Full fresh run
#   SKIP_LGR_SEARCH=true ./run-eval.sh             # AutoQ only, stop for manual LGR
#   SKIP_AUTOQ=true SKIP_LGR_SEARCH=true ./run-eval.sh  # AutoE + retrieval only
#   SKIP_AUTOQ=true SKIP_LGR_SEARCH=true SKIP_AUTOE=true SKIP_RETRIEVAL_METRICS=false ./run-eval.sh  # Retrieval metrics only

set -e

# Parse arguments
FRESH_RUN="false"
MODE="pilot"

for arg in "$@"; do
    case $arg in
        --fresh)
            FRESH_RUN="true"
            shift
            ;;
        --resume)
            FRESH_RUN="false"
            shift
            ;;
        --pilot)
            MODE="pilot"
            shift
            ;;
        --full)
            MODE="full"
            shift
            ;;
    esac
done

export FRESH_RUN

CONFIG_PATH="/config/settings.yaml"
# Use env var if set, otherwise default to ephemeral storage
# MUST export so Python subprocess sees it
export CHECKPOINT_DIR="${CHECKPOINT_DIR:-/data/output/checkpoints}"

# Safety check: CHECKPOINT_DIR must not be empty (prevents accidental root deletion)
if [ -z "$CHECKPOINT_DIR" ]; then
    echo "ERROR: CHECKPOINT_DIR cannot be empty. This is a safety check."
    exit 1
fi

# ALL outputs go to NFS checkpoint directory (not ephemeral storage)
export OUTPUT_DIR="$CHECKPOINT_DIR/output"
export LOG_DIR="$CHECKPOINT_DIR/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Checkpoint paths
EMBEDDINGS_DIR="$CHECKPOINT_DIR/embeddings"
CLUSTERING_DIR="$CHECKPOINT_DIR/clustering"
QUESTIONS_DIR="$OUTPUT_DIR"
ANSWERS_FILE="$OUTPUT_DIR/answers.json"
EVAL_DIR="$OUTPUT_DIR/autoe"

# Create directories on NFS
mkdir -p "$OUTPUT_DIR"
mkdir -p "$LOG_DIR"
mkdir -p "$OUTPUT_DIR/autoq"
mkdir -p "$OUTPUT_DIR/autoe"
mkdir -p "$CLUSTERING_DIR"

echo "=========================================="
echo "BenchmarkQED Evaluation Pipeline"
echo "Mode: $MODE"
echo "Fresh run: $FRESH_RUN"
echo "Timestamp: $TIMESTAMP"
echo "CHECKPOINT_DIR: $CHECKPOINT_DIR"
echo "OUTPUT_DIR: $OUTPUT_DIR (on NFS)"
echo "LOG_DIR: $LOG_DIR (on NFS)"
echo ""
echo "Skip flags:"
echo "  SKIP_AUTOQ: ${SKIP_AUTOQ:-false}"
echo "  SKIP_LGR_SEARCH: ${SKIP_LGR_SEARCH:-false}"
echo "  SKIP_AUTOE: ${SKIP_AUTOE:-false}"
echo "  SKIP_RETRIEVAL_METRICS: ${SKIP_RETRIEVAL_METRICS:-true}"
echo "  RESTART_FROM: ${RESTART_FROM:-<not set>}"
echo "=========================================="

# ============================================
# RESTART_FROM Logic - Wipe from specific step
# ============================================
# Order: embeddings -> clustering -> questions -> lgr_search -> autoe
# RESTART_FROM=X wipes X and everything after it
if [ -n "$RESTART_FROM" ]; then
    echo ""
    echo "[RESTART] RESTART_FROM=$RESTART_FROM"
    case $RESTART_FROM in
        embeddings)
            echo "  Wiping: embeddings, clustering, questions, answers, eval"
            rm -rf "$EMBEDDINGS_DIR"/* 2>/dev/null || true
            rm -rf "$CLUSTERING_DIR"/* 2>/dev/null || true
            rm -rf "$QUESTIONS_DIR"/*_questions 2>/dev/null || true
            rm -f "$ANSWERS_FILE" 2>/dev/null || true
            rm -rf "$EVAL_DIR"/* 2>/dev/null || true
            ;;
        clustering)
            echo "  Keeping: embeddings"
            echo "  Wiping: clustering, questions, answers, eval"
            rm -rf "$CLUSTERING_DIR"/* 2>/dev/null || true
            rm -rf "$QUESTIONS_DIR"/*_questions 2>/dev/null || true
            rm -f "$ANSWERS_FILE" 2>/dev/null || true
            rm -rf "$EVAL_DIR"/* 2>/dev/null || true
            ;;
        questions)
            echo "  Keeping: embeddings, clustering"
            echo "  Wiping: questions, answers, eval"
            rm -rf "$QUESTIONS_DIR"/*_questions 2>/dev/null || true
            rm -f "$ANSWERS_FILE" 2>/dev/null || true
            rm -rf "$EVAL_DIR"/* 2>/dev/null || true
            ;;
        lgr_search)
            echo "  Keeping: embeddings, clustering, questions"
            echo "  Wiping: answers, eval"
            rm -f "$ANSWERS_FILE" 2>/dev/null || true
            rm -rf "$EVAL_DIR"/* 2>/dev/null || true
            ;;
        autoe)
            echo "  Keeping: embeddings, clustering, questions, answers"
            echo "  Wiping: eval only"
            rm -rf "$EVAL_DIR"/* 2>/dev/null || true
            ;;
        *)
            echo "  WARNING: Unknown RESTART_FROM value: $RESTART_FROM"
            echo "  Valid values: embeddings, clustering, questions, lgr_search, autoe"
            ;;
    esac
    echo "[RESTART] Done"
fi

# Wipe if fresh run requested (legacy support)
if [ "$FRESH_RUN" = "true" ]; then
    echo ""
    echo "[WIPE] Clearing all checkpoints and outputs..."
    rm -rf "$CHECKPOINT_DIR"/*
    rm -f "$OUTPUT_DIR"/*.json
    rm -rf "$LOG_DIR"/*
    echo "[WIPE] Done - starting fresh"
    mkdir -p "$CHECKPOINT_DIR"
    mkdir -p "$LOG_DIR"
fi

# Show checkpoint status
echo ""
echo "Checkpoint status:"
if [ -f "$EMBEDDINGS_DIR/state.json" ]; then
    EMBED_COUNT=$(python3 -c "import json; d=json.load(open('$EMBEDDINGS_DIR/state.json')); print(len(d.get('completed_batches',[])))" 2>/dev/null || echo "?")
    echo "  Embeddings: $EMBED_COUNT batches"
else
    echo "  Embeddings: No checkpoint"
fi
if [ -f "$CLUSTERING_DIR/state.json" ]; then
    echo "  Clustering: Cached"
else
    echo "  Clustering: No checkpoint"
fi
QUESTION_COUNT=$(find "$QUESTIONS_DIR" -name "selected_questions.json" 2>/dev/null | wc -l)
if [ "$QUESTION_COUNT" -gt 0 ]; then
    echo "  Questions: Found $QUESTION_COUNT question files"
else
    echo "  Questions: No checkpoint"
fi
if [ -f "$ANSWERS_FILE" ]; then
    ANSWER_COUNT=$(python3 -c "import json; d=json.load(open('$ANSWERS_FILE')); print(len([q for q in d if q.get('answer')]))" 2>/dev/null || echo "?")
    echo "  Answers: $ANSWER_COUNT completed"
else
    echo "  Answers: No checkpoint"
fi
if [ -d "$EVAL_DIR" ] && [ "$(ls -A $EVAL_DIR 2>/dev/null)" ]; then
    echo "  Evaluation: Has results"
else
    echo "  Evaluation: No checkpoint"
fi
echo ""

# ============================================
# Step 1: AutoQ - Generate Questions
# ============================================
if [ "${SKIP_AUTOQ:-false}" = "true" ]; then
    echo ""
    echo "[1/5] Skipping AutoQ (SKIP_AUTOQ=true)"
    echo "Using existing questions from: $OUTPUT_DIR/"
    ls -la "$OUTPUT_DIR"/*_questions/ 2>/dev/null || echo "  No question files found"
else
    echo ""
    echo "[1/5] Running AutoQ - Question Generation"
    echo "=========================================="
    AUTOQ_LOG="$LOG_DIR/autoq_${TIMESTAMP}.log"
    echo "Log file: $AUTOQ_LOG"

    # Use Python wrapper that initializes retry logic and logging
    python3 /app/scripts/run_autoq.py "$CONFIG_PATH" "$OUTPUT_DIR" 2>&1 | tee "$AUTOQ_LOG"
    AUTOQ_EXIT=${PIPESTATUS[0]}

    if [ $AUTOQ_EXIT -ne 0 ]; then
        echo "ERROR: AutoQ failed with exit code $AUTOQ_EXIT"
        exit 1
    fi
    echo "AutoQ completed successfully"
fi
echo "Questions saved to: $OUTPUT_DIR/ (on NFS)"
ls -la "$OUTPUT_DIR"/*_questions/ 2>/dev/null || true

# ============================================
# Step 2: LGR Search
# ============================================
if [ "${SKIP_LGR_SEARCH:-false}" = "true" ]; then
    echo ""
    echo "[2/5] Skipping LGR Search (SKIP_LGR_SEARCH=true)"
    if [ -f "$OUTPUT_DIR/answers.json" ]; then
        echo "Using existing answers from: $OUTPUT_DIR/answers.json"
    else
        echo "WARNING: No answers.json found - AutoE will fail if not skipped"
    fi
else
    # Step 2: LGR Search - Send questions to queue and get answers
    echo ""
    echo "[2/5] Running LGR Search - Queue-based Search"
    echo "=========================================="
    LGR_LOG="$LOG_DIR/lgr_search_${TIMESTAMP}.log"
    echo "Log file: $LGR_LOG"

    # Combine ALL question types (local + global + linked) into a single file
    # This ensures all generated questions are sent to LGR Search
    COMBINED_QUESTIONS="$OUTPUT_DIR/combined_questions.json"
    QUESTIONS_FOUND=0
    
    echo "Searching for question files to combine..."
    
    # Collect all selected_questions.json files from different question types
    python3 << 'COMBINE_QUESTIONS_EOF'
import json
import os
import sys

output_dir = os.environ.get('OUTPUT_DIR', '/mnt/checkpoints/benchmark-qed/output')
combined_file = os.path.join(output_dir, 'combined_questions.json')

# Question types to look for (in order)
question_types = ['data_global', 'data_local', 'data_linked', 'activity_global', 'activity_local']
all_questions = []
sources = []

for qtype in question_types:
    # Prefer selected_questions.json over candidate_questions.json
    selected = os.path.join(output_dir, f'{qtype}_questions', 'selected_questions.json')
    candidate = os.path.join(output_dir, f'{qtype}_questions', 'candidate_questions.json')
    
    questions_file = None
    if os.path.exists(selected):
        questions_file = selected
    elif os.path.exists(candidate):
        questions_file = candidate
    
    if questions_file:
        try:
            with open(questions_file) as f:
                questions = json.load(f)
                if isinstance(questions, list):
                    count = len(questions)
                    all_questions.extend(questions)
                    sources.append(f"{qtype}: {count} questions from {os.path.basename(questions_file)}")
                    print(f"  ✓ {qtype}: {count} questions", file=sys.stderr)
        except Exception as e:
            print(f"  ✗ {qtype}: Error reading {questions_file}: {e}", file=sys.stderr)

if all_questions:
    with open(combined_file, 'w') as f:
        json.dump(all_questions, f, indent=2)
    print(f"\nCombined {len(all_questions)} total questions:", file=sys.stderr)
    for src in sources:
        print(f"  - {src}", file=sys.stderr)
    print(f"Saved to: {combined_file}", file=sys.stderr)
    print(len(all_questions))  # Output count for shell to capture
else:
    print("ERROR: No questions found in any question type directory", file=sys.stderr)
    sys.exit(1)
COMBINE_QUESTIONS_EOF

    COMBINE_EXIT=$?
    if [ $COMBINE_EXIT -ne 0 ]; then
        echo "ERROR: Failed to combine questions"
        exit 2
    fi
    
    if [ ! -f "$COMBINED_QUESTIONS" ]; then
        echo "ERROR: Combined questions file not created"
        exit 2
    fi
    
    QUESTIONS_FILE="$COMBINED_QUESTIONS"
    QUESTION_COUNT=$(python3 -c "import json; print(len(json.load(open('$COMBINED_QUESTIONS'))))")
    echo "Questions file: $QUESTIONS_FILE ($QUESTION_COUNT questions)"

    # Run LGR search V5 (V2 blob polling with short_id resolution)
    # lgr_search_v5.py reads questions from OUTPUT_DIR, saves answers + retrieval data to OUTPUT_DIR
    python3 -u /app/scripts/lgr_search_v5.py 2>&1 | tee "$LGR_LOG"
    LGR_EXIT=${PIPESTATUS[0]}

    if [ $LGR_EXIT -ne 0 ]; then
        echo "ERROR: LGR Search failed with exit code $LGR_EXIT"
        exit 2
    fi
    echo "LGR Search completed successfully"
    echo "Answers saved to: $OUTPUT_DIR/answers.json"
    echo "Retrieval data saved to: $OUTPUT_DIR/lgr_retrieval_data.json"
fi

# ============================================
# Step 3: AutoE - Assertion Scoring
# ============================================
if [ "${SKIP_AUTOE:-false}" = "true" ]; then
    echo ""
    echo "[3/5] Skipping AutoE (SKIP_AUTOE=true)"
else
    # Step 3: AutoE - Evaluate Answers
    echo ""
    echo "[3/5] Running AutoE - Answer Evaluation"
    echo "=========================================="
AUTOE_LOG="$LOG_DIR/autoe_${TIMESTAMP}.log"
echo "Log file: $AUTOE_LOG"

# Combine ALL assertions files (matching the combined questions)
# Each question type has its own assertions.json that must be merged
COMBINED_ASSERTIONS="$OUTPUT_DIR/combined_assertions.json"

echo "Searching for assertion files to combine..."

python3 << 'COMBINE_ASSERTIONS_EOF'
import json
import os
import sys

output_dir = os.environ.get('OUTPUT_DIR', '/mnt/checkpoints/benchmark-qed/output')
combined_file = os.path.join(output_dir, 'combined_assertions.json')

# Question types to look for (same order as questions)
question_types = ['data_global', 'data_local', 'data_linked', 'activity_global', 'activity_local']
all_assertions = []
sources = []

for qtype in question_types:
    assertions_file = os.path.join(output_dir, f'{qtype}_questions', 'assertions.json')
    
    if os.path.exists(assertions_file):
        try:
            with open(assertions_file) as f:
                assertions = json.load(f)
                if isinstance(assertions, list):
                    count = len(assertions)
                    all_assertions.extend(assertions)
                    sources.append(f"{qtype}: {count} assertion sets")
                    print(f"  ✓ {qtype}: {count} assertion sets", file=sys.stderr)
        except Exception as e:
            print(f"  ✗ {qtype}: Error reading {assertions_file}: {e}", file=sys.stderr)

if all_assertions:
    with open(combined_file, 'w') as f:
        json.dump(all_assertions, f, indent=2)
    print(f"\nCombined {len(all_assertions)} total assertion sets:", file=sys.stderr)
    for src in sources:
        print(f"  - {src}", file=sys.stderr)
    print(f"Saved to: {combined_file}", file=sys.stderr)
else:
    print("ERROR: No assertions found in any question type directory", file=sys.stderr)
    sys.exit(1)
COMBINE_ASSERTIONS_EOF

COMBINE_ASSERT_EXIT=$?
if [ $COMBINE_ASSERT_EXIT -ne 0 ]; then
    echo "WARNING: Failed to combine assertions, looking for fallback..."
    # Fallback to first available assertions.json
    ASSERTIONS_FILE=$(find "$OUTPUT_DIR" -name "assertions.json" 2>/dev/null | head -1)
    if [ -z "$ASSERTIONS_FILE" ]; then
        echo "ERROR: No assertions file found"
        exit 2
    fi
else
    ASSERTIONS_FILE="$COMBINED_ASSERTIONS"
fi

echo "Using assertions file: $ASSERTIONS_FILE"

# Transform assertions from objects to strings for AutoE compatibility
# AutoQ saves assertions as objects: {"statement": "...", "score": 0.8, "rank": 1}
# AutoE expects plain strings: "..."
# This transforms assertions to extract just the statement field
AUTOE_ASSERTIONS_FILE="$OUTPUT_DIR/autoe_assertions_${TIMESTAMP}.json"
python3 -c "
import json
import sys

with open('$ASSERTIONS_FILE', 'r') as f:
    data = json.load(f)

# Transform each question's assertions
for item in data:
    if 'assertions' in item and isinstance(item['assertions'], list):
        transformed = []
        for a in item['assertions']:
            # Handle both dict (with statement) and string formats
            if isinstance(a, dict):
                transformed.append(a.get('statement', str(a)))
            else:
                transformed.append(str(a))
        item['assertions'] = transformed

with open('$AUTOE_ASSERTIONS_FILE', 'w') as f:
    json.dump(data, f, indent=2)

print(f'Transformed {len(data)} questions for AutoE')
"
TRANSFORM_EXIT=$?
if [ $TRANSFORM_EXIT -ne 0 ]; then
    echo "ERROR: Failed to transform assertions file"
    echo "Using original file as fallback"
    AUTOE_ASSERTIONS_FILE="$ASSERTIONS_FILE"
else
    echo "Transformed assertions saved to: $AUTOE_ASSERTIONS_FILE"
fi

# Create dynamic AutoE config for assertion scoring
AUTOE_CONFIG="$OUTPUT_DIR/autoe_config_${TIMESTAMP}.yaml"
cat > "$AUTOE_CONFIG" << EOF
# AutoE Assertion Scoring Config (auto-generated by run-eval.sh)
generated:
  name: lgr_search
  answer_base_path: $OUTPUT_DIR/answers.json

assertions:
  assertions_path: $AUTOE_ASSERTIONS_FILE

pass_threshold: 0.5
trials: 4

llm_config:
  model: "gpt-5.2"
  auth_type: "azure_managed_identity"
  concurrent_requests: 8
  llm_provider: "azure.openai.chat"
  init_args:
    api_version: "2024-12-01-preview"
    azure_endpoint: "${AZURE_OPENAI_ENDPOINT}"
    azure_deployment: "gpt-5.2"
  call_args:
    temperature: 0.0
    seed: 42
    reasoning_effort: "none"
EOF

echo "AutoE config created: $AUTOE_CONFIG"
echo "  - Answers: $OUTPUT_DIR/answers.json"
echo "  - Assertions: $ASSERTIONS_FILE"

# Create output directory for scores
AUTOE_OUTPUT="$OUTPUT_DIR/autoe_scores_${TIMESTAMP}"
mkdir -p "$AUTOE_OUTPUT"

# Run AutoE assertion-scores with the config
# Key mappings for assertions.json (from AutoQ _save_assertions):
#   - question_id: unique ID for the question
#   - question_text: the question text  
#   - assertions: array of ranked assertion objects with 'statement' field
# Key mappings for answers.json (from lgr_search_eval):
#   - question_id: matches the question ID
#   - question: the question text (note: 'question' not 'question_text')
#   - answer: the LGR response
benchmark-qed autoe assertion-scores "$AUTOE_CONFIG" "$AUTOE_OUTPUT" \
    --question-id-key "question_id" \
    --question-text-key "question" \
    --answer-text-key "answer" \
    --assertions-key "assertions" \
    2>&1 | tee "$AUTOE_LOG"
AUTOE_EXIT=${PIPESTATUS[0]}

if [ $AUTOE_EXIT -ne 0 ]; then
    echo "ERROR: AutoE failed with exit code $AUTOE_EXIT"
    exit 3
fi
echo "AutoE completed successfully"

# Step 4: Export Q&A to PDF
echo ""
echo "[4/5] Exporting Results to PDF"
echo "=========================================="
PDF_FILE="$OUTPUT_DIR/eval_results_${TIMESTAMP}.pdf"
python3 /app/scripts/export_qa_to_pdf.py "$OUTPUT_DIR" "$PDF_FILE" 2>&1 || true
if [ -f "$PDF_FILE" ]; then
    echo "PDF exported: $PDF_FILE"
else
    echo "WARNING: PDF export failed (reportlab may not be installed)"
fi

fi  # End of SKIP_AUTOE check

echo ""
echo "=========================================="
echo "AutoE Phase Complete!"
echo "=========================================="

# ============================================
# Step 5: Retrieval Metrics (optional)
# ============================================
# Controlled by SKIP_RETRIEVAL_METRICS (default: true, skip unless explicitly enabled)
# Requires: text_units.parquet, lgr_retrieval_data.json, questions
if [ "${SKIP_RETRIEVAL_METRICS:-true}" = "false" ]; then
    echo ""
    echo "[5/5] Running Retrieval Metrics"
    echo "=========================================="

    RETRIEVAL_REF_DIR="$OUTPUT_DIR/retrieval_reference"
    RETRIEVAL_SCORES_DIR="$OUTPUT_DIR/retrieval_scores_v3"
    RETRIEVAL_NUM_CLUSTERS="${RETRIEVAL_NUM_CLUSTERS:-$NUM_CLUSTERS}"
    mkdir -p "$RETRIEVAL_REF_DIR"
    mkdir -p "$RETRIEVAL_SCORES_DIR"

    # Pre-flight checks
    echo "Pre-flight checks..."
    RETRIEVAL_READY=true
    for f in "$OUTPUT_DIR/text_units.parquet" \
             "$OUTPUT_DIR/data_global_questions/selected_questions.json" \
             "$OUTPUT_DIR/lgr_retrieval_data.json"; do
        if [ -f "$f" ]; then
            echo "  ✓ $(basename $f)"
        else
            echo "  ✗ MISSING: $f"
            RETRIEVAL_READY=false
        fi
    done

    if [ "$RETRIEVAL_READY" = "false" ]; then
        echo "WARNING: Skipping retrieval metrics - missing required files"
    else
        # Step 5a: Generate Retrieval Reference
        echo ""
        echo "[5a] Generate Retrieval Reference (num_clusters=$RETRIEVAL_NUM_CLUSTERS)"
        echo "=========================================="

        RETRIEVAL_REF_CONFIG="$OUTPUT_DIR/retrieval_ref_config_v3.yaml"
        cat > "$RETRIEVAL_REF_CONFIG" << REFEOF
llm_config:
  model: "gpt-5.2"
  auth_type: "azure_managed_identity"
  concurrent_requests: 8
  llm_provider: "azure.openai.chat"
  init_args:
    api_version: "2024-12-01-preview"
    azure_endpoint: "${AZURE_OPENAI_ENDPOINT}"
    azure_deployment: "gpt-5.2"
  call_args:
    temperature: 0.0
    seed: 42
    reasoning_effort: "none"

embedding_config:
  model: "text-embedding-3-small"
  auth_type: "azure_managed_identity"
  concurrent_requests: 32
  llm_provider: "azure.openai.embedding"
  init_args:
    api_version: "2024-12-01-preview"
    azure_endpoint: "${AZURE_OPENAI_ENDPOINT}"
    azure_deployment: "text-embedding-3-small"

question_sets:
  - name: "leukemia_global"
    questions_path: "$OUTPUT_DIR/data_global_questions/selected_questions.json"

text_units_path: "$OUTPUT_DIR/text_units.parquet"
output_dir: "$RETRIEVAL_REF_DIR"
num_clusters: $RETRIEVAL_NUM_CLUSTERS
save_clusters: true
semantic_neighbors: 50
centroid_neighbors: 10
relevance_threshold: 2
assessor_type: bing
concurrent_requests: 32
cache_dir: "$RETRIEVAL_REF_DIR/cache"
REFEOF

        RETRIEVAL_REF_LOG="$LOG_DIR/retrieval_ref_${TIMESTAMP}.log"
        echo "Config: $RETRIEVAL_REF_CONFIG"
        echo "Log: $RETRIEVAL_REF_LOG"
        benchmark-qed autoe generate-retrieval-reference "$RETRIEVAL_REF_CONFIG" --print-model-usage 2>&1 | tee "$RETRIEVAL_REF_LOG"
        RETREF_EXIT=${PIPESTATUS[0]}

        if [ $RETREF_EXIT -ne 0 ]; then
            echo "ERROR: generate-retrieval-reference failed with exit code $RETREF_EXIT"
            echo "Skipping retrieval-scores"
        else
            echo "✓ Retrieval reference generation complete"

            # Step 5b: Retrieval Scores
            echo ""
            echo "[5b] Retrieval Scores"
            echo "=========================================="

            RETRIEVAL_SCORES_CONFIG="$OUTPUT_DIR/retrieval_scores_config_v3.yaml"
            cat > "$RETRIEVAL_SCORES_CONFIG" << SCOREEOF
llm_config:
  model: "gpt-5.2"
  auth_type: "azure_managed_identity"
  concurrent_requests: 8
  llm_provider: "azure.openai.chat"
  init_args:
    api_version: "2024-12-01-preview"
    azure_endpoint: "${AZURE_OPENAI_ENDPOINT}"
    azure_deployment: "gpt-5.2"
  call_args:
    temperature: 0.0
    seed: 42
    reasoning_effort: "none"

rag_methods:
  - name: "lgr_v5"
    retrieval_results_path: "$OUTPUT_DIR/lgr_retrieval_data.json"

question_sets:
  - "leukemia_global"

reference_dir: "$RETRIEVAL_REF_DIR/leukemia_global/clusters_${RETRIEVAL_NUM_CLUSTERS}"
clusters_path: "$RETRIEVAL_REF_DIR/clusters/clusters_${RETRIEVAL_NUM_CLUSTERS}.json"
text_units_path: "$OUTPUT_DIR/text_units.parquet"
output_dir: "$RETRIEVAL_SCORES_DIR"

relevance_threshold: 2
context_id_key: "short_id"
context_text_key: "text"
run_significance_test: false
fidelity_metric: "js"
cache_dir: "$RETRIEVAL_SCORES_DIR/cache"
SCOREEOF

            RETRIEVAL_SCORES_LOG="$LOG_DIR/retrieval_scores_${TIMESTAMP}.log"
            echo "Config: $RETRIEVAL_SCORES_CONFIG"
            echo "Log: $RETRIEVAL_SCORES_LOG"
            benchmark-qed autoe retrieval-scores "$RETRIEVAL_SCORES_CONFIG" --print-model-usage 2>&1 | tee "$RETRIEVAL_SCORES_LOG"
            RETSCORE_EXIT=${PIPESTATUS[0]}

            if [ $RETSCORE_EXIT -ne 0 ]; then
                echo "ERROR: retrieval-scores failed with exit code $RETSCORE_EXIT"
            else
                echo "✓ Retrieval scores complete"
                echo "Results in: $RETRIEVAL_SCORES_DIR"
                ls -la "$RETRIEVAL_SCORES_DIR"/ 2>/dev/null
            fi
        fi
    fi
else
    echo ""
    echo "[5/5] Skipping Retrieval Metrics (SKIP_RETRIEVAL_METRICS=true)"
    echo "To enable: set SKIP_RETRIEVAL_METRICS=false"
fi

# Final Summary
echo ""
echo "=========================================="
echo "Pipeline Complete!"
echo "=========================================="
echo "Logs directory: $LOG_DIR"
echo ""
echo "Output files:"
ls -la "$OUTPUT_DIR"/*.json 2>/dev/null || echo "  (no JSON files found)"
ls -la "$OUTPUT_DIR"/*.pdf 2>/dev/null || echo "  (no PDF files found)"
echo "=========================================="

# Keep container alive for result inspection
echo ""
echo "Container will stay alive for 24 hours for result inspection."
echo "Deactivate when done: az containerapp revision deactivate ..."
sleep 86400
