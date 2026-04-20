#!/usr/bin/env python3
"""S25 demo: shows accidental key export via bad wrapper
"""
import requests, base64, os

ENGINE = 'http://127.0.0.1:9000'

# Broken: wrapper sends raw_key field (simulate accidental leak)
raw = base64.b64encode(b'some-private-key-bytes').decode()
try:
    r = requests.post(ENGINE + '/load_key', json={'key_id': 'leaky', 'type': 'mac', 'raw_key': raw}, timeout=1)
    print('Broken load_key response:', r.status_code, r.text)
except Exception as e:
    print('Loading with raw_key failed (engine likely rejects):', e)

print('\nFixed behavior: wrapper should raise before sending raw_key (see wrapper/crypto_wrapper.py)')
