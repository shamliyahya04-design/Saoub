from __future__ import annotations

import json
import os
import time
import urllib.parseimport urllib.request
from typing import Any

FROZEN_COMMIT = "64c1269655012698bc66538967989996191beb6"
CANDIDATE_ID = "openhands"
RUNTIME_VERSION = "openhands-agent-server==1.44.0"


class OpenHandsAdapter:
    candidate_id = CANDIDATE_ID
    candidate_commit = FROZEN_COMMIT
    runtime_version = RUNTIME_VERSION

    def __init__(self) -> None:
        self.base = os.getenv(
            "OPENHANDS_BASE_URL",
            "http://127.0.0.1:18000",
        ).rstrip("/")
        self.key = os.getenv("OPENHANDS_SESSION_API_KEY")

    def _req(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None = None,
        timeout: int = 60,
    ) -> dict[str, Any]:
        if not self.key:
            raise RuntimeError("OPENHANDS_SESSION_API_KEY missing")

        data = None if body is None else json.dumps(body).encode()
        request = urllib.request.Request(
            self.base + path,
            data=data,
            method=method,
            headers={
                "Content-Type": "application/json",
                "X-Session-API-Key": self.key,
            },
        )

        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode()
            return json.loads(raw) if raw else {}

    def prepare(self) -> None:
        self._req("GET", "/server_info")

    def execute(
        self,
        task: dict[str, Any],
        provider_config: dict[str, Any],
    ) -> dict[str, Any]:
        prompt = (
            task.get("prompt")
            or task.get("instructions")
            or task.get("objective")
        )

        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("missing executable task text")

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return {
                "status": "provider_failure",
                "failure_class": "external_dependency",
                "error": "GOOGLE_API_KEY missing",
            }

        workspace = task.get("_workspace")
        if not workspace:
            raise ValueError("missing isolated workspace")

        model = provider_config["model"]
        started = time.monotonic()

        created = self._req(
            "POST",
            "/api/conversations",
            {
                "agent": {
                    "kind": "Agent",
                    "llm": {
                        "model": model,
                        "api_key": api_key,
                    },
                    "tools": [],
                },
                "workspace": {
                    "working_dir": workspace,
                },
                "initial_message": {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        }
                    ],
                    "run": True,
                },
            },
        )

        conversation_id = (
            created.get("conversation_id")
            or created.get("id")
        )

        if not conversation_id:
            raise RuntimeError("conversation id missing")

        timeout_seconds = int(
            os.getenv("OPENHANDS_TASK_TIMEOUT", "180")
        )
        deadline = time.monotonic() + timeout_seconds
        state: dict[str, Any] = {}

        while time.monotonic() < deadline:
            state = self._req(
                "GET",
                f"/api/conversations/{conversation_id}",
            )

            status = str(
                state.get("status")
                or state.get("state")
                or ""
            ).lower()

            if status in {
                "completed",
                "complete",
                "finished",
                "success",
                "failed",
                "error",
                "stopped",
                "cancelled",
                "canceled",
            }:
                break

            time.sleep(2)

        try:
            events = []
            page_id = None
            while True:
                path = f"/api/conversations/{conversation_id}/events/search?limit=100"
                if page_id:
                    path += f"&page_id={urllib.parse.quote(page_id, safe='')}"
                page = self._req("GET", path)
                items = page.get("items", [])
                if not isinstance(items, list):
                    raise RuntimeError("OpenHands events/search returned invalid items")
                events.extend(items)
                page_id = page.get("next_page_id")
                if not page_id:
                    break
        except Exception as exc:
            events = {
                "collection_error": str(exc),
            }

        execution_status = str(state.get("execution_status") or "").lower()

        if execution_status in {"error", "failed", "cancelled", "canceled", "stopped"}:
            return {
                "status": "candidate_failure",
                "failure_class": "execution_failure",
                "duration_seconds": time.monotonic() - started,
                "conversation_id": conversation_id,
                "final_state": state,
                "events": events,
            }

        if not isinstance(events, dict) or "collection_error" in events:
            return {
                "status": "candidate_unproven",
                "failure_class": "proof_missing",
                "duration_seconds": time.monotonic() - started,
                "conversation_id": conversation_id,
                "final_state": state,
                "events": events,
            }

        return {
            "status": "candidate_completed",
            "failure_class": None,
            "duration_seconds": time.monotonic() - started,
            "conversation_id": conversation_id,
            "final_state": state,
            "events": events,
        }

    def collect_observations(
        self,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "status": result.get("status"),
            "final_state": result.get("final_state"),
            "conversation_id": result.get("conversation_id"),
        }

    def collect_evidence(
        self,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "candidate_commit": self.candidate_commit,
            "runtime_version": self.runtime_version,
            "conversation_id": result.get("conversation_id"),
            "events_present": "events" in result,
        }

    @staticmethod
    def classify_failure(exc: Exception) -> str:
        message = str(exc).lower()

        if "timeout" in message:
            return "timeout"
        if "permission" in message or "forbidden" in message or "unauthorized" in message:
            return "security/permission"
        if "429" in message or "rate limit" in message:
            return "external_dependency"
        if "browser" in message or "playwright" in message:
            return "browser interaction"
        if "tool" in message:
            return "tool-use"

        return "unknown"

    def cleanup(self) -> None:
        pass


Adapter = OpenHandsAdapter
