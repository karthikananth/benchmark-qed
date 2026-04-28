#!/bin/bash
# BenchmarkQED Container Startup Script
# Downloads data from blob storage using azcopy with managed identity
# Then runs the specified command

set -e

echo "=========================================="
echo "BenchmarkQED Startup"
echo "=========================================="

# ============================================
# PIPELINE CONTROL ENVIRONMENT VARIABLES
# ============================================
# Skip controls (stop after a step):
#   SKIP_LGR_SEARCH=true  - Stop after AutoQ (question generation)
#   SKIP_AUTOE=true       - Stop after LGR Search (answers)
#
# Restart controls (wipe from a specific step):
#   RESTART_FROM=embeddings   - Wipe all, start fresh
#   RESTART_FROM=clustering   - Keep embeddings, wipe rest
#   RESTART_FROM=questions    - Keep embeddings+clustering, wipe questions onwards
#   RESTART_FROM=lgr_search   - Keep questions, wipe answers onwards
#   RESTART_FROM=autoe        - Keep answers, wipe eval only
#
# These are exported below so run-eval.sh can use them.
# ============================================

# Export pipeline control variables
export SKIP_LGR_SEARCH="${SKIP_LGR_SEARCH:-false}"
export SKIP_AUTOE="${SKIP_AUTOE:-false}"
export RESTART_FROM="${RESTART_FROM:-}"

# Debug: Show relevant env vars (masked for security)
echo "[0/4] Environment check:"
if [ -n "$AZURE_CLIENT_ID" ]; then
    echo "      AZURE_CLIENT_ID: ${AZURE_CLIENT_ID:0:8}..."
else
    echo "      AZURE_CLIENT_ID: NOT SET"
fi
echo "      AZURE_OPENAI_ENDPOINT: ${AZURE_OPENAI_ENDPOINT:-NOT SET}"
echo "      BLOB_INPUT_URL: ${BLOB_INPUT_URL:-NOT SET}"
echo ""
echo "      Pipeline controls:"
echo "        SKIP_LGR_SEARCH: $SKIP_LGR_SEARCH"
echo "        SKIP_AUTOE: $SKIP_AUTOE"
echo "        RESTART_FROM: ${RESTART_FROM:-<not set - resume all>}"

# Login to azcopy with managed identity
if [ -n "$AZURE_CLIENT_ID" ]; then
    echo "[1/4] Using managed identity for blob access..."
    echo "      Client ID: ${AZURE_CLIENT_ID:0:8}..."
else
    echo "[1/4] WARNING: AZURE_CLIENT_ID not set, using default credential"
fi

# Download input data from blob if BLOB_INPUT_URL is set
if [ -n "$BLOB_INPUT_URL" ]; then
    echo "[2/4] Downloading input data from: $BLOB_INPUT_URL"
    echo "      Target: /data/input/"
    
    # Download to temp directory first, only replace on success
    TEMP_INPUT="/data/input_download_$$"
    mkdir -p "$TEMP_INPUT"
    
    START_TIME=$(date +%s)
    if python3 /app/scripts/blob_download.py "$BLOB_INPUT_URL" "$TEMP_INPUT"; then
        # Download succeeded - replace existing input
        rm -rf /data/input/*
        mv "$TEMP_INPUT"/* /data/input/ 2>/dev/null || true
        rm -rf "$TEMP_INPUT"
        END_TIME=$(date +%s)
        FILE_COUNT=$(find /data/input -type f | wc -l)
        echo "      Downloaded $FILE_COUNT files in $((END_TIME - START_TIME)) seconds"
    else
        rm -rf "$TEMP_INPUT"
        echo "ERROR: Blob download failed"
        exit 1
    fi
else
    echo "[2/4] BLOB_INPUT_URL not set, skipping input download"
    echo "      (Using pre-mounted data or manual copy)"
fi

# Create output directory structure
echo "[3/4] Creating output directories..."
mkdir -p /data/output/autoq
mkdir -p /data/output/autoe
mkdir -p /data/output/logs
mkdir -p /data/cache

# Process settings.yaml with environment variable substitution
echo "[3.5/4] Processing settings.yaml with env vars..."
if [ -f /config/settings.yaml ]; then
    # Set defaults for question config
    export NUM_LOCAL_QUESTIONS="${NUM_LOCAL_QUESTIONS:-1}"
    export NUM_GLOBAL_QUESTIONS="${NUM_GLOBAL_QUESTIONS:-3}"
    export NUM_LINKED_QUESTIONS="${NUM_LINKED_QUESTIONS:-0}"
    export NUM_CLUSTERS="${NUM_CLUSTERS:-1}"
    export CHUNK_SIZE="${CHUNK_SIZE:-200}"
    export CHUNK_OVERLAP="${CHUNK_OVERLAP:-40}"
    export NUM_SAMPLES_PER_CLUSTER="${NUM_SAMPLES_PER_CLUSTER:-10}"
    export PRECHUNKED_TEXT_UNITS_PATH="${PRECHUNKED_TEXT_UNITS_PATH:-}"
    
    # Generation types: which question types to generate
    # Options: data_local, data_global, data_linked, activity_local, activity_global
    # Default: only data questions (no activity questions which generate many more)
    export GENERATION_TYPES="${GENERATION_TYPES:-data_local,data_global}"
    
    # IMPORTANT: Only substitute specific variables (not AZURE_OPENAI_ENDPOINT which is set later)
    # envsubst with variable list only replaces those specific vars
    envsubst '${NUM_LOCAL_QUESTIONS} ${NUM_GLOBAL_QUESTIONS} ${NUM_LINKED_QUESTIONS} ${NUM_CLUSTERS} ${CHUNK_SIZE} ${CHUNK_OVERLAP} ${NUM_SAMPLES_PER_CLUSTER} ${PRECHUNKED_TEXT_UNITS_PATH}' \
        < /config/settings.yaml > /config/settings.yaml.tmp
    mv /config/settings.yaml.tmp /config/settings.yaml
    
    echo "      NUM_CLUSTERS=$NUM_CLUSTERS"
    echo "      CHUNK_SIZE=$CHUNK_SIZE"
    echo "      CHUNK_OVERLAP=$CHUNK_OVERLAP"
    echo "      NUM_SAMPLES_PER_CLUSTER=$NUM_SAMPLES_PER_CLUSTER"
    echo "      PRECHUNKED_TEXT_UNITS_PATH=${PRECHUNKED_TEXT_UNITS_PATH:-<not set>}"
    echo "      NUM_LOCAL_QUESTIONS=$NUM_LOCAL_QUESTIONS"
    echo "      NUM_GLOBAL_QUESTIONS=$NUM_GLOBAL_QUESTIONS"  
    echo "      NUM_LINKED_QUESTIONS=$NUM_LINKED_QUESTIONS"
    echo "      GENERATION_TYPES=$GENERATION_TYPES"
fi

echo "[4/4] Starting: $@"
echo "=========================================="

# Execute the command passed to the container
exec "$@"
