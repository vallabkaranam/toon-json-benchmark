# Dataset Specification (Realistic Synthetic Logs)

## Purpose
Synthetic but structurally realistic logs inspired by production systems.

## Dataset Size
- Target: 200 records
- Range: 100–300

## Record Schema
Each record represents one event.

Fields:
- id (string)
- timestamp (ISO string)
- service (string)
- env (enum: prod, staging, dev)
- type (enum: auth, payment, system, network, job)
- status (enum: success, failed, warning)
- severity (int 1–5)
- source (string)
- metadata (object)
- message (string)

### Metadata Fields
- request_id (string)
- user_id (string)
- region (string)
- retry_count (int)
- latency_ms (number)
- tags (array)

## Allowed Tags
auth, payment, infra, edge, batch, critical

## Distribution Guidelines
- status: 60% success / 25% failed / 15% warning
- env: 70% prod / 20% staging / 10% dev
- severity: skewed toward 2–4

## Determinism
- Fixed random seed
- Stable ordering
- Sorted by timestamp + id

## Output
data/events.json
data/schema.json
