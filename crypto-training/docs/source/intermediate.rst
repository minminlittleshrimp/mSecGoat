Intermediate Sessions (S09–S15, S21–S26)
=======================================

.. contents::
   :local:

S09 — Key Engine (Basic)
------------------------
Follow-up hands-on:
- Start the engine process and interact via HTTP client.
- Attempt to request raw key material and observe rejection.
- Add key metadata queries and assert no raw key leakage.

S10 — Key Engine Boundary
-------------------------
Follow-up hands-on:
- Attempt to import the engine package (should fail by design).
- Run engine as separate process and prove wrapper calls succeed.
- Simulate direct library link attempts and discuss mitigations.

S11 — Key Usage Enforcement
---------------------------
Follow-up hands-on:
- Use sign-key for MAC and verify engine rejects misuse.
- Add a policy table to engine metadata and show enforcement.
- Implement a usage limit and trigger rotation when exceeded.

S12 — Wrapper Design
---------------------
Follow-up hands-on:
- Inspect wrapper/crypto_wrapper.py and ensure algorithm selection is forbidden.
- Attempt to inject an algorithm parameter and confirm exception.
- Write a simple app that only exposes sign/verify/mac via wrapper.

S13 — No-fallback rule
----------------------
Follow-up hands-on:
- Compare wrapper/crypto_wrapper.py (safe) vs wrapper/buggy_wrapper.py (broken).
- Force engine failure and show buggy wrapper silently falls back; fix the wrapper.
- Add tests that fail if any fallback path is executed.

S14 — Error Handling
--------------------
Follow-up hands-on:
- Feed invalid key_id and ensure wrapper surfaces the engine error.
- Corrupt signatures and assert verification returns False (not ignored).
- Add a CI test that asserts errors are not swallowed.

S15 — Data Flow Trace
---------------------
Follow-up hands-on:
- Trace logs through app -> wrapper -> engine for a sample operation.
- Mark where plaintext data is present and where keys are stored.
- Create a checklist for trust boundary reviews.

S21 — Padding Oracle
---------------------
Follow-up hands-on:
- Run the broken PKCS#1v1.5 code and observe explicit padding errors.
- Replace with OAEP and show oracle is closed.
- Implement a constant-time error response strategy.

S22 — Timing Attack
-------------------
Follow-up hands-on:
- Run naive vs fixed HMAC verification and measure timing variance.
- Use repeated measurements to illustrate leak over many samples.
- Replace naive compare with hmac.compare_digest in code.

S23 — Side-channel Simulation
-----------------------------
Follow-up hands-on:
- Observe broken branch traces and produce a leakage report.
- Refactor secret-dependent code to constant-time equivalents.
- Add tests to detect secret-dependent print/log outputs.

S24 — HSM / Key Export Policy
-----------------------------
Follow-up hands-on:
- Attempt to export keys from engine; show engine rejects export.
- Validate that wrapper never calls an export endpoint.
- Discuss storage policies and least-privilege rules for HSM keys.

S25 — Key Export Attack
-----------------------
Follow-up hands-on:
- Run the broken wrapper demo that attempts raw_key in request (simulate attack).
- Fix wrapper to disallow raw_key and validate engine logs show no leakage.
- Add unit tests that assert requests do not contain forbidden fields.

S26 — Secure Boot Simulation
---------------------------
Follow-up hands-on:
- Run broken bootloader that accepts unsigned firmware (observe insecure acceptance).
- Implement signature verification and show rejection on tampering.
- Add an automated digest check for firmware integrity.

