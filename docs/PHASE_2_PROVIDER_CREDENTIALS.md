# PHASE 2 — PROVIDER & CREDENTIALS CONTRACT

Status: FROZEN
Purpose: Multi-provider model access without provider lock-in.

## Provider Classes

- FREE: no payment required within the provider's current free policy.
- FREE_TIER: limited free quota.
- PAID: paid usage.
- BYOK: user supplies their own credential.

Provider pricing/quota status must never be hard-coded as permanently free.

## Credential Security

1. Secrets are never stored in source code.
2. Secrets are never written to benchmark artifacts or logs.
3. UI fields must be masked/password inputs.
4. Stored credentials must use an approved encrypted secret store.
5. Full credentials are never returned after storage.
6. Revoke and rotation must be supported.
7. Access follows least privilege.
8. Credentials are injected only at execution time when required.
9. Failed authentication must not expose the secret.
10. Telemetry/evidence must contain metadata only, never secret values.

## Provider Abstraction

Each provider must expose:

- provider_id
- model_id
- capability metadata
- pricing_class
- quota metadata
- credential_type
- availability/status
- health check
- invocation interface
- timeout policy
- error classification
- usage/cost metadata when available

Saoub execution logic must depend on the abstraction, not provider-specific application logic.

## Selection Policies

Supported policy concepts:

- AUTO
- FREE_FIRST
- LOWEST_COST
- USER_SELECTED
- BYOK_ONLY

Selection must remain deterministic and auditable for benchmark runs.

## Benchmark Fairness

Provider/model choice is part of the frozen benchmark environment.
Changing provider, model, limits, prompts, retry policy, or quota handling for only one candidate is prohibited.

## Initial Provider Registry

No provider is permanently mandated by this document.
Providers are added only when required by an approved benchmark or product capability,
with license, security, availability, cost, and reproducibility evidence.

## IP Boundary

Provider APIs, models, SDKs, and third-party infrastructure remain separately attributed.
The provider abstraction itself is not claimed as a patentable invention.
Potential Saoub-specific technical mechanisms must be recorded independently in the Invention Ledger.

## Acceptance

Before production use:

- credential storage security verified
- secret redaction tested
- provider health checks tested
- quota/error handling tested
- auditability verified
- no-secret-leak adversarial test passed
