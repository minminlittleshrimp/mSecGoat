#!/usr/bin/env python3
"""S14 — Error handling: invalid key_id and corrupted signature cases."""
from wrapper import crypto_wrapper as cw

if __name__ == "__main__":
    data = b"check error handling"
    print("Call sign with invalid key -> expect engine to return error (propagated)")
    try:
        cw.sign("no-such-key", data)
    except Exception as e:
        print("error propagated to caller:", type(e), e)

    print("\nBroken case: corrupted signature -> verify returns False")
    # create a valid signature, then corrupt it
    sig = cw.sign("sign1", data)
    bad = bytearray(sig)
    bad[0] = (bad[0] + 1) % 256
    ok = cw.verify("sign1", data, bytes(bad))
    print("verify with corrupted signature:", ok)
