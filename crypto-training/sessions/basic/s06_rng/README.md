S06 — RNG

Run:
  python3 rng_demo.py

Working:
- Uses os.urandom for cryptographic randomness

Broken case:
- Using random.seed(0) produces predictable values

What broke / why: predictable RNG breaks keys/nonces.