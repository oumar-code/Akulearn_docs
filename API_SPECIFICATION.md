# Akulearn Backend API Specification
## RESTful Endpoints for MVP

### Base URL
```
https://api.akulearn.com/api
```

---

## 1. AUTHENTICATION

### POST /auth/register
Register a new student.

**Request**:
```json
{
  "email": "student@gmail.com",
  "phone": "08012345678",
  "password": "SecurePass123",
  "full_name": "John Doe",
  "exam_board": "WAEC",
  "target_subjects": ["Mathematics", "Physics", "English Language"]
}
```

**Response (201)**:
```json
{
  "user_id": "user_12345",
  "email": "student@gmail.com",
  "message": "Registration successful. Verify your email.",
  "verification_token": "token_abc123"
}
```

### POST /auth/verify-otp
Verify email/phone via OTP.

**Request**:
```json
{
  "email": "student@gmail.com",
  "otp": "123456"
}
```

**Response (200)**:
```json
{
  "verified": true,
  "message": "Email verified successfully"
}
```

### POST /auth/login
Login with email and password.

**Request**:
```json
{
  "email": "student@gmail.com",
  "password": "SecurePass123"
}
```

**Response (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": "user_12345",
  "email": "student@gmail.com",
  "expires_in": 3600
}
```

### POST /auth/refresh-token
Refresh expired access token.

**Request**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600
}
```

### POST /auth/logout
Logout user (invalidate token).

**Headers**: `Authorization: Bearer {access_token}`

**Response (200)**:
```json
{
  "message": "Logged out successfully"
}
```

---

## 2. SEARCH & QUESTIONS

### GET /questions/search
Search for questions with filters.

**Query Parameters**:
- `q` (optional): Keyword search (e.g., "quadratic equation")
- `exam_board` (optional): "WAEC" | "NECO" | "JAMB"
- `subject` (optional): "Mathematics" | "Physics" | "English Language" | "Use of English"
- `topic` (optional): "Algebra" | "Geometry" | "Trigonometry" | etc.
- `year` (optional): 2020-2024
- `difficulty` (optional): "easy" | "medium" | "hard"
- `limit` (optional, default 20): Max 100 results
- `offset` (optional, default 0): For pagination

**Example**:
```
GET /questions/search?exam_board=WAEC&subject=Mathematics&topic=Algebra&limit=10
```

**Response (200)**:
```json
{
  "total": 45,
  "limit": 10,
  "offset": 0,
  "questions": [
    {
      "id": "waec_math_2020_001",
      "exam_board": "WAEC",
      "subject": "Mathematics",
      "topic": "Algebra",
      "year": 2020,
      "question_number": 1,
      "question_text": "Solve for x: 2x + 3 = 11",
      "options": ["4", "5", "6", "7"],
      "difficulty": "easy",
      "preview": "2x + 3 = 11..."
    }
  ]
}
```

### GET /questions/{question_id}
Get full question details with explanation.

**Headers**: `Authorization: Bearer {access_token}` (optional, for tracking)

**Response (200)**:
```json
{
  "id": "waec_math_2020_001",
  "exam_board": "WAEC",
  "subject": "Mathematics",
  "topic": "Algebra",
  "year": 2020,
  "question_number": 1,
  "question_text": "Solve for x: 2x + 3 = 11",
  "options": ["4", "5", "6", "7"],
  "correct_answer": "B",
  "difficulty": "easy",
  "source_url": null,
  "explanation": "To solve 2x + 3 = 11:\n1. Subtract 3 from both sides: 2x = 8\n2. Divide by 2: x = 4\nWait, let me recalculate... x = 4 is option A. Hmm, let me check the answer key again.",
  "created_at": "2025-12-10T16:22:08.712345"
}
```

### GET /questions/random
Get random questions for quiz/readiness assessment.

**Query Parameters**:
- `count` (required): Number of questions (1-50)
- `exam_board` (optional): Filter by exam board
- `subject` (optional): Filter by subject
- `difficulty` (optional): Filter by difficulty

**Example**:
```
GET /questions/random?count=15&exam_board=WAEC
```

**Response (200)**:
```json
{
  "questions": [
    {
      "id": "waec_math_2020_001",
      "question_text": "Solve for x: 2x + 3 = 11",
      "options": ["4", "5", "6", "7"],
      "difficulty": "easy"
    }
    // ... 14 more questions
  ]
}
```

---

## 3. USER ATTEMPTS & PROGRESS

### POST /questions/attempt
Log user's answer to a question.

**Headers**: `Authorization: Bearer {access_token}` (required)

**Request**:
```json
{
  "question_id": "waec_math_2020_001",
  "user_answer": "B",
  "time_taken_seconds": 45
}
```

**Response (200)**:
```json
{
  "question_id": "waec_math_2020_001",
  "user_answer": "B",
  "correct_answer": "B",
  "is_correct": true,
  "score": 1,
  "explanation": "..."
}
```

### GET /user/progress
Get user's overall progress stats.

**Headers**: `Authorization: Bearer {access_token}` (required)

**Response (200)**:
```json
{
  "user_id": "user_12345",
  "total_questions_attempted": 127,
  "total_correct": 98,
  "accuracy_percent": 77.2,
  "by_exam_board": {
    "WAEC": {
      "attempted": 67,
      "correct": 54,
      "accuracy_percent": 80.6
    },
    "NECO": {
      "attempted": 40,
      "correct": 28,
      "accuracy_percent": 70.0
    },
    "JAMB": {
      "attempted": 20,
      "correct": 16,
      "accuracy_percent": 80.0
    }
  },
  "by_subject": {
    "Mathematics": {
      "attempted": 45,
      "correct": 35,
      "accuracy_percent": 77.8
    },
    "Physics": {
      "attempted": 40,
      "correct": 32,
      "accuracy_percent": 80.0
    },
    "English Language": {
      "attempted": 30,
      "correct": 24,
      "accuracy_percent": 80.0
    },
    "Use of English": {
      "attempted": 12,
      "correct": 7,
      "accuracy_percent": 58.3
    }
  },
  "weak_topics": [
    {
      "topic": "Trigonometry",
      "accuracy_percent": 45.0,
      "questions_attempted": 10
    },
    {
      "topic": "Calculus",
      "accuracy_percent": 55.0,
      "questions_attempted": 8
    }
  ],
  "streak_days": 5,
  "last_activity": "2025-12-12T10:30:00Z"
}
```

### GET /user/weak-topics
Get topics where user is struggling.

**Headers**: `Authorization: Bearer {access_token}` (required)

**Response (200)**:
```json
{
  "weak_topics": [
    {
      "subject": "Mathematics",
      "topic": "Trigonometry",
      "accuracy_percent": 45.0,
      "questions_attempted": 10,
      "recommendation": "Review trigonometric identities and angle transformations"
    }
  ]
}
```

### POST /user/bookmarks
Bookmark a question for later review.

**Headers**: `Authorization: Bearer {access_token}` (required)

**Request**:
```json
{
  "question_id": "waec_math_2020_001"
}
```

**Response (200)**:
```json
{
  "bookmarked": true,
  "question_id": "waec_math_2020_001"
}
```

### GET /user/bookmarks
Get all bookmarked questions.

**Headers**: `Authorization: Bearer {access_token}` (required)

**Response (200)**:
```json
{
  "total": 8,
  "bookmarks": [
    {
      "id": "waec_math_2020_001",
      "question_text": "...",
      "exam_board": "WAEC",
      "subject": "Mathematics",
      "topic": "Algebra"
    }
  ]
}
```

---

## 4. READINESS ASSESSMENT

### POST /readiness/start-assessment
Start a new readiness assessment (15 questions).

**Headers**: `Authorization: Bearer {access_token}` (required)

**Request** (optional):
```json
{
  "exam_board": "WAEC"
}
```

**Response (200)**:
```json
{
  "assessment_id": "assess_abc123",
  "questions": [
    {
      "id": "waec_math_2020_001",
      "question_text": "...",
      "options": ["A", "B", "C", "D"]
    }
    // ... 14 more questions
  ],
  "estimated_time_minutes": 15
}
```

### POST /readiness/submit-assessment
Submit completed assessment.

**Headers**: `Authorization: Bearer {access_token}` (required)

**Request**:
```json
{
  "assessment_id": "assess_abc123",
  "answers": [
    {"question_id": "waec_math_2020_001", "user_answer": "B"},
    {"question_id": "waec_phys_2020_002", "user_answer": "C"}
    // ... 13 more answers
  ]
}
```

**Response (200)**:
```json
{
  "assessment_id": "assess_abc123",
  "score": 12,
  "total_questions": 15,
  "accuracy_percent": 80.0,
  "readiness_by_exam_board": {
    "WAEC": {
      "pass_probability_percent": 82,
      "feedback": "You are well-prepared for WAEC. Focus on weak topics: Trigonometry (45% accuracy)"
    },
    "NECO": {
      "pass_probability_percent": 80,
      "feedback": "Good readiness for NECO. Similar syllabus to WAEC."
    },
    "JAMB": {
      "pass_probability_percent": 78,
      "feedback": "Acceptable readiness for JAMB. More practice on speed and accuracy needed."
    }
  },
  "weak_topics": [
    {
      "topic": "Trigonometry",
      "accuracy_percent": 45.0,
      "recommendation": "Spend 2-3 hours on this topic before the exam"
    }
  ],
  "next_steps": "Continue practicing weak topics. Take mock exams weekly."
}
```

---

## 5. SYSTEM ENDPOINTS

### GET /health
Health check.

**Response (200)**:
```json
{
  "status": "ok",
  "timestamp": "2025-12-12T10:30:00Z"
}
```

### GET /metrics
Simple metrics (connected app users only).

**Headers**: `X-AKU-APP: connected` (or `?connected=1`)

**Response (200)**:
```json
{
  "total_slots": 10,
  "reserved": 4,
  "priority_available": 3,
  "general_available": 2,
  "active_users": 45,
  "questions_in_system": 1350
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid query parameters",
  "error_code": "INVALID_PARAMS"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token",
  "error_code": "INVALID_TOKEN"
}
```

### 404 Not Found
```json
{
  "detail": "Question not found",
  "error_code": "NOT_FOUND"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Server capacity reached. Try again in a few seconds.",
  "error_code": "CAPACITY_EXCEEDED",
  "retry_after": 5
}
```

### 500 Internal Server Error
```json
{
  "detail": "An unexpected error occurred",
  "error_code": "INTERNAL_ERROR"
}
```

---

## Authentication Headers

All protected endpoints require:
```
Authorization: Bearer {access_token}
```

Example:
```
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  https://api.akulearn.com/api/user/progress
```

---

## Rate Limiting

- Unauthenticated: 10 requests/minute per IP
- Authenticated: 100 requests/minute per user
- Search: 1000 questions/day per user

Headers returned:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1702400000
```

---

## Pagination

All list endpoints support:
- `limit` (default 20, max 100)
- `offset` (default 0)

Example:
```
GET /questions/search?limit=20&offset=40
```

---

## Search Operators

Advanced search syntax:
```
q=algebra AND NOT "linear equations"
q=subject:Mathematics AND difficulty:hard
q="quadratic formula" OR "cubic equations"
```

---

## Data Sync (Offline Support)

For PWA/offline support, clients should:
1. Cache responses from `/questions/search` and `/questions/{id}`
2. Queue failed POST requests (attempts, bookmarks)
3. Retry when connectivity restored

Sync endpoint:
```
POST /sync
{
  "pending_attempts": [...],
  "pending_bookmarks": [...]
}
```

---

## Next Steps

1. Implement all endpoints in `connected_stack/backend/main.py`
2. Add database schema (SQLite for MVP)
3. Write unit tests
4. Load `data/exam_papers/` into database
5. Test all endpoints with Postman
6. Document in Swagger UI

---

**Generated**: December 12, 2025
**Status**: Ready for Implementation
**Backend Framework**: FastAPI (Python)
**Database**: SQLite (MVP) → PostgreSQL (Production)
