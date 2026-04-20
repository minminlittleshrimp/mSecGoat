S02 — HMAC (SHA-256)

Run:
  python3 hmac_demo.py

Working:
- Generates a random key and computes HMAC-SHA256

Broken case:
- Replacing key with wrong key to show verification fails

What broke / why: HMAC binds key+message; wrong key -> verification fails.