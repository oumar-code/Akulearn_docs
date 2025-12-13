// Akulearn Connected App API Service
const BASE_URL = 'http://localhost:8000/api'; // Update this for production

// Authentication APIs
export async function registerUser(userData) {
  const res = await fetch(`${BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData),
  });
  if (!res.ok) throw new Error('Registration failed');
  return res.json();
}

export async function verifyOtp(email, otp) {
  const res = await fetch(`${BASE_URL}/auth/verify-otp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, otp }),
  });
  if (!res.ok) throw new Error('OTP verification failed');
  return res.json();
}

export async function loginUser(email, password) {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error('Login failed');
  return res.json();
}

export async function refreshToken(refreshToken) {
  const res = await fetch(`${BASE_URL}/auth/refresh-token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });
  if (!res.ok) throw new Error('Token refresh failed');
  return res.json();
}

// Questions APIs
export async function searchQuestions(params, token) {
  const queryString = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE_URL}/questions/search?${queryString}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Search failed');
  return res.json();
}

export async function getQuestion(questionId, token) {
  const res = await fetch(`${BASE_URL}/questions/${questionId}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch question');
  return res.json();
}

export async function getRandomQuestions(count, filters = {}, token) {
  const params = { count, ...filters };
  const queryString = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE_URL}/questions/random?${queryString}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch random questions');
  return res.json();
}

// Progress APIs
export async function submitAttempt(questionId, userAnswer, timeTaken, token) {
  const res = await fetch(`${BASE_URL}/questions/attempt`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      question_id: questionId,
      user_answer: userAnswer,
      time_taken_seconds: timeTaken
    }),
  });
  if (!res.ok) throw new Error('Attempt submission failed');
  return res.json();
}

export async function getUserProgress(token) {
  const res = await fetch(`${BASE_URL}/user/progress`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed to fetch progress');
  return res.json();
}

// Legacy functions (keeping for compatibility)
export async function fetchProgress(userId, token) {
  return getUserProgress(token);
}

export async function submitQuiz(answers, token) {
  // This might need to be updated based on actual quiz submission endpoint
  const res = await fetch(`${BASE_URL}/quiz/submit`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ answers }),
  });
  if (!res.ok) throw new Error('Quiz submission failed');
  return res.json();
}

export async function sendChat(message, token) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error('Chat failed');
  return res.json();
}

export async function login(username, password) {
  return loginUser(username, password);
}

// Content APIs
export async function getSubjects(token) {
  const res = await fetch(`${BASE_URL}/content/subjects`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch subjects');
  return res.json();
}

export async function getTopicsBySubject(subject, token) {
  const res = await fetch(`${BASE_URL}/content/${encodeURIComponent(subject)}/topics`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch topics');
  return res.json();
}

export async function getContentByTopic(subject, topic, token) {
  const res = await fetch(`${BASE_URL}/content/${encodeURIComponent(subject)}/${encodeURIComponent(topic)}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch content');
  return res.json();
}

export async function getContentById(contentId, token) {
  const res = await fetch(`${BASE_URL}/content/${contentId}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch content');
  return res.json();
}

export async function searchContent(query, filters = {}, token) {
  const params = { q: query, ...filters };
  const queryString = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE_URL}/content/search?${queryString}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Search failed');
  return res.json();
}

export async function getRecommendedContent(token) {
  const res = await fetch(`${BASE_URL}/content/recommendations`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed to fetch recommendations');
  return res.json();
}

export async function updateContentProgress(contentId, progressData, token) {
  const res = await fetch(`${BASE_URL}/content/${contentId}/progress`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(progressData),
  });
  if (!res.ok) throw new Error('Failed to update progress');
  return res.json();
}

export async function getContentProgress(contentId, token) {
  const res = await fetch(`${BASE_URL}/content/${contentId}/progress`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed to fetch progress');
  return res.json();
}
