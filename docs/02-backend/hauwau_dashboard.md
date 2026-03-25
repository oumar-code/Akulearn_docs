# Hauwau Abubakar Dashboard

The Hauwau Abubakar Dashboard is a special-access interface designed for the **Exam Prep & Access Coordinator** role. It combines a personalised JAMB preparation environment — focused on **English, Biology, Physics, and Chemistry** for a **Medicine & Surgery** admission target — with broad coordinator access across multiple platform dashboards.

## JAMB Subject Modules

Hauwau has four dedicated JAMB subject modules, each structured around the official JAMB UTME syllabus:

### English Language
- Reading comprehension passages at JAMB difficulty level
- Lexis & structure, sentence interpretation, antonyms and synonyms
- Oral English: vowels, consonants, rhymes, and stress patterns
- Summary and cloze passages
- **Post-topic quiz** after each unit (see [Quiz Format](#post-topic-quiz-format) below)

### Biology
- Cell biology, genetics, ecology, evolution, and applied biology
- Organ systems: digestive, respiratory, circulatory, reproductive, nervous
- Genetics and variation: Mendelian ratios, codominance, sex linkage
- **Post-topic quiz** after each unit

### Physics
- Mechanics: motion, forces, energy, momentum, simple machines
- Waves and optics: sound, light, reflection, refraction
- Electricity and magnetism: circuits, capacitors, electromagnetic induction
- Modern Physics: photoelectric effect, radioactivity, nuclear reactions
- **Post-topic quiz** after each unit

### Chemistry
- Atomic structure, periodicity, chemical bonding
- Acids, bases, and salts; redox reactions; electrochemistry
- Organic chemistry: hydrocarbons, functional groups, reactions
- Industrial chemistry: Haber process, Contact process, extraction of metals
- **Post-topic quiz** after each unit

## Post-Topic Quiz Format

Every quiz on Hauwau's dashboard is automatically triggered when she marks a topic as complete. The quizzes mirror JAMB UTME exam conditions:

| Parameter | Value |
|---|---|
| Question type | 4-option multiple choice (A, B, C, D) |
| Questions per quiz | 20 (short topic quiz) or 40 (full mock, end of chapter) |
| Time limit | 25 minutes (topic quiz) / 45 minutes (full mock) |
| Marking | +1 for correct answer, 0 for wrong (no negative marking, matching JAMB) |
| Feedback | Immediate answer reveal with explanation after submission |
| Question bank | Drawn from JAMB past questions (2010–2024) + AI-generated syllabus questions |
| Difficulty grading | Questions increase in difficulty as mastery score rises |
| Score threshold | ≥ 60 % to unlock the next topic; review mode offered below threshold |

## Medicine Pathway

Hauwau's dashboard includes a **Medicine & Surgery Pathway** tracker that:

- Calculates her projected JAMB UTME aggregate score across all four subjects
- Highlights the minimum cut-off marks for Medicine at federal and state universities in Nigeria
- Shows per-subject mastery progress toward the typical 280+ aggregate required for Medicine
- Links to post-JAMB resources: post-UTME preparation, JAMB admission letter guide, and university direct-entry requirements

## Additional Access

As Exam Prep & Access Coordinator, Hauwau also has access to:

- **WAEC & NECO Access:** WAEC and NECO exam preparation content (useful for secondary-school cross-check)
- **Student Dashboard View:** Oversight and support across student accounts
- **Teacher Dashboard View:** Curriculum and content coordination
- **Content Management:** Review and publish learning content
- **Analytics:** Exam readiness metrics and platform analytics
- **School Admin Dashboard View:** School-level coordination
- **Aku Workspace:** Shared team workspace for collaboration and project tracking

## Access

This dashboard is exclusively assigned to **Hauwau Abubakar** (`hauwauabubakargusau2009@gmail.com`) in the `hauwau_special` role. Access is governed by role-based authentication configured in [`team.py`](../../team.py) and [`supabase_provision.py`](../../supabase_provision.py).

## Navigation

From the main navigation, select **Backend > Hauwau Dashboard** to access this page.
For the detailed JAMB preparation specification, see [**Hauwau JAMB Prep**](hauwau_jamb_prep.md).

---

For technical details, see the backend API documentation and the team configuration in `team.py`.

