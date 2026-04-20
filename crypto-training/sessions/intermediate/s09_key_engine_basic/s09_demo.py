#!/usr/bin/env python3
"""S09 — Key engine basic demo: sign/verify and mac via wrapper talking to engine."""
import os
import time
from wrapper import crypto_wrapper as cw


def run():
    data = b"hello from s09"
    print("Signing via engine -> wrapper.sign()")
    sig = cw.sign("sign1", data)
    print("signature (hex):", sig.hex())
    ok = cw.verify("sign1", data, sig)
    print("verify ok:", ok)

    print("MAC via engine -> wrapper.mac()")
    tag = cw.mac("mac1", data)
    print("mac tag:", tag.hex())


if __name__ == "__main__":
    run()
