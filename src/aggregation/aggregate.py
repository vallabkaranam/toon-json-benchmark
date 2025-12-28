import os
import json
import glob
from typing import List, Dict, Optional

from src.dataset.generator import DatasetGenerator
from src.evaluation.parsing import parse_output, EvaluationError
from src.evaluation.correctness import check_task_a, check_task_b, check_task_c
from src.evaluation.failures import classify_failure
from src.aggregation.metrics import compute_metrics

# Map task names (from prompts) to correctness functions
TASK_CHECKS = {
    "Task A - Filtering": check_task_a,
    "Task B - Aggregation": check_task_b,
    "Task C - Transformation": check_task_c
}

def load_run_log(filepath: str) -> Dict:
    with open(filepath, "r") as f:
        return json.load(f)

def aggregate_run(run_dir: str, dataset_records: Optional[List[Dict]] = None) -> List[Dict]:
    """
    Aggregates results for a specific run directory.
    
    Args:
        run_dir: Path to the run directory (e.g. runs/run_xyz)
        dataset_records: The list of dict records used as input. 
                         If None, generates the default 200-record dataset.
    
    Returns:
        List of metric dictionaries.
    """
    
    # 1. Ensure Dataset
    if dataset_records is None:
        # Default fallback
        print("Warning: No dataset provided to aggregator. Generating default (Seed 42, Count 200).")
        gen = DatasetGenerator(seed=42, count=200)
        dataset_records = gen.generate()
        
    results = []
    
    # 2. Iterate Logs (JSON and TOON folders)
    # Pattern: runs/<run_id>/{JSON,TOON}/*.json
    # We use glob to specific path
    path_pattern = os.path.join(run_dir, "*", "*.json")
    files = glob.glob(path_pattern)
    
    for filepath in files:
        if not os.path.isfile(filepath):
            continue
            
        try:
            raw_log = load_run_log(filepath)
        except Exception as e:
            print(f"Skipping corrupt log {filepath}: {e}")
            continue
            
        task_name = raw_log.get("task_name")
        fmt = raw_log.get("format")
        raw_output = raw_log.get("raw_output", "")
        
        # Determine strictness checker
        checker_func = TASK_CHECKS.get(task_name)
        if not checker_func:
            # Maybe mismatch in naming? simple heuristic check?
            # Let's match by substring if exact fail
            found = False
            for k, v in TASK_CHECKS.items():
                if k in task_name:
                    checker_func = v
                    found = True
                    break
            if not found:
                print(f"Warning: No checker found for task '{task_name}' in {filepath}")
                continue

        # 3. Parse & Evaluate
        parsed_data = None
        correctness_res = {
            "is_correct": False,
            "errors": [], 
            "details": {}
        }
        
        try:
            parsed_data = parse_output(fmt, raw_output)
            # Evaluate correctness
            correctness_res = checker_func(parsed_data, dataset_records)
            
        except EvaluationError as e:
            # Handle Parse/Schema errors
            fail_type = classify_failure(e)
            correctness_res["is_correct"] = False
            correctness_res["errors"] = [f"{fail_type}: {str(e)}"]
            
        except Exception as e:
            # unexpected
            fail_type = classify_failure(e)
            correctness_res["is_correct"] = False
            correctness_res["errors"] = [f"System Error: {str(e)}"]

        # 4. Compute Metrics
        metric_entry = compute_metrics(
            task_name=task_name,
            format_name=fmt,
            raw_log=raw_log,
            parsed_output=parsed_data,
            correctness_result=correctness_res
        )
        
        # Add classification label for easier pivoting later
        final_errors = metric_entry.get("error_messages", [])
        if metric_entry["is_correct"]:
            metric_entry["failure_category"] = "success"
        elif any("ParseError" in e for e in final_errors) or any("parse_error" in e for e in final_errors):
             metric_entry["failure_category"] = "parse_error"
        elif any("SchemaViolation" in e for e in final_errors) or any("schema_violation" in e for e in final_errors):
             metric_entry["failure_category"] = "schema_violation"
        # We also reused failures.classify_failure logic on result dict?
        else:
             metric_entry["failure_category"] = classify_failure(correctness_res) # Logic reuse
             
        results.append(metric_entry)
        
    return results
