from .templates import format_prompt
import sys

TASK_NAME = "Task B - Aggregation"

TASK_DESCRIPTION = """For each type:
- total count
- failed count
- average severity"""

# Expected output schema (logical)
expected_output_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "total_count": {"type": "integer"},
            "failed_count": {"type": "integer"},
            "average_severity": {"type": "number"}
        }
    }
}

def get_prompt(format: str, data: str) -> str:
    return format_prompt(
        task_module=sys.modules[__name__],
        format_name=format,
        data=data
    )
