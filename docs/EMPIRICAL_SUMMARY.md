# Empirical Summary of Experimental Results

## 1. Dataset Overview

* **Tasks Evaluated**: 3
  * Task A - Filtering
  * Task B - Aggregation
  * Task C - Transformation
* **Formats Evaluated**: 2
  * JSON
  * TOON
* **Total Runs**: 1 (Single iteration pilot)
* **Dimensions**: Task x Format

## 2. Token Usage Observations

* **Task A - Filtering**
  * JSON: 1474.0 mean total tokens
  * TOON: 716.0 mean total tokens
  * Difference: Δ = 758.0 tokens (TOON is ~51% lower)

* **Task B - Aggregation**
  * JSON: 1472.0 mean total tokens
  * TOON: 715.0 mean total tokens
  * Difference: Δ = 757.0 tokens (TOON is ~51% lower)

* **Task C - Transformation**
  * JSON: 1480.0 mean total tokens
  * TOON: 722.0 mean total tokens
  * Difference: Δ = 758.0 tokens (TOON is ~51% lower)

## 3. Cost Proxy Observations

* **Task A - Filtering**
  * JSON: $0.000227
  * TOON: $0.000113
  * Difference: $0.000114 (TOON is lower)

* **Task B - Aggregation**
  * JSON: $0.000226
  * TOON: $0.000113
  * Difference: $0.000113 (TOON is lower)

* **Task C - Transformation**
  * JSON: $0.000227
  * TOON: $0.000114
  * Difference: $0.000113 (TOON is lower)

## 4. Correctness Observations

* **Task A - Filtering**
  * JSON: 0.0 correctness rate
  * TOON: 0.0 correctness rate
  * Result: Identical (0% success).

* **Task B - Aggregation**
  * JSON: 0.0 correctness rate
  * TOON: 0.0 correctness rate
  * Result: Identical (0% success).

* **Task C - Transformation**
  * JSON: 0.0 correctness rate
  * TOON: 0.0 correctness rate
  * Result: Identical (0% success).

## 5. Failure Distribution Observations

* **Task A - Filtering**
  * JSON: 1 `parse_error` (100% of runs)
  * TOON: 1 `parse_error` (100% of runs)

* **Task B - Aggregation**
  * JSON: 1 `parse_error` (100% of runs)
  * TOON: 1 `parse_error` (100% of runs)

* **Task C - Transformation**
  * JSON: 1 `parse_error` (100% of runs)
  * TOON: 1 `parse_error` (100% of runs)

All failures were categorized as parse errors, indicating the mock model output "[MOCK_OUTPUT]..." could not be decoded as valid JSON or TOON.
