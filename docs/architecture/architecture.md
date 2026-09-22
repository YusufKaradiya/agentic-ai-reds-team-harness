# System Architecture

## 1. Purpose

The Agentic AI Red-Team Harness is a modular security
testing platform for evaluating an AI agent against:

- Direct prompt injection
- Indirect prompt injection
- Tool abuse
- Sensitive-data exfiltration

The system uses configuration-driven components so that
attacks, tools, policies and model settings can be modified
without changing core application logic.

---

## 2. Architectural Principles

### Configuration Driven

Attack scenarios, tools, policies and model settings
are defined through YAML configuration files.

### Defense in Depth

Multiple security layers are applied:

1. Input security
2. Retrieved-content security
3. Tool authorization
4. Output/data leakage detection

### Least Privilege

Tools are granted only the permissions they require.

### Zero Trust for Retrieved Content

Retrieved documents are treated as untrusted content.

### Observability

Security decisions, model interactions, tool calls
and failures are recorded.

### Reproducibility

Attack definitions, datasets, model configuration
and experiment configuration are version controlled.

### Privacy

Only synthetic data and isolated mock tools are used.

---

## 3. Main Components

### Streamlit UI

Provides:

- Attack selection
- Test execution
- Results
- Evaluation metrics
- Tool sandbox information
- Residual-risk reports

### Agent Controller

Coordinates the complete workflow.

### Attack Engine

Loads and executes attack scenarios from configuration.

### Defense Engine

Evaluates user input and retrieved content.

### RAG Security Layer

Retrieves documents and checks retrieved content
before passing it to the agent.

### Ollama Adapter

Provides the local LLM interface.

### Tool Sandbox

Validates agent tool requests against configured
permissions and risk policies.

### Audit Logger

Stores security events and decisions.

### Evaluation Engine

Calculates:

- Attack success rate
- Leakage rate
- False block rate
- Utility
- Latency
- Reproducibility

### MLflow

Stores experiment configuration and metrics.

### OpenTelemetry

Provides traces and metrics across the workflow.

---

## 4. Security Boundary

All external or potentially attacker-controlled
content is treated as untrusted.

Examples:

- User prompts
- Retrieved documents
- Tool parameters
- Model-generated tool requests

---

## 5. Data Flow

User request:

User
→ Input Defense
→ Agent Controller
→ RAG
→ Retrieved Content Scanner
→ Ollama
→ Tool Policy
→ Tool Sandbox
→ Tool
→ Output Security Check
→ Response

---

## 6. Failure Handling

The system must handle:

- Invalid attack configuration
- Unknown attack ID
- Unknown tool
- Unauthorized tool request
- Invalid tool parameters
- Vector database failure
- Ollama unavailable
- Model timeout
- Malformed user input

Security failures must fail closed where appropriate.