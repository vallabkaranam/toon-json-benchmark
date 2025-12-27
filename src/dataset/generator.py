import random
import uuid
import datetime
import json
from typing import List, Dict, Any
from enum import Enum

# Constants for distributions and specific values
SERVICES = ["auth-service", "payment-service", "data-pipeline", "web-server", "notification-service"]
REGIONS = ["us-east-1", "us-west-2", "eu-central-1", "ap-northeast-1"]
STATUS_WEIGHTS = {"success": 0.60, "failed": 0.25, "warning": 0.15}
ENV_WEIGHTS = {"prod": 0.70, "staging": 0.20, "dev": 0.10}
TYPES = ["auth", "payment", "system", "network", "job"]
SEVERITY_WEIGHTS = {1: 0.1, 2: 0.25, 3: 0.3, 4: 0.25, 5: 0.1} # Skewed towards 2-4
TAGS_POOL = ["auth", "payment", "infra", "edge", "batch", "critical"]

class DatasetGenerator:
    def __init__(self, seed: int = 42, count: int = 200):
        self.seed = seed
        self.count = count
        self.rng = random.Random(seed)

    def _generate_weighted_choice(self, choices: Dict[Any, float]) -> Any:
        # Use simple weighted random choice
        population = list(choices.keys())
        weights = list(choices.values())
        return self.rng.choices(population, weights=weights, k=1)[0]

    def _generate_timestamp(self) -> str:
        # Generate a timestamp within the last 7 days
        end_time = datetime.datetime.now(datetime.timezone.utc)
        start_time = end_time - datetime.timedelta(days=7)
        random_seconds = self.rng.randint(0, int((end_time - start_time).total_seconds()))
        timestamp = start_time + datetime.timedelta(seconds=random_seconds)
        return timestamp.isoformat()

    def generate_record(self) -> Dict[str, Any]:
        env = self._generate_weighted_choice(ENV_WEIGHTS)
        status = self._generate_weighted_choice(STATUS_WEIGHTS)
        severity = self._generate_weighted_choice(SEVERITY_WEIGHTS)
        
        # Metadata logic
        num_tags = self.rng.randint(0, 3)
        tags = sorted(self.rng.sample(TAGS_POOL, num_tags))
        
        record = {
            "id": str(uuid.UUID(int=self.rng.getrandbits(128), version=4)),
            "timestamp": self._generate_timestamp(),
            "service": self.rng.choice(SERVICES),
            "env": env,
            "type": self.rng.choice(TYPES),
            "status": status,
            "severity": severity,
            "source": f"{self.rng.choice(REGIONS)}/instance-{self.rng.randint(1000, 9999)}",
            "metadata": {
                "request_id": f"req-{self.rng.getrandbits(32):08x}",
                "user_id": f"usr-{self.rng.randint(1000, 9999)}",
                "region": self.rng.choice(REGIONS),
                "retry_count": self.rng.randint(0, 5) if status == "failed" else 0,
                "latency_ms": round(self.rng.uniform(10.0, 5000.0), 2),
                "tags": tags
            },
            "message": f"Operation {self.rng.choice(['completed', 'failed', 'retrying'])} for {env} environment."
        }
        return record

    def generate(self) -> List[Dict[str, Any]]:
        records = [self.generate_record() for _ in range(self.count)]
        # Sort by timestamp, then id
        records.sort(key=lambda x: (x["timestamp"], x["id"]))
        return records

def get_schema() -> Dict[str, Any]:
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "timestamp": {"type": "string", "format": "date-time"},
            "service": {"type": "string"},
            "env": {"type": "string", "enum": ["prod", "staging", "dev"]},
            "type": {"type": "string", "enum": ["auth", "payment", "system", "network", "job"]},
            "status": {"type": "string", "enum": ["success", "failed", "warning"]},
            "severity": {"type": "integer", "minimum": 1, "maximum": 5},
            "source": {"type": "string"},
            "metadata": {
                "type": "object",
                "properties": {
                    "request_id": {"type": "string"},
                    "user_id": {"type": "string"},
                    "region": {"type": "string"},
                    "retry_count": {"type": "integer"},
                    "latency_ms": {"type": "number"},
                    "tags": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["request_id", "user_id", "region", "retry_count", "latency_ms", "tags"]
            },
            "message": {"type": "string"}
        },
        "required": ["id", "timestamp", "service", "env", "type", "status", "severity", "source", "metadata", "message"]
    }
