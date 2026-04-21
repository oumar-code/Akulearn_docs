"""Comprehensive API tests for AkuAI inference and model endpoints."""

from __future__ import annotations

from httpx import AsyncClient


async def test_list_models_returns_catalogue(client: AsyncClient) -> None:
    response = await client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 4
    assert len(data["models"]) == 4
    assert {m["id"] for m in data["models"]} == {
        "gemma-2b",
        "facebook/bart-large-cnn",
        "facebook/bart-large-mnli",
        "sentence-transformers/all-MiniLM-L6-v2",
    }


async def test_run_inference_returns_stub_payload(client: AsyncClient) -> None:
    payload = {"model": "gemma-2b", "prompt": "Explain vectors in simple terms."}
    response = await client.post("/api/v1/inference", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "gemma-2b"
    assert data["provider"] == "local"
    assert data["tokens_used"] == len(payload["prompt"].split())
    assert "Inference response" in data["output"]


async def test_text_generate_respects_max_tokens(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/text/generate",
        json={"prompt": "Write two lines on Akulearn.", "max_tokens": 123, "temperature": 0.2},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "gemma-2b"
    assert data["tokens_used"] == 123
    assert data["finish_reason"] == "length"
    assert "Generated text" in data["text"]


async def test_text_classify_returns_scores_and_top_label(client: AsyncClient) -> None:
    labels = ["education", "finance", "health"]
    response = await client.post(
        "/api/v1/text/classify",
        json={"text": "This lesson teaches algebra.", "labels": labels},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["top_label"] == labels[0]
    assert len(data["scores"]) == len(labels)
    assert [item["label"] for item in data["scores"]] == labels
    assert all(0 <= item["score"] <= 1 for item in data["scores"])


async def test_text_summarize_returns_lengths(client: AsyncClient) -> None:
    long_text = "Akulearn empowers students with adaptive lessons. " * 8
    response = await client.post("/api/v1/text/summarize", json={"text": long_text})
    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "facebook/bart-large-cnn"
    assert data["original_length"] == len(long_text.strip())
    assert data["summary_length"] > 0
    assert "Summary" in data["summary"]


async def test_embeddings_accepts_single_string(client: AsyncClient) -> None:
    response = await client.post("/api/v1/embeddings", json={"input": "Akulearn AI assistant"})
    assert response.status_code == 200
    data = response.json()
    assert data["dimensions"] == 384
    assert len(data["embeddings"]) == 1
    assert len(data["embeddings"][0]) == 384
    assert data["token_count"] == 3


async def test_embeddings_accepts_list_of_strings(client: AsyncClient) -> None:
    payload = {"input": ["adaptive learning", "offline-first classrooms"]}
    response = await client.post("/api/v1/embeddings", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["embeddings"]) == 2
    assert all(len(vector) == 384 for vector in data["embeddings"])
    assert data["token_count"] == 4


async def test_gemma_infer_returns_hub_context(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/models/gemma/infer",
        json={"prompt": "Explain model drift.", "hub_id": "edge-hub-01", "max_tokens": 64},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "gemma-2b"
    assert data["hub_id"] == "edge-hub-01"
    assert data["tokens_used"] == 64
    assert "Gemma response" in data["text"]


async def test_text_classify_requires_at_least_two_labels(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/text/classify",
        json={"text": "Only one label should fail", "labels": ["single"]},
    )
    assert response.status_code == 422


async def test_text_summarize_rejects_short_text(client: AsyncClient) -> None:
    response = await client.post("/api/v1/text/summarize", json={"text": "too short"})
    assert response.status_code == 422


async def test_gemma_infer_rejects_max_tokens_out_of_range(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/models/gemma/infer",
        json={"prompt": "Hello", "hub_id": "edge-hub-01", "max_tokens": 2048},
    )
    assert response.status_code == 422
