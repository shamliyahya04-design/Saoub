# PHASE 2 — FROZEN BENCHMARK MODEL

Status: FROZEN

| Field | Value |
|---|---|
| provider_id | google |
| model_id | gemini-2.5-flash |
| credential | GOOGLE_API_KEY |
| fallback | NONE |

1. Both frozen candidates MUST use the same provider/model configuration.
2. The model ID MUST remain exactly `gemini-2.5-flash`.
3. Provider/model failures MUST be classified separately from candidate failures.
4. No silent provider or model substitution is permitted.
5. Credentials MUST NOT be committed or included in artifacts.
6. Changes to provider/model configuration require a new benchmark revision and re-audit.
