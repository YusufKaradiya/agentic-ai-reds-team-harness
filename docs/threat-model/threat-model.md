# Threat Model

## 1. System Boundary

The system contains:

- Streamlit frontend
- Agent controller
- Ollama model
- Retrieval system
- Vector database
- Attack corpus
- Defense engine
- Tool sandbox
- Audit database
- MLflow
- OpenTelemetry

---

## 2. Assets

The following assets require protection:

1. Synthetic secrets
2. Synthetic customer information
3. System instructions
4. Tool permissions
5. Retrieved documents
6. Security policies
7. Experiment results
8. Audit records

---

## 3. Trust Boundaries

### Boundary 1

User input → Agent

User input must be considered untrusted.

### Boundary 2

Retrieved documents → Agent

Retrieved content must not automatically be
considered trusted instructions.

### Boundary 3

Agent → Tools

Agent-generated tool requests must be authorized.

### Boundary 4

Agent → Output

Agent output must be checked for sensitive
information before being returned.

---

## 4. Threat Actors

### External Attacker

Attempts to manipulate the agent through prompts
or retrieved content.

### Malicious Document Author

Places adversarial instructions in documents.

### Unauthorized User

Attempts to access restricted information or tools.

### Accidental Malicious Input

A legitimate workflow may unintentionally contain
content that resembles an attack.

---

## 5. Threat Categories

| Threat | Asset | Impact | Control |
|---|---|---|---|
| Direct injection | Agent behaviour | High | Input detection |
| Indirect injection | RAG context | High | Content scanner |
| Tool abuse | Tool access | High | Sandbox |
| Secret extraction | Synthetic secrets | High | Secret detector |
| Parameter manipulation | Tool data | High | Validation |
| Log tampering | Audit evidence | Medium | Structured logging |
| Model/service failure | Availability | Medium | Failure handling |

---

## 6. Security Principles

### Least Privilege

Tools receive only the permissions required.

### Zero Trust for Retrieved Content

Retrieved documents are treated as untrusted data.

### Defense in Depth

Multiple controls are used rather than relying on
one detector.

### Auditability

Important security decisions are logged.

### Reproducibility

Attack definitions and experiment configurations
are version controlled.

### Privacy by Design

Only synthetic data is used.