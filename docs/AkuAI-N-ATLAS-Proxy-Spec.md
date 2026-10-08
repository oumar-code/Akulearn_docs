# AkuAI N-ATLAS Proxy Specification

## 1. Overview

This specification defines the migration of AkuAI from its current Gemma-based inference wrapper to an N-ATLAS-based inference architecture while preserving backward compatibility for all existing services. The goal is to deliver a drop-in replacement that supports the same API contract, request patterns, and orchestration flow with improved multilingual performance, voice-ready inference, and production reliability.

### Background

AkuAI currently exposes a Gemma-based inference wrapper used by multiple platform services, including:
- Akudemy
- AkuTutor
- AkuWorkspace
- Aku-Telhone
- Aku-EdgeHub and regional integrations
- Aku-IGHub routing and service orchestration

The new N-ATLAS proxy layer will act as the single inference surface across the Aku ecosystem while preserving compatibility for internal clients that depend on the present Gemma wrapper behavior.

### Design Goals

- Maintain a drop-in replacement interface for all existing Gemma consumers
- Enable multilingual inference across English, Hausa, and Yoruba
- Support fast fallback to the Gemma model when N-ATLAS latency or quality thresholds are not met
- Standardize telemetry, observability, and model version tracking
- Prepare for future sector-specific model routing (education, agriculture, health, governance)

### Non-Goals

- Full replacement of all service-specific orchestration logic
- Direct modification of downstream application business logic beyond inference call interfaces
- Introducing new request payloads that break existing clients without compatibility shims

---

## 2. API Interface

### 2.1 Existing Interface (Current Gemma Wrapper)

The existing wrapper exposes a generic inference endpoint that may look like the following:

```json
POST /v1/infer
{
  "prompt": "Explain photosynthesis in simple language",
  "max_tokens": 200,
  "temperature": 0.7,
  "top_p": 0.9,
  "stream": false
}
```

Example response:

```json
{
  "request_id": "req_123",
  "output": "Photosynthesis is the process by which plants ...",
  "model": "gemma-2b",
  "latency_ms": 420,
  "tokens_used": 87
}
```

### 2.2 Target Interface (N-ATLAS Compatible)

The N-ATLAS wrapper will provide a drop-in compatible contract, preserving the same core fields while allowing additional metadata for model versioning and multilingual routing.

#### Request Schema

```json
POST /v1/infer
{
  "prompt": "Explain photosynthesis in simple language",
  "context": null,
  "max_tokens": 200,
  "temperature": 0.7,
  "top_p": 0.9,
  "stream": false,
  "language": "en",
  "model_version": "default",
  "session_id": "student_101"
}
```

#### Response Schema

```json
{
  "request_id": "req_123",
  "output": "Photosynthesis is the process by which plants ...",
  "model": "n-atlas-default",
  "model_version": "v1.2",
  "language": "en",
  "latency_ms": 310,
  "tokens_used": 82,
  "fallback_used": false,
  "provider": "n-atlas",
  "status": "success"
}
```

### 2.3 Compatibility Rules

The proxy layer must support the following compatibility behaviors:

- Legacy clients that send only `prompt`, `max_tokens`, `temperature`, and `top_p` must continue to work
- If `language` is missing, default to the service locale or English
- If `model_version` is missing, use the default production N-ATLAS model
- If the request includes a stream flag, the proxy should either stream the response or return the non-stream variant through a compatibility wrapper
- If the request contains a custom `model` name set to `gemma`, the proxy should map it to the fallback engine without changing the client contract

### 2.4 Health and Readiness Endpoints

The proxy should also expose standard operational endpoints:

- `GET /healthz`
- `GET /readyz`
- `GET /v1/models`
- `GET /metrics`

Example model metadata response:

```json
{
  "models": [
    {
      "name": "n-atlas-default",
      "version": "v1.2",
      "status": "active",
      "language_support": ["en", "ha", "yo", "ig"],
      "provider": "n-atlas"
    },
    {
      "name": "gemma-fallback",
      "version": "v1.0",
      "status": "active",
      "provider": "gemma"
    }
  ]
}
```

---

## 3. Inference Pipeline

### 3.1 Request Lifecycle

The proxy layer will route inference requests through the following lifecycle:

1. Validate request schema and compatibility fields
2. Normalize language, model version, and safety controls
3. Determine the active model based on route policy and traffic rules
4. Send the request to the selected backend
5. Measure latency, token usage, and error rate
6. Evaluate fallback conditions
7. Return normalized response to the caller

### 3.2 Model Selection Logic

The model selection algorithm is as follows:

```text
if request includes explicit model_version:
    route to named N-ATLAS model
elif request indicates offline/edge mode:
    route to quantized regional model
elif request language not in cloud primary support:
    route to multilingual N-ATLAS model
elif latency threshold is exceeded or backend health is degraded:
    fallback to Gemma
else:
    route to default N-ATLAS model
```

### 3.3 Fallback Strategy

The service must support a robust fallback mechanism to avoid downtime and preserve quality across deployments.

#### Primary Fallback Condition Matrix

| Condition | Action | Result |
|-----------|--------|--------|
| N-ATLAS healthy and latency < 500ms | Use N-ATLAS | Normal operation |
| N-ATLAS timeout or 5xx errors | Switch to Gemma fallback | Graceful degradation |
| Language-specific model unavailable | Use default multilingual N-ATLAS | Maintain functionality |
| Low-resource edge request | Use quantized edge model | Faster offline inference |
| N-ATLAS quality below threshold | Use fallback with quality alert | Safety and reliability |

### 3.4 Telemetry Requirements

Every request should emit structured telemetry with:

- request_id
- service_name
- model_name
- model_version
- language
- latency_ms
- tokens_used
- error_code
- fallback_used
- status
- timestamp

This telemetry will be consumed by Aku-Sentinel and the platform monitoring stack for SLA validation.

---

## 4. Multi-language Support (English → Hausa/Yoruba)

### 4.1 Language Requirements

AkuAI must support multilingual input and output across at least the following categories:
- English
- Hausa
- Yoruba
- Igbo (future-ready)

### 4.2 Request Language Normalization

The proxy should normalize the request language using a language code map:

```json
{
  "en": "english",
  "ha": "hausa",
  "yo": "yoruba",
  "ig": "igbo"
}
```

### 4.3 Response Behavior

If a client sends:

```json
{
  "prompt": "Gano abin da ya sa shuka ya bushe",
  "language": "ha"
}
```

The proxy must route to the Hausa-capable N-ATLAS model and return the output in Hausa where possible, while preserving factual accuracy and context.

### 4.4 Translation / Context Handling

For cross-language service contexts:
- If input is in Hausa but the service expects English reasoning, use a contextual translation layer inside the proxy
- If no language is specified but the originating service is known to be Yoruba, default to `yo`
- Preserve user intent during translation while minimizing hallucination risk

### 4.5 Prompt Formatting Rules

The proxy should apply language-aware system prompts, for example:

```text
System: You are a helpful AI assistant for Nigerian public services. Respond in Hausa when the user request language is Hausa. Be concise, clear, and culturally appropriate.
```

This helps ensure the response quality remains contextual and appropriate for education, governance, and productivity use cases.

---

## 5. Integration Points

The AkuAI N-ATLAS proxy is designed to be the shared inference layer across several services.

### 5.1 AkuTutor

Use cases:
- adaptive question answering
- multilingual feedback generation
- hint generation in local languages
- tutoring path optimization

Integration behavior:
- `AkuTutor` sends problem context and student profile metadata
- Proxy selects the education-tuned model or default N-ATLAS model
- Response returns in the student's locale

### 5.2 Akudemy

Use cases:
- lecture explanation
- lesson Q&A
- voice-to-text to answer retrieval
- multilingual curriculum support

Integration behavior:
- Prompt includes subject, student level, and language locale
- N-ATLAS handles educational parsing and summarization
- Response is returned to the web/mobile app as plain text or streaming output

### 5.3 AkuWorkspace

Use cases:
- report generation
- document drafting
- multilingual writing assistance
- voice-to-document workflows

Integration behavior:
- Proxy accepts structured context such as report type, region, and industry
- Routing can use sectoral prompt templates
- Response may be passed through a summarization layer before document generation

### 5.4 Aku-Telhone

Use cases:
- voice confirmation flows
- multilingual user prompts
- accessibility support for voice-based service confirmation

Integration behavior:
- ASR result is passed into the proxy as text
- Model returns short-form command confirmation or a structured action payload
- Response is returned as TTS-friendly output or simple status code payload

### 5.5 Future Integration Points

The proxy is also designed to support:
- Aku-EdgeHub offline inference for low-bandwidth scenarios
- Aku-SuperHub regional model routing
- Aku-DaaS retrieval and benchmark evaluation
- Aku-IGHub API gateway traffic management and version-based orchestration

---

## 6. Performance Targets

### 6.1 Functional Targets

- Support 99.9% service availability for proxy layer
- Maintain a latency target under 500ms for standard cloud requests
- Support output generation for English, Hausa, and Yoruba
- Provide automatic fallback within 1–2 seconds when model health degrades
- Support at least 10k requests per day during pilot deployment and scale rapidly beyond that

### 6.2 Quality Targets

- Accuracy across language tasks should remain above established baseline thresholds
- Fallback event rate should be under 5% under normal operation
- P95 latency should remain under 700ms for standard inference use cases
- Multilingual output should improve comprehension by at least 5–15% relative to the Gemma baseline in fine-tuned or sectoral use cases

### 6.3 Observability Targets

- 100% of inference requests must emit telemetry
- All failures must contain a structured error code and request metadata
- Telemetry should be available through the centralized monitoring stack in real time

---

## 7. Code Example

Below is a FastAPI example showing a drop-in compatible proxy implementation. It demonstrates model routing, fallback logic, and multilingual support.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import time

app = FastAPI(title="AkuAI N-ATLAS Proxy")

class InferRequest(BaseModel):
    prompt: str
    context: Optional[str] = None
    max_tokens: int = 200
    temperature: float = 0.7
    top_p: float = 0.9
    stream: bool = False
    language: Optional[str] = "en"
    model_version: Optional[str] = "default"
    session_id: Optional[str] = None

class InferResponse(BaseModel):
    request_id: str
    output: str
    model: str
    model_version: str
    language: str
    latency_ms: int
    tokens_used: int
    fallback_used: bool
    provider: str
    status: str

@app.post("/v1/infer", response_model=InferResponse)
async def infer(req: InferRequest):
    start = time.time()

    try:
        model = "n-atlas-default"
        provider = "n-atlas"
        fallback_used = False

        # Fallback logic
        if req.model_version == "gemma" or req.language not in ["en", "ha", "yo", "ig"]:
            model = "gemma-fallback"
            provider = "gemma"
            fallback_used = True

        # Replace with real inference call
        output = f"Processed prompt in {req.language}: {req.prompt[:120]}"
        latency_ms = int((time.time() - start) * 1000)

        return InferResponse(
            request_id="req_123",
            output=output,
            model=model,
            model_version=req.model_version or "v1.2",
            language=req.language,
            latency_ms=latency_ms,
            tokens_used=80,
            fallback_used=fallback_used,
            provider=provider,
            status="success",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
```

### 7.1 Notes on the Example

This code intentionally keeps the implementation minimal while demonstrating:
- a drop-in request schema
- fallback logic for Gemma compatibility
- base language support
- normalized response contract
- service-level compatibility with the current wrapper model

---

## Appendix: Deployment Checklist

Before production deployment, the team should validate the following:

- [ ] Current Gemma wrapper API remains functionally compatible
- [ ] All service clients accept the new response schema without breakage
- [ ] N-ATLAS latency remains under target thresholds
- [ ] Fallback logic triggers correctly on timeout or model failure
- [ ] Multi-language prompts in Hausa, Yoruba, and English route correctly
- [ ] Telemetry dashboards are configured for request latency, model version, and fallback rate
- [ ] Service-level budgets and observability alerts are created in Aku-Sentinel

---

**Document Owner:** AkuAI Platform Team  
**Last Updated:** 2026-10-08  
**Status:** Ready for roadmap implementation and engineering review
