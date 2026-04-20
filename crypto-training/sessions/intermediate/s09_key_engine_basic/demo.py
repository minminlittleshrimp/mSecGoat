#!/usr/bin/env python3
"""S09 demo: uses engine (must be running) via wrapper
"""
import time, subprocess, os, sys
from wrapper.crypto_wrapper import CryptoWrapper

ENGINE_SCRIPT = os.path.join(os.path.dirname(__file__), '..', 'engine', 'engine_server.py')


def start_engine():
    # Start engine as separate process if not reachable
    print('Attempting to start engine...')
    p = subprocess.Popen([sys.executable, ENGINE_SCRIPT])
    time.sleep(0.5)
    return p


if __name__ == '__main__':
    w = CryptoWrapper()
    try:
        # Try to call meta first; if engine not running this will raise
        print('Engine meta:', w._post('/meta', {}))
    except Exception:
        proc = start_engine()
    else:
        proc = None

    time.sleep(0.2)
    # Use default keys created by engine on startup
    data = b'hello engine'
    sig = w.sign('sign-key', data)
    print('Signature (len):', len(sig))
    print('Verify:', w.verify('sign-key', data, sig))

    tag = w.mac('mac-key', data)
    print('MAC (len):', len(tag))
    print('Verify MAC:', w.verify_mac('mac-key', data, tag))

    if proc:
        proc.terminate()
        proc.wait()
