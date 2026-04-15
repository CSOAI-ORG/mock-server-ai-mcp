#!/usr/bin/env python3
"""Create mock API endpoint definitions with generated test data. — MEOK AI Labs."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json, random, string, hashlib
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 30
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now - t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT:
        return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day. Upgrade: meok.ai"})
    _usage[c].append(now)
    return None

mcp = FastMCP("mock-server-ai", instructions="Create mock API endpoint definitions with generated test data. By MEOK AI Labs.")

_endpoints = {}

FIRST_NAMES = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Iris", "Jack"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson", "Taylor"]
DOMAINS = ["example.com", "test.org", "demo.io", "mock.dev", "sample.net"]
CITIES = ["New York", "London", "Tokyo", "Berlin", "Sydney", "Toronto", "Paris", "Seoul", "Mumbai", "Dubai"]
LOREM = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "sed", "tempor"]


def _gen_value(field_type: str, field_name: str = "") -> object:
    """Generate a realistic mock value based on type."""
    field_type = field_type.lower().strip()
    field_name = field_name.lower()

    if field_type in ("string", "str", "text"):
        if "name" in field_name and "last" in field_name:
            return random.choice(LAST_NAMES)
        if "name" in field_name and "first" in field_name:
            return random.choice(FIRST_NAMES)
        if "name" in field_name:
            return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        if "email" in field_name:
            return f"{random.choice(FIRST_NAMES).lower()}.{random.choice(LAST_NAMES).lower()}@{random.choice(DOMAINS)}"
        if "city" in field_name:
            return random.choice(CITIES)
        if "url" in field_name or "link" in field_name:
            return f"https://{random.choice(DOMAINS)}/{random.choice(LOREM)}"
        if "phone" in field_name:
            return f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
        if "description" in field_name or "bio" in field_name:
            return " ".join(random.choice(LOREM) for _ in range(random.randint(5, 15))).capitalize() + "."
        if "title" in field_name:
            return " ".join(random.choice(LOREM) for _ in range(random.randint(2, 5))).title()
        return "".join(random.choices(string.ascii_lowercase, k=random.randint(5, 12)))
    elif field_type in ("int", "integer", "number"):
        if "age" in field_name:
            return random.randint(18, 85)
        if "year" in field_name:
            return random.randint(2000, 2026)
        if "price" in field_name or "amount" in field_name:
            return round(random.uniform(1.0, 999.99), 2)
        if "count" in field_name or "quantity" in field_name:
            return random.randint(1, 100)
        return random.randint(1, 10000)
    elif field_type in ("float", "decimal", "double"):
        return round(random.uniform(0.01, 999.99), 2)
    elif field_type in ("bool", "boolean"):
        return random.choice([True, False])
    elif field_type in ("date", "datetime"):
        base = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 365))
        return base.isoformat()
    elif field_type in ("uuid", "id"):
        return hashlib.md5(str(random.random()).encode()).hexdigest()
    elif field_type in ("array", "list"):
        return [random.choice(LOREM) for _ in range(random.randint(2, 5))]
    elif field_type in ("email",):
        return f"{random.choice(FIRST_NAMES).lower()}@{random.choice(DOMAINS)}"
    else:
        return f"mock_{field_type}"


@mcp.tool()
def create_endpoint(method: str, path: str, status_code: int = 200, response_schema: str = "", description: str = "", api_key: str = "") -> str:
    """Create a mock API endpoint definition. Provide response_schema as JSON object mapping field names to types (e.g. {\"name\": \"string\", \"age\": \"int\"})."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl():
        return err

    method = method.upper().strip()
    if method not in ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"):
        return json.dumps({"error": f"Invalid HTTP method: {method}"})

    path = path.strip()
    if not path.startswith("/"):
        path = "/" + path

    schema = {}
    if response_schema:
        try:
            schema = json.loads(response_schema)
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid response_schema JSON"})

    sample_response = {}
    if schema:
        for field, ftype in schema.items():
            sample_response[field] = _gen_value(str(ftype), field)
    else:
        if method == "DELETE":
            sample_response = {"deleted": True, "message": "Resource deleted successfully"}
        else:
            sample_response = {"id": hashlib.md5(path.encode()).hexdigest()[:8], "status": "ok", "message": f"Mock response for {method} {path}"}

    endpoint_key = f"{method}:{path}"
    _endpoints[endpoint_key] = {
        "method": method,
        "path": path,
        "status_code": status_code,
        "description": description or f"Mock {method} {path}",
        "schema": schema,
        "sample_response": sample_response,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    return json.dumps({
        "status": "created",
        "endpoint": endpoint_key,
        "method": method,
        "path": path,
        "status_code": status_code,
        "sample_response": sample_response,
        "total_endpoints": len(_endpoints),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@mcp.tool()
def list_endpoints(api_key: str = "") -> str:
    """List all registered mock API endpoints."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl():
        return err

    endpoints = []
    for key, ep in _endpoints.items():
        endpoints.append({
            "method": ep["method"],
            "path": ep["path"],
            "status_code": ep["status_code"],
            "description": ep["description"],
            "has_schema": bool(ep["schema"]),
            "field_count": len(ep["schema"]) if ep["schema"] else 0,
            "created_at": ep["created_at"],
        })

    return json.dumps({
        "total_endpoints": len(endpoints),
        "endpoints": endpoints,
        "methods": list(set(ep["method"] for ep in endpoints)),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@mcp.tool()
def generate_mock_data(schema: str, count: int = 5, api_key: str = "") -> str:
    """Generate mock data from a JSON schema. Schema maps field names to types: string, int, float, bool, date, uuid, email, array."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl():
        return err

    try:
        field_map = json.loads(schema)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid schema JSON. Provide {\"field_name\": \"type\"} mapping."})

    if not isinstance(field_map, dict):
        return json.dumps({"error": "Schema must be a JSON object mapping field names to types."})

    count = max(1, min(count, 100))
    records = []
    for i in range(count):
        record = {"_id": i + 1}
        for field, ftype in field_map.items():
            record[field] = _gen_value(str(ftype), field)
        records.append(record)

    return json.dumps({
        "schema": field_map,
        "count": count,
        "records": records,
        "fields": list(field_map.keys()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@mcp.tool()
def validate_schema(schema_json: str, data_json: str, api_key: str = "") -> str:
    """Validate a data object against a schema definition. Reports missing fields, type mismatches, and extra fields."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl():
        return err

    try:
        schema = json.loads(schema_json)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid schema JSON"})
    try:
        data = json.loads(data_json)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid data JSON"})

    if not isinstance(schema, dict) or not isinstance(data, dict):
        return json.dumps({"error": "Both schema and data must be JSON objects"})

    type_map = {
        "string": str, "str": str, "text": str,
        "int": (int, float), "integer": (int, float), "number": (int, float),
        "float": (int, float), "decimal": (int, float), "double": (int, float),
        "bool": bool, "boolean": bool,
        "array": list, "list": list,
    }

    errors = []
    warnings = []

    for field, expected_type in schema.items():
        if field not in data:
            errors.append({"field": field, "error": "missing", "expected_type": str(expected_type)})
            continue

        value = data[field]
        expected_type_str = str(expected_type).lower()
        python_type = type_map.get(expected_type_str)

        if python_type and not isinstance(value, python_type):
            errors.append({
                "field": field,
                "error": "type_mismatch",
                "expected": expected_type_str,
                "actual": type(value).__name__,
                "value": str(value)[:50],
            })

    extra_fields = set(data.keys()) - set(schema.keys())
    if extra_fields:
        for field in extra_fields:
            warnings.append({"field": field, "warning": "extra_field_not_in_schema"})

    return json.dumps({
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "schema_fields": len(schema),
        "data_fields": len(data),
        "coverage": round(len(set(data.keys()) & set(schema.keys())) / len(schema) * 100, 1) if schema else 0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


if __name__ == "__main__":
    mcp.run()
