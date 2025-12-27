import sys
import os
import uuid
import json
import argparse
from typing import List

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.dataset.generator import DatasetGenerator
from src.encoding.toon_codec import encode_to_toon
from src.prompts import base, task_a, task_b, task_c
from src.runner.executor import ModelExecutor
from src.runner.logger import RunLogger

TASKS = [task_a, task_b, task_c]
FORMATS = ["JSON", "TOON"]

def run_orchestrator(
    model_name: str = "mock-model",
    iterations: int = 1,
    dataset_size: int = 10
):
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    print(f"Starting Benchmark Run: {run_id}")
    print(f"Model: {model_name}, Iterations: {iterations}, Dataset Size: {dataset_size}")
    
    # 1. Generate Dataset (One dataset for the entire run to be consistent?)
    # Usually we want fresh data or fixed data?
    # Spec says "Deterministic via fixed seed". Let's stick to a fixed seed for now or consistent dataset.
    # We will generate a fresh dataset here to simulate the flow.
    
    print("Generating dataset...")
    generator = DatasetGenerator(count=dataset_size, seed=42)
    records = generator.generate()
    
    # Pre-compute formats
    data_map = {
        "JSON": json.dumps(records, indent=2),
        "TOON": encode_to_toon(records)
    }
    
    # 2. Components
    executor = ModelExecutor()
    logger = RunLogger(run_id=run_id)
    
    # 3. Execution Loop
    total_steps = len(TASKS) * len(FORMATS) * iterations
    current_step = 0
    
    for i in range(iterations):
        print(f"Iteration {i+1}/{iterations}...")
        
        for task in TASKS:
            for fmt in FORMATS:
                current_step += 1
                print(f"[{current_step}/{total_steps}] Running {task.TASK_NAME} in {fmt}...")
                
                # Build Prompt
                prompt_text = task.get_prompt(fmt, data_map[fmt])
                
                # Execute
                result = executor.execute(
                    model_name=model_name,
                    system_prompt=base.SYSTEM_PROMPT,
                    user_prompt=prompt_text
                )
                
                # Log
                logger.log_task_execution(
                    task_name=task.TASK_NAME,
                    format_name=fmt,
                    model_name=model_name,
                    execution_result=result
                )
                
    print(f"Run {run_id} complete. Logs saved to runs/{run_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run TOON vs JSON Benchmark Orchestrator")
    parser.add_argument("--model", type=str, default="mock-model", help="Model name to run")
    parser.add_argument("--iterations", type=int, default=1, help="Number of iterations per task/format")
    parser.add_argument("--size", type=int, default=5, help="Dataset size for this run")
    
    args = parser.parse_args()
    
    run_orchestrator(
        model_name=args.model,
        iterations=args.iterations,
        dataset_size=args.size
    )
