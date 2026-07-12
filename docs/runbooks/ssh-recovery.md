# Runbook: recover from broken SSH access

## Purpose

Use this runbook when SSH stops accepting the expected administrator key after a
configuration or firewall change. Do not reboot repeatedly; a bad configuration
will survive reboot.

## Required access

Use the VM hypervisor console, cloud serial console, out-of-band console, or a
provider rescue environment. If none exists, contact the infrastructure owner.
This project cannot restore a machine that has no working network path and no
console access.

## Recovery procedure

1. Log in through the console and become root:

   ```bash
   sudo -i
   id
   ```

2. Preserve evidence and inspect service state:

   ```bash
   cp -a /etc/ssh/sshd_config.d/00-ansible-hardening.conf /root/ssh-hardening.conf.failed
   systemctl status ssh --no-pager
   journalctl -u ssh -n 100 --no-pager
   sshd -t
   ufw status numbered
   ss -lntp | grep sshd
   ```

3. If `sshd -t` reports an error, temporarily remove only the managed drop-in:

   ```bash
   mv /etc/ssh/sshd_config.d/00-ansible-hardening.conf \
      /root/00-ansible-hardening.conf.disabled
   sshd -t
   systemctl restart ssh
   ```

4. If SSH is listening on the wrong port, either restore port 22 in
   `/etc/ssh/sshd_config.d/00-ansible-hardening.conf` or allow the configured port:

   ```bash
   ufw allow 22/tcp
   ufw status verbose
   ```

   If UFW itself is the suspected cause and adding the rule does not help, disable
   it only for the short recovery window:

   ```bash
   ufw disable
   ```

5. Restore the administrator key and strict permissions. Replace the placeholder
   with a trusted public key, never a private key:

   ```bash
   install -d -m 700 -o portfolio_admin -g portfolio_admin /home/portfolio_admin/.ssh
   printf '%s\n' 'ssh-ed25519 REPLACE_WITH_TRUSTED_PUBLIC_KEY operator' \
     > /home/portfolio_admin/.ssh/authorized_keys
   chown portfolio_admin:portfolio_admin /home/portfolio_admin/.ssh/authorized_keys
   chmod 600 /home/portfolio_admin/.ssh/authorized_keys
   ```

6. Verify the account, shell, and sudo membership:

   ```bash
   getent passwd portfolio_admin
   id portfolio_admin
   passwd -S portfolio_admin
   visudo -cf /etc/sudoers.d/90-portfolio_admin
   ```

7. From another terminal, test without closing the console session:

   ```bash
   ssh -vvv portfolio_admin@SERVER_ADDRESS
   sudo -n true
   ```

8. Correct inventory variables, run the bootstrap role first, and then reapply
   hardening in check mode followed by normal mode:

   ```bash
   ansible-playbook -i inventories/production/hosts.yml playbooks/bootstrap.yml
   ansible-playbook -i inventories/production/hosts.yml playbooks/site.yml \
     --check --diff --tags ssh,firewall
   ansible-playbook -i inventories/production/hosts.yml playbooks/site.yml \
     --tags ssh,firewall
   ```

9. Re-enable UFW if it was disabled and verify health:

   ```bash
   ufw enable
   ansible-playbook -i inventories/production/hosts.yml playbooks/verify.yml
   ```

## Post-incident actions

- Keep the failed configuration and relevant logs with secrets removed.
- Record the cause, detection gap, and recovery time.
- Add a test for the failure mode.
- Rotate keys if their integrity is uncertain.
- Confirm a console-access procedure exists before the next SSH change.
