# Contributing

Thank you for improving the project. Open an issue for behavior changes and keep
pull requests focused.

## Development workflow

1. Create a branch from `main`.
2. Install the local toolchain with `make setup` on Linux or WSL2.
3. Make the smallest practical change and update documentation.
4. Run `make test`.
5. Run `make molecule` when Docker is available.
6. Describe risk, rollback, and test evidence in the pull request.

Use Conventional Commit-style subjects when useful, such as
`feat(ssh): add configurable allow-list`, but clear imperative English is more
important than a rigid format.

## Quality expectations

- Use fully qualified Ansible collection names.
- Put tunable values in `defaults/main.yml`.
- Use handlers for service reloads and restarts.
- Avoid `command` and `shell` for state changes when a module exists.
- Add a structural or Molecule assertion for new behavior.
- Never commit generated caches, real inventories, or secrets.
