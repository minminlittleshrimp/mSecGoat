#!/usr/bin/env python3
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


def generate_rsa():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


if __name__ == '__main__':
    key = generate_rsa()
    pub = key.public_key()
    data = b'important message'
    sig = key.sign(data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
    print('Signature len:', len(sig))
    try:
        pub.verify(sig, data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        print('Verify: OK')
    except Exception as e:
        print('Verify failed:', e)

    # Broken: tamper signature
    bad = bytearray(sig)
    bad[0] ^= 1
    try:
        pub.verify(bytes(bad), data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        print('Tampered verify: OK (unexpected)')
    except Exception:
        print('Tampered verify: failed (expected)')
