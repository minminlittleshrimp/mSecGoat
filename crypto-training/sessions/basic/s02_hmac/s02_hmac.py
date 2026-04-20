#!/usr/bin/env python3
"""S02 — HMAC demo: generate and verify; broken case uses wrong key."""
import secrets
from cryptography.hazmat.primitives import hmac, hashes


def make_hmac(key: bytes, data: bytes) -> bytes:
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data)
    return h.finalize()


def verify_hmac(key: bytes, data: bytes, tag: bytes) -> bool:
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data)
    try:
        h.verify(tag)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    key = secrets.token_bytes(32)
    data = b"important message"
    tag = make_hmac(key, data)
    print("HMAC:", tag.hex())
    print("verify (correct):", verify_hmac(key, data, tag))
    print("verify (wrong key):", verify_hmac(secrets.token_bytes(32), data, tag))
