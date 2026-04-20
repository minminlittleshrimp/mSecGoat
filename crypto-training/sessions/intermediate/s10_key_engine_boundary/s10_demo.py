#!/usr/bin/env python3
"""S10 — Boundary enforcement demo.
Attempts to decrypt engine keys with a wrong secret (should fail), demonstrating the
engine keeps key material protected unless the correct `ENGINE_SECRET` is provided.
"""
import os, json, base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

KEY_PATH = os.path.join(os.path.dirname(__file__), "..", "engine", "keys.enc")


def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390000)
    return base64.urlsafe_b64encode(kdf.derive(password))


if __name__ == "__main__":
    kp = os.path.abspath(KEY_PATH)
    print("Trying to open engine keys file:", kp)
    with open(kp, "r") as f:
        obj = json.load(f)
    salt = base64.b64decode(obj["salt"])
    token = obj["token"].encode()
    wrong = b"incorrect_secret"
    try:
        key = derive_key(wrong, salt)
        f = Fernet(key)
        f.decrypt(token)
        print("Unexpected: decrypted with wrong secret")
    except Exception as e:
        print("As expected: cannot decrypt keys with wrong secret:", e)
