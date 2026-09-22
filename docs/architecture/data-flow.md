
---

# 11. Data Flow Diagram

Create:

```text
docs/architecture/data-flow.md
# Data Flow

```text
                    USER INPUT
                        │
                        ▼
                 ┌─────────────┐
                 │ Input Scan  │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │ Agent       │
                 │ Controller  │
                 └──────┬──────┘
                        │
               ┌────────┴─────────┐
               ▼                  ▼
          RAG Retrieval       Attack Engine
               │
               ▼
       Retrieved Documents
               │
               ▼
        Content Security
               │
               ▼
             Ollama
               │
               ▼
        Tool Authorization
               │
               ▼
          Tool Sandbox
               │
               ▼
          Mock Tool
               │
               ▼
       Output Security
               │
               ▼
            Response

All stages
    │
    ├── Audit DB
    ├── OpenTelemetry
    └── MLflow