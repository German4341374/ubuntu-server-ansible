# ADR 0001: Use small role-based server configuration

- Status: Accepted
- Date: 2026-07-13

## Context

A single playbook is easy to start but difficult to review, test, tag, and reuse.
Security changes also need clear ownership and safe handler boundaries.

## Decision

Each operational concern is a role with public defaults and focused tasks. The
site playbook orders roles so access exists before hardening and base packages
exist before dependent configuration. Tags allow targeted maintenance.

## Consequences

The repository contains more files, but changes are easier to review and test.
Role dependencies remain explicit in `playbooks/site.yml` rather than hidden in
role metadata.
