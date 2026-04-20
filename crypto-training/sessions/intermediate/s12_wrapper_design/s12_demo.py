#!/usr/bin/env python3
"""S12 — Wrapper design: only expose sign/verify/mac; algorithm param is ignored."""
from wrapper import crypto_wrapper as cw

if __name__ == "__main__":
    data = b"wrapper design test"
    print("Calling wrapper.sign with extra algorithm parameter (should be ignored)")
    sig = cw.sign("sign1", data, algorithm="rsa-pss")
    print("signature hex:", sig.hex())
