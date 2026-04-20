# Crypto Training — Automotive IVI Embedded Security (Hands-on)

Objective
---------
Fast, hands-on training that takes learners from software crypto primitives through engine-based key isolation and real-world TLS misconfiguration labs. No long theory blocks — every session has a working demo and a broken case to illustrate the security impact.

Quick start
-----------
1. Create and activate a Python 3.10+ virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Initialize engine keys (demo secret)

```bash
# optional: override ENGINE_SECRET for stronger demo isolation
export ENGINE_SECRET=demo_engine_secret
python3 engine/init_keys.py
```

3. Run the demo runner (starts engine and runs selected sessions)

```bash
python3 labs/runner.py
```

If you want to run sessions manually, start the engine in another terminal:

```bash
export ENGINE_SECRET=demo_engine_secret
python3 engine/server.py
# then run session scripts, e.g.:
python3 sessions/s09_key_engine_basic/s09_demo.py
```

Repository layout (short)
------------------------
- `sessions/` — S01–S20 hands-on exercises (each folder contains working + broken demos)
- `engine/` — sample isolated key engine (Flask HTTP API) + key init tool
- `wrapper/` — minimal crypto wrapper that talks to the engine and enforces constraints
- `labs/` — run scripts, runner, and guided lab harnesses
- `docs/` — supporting notes and lab templates

Design principles
-----------------
- All keys are kept inside the `engine` boundary and never exported by the service.
- The `wrapper` exposes a minimal API: `sign()`, `verify()`, and `mac()` only.
- Every session includes a working case and a broken-case to illustrate failure modes.
- Keep everything runnable with a small Python stack (see `requirements.txt`).

Sessions overview
-----------------
S01–S08: primitives (hash, HMAC, AES-GCM, sign/verify, TLS inspection, RNG, KDF, BoringSSL notes)

S09–S11: engine track (key engine basics, boundary enforcement, key usage enforcement)

S12–S15: integration track (wrapper design, no-fallback rule, error handling, data flow tracing)

S16–S20: advanced (OpenSSL engine vs provider, BoringSSL gaps, key lifecycle, TLS misconfig, combined failure lab)

How to extend
-------------
- Add additional sessions under `sessions/` following the same pattern: `demo.py` (good) and `broken.py` (bad).
- Use the `engine/init_keys.py` helper to add keys and extend metadata.

License
-------
This training content is provided for internal training and demo use.

Enjoy — run the labs and break things safely.
