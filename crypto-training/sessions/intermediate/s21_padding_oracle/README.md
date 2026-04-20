S21 — Padding oracle (PKCS#1 v1.5) simulation

Run:
  python3 demo.py

Working:
- Use OAEP/RSA or constant-time decryption to avoid oracle

Broken:
- Vulnerable server reveals padding error vs decryption success (oracle)

What broke / why: padding oracles enable plaintext recovery for RSA PKCS#1 v1.5.

Exercise: run broken/demo.py then run fixed/demo.py to observe the difference.