import csv
import os
from collections import defaultdict
from typing import List, Dict, Any, Tuple

def load_results(results_dir: str) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Loads summarized CSV artifacts.
    Returns (summary_rows, per_task_rows, failure_rows)
    """
    def read_csv(filename):
        path = os.path.join(results_dir, filename)
        if not os.path.exists(path):
            return []
        with open(path, "r") as f:
            return list(csv.DictReader(f))

    summary = read_csv("summary.csv")
    per_task = read_csv("per_task_metrics.csv")
    failures = read_csv("failure_breakdown.csv")
    
    return summary, per_task, failures

def compare_formats(summary_rows: List[Dict]) -> Dict[str, Dict]:
    """
    Groups summary rows by task vs format and computes diffs.
    Assumes standard format keys 'JSON' and 'TOON' (case insensitive match).
    """
    grouped = defaultdict(dict)
    
    # 1. Pivot data into structure
    for row in summary_rows:
        task = row["task"]
        fmt = row["format"].upper()
        
        # Parse numeric values from CSV strings
        data = {
            "mean_total_tokens": float(row["mean_total_tokens"]),
            "mean_estimated_cost": float(row["mean_estimated_cost"]),
            "correctness_rate": float(row["correctness_rate"]),
            "error_rate": float(row["error_rate"])
        }
        grouped[task][fmt] = data

    # 2. Compute Deltas
    comparisons = {}
    for task, formats in grouped.items():
        if "JSON" not in formats or "TOON" not in formats:
            continue
            
        json_data = formats["JSON"]
        toon_data = formats["TOON"]
        
        # Savings: Positive means TOON is cheaper/smaller
        token_savings = json_data["mean_total_tokens"] - toon_data["mean_total_tokens"]
        cost_savings = json_data["mean_estimated_cost"] - toon_data["mean_estimated_cost"]
        
        # Correctness Delta: Positive means TOON is better
        correctness_delta = toon_data["correctness_rate"] - json_data["correctness_rate"]
        
        comparisons[task] = {
            "json": json_data,
            "toon": toon_data,
            "delta": {
                "token_savings": token_savings,
                "cost_savings": cost_savings,
                "correctness_delta": correctness_delta
            }
        }
        
    return comparisons

def summarize_failures(failure_rows: List[Dict]) -> Dict[str, Dict[str, Dict[str, int]]]:
    """
    Structure: task -> format -> failure_type -> count
    """
    tree = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    for row in failure_rows:
        task = row["task"]
        fmt = row["format"]
        ftype = row["failure_type"]
        count = int(row["count"])
        
        tree[task][fmt][ftype] = count
        
    # Convert back to standard dict for clean return
    return {k: {fk: dict(fv) for fk, fv in v.items()} for k, v in tree.items()}

def human_readable_summary(comparison_dict: Dict[str, Dict]) -> List[str]:
    """
    Generates non-judgmental, factual summary strings.
    """
    summaries = []
    
    # Sort for deterministic output
    for task in sorted(comparison_dict.keys()):
        data = comparison_dict[task]
        d = data["delta"]
        
        # Token usage
        if d["token_savings"] > 0:
            summaries.append(f"{task}: TOON used {d['token_savings']:.2f} fewer tokens than JSON")
        elif d["token_savings"] < 0:
            summaries.append(f"{task}: TOON used {-d['token_savings']:.2f} more tokens than JSON")
        else:
            summaries.append(f"{task}: Token usage identical")
            
        # Correctness
        # Use epsilon for float comparison to avoid noise
        if d["correctness_delta"] > 0.001:
            summaries.append(f"{task}: TOON had higher correctness (+{d['correctness_delta']:.2%})")
        elif d["correctness_delta"] < -0.001:
            summaries.append(f"{task}: JSON had higher correctness (+{-d['correctness_delta']:.2%})")
        else:
            summaries.append(f"{task}: Correctness identical across formats")
            
    return summaries
