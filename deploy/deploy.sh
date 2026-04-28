#!/bin/bash
# BenchmarkQED Deployment Script
# 
# SI#21: NEVER use --yaml for env vars. ALWAYS use --set-env-vars
# This script ensures env vars are properly set every deployment.
#
# Usage: ./deploy.sh <version>
# Example: ./deploy.sh v15

set -e

VERSION=${1:-"v15"}
RG="rg-lazygraphrag-poc"
APP="benchmark-qed"
ACR="acrlgrpoc"
IMAGE="$ACR.azurecr.io/benchmark-qed:$VERSION"

echo "=========================================="
echo "BenchmarkQED Deployment"
echo "Version: $VERSION"
echo "Image: $IMAGE"
echo "=========================================="

# SI#14: Deactivate old revisions before deploy
echo "[1/5] Checking current revisions..."
CURRENT_REV=$(az containerapp revision list -n $APP -g $RG --query "[?properties.active].name" -o tsv 2>/dev/null || echo "")
echo "      Current active: $CURRENT_REV"

# Enable ACR public access for deployment
echo "[2/5] Enabling ACR public access..."
az acr update -n $ACR --public-network-enabled true -o none

# Deploy with explicit env vars (SI#21)
echo "[3/5] Deploying $VERSION with env vars..."
az containerapp update -n $APP -g $RG \
  --image $IMAGE \
  --set-env-vars \
    "CHECKPOINT_DIR=/mnt/checkpoints/benchmark-qed" \
    "PYTHONUNBUFFERED=1" \
    "BLOB_INPUT_URL=https://stlgrmpoxdata.blob.core.windows.net/mpoxdata" \
    "LGR_STORAGE_ACCOUNT=stlgrpoc" \
    "LGR_IN_QUEUE=lgr-search-in" \
    "LGR_OUT_QUEUE=lgr-search-out" \
    "LGR_POLL_INTERVAL=30" \
    "LGR_TIMEOUT=120" \
  -o none

# Disable ACR public access
echo "[4/5] Disabling ACR public access..."
az acr update -n $ACR --public-network-enabled false -o none

# SI#14: Deactivate old revision if different
echo "[5/5] Cleaning up old revisions..."
NEW_REV=$(az containerapp revision list -n $APP -g $RG --query "[?properties.active].name" -o tsv)
if [ -n "$CURRENT_REV" ] && [ "$CURRENT_REV" != "$NEW_REV" ]; then
    echo "      Deactivating: $CURRENT_REV"
    az containerapp revision deactivate -n $APP -g $RG --revision $CURRENT_REV 2>/dev/null || true
fi

echo ""
echo "=========================================="
echo "Deployment Complete"
echo "New revision: $NEW_REV"
echo "=========================================="

# Verify env vars
echo ""
echo "Verifying env vars:"
az containerapp show -n $APP -g $RG --query "properties.template.containers[0].env[?name=='CHECKPOINT_DIR']" -o table
