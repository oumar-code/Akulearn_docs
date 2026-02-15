# 🚀 Akulearn First Product Launch Strategy
## "Help Nigerian Students Pass WAEC, NECO & JAMB"

**Target Users**: Nigerian secondary school students (SS1-SS3)
**Geographic**: Nigeria-wide (diaspora accessible)
**Primary Device**: Mobile (iOS/Android) + Browser (PWA)
**First Exam Boards**: WAEC, NECO, JAMB
**Launch Timeline**: 8-12 weeks to MVP

---

## 📋 Product Definition (MVP 1.0)

### Core Features
1. **Registration & Authentication**
   - Simple email/phone registration
   - SMS/Email OTP verification
   - Lightweight user profile (name, exam board, target subjects)

2. **Search & Discovery**
   - Search by exam board (WAEC, NECO, JAMB)
   - Search by subject (Math, Physics, English, etc.)
   - Search by topic (Algebra, Geometry, etc.)
   - Free-text search (keywords, problem descriptions)
   - Browse by year (2020-2024)

3. **Learn & Test**
   - View full question with explanation
   - Multiple-choice quiz UI (A, B, C, D options)
   - Track attempts and score
   - See correct answer + explanation
   - Difficulty level indicator (easy/medium/hard)

4. **Offline Support (PWA)**
   - Download exams for offline use
   - Sync progress when online
   - No internet? Still practice

5. **Progress Tracking**
   - Questions attempted
   - Correct/incorrect counts
   - Accuracy by subject/topic
   - Readiness score (0-100% for each exam board)

6. **Readiness Assessment**
   - Diagnostic quiz (10-15 random questions)
   - Estimated pass probability for WAEC/NECO/JAMB
   - Weak areas highlighted
   - Recommendations for study

---

## 🏗️ Technical Architecture

### Frontend (Connected Stack)
**Framework**: React Native (cross-platform) + React Web (PWA)
**What Exists**: 
- `connected_stack/frontend/` with React Native setup
- App.js, screens, components, theme, user context
- API integration layer

**What We Need to Add**:
1. **Search UI** (SearchScreen.js)
   - Text input with filters (exam board, subject, topic)
   - Results list with preview
   - Deep link to question detail

2. **Question Detail Screen** (QuestionDetailScreen.js)
   - Full question text
   - 4 options (A, B, C, D)
   - Show answer button
   - See explanation button
   - Mark for review / Save for later
   - Next/Previous navigation

3. **Quiz Mode** (QuizScreen.js)
   - Randomized questions (configurable count)
   - Timer (optional)
   - Progress bar
   - Submit button
   - Results screen (score, % correct, breakdown by topic)

4. **Readiness Assessment** (ReadinessScreen.js)
   - 15 random questions across exams
   - Quick assessment (8-10 min)
   - Pass probability prediction
   - Weak topics identified

5. **Offline Support**
   - Service Worker (PWA)
   - IndexedDB for local storage
   - Auto-sync on connection

6. **User Dashboard** (HomeScreen.js)
   - Quick stats (questions done, score, streak)
   - Continue learning button
   - Top weak topics
   - Exam board selector
   - Search bar (prominent)

### Backend (Connected Stack)
**Framework**: FastAPI (Python)
**What Exists**:
- `connected_stack/backend/main.py` with FastAPI + CORS + health/metrics endpoints
- Prioritization for connected users (reserved slots)
- Placeholder LLM integration

**What We Need to Add**:

1. **Auth Service**
   - POST `/auth/register` - email/phone + password
   - POST `/auth/verify-otp` - OTP from SMS
   - POST `/auth/login` - email + password
   - POST `/auth/refresh-token` - refresh JWT
   - POST `/auth/logout`

2. **Search Service**
   - GET `/search?q=<keyword>&exam_board=<WAEC>&subject=<Math>&topic=<Algebra>&year=<2024>`
   - Returns array of questions with summary

3. **Question Service**
   - GET `/questions/<question_id>` - full question + explanation
   - GET `/questions/random?count=10&exam_board=WAEC` - random questions
   - POST `/questions/attempt` - log user's answer + score

4. **Readiness Service**
   - POST `/readiness/assess` - run 15-q diagnostic
   - GET `/readiness/status` - pass probability for each exam board

5. **User Progress Service**
   - GET `/user/progress` - stats (attempted, correct, by subject)
   - GET `/user/weak-topics` - topics needing improvement
   - POST `/user/bookmarks` - save question for later

6. **Data Service**
   - Load exam data from `data/exam_papers/` (1,350 questions)
   - Expose via REST endpoints

### Data Pipeline (MLOps)
**Status**: ✅ COMPLETE
**What Exists**:
- `mlops/exam_paper_scraper.py` - generates 1,350 questions (WAEC/NECO/JAMB, 4 subjects, 27 topics, 2020-2024)
- `data/exam_papers/` - organized by subject/topic
- `mlops/generate_lo_catalog.py` - learning objectives from NERDC curriculum

**Integration**:
- Backend loads `data/exam_papers/all_questions.json` on startup
- Cache in-memory for fast search
- Optional: Load into PostgreSQL for larger datasets

### Database
**Option 1 (MVP)**: JSON files + in-memory cache (fast, simple)
- Suitable for 1,350 questions
- No database setup required
- Scale limit: ~100k questions

**Option 2 (Scale)**: PostgreSQL + Redis
- Horizontal scaling
- Full-text search
- Caching for performance

**Recommendation**: Start with Option 1, migrate to PostgreSQL in Phase 2

---

## 📱 PWA Setup (Cross-Platform)

**Tech Stack**:
- React Web (frontend)
- Service Worker (offline)
- IndexedDB (local sync)
- Web App Manifest (installable)

**Deployment**:
- Netlify or Vercel (CDN)
- Google Play Store + App Store (wrapped with Capacitor or EAS Build)

---

## 🗂️ Folder & File Organization

```
akulearn-docs/
├── connected_stack/
│   ├── backend/
│   │   ├── main.py (FastAPI app)
│   │   ├── auth.py (new: auth logic)
│   │   ├── search.py (new: search service)
│   │   ├── questions.py (new: question service)
│   │   ├── readiness.py (new: readiness assessment)
│   │   ├── progress.py (new: user progress tracking)
│   │   └── requirements.txt (update with new deps)
│   ├── frontend/
│   │   ├── App.js (root)
│   │   ├── components/
│   │   │   ├── SearchBar.js (new)
│   │   │   ├── QuestionCard.js (new)
│   │   │   ├── ProgressBar.js (new)
│   │   │   └── ReadinessScore.js (new)
│   │   ├── screens/
│   │   │   ├── HomeScreen.js (dashboard)
│   │   │   ├── SearchScreen.js (new)
│   │   │   ├── QuestionDetailScreen.js (new)
│   │   │   ├── QuizScreen.js (new)
│   │   │   ├── ReadinessScreen.js (new)
│   │   │   ├── ProgressScreen.js (new)
│   │   │   └── AuthScreen.js (new: register/login)
│   │   ├── api.js (HTTP calls to backend)
│   │   ├── UserContext.js (auth state)
│   │   ├── theme.js (colors, fonts)
│   │   └── package.json
│   ├── deployment/
│   │   ├── docker-compose.yml (frontend + backend services)
│   │   ├── Dockerfile.backend
│   │   ├── Dockerfile.frontend
│   │   ├── nginx.conf (PWA reverse proxy)
│   │   └── env.example
│   └── README.md
├── mlops/
│   ├── exam_paper_scraper.py (existing: data generation)
│   └── data/ (existing: 1,350 questions)
├── docs/
│   ├── API.md (endpoint documentation)
│   ├── PWA_SETUP.md (offline + installation)
│   ├── USER_GUIDE.md (how to use the app)
│   └── DEPLOYMENT.md (production checklist)
└── ...
```

---

## 🔄 Development Roadmap (8-12 Weeks)

### Week 1-2: Backend Core
- [ ] Auth service (register, login, JWT, OTP)
- [ ] Load `data/exam_papers/all_questions.json` into backend
- [ ] Question endpoint (`GET /questions/<id>`)
- [ ] Search endpoint with filters
- [ ] User progress endpoint (POST attempt, GET stats)
- [ ] API documentation (Swagger)

### Week 3-4: Frontend Authentication & Search
- [ ] Auth screens (register, login, OTP)
- [ ] Home screen (dashboard with quick stats)
- [ ] Search screen (search bar, filters, results)
- [ ] Question detail screen (view Q + answer)
- [ ] API integration (calls to backend)

### Week 5-6: Quiz & Readiness
- [ ] Quiz screen (timed questions, submit)
- [ ] Results screen (score breakdown)
- [ ] Readiness assessment (15-q diagnostic)
- [ ] Progress tracking UI
- [ ] Offline support (Service Worker + IndexedDB)

### Week 7-8: Polish & Testing
- [ ] UI/UX refinement
- [ ] Cross-browser testing (Chrome, Safari, Firefox)
- [ ] Mobile testing (iOS, Android)
- [ ] Performance optimization
- [ ] Load testing (simultaneous users)

### Week 9-10: Deployment & Launch Prep
- [ ] Docker setup (containerize frontend + backend)
- [ ] Deploy to staging (Heroku, Railway, or AWS)
- [ ] Setup CI/CD pipeline (GitHub Actions)
- [ ] Create app store listings (Apple + Google)
- [ ] Marketing materials (screenshots, description)

### Week 11-12: Go-Live & Support
- [ ] Launch on app stores + web
- [ ] Monitor errors and performance
- [ ] Support first cohort of users
- [ ] Gather feedback

---

## 📊 Key Metrics to Track

**User Acquisition**
- Downloads (app stores)
- Signups
- Geographic distribution

**Engagement**
- Daily Active Users (DAU)
- Questions answered per user
- Avg session duration
- Return rate (30-day retention)

**Learning Outcomes**
- Avg accuracy by exam board
- Weak topics identified
- Readiness score improvement

**Technical**
- API response time (<200ms)
- Search response time (<500ms)
- Error rate (<0.1%)
- Uptime (>99.5%)

---

## 🎯 Success Criteria (MVP Launch)

✅ **Users Can**:
- Register and login (email or phone)
- Search questions by exam board, subject, topic, keyword
- View full question with 4 options
- See correct answer + detailed explanation
- Take a timed quiz (10-20 questions)
- Get readiness assessment (pass probability for WAEC/NECO/JAMB)
- Track progress (questions done, accuracy, weak topics)
- Use app offline (PWA)
- Download app on iOS + Android

✅ **System**:
- Responds to searches in <500ms
- Handles 100 concurrent users
- Syncs offline data when online
- Logs all user activity for analytics
- Provides simple admin dashboard

✅ **Product**:
- 1,350+ questions available
- All major subjects covered
- Latest exam years (2020-2024)
- Clear explanations for all answers

---

## 📞 Next Immediate Steps

1. **Confirm Backend MVP Endpoints** (Today)
   - Finalize API contract (auth, search, questions, progress)
   - Update `connected_stack/backend/main.py` with all endpoints
   - Add database schema (PostgreSQL or SQLite for MVP)

2. **Start Frontend Screens** (This Week)
   - Auth flow (register → login → home)
   - Search screen
   - Question detail screen
   - Wire to backend

3. **Data Integration** (This Week)
   - Load `data/exam_papers/` into backend
   - Expose via `/questions` endpoint
   - Test search performance

4. **Testing & QA** (Ongoing)
   - Unit tests for backend
   - Integration tests (frontend + backend)
   - Manual testing on real devices

5. **Deployment Plan** (Week 7+)
   - Docker & Docker Compose
   - GitHub Actions CI/CD
   - Staging environment
   - Production deployment

---

## 💡 Quick Wins (Fast to Launch)

1. **Use Existing Data**: Your exam scraper has 1,350 ready questions ✅
2. **Lightweight Auth**: Simple email + password (add SMS later)
3. **No AI Initially**: Static explanations from data (add AI tutoring in Phase 2)
4. **MVP Design**: Clean, simple UI (no animations)
5. **Offline First**: IndexedDB + Service Worker = free offline feature
6. **Leverage Connected Stack**: React Native + FastAPI = faster time-to-market

---

## 🚀 Ready to Start?

**Which phase do you want to focus on first?**

1. **Backend**: Finalize API endpoints, load data, auth system
2. **Frontend**: Build screens, wire to backend
3. **Deployment**: Docker, CI/CD, app store listings
4. **Testing**: Manual testing, load testing, QA

Pick one, and I'll help implement it with working code.

---

**Estimated Cost to Launch**:
- Development: 8-12 weeks (your team)
- Hosting: ~$200-500/month (AWS or similar)
- App Store: $99 (Apple) + Free (Google)
- **Total: ~$1,000-2,000 launch cost**

**Expected Users (First 3 Months)**:
- Organic growth: 500-2,000 users
- With basic marketing: 5,000-10,000 users
- Viral potential (especially exam season): 50,000+ users

Let's build it! 🎓
