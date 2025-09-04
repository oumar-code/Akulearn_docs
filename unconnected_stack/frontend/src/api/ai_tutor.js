// API module for AI Tutor microservice
export async function askTutor(question, context = "") {
  const response = await fetch('/ai_tutor_service/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, context })
  });
  if (!response.ok) throw new Error('Failed to get AI Tutor response');
  return await response.json();
}
