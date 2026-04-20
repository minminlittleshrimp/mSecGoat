Wrapper and constraints

wrapper/crypto_wrapper.py exposes a minimal safe API:
- sign(key_id, data)
- verify(key_id, data, signature)
- mac(key_id, data)
- verify_mac(key_id, data, tag)

It forbids algorithm selection, raw key input and does not fallback to local crypto.

Use wrapper/buggy_wrapper.py to see an unsafe implementation that falls back to local crypto when engine fails.