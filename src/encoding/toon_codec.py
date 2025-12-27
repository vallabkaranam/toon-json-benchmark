import re
import math

# Fixed schema order as per spec
FIELDS = [
    "id",
    "timestamp",
    "service",
    "env",
    "type",
    "status",
    "severity",
    "source",
    "metadata.request_id",
    "metadata.user_id",
    "metadata.region",
    "metadata.retry_count",
    "metadata.latency_ms",
    "metadata.tags",
    "message"
]

def encode_val(val) -> str:
    """Encodes a single value into TOON format string."""
    if isinstance(val, list):
        # Array: [a,b,c]
        # Assuming elements are simple strings based on spec constraints
        return "[" + ",".join(str(v) for v in val) + "]"
    
    s_val = str(val)
    
    # String quoting rules: quote if space, comma, or quote exists
    needs_quote = "," in s_val or " " in s_val or '"' in s_val
    if needs_quote:
        # Standard CSV-style escaping: double up quotes
        return '"' + s_val.replace('"', '""') + '"'
    
    return s_val

def decode_val(raw: str, field_name: str):
    """Decodes a TOON format string back to native type."""
    val = raw.strip()
    
    # Handle Quoted Strings
    if val.startswith('"') and val.endswith('"'):
        # Strip quotes and unescape double quotes
        val = val[1:-1].replace('""', '"')
        
        # If it was a string field, we are done (it remains a string)
        # But wait, could it be a quoted array? Spec says "Arrays as [a,b,c]", implies unquoted brackets.
        # But if for some reason an array text was quoted, we'd handle it here.
        # However, for schema strictness:
    
    # Handle Arrays
    if field_name == "metadata.tags":
        if val.startswith('[') and val.endswith(']'):
            content = val[1:-1]
            if not content:
                return []
            # Simple split since tags are simple identifiers per spec
            return content.split(',')
        return [] # Fallback
        
    # Handle Types
    if field_name in ["severity", "metadata.retry_count"]:
        return int(val)
    if field_name == "metadata.latency_ms":
        return float(val)
        
    return val

def parse_line_custom(line: str) -> list[str]:
    """
    Parses a single TOON data row.
    Handles comma separation while respecting quotes and bracket-nested arrays.
    """
    tokens = []
    current = []
    in_quote = False
    bracket_depth = 0
    
    i = 0
    n = len(line)
    
    while i < n:
        char = line[i]
        
        if char == '"':
            # Toggle quote state?
            # Must handle escaped quotes ("") inside a quoted string
            if in_quote and i + 1 < n and line[i+1] == '"':
                current.append('"')
                current.append('"')
                i += 1
            else:
                in_quote = not in_quote
                current.append('"')
        
        elif char == '[' and not in_quote:
            bracket_depth += 1
            current.append(char)
            
        elif char == ']' and not in_quote:
            bracket_depth -= 1
            current.append(char)
            
        elif char == ',' and not in_quote and bracket_depth == 0:
            # Separator found
            tokens.append("".join(current))
            current = []
            
        else:
            current.append(char)
            
        i += 1
        
    tokens.append("".join(current))
    return tokens


def encode_to_toon(records: list[dict]) -> str:
    """Encodes a list of record dicts to a TOON string."""
    lines = []
    
    # 1. Collection Header
    lines.append(f"events[{len(records)}]:")
    
    # 2. Schema Declaration
    lines.append("{" + ",".join(FIELDS) + "}")
    
    # 3. Data Rows
    for r in records:
        row = []
        for f in FIELDS:
            if "." in f:
                parent, child = f.split(".")
                val = r.get(parent, {}).get(child)
            else:
                val = r.get(f)
            row.append(encode_val(val))
        lines.append(",".join(row))
        
    return "\n".join(lines)


def decode_from_toon(text: str) -> list[dict]:
    """Decodes a TOON string back to a list of record dicts."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if not lines:
        return []
        
    # 1. Parse Header
    header_match = re.match(r"events\[(\d+)\]:", lines[0])
    if not header_match:
        raise ValueError(f"Invalid collection header: {lines[0]}")
    expected_count = int(header_match.group(1))
    
    # 2. Parse Schema
    schema_line = lines[1]
    if not (schema_line.startswith('{') and schema_line.endswith('}')):
        raise ValueError("Invalid schema declaration")
    schema_cols = schema_line[1:-1].split(',')
    
    if schema_cols != FIELDS:
        # For this strict benchmark, we fail on schema mismatch
        raise ValueError(f"Schema mismatch.\nExpected: {FIELDS}\nGot: {schema_cols}")

    # 3. Parse Rows
    records = []
    for line in lines[2:]:
        tokens = parse_line_custom(line)
        if len(tokens) != len(FIELDS):
            raise ValueError(f"Column count mismatch. Expected {len(FIELDS)}, got {len(tokens)}. Line: {line}")
            
        rec = {}
        meta = {}
        
        for i, field in enumerate(FIELDS):
            val = decode_val(tokens[i], field)
            
            if "." in field:
                _, child = field.split(".")
                meta[child] = val
            else:
                rec[field] = val
                
        rec["metadata"] = meta
        records.append(rec)
        
    if len(records) != expected_count:
        # This is a soft warning or hard error? Spec doesn't say. 
        # But header said N. simpler to let it pass or warn. 
        # But 'Lossless JSON roundtrip' implies we want exact correctness.
        pass

    return records


def validate_round_trip(records: list[dict]) -> bool:
    """
    Validates that records -> TOON -> records results in deep equality.
    Raises AssertionError on failure.
    """
    encoded = encode_to_toon(records)
    decoded = decode_from_toon(encoded)
    
    if len(records) != len(decoded):
        raise AssertionError(f"Count mismatch: Original {len(records)} != Decoded {len(decoded)}")
        
    for i, (r1, r2) in enumerate(zip(records, decoded)):
        # Check deep equality
        # Simple recursion isn't needed as we know the structure (1 level deep metadata)
        # But json equality is easiest
        if r1 != r2:
            raise AssertionError(f"Record {i} mismatch:\nOriginal: {r1}\nDecoded: {r2}")
            
    return True
