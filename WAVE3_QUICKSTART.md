# Wave 3 Quick Start Guide

Complete step-by-step guide to run all Wave 3 advanced features.

## 🚀 Quick Setup (5 Minutes)

### Option 1: Automated Integration (Recommended)

```bash
# Run the full integration script
python wave3_full_integration.py
```

This will verify all components and show you what's implemented.

### Option 2: Manual Step-by-Step

Follow these steps to implement everything:

## 📋 Prerequisites

1. **Python Environment**
   ```bash
   # Verify Python virtual environment is activated
   # Should see (myenv) or (base) in your prompt
   ```

2. **Dependencies Installed**
   ```bash
   pip install -r requirements.txt
   ```

3. **Neo4j Running** (Optional but recommended)
   ```bash
   docker-compose -f docker-compose-neo4j.yaml up -d
   ```

## 🎯 Implementation Steps

### Step 1: Ingest Wave 3 Lessons into Neo4j

```bash
python wave3_knowledge_graph_integration.py
```

**Expected Output:**
- 21 lessons ingested
- ~927 nodes created
- ~936 relationships created

**Files Required:** `rendered_lessons/lesson_*.json`

### Step 2: Create Cross-Subject Connections

```bash
python cross_subject_expander.py
```

**What This Does:**
- Creates 15 interdisciplinary connections
- Generates 6 thematic learning paths
- Maps 6 transferable skills across lessons

**Output:** Extended connections in Neo4j graph

### Step 3: Generate Visualizations

```bash
python wave3_visualizer.py
```

**Generates:**
- `visualizations/knowledge_graph.html` - Interactive network
- `visualizations/subject_heatmap.html` - Connection matrix
- `visualizations/pathway_*.html` - Learning path diagrams

**View:** Open HTML files in your browser

### Step 4: Start REST API Server

**Option A: Using the batch file (Windows)**
```bash
start_api.bat
```

**Option B: Direct Python**
```bash
python wave3_rest_api.py --port 8000
```

**Option C: Using uvicorn**
```bash
uvicorn wave3_rest_api:app --host 127.0.0.1 --port 8000 --reload
```

**Access API Documentation:**
- Open browser: http://localhost:8000/api/docs
- Interactive Swagger UI with all endpoints

### Step 5: Use the Interactive Dashboard

```bash
python wave3_interactive_dashboard.py
```

**Features:**
- Browse lessons by subject
- Search by NERDC codes, WAEC topics, keywords
- Track student progress
- Export lessons for teachers

## 🌐 API Endpoints Overview

Once the server is running, you can access:

### Core Endpoints

```bash
# Health check
GET http://localhost:8000/api/health

# Get all subjects
GET http://localhost:8000/api/subjects

# Get lessons for a subject
GET http://localhost:8000/api/subjects/Chemistry/lessons

# Get specific lesson
GET http://localhost:8000/api/lessons/lesson_01_atomic_structure_and_chemical_bonding
```

### Search Endpoints

```bash
# Search by NERDC code
GET http://localhost:8000/api/search/nerdc/SS1.CHEM

# Search by WAEC topic
GET http://localhost:8000/api/search/waec/Atomic%20Structure

# Keyword search
GET http://localhost:8000/api/search/keyword/electron
```

### Progress Tracking

```bash
# Submit quiz result
POST http://localhost:8000/api/progress/quiz
Content-Type: application/json
{
  "quiz_id": "quiz_001",
  "student_id": "STU001",
  "lesson_id": "lesson_01_...",
  "score": 8.5,
  "max_score": 10.0,
  "time_taken_seconds": 600,
  "questions_correct": 17,
  "questions_total": 20
}

# Get student progress
GET http://localhost:8000/api/progress/student/STU001

# Get recommendations
GET http://localhost:8000/api/progress/student/STU001/recommendations
```

### Learning Paths

```bash
# List all learning paths
GET http://localhost:8000/api/learning-paths

# Get specific path
GET http://localhost:8000/api/learning-paths/path_environmental_science

# Get path recommendations for student
GET http://localhost:8000/api/learning-paths/student/STU001/recommendations
```

## 📊 Using the Features

### For Students

```python
from enhanced_progress_tracker import EnhancedProgressTracker, QuizResult, LearningActivity, ActivityType
from datetime import datetime

tracker = EnhancedProgressTracker()

# Record a quiz
quiz = QuizResult(
    quiz_id="quiz_001",
    lesson_id="lesson_01_atomic_structure_and_chemical_bonding",
    student_id="STU001",
    score=8.5,
    max_score=10.0,
    time_taken_seconds=600,
    questions_correct=17,
    questions_total=20,
    timestamp=datetime.now().isoformat()
)
tracker.record_quiz_result(quiz)

# Record study session
activity = LearningActivity(
    activity_id="act_001",
    student_id="STU001",
    lesson_id="lesson_01_atomic_structure_and_chemical_bonding",
    activity_type=ActivityType.CONTENT_READ,
    duration_seconds=1800,  # 30 minutes
    timestamp=datetime.now().isoformat()
)
tracker.record_learning_activity(activity)

# Check mastery
metrics = tracker.calculate_mastery_metrics("STU001", "lesson_01_...")
print(f"Mastery: {metrics.mastery_level.value} ({metrics.mastery_percentage}%)")

# Get recommendations
recommendations = tracker.recommend_next_lessons("STU001", count=5)
for rec in recommendations:
    print(f"- {rec['title']} ({rec['reason']})")
```

### For Teachers

```python
from wave3_interactive_dashboard import Wave3Dashboard

dashboard = Wave3Dashboard()

# Get class overview
subjects = dashboard.get_subjects_overview()

# Export lesson for teaching
lesson_export = dashboard.export_lesson_for_teacher(
    "lesson_01_atomic_structure_and_chemical_bonding"
)

# Track student progress
progress = dashboard.get_student_progress("STU001")
```

### Using the API (JavaScript/Frontend)

```javascript
// Fetch all subjects
const subjects = await fetch('http://localhost:8000/api/subjects')
  .then(r => r.json());

// Search for lessons
const results = await fetch('http://localhost:8000/api/search/keyword/atom')
  .then(r => r.json());

// Submit quiz result
const quizResult = await fetch('http://localhost:8000/api/progress/quiz', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    quiz_id: 'quiz_001',
    student_id: 'STU001',
    lesson_id: 'lesson_01_atomic_structure_and_chemical_bonding',
    score: 8.5,
    max_score: 10.0,
    time_taken_seconds: 600,
    questions_correct: 17,
    questions_total: 20
  })
}).then(r => r.json());

// Get student progress
const progress = await fetch('http://localhost:8000/api/progress/student/STU001')
  .then(r => r.json());
```

## 🐛 Troubleshooting

### Neo4j Connection Issues

If Neo4j is not available, the system will fall back to filesystem mode:

```bash
# Check if Neo4j is running
docker ps | grep neo4j

# Start Neo4j
docker-compose -f docker-compose-neo4j.yaml up -d

# Check Neo4j logs
docker logs akulearn-neo4j
```

### API Server Not Starting

```bash
# Check if port 8000 is already in use
netstat -ano | findstr :8000

# Try a different port
python wave3_rest_api.py --port 8001

# Check for import errors
python -c "import wave3_rest_api; print('OK')"
```

### Missing Dependencies

```bash
# Reinstall requirements
pip install -r requirements.txt --upgrade

# Check specific packages
pip show neo4j fastapi uvicorn plotly networkx
```

## 📚 Documentation

- **[WAVE3_INTEGRATION_GUIDE.md](WAVE3_INTEGRATION_GUIDE.md)** - Initial Neo4j integration
- **[WAVE3_ADVANCED_FEATURES.md](WAVE3_ADVANCED_FEATURES.md)** - Complete feature documentation
- **[API_SPECIFICATION.md](API_SPECIFICATION.md)** - Original API specification

## 🎯 What's Implemented

✅ **Enhanced Progress Tracking**
- 6-level mastery system (Not Started → Mastered)
- Quiz result integration with detailed scoring
- Time-on-task analytics (9 activity types)
- Weighted mastery calculation (quiz 50%, problems 40%, engagement 10%)
- Intelligent lesson recommendations

✅ **Cross-Subject Connections**
- 15 interdisciplinary links (up from 6)
- 6 thematic learning paths
- 6 transferable skill networks
- Connection strength weighting

✅ **REST API**
- 30+ endpoints organized by category
- Complete CRUD operations
- Multi-mode search (NERDC, WAEC, keywords)
- Progress tracking and analytics
- Learning path recommendations
- Teacher exports
- OpenAPI documentation

✅ **Visualizations**
- Interactive knowledge graphs (Plotly)
- Learning pathway diagrams
- Student progress dashboards (4-panel view)
- Time analytics charts
- Subject connection heatmaps

✅ **Knowledge Graph**
- 927 nodes (21 lessons + components)
- 936 relationships
- Neo4j integration with fallback mode
- Curriculum alignment (NERDC + WAEC)

## 🚀 Next Steps

1. **Mobile Integration**
   - Implement WebSocket for real-time updates
   - Add offline sync endpoints
   - Push notification preparation

2. **GraphQL Endpoint**
   - Add GraphQL schema
   - Flexible querying

3. **Advanced Analytics**
   - Predictive mastery modeling
   - At-risk student identification
   - Optimal study time recommendations

4. **Gamification**
   - Achievements and badges
   - Leaderboards
   - Streak tracking

---

**Need Help?** Check the documentation files or run:
```bash
python wave3_full_integration.py
```

This will verify your setup and show what's working!
