S22 — Timing attack on HMAC verification

Run:
  python3 demo.py

Broken:
- naive byte-by-byte comparison leaks timing allowing attacker to guess HMAC

Fixed:
- use constant-time compare (hmac.compare_digest)

Exercise: observe naive_verify takes variable time; fixed_verify is constant-time.