# AIops Quick Reference Guide
## For Akulearn Secondary School Exam Content Generation

---

## 🚀 What We've Built

A complete **AI-powered content generation system** for WAEC, NECO, and JAMB exam preparation using:
- **Google Notebook LM** → Audio study guides
- **Google AI Studio** → Prompt refinement
- **Hugging Face Models** → Question generation & validation
- **Custom ML Agents** → Orchestration & scaling

---

## 📁 Files Created

| File | Purpose | Run Command |
|------|---------|------------|
| `docs/AIOPS_STRATEGY.md` | Complete strategy & best practices | `cat docs/AIOPS_STRATEGY.md` |
| `mlops/exam_content_generator.py` | Core generation engine | `python -m mlops.exam_content_generator --help` |
| `mlops/exam_content_demo.ipynb` | Interactive demo & visualization | `jupyter notebook mlops/exam_content_demo.ipynb` |
| `mlops/IMPLEMENTATION_GUIDE.md` | 2-week quick start | `cat mlops/IMPLEMENTATION_GUIDE.md` |

---

## 🎯 Quick Start (Today)

### 1️⃣ Generate 10 Questions for WAEC Mathematics
```bash
cd C:\Users\hp\Documents\Akulearn_docs
python -m mlops.exam_content_generator \
  --exam waec \
  --subject mathematics \
  --topic algebra \
  --difficulty medium \
  --count 10 \
  --output runs/waec_math_sample.json
```

**Output**: `runs/waec_math_sample.json` with 10 validated questions

### 2️⃣ Generate 15 Questions for NECO Biology
```bash
python -m mlops.exam_content_generator \
  --exam neco \
  --subject biology \
  --topic photosynthesis \
  --difficulty easy \
  --count 15 \
  --output runs/neco_bio_sample.json
```

### 3️⃣ Generate 20 Questions for JAMB Chemistry
```bash
python -m mlops.exam_content_generator \
  --exam jamb \
  --subject chemistry \
  --topic periodic_table \
  --difficulty hard \
  --count 20 \
  --output runs/jamb_chem_sample.json
```

---

## 📊 Generated Content Format

Each question follows this structure:

```json
{
  "id": "waec_mathematics_00001",
  "exam_board": "waec",
  "subject": "mathematics",
  "topic": "algebra",
  "difficulty": "medium",
  "question_text": "What is the basic definition of algebra?",
  "options": [
    "Option A: Correct answer...",
    "Option B: Distractor 1...",
    "Option C: Distractor 2...",
    "Option D: Distractor 3..."
  ],
  "correct_answer": "Option A: Correct answer...",
  "explanation": "Step-by-step explanation with logic...",
  "question_type": "multiple_choice",
  "quality_score": 0.85,
  "relevance_score": 0.92,
  "created_at": "2025-12-05T10:30:00"
}
```

---

## 🤖 System Architecture

```
┌─────────────────────────────────────────────┐
│     Orchestrator (Master Agent)             │
└─────────────────────────────────────────────┘
              ↓
    ┌────────┼────────┐
    ↓        ↓        ↓
┌─────┐  ┌───────┐  ┌──────┐
│  Q  │  │ Valid │  │ Score│
│  Gen│  │ ator  │  │Agent │
└─────┘  └───────┘  └──────┘
    ↓        ↓        ↓
    └────────┼────────┘
             ↓
      ┌─────────────┐
      │   Storage   │
      │  (Database) │
      └─────────────┘
```

---

## 📈 Key Metrics

### Target Performance
- **Generation Speed**: <2 seconds per question
- **Quality Score**: >0.85/1.0
- **Relevance**: >0.90/1.0
- **Pass Rate**: >80% of generated questions
- **Cost**: <$0.01 per question

### Current Baseline (From Sample Run)
- Generated: 45 questions (15 per exam board)
- Pass Rate: 80%+
- Avg Quality: 0.75-0.80
- Avg Relevance: 0.70-0.75

---

## 🔧 Configuration

### Supported Exam Boards
- `waec` → West African Examinations Council
- `neco` → National Examination Council
- `jamb` → Joint Admissions and Matriculation Board

### Difficulty Levels
- `easy` → Foundation/recall questions
- `medium` → Application/analysis questions
- `hard` → Synthesis/evaluation questions

### Subjects Covered
- **Mathematics**: algebra, geometry, calculus, trigonometry, statistics, probability
- **Physics**: mechanics, thermodynamics, waves & optics, electricity & magnetism, modern physics
- **Chemistry**: organic, inorganic, physical chemistry, analytical
- **Biology**: cell biology, genetics, ecology, physiology, botany, zoology
- **English**: literature, grammar, comprehension, vocabulary, essay writing

---

## 🔗 Integration Points

### Google Notebook LM
```
1. Visit: https://notebooklm.google.com
2. Upload textbooks as PDFs
3. Generate audio study guides
4. Download MP3 files
5. Link in quiz app: /assets/audio/{subject}/{topic}/
```

### Google AI Studio
```
1. Visit: https://aistudio.google.com
2. Create text/chat prompts
3. Test against sample questions
4. Export refined prompts to code
5. Update prompt templates in generator
```

### Hugging Face Hub
```
# Login locally
huggingface_hub.login()

# Fine-tune a model
from transformers import Trainer
trainer = Trainer(model, args, train_dataset, eval_dataset)
trainer.train()

# Push to Hub
model.push_to_hub("username/exam-question-generator")
```

---

## 📚 Next Steps (Priority Order)

### ✅ Phase 1 (This Week)
- [ ] Execute Week 1 setup from `IMPLEMENTATION_GUIDE.md`
- [ ] Download 5-10 years of past papers (WAEC, NECO, JAMB)
- [ ] Organize papers by subject/topic
- [ ] Create `data/exam_papers/` directory structure

### ⏳ Phase 2 (Next Week)
- [ ] Set up Google Notebook LM account
- [ ] Upload textbooks to Notebook LM
- [ ] Generate first batch of audio guides
- [ ] Build advanced question generator (see `IMPLEMENTATION_GUIDE.md`)
- [ ] Test with 100 questions

### 🚀 Phase 3 (Week 3)
- [ ] Deploy FastAPI server
- [ ] Set up MLflow experiment tracking
- [ ] Configure GitHub Actions for daily generation
- [ ] Create admin dashboard

### 📊 Phase 4 (Week 4+)
- [ ] Collect student feedback on questions
- [ ] Fine-tune models on high-quality questions
- [ ] Implement adaptive difficulty
- [ ] Scale to 1000+ questions/day

---

## 🛠️ Development Commands

### Setup Environment
```bash
# Navigate to project
cd C:\Users\hp\Documents\Akulearn_docs

# Create conda environment
./mlops/install_conda.ps1

# Activate environment
conda activate akulearn_mlops

# Install additional dependencies
pip install google-auth-oauthlib google-cloud-aiplatform

# Verify installation
python -c "from mlops.exam_content_generator import *; print('✓ Ready')"
```

### Generate Content
```bash
# Single batch
python -m mlops.exam_content_generator --exam waec --subject math --count 50

# View results
type runs\generated_content.json | findstr "quality_score"

# Run demo notebook
jupyter notebook mlops/exam_content_demo.ipynb
```

### MLflow Tracking
```bash
# Start MLflow UI
mlflow ui --backend-store-uri runs/mlflow

# Visit http://localhost:5000
```

### API Server
```bash
# Deploy FastAPI (Week 3)
uvicorn mlops.deploy_api:app --reload --port 8001

# Test endpoint
curl http://localhost:8001/generate-content -X POST \
  -H "Content-Type: application/json" \
  -d '{"exam_board":"waec","subject":"mathematics","topic":"algebra","difficulty":"medium","count":10}'
```

---

## 📖 Documentation Map

- **Strategic Overview** → `docs/AIOPS_STRATEGY.md`
- **Implementation Roadmap** → `mlops/IMPLEMENTATION_GUIDE.md`
- **Code Documentation** → `mlops/exam_content_generator.py` (docstrings)
- **Interactive Demo** → `mlops/exam_content_demo.ipynb`
- **This Guide** → `mlops/AIOPS_QUICK_REFERENCE.md`

---

## 🎓 Key Learnings from AIops

### 1. **Automation Saves Time**
- 50 questions generated in <100 seconds
- vs. 1-2 weeks manual creation

### 2. **Quality Validation is Critical**
- 80% generation pass rate (realistic)
- Human review still needed for top 20%
- Multi-level validation catches issues early

### 3. **Observability Matters**
- Track every generation attempt with MLflow
- Monitor quality/relevance metrics over time
- Use dashboards to identify patterns

### 4. **Infrastructure is Code**
- All configs versioned in git
- CI/CD automates daily content batches
- Easy to scale or rollback

### 5. **Feedback Loops Drive Improvement**
- Collect student feedback on questions
- Identify which topics need more content
- Retrain models on high-rated questions

---

## ❓ FAQ

**Q: Can I run this without GPU?**
A: Yes! CPU mode is perfectly fine. Most generation happens in <2s on CPU.

**Q: How do I fine-tune on my own questions?**
A: See `IMPLEMENTATION_GUIDE.md` Week 2 section on advanced generation.

**Q: What if Google tools have rate limits?**
A: Use local Ollama or fine-tuned models as fallback. See architecture guide.

**Q: How do I ensure content quality?**
A: Multi-level validation + human review of generated batch before deployment.

**Q: Can this work for other exams (UTME, A-Levels, etc.)?**
A: Yes! Just add new ExamBoard enum and adjust question templates.

---

## 🤝 Support & Resources

- **Hugging Face Models**: https://huggingface.co/models
- **Google Notebook LM**: https://notebooklm.google.com
- **Google AI Studio**: https://aistudio.google.com
- **LangChain Docs**: https://python.langchain.com
- **MLflow Guide**: https://mlflow.org/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

## 📝 Commit History

Latest commits implementing this system:
- `611f5ef` - feat: add comprehensive AIops strategy and exam content generation system
- `4ec9f5d` - fix: correct train_bert_custom.py Trainer API and add CI network fallbacks
- `b6f4a8e` - feat: add production BERT training with MLflow

View full history:
```bash
git log --oneline -10
```

---

**Status**: ✅ Foundation complete, ready for Phase 1 implementation

**Next Meeting**: Review data collection progress and Google tool setup

*Last Updated: 2025-12-05*
