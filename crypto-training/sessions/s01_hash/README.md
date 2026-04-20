S01 — Hashing (SHA-256)

Run:
  python3 hash_demo.py "some text"

Working:
- Uses pyca/cryptography SHA-256

Broken case:
- Passing binary data interpreted incorrectly

What broke / why: the demo shows deterministic digest, small errors in input cause different output.