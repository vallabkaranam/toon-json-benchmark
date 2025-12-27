# TOON vs JSON Benchmark Dataset Generation

## How to generate the dataset

This repository contains a deterministic dataset generator for the benchmark.

### Prerequisites

* Python 3.x

### Usage

Run the generation script from the root of the repository:

```bash
python scripts/generate_dataset.py
```

This will create:
* `data/events.json`: The generated events.
* `data/schema.json`: The standard JSON schema for the events.

### Options

* `--count`: Number of records to generate (default: 200)
* `--seed`: Random seed for determinism (default: 42)
* `--output-dir`: Directory to save files (default: data)
# toon-json-benchmark
