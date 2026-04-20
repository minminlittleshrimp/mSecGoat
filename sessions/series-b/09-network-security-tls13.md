# Series B — Session 09: Network Security — TLS 1.3 for IVI

Objective
- Apply TLS 1.3 best practices to IVI networking, including certificate verification, mutual TLS, and secure defaults.

Prereqs
- `openssl` with TLS 1.3 support.

Correct Path (copy/paste)

```bash
# Server (demo)
openssl s_server -accept 8443 -cert server.crt -key server.key -tls1_3

# Client: verify server cert, enable hostname checking
openssl s_client -connect localhost:8443 -CAfile ca.pem -verify_return_error -tls1_3

# For mutual TLS: use -cert on client side and configure server to request client certs
```

Break Case (single-variable change)
- Disable certificate verification or accept any client cert without policy checks; this allows unauthorized endpoints to connect.

Observation
- Strict certificate verification and pinning policies prevent MITM and rogue peers.

Why
- TLS provides channel security only when endpoints authenticate each other correctly and check hostnames.

Hard Rules
- Enforce certificate verification and hostname checks in all clients.
- Use mutual TLS for high-assurance control channels (e.g., provisioning, key management).
- Keep TLS libraries up to date and apply strict ciphersuite/configuration baselines.

Homework
- Configure a TLS client to require both server cert verification and host name matching; demonstrate a failed handshake with a bad cert.
