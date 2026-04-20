#!/usr/bin/env python3
"""Simple standalone key engine HTTP server.

- Run as a separate process: python engine/engine_server.py
- Provides JSON POST endpoints: /load_key, /sign, /verify, /mac, /verify_mac, /meta, /rotate

The engine keeps keys in-memory and never exposes raw key material.
"""
import json, base64, time, os, signal
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives import serialization

HOST = '127.0.0.1'
PORT = 9000

KEY_STORE = {}


def now_ts():
    return int(time.time())


def make_default_keys():
    # Create one signing RSA and one MAC key
    sign_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    mac_key = os.urandom(32)
    KEY_STORE['sign-key'] = {'type': 'sign', 'key': sign_key, 'created_at': now_ts(), 'usage_count': 0, 'usage_limit': 1000000}
    KEY_STORE['mac-key'] = {'type': 'mac', 'key': mac_key, 'created_at': now_ts(), 'usage_count': 0, 'usage_limit': 1000000}


class EngineHandler(BaseHTTPRequestHandler):
    def _read_json(self):
        clen = int(self.headers.get('Content-Length', '0'))
        raw = self.rfile.read(clen) if clen else b''
        if not raw:
            return {}
        return json.loads(raw.decode())

    def _respond(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_POST(self):
        try:
            req = self._read_json()
            path = urlparse(self.path).path
            # Simulate failure when client sets simulate_fail true
            if req.get('simulate_fail'):
                self._respond(500, {'status': 'error', 'message': 'simulated failure'})
                return

            if path == '/load_key':
                key_id = req['key_id']
                ktype = req.get('type', 'mac')
                usage_limit = req.get('usage_limit')
                if ktype == 'sign':
                    k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
                else:
                    k = os.urandom(32)
                KEY_STORE[key_id] = {'type': ktype, 'key': k, 'created_at': now_ts(), 'usage_count': 0, 'usage_limit': usage_limit}
                self._respond(200, {'status': 'ok', 'result': {'key_id': key_id}})
                return

            if path == '/sign':
                key_id = req['key_id']
                data = base64.b64decode(req['data'])
                meta = KEY_STORE.get(key_id)
                if not meta:
                    self._respond(400, {'status': 'error', 'message': 'unknown key_id'})
                    return
                if meta['type'] != 'sign':
                    self._respond(400, {'status': 'error', 'message': 'key not permitted for sign'})
                    return
                priv = meta['key']
                sig = priv.sign(data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
                meta['usage_count'] += 1
                self._respond(200, {'status': 'ok', 'result': {'signature': base64.b64encode(sig).decode()}})
                return

            if path == '/verify':
                key_id = req['key_id']
                data = base64.b64decode(req['data'])
                sig = base64.b64decode(req['signature'])
                meta = KEY_STORE.get(key_id)
                if not meta:
                    self._respond(400, {'status': 'error', 'message': 'unknown key_id'})
                    return
                if meta['type'] != 'sign':
                    self._respond(400, {'status': 'error', 'message': 'key not permitted for verify'})
                    return
                pub = meta['key'].public_key()
                try:
                    pub.verify(sig, data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
                    self._respond(200, {'status': 'ok', 'result': {'valid': True}})
                except Exception:
                    self._respond(200, {'status': 'ok', 'result': {'valid': False}})
                return

            if path == '/mac':
                key_id = req['key_id']
                data = base64.b64decode(req['data'])
                meta = KEY_STORE.get(key_id)
                if not meta:
                    self._respond(400, {'status': 'error', 'message': 'unknown key_id'})
                    return
                if meta['type'] != 'mac':
                    self._respond(400, {'status': 'error', 'message': 'key not permitted for mac'})
                    return
                k = meta['key']
                h = hmac.HMAC(k, hashes.SHA256())
                h.update(data)
                tag = h.finalize()
                meta['usage_count'] += 1
                self._respond(200, {'status': 'ok', 'result': {'tag': base64.b64encode(tag).decode()}})
                return

            if path == '/verify_mac':
                key_id = req['key_id']
                data = base64.b64decode(req['data'])
                tag = base64.b64decode(req['tag'])
                meta = KEY_STORE.get(key_id)
                if not meta:
                    self._respond(400, {'status': 'error', 'message': 'unknown key_id'})
                    return
                if meta['type'] != 'mac':
                    self._respond(400, {'status': 'error', 'message': 'key not permitted for mac verify'})
                    return
                k = meta['key']
                h = hmac.HMAC(k, hashes.SHA256())
                h.update(data)
                try:
                    h.verify(tag)
                    self._respond(200, {'status': 'ok', 'result': {'valid': True}})
                except Exception:
                    self._respond(200, {'status': 'ok', 'result': {'valid': False}})
                return

            if path == '/meta':
                key_id = req.get('key_id')
                if key_id:
                    meta = KEY_STORE.get(key_id)
                    if not meta:
                        self._respond(400, {'status': 'error', 'message': 'unknown key_id'})
                        return
                    # Do not expose raw key material
                    info = {'type': meta['type'], 'created_at': meta['created_at'], 'usage_count': meta['usage_count']}
                    self._respond(200, {'status': 'ok', 'result': info})
                else:
                    info = {k: {'type': v['type'], 'created_at': v['created_at'], 'usage_count': v['usage_count']} for k, v in KEY_STORE.items()}
                    self._respond(200, {'status': 'ok', 'result': info})
                return

            if path == '/rotate':
                key_id = req['key_id']
                meta = KEY_STORE.get(key_id)
                if not meta:
                    self._respond(400, {'status': 'error', 'message': 'unknown key_id'})
                    return
                if meta['type'] == 'sign':
                    meta['key'] = rsa.generate_private_key(public_exponent=65537, key_size=2048)
                else:
                    meta['key'] = os.urandom(32)
                meta['created_at'] = now_ts()
                meta['usage_count'] = 0
                self._respond(200, {'status': 'ok', 'result': {'key_id': key_id}})
                return

            self._respond(404, {'status': 'error', 'message': 'unknown endpoint'})
        except Exception as e:
            self._respond(500, {'status': 'error', 'message': str(e)})


def run_server():
    print('Engine starting with default keys...')
    make_default_keys()
    server = HTTPServer((HOST, PORT), EngineHandler)
    def _sigint(signum, frame):
        print('Engine shutting down')
        server.shutdown()
    signal.signal(signal.SIGINT, _sigint)
    server.serve_forever()


if __name__ == '__main__':
    run_server()
