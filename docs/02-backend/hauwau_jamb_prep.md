# Hauwau Abubakar — JAMB Preparation Specification

This document is the authoritative specification for Hauwau Abubakar's personalised JAMB UTME preparation programme on the Aku platform. It covers subject scope, quiz mechanics, scoring rules, and the Medicine & Surgery admission pathway.

**Account:** `hauwauabubakargusau2009@gmail.com`  
**Dashboard:** `hauwau_special`  
**Target exam:** JAMB UTME  
**Career goal:** Medicine & Surgery

---

## Subjects

JAMB UTME for Medicine & Surgery requires four subjects. Hauwau's combination is:

| # | Subject | JAMB Category | Medicine relevance |
|---|---|---|---|
| 1 | **Use of English** | Compulsory (all candidates) | Communication, comprehension |
| 2 | **Biology** | Core science | Foundation for human anatomy, physiology |
| 3 | **Physics** | Core science | Medical imaging, biophysics |
| 4 | **Chemistry** | Core science | Pharmacology, biochemistry |

---

## Syllabus Scope per Subject

Each subject is covered to the full JAMB UTME syllabus scope. The topics below
are the primary study units that trigger a post-topic quiz when marked complete.

### Use of English

| Unit | Topics |
|---|---|
| Comprehension | Reading passages, inference, summary, cloze tests |
| Lexis & Structure | Sentence interpretation, antonyms, synonyms, word usage |
| Oral English | Vowels, consonants, stress, intonation, rhymes |
| Figures of Speech | Metaphor, simile, irony, hyperbole, personification |
| Register & Idioms | Technical register, idiomatic expressions, phrasal verbs |

### Biology

| Unit | Topics |
|---|---|
| Cell Biology | Cell structure, cell division (mitosis/meiosis), cell transport |
| Genetics | Mendelian inheritance, codominance, sex linkage, mutation |
| Ecology | Food chains, energy flow, population dynamics, conservation |
| Human Physiology | Digestive, respiratory, circulatory, excretory, nervous systems |
| Evolution & Classification | Darwinism, taxonomy, kingdom classification |
| Applied Biology | Agriculture, biotechnology, disease and immunity |

### Physics

| Unit | Topics |
|---|---|
| Mechanics | Scalars and vectors, motion, Newton's laws, work/energy/power |
| Waves | Wave properties, sound, light (reflection, refraction, diffraction) |
| Electricity | DC circuits, Ohm's law, capacitors, resistance, power |
| Magnetism | Magnetic fields, electromagnetic induction, transformers |
| Modern Physics | Photoelectric effect, X-rays, radioactivity, nuclear reactions |
| Thermodynamics | Temperature, heat transfer, gas laws |

### Chemistry

| Unit | Topics |
|---|---|
| Atomic Structure | Bohr model, electron configuration, periodic table trends |
| Chemical Bonding | Ionic, covalent, metallic bonds; VSEPR theory |
| States of Matter | Kinetic theory, gas laws, solutions and solubility |
| Acids, Bases & Salts | pH, neutralisation, buffer solutions, salt hydrolysis |
| Electrochemistry | Electrolysis, galvanic cells, Faraday's laws, corrosion |
| Organic Chemistry | Hydrocarbons, functional groups, isomerism, reaction mechanisms |
| Industrial Chemistry | Haber process, Contact process, metal extraction, fertilisers |
| Redox Reactions | Oxidation numbers, balancing redox equations, disproportionation |

---

## Post-Topic Quiz Rules

A quiz is automatically triggered every time Hauwau marks a topic as **complete** in her study tracker.

### Quiz Types

| Type | When triggered | Questions | Time limit |
|---|---|---|---|
| **Topic Quiz** | End of each individual topic unit | 20 MCQs | 25 minutes |
| **Chapter Mock** | End of a full subject chapter (group of units) | 40 MCQs | 45 minutes |
| **Full Subject Mock** | On demand or end of full subject syllabus | 60 MCQs | 70 minutes |

### Question Format

All questions are 4-option multiple choice (**A, B, C, D**), identical to the JAMB UTME format. Every question:

- Has exactly one correct answer
- Is drawn from the official JAMB past-question archive (2010–2024) or AI-generated questions mapped to the JAMB syllabus
- Is tagged with: subject, unit, topic, difficulty level, and JAMB year (if applicable)

### Scoring & Progression

| Metric | Rule |
|---|---|
| Correct answer | +1 mark |
| Wrong answer | 0 marks (JAMB does not apply negative marking) |
| Pass threshold | ≥ 60 % (12/20 on a topic quiz, 24/40 on a chapter mock) |
| Pass → unlock | Next topic is unlocked automatically |
| Fail → review | Weak topics are flagged; a targeted 10-question review quiz is offered |
| Difficulty scaling | Questions increase in difficulty as running mastery score rises above 75 % |

### Immediate Feedback

After every question submission the platform shows:
1. Whether the selected answer was correct
2. The correct answer (highlighted)
3. A brief explanation (drawn from the question bank annotation or AI-generated)
4. The JAMB year the question appeared (if from past papers)

---

## Medicine & Surgery Pathway Tracker

The Medicine Pathway panel is always visible on Hauwau's dashboard. It shows:

### Aggregate Score Projection

The JAMB aggregate for Medicine is calculated as:

```
JAMB score (out of 400) × 0.5  +  Post-UTME score (out of 100) × 0.5  =  Aggregate (out of 250)
```

The tracker estimates Hauwau's projected JAMB score from her current mastery percentages
across all four subjects (each subject is worth 100 marks in JAMB UTME):

```
Projected JAMB Score = (mastery_english + mastery_biology + mastery_physics + mastery_chemistry) / 4 × 400
```

### University Cut-off Reference Table

| University | Minimum JAMB for Medicine |
|---|---|
| University of Lagos (UNILAG) | 280 |
| Ahmadu Bello University (ABU) | 270 |
| University of Ilorin (UNILORIN) | 270 |
| Obafemi Awolowo University (OAU) | 280 |
| Bayero University Kano (BUK) | 260 |

> Cut-offs are indicative; always check the JAMB admission brochure for the current year.

### Progress Milestones

| Projected score | Status shown on dashboard |
|---|---|
| < 200 | 🔴 Below target — intensify study plan |
| 200–249 | 🟡 Approaching target — maintain momentum |
| 250–279 | 🟢 On track — review weak topics |
| 280+ | 🏆 Target reached — focus on Post-UTME prep |

---

## Study Schedule Recommendation

A suggested 12-week daily study plan is pre-loaded into Hauwau's dashboard:

| Week | Focus |
|---|---|
| 1–2 | English (comprehension, lexis) + Biology (cells, genetics) |
| 3–4 | Physics (mechanics, waves) + Chemistry (atomic structure, bonding) |
| 5–6 | Biology (ecology, physiology) + English (oral, register) |
| 7–8 | Chemistry (organic, industrial) + Physics (electricity, magnetism) |
| 9–10 | Full chapter mocks for all four subjects |
| 11 | Targeted review of flagged weak topics |
| 12 | Full subject mocks + timed JAMB simulation exam |

---

## Supabase Configuration

Hauwau's account in Supabase is provisioned with the following metadata by `supabase_provision.py`:

```json
{
  "user_metadata": {
    "name": "Hauwau Abubakar",
    "role": "Exam Prep & Access Coordinator",
    "dashboard": "hauwau_special",
    "aku_workspace": true,
    "jamb_subjects": ["english", "biology", "physics", "chemistry"],
    "study_goal": "medicine",
    "topic_quiz_enabled": true,
    "quiz_standard": "jamb"
  },
  "app_metadata": {
    "role": "hauwau_special"
  }
}
```

The `topic_quiz_enabled: true` and `quiz_standard: "jamb"` flags instruct the frontend to
auto-trigger a JAMB-format quiz whenever a topic is marked complete for this user.

---

For the dashboard overview, see [**Hauwau Dashboard**](hauwau_dashboard.md).  
For provisioning details, see [`supabase_provision.py`](../../supabase_provision.py).
