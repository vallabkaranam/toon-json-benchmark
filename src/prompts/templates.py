from .base import assemble_prompt

def format_prompt(task_module, format_name: str, data: str) -> str:
    """
    Centralized formatting logic using the module's description.
    """
    return assemble_prompt(
        task_description=task_module.TASK_DESCRIPTION,
        format_name=format_name,
        data=data
    )
