S10 — Key Engine Boundary

Goal: engine must run as a separate process and not be importable as a library. The engine package raises on import; run as a script.

Run:
  python3 demo.py

Broken test: attempt to import engine package (should fail). Then start engine as a process and show wrapper works.