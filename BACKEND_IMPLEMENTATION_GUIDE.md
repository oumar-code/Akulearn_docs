# Backend Implementation Guide for Akulearn MVP

## Quick Start

### 1. Install Dependencies

```bash
cd connected_stack/backend
pip install -r requirements.txt
```

### 2. Run the Backend

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Visit `http://localhost:8000/docs` for interactive API documentation.

### 3. Quick Test

```bash
# Health check
curl http://localhost:8000/api/health

# Get available filters
curl http://localhost:8000/api/questions/filters

# Get filters (pretty print)
curl http://localhost:8000/api/questions/filters | python -m json.tool
```

---

## Project Structure

```
connected_stack/backend/
├── main.py                    # FastAPI application with all endpoints
├── auth_service.py           # User authentication, JWT, OTP
├── questions_service.py      # Question loading, searching, filtering
├── progress_service.py       # User progress tracking, weak topics
├── requirements.txt          # Python dependencies
├── .env                      # (Create: environment variables)
├── .env.example             # (Create: example env file)
├── tests/                    # (Create: unit tests)
└── README.md                # (Create: deployment guide)
```

---

## Services Overview

### 1. AuthService (`auth_service.py`)

**Purpose**: Handle user registration, authentication, OTP verification, JWT tokens

**Key Methods**:
- `register()` - Create new user account
- `login()` - Authenticate with email/password  
- `verify_otp()` - Confirm email via OTP
- `refresh_token()` - Get new access token
- `logout()` - Invalidate token

**Features**:
- Password strength validation
- OTP generation and verification
- JWT token management (access + refresh tokens)
- In-memory user storage (replace with PostgreSQL in production)
- Email validation

**Usage**:
```python
from auth_service import auth_service

# Register
result = auth_service.register(
    email="student@gmail.com",
    password="SecurePass123",
    full_name="John Doe",
    exam_board="WAEC",
    target_subjects=["Mathematics", "Physics"]
)

# Login
result = auth_service.login(
    email="student@gmail.com",
    password="SecurePass123"
)
```

### 2. QuestionsService (`questions_service.py`)

**Purpose**: Load exam questions, search/filter, serve for quizzes

**Key Methods**:
- `load_questions()` - Load all 1,350 questions from JSON
- `search()` - Search with exam board, subject, topic, keyword filters
- `get_question()` - Get full question with answer + explanation
- `get_random_questions()` - Get random questions for quizzes
- `get_filters()` - Get available search filters
- `get_statistics()` - Get question distribution stats

**Features**:
- Loads from `data/exam_papers/all_questions.json`
- Builds indices for fast searching (topic, subject, exam board)
- Calculates statistics on startup
- Supports advanced filtering
- Hides answers for preview searches

**Usage**:
```python
from questions_service import questions_service

# Load questions (called automatically on startup)
questions_service.load_questions()

# Search for questions
results = questions_service.search(
    exam_board="WAEC",
    subject="Mathematics",
    topic="Algebra",
    limit=20,
    offset=0
)

# Get random questions for quiz
questions = questions_service.get_random_questions(
    count=15,
    exam_board="WAEC",
    difficulty="medium"
)

# Get question details
question = questions_service.get_question("waec_math_2020_001")
```

### 3. ProgressService (`progress_service.py`)

**Purpose**: Track user attempts, calculate accuracy, identify weak topics

**Key Methods**:
- `record_attempt()` - Log user's answer to a question
- `get_progress()` - Get overall accuracy statistics
- `get_weak_topics()` - Get topics where user is struggling
- `bookmark_question()` - Bookmark for later review
- `record_assessment()` - Log readiness assessment results

**Features**:
- Tracks accuracy by exam board, subject, topic
- Identifies weak topics (accuracy < 65%)
- Calculates learning streak (consecutive days)
- Generates personalized recommendations
- Estimates pass probability (simplified)

**Usage**:
```python
from progress_service import progress_service

# Record an attempt
progress_service.record_attempt(
    user_id="user_12345",
    question_id="waec_math_2020_001",
    user_answer="B",
    correct_answer="B",
    time_taken_seconds=45,
    exam_board="WAEC",
    subject="Mathematics",
    topic="Algebra"
)

# Get progress stats
progress = progress_service.get_progress("user_12345")

# Get weak topics
weak = progress_service.get_weak_topics("user_12345")
```

---

## API Endpoints Reference

### Authentication

```
POST   /api/auth/register         - Register new student
POST   /api/auth/verify-otp       - Verify email with OTP
POST   /api/auth/resend-otp       - Resend OTP
POST   /api/auth/login            - Login with email/password
POST   /api/auth/refresh-token    - Get new access token
POST   /api/auth/logout           - Logout (requires auth)
```

### Questions & Search

```
GET    /api/questions/search      - Search questions (exam board, subject, topic, keyword)
GET    /api/questions/{id}        - Get full question details (requires auth)
GET    /api/questions/random      - Get random questions for quiz
GET    /api/questions/filters     - Get available search filters
```

### User Progress

```
POST   /api/questions/attempt     - Record user's answer (requires auth)
GET    /api/user/progress         - Get overall progress stats (requires auth)
GET    /api/user/weak-topics      - Get topics to focus on (requires auth)
POST   /api/user/bookmarks        - Bookmark a question (requires auth)
GET    /api/user/bookmarks        - Get bookmarked questions (requires auth)
```

### Readiness Assessment

```
POST   /api/readiness/start-assessment    - Start 15-Q assessment (requires auth)
POST   /api/readiness/submit-assessment   - Submit assessment (requires auth)
```

### System

```
GET    /api/health                - Health check
GET    /api/metrics               - Runtime metrics (connected users only)
GET    /api/test/db-status        - Test database initialization
```

---

## Environment Variables

Create a `.env` file in `connected_stack/backend/`:

```env
# Server
HOST=0.0.0.0
PORT=8000

# JWT Configuration
JWT_SECRET=your-secret-key-here-change-in-production
JWT_EXPIRY_HOURS=24

# Questions Data Path
QUESTIONS_DATA_PATH=../../data/exam_papers/all_questions.json

# Concurrency Control
AKU_TOTAL_SLOTS=10
AKU_RESERVED_SLOTS=4

# Database (future)
# DATABASE_URL=postgresql://user:password@localhost/akulearn
```

---

## Testing the API

### Using cURL

```bash
# 1. Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "password": "SecurePass123",
    "full_name": "Test Student",
    "exam_board": "WAEC",
    "target_subjects": ["Mathematics"]
  }'

# 2. Verify OTP (get OTP from response above)
curl -X POST http://localhost:8000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "otp": "123456"
  }'

# 3. Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "password": "SecurePass123"
  }'

# 4. Search questions (no auth needed)
curl "http://localhost:8000/api/questions/search?exam_board=WAEC&subject=Mathematics&limit=5"

# 5. Get question details (replace TOKEN with access_token from login)
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/questions/waec_math_2020_001

# 6. Record attempt
curl -X POST http://localhost:8000/api/questions/attempt \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": "waec_math_2020_001",
    "user_answer": "B",
    "correct_answer": "B",
    "time_taken_seconds": 45,
    "exam_board": "WAEC",
    "subject": "Mathematics",
    "topic": "Algebra"
  }'

# 7. Get progress
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/user/progress
```

### Using Python

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

# Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "student@test.com",
    "password": "SecurePass123",
    "full_name": "Test Student",
    "exam_board": "WAEC",
    "target_subjects": ["Mathematics"]
})
print(json.dumps(response.json(), indent=2))

# Verify OTP
otp = response.json()["verification_token"]
response = requests.post(f"{BASE_URL}/auth/verify-otp", json={
    "email": "student@test.com",
    "otp": otp
})

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "student@test.com",
    "password": "SecurePass123"
})
token = response.json()["access_token"]

# Search
response = requests.get(f"{BASE_URL}/questions/search", params={
    "exam_board": "WAEC",
    "subject": "Mathematics",
    "limit": 5
})
print(json.dumps(response.json(), indent=2))

# Get progress
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/user/progress", headers=headers)
print(json.dumps(response.json(), indent=2))
```

### Using Postman

1. Import the `API_SPECIFICATION.md` into Postman
2. Create a collection with folders for each endpoint group
3. Use Postman's pre-request script to manage tokens:

```javascript
// Pre-request script
if (pm.environment.get("access_token")) {
    pm.request.headers.add({
        key: "Authorization",
        value: `Bearer ${pm.environment.get("access_token")}`
    });
}
```

---

## Database Schema (Future - PostgreSQL)

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(32) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    exam_board VARCHAR(50),
    target_subjects TEXT,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_user_id (user_id)
);

-- Attempts table
CREATE TABLE attempts (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL,
    question_id VARCHAR(100) NOT NULL,
    user_answer VARCHAR(1),
    correct_answer VARCHAR(1),
    is_correct BOOLEAN NOT NULL,
    time_taken_seconds INT,
    exam_board VARCHAR(50),
    subject VARCHAR(100),
    topic VARCHAR(100),
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id),
    INDEX idx_exam_board (exam_board),
    INDEX idx_subject (subject),
    INDEX idx_topic (topic)
);

-- Assessments table
CREATE TABLE assessments (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL,
    assessment_id VARCHAR(32) UNIQUE NOT NULL,
    exam_board VARCHAR(50),
    score INT,
    total_questions INT,
    accuracy_percent DECIMAL(5,2),
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id)
);

-- Bookmarks table
CREATE TABLE bookmarks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL,
    question_id VARCHAR(100) NOT NULL,
    bookmarked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE KEY unique_bookmark (user_id, question_id)
);
```

---

## Error Handling

The API returns standard HTTP status codes:

| Status | Meaning | Example |
|--------|---------|---------|
| 200 | OK | Question found, request successful |
| 201 | Created | User registered successfully |
| 400 | Bad Request | Invalid email format, missing fields |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Access denied (e.g., metrics for non-connected users) |
| 404 | Not Found | Question doesn't exist |
| 429 | Too Many Requests | Server at capacity, retry later |
| 500 | Internal Error | Unexpected server error |
| 503 | Service Unavailable | Questions not loaded yet |

Error response format:
```json
{
  "detail": "Question not found",
  "status_code": 404,
  "timestamp": "2025-12-12T10:30:00.000000"
}
```

---

## Performance Optimization (TODO)

1. **Caching**
   - Cache frequently searched questions
   - Cache user progress calculations
   - Use Redis for distributed caching

2. **Database**
   - Replace in-memory storage with PostgreSQL
   - Add database indexes for fast lookups
   - Implement query optimization

3. **API**
   - Add response compression (gzip)
   - Implement pagination properly
   - Add rate limiting

4. **Search**
   - Implement full-text search (Elasticsearch)
   - Add faceted search for filtering
   - Implement search suggestions/autocomplete

---

## Deployment Checklist

- [ ] Install production dependencies: `pip install -r requirements.txt`
- [ ] Set secure JWT_SECRET in .env
- [ ] Configure database URL for PostgreSQL
- [ ] Set up environment variables
- [ ] Run database migrations
- [ ] Enable CORS only for allowed origins
- [ ] Set up SSL/TLS certificates
- [ ] Configure logging and monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure backup strategy
- [ ] Test all endpoints with production data
- [ ] Set up health checks and monitoring
- [ ] Configure Docker and docker-compose
- [ ] Set up CI/CD pipeline (GitHub Actions)

---

## Next Steps

1. **Install and Run**
   ```bash
   cd connected_stack/backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Test Locally**
   - Visit http://localhost:8000/docs
   - Try the endpoints with the interactive UI
   - Test with cURL or Python

3. **Frontend Integration**
   - Update `connected_stack/frontend/api.js` to call these endpoints
   - Implement screens for auth, search, quiz, progress
   - Test end-to-end flow

4. **Production Deployment**
   - Set up PostgreSQL database
   - Configure environment variables
   - Deploy with Docker to AWS/Heroku/Railway
   - Set up monitoring and logging

---

**Generated**: December 12, 2025
**Status**: Ready for Development
**Next Milestone**: Frontend integration (Week 3)
