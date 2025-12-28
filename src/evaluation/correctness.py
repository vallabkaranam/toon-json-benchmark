from typing import Any, Dict, List, Union

def is_subset(record: Dict, criterion: Dict) -> bool:
    """Helper to check if record matches criteria."""
    for k, v in criterion.items():
        if record.get(k) != v:
            return False
    return True

def deep_compare(expected: Any, actual: Any, path: str = "") -> List[str]:
    """
    Compares two objects and returns a list of error strings.
    Simplified deep comparison for checking correctness.
    """
    errors = []
    if type(expected) != type(actual):
        return [f"{path}: Type mismatch. Expected {type(expected)}, got {type(actual)}"]
    
    if isinstance(expected, dict):
        for k in expected:
            if k not in actual:
                errors.append(f"{path}: Missing key '{k}'")
                continue
            errors.extend(deep_compare(expected[k], actual[k], f"{path}.{k}"))
        for k in actual:
            if k not in expected:
                errors.append(f"{path}: Extra key '{k}' in output")
    elif isinstance(expected, list):
        if len(expected) != len(actual):
            return [f"{path}: internal list length mismatch"]
        for i, (e, a) in enumerate(zip(expected, actual)):
            errors.extend(deep_compare(e, a, f"{path}[{i}]"))
    else:
        # Primitives
        # For floats, use tolerance? Spec says "strict numeric correctness" for avg severity?
        # Actually Task B spec says "average severity is numerically correct". 
        # Floating point arithmetic might vary slightly. Let's use small epsilon.
        if isinstance(expected, float):
            if abs(expected - actual) > 1e-6:
                errors.append(f"{path}: Value mismatch. Expected {expected}, got {actual}")
        elif expected != actual:
            errors.append(f"{path}: Value mismatch. Expected {expected}, got {actual}")
            
    return errors

def check_task_a(output: List[Dict], input_data: List[Dict]) -> Dict:
    """
    Task A: Filtering.
    Criteria: status=failed, severity>=3, env=prod
    """
    expected_ids = set()
    for r in input_data:
        if (r.get("status") == "failed" and 
            r.get("severity") >= 3 and 
            r.get("env") == "prod"):
            expected_ids.add(r.get("id"))
            
    # Check 1: Verify all output records match criteria AND are in expected set
    output_ids = set()
    errors = []
    
    for i, r in enumerate(output):
        rid = r.get("id")
        if not rid:
            errors.append(f"Row {i} missing 'id'")
            continue
            
        output_ids.add(rid)
        
        # Check integrity vs original input (Hallucination check)
        # We need to find the full original record to be sure, or just rely on ID?
        # Let's verify fields roughly or just trust ID if present? 
        # Stronger check: output record should be IDENTICAL to input record with that ID.
        original = next((x for x in input_data if x["id"] == rid), None)
        if not original:
            errors.append(f"Row {i} (id={rid}) not found in input (Hallucination)")
            continue
            
        # Check criteria explicitly on OUTPUT to fail 'logic' errors even if copied correctly?
        # Actually simplest is: Output Set == Expected Set.
        # But we also want to catch if they modified the record content.
        
        # Let's perform a deep comparison for the fields that exist in output vs original
        # Task A format usually implies full record return.
        diff_errs = deep_compare(original, r, f"Row {i}")
        if diff_errs:
            errors.extend(diff_errs)
            
    # Check 2: Set equality
    missing_ids = expected_ids - output_ids
    extra_ids = output_ids - expected_ids
    
    if missing_ids:
        errors.append(f"Missing {len(missing_ids)} expected records: {list(missing_ids)[:3]}...")
    if extra_ids:
        errors.append(f"Found {len(extra_ids)} extra records that shouldn't be valid: {list(extra_ids)[:3]}...")
        
    return {
        "is_correct": len(errors) == 0,
        "errors": errors,
        "details": {"expected_count": len(expected_ids), "output_count": len(output)}
    }

def check_task_b(output: List[Dict], input_data: List[Dict]) -> Dict:
    """
    Task B: Aggregation.
    Per 'type': total count, failed count, average severity.
    """
    # 1. Compute Expected
    stats = {}
    for r in input_data:
        t = r.get("type")
        if t not in stats:
            stats[t] = {"total": 0, "failed": 0, "severity_sum": 0}
        
        stats[t]["total"] += 1
        if r.get("status") == "failed":
            stats[t]["failed"] += 1
        stats[t]["severity_sum"] += r.get("severity", 0)
        
    expected_rows = []
    for t, data in stats.items():
        avg = data["severity_sum"] / data["total"] if data["total"] > 0 else 0
        expected_rows.append({
            "type": t,
            "total_count": data["total"],
            "failed_count": data["failed"],
            "average_severity": avg
        })
        
    # Sort for easier comparison? Key logic is by "type"
    expected_map = {r["type"]: r for r in expected_rows}
    
    # 2. Verify Output
    errors = []
    seen_types = set()
    
    for i, r in enumerate(output):
        t = r.get("type")
        if not t:
            errors.append(f"Row {i} missing 'type'")
            continue
        if t in seen_types:
            errors.append(f"Duplicate type '{t}' in output")
        seen_types.add(t)
        
        if t not in expected_map:
            errors.append(f"Hallucinated type '{t}' in output")
            continue
            
        exp = expected_map[t]
        
        if r.get("total_count") != exp["total_count"]:
            errors.append(f"Type '{t}': total_count mismatch. Exp {exp['total_count']}, Got {r.get('total_count')}")
        if r.get("failed_count") != exp["failed_count"]:
            errors.append(f"Type '{t}': failed_count mismatch. Exp {exp['failed_count']}, Got {r.get('failed_count')}")
        
        # Float comparison for avg severity
        got_sev = r.get("average_severity")
        if isinstance(got_sev, (int, float)):
             if abs(got_sev - exp["average_severity"]) > 1e-4:
                 errors.append(f"Type '{t}': average_severity mismatch. Exp {exp['average_severity']:.4f}, Got {got_sev}")
        else:
            errors.append(f"Type '{t}': average_severity invalid type. Got {type(got_sev)}")

    # Check for missing types
    missing_types = set(expected_map.keys()) - seen_types
    if missing_types:
        errors.append(f"Missing types in output: {missing_types}")

    return {
        "is_correct": len(errors) == 0,
        "errors": errors,
        "details": {"expected_groups": len(expected_map), "output_groups": len(output)}
    }

def check_task_c(output: List[Dict], input_data: List[Dict]) -> Dict:
    """
    Task C: Transformation.
    Flatten to specific fields.
    """
    REQUIRED_KEYS = ["id", "timestamp", "service", "env", "type", "status", "severity", "region", "latency_ms"]
    
    errors = []
    
    # Needs 1:1 mapping
    if len(output) != len(input_data):
        errors.append(f"Count mismatch. Input {len(input_data)}, Output {len(output)}")
        
    # Build map for fast lookup
    input_map = {r["id"]: r for r in input_data}
    
    for i, r in enumerate(output):
        rid = r.get("id")
        if not rid:
            errors.append(f"Row {i} missing 'id'")
            continue
            
        if rid not in input_map:
            errors.append(f"Row {i} (id={rid}) not found in input (Hallucination)")
            continue
            
        original = input_map[rid]
        
        # Verify fields and values
        for key in REQUIRED_KEYS:
            if key not in r:
                errors.append(f"Row {i} (id={rid}) missing key '{key}'")
                continue
                
            # Derived value lookup
            if key == "region":
                expected_val = original["metadata"].get("region")
            elif key == "latency_ms":
                expected_val = original["metadata"].get("latency_ms")
            else:
                expected_val = original.get(key)
                
            if r[key] != expected_val:
                errors.append(f"Row {i} (id={rid}) value mismatch for '{key}'. Exp '{expected_val}', Got '{r[key]}'")
                
    return {
        "is_correct": len(errors) == 0,
        "errors": errors[:50], # Cap errors to avoid huge logs
        "details": {"input_count": len(input_data), "output_count": len(output)}
    }
