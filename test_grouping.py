import os
import requests
import time
import subprocess

endpoint = "https://otlp.autter.dev"
api_key = "autter_rt_6e5e06b0b211fe45a88bd15ffe1624f1b86e5af4d489e683"  # <-- PASTE YOUR KEY HERE
git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

def send_error(message, trace_id, span_id):
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
                    "traceId": trace_id,
                    "spanId": span_id,
                    "name": "GET /api/factorial",
                    "kind": 1,
                    "startTimeUnixNano": int(time.time() * 1e9),
                    "endTimeUnixNano": int((time.time() + 0.1) * 1e9),
                    "status": {"code": 2, "message": "Unhandled Exception"},
                    "events": [{
                        "name": "exception",
                        "attributes": [
                            {"key": "exception.type", "value": {"stringValue": "ValueError"}},
                            {"key": "exception.message", "value": {"stringValue": message}},
                            {"key": "exception.stacktrace", "value": {"stringValue": "File 'fact.py', line 4, in factorial\n  raise ValueError(...)"}}
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
    print(f"Sent: '{message}' -> HTTP {res.status_code}")

print("[Test 2] Sending two distinct errors with dynamic numbers...")
# Bug A (Batch 9841)
send_error("Negative number error for batch 9841", "20000000000000000000000000000002", "2000000000000002")
time.sleep(1)
# Bug B (Transaction 1205)
send_error("Buffer overflow error for transaction 1205", "30000000000000000000000000000003", "3000000000000003")