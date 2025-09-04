// Frontend API module to fetch solar status from backend
export async function fetchSolarStatus() {
  const response = await fetch('/solar/status');
  if (!response.ok) throw new Error('Failed to fetch solar status');
  return await response.json();
}
