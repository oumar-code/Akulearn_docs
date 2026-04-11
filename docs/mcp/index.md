# MCP Strategy — Aku Platform Content Pipeline

**MCP** = Model Context Protocol — tools that give AkuAI access to external data sources during
content generation and tutoring.

This document defines the MCP selection strategy, priority, and integration plan.

---

## Decision Framework

| MCP | Value | Copyright risk | Offline-compatible | Decision |
|-----|-------|---------------|-------------------|---------|
| **Wikipedia** (Kiwix/API) | High — authoritative, encyclopaedic | ✅ CC-BY-SA free | ✅ via .zim | **Add now** |
| **YouTube Transcripts** (transcript-only) | High — explains concepts in accessible language | ✅ transcripts are fair use | ❌ requires download step | **Add now** (text only) |
| **Khan Academy OER** | High — structured curriculum-aligned | ✅ CC-BY-NC-SA free | ❌ requires sync | **Add now** |
| **NERDC Curriculum PDFs** | Critical — official syllabus / LO source | ✅ Government publication | ✅ once downloaded | **Add now** |
| **Google Books API** | Medium — reference textbooks | ⚠️ Fair use complex | ❌ | **Later** |
| **YouTube video download** | Low (text already covered) | ❌ Copyright violation | ❌ | **Do NOT add** |
| **Twitter/X** | Low | ⚠️ Terms of Service | ❌ | **Skip** |
| **News APIs** (BBC Hausa/Yoruba, Premium Times) | Medium — contextual, multilingual | ⚠️ Check T&C | ❌ | **Phase 2** |

---

## Priority 1 MCPs — Add Now

### 1. Wikipedia MCP

**Implementation**: Two modes depending on connectivity:

**Mode A — Online** (AkuAI with internet access):
```python
# AkuAI tool definition
wikipedia_tool = {
    "name": "wikipedia_search",
    "description": "Search Wikipedia for factual information to ground textbook content",
    "input_schema": {
        "query": {"type": "string"},
        "language": {"type": "string", "enum": ["en", "ha", "yo"], "default": "en"},
        "max_results": {"type": "integer", "default": 3},
    }
}
```

**Mode B — Offline** (Kiwix server — preferred for edge hubs):
```python
# Calls local kiwix-serve REST API
KIWIX_BASE_URL = os.getenv("KIWIX_API_URL", "http://kiwix.local:8080/search")
```

**Download command** (one-time setup):
```bash
wget https://download.kiwix.org/zim/wikipedia/wikipedia_en_school_maxi.zim \
    -O content/offline/wikipedia_school_en.zim

# Nigerian-language Wikipedias:
wget https://download.kiwix.org/zim/wikipedia/wikipedia_ha_all_maxi.zim \
    -O content/offline/wikipedia_ha.zim  # Hausa
wget https://download.kiwix.org/zim/wikipedia/wikipedia_yo_all_maxi.zim \
    -O content/offline/wikipedia_yo.zim  # Yoruba
```

**Integration point**: `AkuAI → app/tools/wikipedia_tool.py`
See: `docs/mcp/wikipedia-mcp.md`

---

### 2. YouTube Transcript MCP

**Principle**: Extract **transcripts only** — no video download or storage.
This is legally safe (transcripts are text; the tool reads publicly available CC/educational captions).

**Use case**: Find popular YouTube explanations of JSS/SS topics; use the transcript as
seed text for AkuTutor lesson notes and textbook chapters.

**Implementation**:
```python
# Uses youtube-transcript-api (MIT licensed)
# pip install youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id: str, language: str = "en") -> str:
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
    return " ".join(entry["text"] for entry in transcript)
```

**Curated channel list** (Nigerian education):
- `@MathandScienceSchool`
- `@NigerianSchoolTV`
- `@PassNGExams`
- `@CBTNaija`
- Khan Academy (all subjects)
- BBC Learning English

**Integration point**: `AkuAI → app/tools/youtube_transcript_tool.py`
See: `docs/mcp/youtube-transcript-mcp.md`

---

### 3. Khan Academy OER MCP

**Source**: Khan Academy Content API + Open Content JSON dumps
**License**: CC-BY-NC-SA 4.0

**Curriculum alignment**:
- KA Grade 6–8 → JSS1–JSS3 (approximate match)
- KA High School → SS1–SS3

**Implementation**:
```bash
# Khan Academy provides content tree dumps
curl "https://www.khanacademy.org/api/v1/topic/math" \
    > data/khan_academy/math_tree.json
```

**Integration point**: `pipeline/khan_academy_importer.py` (to be created in Phase 2)

---

### 4. NERDC Curriculum PDF Parser MCP

**Source**: NERDC official syllabus PDFs (available from Federal Ministry of Education)
**License**: Government publication — public domain in Nigeria

**Purpose**: Extract official Learning Outcomes → generate `content/lo_catalog.json` entries

**Implementation**:
```bash
# One-time download from FME portal
wget https://fme.gov.ng/nerdc/curriculum/jss_curriculum.pdf \
    -O data/curricula/nerdc_jss_curriculum.pdf
```

**Parser**: `pipeline/nerdc_curriculum_parser.py` — extracts topics, LOs and competency statements
(to be created in Phase 2)

---

## Priority 2 MCPs — Phase 2

### 5. News Corpus MCPs

For multilingual content and Nigerian context:

| Source | Language | Type | API/Access |
|--------|---------|------|-----------|
| BBC Hausa | Hausa | News text | RSS feed (free) |
| BBC Yoruba | Yoruba | News text | RSS feed (free) |
| Premium Times | English | Nigerian news | RSS feed (free) |
| VOA Hausa | Hausa | News audio + text | RSS / API |
| Dailytrust.com | English/Hausa | News | RSS |

**Use case**: Populate `content/news_corpus/` for language learning and current affairs modules.

---

## MCP Architecture in AkuAI

```
AkuAI (FastAPI at port 8004)
├── app/
│   ├── tools/
│   │   ├── wikipedia_tool.py      ← Wikipedia MCP (Priority 1)
│   │   ├── youtube_transcript_tool.py  ← YouTube Transcript MCP (Priority 1)
│   │   ├── khan_academy_tool.py   ← Khan Academy MCP (Priority 2)
│   │   └── nerdc_parser_tool.py   ← NERDC Curriculum MCP (Priority 1)
│   └── routers/
│       └── tools.py               ← /tools endpoint exposes all MCPs
└── config/
    └── tools.yaml                 ← Enable/disable MCPs per environment
```

**Tool registration** (in AkuAI `app/main.py`):
```python
from app.tools import wikipedia_tool, youtube_transcript_tool

# Register with the LLM system prompt as available tools
AVAILABLE_TOOLS = [wikipedia_tool, youtube_transcript_tool]
```

---

## What NOT to Do

❌ **Do not add YouTube video download** — copyright violation, massive storage cost
❌ **Do not add Google Books API** for full-text — fair use does not cover complete textbooks
❌ **Do not scrape exam board sites directly** without legal review
❌ **Do not store personally identifiable social media content**

---

## Implementation Order

| Day | Action |
|-----|--------|
| Day 1 | Download Wikipedia .zim files (offline content ready immediately) |
| Day 2 | Implement `wikipedia_tool.py` in AkuAI — wire to Kiwix local server |
| Day 3 | Implement `youtube_transcript_tool.py` — test with 10 JSS topic videos |
| Day 4 | Wire both MCPs to textbook_generator.py (`--use-mcp` flag) |
| Week 2 | NERDC curriculum PDF parser |
| Week 3 | Khan Academy OER importer |
| Month 2 | News corpus MCPs (Hausa, Yoruba) |

---

## Related Files

- `docs/mcp/wikipedia-mcp.md` — Wikipedia MCP specification
- `docs/mcp/youtube-transcript-mcp.md` — YouTube Transcript MCP specification
- `pipeline/textbook_generator.py` — uses MCPs for grounding
- `docs/ecosystem-map.md` — AkuAI service role in the platform
