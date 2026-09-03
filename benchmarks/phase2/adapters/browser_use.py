import os
from pathlib import Path

FROZEN_COMMIT = "eb4126921bea3373f91afc49fb4b59d6eda7fed6"


class BrowserUseAdapter:
    candidate_id = "browser_use"
    candidate_commit = FROZEN_COMMIT

    def __init__(self, workspace="/tmp/saoub-browser-use"):
        self.workspace = Path(workspace)

    def prepare(self):
        self.workspace.mkdir(parents=True, exist_ok=True)

        if not os.environ.get("PHASE2_PROVIDER_ID"):
            raise RuntimeError("PHASE2_PROVIDER_ID is required")

        if not os.environ.get("PHASE2_MODEL_ID"):
            raise RuntimeError("PHASE2_MODEL_ID is required")

    def execute(self, task, provider_config):
        raise NotImplementedError(
            "Browser Use execution adapter requires the frozen runtime "
            "and must not fabricate benchmark results."
        )

    def collect_observations(self):
        return []

    def collect_evidence(self):
        return []

    def classify_failure(self, error):
        if isinstance(error, TimeoutError):
            return "timeout"
        if isinstance(error, PermissionError):
            return "security/permission"
        return "unknown"

    def cleanup(self):
        pass


def validate_frozen_revision(actual_commit):
    if actual_commit != FROZEN_COMMIT:
        raise RuntimeError(
            f"Frozen Browser Use revision mismatch: {actual_commit}"
        )


if __name__ == "__main__":
    print("BROWSER_USE_ADAPTER=READY")
    print(f"FROZEN_COMMIT={FROZEN_COMMIT}")
    print("SOURCE_MODIFICATION=NONE")
    print("EXECUTION=NOT_IMPLEMENTED")
