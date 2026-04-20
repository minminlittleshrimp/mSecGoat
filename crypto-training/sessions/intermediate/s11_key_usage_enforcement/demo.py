#!/usr/bin/env python3
"""S11: show engine rejects wrong key usage
"""
import subprocess, sys, time, os
from wrapper.crypto_wrapper import CryptoWrapper

ENGINE_SCRIPT = os.path.join(os.path.dirname(__file__), '..', 'engine', 'engine_server.py')
proc = subprocess.Popen([sys.executable, ENGINE_SCRIPT])
try:
    time.sleep(0.3)
    w = CryptoWrapper()
    data = b'test'
    try:
        # Attempt to MAC with a sign key (should be rejected by engine)
        print('Attempting mac with sign-key...')
        w.mac('sign-key', data)
        print('Unexpected success: engine did not enforce key usage')
    except Exception as e:
        print('Expected rejection for misuse:', str(e))

    # Correct use
    tag = w.mac('mac-key', data)
    print('mac-key ok, tag len:', len(tag))
finally:
    proc.terminate()
    proc.wait()
