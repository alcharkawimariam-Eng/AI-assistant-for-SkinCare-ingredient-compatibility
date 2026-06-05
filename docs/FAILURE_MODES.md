## Rate limiting

The gateway applies IP-based rate limits.

- Default limit: `60 requests/minute` per IP
- `/scan` limit: `5 requests/minute` per IP
- Status code when exceeded: `429 Too Many Requests`
- Response: `{"detail": "Rate limit exceeded"}`

## Retry behavior

The gateway retries internal service calls up to 3 times using exponential backoff.

- Applies to: Extractor, Analyzer, Personalizer
- Per-attempt timeout: 10 seconds
- Backoff: exponential, capped at 2 seconds

## Extractor circuit breaker

If the extractor fails 5 times within 30 seconds, the gateway opens the extractor circuit for 60 seconds.

While the circuit is open:

- The extractor is not called.
- The gateway returns a fallback response with `fallback: "review_recommended"`.
- Products are marked with `review_recommended: true`.
- Unknown products are returned for manual review.
