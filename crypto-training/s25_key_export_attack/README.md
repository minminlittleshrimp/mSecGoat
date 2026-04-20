S25 — Key export mistake (wrapper bug)

Run:
  python3 demo.py

Broken:
- buggy wrapper accidentally includes raw_key in a request to engine and engine naively writes it to logs

Fixed:
- wrapper forbids raw_key; engine ignores/export requests and never logs raw material

Exercise: run broken demo then fixed demo to observe leak vs safe behavior.