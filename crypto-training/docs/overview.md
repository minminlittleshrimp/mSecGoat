Overview

This training repository provides short runnable demos focused on secure use of crypto in embedded IVI systems.

Structure
- sessions/: hands-on exercises S01..S20 (each has a README and a runnable demo)
- engine/: a standalone key engine (simulates hardware/TEE boundary)
- wrapper/: safe and intentionally-broken wrappers that call the engine
- labs/: helper scripts to run many sessions end-to-end

Goal: make engineers capable of using OpenSSL/BoringSSL at a safe surface and recognise common integration mistakes.