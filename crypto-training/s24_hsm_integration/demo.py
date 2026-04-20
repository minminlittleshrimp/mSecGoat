#!/usr/bin/env python3
"""S24 demo: simulate HSM export policy
"""
import requests, base64, os, time

ENGINE = 'http://127.0.0.1:9000'

# Broken client: asks engine for raw key (simulated endpoint)
try:
    r = requests.post(ENGINE + '/export_key', json={'key_id': 'mac-key'}, timeout=1)
    print('Export response (broken client):', r.status_code, r.text)
except Exception as e:
    print('Broken client: export attempt failed or endpoint missing ->', e)

# Proper flow: ask engine meta only
r = requests.post(ENGINE + '/meta', json={})
print('Engine meta keys:', r.json().get('result'))

print('\nLesson: never request raw key material from engine/HSM; use operations by key_id only.')
