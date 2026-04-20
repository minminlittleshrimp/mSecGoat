S07 — KDFs (PBKDF2, HKDF)

Run:
  python3 kdf_demo.py

Working:
- Derive keys from passwords (PBKDF2) and extract/expand (HKDF)

Broken case:
- Low iteration count or fixed salt

What broke / why: weak KDF parameters reduce entropy of derived keys.