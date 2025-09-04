// API module for Hardware Integration microservice
export async function getEnvStatus() {
  const response = await fetch('/hardware_integration_service/env_status');
  if (!response.ok) throw new Error('Failed to get environment status');
  return await response.json();
}
