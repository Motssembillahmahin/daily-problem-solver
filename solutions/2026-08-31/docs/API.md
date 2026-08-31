# API Documentation

## Base URL

```
http://localhost:8000
```

## Endpoints

### POST /api/solve

Solve a problem using AI agent.

**Request Body:**

```json
{
    "problem": "string",
    "description": "string"
}
```

**Response:**

```json
{
    "problem": "string",
    "solution": "string",
    "code": "string"
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"problem": "How to organize files", "description": "Need automated file organizer"}'
```

### GET /api/health

Health check endpoint.

**Response:**

```json
{
    "status": "healthy"
}
```

## Error Handling

All errors return standard HTTP status codes:

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 500 | Server Error |

## Rate Limiting

No rate limiting - runs locally.

## Authentication

No authentication required - local development only.
