#!/usr/bin/env python3
"""S01 — SHA-256 hash demo: working and broken case."""
from cryptography.hazmat.primitives import hashes


def sha256(data: bytes) -> bytes:
    d = hashes.Hash(hashes.SHA256())
    d.update(data)
    return d.finalize()


if __name__ == "__main__":
    m = b"hello world"
    print("Input:", m)
    d = sha256(m)
    print("SHA-256:", d.hex())

    # Broken case: truncated digest accepted (simulated)
    print("\nBroken case: truncated digest (12 bytes) — demonstrates weakened checks")
    d_trunc = d[:12]
    print("Truncated:", d_trunc.hex())
