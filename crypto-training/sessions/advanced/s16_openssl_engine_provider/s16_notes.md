S16 — OpenSSL ENGINE vs PROVIDER

This session is a guided lab; not every environment has legacy ENGINE support.

Steps:
1. On a system with `openssl` installed, run `openssl engine -t -c` to list engines.
2. Compare with provider model via OpenSSL 3.x docs and `openssl providers -v` if available.

Goal: understand deprecation risk when migrating from ENGINEs to PROVIDER APIs.
