S03 — AES-GCM

Run:
  python3 aes_gcm_demo.py

Working:
- Demonstrates AES-GCM encrypt/decrypt with random nonce

Broken case:
- Reuse the same nonce for two messages (nonce reuse) -> shows why it's bad

What broke / why: GCM nonce reuse breaks confidentiality/AE.