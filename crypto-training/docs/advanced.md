# Advanced notes (S16–S20)

S16 — OpenSSL ENGINE vs Provider
- Use `openssl engine -t -c` to inspect legacy ENGINEs (if available)
- Modern OpenSSL uses the Provider model; ENGINE APIs are deprecated and may be absent in new builds

S17 — BoringSSL gap
- BoringSSL intentionally removes compatibility layers and some high-level APIs
- Vendor binary behavior may differ; do not assume API parity

S18 — Key lifecycle
- Demonstrate generation, rotation, usage counters, and destroy semantics in the engine

S19 — TLS misconfiguration
- Use testssl.sh or manual `openssl s_client` to prove misconfiguring ciphers and verification makes connections insecure

S20 — Combined failure lab
- Combine nonce reuse, weak RNG, fallback, and misconfigured TLS to show systems that "work" but are insecure
