# Failure Modes

## Oversized Payload

The gateway applies endpoint-specific payload limits.

For `/scan`:

- Limit: 100KB
- Status: 413 Payload Too Large
- Response:
  `{"detail":"Scan payload exceeds 100KB limit"}`

For `/extract-ocr`:

- Limit: 5MB
- Status: 413 Payload Too Large
- Response:
  `{"detail":"OCR upload exceeds 5MB limit"}`

## Rate Limiting

Gateway endpoints are rate limited.

- `/health`: 60 requests/minute
- `/scan`: 5 requests/minute
- `/extract-ocr`: 5 requests/minute

When exceeded:

- Status: 429 Too Many Requests
- Response:
  `{"detail":"Rate limit exceeded"}`

## Request Tracing

Each request is assigned a unique request ID.

Response header:

`X-Request-ID`

The request ID is logged for troubleshooting and traceability.

## Extractor Failure

If extractor is unavailable:

- Status: 502 Bad Gateway
- Analyzer is not executed.

## Analyzer Failure

If analyzer is unavailable:

- Status: 502 Bad Gateway

## Personalizer Failure

If personalizer is unavailable:

- Analyzer results are returned without personalization.

## Routine Builder Failure

If routine builder is unavailable:

- Status: 502 Bad Gateway

## Retries

Gateway retries downstream service calls up to 3 times using exponential backoff before failing.