#!/usr/bin/env python3
"""S06 — RNG demo: compare `secrets` vs `random` for key material."""
import random
import secrets


def demo():
    print("secrets.token_bytes(16):", secrets.token_bytes(16).hex())
    print("random.getrandbits(128):", hex(random.getrandbits(128)))
    print("\nBroken case: using Python `random` for key material is insecure (predictable)")


if __name__ == "__main__":
    demo()
