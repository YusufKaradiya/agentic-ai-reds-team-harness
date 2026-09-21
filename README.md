# Agentic AI Red-Team Harness

## Project Overview

The Agentic AI Red-Team Harness is a security testing platform for evaluating
tool-enabled and retrieval-augmented AI agents against prompt injection,
indirect prompt injection, tool abuse and sensitive-data exfiltration.

The system provides:

- Threat modelling
- Configurable attack corpus
- Direct prompt injection testing
- Indirect prompt injection testing
- Tool permission sandbox
- Sensitive-data detection
- RAG security testing
- Audit logging
- OpenTelemetry observability
- MLflow experiment tracking
- Security scorecards
- Residual-risk reporting

## Objectives

1. Detect prompt injection attacks.
2. Detect malicious instructions in retrieved content.
3. Prevent unauthorized tool usage.
4. Detect sensitive-data leakage.
5. Measure attack success rate.
6. Measure false block rate.
7. Measure task utility.
8. Measure latency.
9. Evaluate reproducibility.
10. Generate residual-risk reports.

## Technology Stack

- Python
- PyTorch
- Hugging Face Transformers
- Ollama
- MLflow
- Docker
- Kubernetes
- Chroma/Qdrant
- OpenTelemetry
- Streamlit
- Git
- PyTest

## Security Scope

The system uses only:

- Synthetic secrets
- Mock tools
- Isolated documents
- Local or approved LLMs
- Non-production data

No real customer credentials, production systems,
financial accounts or external destructive tools are used.

## Project Status

Day 1 - Requirements and research foundation.