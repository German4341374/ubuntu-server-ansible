# Ansible Vault workflow

Vault encrypts variables at rest; it does not replace access control or secret
rotation. Public SSH keys are not secrets, but keeping production access data in
the encrypted file reduces accidental disclosure.

Create an ignored production inventory and vault password file:

```bash
mkdir -p inventories/production/group_vars
cp inventories/example/hosts.yml inventories/production/hosts.yml
printf '%s' 'use-a-random-value-from-your-password-manager' > ~/.ansible-vault-pass
chmod 600 ~/.ansible-vault-pass
ansible-vault create \
  --vault-password-file ~/.ansible-vault-pass \
  inventories/production/group_vars/vault.yml
```

Example encrypted file content before encryption:

```yaml
---
admin_authorized_keys:
  - "ssh-ed25519 REPLACE_WITH_YOUR_PUBLIC_KEY operator"
```

Run with the external password file:

```bash
ansible-playbook -i inventories/production/hosts.yml \
  --vault-password-file ~/.ansible-vault-pass playbooks/bootstrap.yml
```

Never use the example password text above, never commit the password file, and
confirm encryption with `head inventories/production/group_vars/vault.yml`—the
first line should begin with `$ANSIBLE_VAULT`.
