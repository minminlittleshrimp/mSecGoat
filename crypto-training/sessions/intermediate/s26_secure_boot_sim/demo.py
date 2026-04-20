#!/usr/bin/env python3
"""S26 demo: signed firmware check
"""
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# create firmware (data), sign it
priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pub = priv.public_key()
firmware = b'VERSION=1\ncontents...'
sig = priv.sign(firmware, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

# Broken bootloader: skip verification
print('Broken bootloader: accepting firmware without checking (INSECURE)')

# Fixed bootloader: verify signature
try:
    pub.verify(sig, firmware, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
    print('Fixed bootloader: signature valid, firmware accepted')
except Exception:
    print('Fixed bootloader: signature invalid, reject')
