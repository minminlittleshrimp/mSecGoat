#!/usr/bin/env python3
"""S04 — Sign/Verify demo (RSA PSS)."""
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def gen_keys():
    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub = priv.public_key()
    return priv, pub


if __name__ == "__main__":
    priv, pub = gen_keys()
    msg = b"sign me"
    sig = priv.sign(
        msg,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )
    print("signature:", sig.hex())
    try:
        pub.verify(
            sig,
            msg,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        print("verify ok")
    except Exception as e:
        print("verify failed:", e)

    # Broken case: tampered message
    print("\nBroken case: tampered message")
    try:
        pub.verify(
            sig,
            b"tampered",
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        print("unexpected: tampered verify ok")
    except Exception:
        print("tampered verify failed (expected)")
