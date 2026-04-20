# Series B — Session 02: Secure Boot & Chain of Trust

Objective
- Explain secure boot concepts: measured boot, verified boot, immutable root of trust, and how to chain signatures from ROM→BL→Kernel→Userland.

Prereqs
- `openssl` for signature generation/verification examples.

Fixed parameters (demo key names)
- `bootpriv.pem`, `bootpub.pem`, `kernel.bin`, `kernel.sig`

Correct Path (copy/paste)

```bash
# Sign kernel image with a private key
openssl dgst -sha256 -sign bootpriv.pem -out kernel.sig kernel.bin

# Verify signature using public key (on device bootloader)
openssl dgst -sha256 -verify bootpub.pem -signature kernel.sig kernel.bin
```

Break Case (single-variable change)
- Skip signature verification step in the bootloader; demonstrate that modified kernel images boot unchecked.

Observation
- Without verification, chain of trust breaks and any image can be installed.

Why
- Secure boot depends on an immutable root of trust verifying each stage; skipping checks removes guarantees.

Hard Rules
- Enforce signature verification in immutable code (ROM or first-stage bootloader).
- Keep verification keys in protected storage; consider hardware-backed keys (TPM/TEE).
- Support rollback protection (monotonic counters or anti-rollback metadata).

Homework
- Sketch the chain of trust for your device and list where signatures and verification occur.
