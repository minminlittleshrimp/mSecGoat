#!/usr/bin/env python3
"""Buggy wrapper that falls back to local crypto if engine fails.
This demonstrates the "silent fallback" anti-pattern described in the program.
"""
import base64
import requests
import os
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import rsa, padding

class BuggyWrapper:
    def __init__(self, engine_url='http://127.0.0.1:9000'):
        self.engine_url = engine_url.rstrip('/')
        # Local key cache (insecure fallback)
        self._local_keys = {}

    def _post(self, path, payload):
        r = requests.post(self.engine_url + path, json=payload, timeout=2)
        if r.status_code != 200:
            raise RuntimeError('Engine error')
        obj = r.json()
        if obj.get('status') != 'ok':
            raise RuntimeError('Engine reported error')
        return obj['result']

    def sign(self, key_id, data: bytes) -> bytes:
        try:
            res = self._post('/sign', {'key_id': key_id, 'data': base64.b64encode(data).decode()})
            return base64.b64decode(res['signature'])
        except Exception:
            # BAD: fallback to local signing
            print('Engine failed — falling back to local signing (INSECURE)')
            if key_id not in self._local_keys:
                self._local_keys[key_id] = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            priv = self._local_keys[key_id]
            return priv.sign(data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

    def mac(self, key_id, data: bytes) -> bytes:
        try:
            res = self._post('/mac', {'key_id': key_id, 'data': base64.b64encode(data).decode()})
            return base64.b64decode(res['tag'])
        except Exception:
            # BAD: fallback to local HMAC using zero key
            print('Engine failed — falling back to local HMAC (INSECURE)')
            k = b'\x00'*32
            h = hmac.HMAC(k, hashes.SHA256())
            h.update(data)
            return h.finalize()

    # verify and verify_mac intentionally omitted for brevity of the broken example
