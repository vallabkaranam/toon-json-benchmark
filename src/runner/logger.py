import os
import json
import datetime
from typing import Dict, Any

class RunLogger:
    def __init__(self, run_id: str, base_dir: str = "runs"):
        self.run_id = run_id
        self.base_dir = base_dir
        self.run_dir = os.path.join(base_dir, run_id)
        os.makedirs(self.run_dir, exist_ok=True)
        
        # Create subdirectories for formats makes manual inspection easier
        os.makedirs(os.path.join(self.run_dir, "JSON"), exist_ok=True)
        os.makedirs(os.path.join(self.run_dir, "TOON"), exist_ok=True)

    def log_task_execution(
        self,
        task_name: str,
        format_name: str,
        model_name: str,
        execution_result: Dict[str, Any]
    ):
        """
        Logs a single task execution result to a structured file.
        """
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "run_id": self.run_id,
            "task_name": task_name,
            "format": format_name,
            "model": model_name,
            "usage": execution_result.get("usage", {}),
            "raw_output": execution_result.get("raw_output", "")
        }
        
        # Sanitize task name for filename
        sanitized_task = task_name.replace(" ", "_").replace("-", "_").lower()
        filename = f"{sanitized_task}.json"
        
        # Path: runs/<run_id>/<FORMAT>/<task_name>.json
        # If repeated runs happen in same session, we might want to append or sequence.
        # For now, we assume one execution per task per run_id, or append to a log list file.
        # Let's write individual event files with timestamps to allow multiple iterations clearly.
        
        filename = f"{sanitized_task}_{int(time.time()*1000)}.json"
        file_path = os.path.join(self.run_dir, format_name, filename)
        
        with open(file_path, "w") as f:
            json.dump(log_entry, f, indent=2)

import time
