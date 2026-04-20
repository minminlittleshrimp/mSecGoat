S24 — HSM / key export policy

Run:
  python3 demo.py

Broken:
- naive HSM mock that allows exporting raw key material

Fixed:
- proper policy: engine rejects export requests; wrapper must never request raw keys

Exercise: attempt export (broken) and observe rejection (fixed).