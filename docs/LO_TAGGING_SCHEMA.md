# Learning Objective (LO) Tagging Schema for Aku Learn

This document describes the canonical tagging schema we will use to map content assets to Nigeria secondary school curricula (NERDC, WAEC, NECO) learning objectives.

Goals
- Make every content asset mappable to one or more Learning Objective IDs (LO_ID).
- Support multiple taxonomies (NERDC LO IDs, WAEC syllabus topics) and map them to a unified internal LO namespace.
- Make tags machine-friendly and easy for human reviewers to apply or correct.

Schema Overview
- LO_ID: Unique identifier for a Learning Objective in the internal system.
  - Format: `LO:{CURRICULUM}:{SUBJECT}:{CLASS}:{TOPIC_CODE}:{SEQ}`
  - Example: `LO:NERDC:MAT:SS2:ALG:001`
  - JSS examples: `LO:NERDC:MAT:JSS1:T1:001` (Mathematics JSS1 Topic 1 LO 1)
                  `LO:NERDC:BSC:JSS3:T8:002` (Basic Science JSS3 Topic 8 LO 2)
                  `LO:NERDC:ENG:JSS2:T3:001` (English Language JSS2 Topic 3 LO 1)

**Class Level Values** (expanded to include Junior Secondary):
| Value | Description | Target Exam |
|-------|-------------|------------|
| `JSS1` | Junior Secondary School Year 1 | National Assessment |
| `JSS2` | Junior Secondary School Year 2 | National Assessment |
| `JSS3` | Junior Secondary School Year 3 | BECE / Common Entrance |
| `SS1` | Senior Secondary School Year 1 | Internal / State exams |
| `SS2` | Senior Secondary School Year 2 | WAEC mock / Checkpoint |
| `SS3` | Senior Secondary School Year 3 | WAEC / NECO / JAMB |

**Subject Codes — Full List** (JSS subjects added):
| Code | Subject | Level |
|------|---------|-------|
| `MAT` | Mathematics | JSS + SS |
| `ENG` | English Language | JSS + SS |
| `BSC` | Basic Science | JSS |
| `SST` | Social Studies | JSS |
| `BTH` | Basic Technology | JSS |
| `CIV` | Civic Education | JSS + SS |
| `AGR` | Agricultural Science | JSS + SS |
| `HEC` | Home Economics | JSS |
| `FRN` | French | JSS + SS |
| `PHY` | Physics | SS |
| `CHE` | Chemistry | SS |
| `BIO` | Biology | SS |
| `ECO` | Economics | SS |
| `GOV` | Government | SS |
| `GEO` | Geography | SS |
| `FMA` | Further Mathematics | SS |
| `ACC` | Financial Accounting | SS |
| `COM` | Commerce | SS |
| `LIT` | Literature in English | SS |
| `CRS` | Christian Religious Studies | JSS + SS |
| `IRS` | Islamic Religious Studies | JSS + SS |
| `ICT` | Information Technology | JSS + SS |

- Fields for each mapping entry (CSV/JSON):
  - asset_path: Relative path to the content asset (e.g., `content/textbooks/math_v1.0/chapter1.pdf`)
  - asset_type: `pdf`, `video`, `quiz`, `simulation`, `flashcard`, `ar`, etc.
  - curriculum: Source curriculum (e.g., `NERDC`, `WAEC`, `NECO`, `FED_MIN_ED`) — can be multiple
  - subject: Standard subject code (MAT, PHY, CHE, BIO, ENG, SST, BSC, BTH, CIV, etc.)
  - class_level: `JSS1`, `JSS2`, `JSS3`, `SS1`, `SS2`, or `SS3`
  - term_week: Optional field for term or week mapping (Term1, Term2, Term3 or week number)
  - topic: Human-readable topic name (e.g., `Quadratic Equations`)
  - subtopic: Optional subtopic name
  - lo_id: The internal LO ID(s) assigned (comma-separated if multiple)
  - confidence: `auto` or numeric confidence (0.0-1.0) if assigned by AI
  - assigned_by: `auto` or reviewer username
  - assigned_at: ISO timestamp when assignment was made
  - notes: Free text for reviewer comments
  - language: `en`, `ha`, `ig`, `yo`, etc.

Tagging Process
1. Automated Pass (AI):
   - Use NLU (transformers) to propose tags and candidate LO IDs based on textual similarity with LO descriptions.
   - Vectorize LO descriptions and content chunks and compute nearest neighbors.
   - Propose `lo_id` and set `confidence` (0-1) and `assigned_by=auto`.
2. Human Review Pass (Teacher / Curriculum Expert):
   - Review AI proposals in a UI, accept/correct LO assignments, set `assigned_by=<username>` and `confidence=1.0`.
   - Add `notes` for exceptional cases.
3. Finalize and Publish:
   - Once an asset has validated LO mappings for a curriculum, publish mappings to the content registry and vector DB index.

LO Naming & Versioning
- LO IDs should be immutable once published. If curriculum changes, create new LO IDs and map old IDs to new via a `lo_version_map`.
- Maintain `lo_catalog.json` with LO_ID, curriculum, subject, class_level, topic, lo_text, created_at, last_updated.

Data Formats
- CSV template: `content/lo_mapping_template.csv` (see repository)
- System store: `lo_catalog.json` (canonical LO descriptions)
- Vector store: embeddings stored in vector DB (Milvus, Pinecone, Weaviate) with metadata linking to LO_IDs.

Review Flow
- Use automatic ingestion to pre-fill LO candidates.
- Teachers/curriculum experts verify via the LO Mapper UI (or CSV batch edits).
- Track reviewer activity logs for audit.

Privacy & Compliance
- Do not store student PII in mapping files.
- Keep reviewer and system logs for audit and quality measurement.

Next Steps
- ✅ JSS1–JSS3 LO schema extended (class levels, subject codes, LO ID format)
- ✅ JSS1–JSS3 textbook starter files created (9 core files in `public/`)
- ✅ Pipeline scripts created (`pipeline/textbook_generator.py`, `flashcard_generator.py`, `quiz_generator.py`, `bece_scraper.py`)
- [ ] Create `lo_catalog.json` with initial LO entries for JSS1–JSS3 Mathematics, English, Basic Science (pilot)
- [ ] Extend `lo_catalog.json` to cover all JSS subjects (SST, BTH, CIV)
- [ ] Build the LO Mapper UI and CSV import/export workflows
- [ ] Integrate auto-tagging NLU pipeline and vector DB for LO similarity search
- [ ] Add SS1–SS3 gap subjects to catalog (Economics, Government, Geography)

**JSS LO Catalog Seed** (starter entries — expand via `pipeline/textbook_generator.py`):

```json
[
  {
    "lo_id": "LO:NERDC:MAT:JSS1:T1:001",
    "curriculum": "NERDC",
    "subject": "MAT",
    "class_level": "JSS1",
    "term": 1,
    "topic_code": "T1",
    "topic": "Place Value and Whole Numbers",
    "lo_text": "Student can identify the place value of any digit in a number up to 1,000,000 and write numbers in expanded form",
    "target_exam": "National Assessment",
    "created_at": "2026-04-10"
  },
  {
    "lo_id": "LO:NERDC:MAT:JSS1:T2:001",
    "curriculum": "NERDC",
    "subject": "MAT",
    "class_level": "JSS1",
    "term": 1,
    "topic_code": "T2",
    "topic": "BODMAS and Order of Operations",
    "lo_text": "Student can apply BODMAS to evaluate multi-step arithmetic expressions correctly",
    "target_exam": "National Assessment",
    "created_at": "2026-04-10"
  },
  {
    "lo_id": "LO:NERDC:ENG:JSS1:T1:001",
    "curriculum": "NERDC",
    "subject": "ENG",
    "class_level": "JSS1",
    "term": 1,
    "topic_code": "T1",
    "topic": "Parts of Speech",
    "lo_text": "Student can identify and correctly use all 8 parts of speech in written and spoken English",
    "target_exam": "National Assessment",
    "created_at": "2026-04-10"
  },
  {
    "lo_id": "LO:NERDC:BSC:JSS1:T1:001",
    "curriculum": "NERDC",
    "subject": "BSC",
    "class_level": "JSS1",
    "term": 1,
    "topic_code": "T1",
    "topic": "Characteristics of Living Things (MRS GREN)",
    "lo_text": "Student can list and explain all 7 MRS GREN characteristics of living things with examples",
    "target_exam": "National Assessment",
    "created_at": "2026-04-10"
  }
]
```

Use `pipeline/textbook_generator.py` to auto-generate the full catalog across all JSS and SS subjects.
