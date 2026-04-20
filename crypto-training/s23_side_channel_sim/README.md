S23 — Side-channel (leak simulation)

Run:
  python3 demo.py

Broken:
- secret-dependent branching leaks information (printed trace)

Fixed:
- constant-time operations and avoid secret-dependent control flow

Exercise: compare execution traces and see how branches reveal secret bits.