S15 — Data flow trace

Trace: app -> wrapper -> engine -> crypto -> response

Run demo and watch logs on wrapper and engine to see where data and keys live. The wrapper logs remote calls; the engine logs metadata but never exports raw keys.