# Series B — Session 04: Key Management Lifecycle

Objective
- Cover provisioning, secure storage, rotation, and revocation for device keys across manufacturing and field operation.

Prereqs
- `softhsm2` or `tpm2-tools` are helpful for local experimentation but not required for the guideline.

Fixed lifecycle stages
- Provisioning → Storage → Use → Rotation → Revocation

Correct Path (DIY checklist)

1. Provisioning: use secure channels or blinded transfer (manufacturing HSMs, encrypted provisioning).
2. Storage: prefer TPM/SE/HSM-backed storage or use OS-protected keystores (OP‑TEE, PKCS#11/SoftHSM for lab).
3. Use: bind keys to specific operations with ACLs and TA boundaries.
4. Rotation: plan key rollover with overlap period and re-encryption strategies.
5. Revocation: support rapid revocation via CRLs, OCSP or device-level revocation counters.

Break Case (single-variable change)
- Omit rotation policy; show long-term use of one key leads to increased exposure and difficulty in incident response.

Observation
- Without rotation and revocation, compromised keys remain valid and amplify damage.

Why
- Key lifecycle management is operational; crypto primitives alone cannot mitigate poor operational practices.

Hard Rules
- Use hardware-backed key storage where possible for root keys.
- Design rotation and revocation procedures before deployment.
- Maintain auditable provisioning records and use ephemeral keys when feasible.

Homework
- Draft a provisioning and rotation workflow for your device family indicating which keys are hardware-backed.
