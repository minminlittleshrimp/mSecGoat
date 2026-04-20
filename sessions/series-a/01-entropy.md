# Series A — Session 01: Entropy & Randomness Discipline

Objective
- Demonstrate why low-entropy keys/seed lead to trivial compromise and how to verify entropy discipline in reproducible labs.

Prereqs
- Ubuntu + `openssl` and `python3` (see repository README for install lines).

Fixed parameters (reproducible fixtures)
- Good key: `keys/fixtures/session01_good_key.hex` (32-byte hex)
- Weak seed: `keys/fixtures/session01_weak_seed.hex` (2-byte hex seed; expanded to 32 bytes by repeating)
- Plaintext: `labs/sessionA01/plaintext.txt`

Correct Path (deterministic demo)
- Compute an HMAC (SHA-256) using the good key and show brute-force over a tiny seed-space fails.

Commands (copy/paste):

```bash
cd labs/sessionA01
bash run_correct.sh
```

Break Case (single-variable change)
- Replace the good key with a weak key (single variable: key source). Run the break script which uses a small entropy seed and shows the key recovered by brute-force.

Commands (copy/paste):

```bash
cd labs/sessionA01
bash run_break.sh
```

Expected Observations
- Correct path: HMAC produced; brute-force script prints `NOTFOUND` (seed-space search does not match the good key pattern).
- Break case: break HMAC produced; brute-force script prints `FOUND:0x1a2b` (the weak seed used by the demo).

Why
- When key material is drawn from a tiny entropy space, an attacker can enumerate possibilities and recover the key quickly. Proper entropy increases brute-force cost exponentially.

Hard Rules
- Always use full-entropy keys for cryptographic keys.
- When demonstrating randomness, publish and pin fixtures for reproducibility, but document that real deployments must use OS CSPRNG.
- Validate entropy assumptions: small seed → possible brute-force.

Files and scripts
- labs/sessionA01/compute_hmac.py  — deterministic HMAC generator
- labs/sessionA01/bruteforce_find_key.py — enumerates 2^16 seed-space and reports FOUND/NOTFOUND
- labs/sessionA01/run_correct.sh — runs the correct demo
- labs/sessionA01/run_break.sh — runs the break demo (weak seed)
