# Series B — Session 06: IPC & Middleware Security (Auth, Integrity, Replay)

Objective
- Explain how to secure IPC channels and middleware in IVI stacks: authenticated encryption, replay protection, and per‑message binding.

Prereqs
- Familiarity with the IPC mechanisms used (dbus, sockets, binder, custom RPC).

Correct Path (pattern)

1. Use AEAD for message confidentiality and integrity (per-message nonce derived from monotonic counter + connection ID).
2. Include sequence numbers or nonces inside associated data and maintain per-peer state to prevent replays.
3. Authenticate peers (mutual TLS, token exchange via TEE, or authenticated IPC frameworks).

Break Case (single-variable change)
- Remove sequence numbers from messages; attacker replays previously captured messages and triggers unauthorized actions.

Observation
- Without replay protection, valid messages can be reused to cause state changes.

Why
- IPC channels are often trusted implicitly; cryptographic bindings and authentication are required to preserve invariants.

Hard Rules
- Bind each IPC channel to authentication and encrypt messages with AEAD.
- Include and verify monotonic counters or timestamps for replay protection.
- Fail closed: reject messages with missing/invalid authentication metadata.

Homework
- Design an IPC message envelope schema containing AEAD ciphertext, AD (sender ID, seq), and verification rules.
