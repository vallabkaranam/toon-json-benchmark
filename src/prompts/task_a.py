from .templates import format_prompt
import sys

TASK_NAME = "Task A - Filtering"

TASK_DESCRIPTION = """Return records where:
- status = failed
- severity >= 3
- env = prod"""

# Expected output is a subset of the original records, same schema.
expected_output_schema = "Same as input schema (Subset of records)"

def get_prompt(format: str, data: str) -> str:
    return format_prompt(
        task_module=sys.modules[__name__],
        format_name=format,
        data=data
    )
