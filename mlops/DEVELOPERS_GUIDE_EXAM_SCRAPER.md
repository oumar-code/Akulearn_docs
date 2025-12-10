# Exam Paper Scraper - Developer's Guide

## Architecture Overview

### Design Pattern: Data Acquisition Pipeline

The exam paper scraper follows a modular pipeline architecture:

```
Input Source → Processing → Organization → Export → Output
     ↓           ↓             ↓            ↓         ↓
  Questions   Validation   By Subject    JSON     Files
  (Demo)      + IDs        By Topic      CSV      Index
              + Metadata   By Year       Files    Stats
```

## Class Structure

### ExamPaperScraper

```python
class ExamPaperScraper:
    """Main class managing the complete data acquisition pipeline"""
    
    # Core attributes
    questions: List[ExamQuestion]      # Storage for questions
    output_dir: Path                   # Output directory
    
    # Core methods
    def generate_questions()            # Create exam questions
    def organize_by_subject()           # Sort by subject
    def organize_by_topic()             # Sort by topic
    def save_as_json()                  # Export JSON
    def save_as_csv()                   # Export CSV
    def create_index()                  # Generate metadata
```

### ExamQuestion

```python
@dataclass
class ExamQuestion:
    id: str                    # Unique identifier
    exam_board: str            # WAEC/NECO/JAMB
    subject: str               # Subject name
    topic: str                 # Topic name
    year: int                  # Year of exam
    question_number: int       # Question number
    question_text: str         # Question content
    options: List[str]         # Multiple choice options
    correct_answer: str        # Correct option (A-D)
    difficulty: str            # easy/medium/hard
    source_url: Optional[str]  # Original source
    created_at: str            # Timestamp
    explanation: Optional[str] # Answer explanation
```

## Data Flow

### 1. Generation Phase
```python
# Current: Demo Mode (Synthetic)
for board in EXAM_BOARDS:
    for subject in board['subjects']:
        for year in board['years']:
            questions = generate_synthetic_questions(
                board, subject, year, count=30
            )

# Future: Live Scraping
def scrape_live(exam_board, subject, year):
    url = URL_PATTERN.format(board=exam_board, subject=subject, year=year)
    response = requests.get(url)
    questions = parse_html_or_pdf(response.content)
    return questions
```

### 2. Processing Phase
```python
# Validation
for q in questions:
    assert q.question_text is not None
    assert len(q.options) == 4
    assert q.correct_answer in ['A', 'B', 'C', 'D']

# ID Generation
q.id = f"{board}_{subject}_{year}_{number}".lower()

# Timestamp
q.created_at = datetime.now().isoformat()
```

### 3. Organization Phase
```python
# By Subject
by_subject = defaultdict(list)
for q in questions:
    by_subject[q.subject].append(q)

# By Topic (nested by subject)
by_topic = defaultdict(lambda: defaultdict(list))
for q in questions:
    by_topic[q.subject][q.topic].append(q)
```

### 4. Export Phase
```python
# JSON (easy to parse, maintains structure)
json.dump(questions, file)

# CSV (spreadsheet compatible, tabular)
csv.DictWriter.writerows(questions)

# Index (metadata and statistics)
index = {
    'total_questions': len(questions),
    'exam_boards': [...],
    'by_exam_board': {...},
    # ... etc
}
```

## Extension Points

### 1. Add New Exam Board

```python
# Step 1: Update EXAM_BOARDS
EXAM_BOARDS['NBUTEB'] = {
    'subjects': ['Technical Drawing', 'Metalwork', ...],
    'years': list(range(2014, 2025)),
    'url_pattern': 'https://...'
}

# Step 2: Add subject topics
SUBJECT_TOPICS['Technical Drawing'] = [
    'Orthographic Projection', 'Isometric Projection', ...
]

# Step 3: Run scraper
scraper.scrape_board('NBUTEB')
```

### 2. Add New Subject

```python
# Update existing board
EXAM_BOARDS['WAEC']['subjects'].append('Further Mathematics')

# Add topics
SUBJECT_TOPICS['Further Mathematics'] = [
    'Complex Numbers', 'Matrices', 'Calculus', ...
]
```

### 3. Implement Live Scraping

Replace `generate_questions()` with actual scraping:

```python
def scrape_questions(self, exam_board, subject, year):
    """Scrape from actual exam board website"""
    
    url = EXAM_BOARDS[exam_board]['url_pattern'].format(
        subject=subject, year=year
    )
    
    # Fetch page
    response = requests.get(url)
    response.raise_for_status()
    
    # Parse HTML/PDF
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract questions
    questions = []
    for item in soup.find_all('div', class_='question'):
        q = self.parse_question(item)
        questions.append(q)
    
    return questions

def parse_question(self, element):
    """Parse HTML element into ExamQuestion"""
    text = element.find('span', class_='text').get_text()
    options = [opt.get_text() for opt in element.find_all('span', class_='option')]
    answer = element.find('input', class_='answer')['value']
    
    return ExamQuestion(
        id=element.get('data-id'),
        question_text=text,
        options=options,
        correct_answer=answer,
        # ... etc
    )
```

### 4. Add Data Enrichment

```python
def enrich_with_explanations(self):
    """Add explanations from external source"""
    for q in self.questions:
        explanation = fetch_explanation(q.id)
        q.explanation = explanation

def calculate_difficulty(self):
    """Calculate difficulty from historical data"""
    for q in self.questions:
        success_rate = get_success_rate(q.id)
        if success_rate > 0.8:
            q.difficulty = 'easy'
        elif success_rate > 0.5:
            q.difficulty = 'medium'
        else:
            q.difficulty = 'hard'
```

## Integration Examples

### Quiz Service Integration

```python
# quiz_service.py
from exam_paper_scraper import ExamPaperScraper
import json

class QuizService:
    def __init__(self):
        with open('data/exam_papers/all_questions.json') as f:
            self.questions = json.load(f)
    
    def create_quiz(self, subject, num_questions=10):
        """Create quiz from dataset"""
        filtered = [q for q in self.questions 
                   if q['subject'] == subject]
        import random
        return random.sample(filtered, num_questions)
    
    def get_question_by_topic(self, subject, topic):
        """Get questions by topic"""
        return [q for q in self.questions 
                if q['subject'] == subject and q['topic'] == topic]
```

### AI Tutor Integration

```python
# ai_tutor_service.py
import json
from sklearn.feature_extraction.text import TfidfVectorizer

class AITutor:
    def __init__(self):
        with open('data/exam_papers/all_questions.json') as f:
            self.questions = json.load(f)
        
        # Vectorize for similarity
        texts = [q['question_text'] for q in self.questions]
        self.vectorizer = TfidfVectorizer()
        self.vectors = self.vectorizer.fit_transform(texts)
    
    def find_similar_questions(self, question_text):
        """Find similar questions for tutoring"""
        vector = self.vectorizer.transform([question_text])
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity(vector, self.vectors)[0]
        indices = similarities.argsort()[-5:][::-1]
        return [self.questions[i] for i in indices]
```

### Analytics Integration

```python
# analytics_service.py
import json
from collections import Counter

class ExamAnalytics:
    def __init__(self):
        with open('data/exam_papers/INDEX.json') as f:
            self.index = json.load(f)
    
    def get_topic_distribution(self, subject):
        """Get distribution by topic"""
        with open(f'data/exam_papers/by_subject/{subject.lower()}.json') as f:
            questions = json.load(f)
        
        topics = Counter(q['topic'] for q in questions)
        return dict(topics)
    
    def get_difficulty_distribution(self):
        """Get difficulty distribution"""
        with open('data/exam_papers/all_questions.json') as f:
            questions = json.load(f)
        
        return {
            'easy': len([q for q in questions if q['difficulty'] == 'easy']),
            'medium': len([q for q in questions if q['difficulty'] == 'medium']),
            'hard': len([q for q in questions if q['difficulty'] == 'hard']),
        }
```

## Testing

### Unit Tests

```python
# test_exam_paper_scraper.py
import pytest
from exam_paper_scraper import ExamPaperScraper, ExamQuestion

def test_question_creation():
    """Test ExamQuestion creation"""
    q = ExamQuestion(
        id='test_1',
        exam_board='WAEC',
        subject='Mathematics',
        topic='Algebra',
        year=2020,
        question_number=1,
        question_text='Test question',
        options=['A', 'B', 'C', 'D'],
        correct_answer='A',
        difficulty='easy',
        source_url=None,
        created_at='2025-12-10',
        explanation=None
    )
    assert q.exam_board == 'WAEC'
    assert len(q.options) == 4

def test_scraper_initialization():
    """Test scraper initialization"""
    scraper = ExamPaperScraper()
    assert scraper.output_dir.exists()
    assert len(scraper.questions) == 0

def test_question_generation():
    """Test question generation"""
    scraper = ExamPaperScraper()
    scraper.generate_data()
    assert len(scraper.questions) > 0
```

### Integration Tests

```python
def test_json_export():
    """Test JSON export"""
    scraper = ExamPaperScraper()
    scraper.generate_data()
    path = scraper.save_as_json()
    
    import json
    with open(path) as f:
        data = json.load(f)
    
    assert len(data) == len(scraper.questions)

def test_csv_export():
    """Test CSV export"""
    scraper = ExamPaperScraper()
    scraper.generate_data()
    path = scraper.save_as_csv()
    
    import csv
    with open(path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == len(scraper.questions)
```

## Performance Optimization

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=10)
def load_subject_questions(subject):
    """Cache loaded questions by subject"""
    import json
    with open(f'data/exam_papers/by_subject/{subject.json}') as f:
        return json.load(f)
```

### Batch Processing

```python
def process_in_batches(questions, batch_size=100):
    """Process large datasets in batches"""
    for i in range(0, len(questions), batch_size):
        batch = questions[i:i+batch_size]
        yield batch
```

### Database Integration

```python
# For production: use database instead of JSON files
from pymongo import MongoClient

class QuestionDB:
    def __init__(self, db_url):
        self.client = MongoClient(db_url)
        self.db = self.client['exams']
        self.collection = self.db['questions']
    
    def insert_questions(self, questions):
        """Insert questions into database"""
        self.collection.insert_many([q.to_dict() for q in questions])
    
    def find_by_subject(self, subject):
        """Query by subject"""
        return list(self.collection.find({'subject': subject}))
```

## Best Practices

1. **Error Handling**: Always use try-except for file I/O
2. **Logging**: Log important operations for debugging
3. **Type Hints**: Use type hints for better IDE support
4. **Documentation**: Document public methods and classes
5. **Testing**: Write tests for critical functionality
6. **Validation**: Validate data before processing
7. **Caching**: Cache frequently accessed data
8. **Modularity**: Keep functions small and focused

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| File not found | Ensure output directory exists |
| JSON decode error | Check UTF-8 encoding |
| CSV fieldnames mismatch | Filter dict to only include defined fields |
| Memory issues | Process in batches or use generators |
| Slow queries | Index data or use database |

## Performance Metrics

- **Generation**: ~2-3 seconds for 1,350 questions
- **Export (JSON)**: ~0.1 seconds
- **Export (CSV)**: ~0.1 seconds
- **Index Creation**: ~0.05 seconds
- **Total Runtime**: ~3-4 seconds

---

**For Production Use**: See integration guides in documentation.
