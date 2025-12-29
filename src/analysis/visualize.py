
import os
import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from typing import List, Dict, Any

def read_csv(filepath: str) -> List[Dict[str, str]]:
    if not os.path.exists(filepath):
        print(f"Warning: File not found: {filepath}")
        return []
    with open(filepath, "r") as f:
        return list(csv.DictReader(f))

def get_tasks_and_formats(rows: List[Dict]) -> tuple[List[str], List[str]]:
    tasks = sorted(list(set(r["task"] for r in rows)))
    formats = sorted(list(set(r["format"] for r in rows)))
    return tasks, formats

def plot_grouped_bar(
    rows: List[Dict],
    value_key: str,
    ylabel: str,
    title: str,
    output_path: str,
    ylim: tuple = None
):
    """
    Generates a generic grouped bar chart from summary.csv rows.
    """
    if not rows:
        return

    tasks, formats = get_tasks_and_formats(rows)
    
    # Organize data: data[format][task_index] = value
    data = defaultdict(list)
    
    # Helper to find value
    def get_val(t, f):
        for r in rows:
            if r["task"] == t and r["format"] == f:
                return float(r[value_key])
        return 0.0

    for fmt in formats:
        for t in tasks:
            data[fmt].append(get_val(t, fmt))

    x = np.arange(len(tasks))
    width = 0.35
    multiplier = 0

    fig, ax = plt.subplots(figsize=(10, 6))

    for fmt, values in data.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, values, width, label=fmt)
        multiplier += 1

    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x + width / 2 * (len(formats) - 1))
    ax.set_xticklabels(tasks, rotation=15, ha="right")
    ax.legend()
    
    if ylim:
        ax.set_ylim(ylim)
    elif value_key == "correctness_rate":
         ax.set_ylim(0, 1.05) # Nice touch for handling small overshoots or just clarify 1.0

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved figure: {output_path}")

def plot_token_usage(summary_rows: List[Dict], output_dir: str):
    plot_grouped_bar(
        summary_rows,
        "mean_total_tokens",
        "Mean Total Tokens",
        "Token Usage by Task and Format",
        os.path.join(output_dir, "token_usage.png")
    )

def plot_cost_comparison(summary_rows: List[Dict], output_dir: str):
    plot_grouped_bar(
        summary_rows,
        "mean_estimated_cost",
        "Mean Estimated Cost ($)",
        "Cost Comparison by Task and Format",
        os.path.join(output_dir, "cost_comparison.png")
    )

def plot_correctness_rate(summary_rows: List[Dict], output_dir: str):
    plot_grouped_bar(
        summary_rows,
        "correctness_rate",
        "Correctness Rate (0-1)",
        "Correctness Rate by Task and Format",
        os.path.join(output_dir, "correctness_rate.png"),
        ylim=(0, 1.05)
    )

def plot_failure_breakdown(failure_rows: List[Dict], output_dir: str):
    """
    Subplots per task.
    """
    if not failure_rows:
        return

    tasks = sorted(list(set(r["task"] for r in failure_rows)))
    formats = sorted(list(set(r["format"] for r in failure_rows)))
    
    # Determine subplot layout
    n_tasks = len(tasks)
    cols = 1
    rows = n_tasks
    
    fig, axes = plt.subplots(rows, cols, figsize=(10, 5 * n_tasks))
    if n_tasks == 1:
        axes = [axes]
    
    for i, task in enumerate(tasks):
        ax = axes[i]
        
        # Filter rows for this task
        task_rows = [r for r in failure_rows if r["task"] == task]
        
        # Get all failure types for this task
        fail_types = sorted(list(set(r["failure_type"] for r in task_rows)))
        
        if not fail_types:
            ax.text(0.5, 0.5, "No Failures Recorded", ha='center', va='center')
            ax.set_title(f"Failure Breakdown: {task}")
            continue

        x = np.arange(len(fail_types))
        width = 0.35
        multiplier = 0
        
        # Helper
        def get_count(f, ft):
            for r in task_rows:
                if r["format"] == f and r["failure_type"] == ft:
                    return int(r["count"])
            return 0

        for fmt in formats:
            counts = [get_count(fmt, ft) for ft in fail_types]
            offset = width * multiplier
            ax.bar(x + offset, counts, width, label=fmt)
            multiplier += 1
            
        ax.set_ylabel("Count")
        ax.set_title(f"Failure Breakdown: {task}")
        ax.set_xticks(x + width / 2 * (len(formats) - 1))
        ax.set_xticklabels(fail_types, rotation=45, ha="right")
        ax.legend()
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, "failure_breakdown.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Saved figure: {output_path}")

def generate_all_figures(results_dir: str = "results") -> None:
    output_dir = os.path.join(results_dir, "figures")
    os.makedirs(output_dir, exist_ok=True)
    
    summary_path = os.path.join(results_dir, "summary.csv")
    failure_path = os.path.join(results_dir, "failure_breakdown.csv")
    
    summary_rows = read_csv(summary_path)
    failure_rows = read_csv(failure_path)
    
    if not summary_rows:
        print(f"No summary data found in {summary_path}")
    else:
        plot_token_usage(summary_rows, output_dir)
        plot_cost_comparison(summary_rows, output_dir)
        plot_correctness_rate(summary_rows, output_dir)
        
    if not failure_rows:
        print(f"No failure data found in {failure_path}")
    else:
        plot_failure_breakdown(failure_rows, output_dir)

if __name__ == "__main__":
    # Allow optional arg for directory
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "results"
    generate_all_figures(target_dir)
