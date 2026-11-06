import os
import requests
import time

endpoint = os.getenv("AUTTER_ENDPOINT", "https://otlp.autter.dev")
api_key = os.getenv("AUTTER_RUNTIME_KEY", "")
git_sha = os.getenv("GIT_SHA", "unknown-sha")

payload = {
    "resourceSpans": [{
        "resource": {
            "attributes": [
                {"key": "service.name", "value": {"stringValue": "backend-service"}},
                {"key": "service.version", "value": {"stringValue": git_sha}}
            ]
        },
        "scopeSpans": [{
            "spans": [{
                "traceId": "33333333333333333333333333333333",
                "spanId": "3333333333333333",
                "name": "POST /api/payout",
                "kind": 1,
                "startTimeUnixNano": int(time.time() * 1e9),
                "endTimeUnixNano": int((time.time() + 0.1) * 1e9),
                "status": {"code": 1, "message": "OK"},  # HTTP 200 (Span status OK)
                "attributes": [
                    {"key": "http.status_code", "value": {"intValue": 200}},
                    {"key": "business.outcome", "value": {"stringValue": "failed"}},
                    {"key": "autter.severity", "value": {"stringValue": "error"}}
                ],
                "events": [{
                    "name": "business_failure",
                    "attributes": [
                        {"key": "failure.reason", "value": {"stringValue": "Critical payout transaction rejected"}}
                    ]
                }]
            }]
        }]
    }]
}

res = requests.post(
    f"{endpoint}/v1/traces",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json=payload
)
print(f"Sent Silent Business Failure -> HTTP {res.status_code}")