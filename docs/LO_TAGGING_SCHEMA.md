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

- Fields for each mapping entry (CSV/JSON):
  - asset_path: Relative path to the content asset (e.g., `content/textbooks/math_v1.0/chapter1.pdf`)
  - asset_type: `pdf`, `video`, `quiz`, `simulation`, `flashcard`, `ar`, etc.
  - curriculum: Source curriculum (e.g., `NERDC`, `WAEC`, `NECO`, `FED_MIN_ED`) — can be multiple
  - subject: Standard subject code (MAT, PHY, CHE, BIO, ENG, GOV, ECO, CRS, AGR, ICT, etc.)
  - class_level: `SS1`, `SS2`, `SS3` (or `JSS` etc. if present)
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
- Create `lo_catalog.json` with initial LO entries for one subject (e.g., Mathematics SS1-SS3) as pilot.
- Build the LO Mapper UI and CSV import/export workflows.
- Integrate auto-tagging NLU pipeline and vector DB for LO similarity search.
