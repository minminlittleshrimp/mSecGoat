# Series A — Session 02: Key Formats & Exposure Handling

Objective
- Understand key encodings (PEM/DER/PKCS#1/PKCS#8), encrypted vs unencrypted storage, and safe export patterns.

Prereqs
- Ubuntu with `openssl` installed.

Fixed parameters (DIY)
- Example filenames used in this guide: `priv.pem`, `priv.p8`, `priv.p8.der`, `pub.pem`.

Correct Path (copy/paste)

```bash
# generate RSA private key (PKCS#1 PEM)
openssl genpkey -algorithm RSA -out priv.pem -pkeyopt rsa_keygen_bits:2048

# export encrypted PKCS#8 (AES-256-CBC) protected with passphrase
openssl pkcs8 -topk8 -inform PEM -outform PEM -in priv.pem -out priv.p8 -v2 aes-256-cbc -passout pass:ChangeThis

# extract public key
openssl rsa -in priv.pem -pubout -out pub.pem

# view public key
openssl pkey -in pub.pem -pubin -text -noout
```

Break Case (single-variable change)
- Export private key without encryption:

```bash
openssl pkcs8 -topk8 -inform PEM -outform PEM -in priv.pem -out priv_unencrypted.p8 -nocrypt
```

Observation
- `priv_unencrypted.p8` contains the full private key in plaintext; `grep "BEGIN PRIVATE KEY"` will show exposed material. Anyone with file access can use it.

Why
- Private keys at rest must be protected with strong encryption or stored in a protected key store (HSM/TPM/SE). Unencrypted exports trivially leak secrets.

Hard Rules
- Prefer encrypted PKCS#8 for file storage when an HSM is not available.
- Avoid exporting private keys in cleartext; never commit them to VCS.
- Use access controls and secure key stores for production keys.

Homework
- Try the commands above in an isolated directory; inspect differences between `priv.p8` and `priv_unencrypted.p8`.
