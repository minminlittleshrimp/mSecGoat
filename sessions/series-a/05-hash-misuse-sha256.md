# Series A — Session 05: Hash Misuse — SHA‑256

Objective
- Explain common hash misuse patterns: using raw hashes for authentication, key derivation, and password storage.

Prereqs
- `openssl` and `python3`.

Fixed parameters (examples)
- Message: `data.bin`
- Password: `hunter2` (DO NOT use in production; demo only)

Correct Path (copy/paste)

```bash
# Compute SHA-256 digest (illustration only)
openssl dgst -sha256 data.bin

# For authentication, use HMAC-SHA256 instead of plain SHA256
python3 - <<'PY'
import hmac,hashlib,binascii
key=b'k'*32
msg=open('data.bin','rb').read()
print(hmac.new(key,msg,hashlib.sha256).hexdigest())
PY
```

Break Case (single-variable change)
- Replace HMAC with raw SHA‑256 in an authentication check. Demonstrate how attackers can compute valid digests and bypass checks.

Observation
- Raw hashes do not provide keyed authenticity; HMAC provides a keyed MAC resistant to forgery.

Why
- Hash functions provide one‑way compression, not keyed authentication; using them alone for integrity/authentication is insecure.

Hard Rules
- Use HMAC for keyed message authentication; do not roll your own MACs.
- Use SHA‑256 only as a primitive inside approved constructions (HMAC, HKDF, KDFs).
- Never use raw hash outputs as password-derived keys; always use a proper KDF with salt and work factor.

Homework
- Show the difference: compute SHA‑256 and HMAC‑SHA256 for the same input and explain why HMAC prevents forgery.
