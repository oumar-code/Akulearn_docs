# Wave 3 Frontend Integration Guide

## Overview

This document provides complete guidance for integrating the Wave 3 Advanced Features backend with the React Native frontend.

**Integration Date:** December 29, 2025  
**Backend Status:** ✅ Complete and Running  
**Frontend Status:** ✅ Ready for Integration  
**API Base URL:** `http://localhost:8000/api/v3`

---

## Table of Contents

1. [Backend API Endpoints](#backend-api-endpoints)
2. [Frontend API Service](#frontend-api-service)
3. [New Screens Created](#new-screens-created)
4. [Navigation Setup](#navigation-setup)
5. [Authentication Integration](#authentication-integration)
6. [WebSocket Integration](#websocket-integration)
7. [GraphQL Integration](#graphql-integration)
8. [Testing Checklist](#testing-checklist)
9. [Deployment Notes](#deployment-notes)

---

## Backend API Endpoints

### Wave 3 Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v3/health` | GET | Health check and feature status |
| `/api/v3/features` | GET | List of enabled features |
| `/api/v3/lessons` | GET | Get all lessons (filterable) |
| `/api/v3/lessons/{id}` | GET | Get lesson details |
| `/api/v3/lessons/search` | POST | Search lessons |

### Recommendations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v3/recommendations/{student_id}` | GET | Get personalized recommendations |
| `/api/v3/recommendations/interaction` | POST | Record student interaction |

### Gamification

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v3/gamification/stats/{student_id}` | GET | Student stats (points, level, streak) |
| `/api/v3/gamification/achievements` | GET | List all achievements |
| `/api/v3/gamification/achievements/{student_id}` | GET | Student achievements |
| `/api/v3/gamification/leaderboard` | GET | Global/school/class leaderboard |
| `/api/v3/gamification/streak/{student_id}` | GET | Student streak information |

### Analytics

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v3/analytics/predict-mastery/{student_id}/{lesson_id}` | GET | Predict mastery level |
| `/api/v3/analytics/study-recommendation/{student_id}` | GET | Optimal study time |
| `/api/v3/analytics/learning-velocity/{student_id}` | GET | Learning velocity analysis |
| `/api/v3/analytics/at-risk/{student_id}` | GET | At-risk status |

### Progress Tracking

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v3/progress/quiz` | POST | Submit quiz results |
| `/api/v3/progress/activity` | POST | Record learning activity |
| `/api/v3/progress/mastery/{student_id}/{lesson_id}` | GET | Get mastery metrics |
| `/api/v3/progress/{student_id}` | GET | Get student progress |

### WebSocket

| Endpoint | Protocol | Description |
|----------|----------|-------------|
| `/ws/{student_id}` | WebSocket | Real-time updates |

### GraphQL

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/graphql` | POST | GraphQL queries |

---

## Frontend API Service

### File: `connected_stack/frontend/api.js`

**Status:** ✅ Updated with Wave 3 functions

### Key Functions Added

#### Health & Features
```javascript
getWave3Health() // Check backend health
getWave3Features() // Get enabled features
```

#### Lessons
```javascript
getWave3Lessons(subject, grade, token) // List lessons
getWave3Lesson(lessonId, token) // Get lesson details
searchWave3Lessons(query, searchType, token) // Search lessons
```

#### Recommendations
```javascript
getWave3Recommendations(studentId, method, limit, token)
recordWave3Interaction(studentId, lessonId, interactionType, metadata, token)
```

#### Gamification
```javascript
getWave3StudentStats(studentId, token)
getWave3Achievements(studentId, token)
getWave3Leaderboard(scope, limit, token)
getWave3Streak(studentId, token)
```

#### Analytics
```javascript
predictWave3Mastery(studentId, lessonId, token)
getWave3StudyRecommendation(studentId, token)
getWave3LearningVelocity(studentId, token)
getWave3AtRiskStatus(studentId, token)
```

#### Progress
```javascript
submitWave3Quiz(quizData, token)
recordWave3Activity(activityData, token)
getWave3Mastery(studentId, lessonId, token)
getWave3Progress(studentId, token)
```

#### WebSocket Helper
```javascript
createWave3WebSocket(studentId, onMessage, onError)
```

#### GraphQL Helper
```javascript
queryWave3GraphQL(query, variables, token)
```

---

## New Screens Created

### 1. Wave3SearchScreen.js
**Location:** `connected_stack/frontend/screens/Wave3SearchScreen.js`

**Features:**
- Search by keyword, NERDC code, or WAEC topic
- Personalized recommendations display
- Interactive lesson cards
- Match score visualization
- Interaction tracking

**Usage:**
```javascript
navigation.navigate('Wave3Search');
```

### 2. Wave3QuizScreen.js
**Location:** `connected_stack/frontend/screens/Wave3QuizScreen.js`

**Features:**
- Progress bar tracking
- Student stats header (points, level, streak)
- Multiple choice questions
- Timed quiz submission
- Results modal with achievements
- Points earned display
- Real-time mastery updates via WebSocket

**Usage:**
```javascript
navigation.navigate('Wave3Quiz', { lessonId: 'lesson_123' });
```

### 3. Wave3LessonScreen.js
**Location:** `connected_stack/frontend/screens/Wave3LessonScreen.js`

**Features:**
- Lesson overview with NERDC codes
- Content sections with tabs
- Worked examples
- Practice problems preview
- Mastery progress bar
- WebSocket real-time updates
- Automatic activity tracking

**Usage:**
```javascript
navigation.navigate('Wave3Lesson', { lessonId: 'lesson_123' });
```

---

## Navigation Setup

### Update App.js

Add the new screens to your navigation stack:

```javascript
// Import new screens
import Wave3SearchScreen from './screens/Wave3SearchScreen';
import Wave3QuizScreen from './screens/Wave3QuizScreen';
import Wave3LessonScreen from './screens/Wave3LessonScreen';

// Add to Stack Navigator
<Stack.Screen
  name="Wave3Search"
  component={Wave3SearchScreen}
  options={{ title: 'Search Lessons' }}
/>
<Stack.Screen
  name="Wave3Lesson"
  component={Wave3LessonScreen}
  options={{ title: 'Lesson' }}
/>
<Stack.Screen
  name="Wave3Quiz"
  component={Wave3QuizScreen}
  options={{ title: 'Quiz' }}
/>
```

### Tab Navigator Update (Optional)

Replace existing SearchScreen with Wave3SearchScreen in bottom tabs:

```javascript
<Tab.Screen
  name="Search"
  component={Wave3SearchScreen}
  options={{
    tabBarLabel: 'Search',
    tabBarIcon: ({ color, size }) => (
      <Icon name="search" color={color} size={size} />
    ),
  }}
/>
```

---

## Authentication Integration

### Student ID Handling

The Wave 3 API uses `student_id` for personalization. Update your UserContext:

```javascript
// UserContext.js
const [user, setUser] = useState({
  id: null, // <- Ensure this is set after login
  email: null,
  token: null,
});

// After successful login
const login = async (userData, token) => {
  setUser({
    id: userData.user_id || userData.id, // <- Map to student_id
    email: userData.email,
    token: token,
  });
  await AsyncStorage.setItem('user', JSON.stringify(userData));
  await AsyncStorage.setItem('token', token);
};
```

### Token Management

All Wave 3 API functions accept an optional `token` parameter:

```javascript
// With authentication
const lessons = await getWave3Lessons('Mathematics', 'SS1', user.token);

// Without authentication (public access)
const lessons = await getWave3Lessons('Mathematics', 'SS1');
```

---

## WebSocket Integration

### Setup in Component

```javascript
import { createWave3WebSocket } from '../api';

useEffect(() => {
  const studentId = user?.id || 'student_001';
  const ws = createWave3WebSocket(
    studentId,
    (data) => {
      // Handle incoming messages
      if (data.type === 'mastery_update') {
        updateMastery(data.mastery_data);
      }
      if (data.type === 'achievement_unlocked') {
        showAchievementNotification(data.achievement);
      }
    },
    (error) => {
      console.error('WebSocket error:', error);
    }
  );

  return () => ws.close();
}, [user]);
```

### Message Types

The backend sends these WebSocket message types:

```javascript
{
  type: 'connection_established',
  student_id: 'student_001',
  timestamp: '2025-12-29T10:00:00Z'
}

{
  type: 'mastery_update',
  lesson_id: 'lesson_123',
  mastery_data: { mastery_level: 'proficient', mastery_percentage: 75 }
}

{
  type: 'achievement_unlocked',
  achievement: { id: 'ach_001', name: 'Quick Learner', ... }
}

{
  type: 'progress_update',
  lesson_id: 'lesson_123',
  progress: { completed: true, score: 85 }
}

{
  type: 'leaderboard_update',
  leaderboard: [...]
}
```

---

## GraphQL Integration

### Example Queries

#### Get Lesson with Progress
```javascript
import { queryWave3GraphQL } from '../api';

const query = `
  query GetLesson($lessonId: String!) {
    lesson(lessonId: $lessonId) {
      id
      title
      subject
      description
      learningObjectives
      contentSections {
        title
        content
      }
      workedExamples {
        problem
        solution
        explanation
      }
    }
  }
`;

const data = await queryWave3GraphQL(query, { lessonId: 'lesson_123' }, user.token);
const lesson = data.lesson;
```

#### Get Student Progress
```javascript
const query = `
  query GetStudentProgress($studentId: String!) {
    studentProgress(studentId: $studentId) {
      lessonsCompleted
      totalLessons
      averageMastery
      recentActivities {
        lessonId
        activityType
        timestamp
      }
    }
  }
`;

const data = await queryWave3GraphQL(query, { studentId: user.id }, user.token);
const progress = data.studentProgress;
```

#### Search Lessons
```javascript
const query = `
  query SearchLessons($searchTerm: String!, $subject: String) {
    searchLessons(searchTerm: $searchTerm, subject: $subject) {
      id
      title
      subject
      difficultyLevel
      nerdcCodes
    }
  }
`;

const data = await queryWave3GraphQL(
  query,
  { searchTerm: 'quadratic', subject: 'Mathematics' },
  user.token
);
const lessons = data.searchLessons;
```

---

## Testing Checklist

### Backend Testing

- [x] ✅ Server running on `http://localhost:8000`
- [x] ✅ Health endpoint responding: `/api/v3/health`
- [x] ✅ Features enabled: WebSocket, GraphQL, Recommendations, Gamification, Analytics
- [x] ✅ API documentation available: `/docs`
- [x] ✅ GraphQL playground available: `/graphql`

### Frontend Testing

#### 1. API Service Tests
```bash
# Test API connectivity
curl http://localhost:8000/api/v3/health
curl http://localhost:8000/api/v3/features
```

#### 2. Screen Navigation Tests
- [ ] Navigate to Wave3SearchScreen
- [ ] Search for lessons by keyword
- [ ] View lesson details
- [ ] Start quiz from lesson
- [ ] Complete quiz and see results

#### 3. Feature Tests

**Search:**
- [ ] Keyword search works
- [ ] NERDC code search works
- [ ] WAEC topic search works
- [ ] Recommendations load correctly
- [ ] Match scores display correctly

**Lesson:**
- [ ] Lesson details load
- [ ] Tabs switch correctly (Overview, Content, Examples, Practice)
- [ ] Mastery progress displays
- [ ] WebSocket updates work
- [ ] Activity tracking works

**Quiz:**
- [ ] Questions load correctly
- [ ] Answer selection works
- [ ] Navigation between questions works
- [ ] Submit button enables when all answered
- [ ] Results modal shows correctly
- [ ] Achievements display
- [ ] Points earned shows

**Gamification:**
- [ ] Student stats load (points, level, streak)
- [ ] Achievements unlock correctly
- [ ] Leaderboard displays
- [ ] Streaks track daily activity

**Analytics:**
- [ ] Mastery prediction works
- [ ] Study recommendations accurate
- [ ] Learning velocity calculates
- [ ] At-risk detection works

---

## Deployment Notes

### Environment Variables

Create `.env` file:

```bash
# Backend URL
WAVE3_API_URL=http://localhost:8000/api/v3
WAVE3_WS_URL=ws://localhost:8000/ws
WAVE3_GRAPHQL_URL=http://localhost:8000/graphql

# For production
WAVE3_API_URL=https://api.akulearn.com/api/v3
WAVE3_WS_URL=wss://api.akulearn.com/ws
WAVE3_GRAPHQL_URL=https://api.akulearn.com/graphql
```

### Update API Service

```javascript
// api.js
const WAVE3_BASE_URL = process.env.WAVE3_API_URL || 'http://localhost:8000/api/v3';
const WS_BASE_URL = process.env.WAVE3_WS_URL || 'ws://localhost:8000/ws';
const GRAPHQL_URL = process.env.WAVE3_GRAPHQL_URL || 'http://localhost:8000/graphql';
```

### Build Configuration

#### iOS
```bash
cd ios
pod install
cd ..
npx react-native run-ios
```

#### Android
```bash
npx react-native run-android
```

### Production Checklist

- [ ] Update API URLs to production
- [ ] Enable HTTPS/WSS
- [ ] Configure CORS for production domain
- [ ] Set up SSL certificates
- [ ] Enable authentication
- [ ] Set up monitoring
- [ ] Configure rate limiting
- [ ] Set up error tracking
- [ ] Test on physical devices
- [ ] Optimize bundle size

---

## Implementation Steps Summary

### ✅ Completed

1. **Backend Implementation**
   - Wave 3 Advanced Features (5 major features)
   - REST API endpoints
   - WebSocket real-time updates
   - GraphQL API
   - Recommendations engine
   - Gamification system
   - Advanced analytics

2. **Frontend API Integration**
   - Updated `api.js` with 20+ Wave 3 functions
   - WebSocket helper
   - GraphQL helper

3. **New Screens**
   - Wave3SearchScreen (search + recommendations)
   - Wave3QuizScreen (gamified quiz taking)
   - Wave3LessonScreen (lesson details + mastery)

4. **Documentation**
   - Complete API reference (WAVE3_API_REFERENCE.md)
   - Comprehensive test suite (test_wave3_advanced.py)
   - This integration guide

### 🔄 Next Steps

1. **App.js Updates**
   - Add new screen imports
   - Configure navigation routes
   - Update tab navigator

2. **UserContext Updates**
   - Ensure student ID mapping
   - Handle WebSocket connections
   - Manage authentication state

3. **Testing**
   - Test all new screens
   - Verify API connectivity
   - Test WebSocket updates
   - Validate gamification features

4. **UI/UX Polish**
   - Add loading states
   - Improve error handling
   - Add animations
   - Optimize performance

---

## Troubleshooting

### Common Issues

#### 1. Cannot connect to backend
**Solution:** Ensure server is running:
```bash
cd C:\Users\hp\Documents\Akulearn_docs
.\myenv\Scripts\python.exe -m uvicorn wave3_advanced_platform:app --host 0.0.0.0 --port 8000
```

#### 2. WebSocket connection fails
**Solution:** Check WebSocket URL and ensure student ID is valid:
```javascript
const ws = createWave3WebSocket(user.id || 'student_001', handleMessage);
```

#### 3. GraphQL queries fail
**Solution:** Verify query syntax and check backend logs:
```javascript
const data = await queryWave3GraphQL(query, variables, user.token);
console.log(data); // Check response
```

#### 4. Recommendations not loading
**Solution:** Ensure interactions are being recorded:
```javascript
await recordWave3Interaction(studentId, lessonId, 'view', {}, token);
```

---

## Support & Resources

- **API Documentation:** http://localhost:8000/docs
- **GraphQL Playground:** http://localhost:8000/graphql
- **Backend Code:** `wave3_advanced_platform.py` and related modules
- **Test Suite:** `test_wave3_advanced.py`
- **API Reference:** `WAVE3_API_REFERENCE.md`

---

## Conclusion

The Wave 3 frontend integration provides:
- ✅ Complete API connectivity
- ✅ 3 new feature-rich screens
- ✅ Real-time WebSocket updates
- ✅ GraphQL flexible querying
- ✅ Gamification integration
- ✅ Advanced analytics
- ✅ Personalized recommendations

**Status:** Ready for integration and testing!

**Last Updated:** December 29, 2025
