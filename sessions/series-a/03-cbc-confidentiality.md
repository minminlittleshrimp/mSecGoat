# Series A — Session 03: Confidentiality Failure — CBC Without Integrity

Objective
- Demonstrate why AES‑CBC without integrity protection leads to undetected message modification and potential chosen‑ciphertext attacks.

Prereqs
- Ubuntu with `openssl` and `python3` (install via `sudo apt install openssl python3`).

Fixed parameters (DIY)
- Example key (hex): `00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff` (32 bytes)
- IV (hex): `000102030405060708090a0b0c0d0e0f` (16 bytes)
- Plaintext file: `message.txt`

Correct Path (copy/paste)

```bash
# AES-CBC encryption (no integrity) - vulnerable
openssl enc -aes-256-cbc -K 0011223344... -iv 00010203... -in message.txt -out message.cbc

# AES-GCM (AEAD) — correct: use AEAD for confidentiality+integrity
python3 - <<'PY'
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
key=bytes.fromhex('00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff')
aes=AESGCM(key)
nonce=bytes.fromhex('000102030405060708090a0b')
pt=open('message.txt','rb').read()
ct=aes.encrypt(nonce,pt,b'')
open('message.gcm','wb').write(ct)
print('WROTE message.gcm')
PY
```

Break Case (single-variable change)
- Use CBC encryption but an attacker flips a single ciphertext block; observe that decryption yields modified plaintext without detection.

Observation
- Decrypting tampered CBC ciphertext produces plausible modified plaintext; AEAD decrypt rejects tampering with an authentication failure.

Why
- CBC provides confidentiality only; without an authentication tag an active attacker can flip bits producing controlled changes. AEAD binds integrity to ciphertext.

Hard Rules
- Never use unauthenticated block cipher modes for data in transit or at rest.
- Use AEAD primitives (AES‑GCM/ChaCha20‑Poly1305) or Encrypt‑then‑MAC with strict verification.
- Include explicit associated data for binding metadata (IDs, sequence numbers).

Homework
- Reproduce both flows and demonstrate a CBC bitflip that yields a changed but valid-looking message.
