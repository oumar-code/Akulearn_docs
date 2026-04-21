# News Multimodal Ingestion

## Objective
Build a compliant ingestion pipeline that converts trusted news sources into multilingual multimodal assets (text, image, audio) usable for Akulearn lessons and AI training.

## Source Strategy
Use feed-first ingestion from reputable sources:
- BBC Hausa/Yoruba/Igbo RSS
- VOA Hausa/Yoruba/Igbo RSS
- Global Voices feed

Rules:
- Prefer RSS-linked pages over full-site crawling.
- Respect robots.txt and publisher terms.
- Store source attribution in every record.

## Ingestion Workflow

## 1) Feed Collection
- Poll feeds on schedule.
- Parse entries and deduplicate by canonical URL/hash.
- Push unseen items into processing queue.

## 2) Article Extraction
- Fetch article HTML with polite rate limiting.
- Extract clean body text, title, publish date, author (if available).
- Preserve language and source metadata.

## 3) Media Extraction
- Capture image URLs, captions, alt text.
- Capture audio URLs (especially podcasts) and duration metadata.
- Optionally download media to managed storage with content hashes.

## 4) Structuring and Storage
Store normalized records (example):
- `content/news_raw/<lang>/YYYY/MM/DD/<slug>.json`
- Optional media path: `content/news_media/<lang>/YYYY/MM/DD/<hash>.<ext>`

Record fields:
- `id`, `source`, `url`, `language`, `published_at`
- `title`, `body_paragraphs[]`
- `images[]` (url, caption, alt)
- `audio[]` (url, duration, transcript_status)
- `license`, `ingested_at`, `checksum`

## 5) Enrichment
- Translate content to English where needed (while retaining original).
- Run language verification and safety filtering.
- Generate metadata tags (topic, subject relevance, grade relevance).

## 6) Multimodal Alignment
- Build text-image pairs from article sections and captions.
- Build audio-text pairs from podcast transcripts or ASR output.
- Link each news item to lesson topics and learning objectives.

## 7) Lesson Integration
- Generate comprehension prompts/questions from aligned content.
- Store traceability links: lesson ID ↔ news ID.
- Mark suitability by age/grade and difficulty.

## Reliability and Operations
- Queue-based processing with retry/backoff.
- Domain-level rate limits (e.g., <=5 req/min/domain).
- Idempotent upserts to avoid duplicates.
- Dead-letter queue for persistent parsing failures.

## Compliance and Safety
- Preserve attribution and publisher metadata.
- Keep licensing field explicit and enforce usage constraints.
- Sensitive personal data handling:
  - Redact direct contact details (phone numbers, email addresses, exact home addresses).
  - Redact government identifiers where present.
  - Redact exposed account numbers or payment identifiers.
  - Keep person names in editorial/news context unless policy requires additional masking.
- Maintain audit logs for ingestion and transformation steps.

## Quality Gates
- Minimum text extraction completeness.
- Media URL validity checks.
- Language confidence threshold.
- Safety/moderation pass before downstream use.

## Suggested Tooling
- HTTP: `httpx` / `requests`
- Feeds: `feedparser`
- Extraction: `readability-lxml`, `beautifulsoup4`
- Async media download: `aiohttp`
- Optional transcript/ASR integration for podcast audio

## KPIs
- New items ingested per day by language/source
- Extraction success rate
- Duplicate rate
- Enrichment latency
- Multimodal alignment coverage
- Lesson reuse rate of ingested items

## Definition of Done
- Feed-to-storage ingestion is automated and reliable.
- Text, image, and audio metadata are captured with attribution.
- Enriched records are linked to lessons with traceability.
- Quality, safety, and compliance gates are enforced in pipeline execution.
