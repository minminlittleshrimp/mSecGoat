#!/usr/bin/env python3
"""Minimal HTTP client for the demo engine."""
import os
import base64
import requests

ENGINE_URL = os.environ.get("ENGINE_URL", "http://127.0.0.1:9001")


def sign(key_id: str, data: bytes, timeout: int = 5) -> bytes:
    r = requests.post(ENGINE_URL + "/sign", json={"key_id": key_id, "data": base64.b64encode(data).decode()}, timeout=timeout)
    r.raise_for_status()
    return base64.b64decode(r.json()["signature"])


def mac(key_id: str, data: bytes, timeout: int = 5) -> bytes:
    r = requests.post(ENGINE_URL + "/mac", json={"key_id": key_id, "data": base64.b64encode(data).decode()}, timeout=timeout)
    r.raise_for_status()
    return base64.b64decode(r.json()["tag"])


def get_pubkey_pem(key_id: str, timeout: int = 5) -> str:
    r = requests.get(f"{ENGINE_URL}/pubkey/{key_id}", timeout=timeout)
    r.raise_for_status()
    return r.json()["public_pem"]


if __name__ == "__main__":
    print("Engine client helper. Use from other scripts.")
