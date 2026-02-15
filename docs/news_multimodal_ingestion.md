# BBC/VOA News Ingestion for Multi-Modal Lessons

Purpose: ingest reputable news to pair text, images, and audio for Hausa/Igbo/Yoruba enrichment in lessons.

## Feeds (preferred)
- BBC Hausa RSS: `https://www.bbc.com/hausa/index.xml`
- BBC Yoruba RSS: `https://www.bbc.com/yoruba/index.xml`
- BBC Igbo RSS: `https://www.bbc.com/igbo/index.xml`
- VOA Hausa RSS: `https://www.voahausa.com/podcast/?count=50`
- VOA Yoruba RSS: `https://www.voayoruba.com/podcast/?count=50`
- VOA Igbo RSS: `https://www.voaigbo.com/podcast/?count=50`
- Global Voices (multi-lang): `https://globalvoices.org/feed/`

Use feeds first; avoid full-site crawling unless necessary.

## Data to capture per article
- URL, title, publish date, language
- Text body (strip HTML, preserve paragraphs)
- Images: URL, caption, alt-text if present
- Audio: URL (for VOA podcasts), duration if available
- Source attribution (publisher, link)

## Minimal pipeline sketch
1) Fetch RSS → parse items → queue URLs
2) For each URL: GET HTML with polite headers + 2-3s backoff
3) Extract main article text (readability/boilerplate clean) and media URLs
4) Store JSON record; example path: `content/news_raw/<lang>/YYYY/MM/DD/<slug>.json`
5) Optional: download images/audio to `content/news_media/...` with hash filenames
6) Enrich: auto-translate to English if source is Hausa/Igbo/Yoruba; keep original
7) Align for lessons: map articles to lesson topics and generate 1-2 comprehension questions

## Compliance and safety
- Respect robots.txt; stick to RSS-linked pages
- Set User-Agent and add contact email if possible
- Rate limit: max ~5 requests/minute per domain
- Cache responses to avoid re-fetching

## Suggested tooling
- HTTP: `requests`, `httpx`
- Parsing: `feedparser`, `readability-lxml`, `beautifulsoup4`
- Media download: `aiohttp` (async) or `requests` (small scale)
- Translation: reuse `translate_lessons.py` pipeline/model

## Future multi-modal alignment
- Use article images with captions as image-text pairs
- For VOA podcasts: pair audio with transcript if present; otherwise run ASR before use
- Store metadata linking lesson ID ⇄ news item ID for traceability
