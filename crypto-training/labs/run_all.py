#!/usr/bin/env python3
"""Run curated sessions grouped by level: basic -> intermediate -> advanced
"""
import subprocess, time, os, sys

ROOT = os.path.dirname(os.path.dirname(__file__))
ENGINE_SCRIPT = os.path.join(ROOT, 'engine', 'engine_server.py')
SESSIONS = [
    # Basic
    's01_hash/hash_demo.py',
    's02_hmac/hmac_demo.py',
    's03_aes_gcm/aes_gcm_demo.py',
    's04_sign_verify/sign_verify_demo.py',
    's05_tls_inspect/tls_server.py',
    's06_rng/rng_demo.py',
    's07_kdf/kdf_demo.py',
    's08_boringssl/README.md',
    # Intermediate
    's09_key_engine_basic/demo.py',
    's10_key_engine_boundary/demo.py',
    's11_key_usage_enforcement/demo.py',
    's12_wrapper_design/README.md',
    's13_no_fallback_rule/demo.py',
    's14_error_handling/demo.py',
    's15_data_flow_trace/demo.py',
    's21_padding_oracle/demo.py',
    's22_timing_attack/demo.py',
    's23_side_channel_sim/demo.py',
    's24_hsm_integration/demo.py',
    's25_key_export_attack/demo.py',
    's26_secure_boot_sim/demo.py',
    # Advanced
    's16_openssl_engine_provider/README.md',
    's17_boringssl_gap/README.md',
    's18_key_lifecycle/demo.py',
    's19_tls_misconfig/demo.py',
    's20_failure_lab/demo.py',
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
