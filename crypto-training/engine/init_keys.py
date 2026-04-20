#!/usr/bin/env python3
"""Generate demo keys and write an encrypted keys blob (keys.enc).
Use `ENGINE_SECRET` env var to derive the encryption key; defaults to `demo_engine_secret`.
"""
import os
import json
import base64
import secrets
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

KEY_PATH = os.path.join(os.path.dirname(__file__), "keys.enc")


def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390000)
    return base64.urlsafe_b64encode(kdf.derive(password))


if __name__ == "__main__":
    secret = os.environ.get("ENGINE_SECRET", "demo_engine_secret").encode()
    salt = secrets.token_bytes(16)

    # generate RSA signing key
    rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = rsa_key.private_bytes(encoding=serialization.Encoding.PEM,
                                        format=serialization.PrivateFormat.PKCS8,
                                        encryption_algorithm=serialization.NoEncryption())
    public_pem = rsa_key.public_key().public_bytes(encoding=serialization.Encoding.PEM,
                                                    format=serialization.PublicFormat.SubjectPublicKeyInfo)

    # generate HMAC key
    hmac_key = secrets.token_bytes(32)

    meta = {
        "keys": {
            "sign1": {
                "type": "sign",
                "created_at": int(__import__('time').time()),
                "usage_count": 0,
                "private": base64.b64encode(private_pem).decode(),
                "public": base64.b64encode(public_pem).decode()
            },
            "mac1": {
                "type": "mac",
                "created_at": int(__import__('time').time()),
                "usage_count": 0,
                "key": base64.b64encode(hmac_key).decode()
            }
        }
    }

    key = derive_key(secret, salt)
    f = Fernet(key)
    token = f.encrypt(json.dumps(meta).encode())

    out = {"salt": base64.b64encode(salt).decode(), "token": token.decode()}
    with open(KEY_PATH, "w") as f_out:
        json.dump(out, f_out)
    print("Wrote keys to:", KEY_PATH)
    print("Use ENGINE_SECRET to control decryption (default `demo_engine_secret`).")
