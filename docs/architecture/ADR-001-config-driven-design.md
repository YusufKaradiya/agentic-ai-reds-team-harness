# ADR-001: Configuration-Driven Security Architecture

## Status

Accepted

## Context

The red-team harness must support multiple attack
scenarios, tools and security policies.

Hardcoding these scenarios inside application logic
would reduce maintainability, extensibility and
reproducibility.

## Decision

Attack scenarios, tools, policies, model settings
and evaluation parameters will be represented using
version-controlled YAML configuration files.

Pydantic models will validate the loaded configuration.

## Consequences

### Positive

- New attacks can be added without modifying core logic.
- Policies can be changed independently.
- Experiments become reproducible.
- Configuration can be version controlled.
- The architecture becomes easier to test.

### Negative

- Configuration validation is required.
- Invalid configuration can cause runtime failures.
- YAML schemas need to be maintained.

## Security Impact

Configuration validation prevents malformed security
rules from silently entering the execution pipeline.