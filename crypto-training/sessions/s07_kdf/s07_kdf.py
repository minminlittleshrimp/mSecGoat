#!/usr/bin/env python3
"""S07 — KDF demo: HKDF usage."""
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


if __name__ == "__main__":
    ikm = b"initial key material"
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"handshake data")
    okm = hkdf.derive(ikm)
    print("HKDF output (32 bytes):", okm.hex())
    print("Broken case: using raw IKM directly as symmetric keys without KDF")
