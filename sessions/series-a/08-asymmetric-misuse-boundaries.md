# Series A — Session 08: Asymmetric Crypto Misuse Boundaries

Objective
- Clarify the intended uses of asymmetric primitives: signing vs encryption, key wrapping vs direct encryption, and hybrid schemes.

Prereqs
- `openssl` installed.

Fixed parameters (filenames)
- `privA.pem`, `pubA.pem`, `privB.pem`, `pubB.pem`, `message.txt`.

Correct Path (copy/paste)

```bash
# Generate keys (demo)
openssl genpkey -algorithm RSA -out privA.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -in privA.pem -pubout -out pubA.pem

# Encrypt with hybrid scheme: generate symmetric key, encrypt data with AEAD, wrap symmetric key with recipient's public key
# (high level, implement with your chosen libraries; do not use RSA raw encryption for large payloads)
```

Break Case (single-variable change)
- Attempt to encrypt large payloads directly with RSA (RSAES) instead of hybrid encryption; observe size limits and padding issues.

Observation
- Direct asymmetric encryption is limited in size and can be misused; signature verification and encryption purposes must be distinct.

Why
- Asymmetric ops are heavy and intended for key transport or signing; hybrid patterns (KEM + AEAD) are standard for large data.

Hard Rules
- Use hybrid encryption (KEM/DEM) or established protocols (ECIES, RSA‑OAEP + AEAD) for data encryption.
- Use separate key pairs or clear usage labels for signing vs encryption.
- Follow recommended formats (CMS, CMS EnvelopedData, RFC 8317) rather than inventing protocols.

Homework
- Outline a hybrid encryption flow for a file and map each step to primitives you would use in production.
