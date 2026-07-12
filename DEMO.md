# Five-minute employer demonstration

## Prepare before the meeting

Install Vagrant and VirtualBox, clone the repository, and run `make up` once so
the box and packages are cached. Leave the VM running. Also run `make test` and
save its output only if it succeeds on your machine. Never present a check as
passing unless you personally ran it.

Open three terminals in the repository:

1. repository overview;
2. Vagrant commands;
3. VM inspection with `vagrant ssh`.

## 0:00-0:45 — explain the goal and safety boundary

Show `README.md` and its Mermaid diagram. Say:

> This project turns a fresh Ubuntu Server VM into a secure Docker host. I split
> initial access from hardening so an SSH key is proven before password access can
> be disabled. Configuration is organized into focused, reusable roles.

Show `playbooks/bootstrap.yml` and `playbooks/site.yml`. Point to `serial: 1`,
role ordering, and tags.

## 0:45-1:45 — show role design

Open these files side by side:

- `roles/ssh_hardening/defaults/main.yml`
- `roles/ssh_hardening/templates/00-ansible-hardening.conf.j2`
- `roles/ssh_hardening/handlers/main.yml`

Explain that defaults are overridable, templates are deterministic, and SSH is
validated with `sshd -t` before a reload. Briefly show the UFW, Fail2ban, Docker,
automatic updates, sysctl, and directories roles in the file tree.

## 1:45-2:45 — demonstrate idempotence

Run:

```bash
make provision
```

Talk through the recap. On a stable cached VM, the second convergence should have
no unnecessary task changes. If upstream apt metadata causes a legitimate change,
say exactly what changed; do not hide it.

Show `molecule/default/molecule.yml` and point to the explicit `idempotence` stage.

## 2:45-3:45 — inspect the configured server

Run:

```bash
vagrant ssh
id portfolio_admin
sudo sshd -t
sudo ufw status verbose
sudo fail2ban-client status sshd
docker compose version
systemctl is-active docker fail2ban ssh systemd-timesyncd
exit
```

Explain that these are live state checks, not only file existence checks.

## 3:45-4:30 — show quality automation

Show `.github/workflows/ci.yml`, `tests/test_structure.py`, and the Makefile.
Explain the layers: YAML and Ansible lint, playbook syntax, structural pytest,
Molecule convergence/idempotence/verification, and a full Vagrant VM path.

If local checks were previously successful, run `make test` only when it reliably
fits the remaining time; otherwise show the saved terminal output and state when
and where you ran it.

## 4:30-5:00 — close with operational maturity

Open `docs/runbooks/ssh-recovery.md` and `docs/explanations/vault.md`. Say:

> Automation includes failure recovery and secret-handling guidance. The example
> inventory uses reserved documentation addresses, production inventory is
> ignored, and real values belong in Vault. I also document limitations such as
> Docker's root-equivalent group and container-test boundaries.

Finish with one future improvement relevant to the employer, such as monitoring,
backup restore testing, or a cloud-specific staging pipeline.

## Cleanup after the demonstration

```bash
make down
make clean
```
