# Series A — Session 06: Password Derivation — PBKDF2

Objective
- Teach correct password-based key derivation with salt and work factor (PBKDF2), and why raw hashing is insufficient.

Prereqs
- `openssl` and `python3` with `cryptography` available.

Fixed parameters (examples)
- Password: `password123`
- Salt (hex): `aabbccddeeff0011223344`
- Iterations: `100000`

Correct Path (copy/paste)

```bash
# Derive key with OpenSSL (PBKDF2)
openssl passwd -pbkdf2 -salt aabbccddeeff0011223344 -stdin <<< "password123"

# Derive using Python cryptography (explicit)
python3 - <<'PY'
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
pw=b'password123'
salt=bytes.fromhex('aabbccddeeff0011223344')
kdf=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
key=kdf.derive(pw)
print(key.hex())
PY
```

Break Case (single-variable change)
- Omit the salt or use a fixed constant salt across users. Show derived keys identical for same password.

Observation
- Missing salt makes passwords susceptible to precomputed dictionary attacks; low iteration counts make brute-force cheaper.

Why
- Salt ensures per-user uniqueness; work factor slows brute-force attempts.

Hard Rules
- Always use a KDF with a per‑password random salt and sufficient iterations/OPs (NIST/OWASP recommendations).
- Avoid custom KDFs; use well-reviewed constructs (PBKDF2, scrypt, Argon2).
- Store salt and work parameters alongside the derived output.

Homework
- Demonstrate identical derived keys when salt is omitted; then re-run with unique salts to show differentiation.
