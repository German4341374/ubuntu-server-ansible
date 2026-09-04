# Design notes

## 1. Why use Ansible roles instead of one playbook?

Roles isolate concerns, expose documented defaults, and give tasks, templates,
and handlers a predictable home. A reviewer can change SSH without reading the
Docker implementation, and tags make focused operations possible.

## 2. Why are bootstrap and site configuration separate?

SSH hardening can remove the access method used for provisioning. Bootstrap only
creates the non-root account and installs its public keys. The operator verifies
a second key-based session before applying password or root-login restrictions.

## 3. What makes the project idempotent?

It uses declarative modules with explicit desired state, deterministic templates,
an apt cache validity window, and handlers triggered only by changed files.
Molecule runs a second convergence and treats unexpected changes as a failure.

## 4. Why keep password authentication configurable?

Key-only SSH is the secure default, but a staged migration may temporarily need
password authentication. Making the control explicit supports a safe transition
without editing role logic.

## 5. How does the SSH handler reduce lockout risk?

The handler runs `sshd -t` before reloading the service. If validation fails,
Ansible stops and does not execute the later reload handler. The operator should
also keep an existing session and console recovery access open.

## 6. Why use an sshd drop-in?

A drop-in owns only project policy and leaves the distribution's main file and
package updates intact. It is easy to identify, remove during recovery, and render
deterministically.

## 7. Why is root login not disabled by default?

It defaults to `prohibit-password`, allowing a trusted root key as a temporary
recovery path while blocking root passwords. After non-root access and console
recovery are verified, production can set it to `no`.

## 8. How does UFW configuration avoid an immediate lockout?

Required TCP rules and the rate-limited SSH rule are created before UFW is
enabled. The site play applies one host at a time, limiting blast radius.

## 9. What does Fail2ban add when passwords are disabled?

It reduces noisy scans and repeated key or account attacks, protects transitional
password-enabled deployments, and provides useful ban telemetry. It complements
authentication policy; it does not replace strong keys and firewall rules.

## 10. Why use Docker's official apt repository?

Ubuntu's repository may lag Docker Engine and Compose plugin releases. The role
installs Docker's signing key into a scoped keyring and uses `signed-by`, avoiding
the deprecated global `apt-key` trust model.

## 11. Is membership in the Docker group least privilege?

No. Docker group access is effectively root-equivalent because a user can mount
the host filesystem in a container. The project limits membership to the named
administrator and documents the exception. Rootless Docker would be a future
option for workloads that support it.

## 12. Why configure Docker log limits?

The default JSON log driver can consume the disk indefinitely. Size and file-count
limits bound this failure mode while leaving application-specific logging open for
future centralized collection.

## 13. Why use systemd-timesyncd rather than installing chrony?

For a general VM baseline, timesyncd is already integrated with Ubuntu and has a
small operational footprint. Chrony would be preferable for strict accuracy,
unstable links, or specialized NTP server requirements.

## 14. How are automatic updates balanced against availability?

Security origins are enabled, but automatic reboots default to false. This closes
many exposure windows without allowing an unmanaged reboot. Production should add
maintenance windows, staged rollout, and reboot monitoring.

## 15. Why are the sysctl settings called safe rather than comprehensive?

They disable redirects and source routing, enable spoofing resistance, and protect
kernel information without aggressive tuning that could break containers,
forwarding, or application performance. A benchmark must be adapted to the host's
role rather than copied blindly.

## 16. What is the purpose of Ansible Vault here?

Vault encrypts sensitive variables stored in the repository. The vault password
stays outside the repository. Vault does not protect secrets after decryption,
Ansible output, backups, or compromised operator machines.

## 17. Why does the example inventory use 192.0.2.0 and 198.51.100.0 ranges?

RFC 5737 reserves those networks for documentation, so examples cannot
accidentally target a real public server. Production inventory is gitignored.

## 18. What does check mode prove?

It previews many changes and catches variable or templating problems, but not all
modules can fully simulate state. It does not prove SSH remains reachable or that
services start. That is why the project also uses Molecule, Vagrant, and explicit
health checks.

## 19. Why test with both Molecule and Vagrant?

Molecule containers are fast and practical in CI, including a second convergence.
Vagrant gives a real Ubuntu kernel boundary, boot sequence, SSH service, and
network stack. The two methods catch different failures.

## 20. What are the risks of privileged Molecule containers?

Privileged containers weaken isolation and should run only on trusted CI workers
with untrusted pull-request execution controlled. They approximate systemd but are
not a security boundary or a replacement for VM testing.

## 21. Why use handlers?

Handlers coalesce repeated notifications and restart or reload a service only when
its configuration changed. This avoids needless disruption and supports
idempotence.

## 22. How do tags help operations?

Tags allow a narrow preview or deployment, such as `--tags ssh,firewall`, reducing
change scope. Operators must still understand role dependencies; a full baseline
run remains the authoritative reconciliation.

## 23. How would you roll this out to many hosts?

Start with a disposable VM, then a staging host, then a small canary group. Keep
`serial: 1` for access changes, run health verification after each batch, retain
console access, and expand batches only after stable observation.

## 24. How would you recover from an SSH lockout?

Use the provider or hypervisor console, inspect `sshd -t`, service logs, listening
ports, UFW rules, account state, and key permissions. Temporarily remove the
managed drop-in or disable UFW only as needed, prove access from a second terminal,
correct variables, and reapply. The repository contains a command-by-command
runbook.

## 25. What would you improve first for real production use?

Add environment-specific monitoring and alerting, tested backup and restore jobs,
a staged reboot workflow, cloud firewall reconciliation, immutable Molecule image
digests, dependency automation, and ephemeral staging tests.

## 26. Why not pin every apt package version?

Exact pins improve repeatability but can delay security updates and differ across
Ubuntu releases. This baseline pins development tooling and repository sources
while allowing current host packages. Strict environments should publish an
approved package snapshot and pass version variables through inventory.

## 27. How does the project limit secret exposure in logs?

The authorized-key task uses `no_log`, production inventory is ignored, and Vault
instructions keep the password external. CI should also restrict logs and secret
access. Public keys are not secret, but production identifiers still deserve care.

## 28. What limitation exists between UFW and Docker?

Docker adds netfilter rules for published ports, and those paths can bypass the
simple mental model of UFW's INPUT policy. Production must review the DOCKER-USER
chain and explicitly test container ingress policy.
