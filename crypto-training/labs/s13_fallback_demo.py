#!/usr/bin/env python3
"""S13 — Demonstrate fallback vulnerability: when engine is down, vulnerable wrapper falls back.
Run this while the engine is stopped to see the insecure fallback.
"""
import os
from wrapper import vulnerable_wrapper as vw


def demo():
    data = b"vulnerable fallback test"
    print("Calling vulnerable_wrapper.sign_with_fallback() with engine NOT running")
    sig = vw.sign_with_fallback("sign1", data)
    print("Produced signature (hex, possibly by fallback):", sig.hex())


if __name__ == "__main__":
    demo()
