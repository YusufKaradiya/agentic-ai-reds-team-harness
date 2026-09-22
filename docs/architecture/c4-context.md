# C4 Context Diagram

```text
                    ┌────────────────────┐
                    │      Security      │
                    │      Reviewer      │
                    └─────────┬──────────┘
                              │
                              ▼
                  ┌──────────────────────────┐
                  │ Agentic AI Red-Team      │
                  │ Harness                  │
                  │                          │
                  │ Security Testing Platform│
                  └───────┬────────┬─────────┘
                          │        │
              ┌───────────┘        └────────────┐
              ▼                                 ▼
      ┌─────────────────┐              ┌─────────────────┐
      │ Local/Approved  │              │ Synthetic Data  │
      │ LLM / Ollama    │              │ & Mock Tools    │
      └─────────────────┘              └─────────────────┘

                          │
                          ▼
                 ┌──────────────────┐
                 │ MLflow /          │
                 │ OpenTelemetry     │
                 └──────────────────┘