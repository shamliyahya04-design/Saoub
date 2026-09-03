import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

FROZEN_COMMIT = "64c1269655012698bc66538967989996191beb6"


class OpenHandsAdapter:
    candidate_id = "openhands"
    candidate_commit = FROZEN_COMMIT

    def __init__(self, workspace="/tmp/saoub-openhands"):
        self.workspace = Path(workspace)
        self.last_result = None

    def prepare(self):
        self.workspace.mkdir(parents=True, exist_ok=True)

        provider = os.environ.get("PHASE2_PROVIDER_ID")
        model = os.environ.get("PHASE2_MODEL_ID")

        if not provider or not model:
            raise RuntimeError("PHASE2_PROVIDER_ID and PHASE2_MODEL_ID are required")

        self.provider = provider
        self.model = model

    def execute(self, task, provider_config):
        self.prepare()

        prompt = task["prompt"]

        env = os.environ.copy()
        env["PHASE2_PROVIDER_ID"] = self.provider
        env["PHASE2_MODEL_ID"] = self.model

        started = time.monotonic()

        command = [
            "openhands",
            "--headless",
            "--json",
            "-t",
            prompt,
        ]

        completed = subprocess.run(
            command,
            cwd=self.workspace,
            env=env,
            capture_output=True,
            text=True,
            timeout=int(task.get("timeout_seconds", 300)),
            check=False,
        )

        duration_ms = int((time.monotonic() - started) * 1000)

        self.last_result = {
            "candidate_id": self.candidate_id,
            "candidate_commit": self.candidate_commit,
            "task_id": task["task_id"],
            "provider_id": self.provider,
            "model_id": self.model,
            "exit_code": completed.returncode,
            "success": completed.returncode == 0,
            "duration_ms": duration_ms,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "workspace": str(self.workspace),
        }

        return self.last_result

    def collect_observations(self):
        if not self.last_result:
            return []
        return [{
            "type": "process_exit",
            "exit_code": self.last_result["exit_code"],
            "duration_ms": self.last_result["duration_ms"],
        }]

    def collect_evidence(self):
        if not self.last_result:
            return []

        evidence = []

        for path in self.workspace.rglob("*"):
            if path.is_file():
                evidence.append({
                    "path": str(path.relative_to(self.workspace)),
                    "size": path.stat().st_size,
                })

        return evidence

    def classify_failure(self, error=None):
        if error is not None:
            if isinstance(error, subprocess.TimeoutExpired):
                return "timeout"
            if isinstance(error, PermissionError):
                return "security/permission"
            return "environment/runtime"

        if self.last_result and self.last_result["exit_code"] != 0:
            return "candidate_execution"

        return None

    def cleanup(self):
        self.last_result = None


def validate_frozen_revision(actual_commit):
    if actual_commit != FROZEN_COMMIT:
        raise RuntimeError(
            f"Frozen OpenHands revision mismatch: {actual_commit}"
        )


if __name__ == "__main__":
    adapter = OpenHandsAdapter()
    adapter.prepare()
    print("OPENHANDS_ADAPTER=EXECUTION_READY")
    print(f"FROZEN_COMMIT={FROZEN_COMMIT}")
    print(f"PROVIDER={adapter.provider}")
    print(f"MODEL={adapter.model}")
    print("SOURCE_MODIFICATION=NONE")
