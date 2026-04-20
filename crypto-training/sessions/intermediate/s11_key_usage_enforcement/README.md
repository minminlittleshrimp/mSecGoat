S11 — Key Usage Enforcement

The engine enforces key usage policies: SIGN keys can only sign, MAC keys can only MAC. Broken case: try to use sign-key for MAC and expect rejection.

Run:
  python3 demo.py
