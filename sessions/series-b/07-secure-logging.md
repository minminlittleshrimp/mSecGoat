# Series B — Session 07: Secure Logging (Integrity, Authenticity, Confidentiality)

Objective
- Define a logging pipeline that preserves integrity and confidentiality of sensitive events while enabling forensic analysis.

Prereqs
- `openssl` for signature examples and `python3` for AEAD examples if desired.

Correct Path (guideline)

1. Per-record AEAD: encrypt sensitive payloads with AEAD; include record metadata as associated data (timestamp, component ID, seq).
2. Record integrity: compute a per-record MAC or signature covering header+ciphertext; store signature in log entry.
3. Append-only storage: protect log storage against truncation (append-only files, remote immutable storage).

Example entry layout (textual)

```
timestamp | component | seq | nonce | aead_ct_hex | tag_hex | sig_hex
```

Break Case (single-variable change)
- Omit the tag or signature: an attacker modifies log files to hide actions; integrity checks fail to detect tampering.

Observation
- Logs without authenticated envelopes can be silently altered; secure logging must detect tampering and ensure availability.

Why
- Logs are critical forensic artifacts; their integrity is essential for incident response and liability.

Hard Rules
- Encrypt sensitive fields with AEAD and include metadata in AD.
- Sign or MAC log batches with a key protected in TEE/HSM.
- Implement retention and secure transport to remote immutable collectors.

Homework
- Draft a minimal log record schema for your IVI system and show how to verify a record offline using `openssl dgst` or an HMAC check.
