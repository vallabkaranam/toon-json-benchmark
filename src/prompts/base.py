SYSTEM_PROMPT = """You are a deterministic data processing system.
Follow instructions exactly.
Do not add explanations.
Return only the requested output.
Use the same representation format as the input."""

def assemble_prompt(task_description: str, format_name: str, data: str) -> str:
    """
    Assembles the final user prompt based on the template in the spec.
    """
    # Template from spec:
    # You are given a dataset encoded in <FORMAT>.
    # 
    # <Task description>
    # 
    # Dataset:
    # <DATA>
    
    return f"""You are given a dataset encoded in {format_name}.

{task_description}

Dataset:
{data}"""
