import os
import requests
import time

endpoint = os.getenv("AUTTER_ENDPOINT", "https://otlp.autter.dev")
api_key = os.getenv("AUTTER_RUNTIME_KEY", "")
git_sha = os.getenv("GIT_SHA", "unknown-sha")

print(f"Sending test error to {endpoint} for commit {git_sha[:8]}...")

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
                "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
                "spanId": "00f067aa0ba902b7",
                "name": "GET /api/factorial",
                "kind": 1,
                "startTimeUnixNano": int(time.time() * 1e9),
                "endTimeUnixNano": int((time.time() + 0.1) * 1e9),
                "status": {"code": 2, "message": "Unhandled Exception"},
                "events": [{
                    "name": "exception",
                    "attributes": [
                        {"key": "exception.type", "value": {"stringValue": "ZeroDivisionError"}},
                        {"key": "exception.message", "value": {"stringValue": "division by zero in factorial calculation"}},
                        {"key": "exception.stacktrace", "value": {"stringValue": "File 'fact.py', line 7, in factorial\n  return n / 0"}}
                    ]
                }]
            }]
        }]
    }]
}

response = requests.post(
    f"{endpoint}/v1/traces",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json=payload
)

print(f"HTTP Status: {response.status_code}")
print(f"Server Response: {response.text}")