# Research and Evaluation Protocol

## Baseline

The baseline system will use the agent with
minimal or no dedicated security controls.

## Proposed System

The proposed system will include:

- input security checks;
- retrieved-content scanning;
- sensitive-data detection;
- tool authorization;
- tool sandboxing;
- audit logging.

## Attack Dataset

The initial corpus will contain approximately
25-30 controlled attack scenarios.

Categories:

1. Direct prompt injection
2. Indirect prompt injection
3. Tool abuse
4. Data exfiltration

## Legitimate Tasks

A separate set of legitimate tasks will be used
to measure false blocks and task utility.

## Experimental Comparison

The same scenarios will be executed against:

A. Baseline agent

B. Defended agent

## Repeated Runs

Selected experiments will be repeated to evaluate
reproducibility.

## Reporting

Results will include:

- security metrics;
- utility metrics;
- latency;
- failure cases;
- limitations;
- residual risks.