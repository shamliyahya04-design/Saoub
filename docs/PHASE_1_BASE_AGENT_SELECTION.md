# Saoub — PHASE 1 Base Agent Selection

## Objective
Select eligible Base Agents objectively before any modification or integration.

## Mandatory Constraints
- Base Agents are evaluated independently and unmodified.
- No ready-made workflows are adopted as Saoub solutions.
- No integration before benchmark evidence.
- No selection based on reputation or preference alone.
- GitHub is the sole source of truth.
- No local Git repository.
- No branches.
- No secrets or credentials.
- No candidate-specific optimization before baseline benchmarking.

## Candidate Registry
Initial candidates for evaluation:
1. OpenHands
2. Browser Use

Candidate status at Phase 1 start:
- Candidate identity: recorded.
- Technical eligibility: pending evidence.
- License compatibility: pending verification.
- Maintainability/activity: pending verification.
- Capability fit: pending verification.
- Benchmark eligibility: pending final gate.

Additional candidates may be added only when there is a documented engineering reason and before the final Phase 1 selection gate.

## Candidate Eligibility Gate
A candidate must satisfy all mandatory gates:
1. Runnable in its original form.
2. License is identified and compatible with Saoub use.
3. Relevant autonomous-execution capabilities are documented.
4. Project maintenance/activity is sufficient for the intended role.
5. Required interfaces/control and observability are available.
6. No Saoub-specific modification is required before baseline evaluation.
7. Dependencies and runtime requirements are reproducible.
8. Security and permission boundaries can be identified.
9. Benchmark execution can be performed without changing the candidate.
10. IP/provenance boundaries can be documented.

Failure of any mandatory gate results in EXCLUDED or DEFERRED status with a documented reason.

## Exclusion Gates
A candidate must not proceed to Phase 2 if:
- It requires source modification to demonstrate its baseline capability.
- Its licensing/provenance cannot be established sufficiently.
- Its required runtime cannot be reproduced.
- Its essential behavior cannot be observed or measured.
- It cannot operate within the approved benchmark environment.
- Its security boundary creates an unacceptable unmitigated risk.
- Evidence is insufficient to make a defensible comparison.

Exclusion is not a negative quality judgment; it means the candidate is not eligible for the defined baseline.

## Evaluation Scoring Rubric
Each eligible candidate is scored from 0–10 in every dimension.

Weights:
- General task execution: 15%
- Tool use: 10%
- Browser/computer interaction: 10%
- Planning/reasoning: 10%
- Reliability: 15%
- Recovery capability: 10%
- Observability: 5%
- Extensibility: 5%
- Security boundaries: 5%
- Performance/cost: 5%
- Documentation/maintainability: 5%
- License/IP compatibility: 5%

Weighted score = sum(score × dimension weight).

Scoring rules:
- 0–2: unacceptable
- 3–4: weak
- 5–6: adequate
- 7–8: strong
- 9–10: exceptional

A high weighted score alone cannot override a failed mandatory eligibility gate.

## Evidence Requirements
Every material score or selection claim must have reproducible evidence.
Evidence may include:
- Official documentation
- Source repository information
- Reproducible runtime tests
- Benchmark measurements
- Failure/recovery observations
- Security and permission analysis
- License/provenance records

Subjective impressions must never be used as primary evidence.

## Anti-Bias Rules
- The same benchmark inputs and success criteria must be used for comparable candidates.
- Candidate-specific advantages must not be embedded into the benchmark.
- No candidate receives architectural modifications before baseline measurement.
- No candidate is selected because it appears easier to integrate.
- Benchmark results must be recorded before architectural role assignment.

## Selection Rule
Phase 1 does not select a final winner based on reputation, documentation quality, or preliminary inspection.

Phase 1 produces:
1. Eligible candidate set.
2. Eligibility evidence.
3. Fixed scoring rubric.
4. Known limitations and risks.
5. IP/provenance boundary.
6. Benchmark-ready candidate definitions.

Final capability selection occurs only after Phase 2 baseline benchmark evidence.

## IP Boundary
Base Agent code, third-party libraries, generic models, and generic capabilities are not Saoub inventions.

Potential Saoub inventions must be recorded separately in the Invention Ledger and evaluated against prior art.

No novelty, inventive-step, or patentability claim may be made solely from candidate selection or tool aggregation.

## Selection Gate
PHASE 1 may be approved only when:
- Candidate registry is complete.
- Eligibility has been verified with evidence.
- Scoring rubric and weights are frozen before benchmarking.
- Exclusion gates are defined.
- Anti-bias rules are defined.
- IP boundaries are documented.
- Risks and limitations are recorded.
- Benchmark inputs and success criteria are protected from candidate-specific bias.
- Final engineering and IP review confirms readiness for Phase 2.

## Exit Criteria
PHASE 1 is not complete until all selection gates pass and a final audit explicitly approves transition to PHASE 2 — Baseline Benchmark.

## Phase Status
STATUS: IN PROGRESS
APPROVAL: PENDING

## Final Approval

PHASE 1 — BASE AGENT SELECTION: APPROVED

Approval: FINAL
Approved for transition to PHASE 2 — Baseline Benchmark
