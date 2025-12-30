# Task Execution & Evaluation

## Tasks

### Task A — Filtering
Return records where:
- status = failed
- severity ≥ 3
- env = prod

### Task B — Aggregation
For each type:
- total count
- failed count
- average severity

### Task C — Transformation
Flatten to:
- id
- timestamp
- service
- env
- type
- status
- severity
- region
- latency_ms

## System Prompt
You are a deterministic data processing system.
Follow instructions exactly.
Do not add explanations.
Return only the requested output.
Use the same representation format as the input.

## Prompt Template
You are given a dataset encoded in <FORMAT>.

<Task description>

Dataset:
<DATA>

## Determinism
- temperature = 0
- fixed prompt
- repeated runs allowed

## Output Rules
- Machine parseable
- No commentary
- Schema-valid

## Failure Types
- parse_error
- schema_violation
- incorrect_result
- hallucination
- nondeterministic_output
