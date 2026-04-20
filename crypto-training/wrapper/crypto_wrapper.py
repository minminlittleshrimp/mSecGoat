#!/usr/bin/env python3
"""Crypto wrapper that exposes only `sign`, `verify`, and `mac`.
- No algorithm selection allowed (ignored)
- No raw key input allowed (raises)
- No fallback to local crypto
"""
import os
import base64
import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

ENGINE_URL = os.environ.get("ENGINE_URL", "http://127.0.0.1:9001")


def _post(path: str, payload: dict):
    r = requests.post(ENGINE_URL + path, json=payload, timeout=5)
    r.raise_for_status()
    return r.json()


def sign(key_id: str, data: bytes, **kwargs) -> bytes:
    if 'algorithm' in kwargs:
        # ignore algorithm selection — wrapper restricts algorithm surface
        pass
    if 'key' in kwargs:
        raise ValueError("raw key input forbidden")
    payload = {"key_id": key_id, "data": base64.b64encode(data).decode()}
    r = _post("/sign", payload)
    return base64.b64decode(r["signature"])


def verify(key_id: str, data: bytes, signature: bytes) -> bool:
    r = requests.get(f"{ENGINE_URL}/pubkey/{key_id}", timeout=5)
    r.raise_for_status()
    pub_pem = r.json()["public_pem"].encode()
    pub = serialization.load_pem_public_key(pub_pem)
    try:
        pub.verify(signature, data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except Exception:
        return False


def mac(key_id: str, data: bytes, **kwargs) -> bytes:
    if 'algorithm' in kwargs:
        pass
    if 'key' in kwargs:
        raise ValueError("raw key input forbidden")
    payload = {"key_id": key_id, "data": base64.b64encode(data).decode()}
    r = _post("/mac", payload)
    return base64.b64decode(r["tag"])
