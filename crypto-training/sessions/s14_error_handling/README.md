S14 — Error handling

Demos show propagation of errors when key_id is invalid or signature corrupted. The wrapper must not swallow errors; it should abort and surface the cause.