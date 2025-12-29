# Evaluating Representation Choices in LLM Pipelines

## 1. Abstract

Large language model systems increasingly rely on structured inputs, yet the effects of representation choices are rarely measured explicitly. This project presents a small, reproducible evaluation framework for comparing different prompt representations under controlled conditions. Using a synthetic but realistic task suite, we measure token usage, cost proxies, and correctness outcomes across representations. Rather than claiming performance superiority, the goal is to demonstrate how representation decisions can be evaluated systematically. The work emphasizes reproducibility, separation of concerns, and infrastructure design over model-specific optimization.

## 2. Motivation

Most applied LLM systems depend on structured formats such as JSON, schemas, or tool-like encodings. These formats are often chosen for convenience or convention rather than empirical evaluation. While model behavior is widely studied, the *representation layer* is rarely treated as a first-class design choice.

As systems grow more complex—especially agentic and tool-using pipelines—representation choices influence cost, robustness, and failure modes. This project explores how such choices can be evaluated using a controlled, reproducible methodology.

## 3. System Overview

The system is organized as a modular evaluation pipeline:

1. Synthetic dataset generation
2. Representation encoding (JSON and TOON)
3. Prompt execution through a model interface
4. Logging of raw outputs
5. Parsing and correctness checking
6. Metric aggregation
7. Visualization and reporting

Each stage is isolated, deterministic, and independently testable. The design mirrors evaluation pipelines used in production ML systems.

## 4. Experimental Design

### Tasks

Three task types are evaluated:

* Filtering
* Aggregation
* Transformation

Each task operates over the same underlying dataset.

### Representations

Two representations are compared:

* JSON
* TOON (a compact, line-oriented structured format)

### Controls

* Identical datasets per run
* Fixed random seed
* Deterministic execution
* Identical task definitions
* Identical evaluation logic

This isolates representation as the primary variable.

## 5. Metrics

The evaluation tracks four categories of metrics:

### Token Usage

Total input and output tokens, used as a proxy for verbosity and cost.

### Cost Proxy

Estimated cost derived directly from token counts.

### Correctness

Binary correctness based on deterministic rule checks per task.

### Failure Types

Failures are classified into:

* parse errors
* schema violations
* hallucinations
* incorrect results

This enables qualitative analysis beyond success rates.

## 6. Results Overview

The evaluation produces:

* Token usage comparisons per task
* Cost proxy comparisons
* Correctness rates per representation
* Failure type distributions

These results are exported as CSV files and rendered as figures, enabling transparent inspection and reuse. As shown in the empirical summary (see `docs/EMPIRICAL_FACTS.md`), the data captures exact token counts and failure rates for each run.

Rather than claiming general performance improvements, the results highlight how different representations exhibit different trade-offs across efficiency and failure behavior, as detailed in the extracted results.

### Empirical Reference

* **Fact Sheet**: Numerical values for all runs are listed in `docs/EMPIRICAL_FACTS.md`.
* **Figures**: Visualizations (`results/figures/`) are rendered directly from the CSV outputs.
* **Source**: All facts are derived deterministically from experiment artifacts (`results/summary.csv`, `results/failure_breakdown.csv`).

### Figure Captions

* **Figure 1: Token Usage Comparison** (`results/figures/token_usage.png`): Displays the mean total token count per task, comparing JSON and TOON formats side-by-side.
* **Figure 2: Cost Proxy Comparison** (`results/figures/cost_comparison.png`): Shows the mean estimated cost per task execution for each representation format.
* **Figure 3: Correctness Rate** (`results/figures/correctness_rate.png`): Illustrates the proportion of correct runs (0.0 to 1.0) for each task and format.
* **Figure 4: Failure Breakdown** (`results/figures/failure_breakdown.png`): Depicts the count of specific failure categories encountered, organized by task and representation format.

## 7. Limitations

This study intentionally avoids overgeneralization.

Limitations include:

* Synthetic data rather than real production logs
* A small set of task archetypes
* A mock execution backend
* No semantic or human evaluation
* No statistical significance testing

The goal is methodological clarity, not benchmark supremacy.

## 8. Reproducibility

All experiments are fully reproducible:

1. Generate dataset
2. Run experiment script
3. Aggregate results
4. Generate figures

Each run produces a manifest capturing parameters and seeds. The pipeline can be re-executed end-to-end with identical outputs.

## 9. Future Work

Possible extensions include:

* Additional task families
* Richer schemas and nested structures
* Integration with real model APIs
* Statistical testing across runs
* Visualization dashboards
* Human evaluation
* Integration with agent frameworks

## 10. Conclusion

This project demonstrates how representation choices can be studied using the same rigor applied to models and algorithms. By treating prompts as structured artifacts and evaluating them systematically, we can better understand their trade-offs in real systems. The broader goal is to encourage more principled, reproducible evaluation practices in applied LLM engineering.
