#!/usr/bin/env python3
import sys
import os
import json

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.prompts import base, task_a, task_b, task_c
from src.encoding.toon_codec import encode_to_toon
from src.dataset.generator import DatasetGenerator

def main():
    print("Generating sample data...")
    generator = DatasetGenerator(count=5)
    records = generator.generate()
    
    # Pre-calculate data formats
    json_data = json.dumps(records, indent=2)
    toon_data = encode_to_toon(records)
    
    tasks = [task_a, task_b, task_c]
    
    for task in tasks:
        print(f"\n{'='*60}")
        print(f"Task: {task.TASK_NAME}")
        print(f"Description:\n{task.TASK_DESCRIPTION}")
        print("-" * 60)
        
        # Show prompt for JSON
        print("Prompt (JSON Version):")
        print(task.get_prompt("JSON", json_data))
        
        print("-" * 20)
        
        # Show prompt for TOON
        print("Prompt (TOON Version):")
        print(task.get_prompt("TOON", toon_data))
        
    print("\nSystem Prompt (Constant):")
    print(base.SYSTEM_PROMPT)

if __name__ == "__main__":
    main()
