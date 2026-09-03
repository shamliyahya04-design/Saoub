from __future__ import annotations

import asyncio
import importlib.metadata
import os
import time
from typing import Any

from browser_use import Agent
from browser_use.llm.google.chat import ChatGoogle

FROZEN_COMMIT = "eb4126921bea3373f91afc49fb4b59d6eda7fed6"
CANDIDATE_ID = "browser_use"
RUNTIME_VERSION = "browser-use==0.13.8"


class BrowserUseAdapter:
    candidate_id = CANDIDATE_ID
    candidate_commit = FROZEN_COMMIT
    runtime_version = RUNTIME_VERSION

    def prepare(self) -> None:
        version = importlib.metadata.version("browser-use")
        if version != "0.13.8":
            raise RuntimeError(f"Unexpected browser-use version: {version}")

    def execute(
        self,
        task: dict[str, Any],
        provider_config: dict[str, Any],
    ) -> dict[str, Any]:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            return {
                "status": "provider_failure",
                "failure_class": "external_dependency",
                "error": "GOOGLE_API_KEY is not configured",
            }

        model = provider_config.get("model", "gemini-2.5-flash")
        if model != "gemini-2.5-flash":
            raise RuntimeError(f"Benchmark model mismatch: {model}")

        prompt = (
            task.get("prompt")
            or task.get("instructions")
            or task.get("objective")
        )

        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError(
                "Task has no executable prompt/instructions/objective"
            )

        started = time.monotonic()

        try:
            llm = ChatGoogle(
                model=model,
                api_key=api_key,
                max_retries=0,
            )

            agent = Agent(
                task=prompt,
                llm=llm,
                use_vision=False,
                generate_gif=False,
            )

            history = asyncio.run(agent.run())

            return {
                "status": "success",
                "failure_class": None,
                "duration_seconds": time.monotonic() - started,
                "history": (
                    history.model_dump()
                    if hasattr(history, "model_dump")
                    else str(history)
                ),
            }

        except Exception as exc:
            return {
                "status": "candidate_failure",
                "failure_class": self.classify_failure(exc),
                "duration_seconds": time.monotonic() - started,
                "error": str(exc),
            }

    def collect_observations(
        self,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "status": result.get("status"),
            "duration_seconds": result.get("duration_seconds"),
        }

    def collect_evidence(
        self,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "candidate_commit": self.candidate_commit,
            "runtime_version": self.runtime_version,
            "status": result.get("status"),
            "history_present": "history" in result,
        }

    @staticmethod
    def classify_failure(exc: Exception) -> str:
        message = str(exc).lower()

        if "timeout" in message:
            return "timeout"
        if "permission" in message or "blocked" in message:
            return "security/permission"
        if "429" in message or "rate limit" in message:
            return "external_dependency"
        if "browser" in message or "playwright" in message:
            return "browser interaction"
        if "tool" in message:
            return "tool-use"

        return "unknown"

    def cleanup(self) -> None:
        return None


Adapter = BrowserUseAdapter
