# Series A — Session 10: Transport Security — TLS 1.3

Objective
- Cover TLS 1.3 basics, certificate verification, and how to validate a TLS stack using OpenSSL `s_server`/`s_client`.

Prereqs
- `openssl` (supporting TLS 1.3) on Ubuntu.

Fixed parameters (demo certs)
- `server.crt`, `server.key`, `ca.pem` (self‑signed CA for demo). Use distinct test certs — never use production certs.

Correct Path (copy/paste)

```bash
# Run a TLS1.3 test server
openssl s_server -accept 4433 -cert server.crt -key server.key -www -tls1_3

# Connect with client and verify server certificate with CA
openssl s_client -connect localhost:4433 -verify_hostname localhost -verify_return_error -CAfile ca.pem -tls1_3
```

Break Case (single-variable change)
- Disable certificate verification on the client (`-verify_return_error` omitted), demonstrating MITM possibility with forged certs.

Observation
- With verification disabled the client accepts any cert; with verification enabled, a mismatched or untrusted cert is rejected.

Why
- TLS provides confidentiality + integrity when endpoints verify certificates; skipping verification turns TLS into unauthenticated encryption.

Hard Rules
- Always verify peer certificates and hostnames in client code.
- Use TLS 1.3 where possible; prefer library-managed TLS stacks for correct defaults.
- Disable deprecated protocols and ciphersuites in server configurations.

Homework
- Configure a minimal server with valid cert chain and demonstrate failed/successful verifications.
