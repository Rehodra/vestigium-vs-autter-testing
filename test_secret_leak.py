import os
import requests
import time
import subprocess

endpoint = "https://otlp.autter.dev"
api_key = "autter_rt_6e5e06b0b211fe45a88bd15ffe1624f1b86e5af4d489e683"  # <-- Paste your key
git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

print("[Adv Test 1] Sending error with fake DB password and API key...")

# A realistic crash where a database URL and API key are leaked in the error
secret_message = "ConnectionRefused: Failed connecting to postgresql://postgres:SuperSecretPassword123@db.prod.internal:5432/main using token Bearer sk-live-999888777666"

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
                "traceId": "50000000000000000000000000000005",
                "spanId": "5000000000000005",
                "name": "POST /api/connect",
                "kind": 1,
                "startTimeUnixNano": int(time.time() * 1e9),
                "endTimeUnixNano": int((time.time() + 0.1) * 1e9),
                "status": {"code": 2, "message": "Unhandled Exception"},
                "events": [{
                    "name": "exception",
                    "attributes": [
                        {"key": "exception.type", "value": {"stringValue": "DatabaseConnectionError"}},
                        {"key": "exception.message", "value": {"stringValue": secret_message}},
                        {"key": "exception.stacktrace", "value": {"stringValue": f"File 'db.py', line 12, in connect\n  raise DatabaseConnectionError('{secret_message}')"}}
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
print(f"Server Response: HTTP {res.status_code}")