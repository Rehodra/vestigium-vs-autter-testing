import os
import requests
import time

endpoint = os.getenv("AUTTER_ENDPOINT", "https://otlp.autter.dev")
api_key = "autter_rt_6e5e06b0b211fe45a88bd15ffe1624f1b86e5af4d489e683"
git_sha = os.getenv("GIT_SHA", "unknown-sha")

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

# Send Bug A
send_error("Negative number error for batch 9841", "11111111111111111111111111111111", "1111111111111111")
time.sleep(2)
# Send Bug B (completely different root cause, but same error type and file)
send_error("Buffer overflow error for transaction 1205", "22222222222222222222222222222222", "2222222222222222")