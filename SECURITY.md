# Security Policy

## Supported scope

The current project targets Ubuntu Server 22.04 and 24.04 on x86_64 and ARM64.
Security fixes are prioritized for the latest revision on the `main` branch.

## Reporting a vulnerability

Do not open a public issue containing exploit details, credentials, hostnames, or
IP addresses. Use the repository host's private security advisory feature. If no
private channel exists, contact the repository owner privately and provide a
minimal reproduction with secrets removed.

## Secret handling

- Store secret variables in an Ansible Vault-encrypted file.
- Keep the vault password outside this repository.
- Never commit private SSH keys; only public keys belong in inventory variables.
- Review `git diff --staged` before every commit.
- Rotate a secret immediately if it is accidentally exposed; removing it from a
  later commit is not sufficient.

## Operational warning

SSH and firewall changes can lock out an operator. Bootstrap and test the new
account in a second session before disabling passwords or root access. Keep
provider console access available and follow `docs/runbooks/ssh-recovery.md`.
