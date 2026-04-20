#!/usr/bin/env python3
"""S11 — Key usage enforcement: try to use a sign key for MAC (should be rejected by engine)."""
import base64
import requests

ENGINE_URL = "http://127.0.0.1:9001"

if __name__ == "__main__":
    data = base64.b64encode(b"message for mac").decode()
    print("Using sign1 as a MAC key (expected to fail)")
    r = requests.post(ENGINE_URL + "/mac", json={"key_id": "sign1", "data": data})
    print("status code:", r.status_code)
    print("response:", r.text)
