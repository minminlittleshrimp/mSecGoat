# mSecGoat — Minimal Setup Guide (Ubuntu)

Install base tools for running the DIY sessions locally (OpenSSL, Python, and optional tooling for hardware-backed experiments).

Required (minimal):

```bash
sudo apt update
sudo apt install -y openssl python3 python3-venv python3-pip
python3 -m pip install --user mkdocs mkdocs-material
```

Recommended (for advanced labs / optional):

```bash
sudo apt install -y build-essential softhsm2 tpm2-tools qemu-system-arm qemu-system-x86
```

OP‑TEE / QEMU

- If you have a local QEMU v8 OP‑TEE setup (you mentioned you do), follow your OP‑TEE build and run instructions. The sessions reference OP‑TEE conceptually and provide pointers to test locally.

Notes

- This repo is a pure Markdown guideline. The sessions include exact commands and examples you can copy/paste into an Ubuntu environment. Do not use production keys or secrets when testing.
