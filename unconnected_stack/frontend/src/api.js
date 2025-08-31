// Akulearn PWA API Service
export async function fetchProgress(userId) {
  const res = await fetch(`/api/progress?user=${userId}`);
  if (!res.ok) throw new Error('Failed to fetch progress');
  return res.json();
}
export async function submitQuiz(answers) {
  const res = await fetch('/api/quiz', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ answers }),
  });
  if (!res.ok) throw new Error('Quiz submission failed');
  return res.json();
}
export async function sendChat(message) {
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error('Chat failed');
  return res.json();
}
export async function login(username, password) {
  const res = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error('Login failed');
  return res.json();
}
