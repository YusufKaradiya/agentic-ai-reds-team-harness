
---

# 8. Direct Injection Sequence

Create:

```text
docs/architecture/sequence-direct-injection.md
# Direct Prompt Injection Sequence

```text
Attacker
 │
 │ Malicious prompt
 ▼
Streamlit
 │
 ▼
Agent Controller
 │
 ▼
Input Defense
 │
 │ SUSPICIOUS
 ▼
Policy Engine
 │
 │ BLOCK
 ▼
Audit Logger
 │
 ▼
Evaluation Engine
 │
 ▼
Security Result