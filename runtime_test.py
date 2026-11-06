import os
import requests
import time
import subprocess

# 1. Configuration
endpoint = "https://otlp.autter.dev"
api_key = "autter_rt_6e5e06b0b211fe45a88bd15ffe1624f1b86e5af4d489e683"  # <-- PASTE YOUR KEY HERE

# Automatically get the current commit SHA from git
git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

print(f"[Test 1] Sending crash for commit {git_sha[:8]}...")

# 2. Build OpenTelemetry Trace Payload
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
                "traceId": "10000000000000000000000000000001",
                "spanId": "1000000000000001",
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

# 3. Send to Autter Runtime
res = requests.post(
    f"{endpoint}/v1/traces",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json=payload
)
print(f"Server Response: HTTP {res.status_code}")