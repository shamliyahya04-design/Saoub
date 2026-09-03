# PHASE 2 — FROZEN BENCHMARK REGISTRY

Status: FROZEN
Purpose: Independent baseline comparison before any candidate integration or optimization.

## Frozen Candidates
- OpenHands: 64c1269655012698bc66538967989996191beb6c
- Browser Use: eb4126921bea3373f91afc49fb4b59d6eda7fed6

## Fixed Repetition
Each task: 5 independent runs per candidate.
No hidden retries.

## Task Registry
B01 Information retrieval + structured output
B02 Multi-step planning + execution
B03 Browser navigation + extraction
B04 Tool invocation
B05 Failure detection + recovery
B06 State consistency
B07 Constraint following
B08 Evidence generation
B09 Permission/security boundary
B10 Reproducibility

## Required Run Record
candidate, commit, task_id, environment_id, start_status, end_status,
success, correctness, duration_ms, resource_cost, tool_calls,
recovery_attempts, final_state, evidence_artifacts, failure_classification.

## Fairness
Identical task definitions, success criteria, repetition count and reporting.
No source modification, candidate-specific prompt optimization, selective retry,
or manual intervention benefiting one candidate.

## Acceptance
Both candidates complete all applicable tasks with traceable evidence.
Regression and adversarial review are mandatory before approval.
