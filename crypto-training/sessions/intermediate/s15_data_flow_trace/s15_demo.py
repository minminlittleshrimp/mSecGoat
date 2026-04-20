#!/usr/bin/env python3
"""S15 — Data flow trace: instrument wrapper->engine calls to show where data and keys live."""
import logging
import base64
from wrapper import crypto_wrapper as cw
from engine import client as eclient

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("dataflow")

if __name__ == "__main__":
    data = b"trace this payload"
    log.info("app -> wrapper.sign()")
    sig = cw.sign("sign1", data)
    log.info("wrapper -> engine /sign (signature returned)")

    log.info("app -> wrapper.verify() -> wrapper fetches public key from engine")
    ok = cw.verify("sign1", data, sig)
    log.info("verify result: %s", ok)

    # Where data exists: app memory and sent to engine over HTTP; keys exist only inside engine process
    pub_pem = eclient.get_pubkey_pem('sign1')
    print('\nPublic key (from engine) length:', len(pub_pem))
    print('\nTrace complete')
