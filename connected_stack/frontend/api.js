// Akulearn Connected App API Service
export async function fetchProgress(userId, token) {
  const res = await fetch(`https://your-backend-url/api/progress?user=${userId}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch progress');
  return res.json();
}
export async function submitQuiz(answers, token) {
  const res = await fetch('https://your-backend-url/api/quiz', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
    body: JSON.stringify({ answers }),
  });
  if (!res.ok) throw new Error('Quiz submission failed');
  return res.json();
}
export async function sendChat(message, token) {
  const res = await fetch('https://your-backend-url/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error('Chat failed');
  return res.json();
}
export async function login(username, password) {
  const res = await fetch('https://your-backend-url/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error('Login failed');
  return res.json();
}
