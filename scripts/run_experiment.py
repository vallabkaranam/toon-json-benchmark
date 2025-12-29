#!/usr/bin/env python3
import sys
import os
import json
import argparse
import time
import datetime
from typing import List

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.dataset.generator import DatasetGenerator
from src.runner.orchestrator import run_orchestrator, TASKS, FORMATS
from src.aggregation.aggregate import aggregate_run
from src.aggregation.export import export_all

def main():
    parser = argparse.ArgumentParser(description="Run full experiment pipeline")
    parser.add_argument("--size", type=int, required=True, help="Dataset size")
    parser.add_argument("--iterations", type=int, required=True, help="Number of iterations")
    parser.add_argument("--model", type=str, default="mock-model", help="Model to evaluate")
    
    args = parser.parse_args()
    
    # Setup paths
    runs_root = os.path.join("runs")
    results_dir = os.path.join("results")
    os.makedirs(runs_root, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    
    # 1. Identify pre-existing runs to detect the new one
    existing_runs = set(os.listdir(runs_root))
    
    # 2. Run Orchestrator
    # Note: Orchestrator currently hardcodes seed=42
    print(f"Running experiment with size={args.size}, iterations={args.iterations}...")
    start_time = datetime.datetime.now().isoformat()
    
    run_orchestrator(
        model_name=args.model,
        iterations=args.iterations,
        dataset_size=args.size
    )
    
    # 3. Detect new run
    current_runs = set(os.listdir(runs_root))
    new_runs = current_runs - existing_runs
    
    if not new_runs:
        print("Error: No new run directory detected.")
        sys.exit(1)
        
    # Assuming the most recent one if multiple (unlikely)
    # But strictly we expect exactly one new run
    run_id = list(new_runs)[0]
    run_path = os.path.join(runs_root, run_id)
    print(f"Detected new run: {run_id}")
    
    # 4. Re-generate dataset (Seed 42 is hardcoded in orchestrator, so we match it here)
    # We need the exact records for correctness checking
    print("Regenerating dataset for verification (Seed 42)...")
    generator = DatasetGenerator(seed=42, count=args.size)
    records = generator.generate()
    
    # 5. Aggregation
    print("Aggregating results...")
    metrics = aggregate_run(run_path, dataset_records=records)
    
    # 6. Export Artifacts
    print("Exporting artifacts...")
    export_all(metrics, results_dir)
    
    # 7. Write Manifest
    manifest = {
        "run_id": run_id,
        "timestamp": start_time,
        "dataset_size": args.size,
        "seed": 42,  # Hardcoded in orchestrator
        "number_of_iterations": args.iterations,
        "model": args.model,
        "formats_evaluated": FORMATS,
        "tasks_evaluated": [t.TASK_NAME for t in TASKS]
    }
    
    manifest_path = os.path.join(results_dir, "run_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"Experiment complete. Manifest written to {manifest_path}")

if __name__ == "__main__":
    main()
