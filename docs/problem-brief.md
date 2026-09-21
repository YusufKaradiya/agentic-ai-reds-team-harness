# Industry Problem Brief

## 1. Project Title

Agentic AI Red-Team Harness for Prompt Injection,
Tool Abuse and Data Exfiltration

---

## 2. Industry Problem

Modern AI assistants increasingly use external tools,
retrieval systems and enterprise data sources.

This creates a larger attack surface than a standalone
question-answering model.

An attacker may attempt to:

- override system instructions;
- manipulate the agent through malicious user input;
- place malicious instructions inside retrieved documents;
- force unauthorized tool calls;
- manipulate tool parameters;
- extract confidential information;
- cause the agent to disclose system instructions;
- combine multiple seemingly harmless actions into a harmful workflow.

The project addresses this problem through a controlled
red-team testing environment.

---

## 3. Proposed Solution

The proposed system is a configurable red-team harness
for evaluating an agentic AI system.

The platform will:

1. Load attack scenarios from a configurable attack corpus.
2. Execute direct and indirect injection tests.
3. Test tool authorization and sandbox controls.
4. Scan user input and retrieved content.
5. Detect synthetic sensitive data.
6. Record security decisions and audit events.
7. Measure security and utility metrics.
8. Compare a baseline agent against a defended agent.
9. Produce residual-risk reports.

---

## 4. Scope

### Included

- Prompt injection
- Indirect prompt injection
- RAG poisoning scenarios
- Tool abuse
- Unauthorized tool access
- Sensitive-data leakage
- Synthetic secrets
- Mock tools
- Local/approved LLMs
- Configurable policies
- Security evaluation
- Observability
- Audit logging
- Reproducibility testing

### Excluded

- Real production systems
- Real customer data
- Real credentials
- Destructive external tools
- Real financial transactions
- Real email transmission
- Real infrastructure exploitation
- Malware deployment
- Unauthorized testing of external systems

---

## 5. Stakeholders

### AI Developers

Need to understand whether their agents can be
manipulated by malicious instructions.

### Security Reviewers

Need repeatable security tests and measurable
attack outcomes.

### Model Governance Teams

Need evidence about residual risk, controls and
system behaviour.

### Product Owners

Need evidence that security controls do not
unnecessarily reduce task utility.

### Researchers

Need reproducible experiments and measurable
comparisons between defensive approaches.

---

## 6. Business/Industry Pain Points

- Manual security testing is difficult to repeat.
- Attack scenarios are often undocumented.
- Tool permissions may be overly broad.
- Retrieved content may contain untrusted instructions.
- Security decisions may not be fully logged.
- Security controls can introduce false blocks.
- Security improvements may reduce task utility.
- Residual risk is difficult to quantify.

---

## 7. Proposed Success Criteria

The prototype should:

- execute at least 25 attack scenarios;
- support at least four attack categories;
- support at least four mock tools;
- compare baseline and defended configurations;
- record security decisions;
- measure attack success rate;
- measure sensitive-data leakage;
- measure false block rate;
- measure task utility;
- measure latency;
- provide reproducible experiments;
- run through documented setup instructions.

---

## 8. Non-Functional Requirements

### Security

No production secrets or personal data.

### Privacy

Only synthetic data is used.

### Reproducibility

Attack corpus and configurations are version controlled.

### Observability

Important system events must be traceable.

### Reliability

The system should handle invalid input,
missing tools and service failures.

### Maintainability

Attack scenarios and policies should be
configuration-driven rather than embedded
through application logic.

### Testability

Core security components must have automated tests.