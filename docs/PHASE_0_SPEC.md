# Saoub — PHASE 0 Engineering Specification

## Objective

Establish a clean, auditable, production-grade foundation for Saoub before Base Agent Selection.

## Mandatory Constraints

- GitHub is the sole project source of truth.
- No local Git repository.
- Termux is execution/inspection only.
- No secrets, API keys, or credentials in source files.
- No modification of a Base Agent before baseline benchmarking.
- No ready-made workflows as the Saoub solution.
- No phase may be approved based on green tests alone.

## Repository Foundation

Required top-level areas:

- base/
- benchmark/
- core/
- outcome/
- state/
- execution/
- verification/
- critic/
- repair/
- proof/
- memory/
- security/
- tests/
- docs/
- experiments/
- ip/

## Engineering Principles

1. Production-grade architecture from the beginning.
2. Explicit contracts between components.
3. Deterministic behavior where deterministic behavior is possible.
4. Observable execution and reproducible evidence.
5. Root-cause correction instead of test-specific patches.
6. Security and permissions are architectural concerns.
7. Every major architectural decision must be testable and auditable.
8. Important outcomes must be verifiable and provable.

## IP Track

Engineering work runs in parallel with the IP protocol.

Required records:

- Invention Ledger
- Prior Art Register
- Patent Boundary
- IP Decisions

No novelty claim is accepted without prior-art analysis.

## Phase 0 Exit Criteria

Phase 0 can be approved only when:

- Repository foundation is verified on GitHub.
- Engineering specification is present.
- IP protocol is present.
- No local Git repository is used.
- Baseline architecture and constraints are documented.
- Phase 0 audit is complete.
- Weaknesses are identified and resolved or explicitly deferred with justification.
- Evidence is recorded for all approval criteria.

## Next Phase

After formal Phase 0 approval, proceed to:

PHASE 1 — Base Agent Selection.

Base agents must first be evaluated independently and unmodified.