#!/usr/bin/env python3
"""S08 — BoringSSL notes and detection (informational demo).
This script detects `openssl` on PATH and prints version output. BoringSSL is often
shipped as a vendor binary; full BoringSSL build instructions are in docs/.
"""
import subprocess
import shutil


def main():
    openssl = shutil.which("openssl")
    if not openssl:
        print("openssl not found on PATH. BoringSSL detection not available.")
        return
    try:
        out = subprocess.check_output([openssl, "version"], stderr=subprocess.STDOUT, text=True)
        print("openssl version output:\n", out)
        if "BoringSSL" in out:
            print("Detected BoringSSL build of openssl")
        else:
            print("No BoringSSL tag in `openssl version` output — may be OpenSSL or vendor build")
    except Exception as e:
        print("failed to run openssl:", e)


if __name__ == "__main__":
    main()
