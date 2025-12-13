# Akulearn Backend - FastAPI

Complete backend API for the Akulearn learning platform serving Nigerian students preparing for WAEC, NECO, and JAMB exams.

## ✨ Features

- **🔐 Authentication**: User registration, OTP verification, JWT tokens
- **🔍 Smart Search**: Filter by exam board, subject, topic, year, difficulty  
- **❓ Question Database**: 1,350 exam questions ready to use
- **📊 Progress Tracking**: Accuracy by subject/topic, weak topic detection
- **🎯 Readiness Assessment**: 15-question diagnostic tests
- **⭐ Bookmarks**: Save questions for later review
- **⚡ Optimized**: In-memory indices for fast searching

## 🚀 Quick Start

### Installation

```bash
# 1. Navigate to backend directory
cd connected_stack/backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Test It

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health
- **See Questions**: http://localhost:8000/api/questions/search?exam_board=WAEC&limit=5

## 📁 Project Structure

```
connected_stack/backend/
├── main.py                          # FastAPI app with all endpoints
├── auth_service.py                 # Authentication & JWT management
├── questions_service.py            # Question loading & search
├── progress_service.py             # User progress & weak topics
├── requirements.txt                # Python packages
├── test_services.py               # Unit tests
└── README.md                      # This file
```

## 🔌 API Overview

### Authentication
```bash
POST   /api/auth/register           # Create account
POST   /api/auth/verify-otp         # Verify email
POST   /api/auth/login              # Login
POST   /api/auth/refresh-token      # Get new access token
POST   /api/auth/logout             # Logout
```

### Questions
```bash
GET    /api/questions/search        # Search questions
GET    /api/questions/{id}          # Get question details
GET    /api/questions/random        # Random questions for quiz
GET    /api/questions/filters       # Available filters
```

### User Progress
```bash
POST   /api/questions/attempt       # Log answer
GET    /api/user/progress           # Overall stats
GET    /api/user/weak-topics        # Topics to focus on
POST   /api/user/bookmarks          # Bookmark question
GET    /api/user/bookmarks          # Get bookmarks
```

### Readiness Assessment
```bash
POST   /api/readiness/start-assessment    # Start 15-Q test
POST   /api/readiness/submit-assessment   # Submit results
```

**Full API docs**: See `API_SPECIFICATION.md` or visit http://localhost:8000/docs

## 🏗️ Architecture

### Services

#### AuthService
- User registration and password validation
- OTP generation and verification
- JWT token management (access + refresh)
- Email verification
- In-memory user storage (replace with DB in production)

#### QuestionsService
- Loads all 1,350 exam questions from JSON
- Builds fast indices (topic, subject, exam board)
- Supports multi-filter searching
- Serves questions for quizzes/assessments
- Calculates statistics

#### ProgressService
- Records user answers/attempts
- Calculates accuracy by exam board/subject/topic
- Identifies weak topics (accuracy < 65%)
- Tracks learning streak
- Manages bookmarks
- Records assessment results

## 📊 Data Sources

Questions are loaded from `data/exam_papers/all_questions.json`:
- **1,350 total questions**
- 3 exam boards: WAEC, NECO, JAMB
- 4 subjects: Mathematics, Physics, English Language, Use of English
- 27 topics across subjects
- Years 2020-2024
- Difficulty levels: easy, medium, hard

## 🧪 Testing

### Run Unit Tests
```bash
pip install pytest
pytest test_services.py -v
```

### Manual Testing
```bash
# Get filters
curl http://localhost:8000/api/questions/filters | python -m json.tool

# Search questions
curl "http://localhost:8000/api/questions/search?exam_board=WAEC&subject=Mathematics&limit=3"

# See detailed test instructions
cat test_services.py
```

## 🔐 Authentication Flow

```
1. Register
   POST /auth/register → Get OTP in response

2. Verify OTP
   POST /auth/verify-otp → Email verified

3. Login
   POST /auth/login → Get access_token + refresh_token

4. Use Token
   GET /user/progress 
   Header: Authorization: Bearer {access_token}

5. Refresh Token (when expired)
   POST /auth/refresh-token → Get new access_token
```

## 📝 Example Workflow

```python
import requests

BASE = "http://localhost:8000/api"

# 1. Register
reg = requests.post(f"{BASE}/auth/register", json={
    "email": "student@gmail.com",
    "password": "SecurePass123",
    "full_name": "John Doe",
    "exam_board": "WAEC",
    "target_subjects": ["Mathematics"]
})
otp = reg.json()["verification_token"]

# 2. Verify OTP
requests.post(f"{BASE}/auth/verify-otp", json={
    "email": "student@gmail.com",
    "otp": otp
})

# 3. Login
login = requests.post(f"{BASE}/auth/login", json={
    "email": "student@gmail.com",
    "password": "SecurePass123"
})
token = login.json()["access_token"]

# 4. Search questions
search = requests.get(f"{BASE}/questions/search", params={
    "exam_board": "WAEC",
    "subject": "Mathematics",
    "limit": 5
})

# 5. Get question details (requires auth)
headers = {"Authorization": f"Bearer {token}"}
q = requests.get(f"{BASE}/questions/waec_math_2020_001", headers=headers)

# 6. Record attempt
attempt = requests.post(f"{BASE}/questions/attempt", 
    json={
        "question_id": "waec_math_2020_001",
        "user_answer": "B",
        "correct_answer": "B",
        "time_taken_seconds": 45
    },
    headers=headers
)

# 7. Get progress
progress = requests.get(f"{BASE}/user/progress", headers=headers)
print(progress.json())
```

## 🔑 Environment Variables

Create `.env` file:
```env
JWT_SECRET=your-secret-key-here
JWT_EXPIRY_HOURS=24
QUESTIONS_DATA_PATH=../../data/exam_papers/all_questions.json
AKU_TOTAL_SLOTS=10
AKU_RESERVED_SLOTS=4
```

## 📦 Deployment

### Docker
```bash
# Build image
docker build -t akulearn-backend:latest .

# Run container
docker run -p 8000:8000 akulearn-backend:latest
```

### Production
```bash
# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## 🗄️ Database (Future)

Currently uses in-memory storage. For production:

```bash
# Install PostgreSQL adapter
pip install psycopg2-binary sqlalchemy

# Create PostgreSQL database
psql -c "CREATE DATABASE akulearn"

# Run migrations (to be created)
# alembic upgrade head
```

**Database schema** is documented in `BACKEND_IMPLEMENTATION_GUIDE.md`

## 🚨 Error Handling

All endpoints return proper HTTP status codes:

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request |
| 401 | Unauthorized |
| 404 | Not found |
| 429 | Too many requests |
| 500 | Server error |

## 📈 Performance

- **Question Loading**: ~1-2 seconds for 1,350 questions
- **Search Time**: <100ms with filters
- **JWT Verification**: <5ms per request
- **Random Questions**: <50ms for 15 questions

## 🔗 Integration

### Frontend
Update `connected_stack/frontend/api.js` to call these endpoints:
- Create API client wrapper
- Handle token management
- Implement error handling

### Mobile
React Native app can use the same REST API.

## 📚 Documentation

- **Full API Spec**: `API_SPECIFICATION.md`
- **Implementation Guide**: `BACKEND_IMPLEMENTATION_GUIDE.md`
- **Product Strategy**: `PRODUCT_LAUNCH_STRATEGY.md`
- **Test Examples**: `test_services.py`

## ✅ Checklist

- [x] Auth service (register, login, JWT)
- [x] Questions service (load, search, filter)
- [x] Progress service (attempts, accuracy, weak topics)
- [x] All API endpoints implemented
- [x] Error handling
- [x] Unit tests
- [ ] PostgreSQL database integration
- [ ] Redis caching
- [ ] Elasticsearch for advanced search
- [ ] Docker deployment
- [ ] GitHub Actions CI/CD

## 🚀 Next Steps

1. **Test Locally**
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Integrate Frontend**
   - Update `connected_stack/frontend/api.js`
   - Implement authentication screens
   - Build search interface
   - Create quiz screens

3. **Production**
   - Set up PostgreSQL database
   - Configure environment variables
   - Deploy to AWS/Heroku/Railway
   - Set up monitoring

## 📞 Support

For issues or questions:
1. Check the API docs: http://localhost:8000/docs
2. Review the tests: `test_services.py`
3. Read the guide: `BACKEND_IMPLEMENTATION_GUIDE.md`

---

**Built**: December 2025  
**Status**: MVP Ready ✓  
**Next Phase**: Frontend Integration (Week 3)  
**Target Users**: Nigerian students (WAEC, NECO, JAMB exam prep)
