
---

# 10. Tool Abuse Sequence

Create:

```text
docs/architecture/sequence-tool-abuse.md
# Tool Abuse Sequence

```text
User / Attacker
       │
       ▼
     Agent
       │
       │ Tool Request
       ▼
 Tool Permission Manager
       │
       ├── Unknown Tool → DENY
       │
       ├── Unauthorized → DENY
       │
       ├── High Risk → APPROVAL
       │
       └── Authorized → ALLOW
                              │
                              ▼
                         Mock Tool
                              │
                              ▼
                         Audit Log