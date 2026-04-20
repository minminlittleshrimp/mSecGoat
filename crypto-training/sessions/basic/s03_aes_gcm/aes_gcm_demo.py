#!/usr/bin/env python3
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt(key: bytes, nonce: bytes, data: bytes) -> bytes:
    aesgcm = AESGCM(key)
    return aesgcm.encrypt(nonce, data, None)


def decrypt(key: bytes, nonce: bytes, ct: bytes) -> bytes:
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ct, None)


if __name__ == '__main__':
    key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    msg1 = b'first message'
    msg2 = b'second message'

    ct1 = encrypt(key, nonce, msg1)
    ct2 = encrypt(key, nonce, msg2)  # intentionally reusing nonce (broken)

    print('Nonce reused (hex):', nonce.hex())
    print('CT1 len:', len(ct1), 'CT2 len:', len(ct2))

    # Decrypting works for library but misuse is catastrophic in practice
    print('Decrypt1:', decrypt(key, nonce, ct1))
    print('Decrypt2:', decrypt(key, nonce, ct2))

    print('\nBroken analysis: using same nonce for different plaintexts leaks relationships and may allow key recovery in real attacks.')
