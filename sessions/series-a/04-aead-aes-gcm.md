# Series A — Session 04: AEAD Enforcement — AES‑GCM

Objective
- Teach AEAD principles, nonce/IV discipline, and correct AES‑GCM usage including associated data (AD).

Prereqs
- `openssl`, `python3`, and `python3-cryptography` (install via apt where available).

Fixed parameters
- 256‑bit key (hex): `a0a1a2a3...a31` (example)
- Nonce length: 12 bytes (96 bits)

Correct Path (copy/paste)

```bash
# Example: AEAD with Python cryptography (copy/paste and replace key/nonce)
python3 - <<'PY'
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
key=bytes.fromhex('a0'*32)
aes=AESGCM(key)
nonce=bytes.fromhex('000000000000000000000001')
pt=b'example plaintext'
ad=b'file-id:42'
ct=aes.encrypt(nonce,pt,ad)
print(ct.hex())
PY
```

Break Case (single-variable change)
- Reuse the same nonce for a second encryption with the same key; observe confidentiality and authenticity collapse for AES‑GCM.

Observation
- Reusing nonce allows attackers to derive relationships between plaintexts and may enable tag forgeries.

Why
- AES‑GCM security requires unique nonces per key; reuse reduces security to catastrophic failures.

Hard Rules
- Nonce/IV must be unique per key operation; prefer a counter or an authenticated construction (e.g., per-record counter combined with random salt).
- Use AEAD always for encryption; never separate encryption and authentication incorrectly.
- If using raw libraries, enforce nonce uniqueness in application logic.

Homework
- Implement a short script (locally) that encrypts two messages with the same key+nonce and compare outputs to observe patterns.
