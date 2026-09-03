# PHASE 2 — CANDIDATE ADAPTER CONTRACT

Status: FROZEN
Purpose: Define the neutral execution boundary between the benchmark runner and frozen third-party candidates.

## Frozen Candidates

- OpenHands: 64c1269655012698bc66538967989996191beb6c
- Browser Use: eb4126921bea3373f91afc49fb4b59d6eda7fed6

## Core Rule

Adapters are Saoub benchmark infrastructure only.

They MUST NOT modify, patch, fork, monkey-patch, or alter candidate source code.

The adapter MUST invoke the frozen candidate revision through its documented public/runtime interface.

## Adapter Interface

Each adapter MUST expose:

- candidate_id
- candidate_commit
- runtime_version
- prepare()
- execute(task, provider_config)
- collect_observations()
- collect_evidence()
- classify_failure()
- cleanup()

## Execution Contract

For every run:

1. Validate candidate identity against the frozen commit.
2. Validate provider/model configuration.
3. Start from an isolated benchmark environment.
4. Create a fresh candidate execution context.
5. Execute exactly one benchmark task.
6. Record start and end status.
7. Record tool/browser actions where available.
8. Record recovery attempts.
9. Capture final state.
10. Capture machine-readable evidence.
11. Classify failures.
12. Clean up the execution context.
13. Never perform hidden retries.

## Provider Contract

Provider configuration MUST contain:

- provider_id
- model_id
- pricing_class
- quota_status

Secrets MUST be supplied only through environment variables populated from GitHub Actions Secrets or an approved secret store.

Secrets MUST NOT appear in:

- source files
- task definitions
- logs
- benchmark results
- evidence artifacts
- exception messages

## Fairness

Both candidates MUST receive:

- identical task definitions
- identical success criteria
- identical repetition count
- identical provider/model configuration for comparable tasks
- equivalent execution isolation
- equivalent retry policy
- equivalent evidence requirements

Candidate-specific optimization is prohibited.

## Failure Boundary

The adapter MUST distinguish at minimum:

- candidate failure
- adapter failure
- provider failure
- environment/runtime failure
- timeout
- security/permission failure
- external dependency failure
- unknown failure

Provider or environment failures MUST NOT be scored as candidate failures.

## Security

Adapters MUST NOT:

- expose the host filesystem unnecessarily
- expose host credentials
- access production services
- use real private user data
- bypass candidate security controls
- silently broaden permissions

All benchmark credentials MUST be synthetic or benchmark-scoped.

## Reproducibility

Every run MUST record:

- benchmark_revision
- candidate_id
- candidate_commit
- adapter_revision
- provider_id
- model_id
- runtime
- OS
- architecture
- environment_id

Candidate source revisions are immutable for this benchmark.

## Evidence

Each successful or failed run MUST produce sufficient machine-readable evidence to independently determine:

- what was requested
- what was executed
- what was observed
- what failed
- what was recovered
- what final state was reached
- whether success criteria were satisfied

## Prohibited Shortcuts

Adapters MUST NOT:

- return synthetic success
- fabricate tool calls
- fabricate observations
- fabricate evidence
- replace candidate execution with direct task execution
- use prebuilt Saoub workflows
- silently retry failed runs
- modify benchmark success criteria per candidate

## Acceptance

The adapter layer is accepted only when:

1. Both adapters execute the frozen candidates.
2. Candidate source remains unmodified.
3. Provider configuration is identical for comparable runs.
4. Failures are correctly separated by boundary.
5. Evidence is machine-readable and traceable.
6. Security isolation is verified.
7. Repeated execution is reproducible.
8. Adapter tests pass.
9. Regression review passes.
10. Adversarial review passes.

This contract does not constitute Phase 2 approval and does not authorize Base Agent integration.
