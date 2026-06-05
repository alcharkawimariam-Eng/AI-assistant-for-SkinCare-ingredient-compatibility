# Failure Modes

## Oversized payload

If a client sends a request larger than 100KB, the gateway rejects it before processing.

- Status code: `413 Payload Too Large`
- Response: `{"detail": "Payload exceeds 100KB limit"}`
- Downstream services called: none

## Extractor unavailable

If the extractor service cannot be reached or times out:

- Status code: `502 Bad Gateway`
- Response contains an extractor failure message.
- Analyzer and Personalizer are not called.

## Analyzer unavailable

If the analyzer service cannot be reached or times out:

- Status code: `502 Bad Gateway`
- Response contains an analyzer failure message.
- Personalizer is not called.

## Personalizer unavailable

If the personalizer service cannot be reached or times out:

- Analyzer results are returned without personalization.
- No error is returned to the client.

## Internal service timeouts

The gateway uses a 10-second timeout for calls to:
- Extractor
- Analyzer
- Personalizer

Requests exceeding this limit are treated as service failures.

## Request tracing

Each incoming request is assigned a unique request ID.

- Added to response header: `X-Request-ID`
- Logged by the gateway for troubleshooting and traceability.