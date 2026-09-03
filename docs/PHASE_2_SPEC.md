# PHASE 2 — BASELINE BENCHMARK

STATUS: IN PROGRESS
APPROVAL: PENDING

## Objective

Measure OpenHands and Browser Use independently in their original, unmodified form before any Base Agent integration or candidate-specific optimization.

## Source of Truth

Repository: shamliyahya04-design/Saoub

Candidate sources and frozen revisions:

- OpenHands: 64c1269655012698bc66538967989996191beb6c
- Browser Use: eb4126921bea3373f91afc49fb4b59d6eda7fed6

No candidate source modification is permitted during Phase 2.

## Benchmark Principles

1. Identical task definitions and evaluation criteria for comparable capabilities.
2. Candidates are evaluated independently.
3. No candidate-specific optimization before baseline completion.
4. No ready-made workflow or template is used as the benchmark solution.
5. No real secrets, API keys, credentials, or private data.
6. Benchmark environment must be reproducible and isolated.
7. Failures must be recorded, not hidden.
8. Green tests alone do not constitute acceptance.
9. Results must include evidence sufficient for independent review.
10. Benchmark results do not establish patentability or novelty.

## Evaluation Dimensions

The Phase 1 rubric remains the evaluation basis:

- General task execution — 15%
- Tool use — 10%
- Browser/computer interaction — 10%
- Planning/reasoning — 10%
- Reliability — 15%
- Recovery capability — 10%
- Observability — 5%
- Extensibility — 5%
- Security boundaries — 5%
- Performance/cost — 5%
- Documentation/maintainability — 5%
- License/IP compatibility — 5%

Total: 100%.

## Benchmark Task Classes

The benchmark must include representative tasks covering:

1. Information retrieval and structured output.
2. Multi-step planning and execution.
3. Browser interaction.
4. Tool invocation.
5. Failure detection and recovery.
6. State consistency across steps.
7. Constraint-following.
8. Observability and evidence generation.
9. Permission/security boundary behavior.
10. Reproducibility.

Tasks must be deterministic or have explicitly defined acceptable outcome ranges wherever practical.

## Required Measurements

For every benchmark run record:

- Candidate
- Frozen commit
- Task identifier
- Environment identifier
- Start/end status
- Success/failure
- Correctness
- Completion time
- Resource/cost measurements when available
- Tool calls
- Recovery attempts
- Final state
- Evidence/artifacts
- Failure classification

## Failure Classification

Failures must be classified at minimum as:

- Planning failure
- Tool-use failure
- Browser interaction failure
- State/reality mismatch
- Constraint violation
- Recovery failure
- Timeout
- Environment/runtime failure
- Security/permission failure
- External dependency failure
- Unknown

## Repetition

Each benchmark task must be repeated sufficiently to distinguish stable behavior from isolated success or failure.

The exact repetition count must be fixed before candidate comparison.

## Fairness Controls

The following are prohibited before baseline completion:

- Candidate-specific patches
- Candidate-specific prompts designed to compensate for observed weaknesses
- Source modifications
- Hidden retries applied to only one candidate
- Different task definitions
- Different success criteria
- Selective reporting
- Manual intervention that benefits only one candidate

## Evidence Requirements

Every claimed benchmark result must be traceable to:

- Frozen candidate revision
- Benchmark task
- Environment
- Run record
- Raw or machine-readable result where available
- Failure/recovery evidence where applicable

## Security Boundary

The benchmark must not expose the host system, real credentials, private data, or production services to either candidate.

Security behavior must be evaluated separately from functional success.

## Acceptance Gate

Phase 2 cannot select a Base Agent until:

- Both eligible candidates have completed the defined baseline.
- The same evaluation protocol has been applied.
- Failures and recoveries are recorded.
- Measurements are reproducible.
- Evidence is traceable.
- Security boundaries have been evaluated.
- No candidate-specific modification occurred.
- Results have passed regression and adversarial review requirements.

## Output

Phase 2 produces:

1. Frozen benchmark specification.
2. Benchmark task registry.
3. Reproducible benchmark environment definition.
4. Candidate run records.
5. Raw evidence.
6. Comparative measurements.
7. Failure/recovery analysis.
8. Benchmark conclusion.

Phase 2 does NOT authorize Base Agent integration.

## IP Boundary

Benchmarking third-party candidates does not itself establish ownership, novelty, inventorship, or patentability.

Third-party candidate code and dependencies remain separately attributed.

Potential Saoub inventions or architectural contributions must be recorded in the Invention Ledger independently of benchmark outcomes.

## Exit Criteria

PHASE 2 may be approved only after the complete baseline benchmark, evidence audit, regression review, and adversarial review are passed.

FINAL APPROVAL: PENDING