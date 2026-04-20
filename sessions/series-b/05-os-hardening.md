# Series B — Session 05: OS Hardening (Isolation & Privilege Boundaries)

Objective
- Provide practical steps to harden Linux/Android-based IVI stacks: minimize privileges, enforce isolation, and reduce attack surface.

Prereqs
- Basic familiarity with Linux namespaces, systemd, and kernel hardening knobs.

Correct Path (items to apply)

- Minimize installed packages; remove debug tools from production images.
- Run services with least privilege (dedicated accounts, capability drops).
- Use seccomp filters, SELinux/AppArmor policies, and user namespaces where appropriate.
- Enable kernel mitigations: ASLR, SMEP/SMAP (if supported), stack canaries, FORTIFY_SOURCE.

Break Case (single-variable change)
- Run a network-exposed service as root; demonstrate that a single vulnerability leads to full system compromise.

Observation
- Privilege separation reduces blast radius; running as root increases impact surface drastically.

Why
- Isolation and least privilege make exploitation chaining more difficult and raise required attacker effort.

Hard Rules
- Run services unprivileged; use namespaces and cgroups for resource control.
- Apply in-depth defense (multiple layers): compile-time, OS-level, and runtime mitigations.
- Regularly audit installed packages and reduce image size for production builds.

Homework
- For one IVI service, document the minimal set of privileges required and create a seccomp profile (or AppArmor/SELinux rule) restricting syscalls.
