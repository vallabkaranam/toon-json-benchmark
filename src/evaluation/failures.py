from typing import Any, Dict, Union

def classify_failure(result_or_exception: Union[Dict, Exception]) -> str:
    """
    Classifies a failure into one of the standard benchmarks categories.
    
    Hashable/Comparable string identifiers:
    - success (if no failure)
    - parse_error
    - schema_violation
    - incorrect_result
    - hallucination (special subset of incorrect result)
    - nondeterministic_output (handled at aggregation level, typically)
    """
    
    # 1. Handle Exceptions (Parsing phase)
    if isinstance(result_or_exception, Exception):
        # We assume specific exception names from parsing.py or generic ones
        name = type(result_or_exception).__name__
        if "ParseError" in name or "JSONDecodeError" in name:
            return "parse_error"
        if "SchemaViolation" in name:
            return "schema_violation"
        # Fallback for unexpected crashes
        return "parse_error" 

    # 2. Handle Result Dict (Correctness phase)
    if isinstance(result_or_exception, dict):
        if result_or_exception.get("is_correct", False):
            return "success"
            
        errors = result_or_exception.get("errors", [])
        error_text = " ".join(str(e) for e in errors).lower()
        
        # Heuristics based on error messages generated in correctness.py
        
        # Schema issues caught during correctness (e.g. missing keys inside valid list dicts)
        if "missing key" in error_text or "extra key" in error_text:
            return "schema_violation"
            
        # Hallucination
        if "hallucination" in error_text or "extra records" in error_text or "hallucinated type" in error_text:
            return "hallucination"
            
        # Default logic failure
        return "incorrect_result"

    return "unknown_error"
