from prometheus_client import Counter

ANALYZE_REQUESTS = Counter(
    "analyzer_requests_total",
    "Total number of analyzer requests"
)

ANALYZE_HIGH_RISK = Counter(
    "analyzer_high_risk_total",
    "Total number of analyzer responses marked high risk"
)