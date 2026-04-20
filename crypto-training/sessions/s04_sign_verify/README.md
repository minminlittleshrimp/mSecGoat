S04 — Sign / Verify (RSA)

Run:
  python3 sign_verify_demo.py

Working:
- Generate RSA keypair, sign with PSS+SHA256, verify

Broken case:
- Tamper the signature -> verification fails

What broke / why: Signature binds message to signer.