"""AkuWorkspace Orchestrator — dispatches workflow steps to AkuAI, Aku-DaaS,
and Akudemy via async httpx calls, then aggregates the results."""

from __future__ import annotations

import time
import uuid
from typing import Any

import httpx
from fastapi import HTTPException, status

from app.schemas.workflows import (
    WorkflowRunResult,
    WorkflowStatus,
    WorkflowStep,
    WorkflowType,
)


# ---------------------------------------------------------------------------
# Configuration dependency (injected at startup via FastAPI lifespan)
# ---------------------------------------------------------------------------


class OrchestratorConfig:
    """Runtime configuration for all downstream micro-services."""

    def __init__(
        self,
        aku_ai_url: str,
        aku_daas_url: str,
        akudemy_url: str,
        redis_url: str,
        http_timeout: float = 30.0,
    ) -> None:
        self.aku_ai_url = aku_ai_url.rstrip("/")
        self.aku_daas_url = aku_daas_url.rstrip("/")
        self.akudemy_url = akudemy_url.rstrip("/")
        self.redis_url = redis_url
        self.http_timeout = http_timeout

    def base_url_for(self, service: str) -> str:
        """Resolve a logical service name to its base URL."""
        mapping: dict[str, str] = {
            "akuai": self.aku_ai_url,
            "daas": self.aku_daas_url,
            "akudemy": self.akudemy_url,
        }
        key = service.lower()
        if key not in mapping:
            raise ValueError(
                f"Unknown service '{service}'. Expected one of: {list(mapping)}"
            )
        return mapping[key]


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


class WorkflowOrchestrator:
    """Executes workflow steps sequentially, passing each step's output as
    additional context to the next step."""

    def __init__(self, config: OrchestratorConfig) -> None:
        self._cfg = config

    # ------------------------------------------------------------------
    # Public entry-point
    # ------------------------------------------------------------------

    async def run(
        self,
        workflow_id: uuid.UUID,
        workflow_type: WorkflowType,
        steps: list[WorkflowStep],
        runtime_input: dict[str, Any],
    ) -> WorkflowRunResult:
        """Execute all steps and return an aggregated result."""
        dispatch = {
            WorkflowType.DATA_QUERY: self._run_data_query,
            WorkflowType.DOC_GENERATION: self._run_doc_generation,
            WorkflowType.CONTENT_SEARCH: self._run_content_search,
            WorkflowType.TUTORING_ASSIST: self._run_tutoring_assist,
        }

        handler = dispatch.get(workflow_type)
        if handler is None:
            return WorkflowRunResult(
                workflow_id=workflow_id,
                status=WorkflowStatus.FAILED,
                error=f"Unsupported workflow type: {workflow_type}",
            )

        t0 = time.monotonic_ns()
        try:
            outputs = await handler(steps, runtime_input)
            duration_ms = (time.monotonic_ns() - t0) // 1_000_000
            return WorkflowRunResult(
                workflow_id=workflow_id,
                status=WorkflowStatus.COMPLETED,
                outputs=outputs,
                duration_ms=duration_ms,
            )
        except HTTPException:
            raise
        except Exception as exc:  # noqa: BLE001
            duration_ms = (time.monotonic_ns() - t0) // 1_000_000
            return WorkflowRunResult(
                workflow_id=workflow_id,
                status=WorkflowStatus.FAILED,
                error=str(exc),
                duration_ms=duration_ms,
            )

    # ------------------------------------------------------------------
    # Workflow-type handlers
    # ------------------------------------------------------------------

    async def _run_data_query(
        self, steps: list[WorkflowStep], runtime_input: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Execute a DATA_QUERY workflow: NL → AkuAI parse → Aku-DaaS query."""
        outputs: list[dict[str, Any]] = []
        accumulated: dict[str, Any] = dict(runtime_input)

        for step in steps:
            response = await self._dispatch_step(step, accumulated)
            outputs.append(response)
            accumulated.update(response)

        return outputs

    async def _run_doc_generation(
        self, steps: list[WorkflowStep], runtime_input: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Execute a DOC_GENERATION workflow: AkuAI text generation + optional
        Akudemy content enrichment."""
        outputs: list[dict[str, Any]] = []
        accumulated: dict[str, Any] = dict(runtime_input)

        for step in steps:
            response = await self._dispatch_step(step, accumulated)
            outputs.append(response)
            accumulated.update(response)

        return outputs

    async def _run_content_search(
        self, steps: list[WorkflowStep], runtime_input: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Execute a CONTENT_SEARCH workflow: AkuAI NL understanding → Akudemy
        content catalogue search."""
        outputs: list[dict[str, Any]] = []
        accumulated: dict[str, Any] = dict(runtime_input)

        for step in steps:
            response = await self._dispatch_step(step, accumulated)
            outputs.append(response)
            accumulated.update(response)

        return outputs

    async def _run_tutoring_assist(
        self, steps: list[WorkflowStep], runtime_input: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Execute a TUTORING_ASSIST workflow: Akudemy lesson lookup + AkuAI
        personalised explanation generation."""
        outputs: list[dict[str, Any]] = []
        accumulated: dict[str, Any] = dict(runtime_input)

        for step in steps:
            response = await self._dispatch_step(step, accumulated)
            outputs.append(response)
            accumulated.update(response)

        return outputs

    # ------------------------------------------------------------------
    # Step dispatcher
    # ------------------------------------------------------------------

    async def _dispatch_step(
        self,
        step: WorkflowStep,
        accumulated_context: dict[str, Any],
    ) -> dict[str, Any]:
        """Merge static step payload with accumulated runtime context, POST to
        the target service, and return the parsed JSON response."""
        try:
            base_url = self._cfg.base_url_for(step.service)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc

        merged_payload = {**step.payload, **accumulated_context}
        url = f"{base_url}{step.endpoint}"

        async with httpx.AsyncClient(timeout=self._cfg.http_timeout) as client:
            try:
                resp = await client.post(url, json=merged_payload)
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPStatusError as exc:
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=(
                        f"Upstream error from {step.service} "
                        f"({url}): {exc.response.text}"
                    ),
                ) from exc
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Failed to reach {step.service} ({url}): {exc}",
                ) from exc

    # ------------------------------------------------------------------
    # Convenience: direct AkuAI text-generation call (used by docs_gen router)
    # ------------------------------------------------------------------

    async def generate_text(
        self,
        prompt: str,
        context: dict[str, Any],
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> dict[str, Any]:
        """Call AkuAI /api/v1/text/generate directly and return the raw JSON."""
        url = f"{self._cfg.aku_ai_url}/api/v1/text/generate"
        payload = {
            "prompt": prompt,
            "context": context,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        async with httpx.AsyncClient(timeout=self._cfg.http_timeout) as client:
            try:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPStatusError as exc:
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=f"AkuAI error: {exc.response.text}",
                ) from exc
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Failed to reach AkuAI: {exc}",
                ) from exc
