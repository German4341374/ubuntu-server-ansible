# Agent Guidelines

## Scope

This repository manages Ubuntu servers. Treat SSH, firewall, sudo, kernel, and
package repository changes as high risk.

## Working rules

- Use English in code, comments, documentation, configuration, and commits.
- Never add credentials, private keys, vault passwords, production inventories,
  or personal data.
- Keep tasks idempotent and prefer Ansible modules over shell commands.
- Preserve the two-stage bootstrap and hardening safety boundary.
- Add variables to role defaults and document security-sensitive settings.
- Notify handlers only when configuration changes.
- Run `make lint` and `make test` before proposing a change.
- Run `make molecule` for changes that affect target state when Docker is available.
- Do not weaken a security default merely to make a container test pass.
- Update the SSH recovery runbook when changing SSH, UFW, or administrator access.

## Commit style

Use short imperative English messages, for example:

```text
Harden OpenSSH with a validated drop-in
```
