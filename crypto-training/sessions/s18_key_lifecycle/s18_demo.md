S18 — Key lifecycle

This session guides through generate -> store -> use -> rotate -> destroy.

Use `engine/init_keys.py` to generate keys, then extend engine metadata with rotation triggers.

Exercises:
- Rotate `sign1` by generating a new key and updating engine storage safely.
- Prove that old signatures verify but old keys are unusable for signing after rotation.
