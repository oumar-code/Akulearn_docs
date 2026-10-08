# Multi-Service Demo Architecture: N-ATLAS Integration

## Overview

This document outlines how three core Aku Platform services consume N-ATLAS as their unified AI backbone. The demo showcases voice-first, multilingual workflows across education, productivity, and connectivity sectors.

### Services Covered

1. **Akudemy** - Education platform with voice Q&A
2. **AkuWorkspace** - Productivity suite with document generation and voice summaries
3. **Aku-Telhone** - Connectivity service with voice authentication

### Key Capabilities Demonstrated

- Voice-to-text (ASR) and text-to-voice (TTS) integration
- Multilingual support (English, Hausa, Yoruba)
- Real-time inference with <500ms latency
- Offline fallback to quantized models on EdgeHub

---

## 1. Akudemy: Voice-First Learning

### Use Case

A student in a low-connectivity zone asks a curriculum question in Hausa via voice. The system processes the question, retrieves relevant educational content, and responds in voice.

### Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         AKUDEMY FLOW                            │
└─────────────────────────────────────────────────────────────────┘

   Student Voice Input (Hausa)
          │
          │ "Menene photosynthesis?"
          │
          ▼
   ┌──────────────────┐
   │  ASR (Whisper)   │  ← Detects Hausa language
   │  Model Inference │
   │  ~50ms           │
   └────────┬─────────┘
            │
            │ Hausa Text: "Menene photosynthesis?"
            │
            ▼
   ┌──────────────────────────────────────────┐
   │       Akudemy Service Layer              │
   │  • Curriculum matching (Biology)          │
   │  • Student profile context (Age 15)       │
   │  • Language locale (Hausa)                │
   └────────┬──────���──────────────────────────┘
            │
            │ Enhanced prompt + context
            │
            ▼
   ┌──────────────────────────────────────┐
   │     AkuAI Proxy (FastAPI)            │
   │  POST /v1/infer                      │
   │  • prompt: curriculum question       │
   │  • language: "ha"                    │
   │  • model_version: "education-v1.2"  │
   │  • session_id: "student_101"        │
   └────────┬───────────────────────────┘
            │
            │ Route to education-tuned
            │ N-ATLAS model
            │
            ▼
   ┌──────────────────────────────────┐
   │   N-ATLAS Backbone               │
   │  (SuperHub fine-tuned)           │
   │  Response: "Photosynthesis       │
   │   nimé ilé wẹ̀ ti lo..." (Yoruba)│ ← Generated in Hausa
   │  Latency: ~310ms                 │
   └────────┬────────────────────────┘
            │
            │ Structured response
            │
            ▼
   ┌──────────────────────────────────┐
   │   AkuAI Response Processing       │
   │  • Validate output quality        │
   │  • Extract summary text           │
   │  • Rate-limit check (Sentinel)    │
   └────────┬────────────────────────┘
            │
            │ Clean Hausa text output
            │
            ▼
   ┌──────────────────┐
   │  TTS (Piper)     │  ← Hausa voice synthesis
   │  Voice Gen       │
   │  ~100ms          │
   └────────┬─────────┘
            │
            │ Audio stream (MP3/WAV)
            │
            ▼
   Student Hears Response (Hausa Voice)
   "Photosynthesis jiya ne ilé wẹ̀..."

   ┌─────────────────────────────────────┐
   │  TOTAL LATENCY: ~460ms (< 500ms ✓)  │
   └─────────────────────────────────────┘
```

### Service Integrations

| Component | Purpose | Latency |
|-----------|---------|---------|
| ASR (Whisper) | Convert voice → text | ~50ms |
| Akudemy Service | Curriculum context + student profile | ~40ms |
| AkuAI Proxy | N-ATLAS routing + load balancing | ~30ms |
| N-ATLAS Model | Education-tuned inference | ~310ms |
| TTS (Piper) | Convert text → voice | ~100ms |
| **Total** | **End-to-end voice response** | **~530ms** |

### Fallback Scenario

If N-ATLAS latency exceeds 500ms or model is unavailable:

```
N-ATLAS Timeout (>800ms)
        │
        ▼
AkuAI Proxy Fallback Logic
        │
        ▼
Route to Gemma Fallback Model
        │
        ▼
Return response in Hausa
        │
        ▼
TTS synthesis to voice
        │
        ▼
Student hears response (slightly lower quality, but functional)
```

### Key Metrics

- **Pilot Users:** 50 students
- **Target Latency:** 2–3 seconds (end-to-end, including network)
- **Language Accuracy:** ≥85% (ASR + NLU)
- **User Satisfaction:** ≥4/5 stars
- **Success Metric:** 40%+ faster response times vs. Gemma baseline

---

## 2. AkuWorkspace: Document Generation + Voice Summary

### Use Case

A farmer uses AkuWorkspace to generate a crop yield report. He speaks the request ("Generate crop yield report for Q3 in Hausa"), the system generates a multilingual document, and reads a voice summary back.

### Data Flow

```
┌────────────────────────────────────────────────────────┐
│            AKUWORKSPACE FLOW                           │
└────────────────────────────────────────────────────────┘

Farmer Voice Request (Hausa)
│
│ "Jawo crop yield report na Q3"
│
▼
┌──────────────────┐
│  ASR (Whisper)   │  ← Hausa detection
│                  │
└────────┬─────────┘
         │
         │ Hausa Text: "Generate crop yield report for Q3"
         │
         ▼
┌───────────────────────────────────────────┐
│   AkuWorkspace Service Layer              │
│  • Detect intent: "report generation"     │
│  • Context: farmer profile, region (N/A)  │
│  • Data source: Aku-DaaS (historical data)│
│  • Language: Hausa                        │
└────────┬────────────────────────────────┘
         │
         │ Structured request
         │
         ▼
┌────────────────────────────────────────┐
│     AkuAI Proxy                        │
│  POST /v1/infer                        │
│  • prompt: template("report",          │
│            sector="agriculture",       │
│            region="north")            │
│  • language: "ha"                     │
│  • model_version: "agriculture-v1.2" │
│  • max_tokens: 1000 (longer output)   │
└────────┬───────────────────────────────┘
         │
         │ Route to agriculture model
         │
         ▼
┌────────────────────────────────────────┐
│   N-ATLAS (Agriculture Fine-tuned)    │
│                                        │
│  Generated Report:                     │
│  "Rahotannin Shuka Q3:                │
│   • Kumma: 45% (waje da fada 5%)     │
│   • Mijebi: 60% (karya 2%)            │
│   • Zafon: 55% (gida)                │
│   • Jiya: 38% (karfi 8%)              │
│   • Shuni: 52% (mafi kyau)"           │
│                                        │
│  Latency: ~350ms                      │
└────────┬─────────────────────────────┘
         │
         │ Raw text output
         │
         ▼
┌────────────────────────────────────────┐
│   Document Generation Service          │
│  • Format: PDF/Markdown                │
│  • Language: Hausa (primary)           │
│  • Add charts/tables from Aku-DaaS    │
│  • Generate timestamp, ID              │
│  Latency: ~150ms                       │
└────────┬────────────────────────────────┘
         │
         │ Formatted document
         │
    ┌────┴──────────────────┐
    │                       │
    ▼                       ▼
Store Document         Extract Summary
(PDF/Markdown)         for Voice
    │                       │
    │                       │ "Q3 crop summary: yields
    │                       │  ranged 38-60%..."
    │                       │
    │                       ▼
    │              ┌──────────────────┐
    │              │  TTS (Piper)     │
    │              │  Voice Summary   │
    │              │  ~120ms          │
    │              └────────┬─────────┘
    │                       │
    │                       ▼
    │              Farmer Hears Summary (Hausa Voice)
    │              "Rahotannin shuka Q3:..."
    │
    ▼
  Farmer Downloads Report PDF
  (In Hausa + English options)

┌─────────────────────────────────────────────┐
│ TOTAL LATENCY: ~620ms (document ready)      │
│ SUMMARY VOICE: ~650ms (voice heard)         │
└─────────────────────────────────────────────┘
```

### Service Integrations

| Component | Purpose | Latency |
|-----------|---------|---------|
| ASR (Whisper) | Voice → text | ~50ms |
| AkuWorkspace Intent Detection | Parse report request | ~60ms |
| AkuAI Proxy | Route to agriculture model | ~30ms |
| N-ATLAS (Agriculture) | Generate report content | ~350ms |
| Document Formatter | Create PDF/Markdown | ~150ms |
| Summary Extraction | Extract key points | ~40ms |
| TTS (Piper) | Convert summary → voice | ~120ms |
| **Total (Document)** | **Ready for download** | **~620ms** |
| **Total (Voice Summary)** | **Voice heard by user** | **~650ms** |

### Fallback Scenario

If agriculture model is unavailable:

```
Agriculture Model Timeout
        │
        ▼
AkuAI Proxy routes to Default N-ATLAS
        │
        ▼
Generate report (generic quality, still multilingual)
        │
        ▼
Document generated, summary voiced
        │
        ▼
Farmer still gets functional output (quality alert logged)
```

### Key Metrics

- **Pilot Users:** 20 farmers
- **Target Latency:** Document generation < 800ms
- **Document Quality:** ≥4/5 relevance score
- **Voice Summary Clarity:** ≥4/5 user rating
- **Success Metric:** Enable data-driven farming decisions via natural language

---

## 3. Aku-Telhone: Voice Authentication

### Use Case

A user needs to activate an eSIM on their device. Instead of typing confirmation codes, they use voice authentication in their local language.

### Data Flow

```
┌──────────────────────────────────────────┐
│         AKU-TELHONE FLOW                 │
└──────────────────────────────────────────┘

User Receives Voice Prompt
│
│ IVR: "Say YES in Hausa to confirm eSIM activation"
│      "Ka ce EH a Hausa don kwashe eSIM"
│
▼
┌──────────────────────────────────────────┐
│ User Voice Response (in Hausa)           │
│ "EH" (Yes) or "A'a" (No)                 │
└────────┬─────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  ASR (Whisper - Hausa Tuned)     │
│  Language: Hausa                 │
│  Intent: Binary (Yes/No)         │
│  Latency: ~60ms                  │
└────────┬────────────────────────┘
         │
         │ Recognized text: "EH"
         │ Confidence: 94%
         │
         ▼
┌──────────────────────────────────────────┐
│    AkuAI Proxy                           │
│  POST /v1/infer                          │
│  • prompt: "User said: 'EH' in Hausa.    │
│              Confirm eSIM activation?"   │
│  • language: "ha"                        │
│  • model_version: "default"              │
│  • max_tokens: 10 (short response)       │
└────────┬───────────────────────────────┘
         │
         │ Route to default N-ATLAS
         │
         ▼
┌──────────────────────────────────┐
│    N-ATLAS Model                 │
│  Response: "CONFIRMED"           │
│  Latency: ~150ms (shorter prompt)│
└────────┬────────────────────────┘
         │
         │ Parsed response: CONFIRMED
         │
         ▼
┌──────────────────────────────────┐
│ Aku-Telhone Service Logic        │
│  • Validate confidence > 90%     │
│  • Cross-check user account      │
│  • Log voice auth event (audit)  │
│  • Trigger eSIM activation       │
│  Latency: ~50ms                  │
└────────┬────────────────────────┘
         │
         │ eSIM activated
         │
         ▼
┌──────────────────────────────────┐
│  Confirmation TTS (Piper)        │
│  Message: "eSIM activated        │
│            successfully"          │
│  Language: Hausa                 │
│  Latency: ~80ms                  │
└────────┬────────────────────────┘
         │
         │ Audio stream
         │
         ▼
User Hears Confirmation (Hausa Voice)
"eSIM jiya ne kwashe kuma daidai"

┌─────────────────────────────────┐
│ TOTAL LATENCY: ~340ms           │
│ SUCCESS RATE TARGET: >95%        │
└─────────────────────────────────┘
```

### Service Integrations

| Component | Purpose | Latency |
|-----------|---------|---------|
| IVR System | Voice prompt to user | (network-dependent) |
| ASR (Whisper) | Voice → binary intent | ~60ms |
| AkuAI Proxy | Route to N-ATLAS | ~20ms |
| N-ATLAS Model | Confirm intent | ~150ms |
| Aku-Telhone Logic | Validate + activate eSIM | ~50ms |
| TTS (Piper) | Confirmation voice | ~80ms |
| **Total** | **End-to-end voice auth** | **~360ms** |

### Fallback Scenario

If N-ATLAS response is unclear or confidence is low:

```
ASR confidence < 85%
        │
        ▼
Prompt user to repeat: "Please say YES or NO again"
        │
        ▼
Re-run ASR + N-ATLAS confirmation
        │
        ▼
If still unclear after 2 attempts:
        ├─ Fall back to USSD/SMS confirmation
        └─ Log attempt for manual review
```

### Key Metrics

- **Pilot Users:** 20 connectivity testers
- **Target Success Rate:** ≥95% (voice auth accepted)
- **Target Latency:** <100ms inference (< 200ms total)
- **Accuracy:** ≥99% on Yes/No binary intent
- **Language Support:** Hausa, Yoruba, English
- **Accessibility Impact:** Voice-first eliminates typing barrier

---

## 4. Cross-Service Data & Telemetry

### Unified Telemetry Pipeline

All three services emit structured telemetry to **Aku-Sentinel** for monitoring:

```
┌────────────────────────────────────────┐
│         Akudemy Service                │
│  Emits: { service: "akudemy",          │
│           model: "education-v1.2",     │
│           latency_ms: 460,             │
│           language: "ha",              │
│           fallback_used: false }       │
└────────┬────────────────────────────────┘
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌──────────────────┐  ┌──────────────────┐
│ AkuWorkspace     │  │ Aku-Telhone      │
│ Telemetry        │  │ Telemetry        │
│ (sector model)   │  │ (binary intent)  │
└────────┬─────────┘  └────────┬─────────┘
         │                     │
         └──────���───┬──────────┘
                    │
                    ▼
        ┌─────────────────────────────┐
        │   Aku-Sentinel             │
        │  (Centralized Monitoring)  │
        │                            │
        │  Dashboards:              │
        │  • Latency heatmaps       │
        │  • Model version usage    │
        │  • Language distribution  │
        │  • Fallback rate (<5%)    │
        │  • Service SLA (99.9%)    │
        └────────────────────────────┘
```

### Key Telemetry Metrics

| Metric | Target | Responsible Service |
|--------|--------|---------------------|
| End-to-end latency | <500ms (cloud) | AkuAI Proxy |
| Fallback rate | <5% | N-ATLAS + Gemma |
| Service uptime | 99.9% | Aku-Sentinel |
| Language accuracy (ASR) | ≥85% | Whisper / AkuAI |
| Voice synthesis quality | ≥4/5 user rating | Piper TTS |
| Model version distribution | Tracked per service | IGHub Gateway |

---

## 5. Deployment Timeline (20-Week Roadmap Context)

### Phase 1 (Weeks 1–4): Foundation
- ✅ AkuAI N-ATLAS migration (proxy layer)
- ✅ EdgeHub quantization (offline fallback)
- ✅ SDK + Contracts (Pydantic, Kafka)

### Phase 2 (Weeks 5–10): Multi-Service Voice Integration
- 📍 **Akudemy voice-first learning** (50 students)
- 📍 **AkuWorkspace document generation** (20 farmers)
- 📍 **Aku-Telhone voice auth** (20 testers)
- ✅ ASR/TTS pipeline integration
- ✅ Multilingual prompt templates

### Phase 3 (Weeks 11–16): Sectoral Fine-Tuning
- Fine-tuned models deployed for each service
- EdgeHub OTA sync for quantized models
- IGHub version routing

### Phase 4 (Weeks 17–20): Validation & NAIC
- Pilot metrics collected and analyzed
- Real-world user feedback validated
- NAIC submission with demo outputs

---

## 6. Demo Success Criteria

| Service | Demo Scenario | Success Metric |
|---------|---------------|----------------|
| **Akudemy** | Student asks curriculum Q in Hausa voice | Response in <2.5s; accuracy ≥85%; user satisfaction ≥4/5 |
| **AkuWorkspace** | Farmer requests Q3 crop report in voice | Document generated <1s; relevance ≥4/5; voice summary clear |
| **Aku-Telhone** | User confirms eSIM activation by voice | Auth success >95%; latency <200ms; no false positives |

---

## 7. Architecture Diagram (Text-Based)

```
┌─────────────────────────────────────────────────────────────────┐
│                      DEMO SERVICES LAYER                        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │  Akudemy     │  │  AkuWorkspace    │  │  Aku-Telhone     │ │
│  │  (Edu)       │  │  (Productivity)  │  │  (Connectivity)  │ │
│  └──────┬───────┘  └────────┬─────────┘  └────────┬─────────┘ │
│         │                   │                     │             │
│         └───────────────────┼─────────────────────┘             │
│                             │                                  │
└─────────────────────────────┼──────────────────────────────────┘
                              │
                   ┌──────────▼──────────┐
                   │   AkuAI Proxy      │
                   │  (FastAPI)         │
                   │  • Routing         │
                   │  • Fallback logic  │
                   │  • Telemetry       │
                   └──────────┬─────────┘
                              │
                   ┌──────────▼──────────┐
                   │   N-ATLAS Backbone │
                   │  • Default model   │
                   │  • Edu model       │
                   │  • Agriculture mdl │
                   └──────────┬─────────┘
                              │
                   ┌──────────┴──────────┐
                   │                    │
        ┌──────────▼──────────┐  ┌─────▼─────────────┐
        │  ASR/TTS Pipeline  │  │  EdgeHub Fallback │
        │  • Whisper ASR     │  │  • Quantized <500MB
        │  • Piper TTS       │  │  • OTA sync       │
        │  • Multilingual    │  │  • Offline mode   │
        └────────────────────┘  └───────────────────┘
```

---

## 8. Next Steps

1. **Weeks 5–6**: Set up Akudemy voice pipeline (ASR + N-ATLAS + TTS integration)
2. **Weeks 7–8**: Deploy AkuWorkspace report generation with agriculture model
3. **Weeks 9–10**: Integrate Aku-Telhone voice authentication flow
4. **Week 10**: Begin real-world pilot with 90 total users (50 + 20 + 20)
5. **Weeks 11–16**: Collect telemetry, fine-tune models based on pilot feedback
6. **Weeks 17–20**: Validate metrics, prepare NAIC submission with demo outputs

---

**Document Owner:** Product & AI Teams  
**Last Updated:** 2026-10-08  
**Status:** Ready for demo implementation roadmap
