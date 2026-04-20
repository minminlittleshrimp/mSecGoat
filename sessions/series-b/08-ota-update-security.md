# Series B — Session 08: OTA / Update Security (Signing & Rollback Protection)

Objective
- Show secure OTA concepts: signed images, verification, staged updates, and anti-rollback measures.

Prereqs
- `openssl` for signing examples; no special hardware required for the guideline.

Fixed parameters (demo)
- `image.bin`, `image.sig`, `vendor_pub.pem`

Correct Path (copy/paste)

```bash
# Sign image
openssl dgst -sha256 -sign vendor_priv.pem -out image.sig image.bin

# On device: verify signature
openssl dgst -sha256 -verify vendor_pub.pem -signature image.sig image.bin
```

Rollforward & rollback protection
- Include a monotonically increasing version/counter inside signed metadata and store device-side monotonic counter in TPM/secure storage. Reject images with version <= stored counter.

Break Case (single-variable change)
- Omit the version check; an attacker can install an older vulnerable image (rollback) even if signatures are valid.

Observation
- Signatures alone protect authenticity but not freshness; anti-rollback requires stored state or counters.

Why
- Secure OTA requires authenticity, integrity, and freshness guarantees — signatures + monotonic state.

Hard Rules
- Sign images with vendor keys and verify chain of trust on device.
- Enforce anti-rollback via secure monotonic counters or version seals.
- Stage updates and provide fallback mechanisms in case of failure.

Homework
- Design an OTA update flow for your device including signing, verification, staging, and rollback protection components.
