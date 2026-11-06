import os
import requests
import time
import subprocess

endpoint = "https://otlp.autter.dev"
api_key = "autter_rt_6e5e06b0b211fe45a88bd15ffe1624f1b86e5af4d489e683"
git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

print("[Test 3] Sending handled business failure (HTTP 200 without throwing an exception)...")

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
                "traceId": "40000000000000000000000000000004",
                "spanId": "4000000000000004",
                "name": "POST /api/payout",
                "kind": 1,
                "startTimeUnixNano": int(time.time() * 1e9),
                "endTimeUnixNano": int((time.time() + 0.1) * 1e9),
                "status": {"code": 1, "message": "OK"},  # Standard OTel OK status
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
print(f"Sent Business Failure -> HTTP {res.status_code}")