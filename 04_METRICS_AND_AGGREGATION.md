# Metrics & Aggregation

## Metrics

### Efficiency
- input_tokens
- output_tokens
- total_tokens
- estimated_cost

### Correctness
- exact_match
- schema_valid
- missing_fields
- incorrect_values

### Stability
- determinism_rate
- output_variance

### Failures
- parse_error
- schema_violation
- hallucination
- aggregation_error

## Aggregation
Metrics aggregated by:
- task
- representation

## Output Tables
- summary.csv
- per_task_metrics.csv
- failure_breakdown.csv

## Interpretation Rules
Allowed:
- token efficiency comparison
- correctness comparison
- stability comparison

Disallowed:
- claims of superiority
- generalization beyond benchmark

Purpose: reproducible, defensible evaluation.
