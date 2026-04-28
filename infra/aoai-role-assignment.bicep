// Helper module for assigning roles on existing AOAI account
// Deployed to rg-lazygraphrag-poc (where aoai-lgr-poc exists)

@description('Name of the existing AOAI account')
param aoaiName string

@description('Principal ID to assign the role to')
param principalId string

@description('Role definition ID')
param roleDefinitionId string

resource existingOpenai 'Microsoft.CognitiveServices/accounts@2024-04-01-preview' existing = {
  name: aoaiName
}

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(existingOpenai.id, principalId, roleDefinitionId)
  scope: existingOpenai
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionId)
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}
