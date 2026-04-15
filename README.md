# Mock Server AI

> By [MEOK AI Labs](https://meok.ai) — Create mock API endpoint definitions

## Installation

```bash
pip install mock-server-ai-mcp
```

## Usage

```bash
python server.py
```

## Tools

### `create_mock_endpoint`
Create a mock API endpoint with method, path, and response body.

**Parameters:**
- `method` (str): HTTP method (GET, POST, etc.)
- `path` (str): API path
- `response_body` (str): Response body content

### `generate_mock_data`
Generate mock data based on a schema definition.

**Parameters:**
- `schema` (str): Data schema description
- `count` (int): Number of records to generate (default: 5)

### `create_openapi_mock`
Create mock endpoints from an OpenAPI specification.

**Parameters:**
- `spec` (str): OpenAPI spec content

### `list_mock_endpoints`
List all currently defined mock endpoints.

## Authentication

Free tier: 30 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
