import os
import requests
import time

endpoint = "https://otlp.autter.dev"
api_key = "autter_rt_6e5e06b0b211fe45a88bd15ffe1624f1b86e5af4d489e683"  # <-- Paste your key

print("[Adv Test 3] Firing a burst of 50 rapid error requests...")

status_counts = {}

payload = {
    "resourceSpans": [{
        "resource": {"attributes": [{"key": "service.name", "value": {"stringValue": "stress-test"}}]},
        "scopeSpans": [{
            "spans": [{
                "traceId": "60000000000000000000000000000006",
                "spanId": "6000000000000006",
                "name": "GET /crash-loop",
                "kind": 1,
                "startTimeUnixNano": int(time.time() * 1e9),
                "endTimeUnixNano": int((time.time() + 0.01) * 1e9),
                "status": {"code": 2, "message": "Loop Crash"}
            }]
        }]
    }]
}

for i in range(50):
    res = requests.post(
        f"{endpoint}/v1/traces",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload
    )
    status_counts[res.status_code] = status_counts.get(res.status_code, 0) + 1

print(f"Results of 50 burst requests: {status_counts}")