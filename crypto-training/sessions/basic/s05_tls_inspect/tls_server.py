#!/usr/bin/env python3
import socket, ssl, os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime

CERT_FILE = 'server_cert.pem'
KEY_FILE = 'server_key.pem'


def ensure_cert():
    if os.path.exists(CERT_FILE) and os.path.exists(KEY_FILE):
        return
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u'localhost')])
    cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.datetime.utcnow()).not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)).add_extension(x509.SubjectAlternativeName([x509.DNSName(u'localhost')]), critical=False).sign(key, hashes.SHA256())
    with open(KEY_FILE, 'wb') as f:
        f.write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption()))
    with open(CERT_FILE, 'wb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))


if __name__ == '__main__':
    ensure_cert()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    bindsocket = socket.socket()
    bindsocket.bind(('127.0.0.1', 8443))
    bindsocket.listen(5)
    print('TLS server listening on 127.0.0.1:8443')
    while True:
        newsocket, addr = bindsocket.accept()
        try:
            ssock = context.wrap_socket(newsocket, server_side=True)
            print('Connection from', addr)
            data = ssock.recv(4096)
            if data:
                print('Received (first bytes):', data[:80])
                ssock.send(b'HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK')
            ssock.close()
        except Exception as e:
            print('TLSServer error:', e)
