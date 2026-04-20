# Series B — Session 01: Threat Modeling (Automotive IVI)

Objective
- Teach lightweight threat modeling for IVI SoC: identify assets, attackers, entry points, and prioritize mitigations.

Prereqs
- Pen & paper or a simple text editor; example templates provided below.

Fixed template
- Assets: bootloader, kernel, userland daemons, keys, firmware images, user data
- Entry points: USB, Bluetooth, Wi‑Fi, CAN bus, local USB debugging, OTA
- Attackers: local attacker with physical access, remote network attacker, supply‑chain adversary

Correct Path (DIY steps)

1. List assets and map to components (e.g., Bootloader→ROM/BL2, Keys→secure storage)
2. Enumerate entry points per asset (e.g., OTA -> firmware image consumption)
3. For each asset, enumerate threats using STRIDE (S,T,R,I,D,E)
4. Assign likelihood and impact, produce a prioritized mitigation list

Break Case (single-variable change)
- Omit physical access as a threat model assumption; observe that several mitigations (secure boot, tamper detection) are deprioritized and gaps appear.

Observation
- Explicit attacker models change mitigation priorities; automotive systems must assume occasional physical access to IVI devices.

Why
- Threat modeling aligns engineering effort with realistic attacker capabilities and system exposure.

Hard Rules
- Assume worst‑practical attacker capabilities for perimeter/external interfaces.
- Map crypto usage to concrete architectural bindings (boot → signatures, OTA → signatures+TLS, logging → AEAD).
- Document assumptions and revalidate as system components change.

Homework
- Produce a one‑page threat model for your IVI architecture listing top 5 risks and mitigations.
