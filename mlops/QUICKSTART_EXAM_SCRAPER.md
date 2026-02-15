# Exam Paper Scraper - Quick Reference Guide

## Quick Start

```bash
# Run the scraper
cd mlops
python exam_paper_scraper.py

# Load and use the data
python
>>> import json
>>> with open('../data/exam_papers/all_questions.json') as f:
...     questions = json.load(f)
>>> len(questions)
1350
```

## Data Access Examples

### Load All Questions
```python
import json

with open('data/exam_papers/all_questions.json') as f:
    all_questions = json.load(f)
```

### Load Questions by Subject
```python
with open('data/exam_papers/by_subject/mathematics.json') as f:
    math_questions = json.load(f)
```

### Load Questions by Topic
```python
with open('data/exam_papers/by_topic/algebra.json') as f:
    algebra_questions = json.load(f)
```

### Load Dataset Statistics
```python
with open('data/exam_papers/INDEX.json') as f:
    stats = json.load(f)
    
print(f"Total: {stats['total_questions']}")
print(f"Boards: {stats['exam_boards']}")
print(f"By Subject: {stats['by_subject']}")
```

## Filter Examples

### Get WAEC Mathematics Questions
```python
import json

with open('data/exam_papers/all_questions.json') as f:
    questions = json.load(f)

waec_math = [q for q in questions 
             if q['exam_board'] == 'WAEC' and q['subject'] == 'Mathematics']
print(f"Found {len(waec_math)} WAEC Mathematics questions")
```

### Get Questions from 2023
```python
questions_2023 = [q for q in questions if q['year'] == 2023]
print(f"Found {len(questions_2023)} questions from 2023")
```

### Get Hard Physics Questions
```python
hard_physics = [q for q in questions 
                if q['subject'] == 'Physics' and q['difficulty'] == 'hard']
print(f"Found {len(hard_physics)} hard physics questions")
```

### Get Questions by Topic and Year
```python
algebra_2024 = [q for q in questions 
                if q['topic'] == 'Algebra' and q['year'] == 2024]
```

## CSV Usage

### Read CSV with Pandas
```python
import pandas as pd

df = pd.read_csv('data/exam_papers/all_questions.csv')
print(df.shape)  # (1350, 11)

# Parse options column (pipe-delimited)
df['options_list'] = df['options'].str.split('|')

# Filter
math_df = df[df['subject'] == 'Mathematics']
```

### Read CSV with CSV Module
```python
import csv

with open('data/exam_papers/all_questions.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        options = row['options'].split('|')
        # Process row
```

## Dataset Statistics

| Metric | Value |
|--------|-------|
| Total Questions | 1,350 |
| Exam Boards | 3 (WAEC, NECO, JAMB) |
| Subjects | 4 (Math, Physics, English, Use of English) |
| Topics | 27 unique topics |
| Years | 5 (2020-2024) |
| Avg Questions/Topic | ~50 |
| Avg Questions/Subject | ~337 |
| Avg Questions/Year | 270 |

## File Locations

```
data/exam_papers/
├── all_questions.json          # 1350 questions (JSON)
├── all_questions.csv           # 1350 questions (CSV)
├── INDEX.json                  # Statistics & metadata
├── by_subject/
│   ├── mathematics.json        # 450 questions
│   ├── physics.json            # 450 questions
│   ├── english_language.json   # 300 questions
│   └── use_of_english.json     # 150 questions
└── by_topic/
    ├── algebra.json            # ~40-50 questions
    ├── geometry.json           # ~40-50 questions
    ├── trigonometry.json       # ~40-50 questions
    └── ... (24 more topics)
```

## Question Format

```json
{
  "id": "waec_math_2020_001",
  "exam_board": "WAEC",
  "subject": "Mathematics",
  "topic": "Algebra",
  "year": 2020,
  "question_number": 1,
  "question_text": "Sample question text",
  "options": ["Option A: ...", "Option B: ...", "Option C: ...", "Option D: ..."],
  "correct_answer": "A",
  "difficulty": "easy|medium|hard",
  "source_url": null,
  "created_at": "2025-12-10T16:22:08.712345",
  "explanation": null
}
```

## Common Operations

### Count Questions by Exam Board
```python
import json
from collections import Counter

with open('data/exam_papers/all_questions.json') as f:
    questions = json.load(f)

boards = Counter(q['exam_board'] for q in questions)
print(dict(boards))
# Output: {'WAEC': 450, 'NECO': 450, 'JAMB': 450}
```

### Distribution by Difficulty
```python
difficulty = Counter(q['difficulty'] for q in questions)
print(dict(difficulty))
```

### Get Random Question
```python
import random

question = random.choice(questions)
print(f"Q: {question['question_text']}")
print(f"Options: {question['options']}")
print(f"Answer: {question['correct_answer']}")
```

### Create Quiz from Dataset
```python
import random

def create_quiz(questions, num=10, subject=None):
    if subject:
        filtered = [q for q in questions if q['subject'] == subject]
    else:
        filtered = questions
    
    quiz = random.sample(filtered, min(num, len(filtered)))
    return quiz

quiz = create_quiz(questions, num=5, subject='Mathematics')
for i, q in enumerate(quiz, 1):
    print(f"{i}. {q['question_text']}")
    for opt in q['options']:
        print(f"   {opt}")
```

## Integration with Services

### AI Tutor Service
```python
# Use exam questions to train models
math_questions = [q for q in questions if q['subject'] == 'Mathematics']
# Feed to AI model for personalized tutoring
```

### Quiz Service
```python
# Generate quizzes from dataset
import random
quiz = random.sample(questions, 20)
# Return to frontend for quiz interaction
```

### Analytics Service
```python
# Track question difficulty trends
stats = {
    'easy': len([q for q in questions if q['difficulty'] == 'easy']),
    'medium': len([q for q in questions if q['difficulty'] == 'medium']),
    'hard': len([q for q in questions if q['difficulty'] == 'hard']),
}
```

## Performance Tips

1. **Cache loaded data**: Load once, reuse in memory
2. **Use generators for large files**: For streaming processing
3. **Index by subject/topic**: Use `by_subject/` and `by_topic/` files
4. **Batch processing**: Load topics instead of all questions
5. **Consider database**: For advanced queries (PostgreSQL/MongoDB)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| File not found | Run `python exam_paper_scraper.py` first |
| JSON decode error | Ensure valid UTF-8 encoding |
| Memory issues | Process in batches, use generators |
| Slow queries | Index data, use `by_subject/` files |

## Next Steps

1. **Extend to more subjects**: Add Chemistry, Biology, etc.
2. **Implement live scraping**: Replace demo with actual web scraping
3. **Add database**: Use MongoDB for faster queries
4. **Create API**: Build REST API for data access
5. **Add caching**: Redis for frequently accessed data

---

**For full documentation**: See `README_EXAM_SCRAPER.md`
