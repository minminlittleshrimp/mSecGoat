#!/usr/bin/env python3
"""S14: Error handling behavior
"""
import subprocess, sys, time, os
from wrapper.crypto_wrapper import CryptoWrapper

ENGINE_SCRIPT = os.path.join(os.path.dirname(__file__), '..', 'engine', 'engine_server.py')
proc = subprocess.Popen([sys.executable, ENGINE_SCRIPT])
try:
    time.sleep(0.2)
    w = CryptoWrapper()
    try:
        w.sign('nonexistent-key', b'data')
        print('Unexpected success')
    except Exception as e:
        print('Correct behavior: error propagated ->', str(e)[:120])

    # Tampered signature
    sig = w.sign('sign-key', b'data')
    bad = bytearray(sig)
    bad[0] ^= 0xFF
    print('Verify tampered signature (expected False):', w.verify('sign-key', b'data', bytes(bad)))
finally:
    proc.terminate()
    proc.wait()
