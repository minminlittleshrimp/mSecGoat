Advanced Sessions (S16–S20)
===========================

.. contents::
   :local:

S16 — OpenSSL ENGINE vs PROVIDER
--------------------------------
Follow-up hands-on:
- Read notes and attempt to load a legacy ENGINE (environment-dependent).
- Explore a PROVIDER-based example and compare integration steps.
- Document risks and migration checklist.

S17 — BoringSSL Gap
-------------------
Follow-up hands-on:
- Review BoringSSL differences and list API gaps relevant to engines.
- Attempt to port a small OpenSSL engine example and log incompatibilities.
- Summarize mitigation strategies.

S18 — Key Lifecycle
-------------------
Follow-up hands-on:
- Exercise key generate/store/use/rotate/destroy flows against engine.
- Rotate a key and attempt to verify old signatures (should fail).
- Add lifecycle metrics (usage_count, created_at) checks.

S19 — TLS Misconfiguration
--------------------------
Follow-up hands-on:
- Run demos that disable verification and prove connections succeed but insecure.
- Run testssl.sh or equivalent scanning tools if available and document warnings.
- Hardening tasks: enforce cipher suites and cert validation.

S20 — Failure Lab
-----------------
Follow-up hands-on:
- Combine failures (nonce reuse, fallback, weak RNG, wrong key usage) and observe system behavior.
- Produce a report listing all violations and propose fixes prioritized by risk.
- Implement fixes and re-run the lab to verify mitigations.

