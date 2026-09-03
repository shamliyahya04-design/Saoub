import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASKS_FILE = ROOT / "benchmarks" / "phase2" / "tasks.json"
RESULTS_DIR = ROOT / "benchmarks" / "phase2" / "results"

CANDIDATES = {
    "openhands": {
        "commit": "64c1269655012698bc66538967989996191beb6c",
    },
    "browser_use": {
        "commit": "eb4126921bea3373f91afc49fb4b59d6eda7fed6",
    },
}

REQUIRED_FIELDS = {
    "candidate",
    "candidate_commit",
    "provider_id",
    "model_id",
    "task_id",
    "environment_id",
    "start_status",
    "end_status",
    "success",
    "correctness",
    "duration_ms",
    "resource_cost",
    "tool_calls",
    "recovery_attempts",
    "final_state",
    "evidence_artifacts",
    "failure_classification",
}


def load_tasks():
    with TASKS_FILE.open("r", encoding="utf-8") as handle:
        tasks = json.load(handle)

    if not isinstance(tasks, list) or len(tasks) != 10:
        raise ValueError("Benchmark registry must contain exactly 10 tasks")

    required = {"id", "class", "objective", "success_criteria", "evaluation"}

    for task in tasks:
        missing = required - set(task)
        if missing:
            raise ValueError(
                f"Task {task.get('id', '<unknown>')} missing fields: {sorted(missing)}"
            )

    ids = [task["id"] for task in tasks]
    if len(set(ids)) != 10:
        raise ValueError("Task IDs must be unique")

    return tasks


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def new_run(candidate, provider, model, task, environment_id):
    if candidate not in CANDIDATES:
        raise ValueError(f"Unknown candidate: {candidate}")

    return {
        "candidate": candidate,
        "candidate_commit": CANDIDATES[candidate]["commit"],
        "provider_id": provider,
        "model_id": model,
        "task_id": task["id"],
        "environment_id": environment_id,
        "start_status": "NOT_STARTED",
        "end_status": "NOT_STARTED",
        "success": False,
        "correctness": None,
        "duration_ms": None,
        "resource_cost": None,
        "tool_calls": [],
        "recovery_attempts": 0,
        "final_state": None,
        "evidence_artifacts": [],
        "failure_classification": None,
        "started_at": None,
        "finished_at": None,
    }


def validate_run_record(record):
    missing = REQUIRED_FIELDS - set(record)
    if missing:
        raise ValueError(f"Run record missing fields: {sorted(missing)}")

    if record["candidate"] not in CANDIDATES:
        raise ValueError("Run record contains unknown candidate")

    if record["candidate_commit"] != CANDIDATES[record["candidate"]]["commit"]:
        raise ValueError("Candidate commit does not match frozen revision")

    if not isinstance(record["success"], bool):
        raise ValueError("success must be boolean")

    if record["duration_ms"] is not None and record["duration_ms"] < 0:
        raise ValueError("duration_ms cannot be negative")

    return True


def build_run_matrix(tasks, providers, repetitions=5):
    if repetitions != 5:
        raise ValueError("Phase 2 requires exactly 5 independent runs per task")

    matrix = []

    for candidate in CANDIDATES:
        for provider in providers:
            for task in tasks:
                for repetition in range(1, repetitions + 1):
                    matrix.append(
                        {
                            "candidate": candidate,
                            "candidate_commit": CANDIDATES[candidate]["commit"],
                            "provider": provider,
                            "task_id": task["id"],
                            "repetition": repetition,
                        }
                    )

    return matrix


def write_jsonl(records, output):
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            validate_run_record(record)
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def main():
    tasks = load_tasks()

    providers = [
        {
            "provider_id": os.environ.get("PHASE2_PROVIDER_ID", "UNSET"),
            "model_id": os.environ.get("PHASE2_MODEL_ID", "UNSET"),
        }
    ]

    matrix = build_run_matrix(tasks, providers, repetitions=5)

    print(f"PHASE2_RUNNER_READY tasks={len(tasks)}")
    print(f"CANDIDATES={len(CANDIDATES)}")
    print(f"RUNS_PER_TASK=5")
    print(f"PLANNED_RUNS={len(matrix)}")
    print("EXECUTION_ENGINE=NOT_IMPLEMENTED")
    print("CANDIDATE_MODIFICATION=NONE")

    if "--validate-only" in sys.argv:
        print("VALIDATION=PASS")
        return 0

    print("EXECUTION=BLOCKED_UNTIL_CANDIDATE_ADAPTERS_ARE_IMPLEMENTED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
