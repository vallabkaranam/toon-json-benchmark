import csv
import os
from collections import defaultdict
from typing import List, Dict, Any

def write_summary(metrics: List[Dict[str, Any]], output_dir: str):
    """
    Writes summary statistics per (task, format) to CSV.
    """
    # 1. Group Data
    grouped = defaultdict(list)
    for m in metrics:
        key = (m["task"], m["format"])
        grouped[key].append(m)
        
    # 2. Compute Aggregates
    rows = []
    headers = [
        "task", "format", 
        "mean_input_tokens", "mean_output_tokens", "mean_total_tokens",
        "mean_estimated_cost", "correctness_rate", "error_rate"
    ]
    
    for (task, fmt), items in grouped.items():
        count = len(items)
        if count == 0:
            continue
            
        avg_in = sum(i["input_tokens"] for i in items) / count
        avg_out = sum(i["output_tokens"] for i in items) / count
        avg_total = sum(i["total_tokens"] for i in items) / count
        avg_cost = sum(i["estimated_cost"] for i in items) / count
        
        correct_count = sum(1 for i in items if i["is_correct"])
        correctness = correct_count / count
        
        rows.append({
            "task": task,
            "format": fmt,
            "mean_input_tokens": round(avg_in, 2),
            "mean_output_tokens": round(avg_out, 2),
            "mean_total_tokens": round(avg_total, 2),
            "mean_estimated_cost": round(avg_cost, 6),
            "correctness_rate": round(correctness, 4),
            "error_rate": round(1.0 - correctness, 4)
        })
        
    # Sort for deterministic output: Task then Format
    rows.sort(key=lambda x: (x["task"], x["format"]))

    # 3. Write CSV
    filepath = os.path.join(output_dir, "summary.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote summary to {filepath}")


def write_per_task_metrics(metrics: List[Dict[str, Any]], output_dir: str):
    """
    Writes raw metrics for every run execution to CSV.
    """
    headers = [
        "run_id", "task", "format",
        "input_tokens", "output_tokens", "total_tokens",
        "estimated_cost", "is_correct", "error_types"
    ]
    
    rows = []
    for m in metrics:
        # Flatten error types slightly for CSV readability
        errs = m.get("error_messages", [])
        # Truncate or join
        err_str = "; ".join(str(e) for e in errs[:5]).replace("\n", " ") 
        
        rows.append({
            "run_id": m.get("run_id"),
            "task": m.get("task"),
            "format": m.get("format"),
            "input_tokens": m.get("input_tokens"),
            "output_tokens": m.get("output_tokens"),
            "total_tokens": m.get("total_tokens"),
            "estimated_cost": m.get("estimated_cost"),
            "is_correct": m.get("is_correct"),
            "error_types": err_str
        })
        
    # Sort for deterministic output
    rows.sort(key=lambda x: (x.get("run_id", ""), x.get("task", ""), x.get("format", "")))

    filepath = os.path.join(output_dir, "per_task_metrics.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote per-task metrics to {filepath}")


def write_failure_breakdown(metrics: List[Dict[str, Any]], output_dir: str):
    """
    Writes counts of failure types per (task, format).
    """
    # Group by (task, format, failure_type) -> count
    counts = defaultdict(int)
    
    for m in metrics:
        key = (
            m["task"],
            m["format"],
            m.get("failure_category", "unknown")
        )
        counts[key] += 1
        
    rows = []
    for (task, fmt, fail_type), count in counts.items():
        rows.append({
            "task": task,
            "format": fmt,
            "failure_type": fail_type,
            "count": count
        })
        
    rows.sort(key=lambda x: (x["task"], x["format"], x["failure_type"]))
    
    headers = ["task", "format", "failure_type", "count"]
    filepath = os.path.join(output_dir, "failure_breakdown.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote failure breakdown to {filepath}")


def export_all(metrics: List[Dict[str, Any]], output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    write_summary(metrics, output_dir)
    write_per_task_metrics(metrics, output_dir)
    write_failure_breakdown(metrics, output_dir)
