#!/usr/bin/env python3
"""S13: demonstrate fallback bypass
"""
import subprocess, sys, time, os
from wrapper.crypto_wrapper import CryptoWrapper
from wrapper.buggy_wrapper import BuggyWrapper

ENGINE_SCRIPT = os.path.join(os.path.dirname(__file__), '..', 'engine', 'engine_server.py')
# Start engine normally then try a simulated failing call
proc = subprocess.Popen([sys.executable, ENGINE_SCRIPT])
try:
    time.sleep(0.2)
    safe = CryptoWrapper()
    buggy = BuggyWrapper()
    data = b'important'
    # normal call
    print('Safe wrapper sign ok:', len(safe.sign('sign-key', data)))
    # Now ask engine to simulate failure for this request
    try:
        print('Safe wrapper when engine fails:')
        safe._post('/sign', {'key_id': 'sign-key', 'data': '', 'simulate_fail': True})
    except Exception as e:
        print('Safe wrapper raised (expected):', str(e)[:120])

    # Buggy wrapper will fallback
    try:
        print('Buggy wrapper attempting sign while engine simulated to fail...')
        res = buggy.sign('sign-key', data)
        print('Buggy wrapper returned signature len (fallback):', len(res))
    except Exception as e:
        print('Buggy wrapper also failed:', e)
finally:
    proc.terminate()
    proc.wait()
