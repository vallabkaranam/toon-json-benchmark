# Portfolio Positioning & Hiring Assets

## 1. Project Overview (for GitHub README)

**TOON vs. JSON: Structured Prompt Representation Benchmark**

This project establishes a rigorous, reproducible framework for evaluating the systems-level impact of data representation choices in Large Language Model (LLM) pipelines. While prompt engineering is often treated qualitatively, this system applies standard ML infrastructure principles—determinism, modularity, and quantifiable metrics—to measure the trade-offs between standard formats (JSON) and optimized representations (TOON).

The benchmark allows engineers to isolate representation as a single variable, measuring its direct effect on token usage, latency proxies, and failure modes across synthetic tasks like filtering and aggregation. The infrastructure includes a deterministic dataset generator, a custom codec for the TOON format, a modular execution orchestrator, and a complete analysis pipeline that aggregates results into publication-ready figures. Pilot results demonstrate a ~51% reduction in input verbosity when switching from JSON to TOON, highlighting the tangible infrastructure value of prompt optimization.

## 2. Resume Bullet Points

*   **Designed and implemented a modular evaluation framework** to benchmark LLM inputs, isolating data representation as a control variable to measure impact on token efficiency and system cost.
*   **Engineered a custom serialization format (TOON)** and deterministic codec to optimize prompt density, achieving a ~51% reduction in token usage compared to standard JSON payloads.
*   **Built a robust orchestration pipeline** separating dataset generation, execution, and metric aggregation, ensuring full reproducibility of experimental results through immutable run manifests.
*   **Developed a strict schema-validation system** to quantify model failure modes, categorizing hallucinations and syntax errors to enable data-driven prompt engineering decisions.

## 3. Why This Matters (Systems Thinking Focus)

In production ML systems, "prompting" often drifts into unmanaged complexity. This project demonstrates the critical shift from intuitive prompt tweaking to rigorous **systems engineering**. by treating data representation not as a default (JSON) but as a design choice with measurable costs and benefits, we can optimize infrastructure constraints like context window usage and latency. The value lies not just in the specific format tested, but in the methodology: decoupling evaluations from model providers, enforcing determinism with fixed seeds, and creating a feedback loop where engineering decisions are based on empirical metrics rather than anecdote.

## 4. Elevator Pitch (for Interviews)

"I built a benchmarking framework to treat prompt engineering as a rigorous systems problem rather than just 'prompt whispering.' By creating a controlled pipeline to compare data formats like JSON against optimized alternatives, I gathered empirical data on token efficiency and failure modes, demonstrating how infrastructure-level choices can cut context usage by over 50% without changing the underlying model."
