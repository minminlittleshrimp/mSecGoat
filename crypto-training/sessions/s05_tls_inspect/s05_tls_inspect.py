#!/usr/bin/env python3
"""S05 — TLS inspect demo: start a local self-signed TLS server and connect.
Demonstrates secure client verification vs disabled verification (broken case).
"""
import socket
import ssl
import threading
import tempfile
import os
import time
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

HOST = '127.0.0.1'
PORT = 8443


def make_self_signed_cert(cert_path, key_path):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Demo"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=10))
        .add_extension(x509.SubjectAlternativeName([x509.DNSName(u"localhost")]), critical=False)
        .sign(key, hashes.SHA256())
    )
    with open(key_path, "wb") as f:
        f.write(key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption()))
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))


def tls_server(certfile, keyfile, stop_event):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    bindsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bindsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bindsock.bind((HOST, PORT))
    bindsock.listen(5)
    print("TLS server listening on {}:{}".format(HOST, PORT))
    while not stop_event.is_set():
        try:
            newsock, addr = bindsock.accept()
            ssock = context.wrap_socket(newsock, server_side=True)
            data = ssock.recv(1024)
            ssock.send(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK")
            ssock.close()
        except Exception:
            pass
    bindsock.close()


if __name__ == "__main__":
    tmpdir = tempfile.mkdtemp(prefix="tls_demo_")
    certfile = os.path.join(tmpdir, "cert.pem")
    keyfile = os.path.join(tmpdir, "key.pem")
    make_self_signed_cert(certfile, keyfile)

    stop_event = threading.Event()
    t = threading.Thread(target=tls_server, args=(certfile, keyfile, stop_event), daemon=True)
    t.start()
    time.sleep(0.5)

    # Good case: verify server certificate (trusted root) — for demo we will trust our generated cert
    print("\nGood case: client verifies server certificate (explicitly trusting cert)")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.load_verify_locations(cafile=certfile)
    with ctx.wrap_socket(socket.socket(), server_hostname='localhost') as s:
        s.connect((HOST, PORT))
        s.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        print(s.recv(1024))

    # Broken case: client disables certificate verification
    print("\nBroken case: client disables verification (INSECURE)")
    ctx2 = ssl._create_unverified_context()
    with ctx2.wrap_socket(socket.socket(), server_hostname='localhost') as s2:
        s2.connect((HOST, PORT))
        s2.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        print(s2.recv(1024))

    # Stop server
    stop_event.set()
    t.join(timeout=1)
    print("done")
