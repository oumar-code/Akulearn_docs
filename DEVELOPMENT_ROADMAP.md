# Akulearn MVP Development Roadmap
## Week-by-Week Implementation Plan (8-12 weeks to launch)

**Target**: Nigerian secondary students preparing for WAEC, NECO, JAMB exams  
**MVP Focus**: Authentication → Search → Quiz → Progress Tracking → Deploy  

---

## PHASE 1: Backend Foundation (Week 1) ✅ COMPLETE

### Completed
- [x] API specification designed (30+ endpoints)
- [x] AuthService implemented (register, OTP, JWT, login)
- [x] QuestionsService implemented (load, search, filter 1,350 questions)
- [x] ProgressService implemented (attempts, accuracy, weak topics, assessments)
- [x] FastAPI application with all endpoints
- [x] Error handling & validation
- [x] Swagger/OpenAPI documentation
- [x] Unit tests (30+ test cases)
- [x] Configuration (.env.example)
- [x] README & guides

### Deliverables
```
connected_stack/backend/
├── main.py (30+ endpoints, fully functional)
├── auth_service.py (user management, JWT)
├── questions_service.py (search, filter, load)
├── progress_service.py (tracking, analytics)
├── requirements.txt (dependencies)
├── test_services.py (unit tests)
├── .env.example (config template)
├── README.md (quick start)
├── BACKEND_IMPLEMENTATION_GUIDE.md (comprehensive guide)
└── API_SPECIFICATION.md (API reference)
```

### Testing Checklist
- [x] All services load without errors
- [x] Auth register/login/OTP working
- [x] Questions load (1,350 total)
- [x] Search/filter returning results
- [x] Progress tracking calculations correct
- [x] API documentation complete
- [x] Example requests working

### Success Criteria
- ✅ Backend runs: `uvicorn main:app --reload`
- ✅ Swagger UI works: http://localhost:8000/docs
- ✅ Can register user
- ✅ Can login and get token
- ✅ Can search questions
- ✅ Can track progress
- ✅ All tests passing

---

## PHASE 2: Frontend Integration (Week 2-3)

### Week 2: Authentication Screens

#### Goals
- User registration screen
- Email verification screen (OTP)
- Login screen
- Profile setup screen

#### Frontend Files to Update
```
connected_stack/frontend/
├── screens/
│   ├── AuthStack.js (navigation)
│   ├── RegisterScreen.js (new)
│   ├── VerifyOTPScreen.js (new)
│   ├── LoginScreen.js (new)
│   └── ProfileSetupScreen.js (new)
├── components/
│   ├── TextInput.js (form field)
│   ├── Button.js (submit button)
│   ├── OTPInput.js (OTP verification)
│   └── LoadingSpinner.js (loading state)
├── context/
│   └── UserContext.js (update with auth logic)
├── api.js (add auth endpoints)
└── utils/
    └── validation.js (email, password validation)
```

#### Tasks
1. Design registration form
   - Email input (validate format)
   - Password input (strength indicator)
   - Full name input
   - Exam board selector (WAEC, NECO, JAMB)
   - Target subjects multi-select
   - Submit button

2. Implement OTP verification
   - OTP input (6 digits)
   - Timer (15 minutes)
   - Resend button
   - Error handling

3. Design login form
   - Email input
   - Password input
   - Remember me checkbox
   - Forgot password link (for future)
   - Submit button

4. Implement UserContext
   - Store user details (email, user_id, full_name)
   - Store auth tokens (access_token, refresh_token)
   - Auto-login on app open
   - Logout functionality

5. Update api.js
   - Add auth endpoints
   - Handle token management
   - Add error handling
   - Add request/response logging

#### Testing
- [ ] Can register with valid data
- [ ] Email validation works
- [ ] Password validation works
- [ ] OTP verification works
- [ ] Login succeeds with correct credentials
- [ ] Login fails with wrong password
- [ ] Token stored securely
- [ ] App remembers user on restart

#### Success Criteria
- User can fully complete auth flow
- Tokens stored and used for subsequent requests
- Error messages clear and helpful
- UI responsive on mobile (iOS + Android)

---

### Week 3: Search & Questions Screens

#### Goals
- Search interface with filters
- Question list view
- Question detail view with answer

#### Frontend Files to Create
```
connected_stack/frontend/
├── screens/
│   ├── SearchScreen.js (new)
│   ├── QuestionListScreen.js (new)
│   └── QuestionDetailScreen.js (new)
├── components/
│   ├── SearchBar.js (keyword search)
│   ├── FilterPanel.js (exam board, subject, topic)
│   ├── QuestionCard.js (list item)
│   └── AnswerDisplay.js (show answer/explanation)
├── hooks/
│   └── useSearch.js (search logic)
└── utils/
    └── question-formatter.js (format question text)
```

#### Tasks
1. Implement SearchScreen
   - Keyword search input
   - Filter by exam board
   - Filter by subject
   - Filter by topic
   - Filter by difficulty
   - Sort options (newest, difficulty, random)
   - Results count display
   - Loading state

2. Implement QuestionListScreen
   - Display search results
   - Scroll pagination
   - Question preview (first 100 chars)
   - Tap to open full question
   - Bookmark button

3. Implement QuestionDetailScreen
   - Full question text
   - All options (A, B, C, D)
   - User can select answer
   - Show/hide answer button
   - Explanation display
   - Navigation buttons (previous, next, back)
   - Bookmark toggle

4. Connect to API
   - Call `/api/questions/filters` on load
   - Call `/api/questions/search` with filters
   - Call `/api/questions/{id}` for details
   - Call `/api/questions/attempt` to log answer
   - Call `/api/user/bookmarks` for saved questions

#### Testing
- [ ] Search returns questions
- [ ] Filters work correctly
- [ ] Question details show correctly
- [ ] Can bookmark/unbookmark
- [ ] Pagination works
- [ ] Loading states display

#### Success Criteria
- Users can find questions easily
- Can filter by all criteria
- Question details clear and readable
- Bookmarks persist

---

## PHASE 3: Quiz & Progress (Week 4)

### Week 4: Quiz & Readiness Assessment

#### Goals
- Quiz mode (timed, multiple choice)
- Readiness assessment (15 questions)
- Progress dashboard

#### Frontend Files to Create
```
connected_stack/frontend/
├── screens/
│   ├── QuizStartScreen.js (new)
│   ├── QuizScreen.js (new)
│   ├── QuizResultsScreen.js (new)
│   ├── ReadinessScreen.js (new)
│   ├── ProgressScreen.js (new)
│   ├── WeakTopicsScreen.js (new)
│   └── BookmarksScreen.js (new)
├── components/
│   ├── Timer.js (countdown timer)
│   ├── ProgressBar.js (quiz progress)
│   ├── AccuracyChart.js (accuracy by subject)
│   ├── WeakTopicsList.js (topics to focus on)
│   └── StatCard.js (stat display)
└── hooks/
    └── useQuiz.js (quiz state management)
```

#### Tasks
1. Implement QuizScreen
   - Timer (configurable duration)
   - Question counter (1/15)
   - Question text and options
   - User selects answer
   - Next/previous buttons
   - Pause/resume
   - Exit confirmation

2. Implement ReadinessScreen
   - Start button
   - Dropdown to select exam board
   - Timer display (15 min)
   - Same Q&A flow as quiz
   - Submit assessment

3. Implement ProgressScreen
   - Overall accuracy percentage
   - Accuracy by subject (pie chart)
   - Accuracy by exam board (bar chart)
   - Attempt count
   - Learning streak
   - Time spent

4. Implement WeakTopicsScreen
   - List of weak topics (accuracy < 65%)
   - Accuracy for each topic
   - Number of attempts
   - Recommendation text
   - Link to practice those topics

5. Implement BookmarksScreen
   - List of bookmarked questions
   - Ability to remove bookmark
   - Ability to open and answer
   - Filter by subject/topic

#### Testing
- [ ] Quiz timer works
- [ ] Can answer all questions
- [ ] Results calculated correctly
- [ ] Progress stats accurate
- [ ] Readiness assessment functional
- [ ] Weak topics identified
- [ ] Bookmarks display correctly

#### Success Criteria
- Complete quiz without errors
- Progress data accurate
- Readiness assessment gives meaningful feedback
- Users can see weak areas clearly

---

## PHASE 4: Backend Enhancement (Week 5)

### Database Migration

#### Tasks
1. Set up PostgreSQL
   ```bash
   # Create database
   psql -c "CREATE DATABASE akulearn"
   
   # Install ORM
   pip install sqlalchemy psycopg2-binary alembic
   ```

2. Create database schema
   - Users table (from BACKEND_IMPLEMENTATION_GUIDE.md)
   - Attempts table
   - Assessments table
   - Bookmarks table
   - Add indices for performance

3. Migrate services to use SQLAlchemy
   - Replace in-memory dicts with ORM models
   - Update AuthService
   - Update ProgressService
   - Keep QuestionsService in-memory (read-only after initial load)

4. Create migration scripts
   - Export existing in-memory data to database
   - Verify data integrity
   - Test backward compatibility

#### Testing
- [ ] PostgreSQL running
- [ ] Schema created
- [ ] Data migrated
- [ ] All endpoints working
- [ ] Tests passing with new database

---

## PHASE 5: Performance & Caching (Week 6)

### Tasks
1. Set up Redis
   ```bash
   # Install Redis
   brew install redis  # macOS
   # or use Docker: docker run -d -p 6379:6379 redis:latest
   
   # Python client
   pip install redis
   ```

2. Implement caching
   - Cache question searches (10 min TTL)
   - Cache user progress calculations (5 min TTL)
   - Cache filter options (1 hour TTL)

3. Add response compression
   - Enable gzip in FastAPI
   - Compress all JSON responses

4. Load testing
   - Test with 100+ concurrent users
   - Measure response times
   - Identify bottlenecks
   - Optimize slow endpoints

#### Success Criteria
- Average response time <100ms
- Can handle 100+ concurrent users
- 90th percentile latency <500ms

---

## PHASE 6: Offline Support (Week 7)

### Tasks
1. Implement Service Worker (web/PWA)
   ```javascript
   // Intercept network requests
   // Cache API responses
   // Serve from cache when offline
   // Sync when back online
   ```

2. Implement local storage
   - Save progress locally
   - Queue offline actions
   - Sync on reconnection

3. Implement IndexedDB
   - Store question database locally
   - Enable offline quizzes
   - Sync with server

#### Success Criteria
- App works offline
- Quiz can be taken without internet
- Data syncs when reconnected
- No data loss

---

## PHASE 7: Deployment (Week 8)

### Tasks
1. Dockerize backend
   ```dockerfile
   FROM python:3.11
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. Set up Docker Compose
   ```yaml
   version: '3.8'
   services:
     backend:
       build: ./connected_stack/backend
       ports:
         - "8000:8000"
       environment:
         - DATABASE_URL=postgresql://user:pass@db:5432/akulearn
       depends_on:
         - db
     
     db:
       image: postgres:15
       environment:
         - POSTGRES_DB=akulearn
         - POSTGRES_USER=user
         - POSTGRES_PASSWORD=pass
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
   volumes:
     postgres_data:
   ```

3. Set up GitHub Actions CI/CD
   ```yaml
   # .github/workflows/deploy.yml
   - Run tests
   - Build Docker image
   - Push to registry
   - Deploy to AWS/Heroku
   ```

4. Deploy to cloud platform
   - Option 1: AWS (EC2, RDS, S3)
   - Option 2: Heroku (simple)
   - Option 3: Railway (modern)
   - Configure environment variables
   - Set up database backups

#### Success Criteria
- App runs in Docker
- CI/CD pipeline working
- Deployed to production
- Domain + SSL certificate

---

## PHASE 8: Testing & QA (Week 9)

### Tasks
1. Comprehensive testing
   - End-to-end tests (Cypress/Playwright)
   - API load testing (K6/JMeter)
   - Security testing (OWASP)
   - User acceptance testing (5-10 beta users)

2. Bug fixes
   - Document all issues
   - Prioritize by severity
   - Fix high-priority bugs
   - Re-test fixes

3. Performance optimization
   - Monitor server metrics
   - Optimize slow queries
   - Reduce bundle size
   - Improve load times

#### Success Criteria
- 95%+ test passing
- <1% error rate in production
- <100ms average response time
- App Store ready

---

## PHASE 9: Launch Preparation (Week 10-11)

### Tasks
1. Marketing
   - Create landing page
   - Social media presence
   - Beta user program
   - Press release

2. App store listings
   - Google Play Store (Android)
   - Apple App Store (iOS)
   - Web app listing

3. Documentation
   - User guides
   - Help/FAQ
   - Support system
   - Community forum

4. Monitoring
   - Set up Sentry for errors
   - Google Analytics
   - Crash reporting
   - Performance monitoring

#### Success Criteria
- App submitted to stores
- Landing page live
- 100+ beta users
- Support system ready

---

## PHASE 10: Launch Day (Week 12)

### Tasks
1. Final checks
   - All systems operational
   - Support team ready
   - Database backups configured
   - Monitoring active

2. Soft launch
   - Release to 1,000 users
   - Monitor for issues
   - Gather feedback
   - Fix critical bugs

3. Public launch
   - Announce on social media
   - Press outreach
   - Influencer partnerships
   - Marketing campaigns

4. Post-launch
   - Monitor user feedback
   - Fix reported issues
   - Track key metrics
   - Plan next features

#### Success Criteria
- 1,000+ users registered
- >80% positive reviews
- <1% crash rate
- <100ms average response time

---

## Key Metrics to Track

### User Metrics
- Total registered users
- Active daily users (DAU)
- Active weekly users (WAU)
- Retention rate
- Churn rate
- User feedback/ratings

### Product Metrics
- Questions answered
- Average accuracy
- Topics studied
- Time spent
- Assessments taken
- Pass probability

### Technical Metrics
- API response time
- Error rate
- Uptime %
- Database query time
- Cache hit rate
- Crash rate

### Business Metrics
- Cost per user acquisition
- Lifetime value
- Monthly active users (MAU)
- Engagement rate
- Conversion (freemium → premium)

---

## Resource Requirements

### Tools
- GitHub (code repository)
- PostgreSQL (database)
- Redis (caching)
- Docker (containerization)
- AWS/Heroku/Railway (hosting)
- Sentry (error tracking)
- DataDog/New Relic (monitoring)

### Team
- 1-2 Backend developers
- 1-2 Frontend developers
- 1 DevOps engineer
- 1 QA engineer
- 1 Product manager
- 1 Designer (optional)

### Budget (Estimate)
- Development: $30,000-50,000 (8-12 weeks)
- Infrastructure: $500-1,000/month
- Marketing: $5,000-10,000
- Total: $35,000-60,000 MVP

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Database performance | Medium | High | Load test early, optimize indices |
| User acquisition | High | High | Start with marketing early |
| Technical bugs | Medium | Medium | Comprehensive testing, CI/CD |
| Competition | Medium | Medium | Launch faster, focus on quality |
| Regulatory (Nigeria) | Low | High | Legal review, compliance check |

---

## Success Indicators

- ✅ 1,000+ users in first month
- ✅ 4.5+ star rating on app stores
- ✅ <1% daily crash rate
- ✅ >70% user retention after 1 week
- ✅ >80% accuracy by students
- ✅ Positive user feedback
- ✅ <100ms API response time
- ✅ 99.9% uptime

---

## Next Phase

**Start Week 2**: Frontend integration begins!

### Immediate Next Steps (This Week)
1. ✅ Approve backend implementation
2. ✅ Test all endpoints locally
3. ✅ Review API documentation
4. ✅ Assign frontend team

### Actions to Take
- [ ] Review BACKEND_IMPLEMENTATION_SUMMARY.md
- [ ] Run backend locally and test
- [ ] Review API_SPECIFICATION.md
- [ ] Start frontend planning
- [ ] Set up project management (Jira/Trello/GitHub Projects)

---

## Contact & Support

For questions about the roadmap:
1. Check `BACKEND_IMPLEMENTATION_GUIDE.md`
2. Review example code in `test_services.py`
3. Test endpoints at http://localhost:8000/docs
4. Read `PRODUCT_LAUNCH_STRATEGY.md` for business context

---

**Status**: Phase 1 Complete ✅  
**Current Focus**: Week 1 (Backend Foundation)  
**Next Phase**: Week 2-3 (Frontend Integration)  
**Target Launch**: Week 12 (90 days)  

**Generated**: December 12, 2025  
**Last Updated**: December 12, 2025
