# Evaluating Representation Choices in LLM Pipelines

## 1. Abstract

Large language model systems increasingly rely on structured inputs, yet the effects of representation choices—such as JSON, XML, or custom DSLs—are rarely measured explicitly. This study presents a reproducible evaluation framework for identifying trade-offs in token usage, cost, and correctness across prompt representations. Using a synthetic task suite, we compare standard JSON against a compact line-oriented format (TOON). Our results indicate that representation choice significantly impacts input verbosity, with TOON reducing token counts by approximately 51% in our test cases. While functional correctness could not be assessed due to the use of a mock execution backend, the framework successfully demonstrates the infrastructure required for systematic prompt engineering experiments.

## 2. Motivation

Most applied LLM systems depend on structured formats for data interchange and function calling. JSON is the de facto standard, chosen largely for widespread library support and human readability. However, in token-constrained environments—such as high-throughput agents or long-context retrieval—verbosity becomes a tangible cost. Furthermore, different representations may induce different failure modes, such as syntax errors or hallucinations.

Despite these implications, the "representation layer" is rarely treated as a systems design variable. This project establishes a methodology to evaluate prompts as engineering artifacts, measuring their efficiency and robustness under controlled conditions.

## 3. System Overview

The evaluation pipeline is designed as a modular, deterministic system:

1.  **Dataset Generation**: Creates synthetic event streams acting as ground truth.
2.  **Representation Encoding**: Encodes the same data into multiple formats (JSON and TOON).
3.  **Prompt Execution**: Wraps encoded data in task-specific instructions and sends them to a model interface.
4.  **Logging**: Captures raw text outputs, timing, and metadata.
5.  **Evaluation**: Parses outputs and verifies them against deterministic logic checks.
6.  **Analysis**: Aggregates metrics and generates visual artifacts.

This separation of concerns ensures that the evaluation logic remains consistent regardless of the underlying model or representation.

## 4. Experimental Design

### Tasks
To simulate realistic workloads, we evaluate three task archetypes:
*   **Filtering**: Selecting records matching specific criteria.
*   **Aggregation**: Computing summary statistics (e.g., counts, sums).
*   **Transformation**: Converting records from one schema to another.

### Representations
*   **JSON**: The standard, verbose format used in most APIs.
*   **TOON (Task-Oriented Object Notation)**: A compact, line-oriented format designed to minimize syntactic overhead (e.g., closing braces, excessive quotes).

### Controls
All runs use a fixed random seed (42) to ensure identical datasets. The logic for task evaluation is shared across formats to isolate representation as the single independent variable.

## 5. Results

The following results are derived from a pilot execution using a mock model backend. Comprehensive empirical data is available in [`docs/EMPIRICAL_FACTS.md`](docs/EMPIRICAL_FACTS.md).

### 5.1 Token Usage and Cost
The primary finding from this pilot is the efficiency delta between formats.
*   **JSON**: Averaged ~1470 total tokens per task.
*   **TOON**: Averaged ~715 total tokens per task.

This represents a **~51% reduction in token usage** for the TOON format (see Figure 1). In a production environment, this linear savings would translate directly to reduced inference latency and cost (see Figure 2).

### 5.2 Correctness and Failures
As expected with a mock backend producing placeholder text, the correctness rate was 0.0 for all runs. The system correctly identified these invalid outputs as failures.
*   **Failure Type**: `parse_error` was the sole failure mode observed.
*   **Robustness**: The evaluation pipeline successfully classified 100% of these "hallucinations" as errors, validating the parsing and checking infrastructure.

### Figure Captions
*   **Figure 1** (`results/figures/token_usage.png`): Token Usage Comparison by Task and Format.
*   **Figure 2** (`results/figures/cost_comparison.png`): Estimated Cost Scale by Task and Format.
*   **Figure 3** (`results/figures/correctness_rate.png`): Correctness Rate (Validation of specific runs).
*   **Figure 4** (`results/figures/failure_breakdown.png`): Distribution of Failure Types (all classified as `parse_error` in pilot).

## 6. Limitations

The current findings are bounded by the following limitations:
*   **Mock Backend**: Actual model behavior (instruction following, reasoning) was not evaluated.
*   **Synthetic Data**: The complexity of real-world "dirty" data is not represented.
*   **Task Scope**: The three tasks represent only a subset of common LLM operations.

## 7. Reproducibility

To reproduce these results:
1.  **Generate Data**: `python scripts/generate_dataset.py`
2.  **Execute Run**: `python scripts/run_experiment.py --size 10 --iterations 1`
3.  **Verify**: Check `results/run_manifest.json` for parameters.

The entire pipeline is deterministic.

## 8. Discussion

While the mock backend precludes conclusions about model intelligence, the infrastructure proves that representation efficiency is a measurable, optimizable quantity. A 50% reduction in context / prompts is significant for agentic loops where history grows rapidly. Future work will involve connecting this pipeline to capable models (e.g., GPT-4, Claude 3) to measure the trade-off between this efficiency and semantic understanding.

## 9. Conclusion

Prompt engineering is often viewed as an art, but it can be maintained as a science. By benchmarking representations like TOON against standards like JSON, we can make informed engineering decisions that balance cost, speed, and reliability. This project provides the scaffolding to make those decisions.
