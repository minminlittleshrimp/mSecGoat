Basic Sessions (S01–S08)
========================

.. contents::
   :local:

S01 — Hashing (SHA-256)
-----------------------
Follow-up hands-on:
- Accept file input and stream-hash large files.
- Compare SHA-256 vs SHA-3 on large inputs.
- Add unit tests that assert deterministic outputs for given inputs.

S02 — HMAC (SHA-256)
---------------------
Follow-up hands-on:
- Implement HMAC verification using constant-time compare.
- Rotate HMAC keys and validate old tags fail.
- Benchmark HMAC performance for different key sizes.

S03 — AES-GCM
-------------
Follow-up hands-on:
- Modify demo to generate a random nonce per message and track nonce storage.
- Demonstrate and detect nonce reuse across runs (log and assert).
- Implement AEAD with associated data and show what gets authenticated.

S04 — Sign / Verify (RSA)
-------------------------
Follow-up hands-on:
- Export public key and verify signatures in a separate process.
- Try different padding schemes (PSS vs PKCS1v15) and observe failures.
- Add negative tests for tampered messages and corrupted signatures.

S05 — TLS inspect
------------------
Follow-up hands-on:
- Run the TLS server and inspect handshake with openssl s_client.
- Enable and disable certificate verification on client; observe effects.
- Capture handshake with Wireshark and locate certificate fields.

S06 — RNG
---------
Follow-up hands-on:
- Replace os.urandom with deterministic PRNG and show breakage.
- Integrate Python's secrets module and demonstrate secure key generation.
- Add tests to detect low-entropy seeds (e.g., repeated outputs).

S07 — KDFs (PBKDF2, HKDF)
-------------------------
Follow-up hands-on:
- Change PBKDF2 iteration count and observe derived key differences.
- Store salt separately and write code to re-derive keys for verification.
- Use HKDF to derive multiple subkeys for different purposes.

S08 — BoringSSL gap (notes)
---------------------------
Follow-up hands-on:
- Read notes and list APIs missing in BoringSSL for engine/provider.
- Create a short compatibility checklist for porting code.
- Try building a small OpenSSL-based example and note BoringSSL differences.

