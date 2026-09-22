
---

# 7. Normal Request Sequence

Create:

```text
docs/architecture/sequence-normal.md
# Normal Request Sequence

```text
User
 │
 │ Legitimate task
 ▼
Streamlit
 │
 ▼
Agent Controller
 │
 ▼
Input Defense
 │
 │ ALLOW
 ▼
RAG Retriever
 │
 ▼
Retrieved Content Scanner
 │
 │ SAFE
 ▼
Ollama
 │
 ▼
Tool Policy
 │
 │ ALLOW
 ▼
Mock Tool
 │
 ▼
Output Security Check
 │
 │ SAFE
 ▼
Audit Logger
 │
 ▼
User Response