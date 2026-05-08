<div align="center">

# Mock Server Ai MCP

**MCP server for mock server ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-mock-server-ai-mcp)](https://pypi.org/project/meok-mock-server-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Mock Server Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `create_endpoint` | Create a mock API endpoint definition. Provide response_schema as JSON object ma |
| `list_endpoints` | List all registered mock API endpoints. |
| `generate_mock_data` | Generate mock data from a JSON schema. Schema maps field names to types: string, |
| `validate_schema` | Validate a data object against a schema definition. Reports missing fields, type |

## Installation

```bash
pip install meok-mock-server-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "mock-server-ai": {
      "command": "python",
      "args": ["-m", "meok_mock_server_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
