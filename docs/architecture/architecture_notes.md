# Architecture Diagram Notes

## Main Flow

User / Browser
→ Frontend React App
→ HTTP POST /scan
→ Gateway API (:8000)

## Internal Services

### Extractor Service (:8001)
Receives product names and ingredient text from the Gateway.
Uses a 4-tier extraction pipeline:
1. Local CSV lookup
2. INCIDecoder scraper
3. OCR extraction
4. LLM fallback

### Risk Engine / Analyzer (:8002)
Checks ingredient interactions and product conflicts.
Outputs risk status such as safe, caution, or conflict.

### Personalizer Service (:8003)
Uses user profile information:
- skin type
- sensitivity
- age
- concerns

Adjusts the final recommendation based on the user profile.

## Observability

### Prometheus
Collects metrics from Gateway, Extractor, Analyzer, and Personalizer.

### Grafana
Displays real-time dashboards using Prometheus metrics.

### MLflow
Tracks experiments, model/rule versions, and evaluation runs.

## Files to Export

- docs/architecture/architecture.drawio
- docs/architecture/architecture.png