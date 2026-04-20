#!/usr/bin/env python3
"""S01: SHA-256 hashing demo
"""
import sys
from cryptography.hazmat.primitives import hashes


def sha256_hex(data: bytes) -> str:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    return digest.finalize().hex()


if __name__ == '__main__':
    data = b'Hello IVI' if len(sys.argv) < 2 else sys.argv[1].encode()
    print('Input:', data)
    print('SHA256:', sha256_hex(data))
