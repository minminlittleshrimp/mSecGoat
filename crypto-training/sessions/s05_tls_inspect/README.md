S05 — TLS inspect

Run TLS server:
  python3 tls_server.py

Then in another shell run:
  openssl s_client -connect 127.0.0.1:8443

Server generates a self-signed cert on first run. Use openssl to inspect the handshake and cert chain.

Broken case: disable cert verification on client -> connection still succeeds but is insecure.