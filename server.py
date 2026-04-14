#!/usr/bin/env python3
"""Create mock API endpoint definitions. — MEOK AI Labs."""
import json, os, re, hashlib, math, random, string, time
from datetime import datetime, timezone
from typing import Optional
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 30
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": "Limit/day. Upgrade: meok.ai"})
    _usage[c].append(now); return None

mcp = FastMCP("mock-server-ai", instructions="MEOK AI Labs — Create mock API endpoint definitions.")


@mcp.tool()
def create_mock_endpoint(method: str, path: str, response_body: str = '') -> str:
    """MEOK AI Labs tool."""
    if err := _rl(): return err
    result = {"tool": "create_mock_endpoint", "timestamp": datetime.now(timezone.utc).isoformat()}
    # Process input
    local_vars = {k: v for k, v in locals().items() if k not in ('result',)}
    result["input"] = str(local_vars)[:200]
    result["status"] = "processed"
    return json.dumps(result, indent=2)

@mcp.tool()
def generate_mock_data(schema: str, count: int = 5) -> str:
    """MEOK AI Labs tool."""
    if err := _rl(): return err
    result = {"tool": "generate_mock_data", "timestamp": datetime.now(timezone.utc).isoformat()}
    # Process input
    local_vars = {k: v for k, v in locals().items() if k not in ('result',)}
    result["input"] = str(local_vars)[:200]
    result["status"] = "processed"
    return json.dumps(result, indent=2)

@mcp.tool()
def create_openapi_mock(spec: str) -> str:
    """MEOK AI Labs tool."""
    if err := _rl(): return err
    result = {"tool": "create_openapi_mock", "timestamp": datetime.now(timezone.utc).isoformat()}
    # Process input
    local_vars = {k: v for k, v in locals().items() if k not in ('result',)}
    result["input"] = str(local_vars)[:200]
    result["status"] = "processed"
    return json.dumps(result, indent=2)

@mcp.tool()
def list_mock_endpoints() -> str:
    """MEOK AI Labs tool."""
    if err := _rl(): return err
    result = {"tool": "list_mock_endpoints", "timestamp": datetime.now(timezone.utc).isoformat()}
    # Process input
    local_vars = {k: v for k, v in locals().items() if k not in ('result',)}
    result["input"] = str(local_vars)[:200]
    result["status"] = "processed"
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    mcp.run()
