# Mock Exam Structure & Design Guide

## Overview
Mock exams are critical for JAMB success. They simulate the real exam pressure, timing, and question mix.

## JAMB Real Exam Format (Reference)
```
Duration: 3 hours
Total Questions: 180
Question Type: All Multiple Choice (4 options)
Subjects: English Language (40) + Mathematics (40) + 2 Chosen Subjects (100)

Scoring:
- Each question = 1 point
- No negative marking
- Total = 180 points
- Average candidate score: 50-70 points (28-39%)
- High achiever score: 120+ points (67%+)
```

---

## Mock Exam Structure Templates

### Mock Exam Format (Complete 3-Hour Exam)

#### **Structure A: Standard Full Mock (Recommended)**
```json
{
  "mockExam": {
    "id": "mock_exam_001_standard",
    "name": "JAMB Full Mock Exam - January 2026",
    "duration": 180,
    "durationUnit": "minutes",
    "totalQuestions": 180,
    
    "sections": [
      {
        "sectionNumber": 1,
        "subject": "English Language",
        "questionCount": 40,
        "timeAllocationMinutes": 60,
        "avgTimePerQuestion": 1.5,
        "questionTopics": [
          "Comprehension (12 questions)",
          "Vocabulary (8 questions)",
          "Grammar (10 questions)",
          "Essay (10 questions)"
        ],
        "difficultyDistribution": {
          "easy": "40%",
          "medium": "40%",
          "hard": "20%"
        }
      },
      {
        "sectionNumber": 2,
        "subject": "Mathematics",
        "questionCount": 40,
        "timeAllocationMinutes": 60,
        "avgTimePerQuestion": 1.5,
        "questionTopics": [
          "Algebra (10 questions)",
          "Geometry (8 questions)",
          "Trigonometry (8 questions)",
          "Statistics (7 questions)",
          "Calculus (7 questions)"
        ],
        "difficultyDistribution": {
          "easy": "25%",
          "medium": "50%",
          "hard": "25%"
        }
      },
      {
        "sectionNumber": 3,
        "subject": "Science (Choice 1) - Chemistry",
        "questionCount": 50,
        "timeAllocationMinutes": 30,
        "avgTimePerQuestion": 0.6,
        "questionTopics": [
          "Atomic Structure (8 questions)",
          "Bonding (8 questions)",
          "Stoichiometry (8 questions)",
          "Organic Chemistry (12 questions)",
          "Physical Chemistry (7 questions)",
          "Inorganic Chemistry (7 questions)"
        ],
        "difficultyDistribution": {
          "easy": "30%",
          "medium": "45%",
          "hard": "25%"
        }
      },
      {
        "sectionNumber": 4,
        "subject": "Science (Choice 2) - Biology",
        "questionCount": 50,
        "timeAllocationMinutes": 30,
        "avgTimePerQuestion": 0.6,
        "questionTopics": [
          "Cell Biology (8 questions)",
          "Photosynthesis (6 questions)",
          "Respiration (6 questions)",
          "Genetics (8 questions)",
          "Ecology (8 questions)",
          "Human Physiology (8 questions)",
          "Reproduction (6 questions)"
        ],
        "difficultyDistribution": {
          "easy": "30%",
          "medium": "45%",
          "hard": "25%"
        }
      }
    ],
    
    "timingStrategy": {
      "section1_english": "Steady pace - 1.5 min per Q",
      "section2_math": "Take time on hard Qs - 2-3 min each",
      "section3_chemistry": "Quick on calc heavy - 0.5-1 min each",
      "section4_biology": "Steady - 0.8-1 min each",
      "breakTime": "1-2 min between sections (mental reset)"
    },

    "scoringMetrics": {
      "passingScore": 120,
      "excellentScore": 160,
      "perfectionScore": 180,
      "feedbackTriggers": {
        "below_80": "Focus on basics - review fundamentals",
        "80_120": "You're on track - keep drilling weak areas",
        "120_150": "Strong prep - polish weak topics",
        "150_plus": "Excellent - ready for exam!"
      }
    }
  }
}
```

---

### Quick Mock Exam (For Daily Practice)
```json
{
  "quickMock": {
    "id": "quick_mock_001",
    "name": "Quick Chemistry Mock (30 min)",
    "duration": 30,
    "totalQuestions": 20,
    "subject": "Chemistry Only",
    "purpose": "Daily skill-building",
    
    "structure": {
      "section1": {
        "name": "Organic Chemistry",
        "questions": 10,
        "timeLimit": 15,
        "topics": ["Nomenclature", "Reactions", "Mechanisms"]
      },
      "section2": {
        "name": "Inorganic Chemistry",
        "questions": 10,
        "timeLimit": 15,
        "topics": ["Bonding", "Reactions", "Calculations"]
      }
    }
  }
}
```

---

### Adaptive Mock (Based on Student Performance)
```json
{
  "adaptiveMock": {
    "id": "adaptive_mock_001",
    "name": "Personalized Mock - Based on Your Weak Topics",
    "duration": 60,
    "totalQuestions": 40,
    
    "algorithm": {
      "step1": "Analyze student's weak topics from previous tests",
      "step2": "Generate 60% hard Qs from weak areas",
      "step3": "Include 20% medium, 20% easy for confidence",
      "step4": "Adjust difficulty after every 10 questions",
      "step5": "Provide real-time feedback and hints"
    },

    "example": {
      "student": "Chioma",
      "weakAreas": ["Organic Chemistry", "Trigonometry", "Genetics"],
      "mockComposition": {
        "organicChemistry": 12,
        "trigonometry": 8,
        "genetics": 8,
        "otherTopics": 12
      },
      "estimatedScore": "105/180 (58%)"
    }
  }
}
```

---

## Question Distribution Guide

### By Difficulty (Realistic JAMB Distribution)

**Section 1 - English (40 Q)**
```
Easy (40%):  16 Q - Vocabulary, basic comprehension
Medium (40%): 16 Q - Grammar, reading comprehension  
Hard (20%):   8 Q - Essay, complex passages
```

**Section 2 - Math (40 Q)**
```
Easy (25%):   10 Q - Basic algebra, simple geometry
Medium (50%): 20 Q - Complex calculations, proofs
Hard (25%):   10 Q - Integration, optimization, difficult word problems
```

**Section 3 & 4 - Sciences (100 Q)**
```
Easy (30%):   30 Q - Recall, definitions
Medium (45%): 45 Q - Application, problem-solving
Hard (25%):   25 Q - Analysis, novel scenarios
```

---

## Timing Guidelines

### Time Budget (3-hour exam = 180 minutes)

```
English Language (40 Q) → 60 minutes
├─ Reading comprehension: 30 min (3 passages × 10 min)
├─ Vocabulary/Grammar: 20 min (20 questions)
└─ Essays/Written work: 10 min (2 questions)

Mathematics (40 Q) → 60 minutes
├─ Calc-heavy (Calculus, Stats): 25 min (hard)
├─ Mid-level (Trig, Geometry): 25 min (medium)
└─ Easy questions: 10 min (basic algebra)

Chemistry (50 Q) → 30 minutes
└─ ~0.6 min per question (fast pace required)

Biology (50 Q) → 30 minutes
└─ ~0.6 min per question (fast pace required)

Buffer/Review Time: 0 minutes (strict timing)
```

---

## Mock Exam Scheduling Strategy

### For Optimal Preparation (12-week prep)

```
Week 1-2:   Diagnostic test (identify weak areas)
Week 3-4:   Practice tests + targeted drilling
Week 5-6:   Full mocks (once per week)
Week 7-8:   Full mocks (twice per week)
Week 9-10:  Full mocks (three times per week)
Week 11-12: Timed full mocks (exam simulation)
```

### Daily Practice Schedule
```
Monday:    10 min Chemistry quick mock
Tuesday:   10 min English comprehension quick mock
Wednesday: 20 min Math quick mock
Thursday:  10 min Biology quick mock
Friday:    30 min - One section full mock
Saturday:  Full 3-hour mock exam (or skip one week)
Sunday:    Review & study weak areas
```

---

## Success Metrics from Mocks

### What to Track

```
Metric 1: Overall Score Trend
Target: +5 points per week improvement
Benchmark: 80 → 100 → 120 → 140 → 160

Metric 2: Subject Performance
Chemistry:  Target 85%+ (high priority)
Biology:    Target 80%+ (high priority)  
Math:       Target 75%+
English:    Target 70%+

Metric 3: Time Management
Avg time per Q maintained under limit?
Rushing on last section?
Need more practice on calculation-heavy sections?

Metric 4: Accuracy by Difficulty
Easy (>85%), Medium (>60%), Hard (>40%)
If hard Q accuracy <40%, study harder

Metric 5: Consistency
Score variation between mocks <10 points?
If >10, performance is inconsistent (luck factor)
```

---

## Mock Exam Feedback Template

### After Each Mock Exam

```json
{
  "feedback": {
    "mockNumber": 1,
    "date": "2026-01-30",
    "totalScore": 95,
    "maxScore": 180,
    "percentage": "52.8%",
    "status": "Below average (Need improvement)",

    "sectionScores": {
      "english": { "score": 28, "max": 40, "percent": 70 },
      "mathematics": { "score": 18, "max": 40, "percent": 45 },
      "chemistry": { "score": 32, "max": 50, "percent": 64 },
      "biology": { "score": 17, "max": 50, "percent": 34 }
    },

    "weakestAreas": [
      "Biology: Genetics (40% accuracy)",
      "Mathematics: Calculus (30% accuracy)",
      "English: Essay writing (50% accuracy)"
    ],

    "strongestAreas": [
      "Chemistry: Organic nomenclature (85%)",
      "English: Comprehension (80%)"
    ],

    "recommendedFocus": [
      "Priority 1: Biology Genetics - 5 hours this week",
      "Priority 2: Math Calculus - 4 hours",
      "Priority 3: English Essay structure - 2 hours"
    ],

    "nextMockTarget": 110,
    "daysUntilNextMock": 3
  }
}
```

---

## Tips for Creating Effective Mocks

1. **Mix question sources**: Past papers + textbook + AI-generated (ensures variety)
2. **Validate by experts**: Have subject teachers review before release
3. **Include trick questions**: Real JAMB has distractors
4. **Realistic difficulty curve**: Not too easy, not impossible
5. **Clear answer explanations**: Each Q needs 2-3 line explanation
6. **Track student performance**: Monitor which Q types stump students most
7. **Update regularly**: Add new questions weekly based on trends
8. **Time limit strictly**: No extra time, builds exam stamina

---

## Implementation Checklist

- [ ] Create first 3 full mock exams (180 Q each)
- [ ] Design quick mocks (1 per subject)
- [ ] Build adaptive mock algorithm
- [ ] Create feedback template
- [ ] Set up scoring & tracking
- [ ] Test on 5 beta students
- [ ] Refine based on feedback
- [ ] Deploy to students
- [ ] Monitor usage & performance
- [ ] Update mocks weekly with new questions
