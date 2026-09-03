# PHASE 2 — FROZEN PROVIDER REGISTRY

Status: FROZEN
Purpose: Reproducible multi-provider baseline.

## Initial Providers

| Provider | Class | Baseline Role |
|---|---|---|
| OpenAI | PAID / BYOK | General reasoning baseline |
| Anthropic | PAID / BYOK | General reasoning baseline |
| Google Gemini | FREE_TIER / PAID / BYOK | Alternative baseline |
| Ollama | FREE / LOCAL | Local-model baseline where hardware permits |

## Rules

1. Exact model IDs must be frozen in the benchmark run manifest before comparison.
2. Free/free-tier status is quota-dependent and must be recorded at run time.
3. No provider receives candidate-specific prompt or retry advantages.
4. Provider availability failure is classified separately from candidate failure.
5. Local Ollama runs must record exact model and hardware/runtime identity.
6. API keys are supplied only through GitHub Actions Secrets or an approved secret store.
7. No credentials are committed to the repository.
8. Benchmark artifacts contain provider/model identifiers and usage metadata only.
9. Provider/model changes require a new benchmark environment revision.
10. Results from different provider/model configurations must not be silently pooled.

## Required Environment Metadata

provider_id
model_id
model_revision_or_digest_when_available
pricing_class
quota_status
runtime
OS
architecture
candidate_commit
benchmark_revision

## Initial Baseline Matrix

The benchmark must execute candidates against the same frozen provider/model
configuration for each comparable test. If a provider cannot support a required
candidate capability, the run is marked NOT_APPLICABLE with evidence rather than
silently substituted.

## IP Boundary

Third-party providers and models remain separately attributed.
No ownership or patentability claim is made from provider selection or aggregation.
