# Content Generation Pipeline

This directory contains the **Aku Platform content generation pipeline** — Python scripts for creating
JSS1–SS3 educational content that is stored in `oumar-code/Aku-Content` and served by `oumar-code/Akudemy`.

---

## Scripts

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `textbook_generator.py` | Generate textbook chapters (MD + JSON) using an LLM | NERDC curriculum map (built-in) | `content/textbooks/<level>/<subject>/chapter_NN.{json,md}` |
| `flashcard_generator.py` | Auto-generate flashcard decks from chapter JSON | `content/textbooks/` | `content/flashcards/<level>/<subject>/flashcards_chapter_NN.json` |
| `quiz_generator.py` | Auto-generate 10-question topic quizzes | `content/textbooks/` | `content/quizzes/<level>/<subject>/quiz_chapter_NN.json` |
| `bece_scraper.py` | Collect BECE / Common Entrance past questions (JSS1–JSS3) | Public exam paper sites | `data/exam_papers/bece/<subject>/questions.json` |

> **Senior secondary exam papers** (WAEC/NECO/JAMB): use `mlops/exam_paper_scraper.py` (gitignored,
> pending migration to `oumar-code/Akudemy`).

---

## Quick Start

### Prerequisites

```bash
pip install openai pydantic requests beautifulsoup4
```

### 1. Generate JSS1–JSS3 P1 textbook chapters (dry run first)

```bash
# Preview what would be generated (no LLM call):
python pipeline/textbook_generator.py --all-jss --dry-run

# Generate for real (using AkuAI local LLM):
python pipeline/textbook_generator.py --all-jss \
    --api-base http://localhost:8004/v1 \
    --output-dir content/textbooks/
```

### 2. Generate flashcard decks from chapters

```bash
python pipeline/flashcard_generator.py \
    --input-dir content/textbooks/ \
    --output-dir content/flashcards/
```

### 3. Generate topic quizzes

```bash
python pipeline/quiz_generator.py \
    --source textbook \
    --input-dir content/textbooks/ \
    --output-dir content/quizzes/
```

### 4. Collect BECE past questions

```bash
python pipeline/bece_scraper.py --all \
    --years 2019 2020 2021 2022 2023 \
    --output-dir data/exam_papers/bece/
```

### 5. Push everything to Aku-Content

```bash
# After running the above, push to Aku-Content via the migration workflow:
# Actions → "Aku-Content — Full Content Migration" → Run workflow
# Or locally:
./docs/service-migrations/migrate-to-aku-content.sh
```

---

## LLM Configuration

All generator scripts use an **OpenAI-compatible API**. Configure via environment variables or CLI flags:

| Variable | Default | Description |
|----------|---------|-------------|
| `AKUAI_API_BASE` | `http://localhost:8004/v1` | AkuAI local server URL |
| `AKUAI_API_KEY` | `local` | API key (any string for local LLM) |
| `AKUAI_MODEL` | `llama-3` | Model name |

To use **OpenAI API** instead (faster, for initial seeding):
```bash
export AKUAI_API_BASE=https://api.openai.com/v1
export AKUAI_API_KEY=sk-your-key-here
export AKUAI_MODEL=gpt-4o
python pipeline/textbook_generator.py --all-jss
```

To use **Anthropic Claude** via a proxy:
```bash
export AKUAI_API_BASE=https://api.anthropic.com/v1
export AKUAI_MODEL=claude-3-5-sonnet-20241022
```

---

## Content Priority Matrix

### Generate in this order:

| Priority | Level | Subjects | Reason |
|----------|-------|---------|--------|
| **P1** | JSS1–JSS3 | Mathematics, English Language, Basic Science | Compulsory, highest volume, zero existing content |
| **P2** | JSS1–JSS3 | Social Studies, Basic Technology, Civic Education | Compulsory JSS subjects |
| **P3** | SS1–SS3 (gaps) | Physics, Chemistry, Biology, Economics, Government | Fill SS gaps |
| **P4** | JSS1–JSS3 | Agricultural Science, Home Economics, French | Electives |
| **P5** | All | AR/VR assets | Requires separate blender/Unity pipeline |

---

## Output Structure

```
content/
├── textbooks/
│   ├── jss1/
│   │   ├── mathematics/
│   │   │   ├── chapter_01.json   ← structured metadata + content
│   │   │   ├── chapter_01.md     ← readable markdown
│   │   │   └── ...
│   │   ├── english_language/
│   │   └── basic_science/
│   ├── jss2/
│   ├── jss3/
│   ├── ss1/
│   ├── ss2/
│   └── ss3/
├── flashcards/
│   └── jss1/mathematics/flashcards_chapter_01.json
├── quizzes/
│   └── jss1/mathematics/quiz_chapter_01.json
data/
└── exam_papers/
    ├── bece/                         ← JSS (from bece_scraper.py)
    │   ├── INDEX.json
    │   └── mathematics/questions.json
    └── waec_neco_jamb/               ← SS (from mlops/exam_paper_scraper.py)
        └── INDEX.json
```

---

## LO Tagging

All generated JSON files include an `lo_id` field following the schema in
[`docs/LO_TAGGING_SCHEMA.md`](../docs/LO_TAGGING_SCHEMA.md):

```
LO:{CURRICULUM}:{SUBJECT_CODE}:{CLASS_LEVEL}:{TOPIC_CODE}:{SEQ}
Example: LO:NERDC:MAT:JSS1:T1:001
```

After generation, update `content/lo_catalog.json` with the new LO entries.

---

## MCPs Used in Generation

See [`docs/mcp/index.md`](../docs/mcp/index.md) for the full MCP strategy.

Active MCPs in generation pipeline:
- **Wikipedia MCP** (Kiwix local or Wikipedia API) — used for factual grounding of textbook content
- **YouTube Transcript MCP** — used as seed text for lesson notes (transcripts only, no video)

---

## Related Workflows

| Workflow | Trigger | What it does |
|----------|---------|-------------|
| `stub-aku-content.yml` | Manual | Initialise Aku-Content repo structure |
| `migrate-aku-content-full.yml` | Manual | Push content files to Aku-Content |
| `stub-akudemy-exam-papers.yml` | Manual | Stub exam papers in Akudemy |
| `generate-jss-content-starters.yml` | Manual | Run generators + PR to Aku-Content |
