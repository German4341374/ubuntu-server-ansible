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

The Molecule scenario validates the timesync package and configuration but does
not start systemd-timesyncd. A container does not own the host clock, so the
service exits without capabilities that should not be granted to this test.
Real Ubuntu hosts keep the default `timesync_manage_service: true`.

## Consequences

The container test needs privileged Docker and depends on an upstream test image
that currently exposes only a moving `latest` tag. Vagrant is slower and requires
a hypervisor, but catches VM-specific behavior.
