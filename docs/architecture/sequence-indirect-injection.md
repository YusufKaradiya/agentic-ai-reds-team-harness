
---

# 9. Indirect Injection Sequence

Create:

```text
docs/architecture/sequence-indirect-injection.md
# Indirect Prompt Injection Sequence

```text
User
 │
 │ Normal request
 ▼
Agent Controller
 │
 ▼
Retriever
 │
 ▼
Vector Database
 │
 ▼
Potentially Malicious Document
 │
 ▼
Retrieved Content Scanner
 │
 ├── SAFE ────────────────┐
 │                        │
 └── SUSPICIOUS → QUARANTINE
                          │
                          ▼
                       Audit Log

SAFE content continues:

Scanner
 │
 ▼
Ollama
 │
 ▼
Tool Policy
 │
 ▼
Response