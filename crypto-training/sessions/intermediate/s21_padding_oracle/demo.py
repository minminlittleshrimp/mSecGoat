#!/usr/bin/env python3
"""S21 demo: simple padding oracle simulation
Broken server leaks whether padding was correct; fixed server uses OAEP or constant-time path.
"""
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Prepare keys
priv = rsa.generate_private_key(public_exponent=65537, key_size=1024)
pub = priv.public_key()

msg = b'secret'
ct = pub.encrypt(msg, padding.PKCS1v15())

# Broken: naive decrypt that returns different messages for padding error
try:
    pt = priv.decrypt(ct, padding.PKCS1v15())
    print('Broken server: decryption succeeded, plaintext:', pt)
except Exception as e:
    print('Broken server: padding error (oracle)')

# Fixed: use OAEP for new encryptions
ct2 = pub.encrypt(msg, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
try:
    pt2 = priv.decrypt(ct2, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('Fixed server: OAEP decrypt succeeded, plaintext:', pt2)
except Exception:
    print('Fixed server: OAEP failed (no oracle)')
