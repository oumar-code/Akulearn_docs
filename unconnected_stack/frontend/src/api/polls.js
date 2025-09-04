// API module for Polls microservice
export async function createPoll(question, options) {
  const response = await fetch('/polls_service/create_poll', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, options })
  });
  if (!response.ok) throw new Error('Failed to create poll');
  return await response.json();
}

export function pollWebSocket(pollId, onUpdate) {
  const ws = new WebSocket(`ws://localhost:8000/polls_service/ws/poll/${pollId}`);
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onUpdate(data.results);
  };
  return ws;
}
