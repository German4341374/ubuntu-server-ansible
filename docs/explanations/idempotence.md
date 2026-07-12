# Idempotence and testing

Idempotence means a second run against unchanged inputs should report no state
changes. Roles use declarative modules, stable templates, cache windows, and
handlers that run only after notifications.

The test pyramid is:

1. pytest checks required files, YAML parsing, and safe example addresses.
2. yamllint and ansible-lint enforce formatting and Ansible practices.
3. syntax checks parse each public playbook with installed collections.
4. Molecule converges twice and fails its idempotence stage on unexpected changes.
5. Vagrant exercises a full Ubuntu VM and supports manual health verification.

Some package metadata and upstream repositories can legitimately change between
runs. Pin application versions in production inventory when deterministic rollout
is more important than automatically receiving the latest package release.
