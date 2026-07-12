# ADR 0003: Combine static checks, Molecule, and Vagrant

- Status: Accepted
- Date: 2026-07-13

## Context

Static checks are fast but cannot prove service behavior. Containers are fast
enough for CI, while a VM more closely matches a fresh Ubuntu Server.

## Decision

Use pytest, yamllint, ansible-lint, and syntax checks on every change. Use a
privileged systemd container with Molecule for convergence, idempotence, and
service assertions. Use Vagrant with a pinned Ubuntu box for the five-minute
local demonstration and final VM-level validation.

## Consequences

The container test needs privileged Docker and depends on an upstream test image
that currently exposes only a moving `latest` tag. Vagrant is slower and requires
a hypervisor, but catches VM-specific behavior.
