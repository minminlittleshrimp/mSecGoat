#!/usr/bin/env python3
"""S15: show data flow logging
"""
import subprocess, time, os, sys
from wrapper.crypto_wrapper import CryptoWrapper

ENGINE_SCRIPT = os.path.join(os.path.dirname(__file__), '..', 'engine', 'engine_server.py')
proc = subprocess.Popen([sys.executable, ENGINE_SCRIPT])
try:
    time.sleep(0.2)
    w = CryptoWrapper()
    data = b'flow-test'
    print('APP: calling wrapper.sign')
    sig = w.sign('sign-key', data)
    print('APP: got signature len', len(sig))
    print('APP: calling wrapper.mac')
    tag = w.mac('mac-key', data)
    print('APP: got tag len', len(tag))
    print('\nCheck engine logs (stdout) to see keys never leave engine store.')
finally:
    proc.terminate()
    proc.wait()
