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

// ============================================================================
// NEW BACKEND SYSTEMS API INTEGRATION
// ============================================================================

// Code Playground APIs
export async function getCodePlaygroundData(token) {
  const res = await fetch(`${BASE_URL}/code-playground/data`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch code playground data');
  return res.json();
}

export async function runCode(code, language, token) {
  const res = await fetch(`${BASE_URL}/code-playground/run`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ code, language }),
  });
  if (!res.ok) throw new Error('Code execution failed');
  return res.json();
}

export async function getCodingChallenges(token) {
  const res = await fetch(`${BASE_URL}/code-playground/challenges`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch coding challenges');
  return res.json();
}

export async function submitCodingChallenge(challengeId, solution, token) {
  const res = await fetch(`${BASE_URL}/code-playground/challenges/${challengeId}/submit`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ solution }),
  });
  if (!res.ok) throw new Error('Challenge submission failed');
  return res.json();
}

// Dataset Integration APIs
export async function getDatasetData(token) {
  const res = await fetch(`${BASE_URL}/datasets/data`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch dataset data');
  return res.json();
}

export async function getDataAnalysisTools(token) {
  const res = await fetch(`${BASE_URL}/datasets/analysis-tools`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch data analysis tools');
  return res.json();
}

export async function analyzeDataset(datasetId, analysisType, token) {
  const res = await fetch(`${BASE_URL}/datasets/${datasetId}/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ analysis_type: analysisType }),
  });
  if (!res.ok) throw new Error('Dataset analysis failed');
  return res.json();
}

// Encyclopedia System APIs
export async function getEncyclopediaData(token) {
  const res = await fetch(`${BASE_URL}/encyclopedia/data`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch encyclopedia data');
  return res.json();
}

export async function searchEncyclopedia(query, subject, token) {
  const params = { q: query };
  if (subject) params.subject = subject;
  const queryString = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE_URL}/encyclopedia/search?${queryString}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Encyclopedia search failed');
  return res.json();
}

export async function getEncyclopediaEntry(subject, entryId, token) {
  const res = await fetch(`${BASE_URL}/encyclopedia/${subject}/${entryId}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch encyclopedia entry');
  return res.json();
}

// Flashcard System APIs
export async function getFlashcardData(token) {
  const res = await fetch(`${BASE_URL}/flashcards/data`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch flashcard data');
  return res.json();
}

export async function getStudySession(deckName, sessionLength, token) {
  const params = { session_length: sessionLength || 20 };
  const queryString = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE_URL}/flashcards/session/${deckName}?${queryString}`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed to get study session');
  return res.json();
}

export async function updateFlashcardProgress(cardId, difficulty, token) {
  const res = await fetch(`${BASE_URL}/flashcards/progress`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ card_id: cardId, difficulty }),
  });
  if (!res.ok) throw new Error('Failed to update flashcard progress');
  return res.json();
}

export async function getFlashcardStats(token) {
  const res = await fetch(`${BASE_URL}/flashcards/stats`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed to fetch flashcard stats');
  return res.json();
}

// Game-Based Learning APIs
export async function getGameData(token) {
  const res = await fetch(`${BASE_URL}/games/data`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch game data');
  return res.json();
}

export async function startGameSession(gameId, token) {
  const res = await fetch(`${BASE_URL}/games/${gameId}/start`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
  });
  if (!res.ok) throw new Error('Failed to start game session');
  return res.json();
}

export async function submitGameScore(gameId, score, level, token) {
  const res = await fetch(`${BASE_URL}/games/${gameId}/score`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ score, level }),
  });
  if (!res.ok) throw new Error('Failed to submit game score');
  return res.json();
}

export async function getGameLeaderboard(gameId, token) {
  const res = await fetch(`${BASE_URL}/games/${gameId}/leaderboard`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch game leaderboard');
  return res.json();
}

export async function getPlayerGameStats(token) {
  const res = await fetch(`${BASE_URL}/games/player/stats`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed to fetch player game stats');
  return res.json();
}

// Journal & Research Integration APIs
export async function getResearchData(token) {
  const res = await fetch(`${BASE_URL}/research/data`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch research data');
  return res.json();
}

export async function searchResearch(query, subject, token) {
  const params = { q: query };
  if (subject) params.subject = subject;
  const queryString = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE_URL}/research/search?${queryString}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Research search failed');
  return res.json();
}

export async function getJournalTemplate(templateType, token) {
  const res = await fetch(`${BASE_URL}/research/templates/${templateType}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch journal template');
  return res.json();
}

export async function getMethodologyGuide(guideType, token) {
  const res = await fetch(`${BASE_URL}/research/methodology/${guideType}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch methodology guide');
  return res.json();
}

export async function getCitationStyle(style, token) {
  const res = await fetch(`${BASE_URL}/research/citations/${style}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch citation style');
  return res.json();
}

export async function saveResearchJournal(journalData, token) {
  const res = await fetch(`${BASE_URL}/research/journals`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(journalData),
  });
  if (!res.ok) throw new Error('Failed to save research journal');
  return res.json();
}

// Localization & Cultural Adaptation APIs
export async function getCulturalContext(subject, token) {
  const res = await fetch(`${BASE_URL}/localization/context/${subject}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch cultural context');
  return res.json();
}

export async function checkContentSensitivity(content, subject, token) {
  const res = await fetch(`${BASE_URL}/localization/sensitivity-check`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ content, subject }),
  });
  if (!res.ok) throw new Error('Sensitivity check failed');
  return res.json();
}

export async function adaptContentForRegion(content, region, token) {
  const res = await fetch(`${BASE_URL}/localization/adapt`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ content, region }),
  });
  if (!res.ok) throw new Error('Content adaptation failed');
  return res.json();
}

export async function getLocalizedAssessment(subject, level, region, token) {
  const params = { subject, level, region };
  const queryString = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE_URL}/localization/assessment?${queryString}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch localized assessment');
  return res.json();
}

// ============================================================================
// AI ENHANCEMENT APIs
// ============================================================================

// Intelligent Tutoring APIs
export async function getPersonalizedLearningPath(userId, token) {
  const res = await fetch(`${BASE_URL}/ai/learning-path/${userId}`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed to fetch personalized learning path');
  return res.json();
}

export async function getAdaptiveRecommendations(userId, currentTopic, token) {
  const params = { current_topic: currentTopic };
  const queryString = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE_URL}/ai/recommendations/${userId}?${queryString}`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed to fetch adaptive recommendations');
  return res.json();
}

export async function analyzeLearningPattern(userId, timeRange, token) {
  const params = { time_range: timeRange };
  const queryString = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE_URL}/ai/patterns/${userId}?${queryString}`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed to analyze learning patterns');
  return res.json();
}

export async function getIntelligentHints(topicId, userLevel, token) {
  const params = { user_level: userLevel };
  const queryString = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE_URL}/ai/hints/${topicId}?${queryString}`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed to fetch intelligent hints');
  return res.json();
}

export async function predictPerformance(userId, subject, token) {
  const params = { subject };
  const queryString = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE_URL}/ai/predict/${userId}?${queryString}`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed to predict performance');
  return res.json();
}
