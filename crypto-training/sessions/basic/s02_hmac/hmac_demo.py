#!/usr/bin/env python3
import os
from cryptography.hazmat.primitives import hashes, hmac


def compute_hmac(key: bytes, data: bytes) -> bytes:
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


if __name__ == '__main__':
    key = os.urandom(32)
    data = b'message for HMAC'
    tag = compute_hmac(key, data)
    print('HMAC (hex):', tag.hex())
    print('Verify (correct):', verify_hmac(key, data, tag))

    # Broken case: wrong key
    bad_key = b'\x00'*32
    print('Verify (wrong key):', verify_hmac(bad_key, data, tag))
