# Empirical Facts from Experimental Results

## 1. summary.csv

* **Task**: Task A - Filtering
  * **Format**: JSON
  * **mean_input_tokens**: 1462.0
  * **mean_output_tokens**: 12.0
  * **mean_total_tokens**: 1474.0
  * **mean_estimated_cost**: 0.000227
  * **correctness_rate**: 0.0
  * **error_rate**: 1.0

* **Task**: Task A - Filtering
  * **Format**: TOON
  * **mean_input_tokens**: 704.0
  * **mean_output_tokens**: 12.0
  * **mean_total_tokens**: 716.0
  * **mean_estimated_cost**: 0.000113
  * **correctness_rate**: 0.0
  * **error_rate**: 1.0

* **Task**: Task B - Aggregation
  * **Format**: JSON
  * **mean_input_tokens**: 1460.0
  * **mean_output_tokens**: 12.0
  * **mean_total_tokens**: 1472.0
  * **mean_estimated_cost**: 0.000226
  * **correctness_rate**: 0.0
  * **error_rate**: 1.0

* **Task**: Task B - Aggregation
  * **Format**: TOON
  * **mean_input_tokens**: 703.0
  * **mean_output_tokens**: 12.0
  * **mean_total_tokens**: 715.0
  * **mean_estimated_cost**: 0.000113
  * **correctness_rate**: 0.0
  * **error_rate**: 1.0

* **Task**: Task C - Transformation
  * **Format**: JSON
  * **mean_input_tokens**: 1468.0
  * **mean_output_tokens**: 12.0
  * **mean_total_tokens**: 1480.0
  * **mean_estimated_cost**: 0.000227
  * **correctness_rate**: 0.0
  * **error_rate**: 1.0

* **Task**: Task C - Transformation
  * **Format**: TOON
  * **mean_input_tokens**: 710.0
  * **mean_output_tokens**: 12.0
  * **mean_total_tokens**: 722.0
  * **mean_estimated_cost**: 0.000114
  * **correctness_rate**: 0.0
  * **error_rate**: 1.0

## 2. failure_breakdown.csv

* **Task**: Task A - Filtering
  * **Format**: JSON
  * **Failure type**: parse_error
  * **Count**: 1

* **Task**: Task A - Filtering
  * **Format**: TOON
  * **Failure type**: parse_error
  * **Count**: 1

* **Task**: Task B - Aggregation
  * **Format**: JSON
  * **Failure type**: parse_error
  * **Count**: 1

* **Task**: Task B - Aggregation
  * **Format**: TOON
  * **Failure type**: parse_error
  * **Count**: 1

* **Task**: Task C - Transformation
  * **Format**: JSON
  * **Failure type**: parse_error
  * **Count**: 1

* **Task**: Task C - Transformation
  * **Format**: TOON
  * **Failure type**: parse_error
  * **Count**: 1

## 3. per_task_metrics.csv (Sample)

* **run_id**: run_af88a7e7
  * **task**: Task A - Filtering
  * **format**: JSON
  * **input_tokens**: 1462
  * **output_tokens**: 12
  * **total_tokens**: 1474
  * **estimated_cost**: 0.0002265
  * **is_correct**: False
  * **error_types**: parse_error: JSON decode failed: Expecting value: line 1 column 2 (char 1)

* **run_id**: run_af88a7e7
  * **task**: Task A - Filtering
  * **format**: TOON
  * **input_tokens**: 704
  * **output_tokens**: 12
  * **total_tokens**: 716
  * **estimated_cost**: 0.0001128
  * **is_correct**: False
  * **error_types**: parse_error: TOON decode failed: Invalid collection header: [MOCK_OUTPUT] Processed input length 2634 chars.

* **run_id**: run_af88a7e7
  * **task**: Task B - Aggregation
  * **format**: JSON
  * **input_tokens**: 1460
  * **output_tokens**: 12
  * **total_tokens**: 1472
  * **estimated_cost**: 0.0002262
  * **is_correct**: False
  * **error_types**: parse_error: JSON decode failed: Expecting value: line 1 column 2 (char 1)

* **run_id**: run_af88a7e7
  * **task**: Task B - Aggregation
  * **format**: TOON
  * **input_tokens**: 703
  * **output_tokens**: 12
  * **total_tokens**: 715
  * **estimated_cost**: 0.00011265
  * **is_correct**: False
  * **error_types**: parse_error: TOON decode failed: Invalid collection header: [MOCK_OUTPUT] Processed input length 2628 chars.

* **run_id**: run_af88a7e7
  * **task**: Task C - Transformation
  * **format**: JSON
  * **input_tokens**: 1468
  * **output_tokens**: 12
  * **total_tokens**: 1480
  * **estimated_cost**: 0.0002274
  * **is_correct**: False
  * **error_types**: parse_error: JSON decode failed: Expecting value: line 1 column 2 (char 1)
