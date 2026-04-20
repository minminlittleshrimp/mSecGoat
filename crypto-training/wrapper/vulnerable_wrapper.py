#!/usr/bin/env python3
"""Vulnerable wrapper demo: falls back to local software crypto when engine fails.
Used by S13 to illustrate why fallback is a silent security bypass.
"""
import traceback
from wrapper.crypto_wrapper import sign as engine_sign


def sign_with_fallback(key_id: str, data: bytes):
    try:
        return engine_sign(key_id, data)
    except Exception as e:
        print("Engine failed, falling back to local crypto (VULNERABLE):", e)
        traceback.print_exc()
        # vulnerable fallback: generate ephemeral software key and sign (insecure)
        from cryptography.hazmat.primitives.asymmetric import rsa, padding
        from cryptography.hazmat.primitives import hashes
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        sig = key.sign(data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return sig
