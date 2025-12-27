#!/usr/bin/env python3
import sys
import os
import json
import argparse

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.dataset.generator import DatasetGenerator, get_schema

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic dataset for TOON vs JSON benchmark")
    parser.add_argument("--count", type=int, default=200, help="Number of records to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for determinism")
    parser.add_argument("--output-dir", type=str, default="data", help="Output directory")
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    print(f"Generating {args.count} records with seed {args.seed}...")
    generator = DatasetGenerator(seed=args.seed, count=args.count)
    records = generator.generate()
    
    events_path = os.path.join(args.output_dir, "events.json")
    with open(events_path, "w") as f:
        json.dump(records, f, indent=2)
    print(f"Wrote events to {events_path}")
    
    schema_path = os.path.join(args.output_dir, "schema.json")
    with open(schema_path, "w") as f:
        json.dump(get_schema(), f, indent=2)
    print(f"Wrote schema to {schema_path}")

if __name__ == "__main__":
    main()
