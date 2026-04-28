# BenchmarkQED Infrastructure Deployment

Deploy Azure infrastructure for running BenchmarkQED evaluation pipeline.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AZURE CONTAINER APPS ENVIRONMENT                         │
│                         (aca-env-bqed-poc)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────┐      ┌────────────────────────────────────────┐    │
│  │  benchmark-qed     │      │  science-bookshelf (external)          │    │
│  │  Container App     │ Queue│  LGR Search processor                  │    │
│  │  - AutoQ           │ ───> │  (separate resource group)             │    │
│  │  - AutoE           │ <─── │                                        │    │
│  └─────────┬──────────┘      └────────────────────────────────────────┘    │
│            │ NFS Mount                                                      │
│  ┌─────────▼──────────┐                                                    │
│  │   NFS Storage      │  Checkpoints, embeddings, outputs                  │
│  │   /mnt/checkpoints │                                                    │
│  └────────────────────┘                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Prerequisites

1. Azure CLI installed and logged in
2. Bicep CLI (`az bicep install`)
3. Contributor access to subscription
4. Your Entra user/group object ID

## Quick Start

```powershell
# 1. Set variables
$RG = "rg-benchmarkqed-poc"
$LOCATION = "swedencentral"

# 2. Create resource group
az group create --name $RG --location $LOCATION

# 3. Get your Entra object ID
$ADMIN_OID = az ad signed-in-user show --query id -o tsv

# 4. Deploy infrastructure (~15-20 minutes)
az deployment group create `
  --resource-group $RG `
  --template-file main.bicep `
  --parameters main.parameters.json `
  --parameters adminObjectId=$ADMIN_OID

# 5. Validate
az deployment group show --resource-group $RG --name main --query properties.provisioningState
```

## What Gets Deployed

| Category | Resources |
|----------|-----------|
| **Networking** | VNet, 2 Subnets, 4 Private DNS Zones, 4 Private Endpoints |
| **Identity** | 2 Managed Identities, RBAC Role Assignments |
| **Storage** | Blob Storage (mpox data), NFS Storage (checkpoints) |
| **AI** | Azure OpenAI (gpt-5.2, text-embedding-3-small) |
| **Container** | ACR (Premium), ACA Environment (E16 profile) |
| **Security** | Key Vault (RBAC mode, PE-only) |
| **Monitoring** | Log Analytics, Diagnostic Settings |

## Post-Deployment Steps

### 1. Push Container Image

```powershell
# Get ACR name from outputs
$ACR = (az deployment group show -g $RG -n main --query properties.outputs.acrLoginServer.value -o tsv).Split('.')[0]

# Enable public access temporarily (SFI: disabled by default)
az acr update -n $ACR --public-network-enabled true

# Build and push (from benchmark-qed repo root)
docker build -t $ACR.azurecr.io/benchmark-qed:v25-azurelinux .
az acr login -n $ACR
docker push $ACR.azurecr.io/benchmark-qed:v25-azurelinux

# Disable public access
az acr update -n $ACR --public-network-enabled false
```

### 2. Upload mpox Dataset

```powershell
# Upload from local or use azcopy
az storage blob upload-batch `
  --account-name stbqedmpoxdata `
  --destination mpoxdata `
  --source ./datasets/mpox `
  --auth-mode login
```

### 3. Deploy Container App

```powershell
# Use the YAML template or az containerapp create
az containerapp create `
  --name benchmark-qed `
  --resource-group $RG `
  --environment aca-env-bqed-poc `
  --yaml ../deploy/benchmark-qed-aca.yaml
```

## Key Differences from LazyGraphRAG Deployment

| Component | LazyGraphRAG | BenchmarkQED |
|-----------|--------------|--------------|
| SQL Server | ✅ Required | ❌ Not needed |
| spaCy Service | ✅ Required | ❌ Not needed |
| Container Apps | 3 (lgr-app, lgr-search, spacy) | 1 (benchmark-qed) |
| Storage | 3 accounts | 2 accounts (blob + NFS) |
| AOAI Models | gpt-5.2, gpt-5-mini, embeddings | gpt-5.2, embeddings |

## Troubleshooting

### Validate Bicep
```powershell
az bicep build --file main.bicep
```

### What-If Deployment
```powershell
az deployment group what-if -g $RG --template-file main.bicep --parameters main.parameters.json
```

### Check Deployment Errors
```powershell
az deployment group list -g $RG --query "[].{name:name, state:properties.provisioningState}" -o table
```

## SFI Compliance Notes

- ✅ All resources use Private Endpoints (PE-only access)
- ✅ Key Vault uses RBAC mode (not access policies)
- ✅ Storage uses Entra-only auth (no shared keys)
- ✅ ACR has admin user disabled
- ✅ AOAI uses managed identity auth
- ✅ All resources log to Log Analytics
- ✅ Container image uses Azure Linux 3.0 base
