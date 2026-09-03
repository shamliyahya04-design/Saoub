from __future__ import annotations

import argparse
import importlib
import json
import os
import pathlib
import shutil
import tempfile
import time
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[3]
TASKS_FILE = ROOT / "benchmarks" / "phase2" / "tasks.json"
RESULTS_DIR = ROOT / "benchmarks" / "phase2" / "results"

FROZEN_CANDIDATES = {
    "openhands": {
        "commit": "64c1269655012698bc66538967989996191beb6",
        "runtime": "openhands-agent-server==1.44.0",
    },
    "browser_use": {
        "commit": "eb4126921bea3373f91afc49fb4b59d6eda7fed6",
        "runtime": "browser-use==0.13.8",
    },
}

PROVIDER_CONFIG = {
    "provider": "google",
    "model": "gemini-2.5-flash",
}


def load_tasks() -> list[dict[str, Any]]:
    raw = json.loads(TASKS_FILE.read_text(encoding="utf-8"))

    tasks = raw.get("tasks") if isinstance(raw, dict) else raw

    if not isinstance(tasks, list):
        raise RuntimeError("tasks.json must contain a task list")

    if len(tasks) != 10:
        raise RuntimeError(
            f"Phase 2 requires exactly 10 tasks; found {len(tasks)}"
        )

    for task in tasks:
        if not isinstance(task, dict):
            raise RuntimeError("Every task must be an object")

        if not task.get("id"):
            raise RuntimeError("Every task requires an id")

    return tasks


def load_adapter(candidate: str):
    module = importlib.import_module(
        f"benchmarks.phase2.adapters.{candidate}"
    )

    adapter_class = getattr(module, "Adapter", None)

    if adapter_class is None:
        raise RuntimeError(
            f"{candidate} adapter does not expose Adapter"
        )

    return adapter_class()


def validate_adapter(candidate: str, adapter: Any) -> None:
    expected = FROZEN_CANDIDATES[candidate]

    if adapter.candidate_id != candidate:
        raise RuntimeError(
            f"{candidate}: candidate_id mismatch"
        )

    if adapter.candidate_commit != expected["commit"]:
        raise RuntimeError(
            f"{candidate}: frozen commit mismatch: "
            f"{adapter.candidate_commit}"
        )

    if adapter.runtime_version != expected["runtime"]:
        raise RuntimeError(
            f"{candidate}: runtime mismatch: "
            f"{adapter.runtime_version}"
        )


def task_prompt(task: dict[str, Any]) -> str:
    prompt = (
        task.get("prompt")
        or task.get("instructions")
        or task.get("objective")
    )

    if not isinstance(prompt, str) or not prompt.strip():
        raise RuntimeError(
            f"{task.get('id')}: missing executable prompt"
        )

    return prompt


def evaluate_result(
    task: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    """
    Benchmark correctness must be evaluated independently
    from candidate execution status.

    If a task provides deterministic expected data, compare it.
    Otherwise mark correctness as not specified rather than
    falsely treating execution completion as correctness.
    """

    expected = task.get("expected")

    if expected is None:
        return {
            "status": "not_specified",
            "passed": False,
            "reason": "task has no deterministic expected value",
        }

    actual = result.get("final_state")

    passed = actual == expected

    return {
        "status": "pass" if passed else "fail",
        "passed": passed,
        "expected": expected,
        "actual": actual,
    }


def execute_one(
    adapter: Any,
    candidate: str,
    task: dict[str, Any],
    repetition: int,
    environment_id: str,
) -> dict[str, Any]:

    workspace = tempfile.mkdtemp(
        prefix=f"saoub-{candidate}-{task['id']}-"
    )

    started_at = time.time()

    record: dict[str, Any] = {
        "candidate": candidate,
        "candidate_commit": adapter.candidate_commit,
        "runtime_version": adapter.runtime_version,
        "task_id": task["id"],
        "repetition": repetition,
        "environment_id": environment_id,
        "start_time": started_at,
        "status": None,
        "correctness": None,
        "duration_seconds": None,
        "tool_calls": [],
        "recovery_attempts": 0,
        "final_state": None,
        "observations": {},
        "evidence": {},
        "failure_class": None,
    }

    try:
        run_task = dict(task)

        # Isolated workspace is supplied only to the adapter.
        run_task["_workspace"] = workspace

        # Validate prompt before execution.
        run_task["_executable_prompt"] = task_prompt(task)

        result = adapter.execute(
            run_task,
            PROVIDER_CONFIG,
        )

        if not isinstance(result, dict):
            raise RuntimeError(
                "Adapter returned non-object result"
            )

        record["status"] = result.get("status")
        record["failure_class"] = result.get("failure_class")
        record["duration_seconds"] = result.get(
            "duration_seconds"
        )

        record["final_state"] = result.get(
            "final_state"
        )

        record["recovery_attempts"] = result.get(
            "recovery_attempts",
            0,
        )

        observations = adapter.collect_observations(
            result
        )

        evidence = adapter.collect_evidence(
            result
        )

        record["observations"] = observations
        record["evidence"] = evidence
        record["correctness"] = evaluate_result(
            task,
            result,
        )

        if "tool_calls" in result:
            record["tool_calls"] = result["tool_calls"]

    except Exception as exc:
        record["status"] = "runner_failure"
        record["failure_class"] = "environment/runtime"
        record["error"] = str(exc)

    finally:
        try:
            adapter.cleanup()
        finally:
            shutil.rmtree(
                workspace,
                ignore_errors=True,
            )

    record["end_time"] = time.time()

    if record["duration_seconds"] is None:
        record["duration_seconds"] = (
            record["end_time"] - started_at
        )

    return record


def run_benchmark(
    candidates: list[str],
    repetitions: int,
) -> pathlib.Path:

    tasks = load_tasks()

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    environment_id = os.getenv(
        "GITHUB_RUN_ID",
        "local",
    )

    output_file = RESULTS_DIR / (
        f"{environment_id}.jsonl"
    )

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as output:

        total = (
            len(candidates)
            * len(tasks)
            * repetitions
        )

        completed = 0

        for candidate in candidates:

            adapter = load_adapter(candidate)

            validate_adapter(
                candidate,
                adapter,
            )

            adapter.prepare()

            for task in tasks:

                for repetition in range(
                    1,
                    repetitions + 1,
                ):

                    record = execute_one(
                        adapter=adapter,
                        candidate=candidate,
                        task=task,
                        repetition=repetition,
                        environment_id=environment_id,
                    )

                    output.write(
                        json.dumps(
                            record,
                            ensure_ascii=False,
                            separators=(",", ":"),
                        )
                        + "\n"
                    )

                    output.flush()

                    completed += 1

                    print(
                        f"[{completed}/{total}] "
                        f"{candidate} "
                        f"{task['id']} "
                        f"run={repetition} "
                        f"status={record['status']}"
                    )

    return output_file


def validate_only(
    candidates: list[str],
) -> None:

    load_tasks()

    for candidate in candidates:

        adapter = load_adapter(candidate)

        validate_adapter(
            candidate,
            adapter,
        )

        print(
            f"VALIDATED "
            f"{candidate} "
            f"{adapter.candidate_commit} "
            f"{adapter.runtime_version}"
        )

    print(
        "PHASE2_RUNNER_VALIDATION_PASS"
    )


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--validate-only",
        action="store_true",
    )

    parser.add_argument(
        "--candidate",
        choices=list(FROZEN_CANDIDATES),
    )

    parser.add_argument(
        "--repetitions",
        type=int,
        default=5,
    )

    args = parser.parse_args()

    if args.repetitions != 5:
        raise RuntimeError(
            "Phase 2 requires exactly 5 repetitions"
        )

    candidates = (
        [args.candidate]
        if args.candidate
        else list(FROZEN_CANDIDATES)
    )

    if args.validate_only:
        validate_only(candidates)
        return

    result_file = run_benchmark(
        candidates=candidates,
        repetitions=5,
    )

    print(
        f"PHASE2_BENCHMARK_COMPLETE={result_file}"
    )


if __name__ == "__main__":
    main()
