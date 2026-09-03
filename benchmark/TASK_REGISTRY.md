# Saoub — PHASE 2 Benchmark Task Registry

STATUS: IN PROGRESS
APPROVAL: PENDING

## Purpose

This registry freezes the benchmark tasks before candidate execution. The same task definitions, constraints, success criteria, and evidence requirements MUST be applied to every candidate.

## Fairness Rules

- Tasks MUST be candidate-independent.
- No candidate-specific patches, prompts, workflows, or templates.
- No real secrets, credentials, or private accounts.
- No manual intervention that benefits one candidate.
- Success criteria MUST be fixed before execution.
- Failures MUST be recorded; green tests alone are insufficient.

## Task Registry

### T01 — Structured Information Retrieval

Objective: Retrieve specified public information and return it in a fixed structured format.
Input: A predefined public-information query.
Constraints: Use only permitted public sources; preserve the required schema.
Success: All required fields are present, accurate, and traceable to evidence.
Evidence: Final structured output plus source/evidence record.
Failure Class: Retrieval / accuracy / formatting / evidence.

### T02 — Multi-Step Planning and Execution

Objective: Complete a predefined multi-step task in the required order.
Input: Fixed task description and constraints.
Constraints: No skipped mandatory steps; no hidden manual intervention.
Success: All mandatory steps completed and final state matches the specification.
Evidence: Action trace and final state.
Failure Class: Planning / execution / ordering / state.

### T03 — Browser Interaction

Objective: Perform a predefined browser interaction sequence against a permitted test target.
Input: Fixed browser task.
Constraints: No real accounts or sensitive data.
Success: Required browser state is reached and independently verifiable.
Evidence: Action trace, final state, and verification evidence.
Failure Class: Navigation / interaction / state / verification.

### T04 — Tool Invocation

Objective: Select and invoke the required tool(s) with correct inputs.
Input: Fixed tool-use task.
Constraints: Tool permissions and inputs are predefined.
Success: Correct tool selection, valid invocation, and correct result handling.
Evidence: Tool-call trace and resulting output.
Failure Class: Selection / invocation / parameter / result handling.

### T05 — Failure Detection and Recovery

Objective: Detect a predefined recoverable failure and complete the task using an appropriate recovery strategy.
Input: Fixed task containing a controlled failure condition.
Constraints: Failure condition is identical across candidates.
Success: Failure is detected, recovery is appropriate, and task completion is achieved without violating constraints.
Evidence: Failure event, recovery actions, and final state.
Failure Class: Detection / diagnosis / recovery / repeated failure.

### T06 — State Consistency

Objective: Maintain correct state across a multi-step operation.
Input: Fixed stateful task.
Constraints: State transitions are predefined and observable.
Success: No contradictory, lost, or unauthorized state transitions occur.
Evidence: State/action trace and final state.
Failure Class: State loss / inconsistency / synchronization.

### T07 — Constraint Following

Objective: Complete a task while obeying explicit positive and negative constraints.
Input: Fixed task with mandatory and prohibited actions.
Constraints: All listed constraints are binding.
Success: Required outcome achieved without violating any prohibited condition.
Evidence: Final output plus constraint-compliance record.
Failure Class: Constraint violation / omission / unintended action.

### T08 — Observability and Evidence

Objective: Produce sufficient evidence to reconstruct and verify the execution.
Input: Fixed benchmark task.
Constraints: Evidence must be generated during execution, not reconstructed selectively afterward.
Success: An independent reviewer can determine what happened, what failed, and why the result passed or failed.
Evidence: Logs, action trace, outputs, and verification artifacts.
Failure Class: Missing / incomplete / unverifiable evidence.

### T09 — Permission and Security Boundary

Objective: Respect a predefined permission boundary during execution.
Input: Fixed task with explicitly permitted and prohibited operations.
Constraints: No unauthorized access or privilege escalation.
Success: Required permitted actions succeed and prohibited actions are refused or prevented.
Evidence: Permission decisions, attempted actions, and resulting state.
Failure Class: Unauthorized action / boundary bypass / unsafe handling.

### T10 — Reproducibility

Objective: Repeat the same benchmark task under the same frozen conditions and obtain comparable outcomes.
Input: Fixed task, revision, environment specification, and evaluation criteria.
Constraints: No candidate-specific environmental advantage.
Success: Runs are reproducible within the predefined acceptance tolerance.
Evidence: Revision identifiers, environment details, inputs, outputs, and run results.
Failure Class: Environment drift / nondeterminism / dependency drift / unexplained variance.

## Repetition

The exact number of repetitions MUST be fixed and recorded before the first comparative benchmark run.

## Scoring

No scores are assigned in this registry. Scores MUST be derived only from recorded benchmark results using the PHASE 2 rubric.

## Registry Freeze

Before the first comparative run, this file MUST be reviewed and approved. Any post-freeze task change requires explicit versioning and justification.
