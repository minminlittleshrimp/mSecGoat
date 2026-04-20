#!/usr/bin/env python3
"""S10: show import boundary and separate-process operation
"""
import subprocess, sys, time, os

try:
    import engine.engine_server as es
    print('Unexpected: import succeeded (boundary failed)')
except Exception as e:
    print('Importing engine.engine_server failed (expected):', type(e), str(e)[:120])

# Now start engine as a process and use wrapper to call it
from wrapper.crypto_wrapper import CryptoWrapper
ENGINE_SCRIPT = os.path.join(os.path.dirname(__file__), '..', 'engine', 'engine_server.py')
proc = subprocess.Popen([sys.executable, ENGINE_SCRIPT])
try:
    time.sleep(0.3)
    w = CryptoWrapper()
    print('Engine meta via wrapper:', w._post('/meta', {}))
finally:
    proc.terminate()
    proc.wait()
