// API module for Akulearn Hub Integration
export async function syncContent(resourceType, resourceId) {
  const response = await fetch('/hub_integration_service/sync_content', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ resource_type: resourceType, resource_id: resourceId })
  });
  if (!response.ok) throw new Error('Failed to sync content');
  return await response.json();
}
