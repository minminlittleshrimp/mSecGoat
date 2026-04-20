#!/usr/bin/env python3
"""Run a subset of sessions end-to-end for demo.
This runner starts the engine once and executes a chosen set of session demos.
"""
import subprocess, time, os, sys

ROOT = os.path.dirname(os.path.dirname(__file__))
ENGINE_SCRIPT = os.path.join(ROOT, 'engine', 'engine_server.py')
SESSIONS = [
    's01_hash/hash_demo.py',
    's02_hmac/hmac_demo.py',
    's03_aes_gcm/aes_gcm_demo.py',
    's04_sign_verify/sign_verify_demo.py',
    's06_rng/rng_demo.py',
    's07_kdf/kdf_demo.py',
    's05_tls_inspect/tls_server.py',
    's09_key_engine_basic/demo.py',
    's11_key_usage_enforcement/demo.py',
    's13_no_fallback_rule/demo.py',
    's18_key_lifecycle/demo.py',
    's20_failure_lab/demo.py'
]

if __name__ == '__main__':
    print('Starting engine...')
    proc = subprocess.Popen([sys.executable, ENGINE_SCRIPT])
    try:
        time.sleep(0.3)
        for s in SESSIONS:
            path = os.path.join(ROOT, 'sessions', s)
            print('\n--- RUNNING', s, '---')
            try:
                r = subprocess.run([sys.executable, path], check=False)
            except Exception as e:
                print('Failed to run', s, e)
            time.sleep(0.1)
    finally:
        proc.terminate()
        proc.wait()
        print('Engine stopped')
