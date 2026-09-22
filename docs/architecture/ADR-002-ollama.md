# ADR-002: Local LLM Through Ollama

## Status

Accepted

## Decision

Ollama will be used as the local model runtime
for the prototype.

## Reasons

- Local execution
- Reduced dependency on external APIs
- Easier reproducibility
- Better privacy for synthetic test data
- Configurable model selection

## Limitations

- Model performance depends on available hardware.
- Different models may produce different results.
- Evaluation must record the model version/configuration.