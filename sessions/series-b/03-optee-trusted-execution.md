# Series B — Session 03: Trusted Execution — OP‑TEE (overview + DIY pointers)

Objective
- Describe OP‑TEE concepts, TA lifecycle, and how to bind cryptographic keys to TEE-resident objects.

Prereqs
- QEMU v8 + OP‑TEE image (you mentioned you have a local setup). This session is conceptual with actionable TODOs for local OP‑TEE testing.

Fixed checklist
- TA signing keypair (host side), TA binary, OP‑TEE TA installation path.

Correct Path (DIY steps)

1. Build a simple Trusted Application (TA) with OP‑TEE examples (use your local OP‑TEE build environment).
2. Sign the TA with the signing key and install to the OP‑TEE image.
3. From normal world, invoke the TA and exercise secure key storage APIs (SE050/TEE storage emulation depends on platform).

Break Case (single-variable change)
- Store a key in normal world and call TA functions that expect keys in TEE; demonstrate that key is not protected by TEE and can be extracted.

Observation
- Keys stored in normal world are exposed; keys provisioned into TEE are isolated from normal world processes.

Why
- TEE provides an isolated environment for sensitive code and keys, but only if the provisioning and usage patterns bind correctly to the TEE.

Hard Rules
- Provision sensitive keys into the TEE or hardware secure element; never rely on userland storage for key confidentiality.
- Validate TA signatures and ensure TA loading path is protected by the chain of trust.
- Document TEE threat model and the guarantees it does/does not provide.

Homework
- On your local QEMU OP‑TEE, build a minimal TA and exercise a protected key store operation; document steps and results.
