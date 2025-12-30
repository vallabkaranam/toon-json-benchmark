# TOON vs. JSON: Structured Prompt Representation Benchmark

This repository contains a modular framework for evaluating the systems-level impact of data representation in Large Language Model (LLM) pipelines. It measures the trade-offs between standard verbose formats (JSON) and optimized, line-oriented formats (TOON) across dimensions of token usage, cost, and functional correctness.

## Project Goal

To move prompt engineering from a qualitative art to a measurable engineering discipline. By isolating data representation as a single variable within a deterministic pipeline, this project quantifies the "physics" of input formatting—demonstrating significant efficiency gains (approx. 51% token reduction) available through infrastructure optimization.

## System Overview

The pipeline is designed as a modular sequence of independent components:

1.  **Dataset Generation**: Deterministic creation of synthetic event logs.
2.  **Encoding**: Transformation of data into competing representations (JSON, TOON).
3.  **Orchestration**: Execution of standardized tasks (Filter, Aggregate, Transform) via a model interface.
4.  **Evaluation**: Parsing of raw outputs and verification against ground truth.
5.  **Analysis**: Aggregation of metrics into static reports and visualizations.

## Key Documentation

*   **[Technical Report](REPORT.md)**: A formal, research-style analysis of the methodology and results.
*   **[Narrative Article](docs/ARTICLE.md)**: A first-person discussion of the motivation and implications.
*   **[Empirical Facts](docs/EMPIRICAL_FACTS.md)**: The raw, non-interpretive log of experimental results.
*   **[Portfolio Context](docs/PORTFOLIO.md)**: A summary of the engineering skills and systems thinking demonstrated by this project.

## Provenance

*   **Codebase**: 100% Python, modular design.
*   **Results**: All figures and findings are generated deterministically from the artifacts in `results/`.
*   **Status**: Pilot complete (Mock Backend).

## How to Run

1.  **Generate Dataset**
    ```bash
    python scripts/generate_dataset.py --count 200 --seed 42
    ```

2.  **Run Experiment**
    Executes the full pipeline, aggregates metrics, and freezes artifacts.
    ```bash
    python scripts/run_experiment.py --size 200 --iterations 1
    ```

3.  **Generate Visualizations**
    Produces plots in `results/figures/`.
    ```bash
    python -m src.analysis.visualize
    ```

## What This Demonstrates

*   **Systems Engineering**: Treating prompts as structured software artifacts rather than magic text.
*   **Reproducibility**: Designing pipelines where every result is traceable to a specific random seed and commit.
*   **Evaluation Rigor**: Implementing deterministic correctness checks and failure categorization.
*   **Infrastructure Design**: Building modular runners that decouple data generation, execution, and analysis.
