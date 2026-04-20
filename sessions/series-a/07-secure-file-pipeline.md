# Series A — Session 07: Secure File Pipeline (KDF + AEAD)

Objective
- Build a repeatable secure file pipeline: derive an encryption key from a passphrase (KDF + salt), then AEAD encrypt the data.

Prereqs
- `openssl`, `python3`, `python3-cryptography`.

Fixed parameters
- Passphrase: `demo-pass`
- Salt (hex): `deadbeef00112233`
- Nonce/IV deterministic example: `000000000000000000000001` (demo only)

Correct Path (copy/paste)

```bash
# Derive key (Python example using PBKDF2 and AES-GCM for AEAD)
python3 - <<'PY'
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
pw=b'demo-pass'
salt=bytes.fromhex('deadbeef00112233')
kdf=PBKDF2HMAC(hashes.SHA256(),32,salt,100000,default_backend())
key=kdf.derive(pw)
aes=AESGCM(key)
nonce=bytes.fromhex('000000000000000000000001')
pt=open('message.txt','rb').read()
ct=aes.encrypt(nonce,pt,b'file:1')
open('message.pipeline.bin','wb').write(ct)
print('WROTE message.pipeline.bin')
PY
```

Break Case (single-variable change)
- Omit salt (use empty salt); derived key becomes predictable for the same passphrase across files.

Observation
- Without salt and KDF work factor, passphrase-derived encryption keys are weak and susceptible to offline brute-force.

Why
- KDF with salt defends against precomputation; AEAD ensures confidentiality+integrity for the encrypted blob.

Hard Rules
- Always use a KDF + per-file salt for deriving keys from low-entropy input.
- Use AEAD to encrypt the derived key's output; include AD to bind metadata.
- Treat passphrases as low-entropy; prefer randomly generated keys for high‑security needs.

Homework
- Implement the pipeline on a test file and verify that changing the salt changes the ciphertext.
