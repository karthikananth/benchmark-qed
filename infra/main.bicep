// =============================================================================
// BenchmarkQED Infrastructure Deployment
// =============================================================================
// Resource Group: rg-benchmarkqed-poc (or reuse rg-lazygraphrag-poc)
// Region: Sweden Central
// Purpose: Deploy infrastructure for BenchmarkQED evaluation pipeline
// Generated: 2026-04-01
// =============================================================================
//
// Architecture Overview:
// ┌─────────────────────────────────────────────────────────────────────────────┐
// │                    AZURE CONTAINER APPS ENVIRONMENT                         │
// │                         (aca-env-benchmarkqed)                              │
// ├─────────────────────────────────────────────────────────────────────────────┤
// │  ┌────────────────────┐      ┌────────────────────────────────────────┐    │
// │  │  benchmark-qed     │      │  science-bookshelf (external)          │    │
// │  │  Container App     │ Queue│  LGR Search processor                  │    │
// │  │  - AutoQ           │ ───> │  (separate deployment)                 │    │
// │  │  - AutoE           │ <─── │                                        │    │
// │  └─────────┬──────────┘      └────────────────────────────────────────┘    │
// │            │ NFS Mount                                                      │
// │  ┌─────────▼──────────┐                                                    │
// │  │   NFS Storage      │  Checkpoints, embeddings, outputs                  │
// │  │   /mnt/checkpoints │                                                    │
// │  └────────────────────┘                                                    │
// └─────────────────────────────────────────────────────────────────────────────┘
//
// Key Differences from LazyGraphRAG deployment:
// - NO SQL Server (benchmark-qed doesn't use database)
// - NO spaCy service (not needed for evaluation)
// - Simpler networking (only needs blob + NFS + ACR endpoints)
// - Single container app (benchmark-qed) vs multiple
// =============================================================================

@description('Azure region for all resources')
param location string = 'swedencentral'

@description('Environment suffix for resource naming')
param envSuffix string = 'bqed-poc'

@description('Admin user object ID for Key Vault access (your Entra user/group)')
param adminObjectId string

@description('Tags for all resources')
param tags object = {
  project: 'BenchmarkQED'
  environment: 'poc'
  owner: 'AI for Science Platform'
}

// =============================================================================
// EXISTING RESOURCES (in rg-lazygraphrag-poc)
// =============================================================================
// AOAI account was recovered from soft-delete - reuse instead of creating new
@description('Resource group containing the existing AOAI account')
param existingAoaiResourceGroup string = 'rg-lazygraphrag-poc'

@description('Name of the existing AOAI account')
param existingAoaiName string = 'aoai-lgr-poc'

// =============================================================================
// VARIABLES
// =============================================================================

// Resource names
var vnetName = 'vnet-${envSuffix}'
var snetAcaName = 'snet-aca'
var snetPeName = 'snet-private-endpoints'

var kvName = 'kv-${envSuffix}'
var acrName = 'acr${replace(envSuffix, '-', '')}'
var aoaiName = 'aoai-${envSuffix}'
var laName = 'la-${envSuffix}'
var acaEnvName = 'aca-env-${envSuffix}'

var stBlobDataName = 'stbqedmpoxdata'
var stNfsName = 'stbqednfs'

var miAppName = 'id-${envSuffix}'
var miAcrPullName = 'mi-${envSuffix}-acrpull'

// Role Definition IDs (built-in Azure roles)
var roleKeyVaultSecretsUser = '4633458b-17de-408a-b874-0445c86b69e6'
var roleCognitiveServicesOpenAIUser = '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'
var roleStorageBlobDataContributor = 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
var roleAcrPull = '7f951dda-4ed3-4680-a7ca-43fe172d538d'

// DNS Zone names
var dnsZones = [
  'privatelink.vaultcore.azure.net'
  'privatelink.blob.core.windows.net'
  'privatelink.file.core.windows.net'
  'privatelink.azurecr.io'
]

// =============================================================================
// 1. LOG ANALYTICS WORKSPACE (Deploy first - other resources depend on it)
// =============================================================================

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: laName
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
    workspaceCapping: {
      dailyQuotaGb: 5
    }
  }
}

// =============================================================================
// 2. NETWORKING
// =============================================================================

resource vnet 'Microsoft.Network/virtualNetworks@2023-05-01' = {
  name: vnetName
  location: location
  tags: tags
  properties: {
    addressSpace: {
      addressPrefixes: ['10.0.0.0/16']
    }
    subnets: [
      {
        name: snetAcaName
        properties: {
          addressPrefix: '10.0.0.0/21'  // /21 required for ACA (2048 IPs)
          delegations: [
            {
              name: 'Microsoft.App.environments'
              properties: {
                serviceName: 'Microsoft.App/environments'
              }
            }
          ]
        }
      }
      {
        name: snetPeName
        properties: {
          addressPrefix: '10.0.8.0/24'
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
    ]
  }
}

// =============================================================================
// 3. MANAGED IDENTITIES
// =============================================================================

// Primary managed identity for app workloads (AOAI, Storage, KV access)
// Using 2024-11-30 API version which supports isolationScope property
resource miApp 'Microsoft.ManagedIdentity/userAssignedIdentities@2024-11-30' = {
  name: miAppName
  location: location
  tags: tags
  properties: {
    isolationScope: 'Regional'  // SFI compliance requirement
  }
}

// Separate MI for ACR pull (principle of least privilege)
resource miAcrPull 'Microsoft.ManagedIdentity/userAssignedIdentities@2024-11-30' = {
  name: miAcrPullName
  location: location
  tags: tags
  properties: {
    isolationScope: 'Regional'  // SFI compliance requirement
  }
}

// =============================================================================
// 4. KEY VAULT (SFI Compliant - RBAC mode, PE-only)
// =============================================================================

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: kvName
  location: location
  tags: tags
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    enableRbacAuthorization: true  // SFI: RBAC mode, not access policies
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    enablePurgeProtection: true  // SFI: deletion protection required
    publicNetworkAccess: 'Disabled'  // SFI: PE-only access
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'
    }
  }
}

// KV Secrets User role for app MI
resource roleAssignmentKvSecretsUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, miApp.id, roleKeyVaultSecretsUser)
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleKeyVaultSecretsUser)
    principalId: miApp.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// KV Secrets User role for admin (for management)
resource roleAssignmentKvSecretsAdmin 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, adminObjectId, roleKeyVaultSecretsUser)
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleKeyVaultSecretsUser)
    principalId: adminObjectId
    principalType: 'User'
  }
}

// KV diagnostics
resource kvDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'diag-${kvName}'
  scope: keyVault
  properties: {
    workspaceId: logAnalytics.id
    logs: [
      { category: 'AuditEvent', enabled: true }
    ]
    metrics: [
      { category: 'AllMetrics', enabled: true }
    ]
  }
}

// =============================================================================
// 5. AZURE CONTAINER REGISTRY (SFI Compliant - PE-only, Premium)
// =============================================================================

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location
  tags: tags
  sku: {
    name: 'Premium'  // Required for Private Endpoints
  }
  properties: {
    adminUserEnabled: false  // SFI: No admin user, use MI
    publicNetworkAccess: 'Disabled'  // SFI: PE-only
    networkRuleBypassOptions: 'AzureServices'
    policies: {
      retentionPolicy: {
        days: 30
        status: 'enabled'
      }
    }
  }
}

// ACR Pull role for ACR-pull MI
resource roleAssignmentAcrPull 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(acr.id, miAcrPull.id, roleAcrPull)
  scope: acr
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleAcrPull)
    principalId: miAcrPull.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// ACR diagnostics
resource acrDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'diag-${acrName}'
  scope: acr
  properties: {
    workspaceId: logAnalytics.id
    logs: [
      { category: 'ContainerRegistryRepositoryEvents', enabled: true }
      { category: 'ContainerRegistryLoginEvents', enabled: true }
    ]
    metrics: [
      { category: 'AllMetrics', enabled: true }
    ]
  }
}

// =============================================================================
// 6. AZURE OPENAI (Reference existing account in rg-lazygraphrag-poc)
// =============================================================================
// Deployments already exist: gpt-5.2 (7000 TPM), text-embedding-3-small (6880 TPM)

resource existingOpenai 'Microsoft.CognitiveServices/accounts@2024-04-01-preview' existing = {
  name: existingAoaiName
  scope: resourceGroup(existingAoaiResourceGroup)
}

// AOAI Cognitive Services OpenAI User role for MI (on the existing AOAI account)
// Using a module to deploy to a different resource group
module aoaiRoleAssignment 'aoai-role-assignment.bicep' = {
  name: 'aoai-role-assignment'
  scope: resourceGroup(existingAoaiResourceGroup)
  params: {
    aoaiName: existingAoaiName
    principalId: miApp.properties.principalId
    roleDefinitionId: roleCognitiveServicesOpenAIUser
  }
}

// =============================================================================
// 7. STORAGE ACCOUNTS
// =============================================================================

// Blob Storage for mpox input data
resource stBlobData 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: stBlobDataName
  location: location
  tags: tags
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    publicNetworkAccess: 'Disabled'  // SFI: PE-only
    allowSharedKeyAccess: false  // SFI: Entra-only auth
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'
    }
  }
}

// Blob container for mpox data
resource mpoxContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${stBlobData.name}/default/mpoxdata'
  properties: {
    publicAccess: 'None'
  }
}

// Blob Data Contributor role for MI
resource roleAssignmentBlob 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(stBlobData.id, miApp.id, roleStorageBlobDataContributor)
  scope: stBlobData
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleStorageBlobDataContributor)
    principalId: miApp.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// NFS Storage for checkpoints (FileStorage Premium)
// NOTE: NFS uses Entra ID auth (not shared keys), so allowSharedKeyAccess: false is fine
// NOTE: NFS requires supportsHttpsTrafficOnly: false (port 2049, not HTTPS)
resource stNfs 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: stNfsName
  location: location
  tags: tags
  kind: 'FileStorage'  // Required for NFS
  sku: {
    name: 'Premium_LRS'
  }
  properties: {
    publicNetworkAccess: 'Disabled'
    allowSharedKeyAccess: false  // SFI: Entra-only auth (NFS supports this)
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: false  // Required for NFS protocol
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'
    }
  }
}

// NFS file share
resource nfsShare 'Microsoft.Storage/storageAccounts/fileServices/shares@2023-01-01' = {
  name: '${stNfs.name}/default/checkpoints'
  properties: {
    enabledProtocols: 'NFS'
    shareQuota: 100  // 100 GB
  }
}

// =============================================================================
// 8. PRIVATE DNS ZONES
// =============================================================================

resource privateDnsZones 'Microsoft.Network/privateDnsZones@2020-06-01' = [for zone in dnsZones: {
  name: zone
  location: 'global'
  tags: tags
}]

resource vnetLinks 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = [for (zone, i) in dnsZones: {
  name: '${zone}/link-${vnetName}'
  location: 'global'
  properties: {
    virtualNetwork: {
      id: vnet.id
    }
    registrationEnabled: false
  }
  dependsOn: [privateDnsZones[i]]
}]

// =============================================================================
// 9. PRIVATE ENDPOINTS
// =============================================================================

var peSubnetId = '${vnet.id}/subnets/${snetPeName}'

// Key Vault PE
resource peKv 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: 'pe-${kvName}'
  location: location
  tags: tags
  properties: {
    subnet: {
      id: peSubnetId
    }
    privateLinkServiceConnections: [
      {
        name: 'kv-connection'
        properties: {
          privateLinkServiceId: keyVault.id
          groupIds: ['vault']
        }
      }
    ]
  }
}

resource peKvDnsGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-05-01' = {
  parent: peKv
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'kv'
        properties: {
          privateDnsZoneId: privateDnsZones[0].id  // vaultcore.azure.net
        }
      }
    ]
  }
}

// ACR PE
resource peAcr 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: 'pe-${acrName}'
  location: location
  tags: tags
  properties: {
    subnet: {
      id: peSubnetId
    }
    privateLinkServiceConnections: [
      {
        name: 'acr-connection'
        properties: {
          privateLinkServiceId: acr.id
          groupIds: ['registry']
        }
      }
    ]
  }
}

resource peAcrDnsGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-05-01' = {
  parent: peAcr
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'acr'
        properties: {
          privateDnsZoneId: privateDnsZones[3].id  // azurecr.io
        }
      }
    ]
  }
}

// Blob Storage PE
resource peBlob 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: 'pe-${stBlobDataName}'
  location: location
  tags: tags
  properties: {
    subnet: {
      id: peSubnetId
    }
    privateLinkServiceConnections: [
      {
        name: 'blob-connection'
        properties: {
          privateLinkServiceId: stBlobData.id
          groupIds: ['blob']
        }
      }
    ]
  }
}

resource peBlobDnsGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-05-01' = {
  parent: peBlob
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'blob'
        properties: {
          privateDnsZoneId: privateDnsZones[1].id  // blob.core.windows.net
        }
      }
    ]
  }
}

// NFS Storage PE
resource peNfs 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: 'pe-${stNfsName}'
  location: location
  tags: tags
  properties: {
    subnet: {
      id: peSubnetId
    }
    privateLinkServiceConnections: [
      {
        name: 'nfs-connection'
        properties: {
          privateLinkServiceId: stNfs.id
          groupIds: ['file']
        }
      }
    ]
  }
}

resource peNfsDnsGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-05-01' = {
  parent: peNfs
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'file'
        properties: {
          privateDnsZoneId: privateDnsZones[2].id  // file.core.windows.net
        }
      }
    ]
  }
}

// =============================================================================
// 10. CONTAINER APPS ENVIRONMENT
// =============================================================================

resource acaEnv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: acaEnvName
  location: location
  tags: tags
  properties: {
    vnetConfiguration: {
      infrastructureSubnetId: '${vnet.id}/subnets/${snetAcaName}'
      internal: false
    }
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
    workloadProfiles: [
      {
        name: 'Consumption'
        workloadProfileType: 'Consumption'
      }
      {
        name: 'E16'  // 4 vCPU, 16GB RAM - required for embedding 133K vectors
        workloadProfileType: 'E16'
        minimumCount: 0
        maximumCount: 1
      }
    ]
  }
  dependsOn: [peNfs]  // Ensure NFS PE is ready before ACA env
}

// NOTE: NFS Storage mount must be added via ARM REST API after deployment
// Bicep/CLI doesn't support nfsAzureFile property
// Command to run after deployment:
// $body = @{
//   properties = @{
//     nfsAzureFile = @{
//       server = "${stNfs.name}.file.core.windows.net"
//       shareName = "checkpoints"
//       accessMode = "ReadWrite"
//     }
//   }
// } | ConvertTo-Json -Depth 3
// az rest --method put --url "https://management.azure.com${acaEnv.id}/storages/checkpointsnfs?api-version=2024-10-02-preview" --body $body

// =============================================================================
// 11. KEY VAULT SECRETS
// =============================================================================

// Store AOAI endpoint (from existing account in rg-lazygraphrag-poc)
resource secretApiBase 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'api-base'
  properties: {
    value: existingOpenai.properties.endpoint
    attributes: {
      enabled: true
    }
  }
}

// Store MI client ID for container app to use
resource secretClientId 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'azure-client-id'
  properties: {
    value: miApp.properties.clientId
    attributes: {
      enabled: true
    }
  }
}

// =============================================================================
// OUTPUTS
// =============================================================================

output resourceGroupName string = resourceGroup().name
output location string = location

// Identity outputs
output miAppClientId string = miApp.properties.clientId
output miAppPrincipalId string = miApp.properties.principalId
output miAcrPullClientId string = miAcrPull.properties.clientId
output miAcrPullPrincipalId string = miAcrPull.properties.principalId

// Resource outputs for container app configuration
output acrLoginServer string = acr.properties.loginServer
output aoaiEndpoint string = existingOpenai.properties.endpoint
output kvUri string = keyVault.properties.vaultUri
output acaEnvId string = acaEnv.id
output nfsServer string = '${stNfs.name}.file.core.windows.net'
output nfsShareName string = 'checkpoints'
output blobStorageUrl string = 'https://${stBlobData.name}.blob.core.windows.net/mpoxdata'

// Container app deployment reference
output containerAppConfig object = {
  image: '${acr.properties.loginServer}/benchmark-qed:v25-azurelinux'
  workloadProfile: 'E16'
  envVars: {
    AZURE_OPENAI_ENDPOINT: 'secretRef:api-base'
    AZURE_CLIENT_ID: 'secretRef:azure-client-id'
    BLOB_INPUT_URL: 'https://${stBlobData.name}.blob.core.windows.net/mpoxdata'
    CHECKPOINT_DIR: '/mnt/checkpoints/benchmark-qed'
  }
  volumeMount: {
    name: 'checkpoint-vol'
    mountPath: '/mnt/checkpoints'
    storageName: 'checkpointsnfs'
  }
}
