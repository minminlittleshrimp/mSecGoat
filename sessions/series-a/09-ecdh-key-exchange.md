# Series A — Session 09: Key Exchange — Elliptic Curve Diffie‑Hellman (ECDH)

Objective
- Demonstrate ECDH key agreement, shared secret derivation, and secure usage with KDF + AEAD.

Prereqs
- `openssl` installed (OpenSSL provides `pkey` and `pkeyutl`).

Fixed parameters (curves)
- Curve: `prime256v1` (aka P‑256)

Correct Path (copy/paste)

```bash
# Generate keypairs
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:prime256v1 -out privA.pem
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:prime256v1 -out privB.pem
openssl pkey -in privA.pem -pubout -out pubA.pem
openssl pkey -in privB.pem -pubout -out pubB.pem

# Derive shared secret (OpenSSL pkeyutl)
openssl pkeyutl -derive -inkey privA.pem -peerkey pubB.pem -out sharedA.bin
openssl pkeyutl -derive -inkey privB.pem -peerkey pubA.pem -out sharedB.bin

# Verify shared secrets equal (hex)
xxd -p sharedA.bin; xxd -p sharedB.bin
```

Break Case (single-variable change)
- Use mismatched curves or convert public key formats incorrectly; derivation fails or produces different secrets.

Observation
- Correct ECDH derivations yield identical shared secrets; mismatches indicate parameter or format errors.

Why
- Key agreement relies on exact curve parameters and correct key formats; KDF must be applied to the raw shared secret before use.

Hard Rules
- Always apply a KDF (e.g., HKDF-SHA256) to the raw shared secret before deriving symmetric keys.
- Validate peer public keys (parameters, formats) before using them in derivation.
- Use standardized curves and avoid undocumented custom curves.

Homework
- Run the commands above and pipe the derived secret into an HKDF to produce an AEAD key for secure exchange.
