# Wave 3 Advanced Features - Complete API Reference

## Table of Contents
1. [Quick Start](#quick-start)
2. [Authentication](#authentication)
3. [WebSocket API](#websocket-api)
4. [GraphQL API](#graphql-api)
5. [Recommendations API](#recommendations-api)
6. [Gamification API](#gamification-api)
7. [Analytics API](#analytics-api)
8. [Error Handling](#error-handling)
9. [Rate Limiting](#rate-limiting)
10. [Examples](#examples)

---

## Quick Start

### Base URL
```
http://localhost:8000
```

### Health Check
```http
GET /api/v3/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "3.0.0",
  "features": {
    "websocket": true,
    "graphql": true,
    "recommendations": true,
    "gamification": true,
    "analytics": true
  }
}
```

### API Documentation
- **OpenAPI/Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **GraphQL Playground**: http://localhost:8000/graphql

---

## Authentication

**Current Status**: No authentication required (development mode)

**Production**: Add JWT Bearer token authentication
```http
Authorization: Bearer <your_token_here>
```

---

## WebSocket API

### Connect to WebSocket

**Endpoint**: `ws://localhost:8000/ws/{student_id}`

**Parameters**:
- `student_id` (path): Student identifier

### Message Format

#### Client → Server

**Subscribe to Topics**:
```json
{
  "action": "subscribe",
  "topics": ["progress", "achievements", "mastery", "quizzes", "leaderboard"]
}
```

**Unsubscribe from Topics**:
```json
{
  "action": "unsubscribe",
  "topics": ["progress"]
}
```

**Ping** (keepalive):
```json
{
  "action": "ping"
}
```

#### Server → Client

**Progress Update**:
```json
{
  "type": "progress_update",
  "data": {
    "student_id": "student_001",
    "lesson_id": "physics_ss1_motion_l1",
    "progress_percentage": 75.5,
    "mastery_points": 12,
    "timestamp": "2024-12-28T10:30:00Z"
  }
}
```

**Achievement Unlocked**:
```json
{
  "type": "achievement",
  "data": {
    "achievement_id": "first_mastery",
    "title": "First Steps",
    "description": "Achieved first mastery level",
    "points": 50,
    "icon": "🏆",
    "timestamp": "2024-12-28T10:30:00Z"
  }
}
```

**Mastery Level Up**:
```json
{
  "type": "mastery_level_up",
  "data": {
    "student_id": "student_001",
    "lesson_id": "physics_ss1_motion_l1",
    "old_level": "developing",
    "new_level": "proficient",
    "timestamp": "2024-12-28T10:30:00Z"
  }
}
```

**Quiz Result**:
```json
{
  "type": "quiz_result",
  "data": {
    "student_id": "student_001",
    "quiz_id": "quiz_001",
    "score_percentage": 85,
    "passed": true,
    "timestamp": "2024-12-28T10:30:00Z"
  }
}
```

**Leaderboard Update**:
```json
{
  "type": "leaderboard_update",
  "data": {
    "student_id": "student_001",
    "new_rank": 15,
    "previous_rank": 18,
    "total_points": 1250,
    "timestamp": "2024-12-28T10:30:00Z"
  }
}
```

**Pong** (keepalive response):
```json
{
  "type": "pong",
  "timestamp": "2024-12-28T10:30:00Z"
}
```

### JavaScript Client Example

```javascript
const studentId = 'student_001';
const ws = new WebSocket(`ws://localhost:8000/ws/${studentId}`);

ws.onopen = () => {
  console.log('Connected to WebSocket');
  
  // Subscribe to topics
  ws.send(JSON.stringify({
    action: 'subscribe',
    topics: ['progress', 'achievements', 'mastery']
  }));
  
  // Send keepalive ping every 25 seconds
  setInterval(() => {
    ws.send(JSON.stringify({ action: 'ping' }));
  }, 25000);
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  switch(message.type) {
    case 'progress_update':
      updateProgressBar(message.data);
      break;
    case 'achievement':
      showAchievementNotification(message.data);
      break;
    case 'mastery_level_up':
      showLevelUpAnimation(message.data);
      break;
    case 'pong':
      console.log('Keepalive: Connection alive');
      break;
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('WebSocket disconnected. Reconnecting...');
  setTimeout(() => location.reload(), 3000);
};
```

---

## GraphQL API

### Endpoint
```
POST /graphql
GET /graphql (GraphQL Playground)
```

### Available Queries

#### Get Lesson
```graphql
query GetLesson($lessonId: String!) {
  lesson(lessonId: $lessonId) {
    id
    title
    subject
    gradeLevel
    introduction
    learningObjectives {
      objective
      bloomLevel
    }
    contentSections {
      title
      content
      subsections
    }
    workedExamples {
      title
      problem
      solution
      explanation
    }
    practiceProblem {
      problem
      difficulty
      hints
    }
    glossary {
      term
      definition
    }
    prerequisites
    connections
  }
}
```

**Variables**:
```json
{
  "lessonId": "physics_ss1_motion_l1"
}
```

#### Get Student Progress
```graphql
query GetStudentProgress($studentId: String!) {
  studentProgress(studentId: $studentId) {
    studentId
    totalLessons
    completedLessons
    inProgressLessons
    averageMastery
    totalTimeHours
    totalQuizzesTaken
    achievementsCount
  }
}
```

#### Get Recommendations
```graphql
query GetRecommendations($studentId: String!, $count: Int) {
  recommendations(studentId: $studentId, count: $count) {
    lessonId
    title
    subject
    score
    reason
  }
}
```

#### Search Lessons
```graphql
query SearchLessons($keyword: String!) {
  searchLessons(keyword: $keyword) {
    id
    title
    subject
    introduction
  }
}
```

#### Get Leaderboard
```graphql
query GetLeaderboard($limit: Int) {
  leaderboard(limit: $limit) {
    rank
    studentId
    studentName
    totalPoints
    achievementsCount
    masteryAverage
  }
}
```

### cURL Example
```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ lesson(lessonId: \"physics_ss1_motion_l1\") { title subject } }"}'
```

---

## Recommendations API

### Get Recommendations

```http
GET /api/v3/recommendations/{student_id}?count=5&method=hybrid
```

**Parameters**:
- `student_id` (path, required): Student identifier
- `count` (query, optional): Number of recommendations (default: 5, max: 50)
- `method` (query, optional): Recommendation algorithm
  - `content`: Content-based filtering
  - `collaborative`: Collaborative filtering
  - `hybrid`: Combined approach (default)
  - `prerequisite`: Prerequisite-aware recommendations

**Response**:
```json
{
  "student_id": "student_001",
  "method": "hybrid",
  "count": 5,
  "recommendations": [
    {
      "lesson_id": "physics_ss1_forces_l1",
      "title": "Introduction to Forces",
      "subject": "physics",
      "grade_level": "SS1",
      "score": 0.87,
      "reason": "Strong topic overlap with completed lessons and high ratings from similar students",
      "estimated_duration": 45,
      "difficulty": "intermediate"
    }
  ]
}
```

### Record Interaction Feedback

```http
POST /api/v3/recommendations/feedback
Content-Type: application/json
```

**Request Body**:
```json
{
  "student_id": "student_001",
  "lesson_id": "physics_ss1_forces_l1",
  "interaction_score": 0.9
}
```

**Interaction Score**: 0.0 (ignored) to 1.0 (completed with high engagement)

**Response**:
```json
{
  "status": "recorded",
  "student_id": "student_001",
  "lesson_id": "physics_ss1_forces_l1"
}
```

### Examples

**Python**:
```python
import requests

# Get recommendations
response = requests.get(
    'http://localhost:8000/api/v3/recommendations/student_001',
    params={'count': 10, 'method': 'hybrid'}
)
recommendations = response.json()

# Record interaction
requests.post(
    'http://localhost:8000/api/v3/recommendations/feedback',
    json={
        'student_id': 'student_001',
        'lesson_id': 'physics_ss1_forces_l1',
        'interaction_score': 0.85
    }
)
```

**JavaScript**:
```javascript
// Get recommendations
const response = await fetch(
  'http://localhost:8000/api/v3/recommendations/student_001?count=5&method=hybrid'
);
const data = await response.json();

// Record interaction
await fetch('http://localhost:8000/api/v3/recommendations/feedback', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    student_id: 'student_001',
    lesson_id: 'physics_ss1_forces_l1',
    interaction_score: 0.85
  })
});
```

---

## Gamification API

### Get Student Achievements

```http
GET /api/v3/gamification/achievements/{student_id}
```

**Response**:
```json
{
  "student_id": "student_001",
  "total_achievements": 12,
  "total_points": 1250,
  "badge_level": "gold",
  "achievements": [
    {
      "achievement_id": "first_mastery",
      "title": "First Steps",
      "description": "Achieved first mastery level",
      "category": "mastery",
      "points": 50,
      "icon": "🏆",
      "unlocked_at": "2024-12-20T14:30:00Z",
      "progress": 100
    },
    {
      "achievement_id": "week_warrior",
      "title": "Week Warrior",
      "description": "Maintained a 7-day learning streak",
      "category": "streak",
      "points": 100,
      "icon": "🔥",
      "unlocked_at": "2024-12-27T09:00:00Z",
      "progress": 100
    }
  ],
  "achievements_available": 12,
  "achievements_earned": 5
}
```

### Check and Award Achievements

```http
POST /api/v3/gamification/check-achievements
Content-Type: application/json
```

**Request Body**:
```json
{
  "student_id": "student_001",
  "student_stats": {
    "mastery_levels": {
      "physics": "proficient",
      "chemistry": "developing"
    },
    "streak_days": 7,
    "subjects_explored": ["physics", "chemistry", "biology"],
    "problems_solved": 105,
    "high_quiz_scores": 8,
    "late_night_sessions": 5,
    "early_morning_sessions": 12
  }
}
```

**Response**:
```json
{
  "student_id": "student_001",
  "newly_earned": 2,
  "achievements": [
    {
      "id": "week_warrior",
      "title": "Week Warrior",
      "points": 100,
      "icon": "🔥"
    },
    {
      "id": "century_club",
      "title": "Century Club",
      "points": 200,
      "icon": "💯"
    }
  ]
}
```

### Get Leaderboard

```http
GET /api/v3/gamification/leaderboard?limit=10&timeframe=week
```

**Parameters**:
- `limit` (optional): Number of entries (default: 10, max: 100)
- `timeframe` (optional): Time period - `day`, `week`, `month`, `all_time` (default)

**Response**:
```json
{
  "timeframe": "week",
  "limit": 10,
  "entries": [
    {
      "rank": 1,
      "student_id": "student_042",
      "student_name": "Ada Lovelace",
      "total_points": 2150,
      "achievements_count": 8,
      "badge_level": "platinum",
      "current_streak": 15
    }
  ]
}
```

### Get/Update Streak

**Get Streak**:
```http
GET /api/v3/gamification/streak/{student_id}
```

**Response**:
```json
{
  "student_id": "student_001",
  "current_streak": 7,
  "longest_streak": 15,
  "last_activity": "2024-12-28"
}
```

**Update Streak**:
```http
POST /api/v3/gamification/streak/{student_id}
Content-Type: application/json
```

**Request Body**:
```json
{
  "activity_date": "2024-12-28"
}
```

**Response**:
```json
{
  "student_id": "student_001",
  "current_streak": 8,
  "status": "updated"
}
```

---

## Analytics API

### Predict Mastery Level

```http
POST /api/v3/analytics/predict-mastery
Content-Type: application/json
```

**Request Body**:
```json
{
  "student_id": "student_001",
  "lesson_id": "physics_ss1_motion_l1",
  "current_metrics": {
    "quiz_scores": [75, 80, 85],
    "problems_completed": [0.7, 0.8, 0.85],
    "time_spent_minutes": [30, 35, 40],
    "engagement_score": 0.82
  }
}
```

**Response**:
```json
{
  "student_id": "student_001",
  "lesson_id": "physics_ss1_motion_l1",
  "predicted_level": "proficient",
  "confidence": 0.87,
  "estimated_hours": 3.2,
  "recommendations": [
    "Continue with practice problems to solidify understanding",
    "Review worked examples for complex scenarios",
    "Take the summative assessment when ready"
  ]
}
```

### Identify At-Risk Students

```http
POST /api/v3/analytics/at-risk
Content-Type: application/json
```

**Request Body**:
```json
{
  "grade_level": "SS1",
  "subject": "physics",
  "student_data": {
    "student_001": {
      "mastery_average": 0.28,
      "recent_trend": "declining",
      "engagement_time": 15,
      "completion_rate": 0.35,
      "streak_status": "broken",
      "struggling_topics": ["forces", "motion"]
    }
  }
}
```

**Response**:
```json
{
  "total_at_risk": 3,
  "high_risk": 1,
  "medium_risk": 2,
  "students": [
    {
      "student_id": "student_001",
      "risk_level": "high",
      "risk_score": 8.5,
      "risk_factors": [
        "Low mastery level (28%)",
        "Declining trend in last 7 days",
        "Low engagement time (15 min/week)",
        "Poor completion rate (35%)",
        "Broken study streak"
      ],
      "interventions": [
        "Schedule immediate 1-on-1 tutoring session",
        "Assign foundational review lessons",
        "Provide additional practice problems with hints",
        "Set up daily check-ins for motivation"
      ],
      "affected_subjects": ["physics"]
    }
  ]
}
```

### Get Optimal Study Time

```http
POST /api/v3/analytics/optimal-study-time
Content-Type: application/json
```

**Request Body**:
```json
{
  "student_id": "student_001",
  "activity_history": [
    {"time_of_day": "morning", "performance": 0.88, "duration": 45},
    {"time_of_day": "afternoon", "performance": 0.72, "duration": 30},
    {"time_of_day": "evening", "performance": 0.65, "duration": 60},
    {"time_of_day": "morning", "performance": 0.90, "duration": 50}
  ]
}
```

**Response**:
```json
{
  "student_id": "student_001",
  "recommended_time": "morning",
  "duration_minutes": 45,
  "break_pattern": "pomodoro",
  "reasoning": "Your performance is 25% higher in morning sessions (7-11 AM). Optimal duration is 45 minutes with 5-minute breaks every 25 minutes (Pomodoro technique)."
}
```

### Analyze Learning Velocity

```http
POST /api/v3/analytics/learning-velocity
Content-Type: application/json
```

**Request Body**:
```json
{
  "student_id": "student_001",
  "progress_history": [
    {"date": "2024-12-20", "mastery_points": 10},
    {"date": "2024-12-21", "mastery_points": 15},
    {"date": "2024-12-22", "mastery_points": 25},
    {"date": "2024-12-23", "mastery_points": 40}
  ]
}
```

**Response**:
```json
{
  "student_id": "student_001",
  "mastery_points_per_day": 12.5,
  "trend": "accelerating",
  "velocity_change": "+45%",
  "days_to_complete_remaining": 32,
  "insights": "Learning pace has increased significantly in recent days. Maintain current study habits for optimal progress."
}
```

---

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid student_id format",
    "details": {
      "field": "student_id",
      "constraint": "Must be alphanumeric"
    },
    "timestamp": "2024-12-28T10:30:00Z"
  }
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Feature temporarily disabled |

---

## Rate Limiting

### Current Limits

| Endpoint Type | Rate Limit | Burst Limit |
|---------------|-----------|-------------|
| REST API | 100 req/min | 200 |
| GraphQL | 50 req/min | 100 |
| WebSocket Messages | 10 msg/sec | 50 |
| Analytics | 20 req/min | 30 |

### Rate Limit Headers

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1703761200
```

### Rate Limit Exceeded Response

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again in 45 seconds.",
    "retry_after": 45,
    "timestamp": "2024-12-28T10:30:00Z"
  }
}
```

---

## Examples

### Complete React Integration

```jsx
import React, { useEffect, useState } from 'react';
import { ApolloClient, InMemoryCache, useQuery, gql } from '@apollo/client';

// Apollo Client setup
const client = new ApolloClient({
  uri: 'http://localhost:8000/graphql',
  cache: new InMemoryCache()
});

// GraphQL Query
const GET_RECOMMENDATIONS = gql`
  query GetRecommendations($studentId: String!) {
    recommendations(studentId: $studentId, count: 5) {
      lessonId
      title
      subject
      score
      reason
    }
  }
`;

function StudentDashboard({ studentId }) {
  const [ws, setWs] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const { data, loading } = useQuery(GET_RECOMMENDATIONS, {
    variables: { studentId },
    client
  });

  // WebSocket connection
  useEffect(() => {
    const websocket = new WebSocket(`ws://localhost:8000/ws/${studentId}`);
    
    websocket.onopen = () => {
      websocket.send(JSON.stringify({
        action: 'subscribe',
        topics: ['achievements', 'progress', 'mastery']
      }));
    };

    websocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setNotifications(prev => [message, ...prev].slice(0, 10));
    };

    setWs(websocket);
    return () => websocket.close();
  }, [studentId]);

  return (
    <div className="dashboard">
      <h2>Your Recommendations</h2>
      {loading ? <p>Loading...</p> : (
        <ul>
          {data.recommendations.map(rec => (
            <li key={rec.lessonId}>
              <strong>{rec.title}</strong>
              <p>Score: {rec.score.toFixed(2)}</p>
              <p>{rec.reason}</p>
            </li>
          ))}
        </ul>
      )}
      
      <h2>Live Notifications</h2>
      <ul>
        {notifications.map((notif, i) => (
          <li key={i}>
            {notif.type}: {JSON.stringify(notif.data)}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Python Complete Example

```python
import requests
import asyncio
import websockets
import json
from datetime import datetime

class Wave3Client:
    def __init__(self, base_url="http://localhost:8000", student_id=None):
        self.base_url = base_url
        self.student_id = student_id
    
    # Recommendations
    def get_recommendations(self, method="hybrid", count=5):
        response = requests.get(
            f"{self.base_url}/api/v3/recommendations/{self.student_id}",
            params={"method": method, "count": count}
        )
        return response.json()
    
    def record_interaction(self, lesson_id, score):
        response = requests.post(
            f"{self.base_url}/api/v3/recommendations/feedback",
            json={
                "student_id": self.student_id,
                "lesson_id": lesson_id,
                "interaction_score": score
            }
        )
        return response.json()
    
    # Gamification
    def get_achievements(self):
        response = requests.get(
            f"{self.base_url}/api/v3/gamification/achievements/{self.student_id}"
        )
        return response.json()
    
    def get_leaderboard(self, limit=10):
        response = requests.get(
            f"{self.base_url}/api/v3/gamification/leaderboard",
            params={"limit": limit}
        )
        return response.json()
    
    # Analytics
    def predict_mastery(self, lesson_id, metrics):
        response = requests.post(
            f"{self.base_url}/api/v3/analytics/predict-mastery",
            json={
                "student_id": self.student_id,
                "lesson_id": lesson_id,
                "current_metrics": metrics
            }
        )
        return response.json()
    
    # WebSocket
    async def listen_websocket(self, topics=None):
        if topics is None:
            topics = ["progress", "achievements", "mastery"]
        
        uri = f"ws://localhost:8000/ws/{self.student_id}"
        async with websockets.connect(uri) as websocket:
            # Subscribe
            await websocket.send(json.dumps({
                "action": "subscribe",
                "topics": topics
            }))
            
            # Listen
            async for message in websocket:
                data = json.loads(message)
                print(f"[{datetime.now()}] {data['type']}: {data.get('data', {})}")

# Usage
if __name__ == "__main__":
    client = Wave3Client(student_id="student_001")
    
    # Get recommendations
    recs = client.get_recommendations(method="hybrid", count=5)
    print("Recommendations:", recs)
    
    # Get achievements
    achievements = client.get_achievements()
    print("Achievements:", achievements)
    
    # Get leaderboard
    leaderboard = client.get_leaderboard(limit=10)
    print("Leaderboard:", leaderboard)
    
    # WebSocket (run in async context)
    # asyncio.run(client.listen_websocket())
```

---

## Support & Resources

- **GitHub Repository**: https://github.com/oumar-code/Akulearn_docs
- **Branch**: docs-copilot-refactor
- **OpenAPI Spec**: http://localhost:8000/openapi.json
- **Interactive Docs**: http://localhost:8000/docs

**Version**: 3.0.0  
**Last Updated**: December 28, 2025
