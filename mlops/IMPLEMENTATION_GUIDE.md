# Implementation Guide: Building AI Agents for Exam Content Generation

## Quick Start (Next 2 Weeks)

This guide walks you through implementing the AIops strategy for WAEC, NECO, JAMB content generation using Google tools and Hugging Face.

---

## Week 1: Foundation & Data Pipeline

### Day 1-2: Setup & Account Creation

```bash
# 1. Create Google Account (if not already)
# - Visit https://notebook.google.com (Notebook LM)
# - Visit https://aistudio.google.com (Google AI Studio)
# - Enable APIs in Google Cloud Console

# 2. Set up Hugging Face
# - Create account at https://huggingface.co
# - Generate token: Settings → Access Tokens
# - Save token: huggingface_hub.login()

# 3. Install dependencies locally
pip install google-auth-oauthlib google-cloud-aiplatform
pip install huggingface-hub transformers datasets accelerate
pip install langchain langchain-community ollama
```

### Day 3-4: Data Collection & Organization

```python
# Create a structured data collection script
# File: mlops/data_collection.py

import json
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class ExamPaper:
    """Structured exam paper"""
    exam_board: str  # waec, neco, jamb
    year: int
    subject: str
    questions: list  # List of questions with answers
    source_url: str
    
def collect_exam_papers():
    """
    Collect past papers from official sources
    
    WAEC: https://waeconline.org.ng/
    NECO: https://necoobjective.com.ng/
    JAMB: https://www.jamb.org.ng/
    """
    
    # Download PDFs, parse into structured format
    pass

def organize_by_topic():
    """Organize questions by subject and topic"""
    
    topic_mapping = {
        "mathematics": [
            "algebra", "geometry", "calculus", 
            "trigonometry", "statistics", "probability"
        ],
        "physics": [
            "mechanics", "thermodynamics", "waves_optics",
            "electricity_magnetism", "modern_physics"
        ],
        "chemistry": [
            "organic", "inorganic", "physical_chemistry",
            "analytical_chemistry"
        ],
        "biology": [
            "cell_biology", "genetics", "ecology",
            "human_physiology", "botany", "zoology"
        ],
        "english": [
            "literature", "grammar", "comprehension",
            "vocabulary", "essay_writing"
        ]
    }
    
    return topic_mapping

# Run data collection
papers = collect_exam_papers()
topics = organize_by_topic()
```

**Deliverable**: `data/exam_papers/` directory with organized JSON files

### Day 5-7: Google Notebook LM Setup

```bash
# Step 1: Upload textbooks to Notebook LM
# Go to https://notebooklm.google.com
# Click "Create notebook"
# Upload PDFs of textbooks for key subjects:
#   - Mathematics (OAU prep guide)
#   - Physics (JAMB recommended texts)
#   - Chemistry (NECO syllabus materials)
#   - Biology (Cambridge IGCSE)
#   - English (WAEC recommended texts)

# Step 2: Generate audio guides
# - Select chapters/topics
# - Generate study guide
# - Generate podcast
# - Download MP3 files

# Step 3: Organize audio assets
# File structure:
# assets/audio/
#   └── subject/
#       └── topic/
#           ├── study_guide.mp3
#           └── podcast.mp3
```

**Deliverable**: Audio files organized by subject/topic

---

## Week 2: Question Generation & Validation

### Day 1-2: Set Up Question Generation

```python
# File: mlops/advanced_question_generator.py

from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import hf_hub_download
import langchain
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class AdvancedQuestionGenerator:
    """Generate exam questions using fine-tuned models"""
    
    def __init__(self):
        # Load a model suitable for question generation
        # Option 1: Fine-tuned GPT-2 on exam questions
        # Option 2: T5 model fine-tuned for QA
        # Option 3: LLaMA 2 via Ollama (local)
        
        self.model_id = "gpt2"  # Replace with fine-tuned version
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id)
    
    def generate_questions_from_topic(self, subject, topic, difficulty, count=10):
        """
        Generate questions for a specific topic
        
        Args:
            subject: e.g., "mathematics"
            topic: e.g., "quadratic_equations"
            difficulty: "easy", "medium", "hard"
            count: number of questions to generate
        
        Returns:
            list of Question objects
        """
        
        prompt_template = f"""
        You are an expert Nigerian secondary school educator creating {difficulty} exam questions.
        Generate {count} multiple-choice questions about {subject}: {topic}
        
        For WAEC/NECO/JAMB exams, create questions that:
        1. Test conceptual understanding
        2. Include practical applications
        3. Have diverse question types
        4. Cover different difficulty aspects of the topic
        
        Format: 
        Question 1: [text]
        A) [option]
        B) [option]
        C) [option]
        D) [option]
        Answer: [A/B/C/D]
        """
        
        # Generate using the model
        pass
    
    def refine_with_google_ai_studio(self, question, prompts_api_key):
        """
        Refine a generated question using Google AI Studio
        Improves clarity and relevance
        """
        
        import anthropic  # or use google generativeai
        
        refinement_prompt = f"""
        Review this exam question for clarity, correctness, and relevance:
        
        {question}
        
        Provide:
        1. Quality score (0-100)
        2. Suggested improvements
        3. Refined version if needed
        """
        
        # Call Google API or Claude API
        pass

# Usage
generator = AdvancedQuestionGenerator()
questions = generator.generate_questions_from_topic(
    subject="mathematics",
    topic="quadratic_equations",
    difficulty="medium",
    count=20
)
```

**Deliverable**: `mlops/advanced_question_generator.py`

### Day 3-5: Build Validation Pipeline

```python
# File: mlops/content_validation.py

from transformers import pipeline
import re

class AdvancedValidator:
    """Advanced validation of generated content"""
    
    def __init__(self):
        # Load models for various checks
        self.toxicity_classifier = pipeline("zero-shot-classification")
        self.qa_validator = pipeline("question-answering")
        self.similarity_model = pipeline("feature-extraction")
    
    def validate_question_comprehensive(self, question):
        """Multi-level validation"""
        
        checks = {
            "format_valid": self._check_format(question),
            "no_toxicity": self._check_toxicity(question),
            "answer_reasonable": self._check_answer(question),
            "syllabus_alignment": self._check_alignment(question),
            "uniqueness": self._check_uniqueness(question),
            "clarity_score": self._score_clarity(question),
        }
        
        overall_score = sum(
            1 for v in checks.values() 
            if v.get("passed", False)
        ) / len(checks)
        
        return {
            "question_id": question.id,
            "passed": overall_score > 0.8,
            "overall_score": overall_score,
            "checks": checks
        }
    
    def _check_format(self, question):
        """Check if question has proper format"""
        has_text = len(question.question_text) > 10
        has_options = len(question.options) == 4
        has_answer = question.correct_answer in question.options
        
        return {
            "passed": has_text and has_options and has_answer,
            "details": {
                "text_length": len(question.question_text),
                "option_count": len(question.options),
                "answer_in_options": has_answer
            }
        }
    
    def _check_toxicity(self, question):
        """Check for harmful or biased content"""
        
        combined_text = (
            question.question_text + " " +
            " ".join(question.options)
        )
        
        labels = ["toxic", "respectful", "educational"]
        result = self.toxicity_classifier(combined_text, labels)
        
        is_safe = result['labels'][0] != "toxic"
        
        return {
            "passed": is_safe,
            "confidence": result['scores'][0]
        }
    
    def _check_alignment(self, question):
        """Check alignment with exam syllabus"""
        
        syllabus_keywords = {
            "mathematics": ["equation", "formula", "calculate", "solve"],
            "physics": ["force", "energy", "motion", "acceleration"],
            "chemistry": ["reaction", "compound", "element", "bonding"],
            "biology": ["cell", "organism", "genetics", "evolution"],
        }
        
        keywords = syllabus_keywords.get(question.subject, [])
        text = question.question_text.lower()
        
        aligned = any(kw in text for kw in keywords)
        
        return {
            "passed": aligned,
            "matched_keywords": [kw for kw in keywords if kw in text]
        }
    
    def _check_uniqueness(self, question):
        """Check against existing questions"""
        
        # Compare with stored questions
        # Return uniqueness score
        
        return {
            "passed": True,
            "uniqueness_score": 0.95
        }
    
    def _check_answer(self, question):
        """Validate answer is reasonable"""
        
        return {
            "passed": len(question.correct_answer) > 0,
            "answer_length": len(question.correct_answer)
        }
    
    def _score_clarity(self, question):
        """Score question clarity (0-100)"""
        
        # Factors: length, vocabulary complexity, sentence structure
        words = question.question_text.split()
        avg_word_length = sum(len(w) for w in words) / len(words)
        
        # Ideal: 4-6 character average word length
        clarity = 100 if 4 <= avg_word_length <= 6 else 70
        
        return {
            "passed": clarity > 75,
            "clarity_score": clarity
        }

# Usage
validator = AdvancedValidator()
validation_result = validator.validate_question_comprehensive(question)
print(validation_result)
```

**Deliverable**: `mlops/content_validation.py`

### Day 6-7: Integration & Testing

```python
# File: mlops/test_integration.py

import pytest
from exam_content_generator import ExamContentOrchestrator, GenerationRequest, ExamBoard, Difficulty

def test_waec_question_generation():
    """Test WAEC question generation"""
    
    orchestrator = ExamContentOrchestrator()
    request = GenerationRequest(
        exam_board=ExamBoard.WAEC,
        subject="mathematics",
        topic="algebra",
        difficulty=Difficulty.MEDIUM,
        question_count=5
    )
    
    result = orchestrator.generate_content_batch(request)
    
    assert len(result['generated']) == 5
    assert all(q.exam_board == ExamBoard.WAEC for q in result['validated'])
    assert result['validation_report']['pass_rate'] > 0.7

def test_neco_question_generation():
    """Test NECO question generation"""
    
    orchestrator = ExamContentOrchestrator()
    request = GenerationRequest(
        exam_board=ExamBoard.NECO,
        subject="biology",
        topic="photosynthesis",
        difficulty=Difficulty.EASY,
        question_count=5
    )
    
    result = orchestrator.generate_content_batch(request)
    
    assert len(result['generated']) == 5
    assert all(q.exam_board == ExamBoard.NECO for q in result['validated'])

def test_jamb_question_generation():
    """Test JAMB question generation"""
    
    orchestrator = ExamContentOrchestrator()
    request = GenerationRequest(
        exam_board=ExamBoard.JAMB,
        subject="chemistry",
        topic="periodic_table",
        difficulty=Difficulty.HARD,
        question_count=5
    )
    
    result = orchestrator.generate_content_batch(request)
    
    assert len(result['generated']) == 5
    assert all(q.exam_board == ExamBoard.JAMB for q in result['validated'])

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**Deliverable**: Working test suite, validated questions database

---

## Beyond Week 2: Scale & Production

### Week 3-4: MLflow Tracking & API Deployment

```python
# File: mlops/deploy_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from exam_content_generator import ExamContentOrchestrator, GenerationRequest
import mlflow

app = FastAPI(title="Exam Content API")
orchestrator = ExamContentOrchestrator()

class ContentRequest(BaseModel):
    exam_board: str
    subject: str
    topic: str
    difficulty: str
    count: int

@app.post("/generate-content")
async def generate_content(request: ContentRequest):
    """Generate exam content on demand"""
    
    try:
        gen_request = GenerationRequest(
            exam_board=request.exam_board,
            subject=request.subject,
            topic=request.topic,
            difficulty=request.difficulty,
            question_count=request.count
        )
        
        result = orchestrator.generate_content_batch(gen_request)
        
        return {
            "status": "success",
            "generated": len(result['generated']),
            "valid": len(result['validated']),
            "pass_rate": result['validation_report']['pass_rate'],
            "questions": [q.to_dict() for q in result['validated']]
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Deploy
# uvicorn deploy_api:app --host 0.0.0.0 --port 8001
```

### Week 4-5: Auto-Scaling & CI/CD

```yaml
# File: .github/workflows/content-generation.yml

name: Daily Content Generation

on:
  schedule:
    - cron: '0 2 * * *'  # Run daily at 2 AM
  workflow_dispatch:

jobs:
  generate-content:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Generate WAEC content
        run: |
          python -m mlops.exam_content_generator \
            --exam waec --subject mathematics --count 50
      
      - name: Generate NECO content
        run: |
          python -m mlops.exam_content_generator \
            --exam neco --subject biology --count 50
      
      - name: Generate JAMB content
        run: |
          python -m mlops.exam_content_generator \
            --exam jamb --subject chemistry --count 50
      
      - name: Validate all content
        run: |
          python mlops/validate_batch.py
      
      - name: Upload to database
        run: |
          python mlops/upload_to_db.py
      
      - name: Commit and push
        run: |
          git add runs/
          git commit -m "feat: auto-generated exam content $(date +%Y-%m-%d)"
          git push
```

---

## Success Metrics (Track These)

- **Content Generated**: Target 100+ questions/day
- **Quality Score**: Target avg >0.85
- **Relevance**: Target >95% alignment with syllabus
- **Uniqueness**: Target >90% unique vs past papers
- **API Response Time**: Target <1s
- **Cost**: Target <$0.01 per question

---

## Files to Create This Week

```
mlops/
├── exam_content_generator.py          ✅ DONE
├── advanced_question_generator.py     TODO Week 2
├── content_validation.py              TODO Week 2
├── deploy_api.py                      TODO Week 3
├── exam_content_demo.ipynb            ✅ DONE
├── data_collection.py                 TODO Week 1
└── requirements_aiops.txt             TODO
```

---

## Resources

- **Google Notebook LM**: https://notebook.google.com
- **Google AI Studio**: https://aistudio.google.com
- **Hugging Face**: https://huggingface.co
- **LangChain**: https://python.langchain.com
- **MLflow**: https://mlflow.org

## Next Meeting: Review progress on Week 1 data collection

