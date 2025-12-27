from .templates import format_prompt
import sys

TASK_NAME = "Task C - Transformation"

TASK_DESCRIPTION = """Flatten to:
- id
- timestamp
- service
- env
- type
- status
- severity
- region
- latency_ms"""

# Expected output schema (logical)
expected_output_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "timestamp": {"type": "string"},
            "service": {"type": "string"},
            "env": {"type": "string"},
            "type": {"type": "string"},
            "status": {"type": "string"},
            "severity": {"type": "integer"},
            "region": {"type": "string"},
            "latency_ms": {"type": "number"}
        }
    }
}

def get_prompt(format: str, data: str) -> str:
    return format_prompt(
        task_module=sys.modules[__name__],
        format_name=format,
        data=data
    )
