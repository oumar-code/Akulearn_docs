// API module for Accessibility microservice
export async function textToSpeech(text, language = "en") {
  const response = await fetch('/accessibility_service/text_to_speech', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, language })
  });
  if (!response.ok) throw new Error('Failed to get TTS audio');
  return await response.json();
}
