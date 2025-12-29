// Akulearn Connected App API Service
const BASE_URL = 'http://localhost:8000/api'; // Update this for production
const WAVE3_BASE_URL = 'http://localhost:8000/api/v3'; // Wave 3 API

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

// ============================================================================
// WAVE 3 ADVANCED APIs
// ============================================================================

// Wave 3 Health & Features
export async function getWave3Health() {
  const res = await fetch(`${WAVE3_BASE_URL}/health`);
  if (!res.ok) throw new Error('Wave 3 health check failed');
  return res.json();
}

export async function getWave3Features() {
  const res = await fetch(`${WAVE3_BASE_URL}/features`);
  if (!res.ok) throw new Error('Failed to fetch Wave 3 features');
  return res.json();
}

// Wave 3 Lessons
export async function getWave3Lessons(subject = null, grade = null, token = null) {
  const params = new URLSearchParams();
  if (subject) params.append('subject', subject);
  if (grade) params.append('grade', grade);
  
  const res = await fetch(`${WAVE3_BASE_URL}/lessons?${params.toString()}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch Wave 3 lessons');
  return res.json();
}

export async function getWave3Lesson(lessonId, token = null) {
  const res = await fetch(`${WAVE3_BASE_URL}/lessons/${lessonId}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch Wave 3 lesson');
  return res.json();
}

export async function searchWave3Lessons(query, searchType = 'keyword', token = null) {
  const res = await fetch(`${WAVE3_BASE_URL}/lessons/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    },
    body: JSON.stringify({ query, search_type: searchType }),
  });
  if (!res.ok) throw new Error('Wave 3 lesson search failed');
  return res.json();
}

// Wave 3 Recommendations
export async function getWave3Recommendations(studentId, method = 'hybrid', limit = 5, token = null) {
  const params = new URLSearchParams({ method, limit: limit.toString() });
  const res = await fetch(`${WAVE3_BASE_URL}/recommendations/${studentId}?${params.toString()}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch Wave 3 recommendations');
  return res.json();
}

export async function recordWave3Interaction(studentId, lessonId, interactionType, metadata = {}, token = null) {
  const res = await fetch(`${WAVE3_BASE_URL}/recommendations/interaction`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    },
    body: JSON.stringify({
      student_id: studentId,
      lesson_id: lessonId,
      interaction_type: interactionType,
      metadata
    }),
  });
  if (!res.ok) throw new Error('Failed to record Wave 3 interaction');
  return res.json();
}

// Wave 3 Gamification
export async function getWave3StudentStats(studentId, token = null) {
  const res = await fetch(`${WAVE3_BASE_URL}/gamification/stats/${studentId}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch Wave 3 student stats');
  return res.json();
}

export async function getWave3Achievements(studentId = null, token = null) {
  const url = studentId 
    ? `${WAVE3_BASE_URL}/gamification/achievements/${studentId}`
    : `${WAVE3_BASE_URL}/gamification/achievements`;
  const res = await fetch(url, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch Wave 3 achievements');
  return res.json();
}

export async function getWave3Leaderboard(scope = 'global', limit = 10, token = null) {
  const params = new URLSearchParams({ scope, limit: limit.toString() });
  const res = await fetch(`${WAVE3_BASE_URL}/gamification/leaderboard?${params.toString()}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch Wave 3 leaderboard');
  return res.json();
}

export async function getWave3Streak(studentId, token = null) {
  const res = await fetch(`${WAVE3_BASE_URL}/gamification/streak/${studentId}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch Wave 3 streak');
  return res.json();
}

// Wave 3 Analytics
export async function predictWave3Mastery(studentId, lessonId, token = null) {
  const res = await fetch(`${WAVE3_BASE_URL}/analytics/predict-mastery/${studentId}/${lessonId}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to predict Wave 3 mastery');
  return res.json();
}

export async function getWave3StudyRecommendation(studentId, token = null) {
  const res = await fetch(`${WAVE3_BASE_URL}/analytics/study-recommendation/${studentId}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch Wave 3 study recommendation');
  return res.json();
}

export async function getWave3LearningVelocity(studentId, token = null) {
  const res = await fetch(`${WAVE3_BASE_URL}/analytics/learning-velocity/${studentId}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch Wave 3 learning velocity');
  return res.json();
}

export async function getWave3AtRiskStatus(studentId, token = null) {
  const res = await fetch(`${WAVE3_BASE_URL}/analytics/at-risk/${studentId}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch Wave 3 at-risk status');
  return res.json();
}

// Wave 3 Progress
export async function submitWave3Quiz(quizData, token = null) {
  const res = await fetch(`${WAVE3_BASE_URL}/progress/quiz`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    },
    body: JSON.stringify(quizData),
  });
  if (!res.ok) throw new Error('Failed to submit Wave 3 quiz');
  return res.json();
}

export async function recordWave3Activity(activityData, token = null) {
  const res = await fetch(`${WAVE3_BASE_URL}/progress/activity`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    },
    body: JSON.stringify(activityData),
  });
  if (!res.ok) throw new Error('Failed to record Wave 3 activity');
  return res.json();
}

export async function getWave3Mastery(studentId, lessonId, token = null) {
  const res = await fetch(`${WAVE3_BASE_URL}/progress/mastery/${studentId}/${lessonId}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch Wave 3 mastery');
  return res.json();
}

export async function getWave3Progress(studentId, token = null) {
  const res = await fetch(`${WAVE3_BASE_URL}/progress/${studentId}`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error('Failed to fetch Wave 3 progress');
  return res.json();
}

// WebSocket connection helper
export function createWave3WebSocket(studentId, onMessage, onError = null) {
  const ws = new WebSocket(`ws://localhost:8000/ws/${studentId}`);
  
  ws.onopen = () => {
    console.log('Wave 3 WebSocket connected');
  };
  
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (error) {
      console.error('WebSocket message parse error:', error);
    }
  };
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
    if (onError) onError(error);
  };
  
  ws.onclose = () => {
    console.log('Wave 3 WebSocket disconnected');
  };
  
  return ws;
}

// GraphQL query helper
export async function queryWave3GraphQL(query, variables = {}, token = null) {
  const res = await fetch(`http://localhost:8000/graphql`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    },
    body: JSON.stringify({ query, variables }),
  });
  if (!res.ok) throw new Error('GraphQL query failed');
  const result = await res.json();
  if (result.errors) throw new Error(result.errors[0].message);
  return result.data;
}
