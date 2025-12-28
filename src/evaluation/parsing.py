import json
from typing import Any, List, Dict
import sys
import os

# Add project root to path to import encoding module
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.encoding.toon_codec import decode_from_toon

class EvaluationError(Exception):
    """Base class for evaluation errors."""
    pass

class ParseError(EvaluationError):
    """Raised when the output cannot be parsed into the expected format."""
    pass

class SchemaViolation(EvaluationError):
    """Raised when the parsed output does not match the expected structural schema."""
    pass

def parse_output(format_name: str, raw_text: str) -> Any:
    """
    Parses raw text output based on the specified format.
    
    Args:
        format_name: "JSON" or "TOON" (case insensitive)
        raw_text: The raw output string from the model.
        
    Returns:
        The parsed Python object (usually a list of dicts).
        
    Raises:
        ParseError: If parsing fails.
        SchemaViolation: If the structure is fundamentally invalid (e.g., not a list).
    """
    fmt = format_name.upper()
    
    # Pre-cleaning: simple heuristic to find start of content if model adds chatter?
    # Spec says "Return only the requested output." and "Follow instructions exactly."
    # But models might add markdown code blocks.
    cleaned_text = raw_text.strip()
    if cleaned_text.startswith("```"):
        # Strip markdown code blocks
        lines = cleaned_text.split('\n')
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned_text = "\n".join(lines).strip()

    try:
        if fmt == "JSON":
            try:
                data = json.loads(cleaned_text)
            except json.JSONDecodeError as e:
                # Try to find JSON array if it's embedded
                try:
                    start = cleaned_text.find('[')
                    end = cleaned_text.rfind(']')
                    if start != -1 and end != -1:
                        data = json.loads(cleaned_text[start:end+1])
                    else:
                        raise e
                except Exception:
                    raise ParseError(f"JSON decode failed: {str(e)}")
        elif fmt == "TOON":
            try:
                data = decode_from_toon(cleaned_text)
            except Exception as e:
                raise ParseError(f"TOON decode failed: {str(e)}")
        else:
            raise ValueError(f"Unknown format: {format_name}")
            
    except ParseError:
        raise
    except Exception as e:
        raise ParseError(f"Unexpected parsing error: {str(e)}")

    # Basic Structural Sanity Check
    # We expect a list of dicts for all defined tasks, 
    # OR a specific structure if the task implies something else.
    # However, Phase 3 defines "expected_output_schema" which implies structured data.
    # For now, we enforce that the result is a LIST (since all 3 tasks return lists of records or aggregates).
    
    if not isinstance(data, list):
        raise SchemaViolation(f"Output is not a list. Got type: {type(data).__name__}")
        
    return data
