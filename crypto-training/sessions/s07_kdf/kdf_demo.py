#!/usr/bin/env python3
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import os

password = b'supersecret'
salt = os.urandom(16)

pbkdf2 = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
key = pbkdf2.derive(password)
print('PBKDF2-derived key (hex):', key.hex())

hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake data')
master = hkdf.derive(b'master secret')
print('HKDF-derived key (hex):', master.hex())
