#!/usr/bin/env python3
"""Engine server: provides `/sign`, `/mac`, and `/pubkey/<id>` REST endpoints.
Requires `ENGINE_SECRET` env var (default `demo_engine_secret`).
"""
import os
import json
import base64
from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import serialization, hashes, hmac
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

app = Flask(__name__)
BASE = os.path.dirname(__file__)
KEY_FILE = os.path.join(BASE, "keys.enc")
_engine_keys = {}


def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390000)
    return base64.urlsafe_b64encode(kdf.derive(password))


def load_keys():
    global _engine_keys
    if not os.path.exists(KEY_FILE):
        raise RuntimeError("keys.enc missing; run engine/init_keys.py")
    with open(KEY_FILE, "r") as f:
        blob = json.load(f)
    salt = base64.b64decode(blob["salt"])
    token = blob["token"].encode()
    secret = os.environ.get("ENGINE_SECRET", "demo_engine_secret").encode()
    key = derive_key(secret, salt)
    fernet = Fernet(key)
    payload = fernet.decrypt(token)
    meta = json.loads(payload)

    _engine_keys = meta["keys"]
    # materialize binary objects
    for kid, info in _engine_keys.items():
        if info["type"] == "sign":
            priv_pem = base64.b64decode(info["private"])
            pub_pem = base64.b64decode(info["public"])
            info["private_obj"] = serialization.load_pem_private_key(priv_pem, password=None)
            info["public_obj"] = serialization.load_pem_public_key(pub_pem)
        elif info["type"] == "mac":
            info["key_bytes"] = base64.b64decode(info["key"])
    print("Engine: loaded keys:", list(_engine_keys.keys()))


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"ok": True, "keys": list(_engine_keys.keys())})


@app.route("/pubkey/<key_id>", methods=["GET"])
def pubkey(key_id):
    info = _engine_keys.get(key_id)
    if not info:
        return jsonify({"error": "unknown key"}), 404
    if info["type"] != "sign":
        return jsonify({"error": "no public key for non-sign key"}), 400
    pub_pem = info["public_obj"].public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return jsonify({"key_id": key_id, "public_pem": pub_pem.decode()})


def require_json(req):
    if not req.is_json:
        return jsonify({"error": "expected application/json"}), 400
    return None


@app.route("/sign", methods=["POST"])
def sign():
    err = require_json(request)
    if err:
        return err
    data = request.get_json()
    key_id = data.get("key_id")
    payload_b64 = data.get("data")
    if not key_id or not payload_b64:
        return jsonify({"error": "missing parameter"}), 400
    info = _engine_keys.get(key_id)
    if not info:
        return jsonify({"error": "unknown key"}), 404
    if info["type"] != "sign":
        return jsonify({"error": "key not allowed for sign"}), 400
    bs = base64.b64decode(payload_b64)
    priv = info["private_obj"]
    sig = priv.sign(bs, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
    info["usage_count"] = info.get("usage_count", 0) + 1
    return jsonify({"signature": base64.b64encode(sig).decode()})


@app.route("/mac", methods=["POST"])
def mac_route():
    err = require_json(request)
    if err:
        return err
    data = request.get_json()
    key_id = data.get("key_id")
    payload_b64 = data.get("data")
    if not key_id or not payload_b64:
        return jsonify({"error": "missing parameter"}), 400
    info = _engine_keys.get(key_id)
    if not info:
        return jsonify({"error": "unknown key"}), 404
    if info["type"] != "mac":
        return jsonify({"error": "key not allowed for mac"}), 400
    bs = base64.b64decode(payload_b64)
    h = hmac.HMAC(info["key_bytes"], hashes.SHA256())
    h.update(bs)
    tag = h.finalize()
    info["usage_count"] = info.get("usage_count", 0) + 1
    return jsonify({"tag": base64.b64encode(tag).decode()})


if __name__ == "__main__":
    load_keys()
    app.run(host="127.0.0.1", port=9001)
