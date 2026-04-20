S26 — Secure boot simulation (signed firmware)

Run:
  python3 demo.py

Broken:
- bootloader that accepts unsigned firmware or skips signature check

Fixed:
- verify signature before accepting firmware image

Exercise: run broken demo to see insecure acceptance; run fixed demo to verify signature enforcement.