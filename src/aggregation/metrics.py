from typing import Dict, List, Any

# Hypothetical Cost Constants (e.g. GPT-4o-mini rates)
COST_PER_1M_INPUT_TOKENS = 0.15
COST_PER_1M_OUTPUT_TOKENS = 0.60

def compute_metrics(
    *,
    task_name: str,
    format_name: str,
    raw_log: Dict[str, Any],
    parsed_output: Any,
    correctness_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Computes efficiency and correctness metrics for a single run result.
    """
    
    # 1. Efficiency Metrics
    usage = raw_log.get("usage", {})
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)
    
    # Cost calculation ($)
    input_cost = (input_tokens / 1_000_000) * COST_PER_1M_INPUT_TOKENS
    output_cost = (output_tokens / 1_000_000) * COST_PER_1M_OUTPUT_TOKENS
    estimated_cost = input_cost + output_cost
    
    # 2. Correctness Metrics
    is_correct = correctness_result.get("is_correct", False)
    errors = correctness_result.get("errors", [])
    
    # 3. Result Construction
    return {
        "run_id": raw_log.get("run_id"),
        "task": task_name,
        "format": format_name,
        "model": raw_log.get("model"),
        "timestamp": raw_log.get("timestamp"),
        
        # Efficiency
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "estimated_cost": round(estimated_cost, 8),
        
        # Correctness
        "is_correct": is_correct,
        "error_count": len(errors),
        "error_messages": errors,  # Storing full list can be heavy, but useful for debug
        
        # Placeholder for stability (evaluated across runs)
        "determinism_score": None 
    }
