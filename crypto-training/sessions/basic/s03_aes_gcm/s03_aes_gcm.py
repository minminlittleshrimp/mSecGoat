#!/usr/bin/env python3
"""S03 — AES-GCM demo: encryption/decryption and nonce reuse broken case."""
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt(key: bytes, nonce: bytes, pt: bytes, aad: bytes = b"") -> bytes:
    aes = AESGCM(key)
    return aes.encrypt(nonce, pt, aad)


def decrypt(key: bytes, nonce: bytes, ct: bytes, aad: bytes = b"") -> bytes:
    aes = AESGCM(key)
    return aes.decrypt(nonce, ct, aad)


if __name__ == "__main__":
    key = AESGCM.generate_key(bit_length=128)
    nonce = os.urandom(12)
    pt = b"secret message"
    ct = encrypt(key, nonce, pt)
    print("ciphertext:", ct.hex())
    pt2 = decrypt(key, nonce, ct)
    print("decrypted:", pt2)

    # Broken case: nonce reuse
    print("\nBroken case: nonce reuse demonstration (do NOT reuse nonces in AES-GCM)")
    nonce2 = nonce
    pt3 = b"another message"
    ct1 = encrypt(key, nonce2, pt)
    ct2 = encrypt(key, nonce2, pt3)
    print("reused nonce produced cipher1:", ct1.hex())
    print("reused nonce produced cipher2:", ct2.hex())
