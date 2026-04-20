#!/usr/bin/env python3
"""Lab runner: initialize keys, start engine, run a subset of demos, then stop engine.
Runs selected sessions to demonstrate end-to-end behavior.
"""
import subprocess, os, sys, time, signal

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENGINE_DIR = os.path.join(ROOT, "engine")
PY = sys.executable

SESSIONS = [
    os.path.join(ROOT, "sessions", "s01_hash", "s01_hash.py"),
    os.path.join(ROOT, "sessions", "s02_hmac", "s02_hmac.py"),
    os.path.join(ROOT, "sessions", "s03_aes_gcm", "s03_aes_gcm.py"),
    os.path.join(ROOT, "sessions", "s04_sign_verify", "s04_sign_verify.py"),
    os.path.join(ROOT, "sessions", "s05_tls_inspect", "s05_tls_inspect.py"),
    os.path.join(ROOT, "sessions", "s09_key_engine_basic", "s09_demo.py"),
    os.path.join(ROOT, "sessions", "s11_key_usage_enforcement", "s11_demo.py"),
    os.path.join(ROOT, "labs", "s13_fallback_demo.py"),
]


def run(cmd, cwd=None):
    print("--- RUN:", cmd)
    r = subprocess.run(cmd, cwd=cwd, shell=False)
    return r.returncode


def main():
    env = os.environ.copy()
    env.setdefault("ENGINE_SECRET", "demo_engine_secret")
    # run init_keys
    rc = run([PY, os.path.join(ENGINE_DIR, "init_keys.py")], cwd=ENGINE_DIR)
    if rc != 0:
        print("init_keys failed, abort")
        return

    # start engine
    print("Starting engine server...")
    engine_proc = subprocess.Popen([PY, os.path.join(ENGINE_DIR, "server.py")], cwd=ENGINE_DIR, env=env)
    try:
        time.sleep(1.5)
        for s in SESSIONS:
            print("\n=== Session:", s)
            rc = run([PY, s], cwd=ROOT)
            if rc != 0:
                print("Session returned non-zero:", rc)
        print("\nAll sessions complete")
    finally:
        print("Stopping engine...")
        engine_proc.terminate()
        try:
            engine_proc.wait(timeout=3)
        except Exception:
            engine_proc.kill()


if __name__ == "__main__":
    main()
